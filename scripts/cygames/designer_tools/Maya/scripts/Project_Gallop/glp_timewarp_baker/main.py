# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

import sys

import maya.cmds as cmds
import maya.mel as mel

import shiboken2

from PySide2 import QtWidgets
from maya import OpenMayaUI

from . import view

reload(view)


class Main(object):

    def __init__(self):
        """コンストラクタ
        """

        self.tool_name = 'GlpTimeWarpBaker'
        self.tool_version = '23011901'

        self.view = view.View()
        self.view.setWindowTitle(self.tool_name + self.tool_version)

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.setup_view_event()
        self.view.show()

    def setup_view_event(self):
        """UIのevent設定
        """

        self.view.ui.frame_adj_scene_button.clicked.connect(self.__frame_adj_scene_event)
        self.view.ui.frame_adj_max_key_button.clicked.connect(self.__frame_adj_max_key_event)
        self.view.ui.frame_adj_timewarp_button.clicked.connect(self.__frame_adj_timewarp_event)

        self.view.ui.bake_exe_button.clicked.connect(self.__bake_exe_event)

    def bake_timewarp(self, bake_attrs, start_frame, end_frame, should_merge_bake_result, should_del_timewarp):
        """タイムワープのベイク処理

        Args:
            bake_attrs ([str]): ベイクするアトリビュートのフルパスリスト
            start_frame (int): ベイク開始フレーム
            end_frame (int): ベイク終了フレーム
            should_merge_bake_result (bool): ベイクに使用したレイヤーをBaseAnimationにマージするか
            should_del_timewarp (bool): タイムワープノードを削除するか
        """

        self.__set_timewarp_state(True)

        active_anim_layers = self.__get_active_anim_layers()
        self.__select_anim_layers(active_anim_layers)

        # タイムワープをベイク
        cmds.bakeResults(
            bake_attrs,
            time=(start_frame, end_frame),
            simulation=True,
            shape=True,
            minimizeRotation=True,
            removeBakedAttributeFromLayer=False,
            removeBakedAnimFromLayer=False,
            bakeOnOverrideLayer=True,
            disableImplicitControl=False,
        )

        # ベイクが終わったらタイムワープを無効化
        self.__set_timewarp_state(False)

        # BaseAnimationに全てベイクして元レイヤーは削除
        if should_merge_bake_result:

            org_min = cmds.playbackOptions(q=True, min=True)
            org_anim_start = cmds.playbackOptions(q=True, ast=True)
            org_anim_end = cmds.playbackOptions(q=True, aet=True)
            org_max = cmds.playbackOptions(q=True, max=True)

            cmds.playbackOptions(min=start_frame)
            cmds.playbackOptions(ast=start_frame)
            cmds.playbackOptions(aet=end_frame)
            cmds.playbackOptions(max=end_frame)

            active_anim_layers = self.__get_active_anim_layers()
            self.__select_anim_layers(active_anim_layers)

            cmds.bakeResults(
                bake_attrs,
                time=(start_frame, end_frame),
                simulation=True,
                shape=True,
                minimizeRotation=True,
                removeBakedAttributeFromLayer=False,
                removeBakedAnimFromLayer=False,
                disableImplicitControl=False,
            )

            for anim_layer in self.__get_active_anim_layers():
                if anim_layer == 'BaseAnimation':
                    continue
                cmds.delete(anim_layer)
                container = anim_layer + 'Container'
                if cmds.objExists(container):
                    cmds.delete(container)

            cmds.playbackOptions(min=org_min)
            cmds.playbackOptions(ast=org_anim_start)
            cmds.playbackOptions(aet=org_anim_end)
            cmds.playbackOptions(max=org_max)

        # タイムワープノードの削除
        if should_del_timewarp:
            warp = self.__get_timewarp_node()
            if warp:
                cmds.delete(warp)

    def __bake_exe_event(self):
        """ベイク実行
        """

        # UI情報取得
        start_frame = self.view.ui.start_frame_box.value()
        end_frame = self.view.ui.end_frame_box.value()
        should_del_timewarp = self.view.ui.delete_timewarp_check.isChecked()
        should_merge_bake_result = self.view.ui.merge_bake_result_check.isChecked()

        if start_frame >= end_frame:
            cmds.confirmDialog(title='エラー', message='ベイク範囲が不適切です')
            return

        # ベイクアトリビュートの取得
        target_objs = self.__get_target_objs()
        bake_attrs = self.__get_all_keyed_attrs(target_objs)

        if not bake_attrs:
            cmds.confirmDialog(title='エラー', message='ベイク対象がありません')
            return

        # タイムワープノードの確認
        timewarp_node = self.__get_timewarp_node()
        if not timewarp_node:
            cmds.confirmDialog(title='エラー', message='ベイクするタイムワープがありません')
            return

        # ベイク範囲外のキーは保持されないので、範囲外のキーがある場合は実行確認
        if not self.__confirm_not_bake_keys(target_objs, timewarp_node, start_frame, end_frame):
            return

        # マージされるアニメーションレイヤーの確認
        if not self.__confirm_merge_anim_layers(should_merge_bake_result):
            return

        # タイムワープが有効になっていない場合の確認
        if not self.__confirm_enable_timewarp():
            return

        # 以降ベイク処理を行う
        cmds.undoInfo(openChunk=True)
        self.bake_timewarp(bake_attrs, start_frame, end_frame, should_merge_bake_result, should_del_timewarp)
        cmds.undoInfo(closeChunk=True)

    def __confirm_not_bake_keys(self, target_objs, timewarp_node, start_frame, end_frame):
        """ベイクされないキーに対する確認

        Args:
            target_objs ([str]): 対象オブジェクトリスト
            timewarp_node (str): タイムワープノード
            start_frame (int): ベイク開始フレーム
            end_frame (int): ベイク終了フレーム

        Returns:
            bool: ユーザーの確認結果
        """

        bake_raw_start = cmds.getAttr('{}.output'.format(timewarp_node), t=start_frame)
        bake_raw_end = cmds.getAttr('{}.output'.format(timewarp_node), t=end_frame)
        keyframes = sorted(cmds.keyframe(target_objs, query=True))

        if keyframes[0] < bake_raw_start or keyframes[-1] > bake_raw_end:
            msg = 'ベイク範囲(=タイムワープ適用前 {}f-{}f)外にキーが打たれています'.format(str(int(bake_raw_start)), str(int(bake_raw_end)))
            msg += '\n範囲外のキーはベイクされません。ベイクを続行しますか？'
            result = cmds.confirmDialog(title='ベイクされないキーの確認',
                                        message=msg,
                                        button=['ベイク続行', 'ベイク中止'],
                                        defaultButton='ベイク続行',
                                        cancelButton='ベイク中止',
                                        dismissString='ベイク中止')
            if result == 'ベイク中止':
                return False

        return True

    def __confirm_merge_anim_layers(self, should_merge_bake_result):
        """ベイクに使用したアニメーションレイヤーのマージ確認

        Args:
            should_merge_bake_result (bool): ベイクに使用したアニメーションレイヤー一式をマージするか

        Returns:
            bool: ユーザーの確認結果
        """

        if len(self.__get_active_anim_layers()) > 1 and should_merge_bake_result:
            msg = '現在ミュートされていないレイヤーは全てBaseAnimationにマージされます。'
            msg += '\nマージしたくない場合は「ベイクに使用した全レイヤーをBaseAnimationにマージ」のチェックを外して下さい。'
            msg += 'この設定のままベイクを続行しますか？'
            result = cmds.confirmDialog(title='アニメーションレイヤーのマージ確認',
                                        message=msg,
                                        button=['ベイク続行', 'ベイク中止'],
                                        defaultButton='ベイク続行',
                                        cancelButton='ベイク中止',
                                        dismissString='ベイク中止')
            if result == 'ベイク中止':
                return False

        return True

    def __confirm_enable_timewarp(self):
        """ベイク前にタイムワープを有効化することの確認

        Returns:
            bool: ユーザーの確認結果
        """

        if not self.__get_timewarp_state():
            result = cmds.confirmDialog(title='タイムワープの有効化確認',
                                        message='タイムワープが無効になっています。ベイク前に有効化します。',
                                        button=['有効化', 'ベイク中止'],
                                        defaultButton='有効化',
                                        cancelButton='ベイク中止',
                                        dismissString='ベイク中止')
            if result == '有効化':
                return True
            elif result == 'ベイク中止':
                return False

        return True

    def __frame_adj_scene_event(self):
        """frame_adj_scene_buttonイベント
        """

        start = cmds.playbackOptions(q=True, ast=True)
        end = cmds.playbackOptions(q=True, aet=True)
        self.__set_frame(start, end)

    def __frame_adj_max_key_event(self):
        """frame_adj_max_key_buttonイベント
        """

        target_objs = self.__get_target_objs()

        if not target_objs:
            cmds.confirmDialog(title='エラー', message='対象オブジェクトがみつかりません')
            return

        keyframes = self.__get_all_key_times(target_objs)

        if not keyframes:
            cmds.confirmDialog(title='エラー', message='オブジェクトにキーフレームが打たれていません')
            return

        keyframes.sort()
        self.__set_frame(keyframes[0], keyframes[-1])

    def __frame_adj_timewarp_event(self):
        """frame_adj_timewarp_buttonイベント
        """

        warp = self.__get_timewarp_node()

        if not warp:
            cmds.confirmDialog(title='エラー', message='タイムワープが存在しません')
            return

        frames = cmds.keyframe(warp, query=True)

        self.__set_frame(frames[0], frames[-1])

    def __set_frame(self, start, end):
        """ベイクフレームをセット

        Args:
            start (int): 開始フレーム
            end (int): 終了フレーム
        """

        self.view.ui.start_frame_box.setValue(start)
        self.view.ui.end_frame_box.setValue(end)

    def __get_target_objs(self):
        """UIの設定から対象オブジェクトのリストを取得

        Returns:
            [str]: 対象オブジェクトのリスト
        """

        target_objs = []

        if self.view.ui.selection_only_radio.isChecked():

            selections = cmds.ls(sl=True, l=True, fl=True)
            if selections:
                target_objs = selections

        elif self.view.ui.all_descendents_radio.isChecked():

            selections = cmds.ls(sl=True, l=True, fl=True)
            if selections:
                target_objs = selections
                descendent_objs = cmds.listRelatives(selections, ad=True, s=False, ni=True, f=True)
                if descendent_objs:
                    target_objs.extend(descendent_objs)

        elif self.view.ui.all_keyed_radio.isChecked():

            all_objs = cmds.ls('*', r=True, dag=True)

            for obj in all_objs:
                if self.__get_all_key_times([obj]):
                    target_objs.append(obj)

        return target_objs

    def __get_all_keyed_attrs(self, target_objs):
        """キーが打たれている全アトリビュートを取得
        全アクティブなアニメーションレイヤーのどこかに打たれている場合もヒットする

        Args:
            target_objs ([str]): 対象オブジェクトリスト

        Returns:
            [str]: 各アトリビュートへのフルパス
        """

        if not target_objs:
            return []

        result_attrs = []
        current_anim_layer = self.__get_selected_anim_layer()
        anim_layers = self.__get_active_anim_layers()

        if anim_layers:
            for layer in anim_layers:
                self.__select_anim_layer_on_editor(layer)
                result_attrs.extend(self.__get_current_all_keyed_attrs(target_objs))

            if current_anim_layer:
                self.__select_anim_layer_on_editor(current_anim_layer)

        else:
            result_attrs = self.__get_current_all_keyed_attrs(target_objs)

        return result_attrs

    def __get_current_all_keyed_attrs(self, objs):
        """現在のアニメーションレイヤーの状態でキーが打たれている全アトリビュートを取得

        Args:
            objs ([str]): 対象オブジェクトリスト

        Returns:
            [str]: 各アトリビュートへのフルパス
        """

        if not objs:
            return []

        result_attrs = []
        for obj in objs:
            for attr in cmds.listAttr(obj, keyable=True):
                attr_full_path = '{}.{}'.format(obj, attr)
                if cmds.keyframe(obj, q=True, at=attr, kc=True) and attr_full_path not in result_attrs:
                    result_attrs.append(attr_full_path)

        return result_attrs

    def __get_all_key_times(self, target_objs):
        """キーが打たれているタイムのリストを取得

        Args:
            target_obj ([str]): 対象オブジェクトリスト

        Returns:
            [int]: キーが打たれているtimeのリスト
        """

        current_anim_layer = self.__get_selected_anim_layer()
        anim_layers = self.__get_active_anim_layers()

        all_key_times = []

        if anim_layers:
            for layer in anim_layers:
                self.__select_anim_layer_on_editor(layer)
                for obj in target_objs:
                    key_times = cmds.keyframe(obj, q=True)
                    if key_times:
                        all_key_times.extend(key_times)

            if current_anim_layer:
                self.__select_anim_layer_on_editor(current_anim_layer)

        else:
            for obj in target_objs:
                key_times = cmds.keyframe(obj, q=True)
                if key_times:
                    all_key_times.extend(key_times)

        return sorted(list(set(all_key_times)))

    def __get_timewarp_node(self):
        """タイムワープノード取得

        Returns:
            str: タイムワープノード
        """

        warps = cmds.ls('timewarp', type='animCurveTT')
        if warps:
            return warps[0]
        else:
            return None

    def __get_timewarp_state(self):
        """タイムワープノードの有効無効取得

        Returns:
            bool: 有効/無効
        """

        warp = self.__get_timewarp_node()

        if not warp:
            return False

        times = cmds.listConnections(warp, type='time')

        if times:
            return cmds.getAttr('{}.{}'.format(times[0], 'enableTimewarp'))

    def __set_timewarp_state(self, state):
        """タイムワープノードの有効無効切り替え

        Args:
            state (bool): 有効/無効
        """

        warp = self.__get_timewarp_node()

        if not warp:
            return

        times = cmds.listConnections(warp, type='time')

        if times:
            cmds.setAttr('{}.{}'.format(times[0], 'enableTimewarp'), state)

    def __select_anim_layer_on_editor(self, anim_layer):
        """アニメーションレイヤーをエディタ上で選択する

        Args:
            anim_layer (str): 選択するアニメーションレイヤー名
        """

        anim_layers = cmds.ls(type='animLayer')

        if not anim_layers:
            return

        for layer in anim_layers:
            if layer == anim_layer:
                mel.eval('animLayerEditorOnSelect "{}" 1'.format(layer))
            else:
                mel.eval('animLayerEditorOnSelect "{}" 0'.format(layer))

    def __select_anim_layers(self, target_anim_layers):
        """アニメーションレイヤーを選択

        Args:
            target_anim_layers ([str]): 選択するアニメーションレイヤーリスト
        """

        all_anim_layers = cmds.ls(type='animLayer')

        for anim_layer in all_anim_layers:
            if anim_layer == 'BaseAnimation':
                continue
            if anim_layer in target_anim_layers:
                cmds.animLayer(anim_layer, e=True, selected=True)
            else:
                cmds.animLayer(anim_layer, e=True, selected=False)

    def __get_selected_anim_layer(self):
        """選択状態のアニメーションレイヤーを取得

        Returns:
            str: 選択されているアニメーションレイヤー
        """

        anim_layers = cmds.ls(type='animLayer')

        if not anim_layers:
            return

        for layer in anim_layers:
            if cmds.animLayer(layer, q=True, selected=True):
                return layer

    def __get_active_anim_layers(self):
        """ミュートされていないアニメーションレイヤーのリストを取得

        Returns:
            [str]: ミュートされていないアニメーションレイヤーのリスト
        """

        anim_layers = cmds.ls(type='animLayer')

        if not anim_layers:
            return []

        active_layers = []
        for layer in anim_layers:
            if not cmds.animLayer(layer, q=True, mute=True):
                active_layers.append(layer)

        return active_layers
