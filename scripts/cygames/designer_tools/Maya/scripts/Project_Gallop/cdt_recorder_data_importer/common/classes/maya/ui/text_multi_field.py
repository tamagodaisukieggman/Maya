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

import maya.cmds as cmds

from .... import utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextMultiField(object):

    # ===============================================
    def __init__(self, label, value_info_list, **layout_param):

        self.ui_layout_id = utility.base.string.get_random_string(16)
        self.ui_label_id = self.ui_layout_id + '_label'
        self.ui_value_id_list = None
        self.ui_value_label_id_list = None

        self.__value_info_list = value_info_list

        self.__function = None
        self.__function_arg = None

        self.__draw()

        if layout_param:
            layout_param['edit'] = True
            self.apply_layout_param(**layout_param)

        self.apply_label_param(e=True, label=label)

    # ===============================================
    def __draw(self):

        if not self.__value_info_list:
            self.__value_info_list = [['Value', 'Value', '']]

        self.ui_value_id_list = []
        self.ui_value_label_id_list = []

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_key = value_info[0]

            self.ui_value_id_list.append(
                self.ui_layout_id + '_' + this_key)

            self.ui_value_label_id_list.append(
                self.ui_layout_id + '_' + this_key + '_label')

        cmds.rowLayout(
            self.ui_layout_id, numberOfColumns=2, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        cmds.rowLayout(numberOfColumns=len(self.__value_info_list), adj=1)

        count = -1
        for value_info in self.__value_info_list:
            count += 1

            this_label = value_info[1]
            this_value = value_info[2]

            cmds.rowLayout(numberOfColumns=2, adj=1)

            cmds.text(
                self.ui_value_label_id_list[count],
                label=this_label,
                align='right'
            )

            cmds.textField(
                self.ui_value_id_list[count],
                text=this_value,
                tcc=self.__execute_function
            )

            cmds.setParent('..')

        cmds.setParent('..')

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
    def get_value(self, index):

        return self.apply_value_param(index, q=True, text=True)

    # ===============================================
    def set_value(self, index, value):

        self.apply_value_param(index, e=True, text=value)

    # ===============================================
    def get_value_list(self):

        value_list = []

        count = -1
        for value_id in self.ui_value_id_list:
            count += 1

            this_value = cmds.textField(value_id, q=True, text=True)

            value_list.append(this_value)

        return value_list

    # ===============================================
    def set_value_list(self, value_list):

        if not value_list:
            return

        count = -1
        for value_id in self.ui_value_id_list:
            count += 1

            if count >= len(value_list):
                break

            cmds.textField(value_id, e=True, text=value_list[count])

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
    def apply_value_param(self, index, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'textField', self.ui_value_id_list[index], param
        )

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

            this_key = value_info[0]
            this_value = value_info[2]

            this_value = setting.load(
                setting_key + '_' + this_key, str, this_value)

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

            this_key = value_info[0]

            if count >= len(this_value_list):
                break

            setting.save(
                setting_key + '_' + this_key, this_value_list[count])
