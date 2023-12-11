# -*- coding: utf-8 -*-
"""
新規クラス作成用テンプレート
ここに説明を入れる
"""

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class
# from ....base_common import utility as base_utility  # 必要になったらコメントを外してください

from .. import main_template
from .. import ui as chara_util_ui
from . import template_classes


class Main(main_template.Main):
    """
    """

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        # ツール名
        self.tool_name = 'GlpTemplateClasses'
        # frameLayout/個別windowのラベルに表示するラベル
        self.tool_label = 'テンプレートクラス'
        # ツール更新日
        self.tool_version = '19121101'

        # シェルフに登録用のコマンドを入れる
        # _create_shelf_func_command_str -> クラスと同階層の関数を実行するコマンドを作成する
        # _create_shelf_command_str -> クラス内の関数を実行するコマンドを作成する
        self.sub_shelf_command_param_list = [
            {
                'label': 'クラスと同階層の関数を実行する',
                'command': self._create_shelf_func_command_str(
                    'template_classes',
                    'template_exec_cmd'
                )
            },
            {
                'label': 'クラス内の関数を実行する',
                'command': self._create_shelf_command_str(
                    'template_classes',
                    'exec_cmd'
                )
            }
        ]

        # シェルフコマンドから「windowを開く」で実行したときの初期windowの大きさ
        # 500, 300から変えなくても大丈夫な場合は消しても問題なし
        # また、windowの大きさを変更したときは自動的に値が変更される
        self.default_single_window_width = 500
        self.default_single_window_height = 300

        # base_common.satting.Settingはself.settingとしてオーバーライド元で指定されているので
        # ここで呼び出さなくても大丈夫

        self.template_classes = template_classes.TemplateClasses()

    def save_setting(self):
        """
        windowを閉じたときにセーブしたい項目を入力する
        """

        pass

    def load_setting(self):
        """
        windowを開いたときにロードしたい項目を入力する
        呼び出されるタイミングはUIが全て作成された後
        """

        pass

    def ui_body(self):
        """
        ここにframeLayout内のUIを入力する
        frameLayoutは大元で作成されているのでここで書かなくても大丈夫
        """

        cmds.columnLayout(adj=True, rs=5)

        cmds.button(l='ボタンテスト')
        cmds.button(l='ボタンテスト', c=self.template_classes.exec_cmd)
        base_class.ui.button.Button('ボタンテスト', self.template_classes.exec_cmd)

        cmds.setParent('..')

        # レイアウトに合わせて均等割りな横並びのボタンを作りたい時などに利用する
        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('ボタン1', self.template_classes.exec_cmd, '引数ここ')
        _button_row_layout.set_button('ボタン2', self.template_classes.exec_cmd, '引数複数も', '行けるよ')
        _button_row_layout.show_layout()
