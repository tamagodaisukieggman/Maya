# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UICheckBox(object):

    # ===============================================
    def __init__(self, label, value, function=None, arg=None):

        self.ui_id = None

        self.function = function
        self.function_arg = arg

        self.__draw()

        self.set_label(label)
        self.set_value(value)
        self.set_function(self.function, self.function_arg)

    # ===============================================
    def __draw(self):

        self.ui_id = cmds.checkBox(cc=self.__execute_function)

    # ===============================================
    def __execute_function(self, value):

        if self.function is None:
            return

        if self.function_arg is None:
            self.function()
            return

        self.function(self.function_arg)

    # ===============================================
    def set_function(self, function, arg=None):

        self.function = function
        self.function_arg = arg

    # ===============================================
    def set_bg_color(self, color):

        cmds.checkBox(self.ui_id, e=True, bgc=color)

    # ===============================================
    def set_label(self, label):

        cmds.checkBox(self.ui_id, e=True, label=label)

    # ===============================================
    def set_size(self, size):

        if size is None:
            return

        if size[0] is not None:
            cmds.checkBox(self.ui_id, e=True, width=size[0])

        if size[1] is not None:
            cmds.checkBox(self.ui_id, e=True, height=size[1])

    # ===============================================
    def set_value(self, value):

        cmds.checkBox(self.ui_id, e=True, v=value)

    # ===============================================
    def get_value(self):

        return cmds.checkBox(self.ui_id, q=True, v=True)
