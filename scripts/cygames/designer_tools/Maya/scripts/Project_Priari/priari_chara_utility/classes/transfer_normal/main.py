# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from . import transfer_normal
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'PriariCharaUtilityTransferNormal'
        self.tool_label = '法線転写'
        self.tool_version = '19112201'

        self.transfer_normal = transfer_normal.TransferNormal()

    def ui_body(self):
        """
        UI要素のみ
        """

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('テンプレートから転写', self.transfer_normal.tarnsfer_normal)
        _button_row_layout.set_button('テンプレートのインポート', self.transfer_normal.import_template_mesh)
        _button_row_layout.show_layout()
