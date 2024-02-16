# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Button(object):

    # ===============================================
    def __init__(self, label, function=None, arg=None):

        self.ui_id = None

        self.function = function
        self.function_arg = arg

        self.__create_ui()

        self.set_label(label)
        self.set_size([None, 30])
        self.set_function(self.function, self.function_arg)

    # ===============================================
    def __create_ui(self):

        self.ui_id = cmds.button(c=self.__execute_function)

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

        cmds.button(self.ui_id, e=True, bgc=color)

    # ===============================================
    def set_label(self, label):

        cmds.button(self.ui_id, e=True, label=label)

    # ===============================================
    def set_size(self, size):

        if size[0] is not None:
            cmds.button(self.ui_id, e=True, width=size[0])

        if size[1] is not None:
            cmds.button(self.ui_id, e=True, height=size[1])

    # ===============================================
    def set_visible(self, visible):

        cmds.button(self.ui_id, e=True, vis=visible)

    # ===============================================
    def set_enable(self, enable):

        cmds.button(self.ui_id, e=True, en=enable)

    # ===============================================
    def set_info(self, info):

        cmds.button(self.ui_id, e=True, ann=info)
