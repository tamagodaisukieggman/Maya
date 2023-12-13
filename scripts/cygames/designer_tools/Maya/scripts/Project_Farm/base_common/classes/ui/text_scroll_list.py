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

from ... import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextScrollList(object):

    # ===============================================
    def __init__(self, **text_scroll_list_edit_param):

        self.ui_text_scroll_list_id = base_utility.string.get_random_string(16)

        self.__select_function = None
        self.__select_function_arg = None

        self.__double_click_function = None
        self.__double_click_function_arg = None

        self.selected_index = 0
        self.selected_index_list = None

        self.selected_item = None
        self.selected_item_list = None

        self.__draw()

        if text_scroll_list_edit_param:
            text_scroll_list_edit_param['edit'] = True
            self.apply_text_scroll_list_param(**text_scroll_list_edit_param)

    # ===============================================
    def __draw(self):

        cmds.textScrollList(
            self.ui_text_scroll_list_id,
            ams=True,
            sc=self.__execute_select_function,
            dcc=self.__execute_double_click_function)

    # ==================================================
    def __execute_select_function(self):

        self.__update_select_info()

        if self.__select_function is None:
            return

        self.__select_function(*self.__select_function_arg)

    # ==================================================
    def __update_select_info(self):

        self.selected_index_list = cmds.textScrollList(
            self.ui_text_scroll_list_id,
            q=True,
            sii=True)

        if not self.selected_index_list:
            self.selected_index_list = []
            self.selected_index = -1
        else:
            self.selected_index = self.selected_index_list[0] - 1

            for p in range(len(self.selected_index_list)):
                self.selected_index_list[p] -= 1

        self.selected_item_list = cmds.textScrollList(
            self.ui_text_scroll_list_id,
            q=True,
            si=True)

        if not self.selected_item_list:
            self.selected_item_list = []
            self.selected_item = ''
        else:
            self.selected_item = self.selected_item_list[0]

    # ==================================================
    def set_select_function(self, function, *arg):

        self.__select_function = function
        self.__select_function_arg = arg

    # ==================================================
    def __execute_double_click_function(self):

        if self.__double_click_function is None:
            return

        self.__double_click_function(*self.__double_click_function_arg)

    # ==================================================
    def set_double_click_function(self, function, *arg):

        self.__double_click_function = function
        self.__double_click_function_arg = arg

    # ==================================================
    def add_item_list(self, target_item_list):

        if not target_item_list:
            return

        for cnt in range(0, len(target_item_list)):

            cmds.textScrollList(
                self.ui_text_scroll_list_id,
                e=True,
                a=target_item_list[cnt]
            )

    # ==================================================
    def remove_item_list(self, target_item_list):

        if not target_item_list:
            return

        for cnt in range(0, len(target_item_list)):

            cmds.textScrollList(
                self.ui_text_scroll_list_id,
                e=True,
                ri=target_item_list[cnt]
            )

    # ==================================================
    def set_item_list(self, target_item_list):

        self.remove_all_item()
        self.add_item_list(target_item_list)

    # ==================================================
    def remove_all_item(self):

        cmds.textScrollList(self.ui_text_scroll_list_id, e=True, ra=True)

    # ==================================================
    def select_item_list(self, target_item_list):

        if not target_item_list:
            return

        for target_item in target_item_list:

            cmds.textScrollList(
                self.ui_text_scroll_list_id,
                e=True,
                si=target_item
            )

        self.__execute_select_function()

    # ==================================================
    def deselect_item_list(self, target_item_list):

        if not target_item_list:
            return

        for target_item in target_item_list:

            cmds.textScrollList(
                self.ui_text_scroll_list_id,
                e=True,
                di=target_item
            )

        self.__execute_select_function()

    # ==================================================
    def select_all_item(self):

        all_item_list = cmds.textScrollList(
            self.ui_text_scroll_list_id, q=True, ai=True)

        if not all_item_list:
            return

        self.select_item_list(all_item_list)

    # ==================================================
    def deselect_all_item(self):

        cmds.textScrollList(self.ui_text_scroll_list_id, e=True, da=True)

        self.__execute_select_function()

    # ===============================================
    def apply_text_scroll_list_param(self, **param):

        return_value = base_utility.system.exec_maya_command(
            'textScrollList', self.ui_text_scroll_list_id, **param)

        return return_value
