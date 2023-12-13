# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from . import open_explorer
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpCharaUtilityOpenExolorer'
        self.tool_label = 'フォルダを開く'
        self.tool_version = '19112201'

        self.open_explorer = open_explorer.OpenExplorer()

    def ui_body(self):
        """
        UI要素のみ
        """

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('rootを開く', self.open_explorer.open_explorer, 'mayaRoot')
        _button_row_layout.set_button('sceneを開く', self.open_explorer.open_explorer, 'scenes')
        _button_row_layout.set_button('sourceimagesを開く', self.open_explorer.open_explorer, 'sourceimages')
        _button_row_layout.show_layout()
