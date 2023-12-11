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

import maya.cmds as cmds

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Button(object):

    # ===============================================
    def __init__(self, label, on_function, *on_function_arg, **button_edit_param):

        self.ui_button_id = base_utility.string.get_random_string(16)

        self.__on_function = on_function
        self.__on_function_arg = on_function_arg

        self.__draw()

        self.set_on_function(on_function, *on_function_arg)

        if button_edit_param:
            button_edit_param['edit'] = True
            self.apply_button_param(**button_edit_param)

        self.apply_button_param(e=True, label=label)

    # ===============================================
    def __draw(self):

        cmds.button(self.ui_button_id, c=self.__execute_on_function)

    # ===============================================
    def __execute_on_function(self, value):

        if not self.__on_function:
            return

        self.__on_function(*self.__on_function_arg)

    # ===============================================
    def set_on_function(self, function, *arg):

        self.__on_function = function
        self.__on_function_arg = arg

    # ===============================================
    def apply_button_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'button', self.ui_button_id, **param)

        return return_value
