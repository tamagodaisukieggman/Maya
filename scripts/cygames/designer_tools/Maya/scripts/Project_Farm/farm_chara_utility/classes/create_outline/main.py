# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import create_outline
from .. import main_template


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'FarmCharaUtilityCreateOutline'
        self.tool_label = 'アウトラインの生成'
        self.tool_version = '19112201'

        self.create_outline = create_outline.CreateOutline()

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button(
            '現在のアウトラインの法線を使って再生成', self.create_outline.create_outline_with_current_normal)
        cmds.setParent('..')
