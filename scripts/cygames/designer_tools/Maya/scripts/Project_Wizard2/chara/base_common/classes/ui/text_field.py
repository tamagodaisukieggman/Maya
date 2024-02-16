# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextField(object):

    # ===============================================
    def __init__(self, label, value, **layout_edit_param):

        self.ui_layout_id = base_utility.string.get_random_string(16)
        self.ui_label_id = self.ui_layout_id + '_label'
        self.ui_value_id = self.ui_layout_id + '_value'

        self.default_value = value

        self.__change_function = None
        self.__change_function_arg = None

        self.__draw()

        if layout_edit_param:
            layout_edit_param['edit'] = True
            self.apply_layout_param(**layout_edit_param)

        self.apply_label_param(e=True, label=label)

        self.set_value(value)

    # ===============================================
    def __draw(self):

        cmds.rowLayout(self.ui_layout_id, numberOfColumns=2, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        cmds.textField(
            self.ui_value_id,
            text='',
            tcc=self.__execute_change_function
        )

        cmds.setParent('..')

    # ===============================================
    def __execute_change_function(self, value):

        if not self.__change_function:
            return

        self.__change_function(*self.__change_function_arg)

    # ===============================================
    def set_function(self, function, *arg):

        self.__change_function = function
        self.__change_function_arg = arg

    # ===============================================
    def get_value(self):

        return self.apply_value_param(q=True, text=True)

    # ===============================================
    def set_value(self, value):

        self.apply_value_param(e=True, text=value)

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

        this_value = setting.load(
            setting_key + '_Value', str, self.default_value)

        self.set_value(this_value)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = self.get_value()

        setting.save(setting_key + '_Value', this_value)
