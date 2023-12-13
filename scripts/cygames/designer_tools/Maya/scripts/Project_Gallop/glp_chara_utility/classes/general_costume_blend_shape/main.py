# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from . import general_costume_blend_shape
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpGeneralCostumeBlendShape'
        self.tool_label = '汎用衣装のブレンドシェイプ設定'
        self.tool_version = '19112201'

        self.sub_shelf_command_param_list = [
            {
                'label': '汎用衣装 BlendShape一発設定',
                'command': self._create_shelf_command_str(
                    'general_costume_blend_shape',
                    'set_general_costume_blend_shape'
                )
            }
        ]

    def ui_body(self):
        """
        UI要素のみ
        """

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button(
            '汎用衣装 BlendShape一発設定',
            general_costume_blend_shape.GeneralCostumeBlendShape().create_general_costume_blend_shape,
            True)
        _button_row_layout.show_layout()
