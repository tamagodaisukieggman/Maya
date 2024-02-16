# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import os

import maya.cmds as cmds

from .... import utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DataSelector(object):

    # ===============================================
    def __init__(self, label, path, is_directory, is_search_type, **layout_param):

        self.ui_layout_id = utility.base.string.get_random_string(16)
        self.ui_label_id = self.ui_layout_id + '_label'
        self.ui_value_id = self.ui_layout_id + '_value'
        self.ui_filter_id = self.ui_layout_id + '_filter'
        self.ui_nofilter_id = self.ui_layout_id + '_nofilter'
        self.ui_extfilter_id = self.ui_layout_id + '_extfilter'
        self.ui_lower_id = self.ui_layout_id + '_lower'

        self.is_directory = is_directory
        self.is_search_type = is_search_type

        self.__function = None
        self.__function_arg = None

        self.__draw()

        if layout_param:
            layout_param['edit'] = True
            self.apply_layout_param(**layout_param)

        self.apply_label_param(e=True, label=label)

        self.set_path(path)

        self.set_filter('', '', '')
        self.set_contain_lower(False)

    # ===============================================
    def __draw(self):

        cmds.columnLayout(self.ui_layout_id, adj=True)

        # データ選択
        cmds.rowLayout(self.ui_layout_id, numberOfColumns=5, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        cmds.textField(
            self.ui_value_id, text='', tcc=self.__execute_function
        )

        cmds.button(label='選択', c=self.__select_data_path_from_ui, width=40)
        cmds.button(label='開く', c=self.__open_explorer_from_ui, width=40)
        cmds.button(label='チェック', c=self.__check_path_from_ui, width=40)

        cmds.setParent('..')

        # 拡張子フィルタ
        advanced_layout = cmds.columnLayout(adj=True)

        extension_layout = cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='拡張子フィルタ', align='left', width=100)

        cmds.textField(
            self.ui_extfilter_id, text=''
        )

        cmds.setParent('..')

        # フィルタ
        cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='名前フィルタ(含む)', align='left', width=100)

        cmds.textField(
            self.ui_filter_id, text=''
        )

        cmds.setParent('..')

        # 含まないフィルタ
        cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='名前フィルタ(含まない)', align='left', width=100)

        cmds.textField(
            self.ui_nofilter_id, text=''
        )

        cmds.setParent('..')

        cmds.checkBox(self.ui_lower_id, label='下層を含む', value=False)

        cmds.setParent('..')

        if self.is_directory:
            cmds.rowLayout(extension_layout, e=True, vis=False)

        if not self.is_search_type:
            cmds.columnLayout(advanced_layout, e=True, vis=False)

        cmds.setParent('..')

    # ===============================================
    def __execute_function(self, value):

        if not self.__function:
            return

        self.__function(*self.__function_arg)

    # ===============================================
    def set_function(self, function, *arg):

        self.__function = function
        self.__function_arg = arg

    # ===============================================
    def __select_data_path_from_ui(self, value):

        if self.is_directory or self.is_search_type:
            self.__select_folder_path()
        else:
            self.__select_file_path()

    # ===============================================
    def __select_folder_path(self):

        select_dir_path = cmds.fileDialog2(
            dialogStyle=2,
            fileMode=3,
            cap='Select Folder',
            okc='Select'
        )

        if not select_dir_path:
            return

        select_dir_path = select_dir_path[0]

        self.set_path(select_dir_path)

    # ===============================================
    def __select_file_path(self):

        select_file_path = cmds.fileDialog2(
            dialogStyle=2,
            fileMode=1,
            cap='Select File',
            okc='Select'
        )

        if not select_file_path:
            return

        select_file_path = select_file_path[0]

        self.set_path(select_file_path)

    # ===============================================
    def __check_path_from_ui(self, value):

        if not utility.maya.ui.dialog.open_yes_no('確認', '対象データを確認しますか?'):
            return

        data_path_list = self.get_data_path_list()

        if not data_path_list:

            utility.maya.ui.dialog.open_ok(
                '対象リスト', '対象データがありません'
            )

            return

        utility.maya.ui.dialog.open_ok(
            '対象リスト', data_path_list
        )

    # ===============================================
    def __open_explorer_from_ui(self, value):

        utility.base.io.open_directory(self.get_path())

    # ===============================================
    def get_path(self):

        target_path = cmds.textField(
            self.ui_value_id, q=True, text=True)

        return target_path

    # ===============================================
    def set_path(self, path):

        cmds.textField(self.ui_value_id, e=True, text='')

        if self.is_directory or self.is_search_type:
            if os.path.isdir(path):
                cmds.textField(
                    self.ui_value_id, e=True, text=path)
        else:
            if os.path.isfile(path):
                cmds.textField(
                    self.ui_value_id, e=True, text=path)

    # ===============================================
    def get_data_path_list(self):

        data_path = cmds.textField(
            self.ui_value_id, q=True, text=True
        )

        this_filter = cmds.textField(
            self.ui_filter_id, q=True, text=True
        )

        this_nofilter = cmds.textField(
            self.ui_nofilter_id, q=True, text=True
        )

        this_extfilter = cmds.textField(
            self.ui_extfilter_id, q=True, text=True
        )

        this_contain_lower = cmds.checkBox(
            self.ui_lower_id, q=True, value=True
        )

        file_path_list = utility.base.io.get_target_data_path_list(
            data_path, self.is_directory, this_filter, this_nofilter, this_extfilter, this_contain_lower
        )

        return file_path_list

    # ===============================================
    def set_filter(self, name_filter, name_nofilter, extension_filter):

        if name_filter:
            cmds.textField(
                self.ui_filter_id, e=True, text=name_filter
            )

        if name_nofilter:
            cmds.textField(
                self.ui_nofilter_id, e=True, text=name_nofilter
            )

        if extension_filter:
            cmds.textField(
                self.ui_extfilter_id, e=True, text=extension_filter
            )

    # ===============================================
    def set_contain_lower(self, contain):

        cmds.checkBox(
            self.ui_lower_id, e=True, value=contain
        )

    # ===============================================
    def apply_layout_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'rowLayout', self.ui_layout_id, param
        )

        return return_value

    # ===============================================
    def apply_label_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'text', self.ui_label_id, param
        )

        return return_value

    # ===============================================
    def apply_value_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'textField', self.ui_value_id, param
        )

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_data_path = setting.load(setting_key + '_DataPath', str, '')
        this_filter = setting.load(setting_key + '_Filter', str, '')
        this_nofilter = setting.load(setting_key + '_NoFilter', str, '')
        this_extfilter = setting.load(setting_key + '_ExtFilter', str, '')
        this_contain_lower = setting.load(
            setting_key + '_ContainLower', bool, False)

        self.set_path(this_data_path)
        self.set_filter(this_filter, this_nofilter, this_extfilter)
        self.set_contain_lower(this_contain_lower)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_data_path = self.get_path()

        this_filter = cmds.textField(
            self.ui_filter_id, q=True, text=True
        )

        this_nofilter = cmds.textField(
            self.ui_nofilter_id, q=True, text=True
        )

        this_extfilter = cmds.textField(
            self.ui_extfilter_id, q=True, text=True
        )

        this_contain_lower = cmds.checkBox(
            self.ui_lower_id, q=True, value=True
        )

        setting.save(setting_key + '_DataPath', this_data_path)
        setting.save(setting_key + '_Filter', this_filter)
        setting.save(setting_key + '_NoFilter', this_nofilter)
        setting.save(setting_key + '_ExtFilter', this_extfilter)
        setting.save(setting_key + '_ContainLower', this_contain_lower)
