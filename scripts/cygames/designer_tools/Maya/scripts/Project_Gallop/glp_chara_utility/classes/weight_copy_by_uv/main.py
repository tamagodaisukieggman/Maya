# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import weight_copy_by_uv
from .. import main_template


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpCharaUtilityWeightCopyByUv'
        self.tool_label = 'UVの位置によるウェイトコピー'
        self.tool_version = '19112201'

        self.weight_copy_by_uv = weight_copy_by_uv.WeightCopyByUv()

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button('ウェイト情報をUV値を含めて取得', self.weight_copy_by_uv.copy_weight_by_uv)
        base_class.ui.button.Button('ウェイト情報からUV値でウェイトをペースト', self.weight_copy_by_uv.paste_weight_by_uv)
        cmds.setParent('..')
