# -*- coding: utf-8 -*-
"""
選択した頂点に対して、素体からweightをPositionでコピーするツール
"""

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from .. import main_template
from . import transfer_base_body_weight


class Main(main_template.Main):
    """
    """

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpTransferBaseBodyWeight'
        self.tool_label = '選択した頂点へ素体weightをPositionコピー'
        self.tool_version = '19121101'

        self.sub_shelf_command_param_list = [
            {
                'label': '選択した頂点へ素体のweightをPositionコピーする',
                'command': self._create_shelf_command_str(
                    'transfer_base_body_weight',
                    'set_base_body_weight_data'
                )
            }
        ]

        self.transfer_base_body_weight = transfer_base_body_weight.TransferBaseBodyWeight()

    def ui_body(self):
        """
        """

        cmds.columnLayout(adj=True, rs=5)

        base_class.ui.button.Button(
            '選択した頂点に素体weightデータをPositionコピー',
            self.transfer_base_body_weight.set_base_body_weight_data
        )

        cmds.setParent('..')
