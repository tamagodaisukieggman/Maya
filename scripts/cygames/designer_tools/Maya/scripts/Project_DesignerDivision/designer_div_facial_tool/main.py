# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from collections import OrderedDict
from PySide2.QtWidgets import QMessageBox

import maya.cmds as cmds

from . import view
from .models import facial_rig_head_attach, facial_target_export, ear_target_export, eye_controller_creator, util, blend_shape_target_export, target_info

try:
    from importlib import reload
    from builtins import range
    from builtins import object
except Exception:
    pass

reload(view)
reload(facial_rig_head_attach)
reload(facial_target_export)
reload(ear_target_export)
reload(eye_controller_creator)
reload(util)
reload(blend_shape_target_export)
reload(target_info)

# TOOL名
TOOL_NAME = 'cdt_facial_tools'
MODULE_NAME = 'Project_DesignerDivision.designer_div_facial_tool.main'


def batch():

    settings = util.load_setting(TOOL_NAME)
    func = settings.get('func')
    if not func:
        return

    # 実行
    try:
        exec('Main().{}({})'.format(func, settings))
    except Exception:
        pass


class Main(object):

    def __init__(self):

        self.view = None

        # UI操作用のtarget_info
        self.facial_target_info = None
        self.ear_target_info = None

        self.facial_now_frame = 0
        self.facial_prev_frame = 0

        self.ear_now_frame = 0
        self.ear_prev_frame = 0

        self.facial_part_dict = OrderedDict((['眉', 'Eyebrow_'], ['目', 'Eye_'], ['口', 'Mouth']))
        self.ear_part_dict = {'耳': 'Ear_'}

    def show_ui(self):
        """UI表示
        """

        self.view = view.View()

        if not self.__create_facial_target_info():
            return

        if not self.__create_ear_target_info():
            return

        self.__setup_event()

        self.__setup_check_facial_button()

        self.__setup_check_ear_button()

        self.view.show()

    def __create_facial_target_info(self):
        """フェイシャルアニメーション一覧を作成する

        Returns:
            bool: 作成に成功したか
        """

        self.facial_target_info = target_info.TargetInfo()
        self.facial_target_info.create_info_from_csv('facial_target_info')

        return self.facial_target_info.is_created

    def __create_ear_target_info(self):
        """耳アニメーション一覧を作成する

        Returns:
            bool: 作成に成功したか
        """

        self.ear_target_info = target_info.TargetInfo()
        self.ear_target_info.create_info_from_csv('ear_target_info')

        return self.ear_target_info.is_created

    def __setup_event(self):
        """PySide UI側のボタンのクリック時イベントを設定する
        """

        # headリグ周り
        self.view.ui.exec_attach_head_rig_btn.clicked.connect(lambda: self.__exec_attach_head_rig_btn_event())
        self.view.ui.exec_detach_head_rig_btn.clicked.connect(lambda: self.__exec_detach_head_rig_btn_event())
        self.view.ui.exec_reset_head_rig_controller_btn.clicked.connect(lambda: self.__exec_reset_head_rig_controller_btn_event())
        self.view.ui.exec_edit_eye_highlight_rig_btn.clicked.connect(lambda: self.__exec_edit_eye_highlight_rig_btn())

        # facialチェックの戻る・進む
        self.view.ui.exec_next_eyebrow_btn.clicked.connect(lambda x=self.facial_target_info, y='Eyebrow_L': self.__next_facial_button_event(x, y, False, True))
        self.view.ui.exec_prev_eyebrow_btn.clicked.connect(lambda x=self.facial_target_info, y='Eyebrow_L': self.__prev_facial_button_event(x, y, False, True))
        self.view.ui.exec_next_eye_btn.clicked.connect(lambda x=self.facial_target_info, y='Eye_L': self.__next_facial_button_event(x, y, False, True))
        self.view.ui.exec_prev_eye_btn.clicked.connect(lambda x=self.facial_target_info, y='Eye_L': self.__prev_facial_button_event(x, y, False, True))
        self.view.ui.exec_next_mouth_btn.clicked.connect(lambda x=self.facial_target_info, y='Mouth': self.__next_facial_button_event(x, y, False, True))
        self.view.ui.exec_prev_mouth_btn.clicked.connect(lambda x=self.facial_target_info, y='Mouth': self.__prev_facial_button_event(x, y, False, True))
        self.view.ui.exec_reset_animation_layer_btn.clicked.connect(lambda x=self.facial_target_info.info_item_list: self.__reset_facial_animation_layer_event(x))
        self.view.ui.exec_back_facial_btn.clicked.connect(lambda x=self.facial_target_info: self.__back_facial_button_event(x, True))
        self.view.ui.exec_all_next_facial_btn.clicked.connect(lambda x=self.facial_target_info, y='Eyebrow_L': self.__next_facial_button_event(x, y, True, True))
        self.view.ui.exec_all_prev_facial_btn.clicked.connect(lambda x=self.facial_target_info, y='Eyebrow_L': self.__prev_facial_button_event(x, y, True, True))

        # earチェックの戻る・進む
        self.view.ui.exec_next_ear_btn.clicked.connect(lambda x=self.ear_target_info, y='Ear_L': self.__next_facial_button_event(x, y, False, False))
        self.view.ui.exec_prev_ear_btn.clicked.connect(lambda x=self.ear_target_info, y='Ear_L': self.__prev_facial_button_event(x, y, False, False))
        self.view.ui.exec_reset_ear_animation_layer_btn.clicked.connect(lambda x=self.ear_target_info.info_item_list: self.__reset_facial_animation_layer_event(x))
        self.view.ui.exec_back_ear_btn.clicked.connect(lambda x=self.ear_target_info: self.__back_facial_button_event(x, False))
        self.view.ui.exec_all_next_ear_btn.clicked.connect(lambda x=self.ear_target_info, y='Ear_L': self.__next_facial_button_event(x, y, True, False))
        self.view.ui.exec_all_prev_ear_btn.clicked.connect(lambda x=self.ear_target_info, y='Ear_L': self.__prev_facial_button_event(x, y, True, False))

        # facial_target/ear_targetの出力
        self.view.ui.exec_export_facial_target_btn.clicked.connect(lambda: self.__exec_export_facial_target_btn_event())
        self.view.ui.exec_export_ear_target_btn.clicked.connect(lambda: self.__exec_export_ear_target_event())

        # facial_blend_targetの出力
        self.view.ui.exec_export_facial_blend_target_btn.clicked.connect(lambda: self.__exec_export_facial_blend_target_btn_event())

    def __setup_check_facial_button(self):
        """フェイシャル確認部分のボタンを配置する
        """

        # 状態のリセット
        self.view.reset_facial_check_button()

        # 眉のボタンセット
        self.__create_part_button(
            self.view.ui.eyebrow_check_top_layout,
            self.view.ui.eyebrow_check_mid_layout,
            self.facial_target_info,
            'Eyebrow_L', True)

        # 目のボタンセット
        self.__create_part_button(
            self.view.ui.eye_check_top_layout,
            self.view.ui.eye_check_mid_layout,
            self.facial_target_info,
            'Eye_L', True)

        # 口のボタンセット
        self.__create_part_button(
            self.view.ui.mouth_check_top_layout,
            self.view.ui.mouth_check_mid_layout,
            self.facial_target_info,
            'Mouth', True)

    def __setup_check_ear_button(self):
        """耳確認部分のボタンを配置する
        """

        # 状態のリセット
        self.view.reset_ear_check_button()

        # 耳のボタンセット
        self.__create_part_button(
            self.view.ui.ear_check_top_layout,
            self.view.ui.ear_check_mid_layout,
            self.ear_target_info, 'Ear_L', False)

    def __create_part_button(self, top_layout, mid_layout, target_info, part, is_facial_part):
        """各フェイシャル・耳アニメーションの確認ボタンUIを作成する

        Args:
            top_layout (PySide2.QtWidgets.QVBoxLayout): 確認ボタンの上部レイアウト(vartical Layout)
            mid_layout (PySide2.QtWidgets.QVBoxLayout): 確認ボタンの中段レイアウト(vartical Layout)
            target_info (TargetInfo): 対象のアニメーション一覧が保存されているclass object
            part (String): ボタンの設置対象部位(part)
        """

        target_part_top_button_info_list = []
        target_part_mid_button_info_list = []

        # 対象のpartのボタンリストを作成する
        for i in range(len(target_info.info_item_list)):

            target_info_item = target_info.info_item_list[i]

            if part != target_info_item.part:
                continue

            label = target_info_item.label

            # アニメーションレイヤーが付随しているレイヤーは中段レイアウトに格納する
            if target_info_item.animation_layer_name:
                if label not in [eyebrow_button_info.label for eyebrow_button_info in target_part_mid_button_info_list]:
                    target_part_mid_button_info_list.append(target_info_item)
            else:
                if label not in [eyebrow_button_info.label for eyebrow_button_info in target_part_top_button_info_list]:
                    target_part_top_button_info_list.append(target_info_item)

        if not target_part_mid_button_info_list and not target_part_top_button_info_list:
            return

        # frame順にsortする(CSVで既にSortされているハズだが一応)
        target_part_top_button_info_list = sorted(target_part_top_button_info_list, key=lambda x: x.frame)
        target_part_mid_button_info_list = sorted(target_part_mid_button_info_list, key=lambda x: x.frame)

        # 横に並べて配置するボタンの限界数
        vartical_max_count = view.CHECK_BUTTON_LAYOUT_VARTICAL_ITEM_MAX_COUNT

        # ボタン押下時に実行するfunction
        func = self.__check_button_event

        # 上段・中段それぞれのボタン作成
        for i in range(0, len(target_part_top_button_info_list), vartical_max_count):
            self.view.create_check_button_layout(top_layout, target_part_top_button_info_list[i: i + vartical_max_count], func, target_info, is_facial_part)

        # ボタン押下時に実行するfunction
        func = self.__check_animation_button_event

        for i in range(0, len(target_part_mid_button_info_list), vartical_max_count):
            self.view.create_check_button_layout(mid_layout, target_part_mid_button_info_list[i: i + vartical_max_count], func)

    def __next_facial_button_event(self, target_info, target_part, target_all_part=False, is_facial_part=True):
        """指定した部位のアニメーションを次のフレーム(アニメーションレイヤーが付いているフレームを除く)に移動する
        最後のフレームから戻るときは一番最初のフレームにループする

        Args:
            target_info (TargetInfo): 対象のアニメーション一覧が保存されているclass object
            target_part (String): 対象の部位(part)
            target_all_part (bool): target_infoの全てのパートを対象にするか
            is_facial_part (bool): フェイシャルかどうか。elseで耳判定
        """

        now_frame = None
        if is_facial_part:
            now_frame = self.facial_now_frame
        else:
            now_frame = self.ear_now_frame

        next_frame = None
        start_frame = None
        for info_item in target_info.info_item_list:

            if target_all_part is False and info_item.part != target_part:
                continue

            if info_item.animation_layer_name:
                continue

            if now_frame < info_item.frame:
                if next_frame is None:
                    next_frame = info_item.frame
                elif info_item.frame < next_frame:
                    next_frame = info_item.frame

            if start_frame is None:
                start_frame = info_item.frame
            elif start_frame > info_item.frame:
                start_frame = info_item.frame

        # 次のフレームがヒットしなかったときは一番最初のフレームをセット
        if next_frame is None:
            next_frame = start_frame

        cmds.currentTime(next_frame)

        if is_facial_part:
            self.facial_now_frame = next_frame
            self.facial_prev_frame = now_frame
        else:
            self.ear_now_frame = next_frame
            self.ear_prev_frame = now_frame

        self.__update_facial_list_ui(target_info, is_facial_part)

    def __prev_facial_button_event(self, target_info, target_part, target_all_part=False, is_facial_part=True):
        """指定した部位のアニメーションを前のフレーム(アニメーションレイヤーが付いているフレームを除く)に移動する
        最初のフレームから戻るときは一番最後のフレームにループする

        Args:
            target_info (TargetInfo): 対象のアニメーション一覧が保存されているclass object
            target_part (String)): 対象の部位(part)
            target_all_part (bool): target_infoの全てのパートを対象にするか
            is_facial_part (bool): フェイシャルかどうか。elseで耳判定
        """

        now_frame = None
        if is_facial_part:
            now_frame = self.facial_now_frame
        else:
            now_frame = self.ear_now_frame

        prev_frame = None
        end_frame = None
        for info_item in target_info.info_item_list:

            if target_all_part is False and info_item.part != target_part:
                continue

            if info_item.animation_layer_name:
                continue

            if now_frame > info_item.frame:
                if prev_frame is None:
                    prev_frame = info_item.frame
                elif info_item.frame > prev_frame:
                    prev_frame = info_item.frame

            if end_frame is None:
                end_frame = info_item.frame
            elif end_frame < info_item.frame:
                end_frame = info_item.frame

        # 前のフレームがヒットしなかったときは一番最後のフレームをセット
        if prev_frame is None:
            prev_frame = end_frame

        cmds.currentTime(prev_frame)

        if is_facial_part:
            self.facial_now_frame = prev_frame
            self.facial_prev_frame = now_frame
        else:
            self.ear_now_frame = prev_frame
            self.ear_prev_frame = now_frame

        self.__update_facial_list_ui(target_info, is_facial_part)

    def __check_button_event(self, target_info_item, target_info, is_facial_part=True):
        """フェイシャル・耳チェックボタン押下時のイベント

        Args:
            target_info_item (TargetItemInfo): 対象のアニメーション情報が保存されているclass object
            target_info (TargetInfo)): 対象のアニメーション一覧が保存されているclass object
            is_facial_part (bool): フェイシャルかどうか。elseで耳判定
        """

        frame = target_info_item.frame
        if frame is not None:

            cmds.currentTime(frame)

            if is_facial_part:
                self.facial_prev_frame = self.facial_now_frame
                self.facial_now_frame = frame
            else:
                self.ear_prev_frame = self.ear_now_frame
                self.ear_now_frame = frame

            self.__update_facial_list_ui(target_info, is_facial_part)

    def __check_animation_button_event(self, target_info_item):
        """animationLayerがある表情チェックボタン押下時のイベント

        Args:
            target_info_item (TargetItemInfo): 対象のアニメーション情報が保存されているclass object
        """

        animation_layer_name = target_info_item.animation_layer_name

        if not cmds.animLayer(animation_layer_name, q=True, exists=True):
            return

        this_weight = cmds.animLayer(animation_layer_name, q=True, weight=True)

        this_weight += 1.0

        if this_weight > 1:
            this_weight = 0

        this_weight = cmds.animLayer(animation_layer_name, e=True, weight=this_weight, mute=False)

    def __back_facial_button_event(self, target_info, is_facial_part=True):
        """一つ前の表情に戻るボタン押下時のイベント

        Args:
            target_info (TargetInfo)): 対象のアニメーション一覧が保存されているclass object
            is_facial_part (bool): フェイシャルかどうか。elseで耳判定
        """

        target_list_label = None
        if is_facial_part:
            target_list_label = self.view.ui.prev_facial_list_count_label.text()
        else:
            target_list_label = self.view.ui.prev_ear_list_count_label.text()

        match_obj = re.search(r'\(([0-9]{1,})\)', target_list_label)
        if not match_obj:
            return

        frame = int(match_obj.group(1))
        cmds.currentTime(frame)
        if is_facial_part:
            self.facial_prev_frame = self.facial_now_frame
            self.facial_now_frame = frame
        else:
            self.ear_prev_frame = self.ear_now_frame
            self.ear_now_frame = frame

        self.__update_facial_list_ui(target_info, is_facial_part)

    def __reset_facial_animation_layer_event(self, info_item_list):
        """アニメーションレイヤーのリセットボタン押下時のイベント

        Args:
            info_item_list (list): target_info_itemのリスト
        """

        for info_item in info_item_list:

            if not info_item.animation_layer_name:
                continue

            if not cmds.animLayer(info_item.animation_layer_name, q=True, exists=True):
                return

            cmds.animLayer(info_item.animation_layer_name, e=True, weight=0.0, mute=False)

    def __update_facial_list_ui(self, target_info, is_facial_part=True):
        """UIの「1つ前の表情」、「現在の表情」リストを更新する

        Args:
            target_info (_type_): 対象のアニメーション一覧が保存されているclass object
            is_facial_part (bool, optional): フェイシャルかどうか。elseで耳判定
        """

        now_frame = self.facial_now_frame
        prev_frame = self.facial_prev_frame
        prev_label_ui = self.view.ui.prev_facial_list_count_label
        prev_list_edit_ui = self.view.ui.prev_facial_list_edit
        now_label_ui = self.view.ui.now_facial_list_count_label
        now_list_edit_ui = self.view.ui.now_facial_list_edit
        target_part_dict = self.facial_part_dict

        if not is_facial_part:
            target_part_dict = self.ear_part_dict
            prev_label_ui = self.view.ui.prev_ear_list_count_label
            prev_list_edit_ui = self.view.ui.prev_ear_list_edit
            now_label_ui = self.view.ui.now_ear_list_count_label
            now_list_edit_ui = self.view.ui.now_ear_list_edit
            now_frame = self.ear_now_frame
            prev_frame = self.ear_prev_frame

        prev_frame_msg = 'Frame ({})'.format(prev_frame)
        now_frame_msg = 'Frame ({})'.format(now_frame)

        now_msg = ''
        for key, value in list(target_part_dict.items()):
            for target_info_item in target_info.info_item_list:
                if (target_info_item.frame == now_frame) and (target_info_item.part.startswith(value)):
                    now_msg += '{}: {}\n'.format(key, target_info_item.label)
                    break
            else:
                now_msg += '{}: -\n'.format(key)

        prev_label_ui.setText(prev_frame_msg)
        now_label_ui.setText(now_frame_msg)

        prev_list_edit_ui.setPlainText(now_list_edit_ui.toPlainText())
        now_list_edit_ui.setPlainText(now_msg)

    def __exec_attach_head_rig_btn_event(self):
        """headリグのアタッチボタン押下時のイベント
        """

        if QMessageBox.information(None, '確認', 'Rig_headとジョイントをデタッチしますか？', QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()
        rig_attach.attach_rig()

        QMessageBox.information(None, '完了', '処理が完了しました')

    def __exec_detach_head_rig_btn_event(self):
        """headリグのデタッチボタン押下時のイベント
        """

        if QMessageBox.information(None, '確認', 'Rig_headとジョイントをデタッチしますか？', QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()
        rig_attach.detach_rig()

        QMessageBox.information(None, '完了', '処理が完了しました')

    def __exec_reset_head_rig_controller_btn_event(self):

        if QMessageBox.information(None, '確認', 'Rig_headのコントローラーをリセットしますか？', QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()
        rig_attach.reset_rig()

        QMessageBox.information(None, '完了', '処理が完了しました')

    def __exec_edit_eye_highlight_rig_btn(self):

        if QMessageBox.information(None, '確認', '目のハイライトリグを作成しますか？', QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        controller_creator = eye_controller_creator.EyeControllerCreator()
        controller_creator.create()

        QMessageBox.information(None, '完了', '処理が完了しました')

    def __exec_export_facial_target_btn_event(self):
        """facial_targetエクスポートボタン押下時のイベント
        """

        if QMessageBox.information(None, '確認', 'facial_target.fbxを出力しますか？', QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        scene_file_path = cmds.file(q=True, sn=True)

        settings = {
            'func': 'exec_batch_export_facial_target',
            'target_file_path_list': [scene_file_path]
        }

        if not util.save_setting(TOOL_NAME, settings):
            QMessageBox.information(None, '情報', 'Setting情報が保存できませんでした')
            return

        util.batch_exec(MODULE_NAME, 'batch()')

    def __exec_export_ear_target_event(self):
        """ear_targetエクスポートボタン押下時のイベント
        """

        if QMessageBox.information(None, '確認', 'ear_target.fbxを出力しますか？', QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        scene_file_path = cmds.file(q=True, sn=True)

        settings = {
            'func': 'exec_batch_export_ear_target',
            'target_file_path_list': [scene_file_path]
        }

        if not util.save_setting(TOOL_NAME, settings):
            QMessageBox.information(None, '情報', 'Setting情報が保存できませんでした')
            return

        util.batch_exec(MODULE_NAME, 'batch()')

    def __exec_export_facial_blend_target_btn_event(self):
        """facial_blend_targetエクスポートボタンの押下時のイベント
        """

        if QMessageBox.information(None, '確認', 'facial_blend_target.ma/fbxを出力しますか？', QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
            return

        scene_file_path = cmds.file(q=True, sn=True)

        settings = {
            'func': 'exec_batch_export_facial_blend_target',
            'target_file_path_list': [scene_file_path]
        }

        if not util.save_setting(TOOL_NAME, settings):
            QMessageBox.information(None, '情報', 'Setting情報が保存できませんでした')
            return

        util.batch_exec(MODULE_NAME, 'batch()')

    def exec_batch_export_facial_target(self, settings):
        """facial_targetエクスポートの実行関数

        Args:
            settings (dict): 出力時設定情報
        """

        target_file_path_list = settings.get('target_file_path_list')
        if not target_file_path_list:
            return

        for target_file_path in target_file_path_list:
            facial_target_export_obj = facial_target_export.FacialTargetExport()
            facial_target_export_obj.export(target_file_path)

    def exec_batch_export_ear_target(self, settings):
        """ear_targetエクスポートの実行関数

        Args:
            settings (dict): 出力時設定情報
        """

        target_file_path_list = settings.get('target_file_path_list')
        if not target_file_path_list:
            return

        for target_file_path in target_file_path_list:
            facial_target_export_obj = ear_target_export.EarTargetExport()
            facial_target_export_obj.export(target_file_path)

    def exec_batch_export_facial_blend_target(self, settings):
        """facial_blend_targetエクスポートの実行関数

        Args:
            settings (dict): 出力時設定情報
        """

        target_file_path_list = settings.get('target_file_path_list')
        if not target_file_path_list:
            return

        for target_file_path in target_file_path_list:
            blend_shape_target_export_obj = blend_shape_target_export.BlendShapeTargetExport()
            blend_shape_target_export_obj.export(target_file_path, 'M_Face', 'M_Hair')
