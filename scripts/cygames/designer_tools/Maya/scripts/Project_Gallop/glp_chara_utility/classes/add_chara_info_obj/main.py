# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import add_chara_info_obj
from .. import main_template


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpAddCharaInfoObj'
        self.tool_label = 'オブジェクトの追加'
        self.tool_version = '19112201'

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adj=True)
        base_class.ui.button.Button('IK用ロケーターの追加', self.add_ik_locator)
        cmds.setParent('..')

    def add_ik_locator(self):
        """
        """

        add_obj = add_chara_info_obj.AddCharaInfoObj()
        add_obj.add_obj('locator', 'Wrist_L_Pole')
        add_obj.add_obj('locator', 'Wrist_R_Pole')
        add_obj.add_obj('locator', 'Wrist_L_Target')
        add_obj.add_obj('locator', 'Wrist_R_Target')
