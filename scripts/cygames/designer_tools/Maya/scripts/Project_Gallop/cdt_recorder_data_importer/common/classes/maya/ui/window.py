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
class Window(object):

    # ===============================================
    def __init__(self, ui_window_id, **window_param):

        self.ui_window_id = ui_window_id

        self.__ui_form_layout = None

        self.__ui_header_root = None
        self.ui_header_main = None

        self.__ui_body_root = None
        self.ui_body_main = None

        self.__ui_footer_root = None
        self.ui_footer_main = None

        self.__show_func = None
        self.__show_func_arg = None

        self.__close_func = None
        self.__close_func_arg = None

        self.__draw()

        if window_param:
            window_param['edit'] = True
            self.apply_window_param(**window_param)

    # ===============================================
    def __draw(self):

        utility.maya.ui.window.remove_same_id_window(self.ui_window_id)

        cmds.window(
            self.ui_window_id,
            s=1,
            mnb=True,
            mxb=False,
            rtf=True,
            cc=self.__execute_close_function
        )

        self.__ui_form_layout = cmds.formLayout()

        self.__ui_header_root = cmds.columnLayout(adj=True)
        self.ui_header_main = cmds.columnLayout(adj=True)
        cmds.setParent("..")
        cmds.separator(height=5, style='in')
        cmds.setParent("..")

        self.__ui_body_root = cmds.scrollLayout(cr=True)
        self.ui_body_main = cmds.columnLayout(adj=True)
        cmds.setParent("..")
        cmds.setParent("..")

        self.__ui_footer_root = cmds.columnLayout(adj=True)
        cmds.separator(height=5, style='in')
        self.ui_footer_main = cmds.columnLayout(adj=True)
        cmds.setParent("..")
        cmds.setParent("..")

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_header_root, 'top', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_header_root, 'left', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_header_root, 'right', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_footer_root, 'left', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_footer_root, 'right', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_footer_root, 'bottom', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_body_root, 'left', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachForm=[self.__ui_body_root, 'right', 0])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachControl=[
                self.__ui_body_root, 'top', 0, self.__ui_header_root])

        cmds.formLayout(
            self.__ui_form_layout, e=True,
            attachControl=[
                self.__ui_body_root, 'bottom', 0, self.__ui_footer_root])

    # ===============================================
    def show(self):

        if not utility.maya.ui.window.exist_window(self.ui_window_id):
            self.__draw()

        self.__execute_show_function()

        cmds.showWindow(self.ui_window_id)

    # ===============================================
    def __execute_show_function(self):

        if not self.__show_func:
            return

        self.__show_func(*self.__show_func_arg)

    # ===============================================
    def set_show_function(self, function, *arg):

        self.__show_func = function
        self.__show_func_arg = arg

    # ===============================================
    def __execute_close_function(self):

        if not self.__close_func:
            return

        self.__close_func(*self.__close_func_arg)

    # ===============================================
    def set_close_function(self, function, *arg):

        self.__close_func = function
        self.__close_func_arg = arg

    # ===============================================
    def apply_window_param(self, **param):

        return_value = utility.maya.base.other.exec_maya_param(
            'window', self.ui_window_id, param
        )

        return return_value

    # ===============================================
    def load_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_width = setting.load(setting_key + '_Width', int)
        this_height = setting.load(setting_key + '_Height', int)
        this_left = setting.load(setting_key + '_Left', int)
        this_top = setting.load(setting_key + '_Top', int)

        if this_width > 10:
            self.apply_window_param(e=True, width=this_width)

        if this_height > 10:
            self.apply_window_param(e=True, height=this_height)

        if this_left > 10:
            self.apply_window_param(e=True, leftEdge=this_left)

        if this_top > 10:
            self.apply_window_param(e=True, topEdge=this_top)

    # ===============================================
    def save_setting(self, setting, setting_key):

        if not setting:
            return

        if not setting_key:
            return

        this_width = self.apply_window_param(q=True, width=True)
        this_height = self.apply_window_param(q=True, height=True)
        this_left = self.apply_window_param(q=True, leftEdge=True)
        this_top = self.apply_window_param(q=True, topEdge=True)

        setting.save(setting_key + '_Width', this_width)
        setting.save(setting_key + '_Height', this_height)
        setting.save(setting_key + '_Left', this_left)
        setting.save(setting_key + '_Top', this_top)
