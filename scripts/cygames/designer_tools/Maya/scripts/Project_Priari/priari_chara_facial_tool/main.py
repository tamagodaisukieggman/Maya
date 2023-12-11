# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os
import sys
import re
import glob
import time

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI
from maya.app.general import mayaMixin

import random
import shiboken2
from PySide2.QtCore import Qt
from PySide2.QtCore import QSettings
from PySide2 import QtGui, QtWidgets
from . import priari_chara_facial_tool_gui
from . import facial_blend_shape_info
from . import facial_blend_shape_reorder
from . import facial_blend_shape_switcher

reload(facial_blend_shape_info)
reload(facial_blend_shape_reorder)
reload(facial_blend_shape_switcher)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ===============================================
    def __init__(self):

        self.main_window = priari_chara_facial_tool_gui.GUI()
        self.script_path = os.path.abspath(__file__)
        self.target_csv_path = os.path.dirname(self.script_path) + '/resources/facial_target.csv'

        self.blend_shape_info = facial_blend_shape_info.FacialBlendShapeInfo()
        self.blend_shape_info.initialize()

        self.reorder = facial_blend_shape_reorder.FacialBlendShapeReorder()
        self.switcher = facial_blend_shape_switcher.FacialBlendShapeSwicher()
        self.look_label_list = []
        self.mouth_label_list = []
        self.facial_label_list = []
        self.active_look_label_list = []
        self.active_mouth_label_list = []
        self.active_facial_label_list = []

    # ===============================================
    def show_ui(self):
        '''UIの呼び出し
        '''

        self.initialize()
        self.deleteOverlappingWindow(self.main_window)
        self.__setup_view_event()
        self.main_window.show()

    # ===============================================
    def initialize(self):

        for item in self.blend_shape_info.blend_shape_item_list:

            target_list = None
            if item.facial_type == 'look':
                target_list = self.look_label_list
            elif item.facial_type == 'facial':
                target_list = self.facial_label_list
            elif item.facial_type == 'mouth':
                target_list = self.mouth_label_list
            else:
                continue

            if item.label not in target_list:
                target_list.append(item.label)

    # ===============================================
    def deleteOverlappingWindow(self, target):
        '''Windowの重複削除処理
        '''

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        try:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        except:
            # Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)
        for widget in main_window.children():
            if type(target) == type(widget):
                widget.close()
                widget.deleteLater()

    # ===============================================
    def __setup_view_event(self):

        # index整列
        self.main_window.ui.order_index_button.clicked.connect(self.__reorder_button_event)

        # shapeEditorを開く
        self.main_window.ui.open_shape_editor_button.clicked.connect(self.__open_shape_editor_button_event)

        # 表情チェックボタン
        self.main_window.ui.look_default_button.clicked.connect(self.__look_default_button_event)
        self.main_window.ui.mouth_default_button.clicked.connect(self.__mouth_default_button_event)
        self.main_window.ui.facial_default_button.clicked.connect(self.__facial_default_button_event)
        self.__create_check_button()

        # 確認用anim関連
        self.main_window.ui.create_look_key_button.clicked.connect(self.__create_look_key_button_event)
        self.main_window.ui.create_mouth_key_button.clicked.connect(self.__create_mouth_key_button_event)
        self.main_window.ui.create_facial_key_button.clicked.connect(self.__create_facial_key_button_event)
        self.main_window.ui.delete_look_key_button.clicked.connect(self.__delete_look_key_button_event)
        self.main_window.ui.delete_mouth_key_button.clicked.connect(self.__delete_mouth_key_button_event)
        self.main_window.ui.delete_facial_key_button.clicked.connect(self.__delete_facial_key_button_event)

        # ツールを一度初期化
        self.__update_from_active_list()

    # ===============================================
    def __create_check_button(self):
        '''blend_shape_infoから動的にボタンを作成
        '''

        for look_label in self.look_label_list:
            this_item_button = QtWidgets.QPushButton(self.main_window.ui.look_item_frame)
            self.main_window.ui.verticalLayout_4.addWidget(this_item_button)
            this_item_button.setText(look_label)
            this_item_button.clicked.connect(lambda x=look_label: self.__look_button_event(x))

        for mouth_label in self.mouth_label_list:
            this_item_button = QtWidgets.QPushButton(self.main_window.ui.mouth_item_frame)
            self.main_window.ui.verticalLayout_9.addWidget(this_item_button)
            this_item_button.setText(mouth_label)
            this_item_button.clicked.connect(lambda x=mouth_label: self.__mouth_button_event(x))

        for facial_label in self.facial_label_list:
            this_item_button = QtWidgets.QPushButton(self.main_window.ui.facial_item_frame)
            self.main_window.ui.verticalLayout_6.addWidget(this_item_button)
            this_item_button.setText(facial_label)
            this_item_button.clicked.connect(lambda x=facial_label: self.__facial_button_event(x))

    # ===============================================
    def __reorder_button_event(self, arg=None):
        '''indexの並び替えイベント
        '''

        if cmds.confirmDialog(
                title='確認',
                message='仕様に合わせてIndexを並び替えます\nブレンドシェイプのグループは保持されません\n続行しますか？',
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No') == 'No':
            return

        self.reorder.initialize(self.blend_shape_info)
        self.reorder.reorder_blend_shape_index()

    # ===============================================
    def __open_shape_editor_button_event(self, arg=None):
        '''ShapeEditor表示イベント
        '''

        mel.eval('ShapeEditor')

    # ===============================================
    def __look_default_button_event(self, arg=None):
        '''目線のデフォルト表示イベント
        '''

        self.active_look_label_list = []
        self.__update_from_active_list()

    # ===============================================
    def __mouth_default_button_event(self, arg=None):
        '''口のデフォルト表示イベント
        '''

        self.active_mouth_label_list = []
        self.__update_from_active_list()

    # ===============================================
    def __facial_default_button_event(self, arg=None):
        '''表情のデフォルト表示イベント
        '''

        self.active_facial_label_list = []
        self.__update_from_active_list()

    # ===============================================
    def __look_button_event(self, label=None):
        '''目線の切り替えイベント
        '''

        # lookは加算
        if label in self.active_look_label_list:
            self.active_look_label_list.remove(label)
        else:
            self.active_look_label_list.append(label)

        self.__update_from_active_list()

    # ===============================================
    def __mouth_button_event(self, label=None):
        '''口の切り替えイベント
        '''

        # mouthは1つしか選ばせない
        if label in self.active_mouth_label_list:
            self.active_mouth_label_list = []
        else:
            self.active_mouth_label_list = [label]

        self.__update_from_active_list()

    # ===============================================
    def __facial_button_event(self, label=None):
        '''表情の切り替えイベント
        '''

        # facialは1つしか選ばせない
        if label in self.active_facial_label_list:
            self.active_facial_label_list = []
        else:
            self.active_facial_label_list = [label]

        self.__update_from_active_list()

    # ===============================================
    def __create_look_key_button_event(self, arg=None):
        '''目線の確認アニメ作成イベント
        '''

        self.switcher.initialize(self.blend_shape_info)
        self.switcher.create_check_anim('look')

    # ===============================================
    def __create_mouth_key_button_event(self, arg=None):
        '''口の確認アニメ作成イベント
        '''

        self.switcher.initialize(self.blend_shape_info)
        self.switcher.create_check_anim('mouth')

    # ===============================================
    def __create_facial_key_button_event(self, arg=None):
        '''表情の確認アニメ作成イベント
        '''

        self.switcher.initialize(self.blend_shape_info)
        self.switcher.create_check_anim('facial')

    # ===============================================
    def __delete_look_key_button_event(self, arg=None):
        '''目線の確認アニメ削除イベント
        '''

        self.switcher.initialize(self.blend_shape_info)
        self.switcher.delete_check_anim('look')

    # ===============================================
    def __delete_mouth_key_button_event(self, arg=None):
        '''口の確認アニメ削除イベント
        '''

        self.switcher.initialize(self.blend_shape_info)
        self.switcher.delete_check_anim('mouth')

    # ===============================================
    def __delete_facial_key_button_event(self, arg=None):
        '''表情の確認アニメ削除イベント
        '''

        self.switcher.initialize(self.blend_shape_info)
        self.switcher.delete_check_anim('facial')

    # ===============================================
    def __update_from_active_list(self):
        '''active_label_listからツールを更新する
        '''

        # UIの更新
        self.__update_button_state_from_active_list()

        # ブレンドシェイプの更新
        self.__update_look_from_active_list()
        self.__update_mouth_from_active_list()
        self.__update_facial_from_active_list()

    # ===============================================
    def __update_look_from_active_list(self):

        self.switcher.initialize(self.blend_shape_info)

        if not self.active_look_label_list:
            self.switcher.goto_default_facial('look')
            return

        for label in self.look_label_list:
            if label in self.active_look_label_list:
                self.switcher.change_weight_by_label('look', label, 1)
            else:
                self.switcher.change_weight_by_label('look', label, 0)

    # ===============================================
    def __update_mouth_from_active_list(self):

        self.switcher.initialize(self.blend_shape_info)

        if not self.active_mouth_label_list:
            self.switcher.goto_default_facial('mouth')
            return

        self.switcher.apply_facial_by_label('mouth', self.active_mouth_label_list[0])

    # ===============================================
    def __update_facial_from_active_list(self):

        self.switcher.initialize(self.blend_shape_info)

        if not self.active_facial_label_list:
            self.switcher.goto_default_facial('facial')
            return

        # facialの方は1つしか選ばれないはず
        self.switcher.apply_facial_by_label('facial', self.active_facial_label_list[0])

        # 発音が選択されている場合は表情としての口の動きは無し
        if self.active_mouth_label_list:
            self.switcher.change_weight_by_part('facial', 'mouth', 0)

    # ===============================================
    def __update_button_state_from_active_list(self):

        look_button_list = self.__get_button_widget_list(self.main_window.ui.look_item_frame)

        for look_button in look_button_list:
            if look_button.text() in self.active_look_label_list:
                self.__change_button_state(look_button, True)
            else:
                self.__change_button_state(look_button, False)

        mouth_button_list = self.__get_button_widget_list(self.main_window.ui.mouth_item_frame)

        for mouth_button in mouth_button_list:
            if mouth_button.text() in self.active_mouth_label_list:
                self.__change_button_state(mouth_button, True)
            else:
                self.__change_button_state(mouth_button, False)

        facial_button_list = self.__get_button_widget_list(self.main_window.ui.facial_item_frame)

        for facial_button in facial_button_list:
            if facial_button.text() in self.active_facial_label_list:
                self.__change_button_state(facial_button, True)
            else:
                self.__change_button_state(facial_button, False)

    # ===============================================
    def __get_button_widget_list(self, parent):

        all_widgets = parent.children()
        button_widgets = []

        for widget in all_widgets:

            if widget == self.main_window.ui.look_default_button:
                continue

            if widget == self.main_window.ui.mouth_default_button:
                continue

            if widget == self.main_window.ui.facial_default_button:
                continue

            if type(widget) is QtWidgets.QPushButton:
                button_widgets.append(widget)

        return button_widgets

    # ===============================================
    def __change_button_state(self, button, is_active):

        if is_active:
            button.setStyleSheet('background-color: {};'.format('#008888'))
        else:
            button.setStyleSheet('background-color: {};'.format('#000000'))