# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from ....base_common import utility as base_utility

from . import eye_uv_changer
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpEyeUVChangerClass'
        self.tool_label = '目のUV展開切り替え'
        self.tool_version = '19112201'

        self.sub_shelf_command_param_list = [
            {
                'label': 'newEye',
                'command': self._create_shelf_command_str(
                    'eye_uv_changer',
                    'main',
                    '\"oldUV\"'
                )
            }
        ]

    def ui_body(self):
        """
        UI要素のみ
        """

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('UV展開を旧仕様に変更', self.change_eye_uv, 'oldUV')
        _button_row_layout.set_button('UV展開を新仕様に変更', self.change_eye_uv, 'newUV')
        _button_row_layout.show_layout()

    def change_eye_uv(self, flag):

        base_utility.select.save_selection()

        euc = eye_uv_changer.EyeUvChanger()
        euc.main(flag)

        base_utility.select.load_selection()
