# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from ..base_common import utility as base_utility
from ..base_common import classes as base_class


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CheckerInfoWindow(object):

    # ==================================================
    def __init__(self, root):

        self.root = root
        self.main = root.main

        self.ui_window = None
        self.ui_header_info = None
        self.ui_scroll_list = None
        self.ui_footer_info = None

        self.info = None

        self.target_list = None

        self.view_type = None

        self.detail_separator = '     :detail>>> '

    # ==================================================
    def initialize(self):
        pass

    # ==================================================
    def show(self):

        self.create_ui()

        if self.info:
            self.ui_header_info.set_value(self.info)
        else:
            self.ui_header_info.set_value('')

        if self.target_list:

            self.ui_scroll_list.set_item_list(self.target_list)

            self.ui_footer_info.set_value(
                'リスト数 : ' + str(len(self.target_list)))

        self.ui_window.show()

    # ==================================================
    def close(self):

        if self.ui_window:
            self.ui_window.close()

    # ==================================================
    def create_ui(self):

        self.ui_window = base_class.ui.window.Window(
            'abcd', 'window', w=400, h=400, parent=self.main.checker_param_root.ui_window.ui_window_id)

        self.ui_window.set_show_function(self.show_window)
        self.ui_window.set_close_function(self.close_window)

        cmds.columnLayout(adj=True, p=self.ui_window.ui_header_layout_id)
        self.ui_header_info = base_class.ui.label.Label('')
        cmds.setParent('..')

        cmds.frameLayout(
            lv=False, p=self.ui_window.ui_body_footer_layout_id)

        self.ui_scroll_list = base_class.ui.text_scroll_list.TextScrollList()
        self.ui_scroll_list.set_select_function(self.select_textscroll_from_ui)
        self.ui_scroll_list.set_double_click_function(
            self.double_click_textscroll)

        cmds.setParent('..')

        cmds.columnLayout(adj=True, p=self.ui_window.ui_footer_layout_id)

        self.ui_footer_info = base_class.ui.label.Label('')

        cmds.rowLayout(numberOfColumns=2)

        base_class.ui.button.Button(
            '全て選択', self.on_all_select_button, w=100)

        base_class.ui.button.Button(
            '全て選択解除', self.on_all_deselect_button, w=100)

        cmds.setParent('..')

        cmds.setParent('..')

    # ==================================================
    def select_textscroll_from_ui(self):

        if self.view_type == 'explorer':
            return
        else:

            cmds.select(cl=True)

            select_list = []

            for select in self.ui_scroll_list.selected_item_list:

                this_item = select.split(self.detail_separator)[0]

                if not base_utility.node.exists(this_item):
                    continue

                select_list.append(this_item)

            if not select_list:
                return

            cmds.select(select_list, r=True)

    # ==================================================
    def double_click_textscroll(self):

        if not self.ui_scroll_list.selected_item:
            return

        this_item = self.ui_scroll_list.selected_item

        if self.view_type == 'explorer':
            base_utility.io.open_directory(this_item)
        elif self.view_type == 'attribute':
            mel.eval('ShowAttributeEditorOrChannelBox;')
        elif self.view_type == 'component':
            mel.eval('ComponentEditor;')
        elif self.view_type == 'colorset':
            mel.eval('colorSetEditor;')
        elif self.view_type == 'uvset':
            mel.eval('uvSetEditor;')
        elif self.view_type == 'uv':
            mel.eval('TextureViewWindow;')
        elif self.view_type == 'material':
            mel.eval('HypershadeWindow;')

    # ==================================================
    def on_all_select_button(self):

        self.ui_scroll_list.select_all_item()

    # ==================================================
    def on_all_deselect_button(self):

        self.ui_scroll_list.deselect_all_item()

    # ==================================================
    def show_window(self):

        self.load_setting()

    # ==================================================
    def close_window(self):

        self.save_setting()

    # ==================================================
    def load_setting(self):

        self.ui_window.load_setting(self.main.setting, 'SubWindow')

    # ==================================================
    def save_setting(self):

        self.ui_window.save_setting(self.main.setting, 'SubWindow')
