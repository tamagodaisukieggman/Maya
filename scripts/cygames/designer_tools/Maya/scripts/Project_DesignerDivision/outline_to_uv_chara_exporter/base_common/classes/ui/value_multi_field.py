# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ValueMultiField(object):

    # ===============================================
    def __init__(self, label, value_info_list, isInteger, **layout_edit_param):

        self.ui_layout_id = base_utility.string.get_random_string(16)
        self.ui_label_id = self.ui_layout_id + '_label'

        self.ui_value_id_list = None
        self.ui_value_label_id_list = None

        self.__value_info_list = value_info_list
        self.__value_info_index_dict = None

        self.__isInteger = isInteger

        self.__change_function = None
        self.__change_function_arg = None

        self.__draw()

        if layout_edit_param:
            layout_edit_param['edit'] = True
            self.apply_layout_param(**layout_edit_param)

        self.apply_label_param(e=True, label=label)

    # ===============================================
    def __draw(self):

        if not self.__value_info_list:
            self.__value_info_list = [
                {
                    'key': 'value',
                    'label': 'Value',
                    'value': 0,
                    'type': int
                }
            ]

        self.ui_value_id_list = []
        self.ui_value_label_id_list = []
        self.__value_info_index_dict = {}

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_key = value_info['key']

            self.__value_info_index_dict[this_key] = count

            self.ui_value_id_list.append(
                self.ui_layout_id + '_' + this_key)

            self.ui_value_label_id_list.append(
                self.ui_layout_id + '_' + this_key + '_label')

        cmds.rowLayout(
            self.ui_layout_id, numberOfColumns=2, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        cmds.rowLayout(
            numberOfColumns=len(self.__value_info_list), adj=1)

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_label = value_info['label']
            this_value = value_info['value']

            this_type = float
            if self.__isInteger:
                this_type = int

            if 'type' in value_info:
                this_type = value_info['type']

            cmds.rowLayout(numberOfColumns=2, adj=1)

            cmds.text(
                self.ui_value_label_id_list[count],
                label=this_label,
                align='right'
            )

            if this_type == int:

                cmds.intField(
                    self.ui_value_id_list[count], v=this_value,
                    cc=self.__execute_change_function
                )

            else:

                cmds.floatField(
                    self.ui_value_id_list[count], v=this_value,
                    cc=self.__execute_change_function
                )

            cmds.setParent('..')

        cmds.setParent('..')

        cmds.setParent('..')

    # ===============================================
    def __execute_change_function(self, value):

        if self.__change_function is None:
            return

        self.__change_function(*self.__change_function_arg)

    # ===============================================
    def set_change_function(self, function, *arg):

        self.__change_function = function
        self.__change_function_arg = arg

    # ===============================================
    def get_value_by_key(self, key):

        return self.apply_value_param_by_key(key, q=True, v=True)

    # ===============================================
    def get_value_by_index(self, index):

        return self.apply_value_param_by_index(index, q=True, v=True)

    # ===============================================
    def set_value_by_key(self, key, value):

        self.apply_value_param_by_key(key, e=True, v=value)

    # ===============================================
    def set_value_by_index(self, index, value):

        self.apply_value_param_by_index(index, e=True, v=value)

    # ===============================================
    def get_value_list(self):

        value_list = []

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_value = self.apply_value_param_by_index(count, q=True, v=True)

            value_list.append(this_value)

        return value_list

    # ===============================================
    def set_value_list(self, value_list):

        if not value_list:
            return

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            if count >= len(value_list):
                break

            self.apply_value_param_by_index(count, e=True, v=value_list[count])

    # ===============================================
    def apply_layout_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'rowLayout', self.ui_layout_id, **param)

        return return_value

    # ===============================================
    def apply_label_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'text', self.ui_label_id, **param)

        return return_value

    # ===============================================
    def apply_value_param_by_key(self, key, **param):

        if key not in self.__value_info_index_dict:
            return

        index = self.__value_info_index_dict[key]

        return self.apply_value_param_by_index(index, **param)

    # ===============================================
    def apply_value_param_by_index(self, index, **param):

        return_value = None

        value_info = self.__value_info_list[index]

        this_type = float
        if self.__isInteger:
            this_type = int

        if 'type' in value_info:
            this_type = value_info['type']

        if this_type == int:
            return_value = base_utility.system.exec_maya_command(
                'intField', self.ui_value_id_list[index], **param)
        else:
            return_value = base_utility.system.exec_maya_command(
                'floatField', self.ui_value_id_list[index], **param)

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value_list = []

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_key = value_info['key']
            this_value = value_info['value']

            this_value = setting.load(
                setting_key + '_' + this_key, float, this_value)

            this_value_list.append(this_value)

        self.set_value_list(this_value_list)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value_list = self.get_value_list()

        if not this_value_list:
            return

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_key = value_info['key']

            if count >= len(this_value_list):
                break

            setting.save(
                setting_key + '_' + this_key, this_value_list[count])
