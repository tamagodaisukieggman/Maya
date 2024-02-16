# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import os
import maya.cmds as cmds

from . import transfer_normal
from .. import main_template
from .. import ui as chara_util_ui

reload(transfer_normal)
reload(main_template)
reload(chara_util_ui)


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpCharaUtilityTransferNormal'
        self.tool_label = '法線転写'
        self.tool_version = '22060601'

        self.transfer_normal = transfer_normal.TransferNormal()

    def ui_body(self):
        """
        UI要素のみ
        """

        template_button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        cmds.text(label='bake_face.maテンプレートの法線を使い M_Face と M_Hair の法線をスムースにします\n' +
                  '実行対象のオブジェクトを選択して実行して下さい', align='left')
        template_button_row_layout.set_button('テンプレートから転写', self.transfer_normal.tarnsfer_normal)
        template_button_row_layout.set_button('テンプレートのインポート', self.transfer_normal.import_template_mesh)
        template_button_row_layout.show_layout()

        normal_button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        cmds.text(label='法線設定（フェースを選択して実行してください）', align='left')
        normal_button_row_layout.set_button('唇', self.transfer_normal.set_normal_to_lips)
        normal_button_row_layout.set_button('口下', self.transfer_normal.set_normal_to_mouth_shade)
        normal_button_row_layout.show_layout()
