# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds

from . import button


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RadioButton(object):

    # ===============================================
    def __init__(self, label_list, function=None, arg=None):

        self.ui_id = None

        self.label_list = label_list
        self.ui_button_list = None

        self.function = function
        self.function_arg = arg

        self.current_index = 0

        self.active_color = [0.8] * 3
        self.deactive_color = [0.4] * 3

        self.__create_ui()

        self.set_label(self.label_list)
        self.set_size([100, None])
        self.set_function(self.function, self.function_arg)

    # ===============================================
    def __create_ui(self):

        self.ui_button_list = []

        function_list = []
        function_list.append(self.__execute_function0)
        function_list.append(self.__execute_function1)
        function_list.append(self.__execute_function2)
        function_list.append(self.__execute_function3)
        function_list.append(self.__execute_function4)
        function_list.append(self.__execute_function5)

        self.ui_id = cmds.rowLayout(nc=len(self.label_list))

        for p in range(len(self.label_list)):

            this_ui_button = cmds.button(c=function_list[p])

            self.ui_button_list.append(this_ui_button)

        cmds.setParent('..')

        self.__update_current_button()

    # ===============================================
    def __execute_function0(self, value):

        self.current_index = 0

        self.__execute_function()

    # ===============================================
    def __execute_function1(self, value):

        self.current_index = 1

        self.__execute_function()

    # ===============================================
    def __execute_function2(self, value):

        self.current_index = 2

        self.__execute_function()

    # ===============================================
    def __execute_function3(self, value):

        self.current_index = 3

        self.__execute_function()

    # ===============================================
    def __execute_function4(self, value):

        self.current_index = 4

        self.__execute_function()

    # ===============================================
    def __execute_function5(self, value):

        self.current_index = 5

        self.__execute_function()

    # ===============================================
    def __execute_function(self):

        self.__update_current_button()

        if self.function is None:
            return

        if self.function_arg is None:
            self.function(self.current_index)
            return

        self.function(self.current_index, self.function_arg)

    # ===============================================
    def __update_current_button(self):

        for p in range(len(self.ui_button_list)):

            cmds.button(
                self.ui_button_list[p], e=True,
                bgc=self.deactive_color, en=True)

            if p == self.current_index:

                cmds.button(
                    self.ui_button_list[p], e=True,
                    bgc=self.active_color, en=False)

    # ===============================================
    def set_function(self, function, arg=None):

        self.function = function
        self.function_arg = arg

    # ===============================================
    def set_current_index(self, index, execute_function=False):

        self.current_index = index

        self.__update_current_button()

        if execute_function:
            self.__execute_function()

    # ===============================================
    def set_active_color(self, active_color):

        if active_color is None:
            return

        self.active_color = active_color

        self.__update_current_button()

    # ===============================================
    def set_deactive_color(self, deactive_color):

        if deactive_color is None:
            return

        self.deactive_color = deactive_color

        self.__update_current_button()

    # ===============================================
    def set_label(self, label_list):

        for p in range(len(self.ui_button_list)):

            if label_list[p] is None:
                continue

            cmds.button(self.ui_button_list[p], e=True, label=label_list[p])

    # ===============================================
    def set_size(self, size):

        for p in range(len(self.ui_button_list)):

            if size[0] is not None:
                cmds.button(self.ui_button_list[p], e=True, w=size[0])

            if size[1] is not None:
                cmds.button(self.ui_button_list[p], e=True, h=size[1])

    # ===============================================
    def set_visible(self, visible):

        cmds.rowLayout(self.ui_id, e=True, vis=visible)

    # ===============================================
    def set_enable(self, enable):

        cmds.rowLayout(self.ui_id, e=True, en=enable)
