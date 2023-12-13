# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
except:
    pass

import os

import maya.cmds as cmds

from . import vtx_color_utility
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'FarmVtxColorUtility'
        self.tool_label = '頂点カラー補助ツール'
        self.tool_version = '22091401'

        self.axis_menue = None
        self.precision_field = None

        self.color_prisets = [
            [1, 1, 1],
            [0.7, 0.7, 0.7],
            [0, 1, 1],
            [0, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
            [1, 0.99, 1],
        ]

        self.axis_dict_list = [
            {
                'label': '+x',
                'axis': 'x',
                'is_positive': True
            },
            {
                'label': '-x',
                'axis': 'x',
                'is_positive': False
            },
            {
                'label': '+y',
                'axis': 'y',
                'is_positive': True
            },
            {
                'label': '-y',
                'axis': 'y',
                'is_positive': False
            },
            {
                'label': '+z',
                'axis': 'z',
                'is_positive': True
            },
            {
                'label': '-z',
                'axis': 'z',
                'is_positive': False
            },
        ]

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.frameLayout(l='頂点カラー調整', cll=1, cl=0, bv=1, mw=5, mh=5)

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()

        for color in self.color_prisets:
            label = ','.join([str(x) for x in color])
            _button_row_layout.set_button(label, vtx_color_utility.set_color_to_selected_vtx, color, bgc=color)
        _button_row_layout.show_layout()

        cmds.rowLayout(numberOfColumns=3, adj=2)
        cmds.text(label='カラー変換')
        _button_row_layout2 = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout2.set_button('緑から0.99', self.__color_change_func, [0, 1, 0], [1, 0.99, 1])
        _button_row_layout2.set_button('0.99から緑', self.__color_change_func, [1, 0.99, 1], [0, 1, 0])
        _button_row_layout2.show_layout()
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.frameLayout(l='頂点カラーミラーリング', cll=1, cl=0, bv=1, mw=5, mh=5)

        cmds.rowLayout(numberOfColumns=4)

        cmds.text(label='ミラー元の範囲')

        self.axis_menue = cmds.optionMenu()
        for axis_dict in self.axis_dict_list:
            cmds.menuItem(label=axis_dict['label'])

        cmds.text(label='精度')

        self.precision_field = cmds.floatField(min=0.0, v=0.001)

        cmds.setParent('..')

        _button_row_layout3 = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout3.set_button('頂点カラーミラーリング', self.__vtx_color_mirror, None)
        _button_row_layout3.show_layout()

        cmds.setParent('..')

    def __color_change_func(self, rgb1, rgb2):
        vtx_color_utility.replace_vtx_color(rgb1, rgb2)

    def __vtx_color_mirror(self, arg):

        axis_label = cmds.optionMenu(self.axis_menue, q=True, value=True)
        precision = cmds.floatField(self.precision_field, q=True, v=True)
        axis = ''
        is_positive = None

        for axis_dict in self.axis_dict_list:
            if axis_dict['label'] == axis_label:
                axis = axis_dict['axis']
                is_positive = axis_dict['is_positive']
                break

        if not axis:
            return

        vtx_color_utility.symmetry_vtx_color(axis, is_positive, precision)
