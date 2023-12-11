# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import reorder_nodes as rn
from .. import main_template


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpReorderNodes'
        self.tool_label = 'アウトライナーを整理'
        self.tool_version = '23110901'

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button(
            'アウトライナーを整理', self.reorder_nodes)
        cmds.setParent('..')

    def reorder_nodes(self):
        """アウトライナーの整理
        """

        reorder_nodes = rn.ReorderNodes()
        reorder_nodes.reorder_nodes()
        reorder_nodes.apply_outliner_color()
