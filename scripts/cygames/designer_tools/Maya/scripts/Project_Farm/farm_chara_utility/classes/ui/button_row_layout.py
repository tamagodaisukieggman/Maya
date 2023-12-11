# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except:
    pass

import maya.cmds as cmds

from ....base_common import classes as base_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ButtonRowLayout(object):

    # ===============================================
    def __init__(self):
        """
        """

        self.button_param_list = []

    # ===============================================
    def __get_attach_controls(self):
        """
        """

        row_count = len(self.button_param_list)
        attach_controls = []

        for i in range(row_count):

            if i != row_count - 1:
                button_id = self.button_param_list[i].button.ui_button_id
                next_button_id = self.button_param_list[i + 1].button.ui_button_id
                attach_controls.append((button_id, 'right', 3, next_button_id))

        return attach_controls

    # ===============================================
    def __get_attach_positions(self):
        """
        """

        row_count = len(self.button_param_list)
        attach_positions = []

        for i in range(row_count):

            value = (100 / row_count) * i
            button_id = self.button_param_list[i].button.ui_button_id
            attach_positions.append((button_id, 'left', 0, value))
            if i == row_count - 1:
                attach_positions.append((button_id, 'right', 0, 100))

        return attach_positions

    # ===============================================
    def show_layout(self):
        """
        """

        row_count = len(self.button_param_list)
        if not row_count:
            return

        form = cmds.formLayout()

        for button_param in self.button_param_list:
            button_param.create()

        attach_controls = self.__get_attach_controls()
        attach_positions = self.__get_attach_positions()

        cmds.formLayout(
            form,
            e=True,
            attachControl=attach_controls,
            attachPosition=attach_positions)

        cmds.setParent('..')

    # ===============================================
    def set_button(self, label, function, *on_function_args, **button_edit_param):
        """
        """

        button_param = ButtonParam(label, function, on_function_args, button_edit_param)
        self.button_param_list.append(button_param)


class ButtonParam(object):

    # ===============================================
    def __init__(self, label='', function=None, args=[], params={}):
        """
        """

        self.label = label
        self.function = function
        self.args = args
        self.params = params
        self.button = None

    # ===============================================
    def create(self):

        self.button = base_class.ui.button.Button(self.label, self.function, *self.args, **self.params)
