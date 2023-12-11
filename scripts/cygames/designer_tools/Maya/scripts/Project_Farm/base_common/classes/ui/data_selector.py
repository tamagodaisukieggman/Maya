# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import os
import re
import subprocess

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DataSelector(object):

    # ===============================================
    def __init__(self, label, path, is_directory, is_search_type,
                 **layout_edit_param):

        self.ui_layout_id = base_utility.string.get_random_string(16)

        self.ui_label_id = self.ui_layout_id + '_label'
        self.ui_value_id = self.ui_layout_id + '_value'

        self.ui_file_filter_id = self.ui_layout_id + '_file_filter'
        self.ui_file_nofilter_id = self.ui_layout_id + '_file_nofilter'
        self.ui_ext_filter_id = self.ui_layout_id + '_ext_filter'

        self.ui_dir_filter_id = self.ui_layout_id + '_dir_filter'
        self.ui_dir_nofilter_id = self.ui_layout_id + '_dir_nofilter'

        self.ui_lower_id = self.ui_layout_id + '_contain_lower'

        self.ui_file_setting_layout_id = None
        self.ui_dir_setting_layout_id = None

        self.__is_directory = is_directory
        self.__is_search_type = is_search_type

        self.__change_function = None
        self.__change_function_arg = None

        self.__draw()

        if layout_edit_param:
            layout_edit_param['edit'] = True
            self.apply_layout_param(**layout_edit_param)

        self.apply_label_param(e=True, label=label)

        self.set_path(path)

    # ===============================================
    def __draw(self):

        cmds.frameLayout(self.ui_layout_id, lv=False, bv=True, mw=10, mh=10)

        # データ選択
        cmds.rowLayout(numberOfColumns=5, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        cmds.textField(
            self.ui_value_id, text='', tcc=self.__execute_change_function
        )

        cmds.button(label='選択', c=self.__select_data_path_from_ui, width=40)
        cmds.button(label='開く', c=self.__open_explorer_from_ui, width=40)
        cmds.button(label='チェック', c=self.__check_path_from_ui, width=40)

        cmds.setParent('..')

        search_type_layout = cmds.frameLayout(lv=False, mw=0, mh=0)

        # ------------------------------
        # ファイル設定

        self.ui_file_setting_layout_id = cmds.frameLayout(
            l='ファイル設定', cll=True, bv=True, mw=10, mh=10)

        # 拡張子フィルタ
        cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='拡張子', align='left', width=150)

        cmds.textField(
            self.ui_ext_filter_id, text=''
        )

        cmds.setParent('..')

        # ファイル 含むフィルタ
        cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='ファイル名(含む)', align='left', width=150)

        cmds.textField(
            self.ui_file_filter_id, text=''
        )

        cmds.setParent('..')

        # ファイル 含まないフィルタ
        cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='ファイル名(含まない)', align='left', width=150)

        cmds.textField(
            self.ui_file_nofilter_id, text=''
        )

        cmds.setParent('..')

        cmds.setParent('..')

        # ------------------------------
        # フォルダ設定

        self.ui_dir_setting_layout_id = cmds.frameLayout(
            l='フォルダ設定', cll=True, bv=True, mw=10, mh=10)

        # フォルダ 含むフィルタ
        cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='フォルダ名(含む)', align='left', width=150)

        cmds.textField(
            self.ui_dir_filter_id, text=''
        )

        cmds.setParent('..')

        # フォルダ 含まないフィルタ
        cmds.rowLayout(numberOfColumns=2, adj=2)

        cmds.text(label='フォルダ名(含まない)', align='left', width=150)

        cmds.textField(
            self.ui_dir_nofilter_id, text=''
        )

        cmds.setParent('..')

        # 下層を含む
        cmds.checkBox(self.ui_lower_id, label='下層を含む', value=False)

        cmds.setParent('..')

        cmds.setParent('..')

        # ------------------------------

        if self.__is_directory:
            cmds.frameLayout(self.ui_file_setting_layout_id,
                              e=True, vis=False)

        if not self.__is_search_type:
            cmds.frameLayout(search_type_layout, e=True, vis=False)

        cmds.setParent('..')

    # ===============================================
    def __execute_change_function(self, value):

        if not self.__change_function:
            return

        self.__change_function(*self.__change_function_arg)

    # ===============================================
    def set_change_function(self, function, *arg):

        self.__change_function = function
        self.__change_function_arg = arg

    # ===============================================
    def __select_data_path_from_ui(self, value):

        if self.__is_directory or self.__is_search_type:
            self.__select_dir_path()
        else:
            self.__select_file_path()

    # ===============================================
    def __select_dir_path(self):

        # ------------------------------
        # カレントパス取得

        current_dir_path = self.get_path()

        if current_dir_path:
            if os.path.isdir(current_dir_path):
                current_dir_path = \
                    os.path.dirname(current_dir_path).replace('\\', '/')
        else:
            current_dir_path = ''

        select_dir_path = cmds.fileDialog2(
            dialogStyle=2,
            fileMode=3,
            cap='Select Folder',
            okc='Select',
            dir=current_dir_path
        )

        if not select_dir_path:
            return

        select_dir_path = select_dir_path[0]

        self.set_path(select_dir_path)

    # ===============================================
    def __select_file_path(self):

        # ------------------------------
        # フィルタ設定

        fix_file_filter = ''

        this_ext_filter = cmds.textField(
            self.ui_ext_filter_id, q=True, text=True
        )

        if this_ext_filter:
            this_ext_filter_list = this_ext_filter.split(',')
            for ext_filter in this_ext_filter_list:

                fix_filter_name = ext_filter.replace('.', '')

                fix_file_filter += '{0}(*.{1} *.{2});;'.format(
                    ext_filter, fix_filter_name.lower(), fix_filter_name.upper())

        if not fix_file_filter:
            fix_file_filter = 'All Files(*.*)'

        # ------------------------------
        # カレントパス取得

        current_file_path = self.get_path()
        current_dir_path = ''

        if current_file_path:
            if os.path.isfile(current_file_path):
                current_dir_path = \
                    os.path.dirname(current_file_path).replace('\\', '/')

        # ------------------------------
        # ダイアログ表示

        select_file_path = cmds.fileDialog2(
            dialogStyle=2,
            fileMode=1,
            cap='Select File',
            okc='Select',
            fileFilter=fix_file_filter,
            dir=current_dir_path
        )

        if not select_file_path:
            return

        select_file_path = select_file_path[0]

        self.set_path(select_file_path)

    # ===============================================
    def __check_path_from_ui(self, value):

        if not base_utility.ui.dialog.open_ok_cancel('確認', '対象データを確認しますか?'):
            return

        data_path_list = self.get_data_path_list()

        if not data_path_list:

            base_utility.ui.dialog.open_ok(
                '対象データリスト', '対象データがありません'
            )

            return

        base_utility.ui.dialog.open_ok_with_scroll(
            '対象データリスト', '以下のデータが対象になります', data_path_list
        )

    # ===============================================
    def __open_explorer_from_ui(self, value):

        if not self.get_path():
            return

        target_dir_path = None

        if os.path.isfile(self.get_path()):
            target_dir_path = os.path.dirname(self.get_path())

        elif os.path.isdir(self.get_path()):
            target_dir_path = self.get_path()

        if target_dir_path is None:
            return

        target_dir_path = target_dir_path.replace('/', '\\')
        subprocess.Popen('explorer "' + target_dir_path + '"')

    # ===============================================
    def get_path(self):

        target_path = cmds.textField(
            self.ui_value_id, q=True, text=True)

        return target_path

    # ===============================================
    def set_path(self, path):

        cmds.textField(self.ui_value_id, e=True, text='')

        if not path:
            return

        cmds.textField(
            self.ui_value_id, e=True, text=path)

    # ===============================================
    def get_data_path_list(self):

        data_path = cmds.textField(
            self.ui_value_id, q=True, text=True
        )

        this_file_filter = cmds.textField(
            self.ui_file_filter_id, q=True, text=True
        )

        this_file_nofilter = cmds.textField(
            self.ui_file_nofilter_id, q=True, text=True
        )

        this_ext_filter = cmds.textField(
            self.ui_ext_filter_id, q=True, text=True
        )

        this_dir_filter = cmds.textField(
            self.ui_dir_filter_id, q=True, text=True
        )

        this_dir_nofilter = cmds.textField(
            self.ui_dir_nofilter_id, q=True, text=True
        )

        this_contain_lower = cmds.checkBox(
            self.ui_lower_id, q=True, value=True
        )

        data_path_list = []

        # --------------------
        # 一時データリストの作成

        temp_data_path_list = []

        if os.path.isdir(data_path):

            target_dir_path = data_path.replace('\\', '/')

            if self.__is_directory:
                temp_data_path_list.append(target_dir_path)

            for root, dirs, files in os.walk(target_dir_path):

                this_root_path = root.replace('\\', '/')

                if this_root_path.find('/.') >= 0:
                    continue

                # ファイル
                if not self.__is_directory:

                    for this_file in files:

                        this_file_path = os.path.join(
                            root, this_file).replace('\\', '/')

                        temp_data_path_list.append(this_file_path)

                if not this_contain_lower:
                    break

                # ディレクトリ
                if self.__is_directory:

                    for this_dir in dirs:

                        this_dir_path = os.path.join(
                            root, this_dir).replace('\\', '/')

                        temp_data_path_list.append(this_dir_path)

        elif os.path.isfile(data_path):

            target_file_path = data_path.replace('\\', '/')

            if not self.__is_directory:
                temp_data_path_list.append(target_file_path)

        if not temp_data_path_list:
            return data_path_list

        # --------------------
        # フィルタのリスト化

        fix_file_name_filter_list = []
        fix_file_name_nofilter_list = []
        fix_this_ext_filter_list = []

        fix_dir_name_filter_list = []
        fix_dir_name_nofilter_list = []

        if this_file_filter:
            fix_file_name_filter_list = this_file_filter.split(',')

        if this_file_nofilter:
            fix_file_name_nofilter_list = this_file_nofilter.split(',')

        if this_ext_filter:
            fix_this_ext_filter_list = this_ext_filter.split(',')

        if dir_name_filter:
            fix_dir_name_filter_list = dir_name_filter.split(',')

        if this_dir_nofilter:
            fix_dir_name_nofilter_list = this_dir_nofilter.split(',')

        # --------------------
        # データパスをフィルタから割り出し

        for data_path in temp_data_path_list:

            this_dir_path = os.path.dirname(data_path)
            this_data_name = os.path.basename(data_path)
            this_data_name_noext, this_data_ext = \
                os.path.splitext(this_data_name)

            this_data_ext = this_data_ext.lower()

            if this_dir_path.find('/.') >= 0:
                continue

            is_target = True

            # --------------------
            # フォルダ(含む)判定

            if fix_dir_name_filter_list:

                is_target = False

                for this_filter in fix_dir_name_filter_list:

                    if re.search(this_filter, this_dir_path):
                        is_target = True
                        break
            else:
                is_target = True

            if not is_target:
                continue

            # --------------------
            # フォルダ(含まない)判定

            if fix_dir_name_nofilter_list:

                is_target = True

                for this_filter in fix_dir_name_nofilter_list:

                    if re.search(this_filter, this_dir_path):
                        is_target = False
                        break
            else:
                is_target = True

            if not is_target:
                continue

            # --------------------
            # ファイル拡張子(含む)判定

            if not self.__is_directory:

                if fix_this_ext_filter_list:

                    is_target = False

                    for this_filter in fix_this_ext_filter_list:

                        if not this_filter:
                            continue

                        if re.search(this_filter.lower(), this_data_ext):
                            is_target = True
                            break
                else:
                    is_target = True

            if not is_target:
                continue

            # --------------------
            # ファイル(含む)判定

            if fix_file_name_filter_list:

                is_target = False

                for this_filter in fix_file_name_filter_list:

                    if re.search(this_filter, this_data_name):
                        is_target = True
                        break
            else:
                is_target = True

            if not is_target:
                continue

            # --------------------
            # ファイル(含まない)判定

            if fix_file_name_nofilter_list:

                is_target = True

                for this_filter in fix_file_name_nofilter_list:

                    if re.search(this_filter, this_data_name):
                        is_target = False
                        break
            else:
                is_target = True

            if not is_target:
                continue

            # --------------------

            data_path_list.append(data_path)

        return data_path_list

    # ===============================================
    def set_file_filter(self, file_filter, file_nofilter):

        if file_filter is not None:
            cmds.textField(
                self.ui_file_filter_id, e=True, text=file_filter
            )

        if file_nofilter is not None:
            cmds.textField(
                self.ui_file_nofilter_id, e=True, text=file_nofilter
            )

    # ===============================================
    def set_extension_filter(self, extension_filter):

        if extension_filter is not None:
            cmds.textField(
                self.ui_ext_filter_id, e=True, text=extension_filter
            )

    # ===============================================
    def set_dir_filter(self, dir_filter, dir_nofilter):

        if dir_filter is not None:
            cmds.textField(
                self.ui_dir_filter_id, e=True, text=dir_filter
            )

        if dir_nofilter is not None:
            cmds.textField(
                self.ui_dir_nofilter_id, e=True, text=dir_nofilter
            )

    # ===============================================
    def set_contain_lower(self, contain):

        cmds.checkBox(
            self.ui_lower_id, e=True, value=contain
        )

    # ===============================================
    def apply_layout_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'frameLayout', self.ui_layout_id, **param)

        return return_value

    # ===============================================
    def apply_label_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'text', self.ui_label_id, **param)

        return return_value

    # ===============================================
    def apply_value_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'textField', self.ui_value_id, **param)

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_data_path = setting.load(setting_key + '_DataPath', str, '')

        this_file_filter = setting.load(setting_key + '_FileFilter', str, '')
        this_file_nofilter = setting.load(
            setting_key + '_FileNoFilter', str, '')
        this_ext_filter = setting.load(setting_key + '_ExtFilter', str, '')

        this_dir_filter = setting.load(setting_key + '_DirFilter', str, '')
        this_dir_nofilter = setting.load(setting_key + '_DirNoFilter', str, '')
        this_contain_lower = setting.load(
            setting_key + '_ContainLower', bool, False)

        this_file_setting_close = setting.load(
            setting_key + '_FileSettingClose', bool, False
        )

        this_dir_setting_close = setting.load(
            setting_key + '_DirSettingClose', bool, False
        )

        self.set_path(this_data_path)

        self.set_file_filter(
            this_file_filter, this_file_nofilter)

        self.set_extension_filter(this_ext_filter)

        self.set_dir_filter(
            this_dir_filter, this_dir_nofilter)

        self.set_contain_lower(this_contain_lower)

        cmds.frameLayout(self.ui_file_setting_layout_id,
                          e=True, cl=this_file_setting_close)

        cmds.frameLayout(self.ui_dir_setting_layout_id,
                          e=True, cl=this_dir_setting_close)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_data_path = self.get_path()

        this_file_filter = cmds.textField(
            self.ui_file_filter_id, q=True, text=True
        )

        this_file_nofilter = cmds.textField(
            self.ui_file_nofilter_id, q=True, text=True
        )

        this_ext_filter = cmds.textField(
            self.ui_ext_filter_id, q=True, text=True
        )

        this_dir_filter = cmds.textField(
            self.ui_dir_filter_id, q=True, text=True
        )

        this_dir_nofilter = cmds.textField(
            self.ui_dir_nofilter_id, q=True, text=True
        )

        this_contain_lower = cmds.checkBox(
            self.ui_lower_id, q=True, value=True
        )

        this_file_setting_close = cmds.frameLayout(
            self.ui_file_setting_layout_id, q=True, cl=True
        )

        this_dir_setting_close = cmds.frameLayout(
            self.ui_dir_setting_layout_id, q=True, cl=True
        )

        setting.save(setting_key + '_DataPath', this_data_path)

        setting.save(setting_key + '_FileFilter', this_file_filter)
        setting.save(setting_key + '_FileNoFilter', this_file_nofilter)
        setting.save(setting_key + '_ExtFilter', this_ext_filter)

        setting.save(setting_key + '_DirFilter', this_dir_filter)
        setting.save(setting_key + '_DirNoFilter', this_dir_nofilter)
        setting.save(setting_key + '_ContainLower', this_contain_lower)

        setting.save(setting_key + '_FileSettingClose',
                     this_file_setting_close)
        setting.save(setting_key + '_DirSettingClose', this_dir_setting_close)
