# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from . import cleanup_cmd
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'PriariCharaUtilitySceneCleaner'
        self.tool_label = 'シーンクリーナー'
        self.tool_version = '22090101'

    def ui_body(self):
        """
        UI要素のみ
        """

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('lambert1エラー解消', self.fix_initial_node)
        _button_row_layout.set_button('unknownノード&プラグイン削除', self.delete_unknown_nodes_and_plugins)
        _button_row_layout.show_layout()

    def fix_initial_node(self):
        """lambert1エラー解消
        """

        result = cleanup_cmd.fix_initial_node()
        if result:
            cmds.confirmDialog(title='', message='シーンクリーン完了')
        else:
            cmds.confirmDialog(title='', message='修正項目はありませんでした')

    def delete_unknown_nodes_and_plugins(self):
        """unknownノード&プラグイン削除
        """

        result = cleanup_cmd.delete_unknown_nodes_and_plugins()
        if result:
            cmds.confirmDialog(title='', message='シーンクリーン完了')
        else:
            cmds.confirmDialog(title='', message='修正項目はありませんでした')
