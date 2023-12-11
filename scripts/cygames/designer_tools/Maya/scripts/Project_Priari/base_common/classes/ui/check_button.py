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
class CheckButton(object):

    # ===============================================
    def __init__(self, on_label, off_label, is_on, change_function=None, *change_function_arg, **button_edit_param):

        self.ui_button_id = base_utility.string.get_random_string(16)

        self.__change_function = change_function
        self.__change_function_arg = change_function_arg

        self.__on_label = on_label
        self.__off_label = off_label

        self.__on_color = [0.7] * 3
        self.__off_color = [0.4] * 3

        self.__current_value = is_on

        self.__draw()

        if button_edit_param:
            button_edit_param['edit'] = True
            self.apply_button_param(**button_edit_param)

        self.set_label(self.__on_label, self.__off_label)
        self.set_bg_color(self.__on_color, self.__off_color)

    # ===============================================
    def __draw(self):

        cmds.button(self.ui_button_id, c=self.__execute_change_function)

        self.__update_ui()

    # ==================================================
    def __update_ui(self):

        if self.__current_value:

            cmds.button(self.ui_button_id,
                         e=True, label=self.__on_label, bgc=self.__on_color)

        else:

            cmds.button(self.ui_button_id,
                         e=True, label=self.__off_label, bgc=self.__off_color)

    # ==================================================
    def __execute_change_function(self, value):

        self.__current_value = not self.__current_value

        self.__update_ui()

        if self.__change_function is None:
            return

        self.__change_function(*self.__change_function_arg)

    # ==================================================
    def set_change_function(self, function, *arg):

        self.__change_function = function
        self.__change_function_arg = arg

    # ==================================================
    def set_value(self, value, execute_function=False):

        self.__current_value = value

        self.__update_ui()

        if execute_function:

            self.__execute_change_function(None)

    # ==================================================
    def get_value(self):

        this_label = self.apply_button_param(q=True, l=True)

        if not this_label:
            return False

        if this_label == self.__on_label:
            return True

        return False

    # ==================================================
    def set_bg_color(self, on_color, off_color):

        if on_color:
            self.__on_color = on_color

        if off_color:
            self.__off_color = off_color

        self.__update_ui()

    # ===============================================
    def set_label(self, on_label, off_label):

        if on_label:
            self.__on_label = on_label

        if off_label:
            self.__off_label = off_label

        self.__update_ui()

    # ===============================================
    def apply_button_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'button', self.ui_button_id, **param)

        return return_value
