# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from PySide2 import QtWidgets

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility

from . import gui
from . import reference_part
from .. import main_template


DRESS_TYPE_LABELS = ['デカ', 'ミニ']


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpCharaUtilityReferancePart'
        self.tool_label = '頭・身体のリファレンス表示・非表示'
        self.tool_version = '19112201'

        self.body_general_menu = None
        self.head_menu = None
        self.body_shape_menu = None
        self.special_dress_type_radio_collection = None
        self.special_dress_type_normal_button = None
        self.special_dress_id_menu = None

        self.special_dress_ids_list = [], []
        self.special_dress_ids_list_is_loaded = False

        self.reference_part = reference_part.ReferencePart()

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.frameLayout(l=u"汎用衣装", cll=0, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        self.body_general_menu = cmds.optionMenuGrp(
            label='リファレンスで表示する衣装ID : ', columnAlign=[1, 'left'], adjustableColumn=2, changeCommand=self.__on_body_id_changed)
        self.head_menu = cmds.optionMenuGrp(
            label='リファレンスで表示する頭部ID : ', columnAlign=[1, 'left'], adjustableColumn=2)

        cmds.rowLayout(numberOfColumns=3, adjustableColumn3=1)
        self.body_shape_menu = cmds.optionMenuGrp(
            label='リファレンスで表示する体型ID : ', columnAlign=[1, 'left'], adjustableColumn=2)
        base_class.ui.button.Button('デフォルトID', self.__set_default_body_shape)
        base_class.ui.button.Button('現在のシーンのID', self.__set_scene_body_shape)
        cmds.setParent('..')

        base_class.ui.button.Button('リファレンスIDリスト更新', self.set_menu_item)
        cmds.separator()
        base_class.ui.button.Button('リファレンス表示', self.__view_parts_ref_cmd, [True, True])
        base_class.ui.button.Button('リファレンス非表示', self.__view_parts_ref_cmd, [False, True])
        cmds.setParent('..')
        cmds.setParent('..')

        frame = cmds.frameLayout(l=u"特別衣装", cll=0, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        cmds.rowLayout(numberOfColumns=5, adjustableColumn5=3)
        self.special_dress_type_radio_collection = cmds.radioCollection()
        for i, dress_type_label in enumerate(DRESS_TYPE_LABELS):
            radio_button = cmds.radioButton(label=dress_type_label, width=40, changeCommand=lambda _: self.__update_special_dress_id_menu(True))
            if i == 0:
                cmds.radioButton(radio_button, e=True, select=True)
                self.special_dress_type_normal_button = radio_button
        self.special_dress_id_menu = cmds.optionMenuGrp(label='ID : ', columnAlign=[1, 'left'], columnWidth=[1, 20], adjustableColumn=2)
        base_class.ui.button.Button('IDリスト更新', self.__update_special_dress_ids_list, width=80)
        base_class.ui.button.Button('現在のシーンのID', self.__set_scene_dress_id, [True])
        self.__set_scene_dress_id(False)
        cmds.scriptJob(event=['SceneOpened', lambda: self.__set_scene_dress_id(False)], protected=True, parent=frame)
        cmds.setParent('..')
        base_class.ui.button.Button('リファレンス表示', self.__view_parts_ref_cmd, [True, False])
        base_class.ui.button.Button('リファレンス非表示', self.__view_parts_ref_cmd, [False, False])
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button('全リファレンスを非表示', self.__unload_all_ref_cmd, None)
        base_class.ui.button.Button('リファレンス管理', self.__show_reference_manager)
        cmds.setParent('..')

    def __update_special_dress_ids_list(self):
        """特別衣装IDリストを更新する
        """

        self.special_dress_ids_list = self.reference_part.get_special_dress_ids_list()
        self.special_dress_ids_list_is_loaded = True

        self.__update_special_dress_id_menu(True)

    def __update_special_dress_id_menu(self, keep_selection):
        """特別衣装IDリストUIを更新する
        """

        previous_id = None

        item_list = cmds.optionMenuGrp(self.special_dress_id_menu, q=True, itemListLong=True)
        if item_list:
            previous_id = cmds.optionMenuGrp(self.special_dress_id_menu, q=True, value=True)
            cmds.deleteUI(item_list)

        selected_dress_type_radio_button = cmds.radioCollection(self.special_dress_type_radio_collection, q=True, select=True)
        selected_dress_type = cmds.radioButton(selected_dress_type_radio_button, q=True, label=True)

        if selected_dress_type not in DRESS_TYPE_LABELS:
            return

        dress_type_num = DRESS_TYPE_LABELS.index(selected_dress_type)

        special_dress_ids = self.special_dress_ids_list[dress_type_num]

        for special_dress_id in special_dress_ids:
            cmds.menuItem(parent='{}|OptionMenu'.format(self.special_dress_id_menu), label=special_dress_id)

        if not keep_selection:
            return

        if previous_id in special_dress_ids:
            cmds.optionMenuGrp(self.special_dress_id_menu, e=True, value=previous_id)

    def __set_scene_dress_id(self, show_dialog):
        """衣装IDを現在のシーンのIDに設定する
        """

        if not self.special_dress_ids_list_is_loaded:
            self.special_dress_ids_list = [], []

        is_normal, scene_dress_id, is_general = reference_part.get_scene_dress_id()

        if scene_dress_id is None:
            text = 'シーンから衣装IDが取得できません'
            cmds.warning(text)
            if show_dialog:
                QtWidgets.QMessageBox.information(None, self.tool_name, text, QtWidgets.QMessageBox.Ok)
            if self.special_dress_type_normal_button:
                cmds.radioButton(self.special_dress_type_normal_button, e=True, select=True)
                self.__update_special_dress_id_menu(False)
            return

        # 特別衣装IDリストが初期化されていない場合は現在のシーンのIDのみを含めたリストを設定する
        if not self.special_dress_ids_list_is_loaded and not is_general:
            self.special_dress_ids_list = [scene_dress_id], [scene_dress_id]

        radio_buttons = cmds.radioCollection(self.special_dress_type_radio_collection, q=True, collectionItemArray=True)

        dress_type_label = DRESS_TYPE_LABELS[0 if is_normal else 1]

        for radio_button in radio_buttons:
            if cmds.radioButton(radio_button, q=True, label=True) == dress_type_label:
                cmds.radioButton(radio_button, e=True, select=True)

        self.__update_special_dress_id_menu(False)

        # ミニ顔、汎用尻尾はIDを設定しない
        if is_general:
            print('', end='')  # warningリセット
            return

        menu_items = cmds.optionMenuGrp(self.special_dress_id_menu, q=True, ill=True) or []
        dress_ids = [cmds.menuItem(item, q=True, l=True) for item in menu_items]

        if scene_dress_id in dress_ids:
            cmds.optionMenuGrp(self.special_dress_id_menu, e=True, value=scene_dress_id)
            print('', end='')  # warningリセット
            return

        text = '現在のシーンの衣装IDが見つかりません'
        cmds.warning('{} ({})'.format(text, scene_dress_id))
        if show_dialog:
            QtWidgets.QMessageBox.information(None, self.tool_name, text, QtWidgets.QMessageBox.Ok)

    def set_menu_item(self, *args):
        """[summary]
        """

        self.reference_part.set_chara_path_list()
        general_dress_name_list = self.reference_part.get_file_name_list_without_ext(
            self.reference_part.general_dress_path_list
        )
        head_name_list = self.reference_part.get_file_name_list_without_ext(
            self.reference_part.head_path_list
        )

        if self.body_general_menu is not None:

            item_list = cmds.optionMenuGrp(self.body_general_menu, q=True, itemListLong=True)
            if item_list:
                cmds.deleteUI(item_list)

            for general_dress_name in general_dress_name_list:
                cmds.menuItem(parent='{}|OptionMenu'.format(self.body_general_menu), label=general_dress_name)

            self.__update_body_shape_menu(cmds.optionMenuGrp(self.body_general_menu, q=True, value=True))

        if self.head_menu is not None:

            item_list = cmds.optionMenuGrp(self.head_menu, q=True, itemListLong=True)
            if item_list:
                cmds.deleteUI(item_list)

            for head_name in head_name_list:
                cmds.menuItem(parent='{}|OptionMenu'.format(self.head_menu), label=head_name)

    def __view_parts_ref_cmd(self, args):

        base_utility.select.save_selection()

        head_name = cmds.optionMenuGrp(self.head_menu, q=True, value=True) if cmds.optionMenuGrp(self.head_menu, q=True, ni=True) > 0 else ''
        body_name = cmds.optionMenuGrp(self.body_general_menu, q=True, value=True) if cmds.optionMenuGrp(self.body_general_menu, q=True, ni=True) > 0 else ''
        body_shape_id = cmds.optionMenuGrp(self.body_shape_menu, q=True, value=True) if cmds.optionMenuGrp(self.body_shape_menu, q=True, ni=True) > 0 else ''
        is_normal_dress_type = cmds.radioButton(self.special_dress_type_normal_button, q=True, select=True)
        special_dress_id = cmds.optionMenuGrp(self.special_dress_id_menu, q=True, value=True) if cmds.optionMenuGrp(self.special_dress_id_menu, q=True, ni=True) > 0 else ''

        self.reference_part.view_parts_ref(args[0], args[1], head_name, body_name, body_shape_id, is_normal_dress_type, special_dress_id)

        base_utility.select.load_selection()

    def __unload_all_ref_cmd(self, args):

        self.reference_part.unload_all_ref()

    def __on_body_id_changed(self, id):
        self.__update_body_shape_menu(id)

    def __update_body_shape_menu(self, id):
        """体型リストUIを更新する

        Args:
            id ([str]): 汎用衣装ID
        """

        if self.body_shape_menu is None:
            return

        previous_id = None

        item_list = cmds.optionMenuGrp(self.body_shape_menu, q=True, itemListLong=True)
        if item_list:
            previous_id = cmds.optionMenuGrp(self.body_shape_menu, q=True, value=True)
            cmds.deleteUI(item_list)

        body_shape_name_list = self.reference_part.get_body_shape_list(id)

        for body_shape_name in body_shape_name_list:
            cmds.menuItem(parent='{}|OptionMenu'.format(self.body_shape_menu), label=body_shape_name)

        # 体型IDの指定
        # 優先順: リスト更新前に選択されていたID > デフォルトID（1_0_2 or 1） > リストの先頭（設定しない）

        if previous_id in body_shape_name_list:
            cmds.optionMenuGrp(self.body_shape_menu, e=True, value=previous_id)
            return

        self.__set_default_body_shape()

    def __set_default_body_shape(self):
        """体型IDをデフォルトIDに設定する
        """

        if self.body_shape_menu is None:
            return

        menu_items = cmds.optionMenuGrp(self.body_shape_menu, q=True, ill=True) or []
        body_shape_name_list = [cmds.menuItem(item, q=True, l=True) for item in menu_items]

        default_body_shape = self.reference_part.get_default_body_shape()

        if default_body_shape in body_shape_name_list:
            cmds.optionMenuGrp(self.body_shape_menu, e=True, value=default_body_shape)
            print('', end='')  # warningリセット
            return

        body_id = cmds.optionMenuGrp(self.body_general_menu, q=True, value=True)
        cmds.warning('デフォルト体型差分データが見つかりません ({}, {})'.format(body_id, default_body_shape))

    def __set_scene_body_shape(self):
        """体型IDを現在のシーンのIDに設定する
        """

        if self.body_shape_menu is None:
            return

        menu_items = cmds.optionMenuGrp(self.body_shape_menu, q=True, ill=True) or []
        body_shape_name_list = [cmds.menuItem(item, q=True, l=True) for item in menu_items]

        scene_body_shape = self.reference_part.get_scene_body_shape()

        if scene_body_shape is None:
            text = '現在のシーンの体型差分データが見つかりません'
            QtWidgets.QMessageBox.information(None, self.tool_name, text, QtWidgets.QMessageBox.Ok)
            return

        if scene_body_shape in body_shape_name_list:
            cmds.optionMenuGrp(self.body_shape_menu, e=True, value=scene_body_shape)
            print('', end='')  # warningリセット
            return

        body_id = cmds.optionMenuGrp(self.body_general_menu, q=True, value=True)
        cmds.warning('現在のシーンの体型差分データが見つかりません ({}, {})'.format(body_id, scene_body_shape))

    def __show_reference_manager(self):
        """リファレンス管理ウィンドウを開く
        """

        gui.ManagerWindow().show()
