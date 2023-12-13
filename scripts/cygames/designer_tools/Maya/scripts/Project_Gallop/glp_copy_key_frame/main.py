# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
import shiboken2
import maya.cmds as cmds

from PySide2 import QtWidgets
from maya import OpenMayaUI
from . import view

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(view)


class Main(object):

    def __init__(self):
        """
        """

        self.tool_name = 'GlpCopyKeyFrame'
        self.tool_version = '23110701'

        self.view = view.View()
        self.view.setWindowTitle(self.tool_name + self.tool_version)
        self.__progress_window = None

        self.src_objs = []

    def show_progress_bar(self, min, max):
        """プログレスバーを表示

        Args:
            min (int): 最小値
            max (int): 最大値

        Returns:
            str: 作成したプログレスバーコントロールへのパス
        """

        if self.__progress_window:
            self.delete_progress_bar()
            self.__progress_window = None

        self.__progress_window = cmds.window(t='progress', tb=False)
        layout = cmds.columnLayout(p=self.__progress_window)
        progress_ctrl = cmds.progressBar(min=min, max=max, width=300, p=layout)
        cmds.showWindow(self.__progress_window)

        return progress_ctrl

    def delete_progress_bar(self):
        """プログレスバーを閉じる
        """

        if self.__progress_window and cmds.window(self.__progress_window, ex=True):
            cmds.deleteUI(self.__progress_window)

        self.__progress_window = None

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)
        self.initialize_ui()
        self.setup_view_event()
        self.view.show()

    def initialize_ui(self):
        """UI初期化
        """

        self.view.ui.select_hierarchy_check.setChecked(True)
        self.update_range_ui_enable()
        self.update_src_info_label()

    def setup_view_event(self):
        """UIのevent設定
        """

        ui = self.view.ui

        ui.use_frame_range_check.stateChanged.connect(self.update_range_ui_enable)
        ui.set_source_obj_button.clicked.connect(self.set_source_button_event)
        ui.key_frame_copy_button.clicked.connect(self.copy_button_event)
        ui.start_frame_spin.editingFinished.connect(self.set_time_range_event)
        ui.end_frame_spin.editingFinished.connect(self.set_time_range_event)
        ui.set_range_from_timeline_button.clicked.connect(self.set_time_range_from_scene_event)

    def update_range_ui_enable(self):
        """範囲指定UIの有効/無効を更新
        """

        ui = self.view.ui
        is_enabled = ui.use_frame_range_check.isChecked()
        ui.start_range_label.setEnabled(is_enabled)
        ui.start_frame_spin.setEnabled(is_enabled)
        ui.end_range_label.setEnabled(is_enabled)
        ui.end_frame_spin.setEnabled(is_enabled)
        ui.set_range_from_timeline_button.setEnabled(is_enabled)

    def set_source_button_event(self):
        """ソース指定ボタンイベント
        """

        self.src_objs = cmds.ls(sl=True, typ='transform', l=True, fl=True)

        if self.src_objs and self.view.ui.select_hierarchy_check.isChecked():
            all_children = cmds.listRelatives(self.src_objs, ad=True, f=True, type='transform')
            if all_children:
                self.src_objs.extend(all_children)

        self.update_src_info_label()

    def update_src_info_label(self):
        """ソース情報を更新
        """

        src_len = 0
        if self.src_objs:
            src_len = len(self.src_objs)

        ui = self.view.ui
        if src_len == 0:
            ui.src_info_label.setText('ソースが指定されていません')
        else:
            ui.src_info_label.setText('{} オブジェクトをソースに指定しています'.format(str(src_len)))

    def set_time_range_event(self):
        """範囲指定更新イベント
        """

        ui = self.view.ui

        if ui.start_frame_spin.value() < 0:
            ui.start_frame_spin.setValue(0)

        if ui.end_frame_spin.value() < ui.start_frame_spin.value():
            ui.end_frame_spin.setValue(ui.start_frame_spin.value())

    def set_time_range_from_scene_event(self):
        """タイムラインから範囲指定イベント
        """

        ui = self.view.ui

        start = cmds.playbackOptions(q=True, minTime=True)
        end = cmds.playbackOptions(q=True, maxTime=True)
        ui.start_frame_spin.setValue(start)
        ui.end_frame_spin.setValue(end)

    def get_time_range(self):
        """範囲を取得

        Returns:
            [int, int]: 開始フレーム、終了フレームのリスト
        """

        ui = self.view.ui

        if not ui.use_frame_range_check.isChecked():
            return

        start = ui.start_frame_spin.value()
        end = ui.end_frame_spin.value()
        return [start, end]

    def copy_button_event(self):
        """コピーボタンイベント
        """

        if not self.src_objs:
            cmds.confirmDialog(m='ソースが指定されていません')
            return

        sels = cmds.ls(sl=True, typ='transform', l=True, fl=True)

        if not sels:
            cmds.confirmDialog(m='コピー対象が選択されていません')
            return

        if self.view.ui.select_hierarchy_check.isChecked():
            all_children = cmds.listRelatives(sels, ad=True, f=True, type='transform')
            if all_children:
                sels.extend(all_children)

        self.copy_key_frames_by_name(self.src_objs, sels)

    def copy_key_frames_by_name(self, srcs, targets):
        """ショートネーム一致でキーフレームをコピー

        Args:
            srcs (list): ソースリスト
            targets (list): ターゲットリスト
        """

        # 対応するコピー元とコピー先のリストを作成
        copy_srcs = []
        copy_dsts = []

        for src in srcs:

            if not cmds.keyframe(src, q=True):
                continue

            src_short_name = src.split('|')[-1].split(':')[-1]

            for target in targets:

                target_short_name = target.split('|')[-1].split(':')[-1]

                if target_short_name == src_short_name:
                    copy_srcs.append(src)
                    copy_dsts.append(target)

        if not copy_srcs:
            cmds.confirmDialog(m='対応するオブジェクトがありません')
            return

        time_range = self.get_time_range()

        # プログレスバー表示
        progress_ctrl = self.show_progress_bar(0, len(copy_srcs))

        # 対応リスト通りに1つずつキーフレームコピーを実行
        # 全部を一度に実行した方が効率はよいはずだが、srcs内に重複があった場合にクリップボードコピー時にまとめられ
        # オブジェクトのインデックスが担保できないためこのように実装している
        for src, dst in zip(copy_srcs, copy_dsts):

            self.copy_key_frame(src, dst, time_range)

            if cmds.progressBar(progress_ctrl, ex=True):
                cmds.progressBar(progress_ctrl, e=True, step=1)

        self.delete_progress_bar()

    def copy_key_frame(self, src, dst, start_end=None):
        """キーフレームをコピー

        Args:
            src (str): コピー元
            dst (str): コピー先
            start_end ([int, int], optional): 開始フレーム、終了フレームのリスト. Defaults to None.
        """

        if not start_end:
            cmds.copyKey(src, cb='api', o='curve')
            cmds.pasteKey(dst, cb='api', o='replace')
        else:
            cmds.copyKey(src, cb='api', o='curve', t=(start_end[0], start_end[1]))
            cmds.pasteKey(dst, cb='api', o='replace', t=(start_end[0], start_end[1]))
