# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility

from . import reference_part
from .. import main_template


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
        base_class.ui.button.Button('リファレンス表示', self._view_parts_ref_cmd, [True, True, False])
        base_class.ui.button.Button('リファレンス非表示', self._view_parts_ref_cmd, [False, True, False])
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u"特別衣装", cll=0, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button('リファレンス表示', self._view_parts_ref_cmd, [True, False, False])
        base_class.ui.button.Button('リファレンス非表示', self._view_parts_ref_cmd, [False, False, False])
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u"ミニ", cll=0, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button('デカリファレンス表示', self._view_parts_ref_cmd, [True, False, True])
        base_class.ui.button.Button('デカリファレンス非表示', self._view_parts_ref_cmd, [False, False, True])
        cmds.setParent('..')
        cmds.setParent('..')

        base_class.ui.button.Button('全リファレンスを非表示', self._unload_all_ref_cmd, None)

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

    # ===============================================
    def _view_parts_ref_cmd(self, args):

        base_utility.select.save_selection()

        head_short_name_without_ext = cmds.optionMenuGrp(self.head_menu, q=True, value=True)
        body_short_name_without_ext = cmds.optionMenuGrp(self.body_general_menu, q=True, value=True)
        body_shape_id = cmds.optionMenuGrp(self.body_shape_menu, q=True, value=True)

        self.reference_part.view_parts_ref(args[0], args[1], args[2], head_short_name_without_ext, body_short_name_without_ext, body_shape_id)

        base_utility.select.load_selection()

    # ===============================================
    def _unload_all_ref_cmd(self, args):

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
            cmds.confirmDialog(title=self.tool_name, message='現在のシーンの体型差分データが見つかりません')
            return

        if scene_body_shape in body_shape_name_list:
            cmds.optionMenuGrp(self.body_shape_menu, e=True, value=scene_body_shape)
            print('', end='')  # warningリセット
            return

        body_id = cmds.optionMenuGrp(self.body_general_menu, q=True, value=True)
        cmds.warning('現在のシーンの体型差分データが見つかりません ({}, {})'.format(body_id, scene_body_shape))
