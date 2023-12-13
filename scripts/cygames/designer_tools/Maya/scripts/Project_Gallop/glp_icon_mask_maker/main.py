# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from builtins import range
    from importlib import reload
except Exception:
    pass

import sys

import maya.cmds as cmds

import shiboken2

from PySide2 import QtWidgets
from maya import OpenMayaUI

from . import view
from . import icon_mask_maker

reload(view)
reload(icon_mask_maker)


class Main(object):

    def __init__(self):
        """コンストラクタ
        """

        self.tool_name = 'GlpIconMaskMaker'
        self.tool_version = '22100501'

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

        self.view.ui.add_face_button.clicked.connect(self.add_face_button_event)
        self.view.ui.rem_face_button.clicked.connect(self.rem_face_button_event)
        self.view.ui.view_body_button.clicked.connect(self.view_body_button_event)
        self.view.ui.view_mask_button.clicked.connect(self.view_mask_button_event)
        self.view.ui.isolate_off_button.clicked.connect(self.isolate_off_button_event)

    def add_face_button_event(self):
        """選択面を指定ボタンイベント
        """
        target_list = cmds.ls(sl=True)
        if target_list:
            icon_mask_maker.add_mmask(target_list)

    def rem_face_button_event(self):
        """選択面を除外ボタンイベント
        """
        target_list = cmds.ls(sl=True)
        if target_list:
            icon_mask_maker.remove_mmask(target_list)

    def view_body_button_event(self):
        """衣装部分を分離表示ボタンイベント
        """
        icon_mask_maker.turn_on_body_isolate_view()

    def view_mask_button_event(self):
        """マスク部分を分離表示ボタンイベント
        """
        icon_mask_maker.turn_on_mask_isolate_view()

    def isolate_off_button_event(self):
        """分離表示OFFボタンイベント
        """
        icon_mask_maker.turn_off_isolate_view()
