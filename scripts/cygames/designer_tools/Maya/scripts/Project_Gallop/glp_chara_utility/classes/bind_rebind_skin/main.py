# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from . import bind_rebind_skin
from .. import main_template
from .. import ui as chara_util_ui


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpBindRebindSkin'
        self.tool_label = 'スキンのバインド・リバインド'
        self.tool_version = '19112201'

        self.sub_shelf_command_param_list = [
            {
                'label': '全ての子ジョイントを含んでバインド',
                'command': self._create_shelf_func_command_str(
                    'bind_rebind_skin',
                    'bind_to_all_child_joints'
                )
            },
            {
                'label': 'リバインド',
                'command': self._create_shelf_func_command_str(
                    'bind_rebind_skin',
                    'rebind_skin'
                )
            }
        ]

    def ui_body(self):
        """
        UI要素のみ
        """

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('全ての子ジョイントを含んでバインド', bind_rebind_skin.bind_to_all_child_joints)
        _button_row_layout.show_layout()

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('リバインド', bind_rebind_skin.rebind_skin)
        _button_row_layout.show_layout()
