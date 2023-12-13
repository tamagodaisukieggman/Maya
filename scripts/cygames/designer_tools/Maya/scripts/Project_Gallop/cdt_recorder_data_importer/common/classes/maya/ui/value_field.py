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
class ValueField(object):

    # ===============================================
    def __init__(self, label, value, isInteger, **layout_param):

        self.ui_layout_id = utility.base.string.get_random_string(16)
        self.ui_label_id = self.ui_layout_id + '_label'
        self.ui_value_id = self.ui_layout_id + '_value'

        self.default_value = value

        self.isInteger = isInteger

        self.__function = None
        self.__function_arg = None

        self.__draw()

        if layout_param:
            layout_param['edit'] = True
            self.set_layout_param(**layout_param)

        self.set_label_param(e=True, label=label)
        self.set_value(value)

    # ===============================================
    def __draw(self):

        cmds.rowLayout(
            self.ui_layout_id, numberOfColumns=2, adj=2)

        cmds.text(self.ui_label_id, label='', align='left')

        if self.isInteger:
            cmds.intField(self.ui_value_id, cc=self.__execute_function)
        else:
            cmds.floatField(self.ui_value_id, cc=self.__execute_function)

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
    def get_value(self):

        return self.set_value_param(q=True, value=True)

    # ===============================================
    def set_value(self, value):

        self.set_value_param(e=True, value=value)

    # ===============================================
    def set_layout_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'rowLayout', self.ui_layout_id, param
        )

        return return_value

    # ===============================================
    def set_label_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'text', self.ui_label_id, param
        )

        return return_value

    # ===============================================
    def set_value_param(self, **param):

        command_name = None

        if self.isInteger:
            command_name = 'intField'
        else:
            command_name = 'floatField'

        return_value = utility.maya.base.other.exec_maya_param(
            command_name, self.ui_value_id, param
        )

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = setting.load(
            setting_key + '_Value', float, self.default_value)

        self.set_value(this_value)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = self.get_value()

        setting.save(setting_key + '_Value', this_value)
