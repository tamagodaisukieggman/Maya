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
class CheckBox(object):

    # ===============================================
    def __init__(self, label, value, **check_box_param):

        self.ui_check_box_id = utility.base.string.get_random_string(16)

        self.default_value = value

        self.__function = None
        self.__function_arg = None

        self.__draw()

        if check_box_param:
            check_box_param['edit'] = True
            self.apply_check_box_param(**check_box_param)

        self.apply_check_box_param(e=True, label=label)
        self.set_value(value)

    # ===============================================
    def __draw(self):

        cmds.checkBox(self.ui_check_box_id, cc=self.__execute_function)

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

        return self.apply_check_box_param(q=True, v=True)

    # ===============================================
    def set_value(self, value):

        self.apply_check_box_param(e=True, v=value)

    # ===============================================
    def apply_check_box_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'checkBox', self.ui_check_box_id, param
        )

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = setting.load(
            setting_key + '_Value', bool, self.default_value)

        self.set_value(this_value)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_value = self.get_value()

        setting.save(setting_key + '_Value', this_value)
