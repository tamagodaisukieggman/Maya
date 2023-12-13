# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility

from . import move_chara_light
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'FarmCharaUtilityMoveCharaLight'
        self.tool_label = 'CharaLight0の操作'
        self.tool_version = '19112201'

        self.move_chara_light_class = move_chara_light.MoveCharaLight()

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button('カメラフォロー', self.follow_chara_light_to_persp)
        cmds.setParent('..')

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('ライト周回(low)', self.move_chara_light, ['low'])
        _button_row_layout.set_button('ライト周回(middle)', self.move_chara_light, ['middle'])
        _button_row_layout.set_button('ライト周回(high)', self.move_chara_light, ['high'])
        _button_row_layout.set_button('ライト周回(user)', self.move_chara_light, ['user'])
        _button_row_layout.show_layout()

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('左45度に移動', self.set_chara_light_transform, ['side', 'left', 'middle'])
        _button_row_layout.set_button('右45度に移動', self.set_chara_light_transform, ['side', 'right', 'middle'])
        _button_row_layout.set_button('左90度に移動', self.set_chara_light_transform, ['half', 'left', 'middle'])
        _button_row_layout.set_button('右90度に移動', self.set_chara_light_transform, ['half', 'right', 'middle'])
        _button_row_layout.show_layout()

    def move_chara_light(self, args):
        """
        """

        base_utility.select.save_selection()

        light_height = args[0]

        self.move_chara_light_class.chara_light_anim(light_height)

        base_utility.select.load_selection()

    def set_chara_light_transform(self, args):
        """
        """

        base_utility.select.save_selection()

        shadow_angle = args[0]
        light_direction = args[1]
        light_height = args[2]

        self.move_chara_light_class.set_chara_light_transform(shadow_angle, light_direction, light_height)

        base_utility.select.load_selection()

    def follow_chara_light_to_persp(self):
        """
        """

        base_utility.select.save_selection()

        self.move_chara_light_class.follow_light_to_persp()

        base_utility.select.load_selection()
