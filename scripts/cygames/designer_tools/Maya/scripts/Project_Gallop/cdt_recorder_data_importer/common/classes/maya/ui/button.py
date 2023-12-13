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
class Button(object):

    # ===============================================
    def __init__(self, label, function, *function_arg, **button_param):

        self.ui_button_id = utility.base.string.get_random_string(16)

        self.__function = function
        self.__function_arg = function_arg

        self.__draw()

        self.set_function(function, *function_arg)

        if button_param:
            button_param['edit'] = True
            self.set_button_param(**button_param)

        self.set_button_param(e=True, label=label)

    # ===============================================
    def __draw(self):

        cmds.button(self.ui_button_id, c=self.__execute_function)

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
    def set_button_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'button', self.ui_button_id, param
        )

        return return_value
