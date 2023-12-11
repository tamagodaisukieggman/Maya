# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from . import mesh_path_creator

reload(base_common)

reload(mesh_path_creator)


# ===============================================
def main():

    main = Main()
    main.create_ui()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main:

    # ==================================================
    def __init__(self):

        self.tool_version = '19061801'
        self.tool_name = 'MeshPathCreator'

        self.window_name = self.tool_name + 'Win'

        # スクリプトのパス関連
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        # 設定関連
        self.setting = base_class.setting.Setting(self.tool_name)

    # ==================================================
    def create_ui(self):

        self.ui_window = base_class.ui.window.Window(
            self.window_name,
            'Glp' + self.tool_name + '  ' + self.tool_version,
            width=420, height=190
        )

        self.ui_window.set_close_function(self.__save_setting)

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button("メッシュパスを生成",
                                        self.__create_mesh_path, bgc=[0.7, 0.5, 0.5], height=40)

        self.ui_root_name = base_class.ui.text_field.TextField(
            "メッシュパスルート名", 'meshPath')

        self.ui_locator_size = base_class.ui.value_field.ValueField(
            'ロケータのサイズ', 0.5, False)

        self.ui_offset_locator_offset = base_class.ui.value_field.ValueField(
            'オフセットロケータのオフセット', 0.1, False)

        self.ui_up_locator_offset = base_class.ui.value_field.ValueField(
            'アップベクター用ロケータのオフセット', 1, False)

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True, parent=self.ui_window.ui_body_layout_id)

        self.__load_setting()

        self.ui_window.show()

    # ==================================================
    def __load_setting(self):

        self.ui_window.load_setting(
            self.setting, 'mainWindow')

        self.ui_root_name.load_setting(
            self.setting, 'RootName'
        )

        self.ui_locator_size.load_setting(
            self.setting, 'locatorSize'
        )

        self.ui_offset_locator_offset.load_setting(
            self.setting, 'offsetLocatorOffset'
        )

        self.ui_up_locator_offset.load_setting(
            self.setting, 'upLocatorOffset'
        )

    # ==================================================
    def __save_setting(self):

        self.ui_window.save_setting(
            self.setting, 'mainWindow')

        self.ui_root_name.save_setting(
            self.setting, 'RootName'
        )

        self.ui_locator_size.save_setting(
            self.setting, 'locatorSize'
        )

        self.ui_offset_locator_offset.save_setting(
            self.setting, 'offsetLocatorOffset'
        )

        self.ui_up_locator_offset.save_setting(
            self.setting, 'upLocatorOffset'
        )

    # ==================================================
    def __create_mesh_path(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'パスを作成しますか?',
                self.ui_window.ui_window_id):
            return

        select_list = cmds.ls(os=True, l=True)

        if not select_list:
            return

        path_creator = mesh_path_creator.MeshPathCreator()

        path_creator.target_vertex_list = select_list

        path_creator.root_transform_name = self.ui_root_name.get_value()

        path_creator.locator_size = self.ui_locator_size.get_value()

        path_creator.offset_curve_offset = self.ui_offset_locator_offset.get_value()

        path_creator.up_curve_offset = self.ui_up_locator_offset.get_value()

        path_creator.create()
