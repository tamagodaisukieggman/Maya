# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function
"""
フェイシャルのプレビューを行う
"""

import os

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....farm_common.classes.info import facial_info
# from ....base_common import utility as base_utility  # 必要になったらコメントを外してください

from .. import main_template
from .. import ui as chara_util_ui
# from . import template_classes


class Main(main_template.Main):
    """
    """

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        # ツール名
        self.tool_name = 'FarmFacialViewer'
        self.tool_label = 'フェイシャルビュワー'
        # ツール更新日
        self.tool_version = '20111301'

        self.facial_info = facial_info.FacialInfo()
        self.facial_info.create_info()

        self.ui_upper_layout = None
        self.ui_lower_layout = None
        self.ui_current_label = None

    # ==================================================
    def ui_body(self):

        update_button = base_class.ui.button.Button(
            'フェイシャルビュワーを更新',
            self.update_ui)

        # if not self.facial_info.facial_item_dict_list:
        #     cmds.text(l='表示できる表情がありません')
        #     return

        self.ui_upper_layout = cmds.rowColumnLayout(numberOfColumns=4)

        self.__create_facial_change_buttons()

        cmds.setParent('..')

        self.ui_lower_layout = cmds.rowLayout(
            numberOfColumns=4,
            columnWidth4=(100, 80, 100, 100),
            adjustableColumn=3,
            columnAlign=(2, 'right'),
            columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)]
        )

        previous_button = base_class.ui.button.Button(
            '<',
            self.change_facial_previous,
            width=100)

        cmds.text(l='現在の表情:')

        self.ui_current_label = cmds.textField(tx='', ed=False)
        self.__update_current_label()

        next_button = base_class.ui.button.Button(
            '>',
            self.change_facial_next,
            width=100)

        cmds.setParent('..')

    # ==================================================
    def update_ui(self):

        self.facial_info = facial_info.FacialInfo()
        self.facial_info.create_info()

        upper_child_list = []
        upper_child_list = cmds.rowColumnLayout(self.ui_upper_layout, q=True, ca=True)

        if upper_child_list:
            cmds.deleteUI(upper_child_list, control=True)

        cmds.setParent(self.ui_upper_layout)

        self.__create_facial_change_buttons()

        self.__update_current_label()

    # ==================================================
    def facial_view_button_event(self, facial_item_dict):

        this_facial_index = facial_item_dict.get('index')
        self.__change_facial_by_index(this_facial_index)
        self.__update_current_label()

    # ==================================================
    def change_facial_next(self):

        item = self.facial_info.get_current_item()

        if not item:
            return ''

        current_index = item.get('index', 0)
        new_index = current_index + 1

        if new_index > len(self.facial_info.facial_item_dict_list) - 1:
            new_index = new_index - len(self.facial_info.facial_item_dict_list)

        self.__change_facial_by_index(new_index)
        self.__update_current_label()

    # ==================================================
    def change_facial_previous(self):

        item = self.facial_info.get_current_item()

        if not item:
            return ''

        current_index = item.get('index', 0)
        new_index = current_index - 1

        if new_index < 0:
            new_index = new_index + len(self.facial_info.facial_item_dict_list)

        self.__change_facial_by_index(new_index)
        self.__update_current_label()

    # ==================================================
    def __change_facial_by_index(self, index):

        self.facial_info.apply_facial(index)

    # ==================================================
    def __update_current_label(self):

        if not self.ui_current_label:
            return

        label = self.__get_current_label()

        cmds.textField(self.ui_current_label, e=True, tx=label)

    # ==================================================
    def __get_current_label(self):

        item = self.facial_info.get_current_item()

        if not item:
            return ''

        return item.get('label', '')

    # ==================================================
    def __create_facial_change_buttons(self):

        for facial_item_dict in self.facial_info.facial_item_dict_list:

            this_button = base_class.ui.button.Button(
                facial_item_dict.get('label', ''),
                self.facial_view_button_event,
                *[facial_item_dict],
                width=100)
