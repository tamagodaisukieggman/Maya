# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import transfer_to_unity
from .. import main_template
from .. import ui as chara_util_ui

reload(transfer_to_unity)


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'FarmTransferToUnity'
        self.tool_label = 'Unity転送'
        self.tool_version = '19112201'

        self.ui_unity_assets_dir_path = None
        self.unity_asset_dir_path_setting_key = 'Setting{}'.format(self.tool_name)

    def save_setting(self):
        """
        """

        self.ui_unity_assets_dir_path.save_setting(self.setting, self.unity_asset_dir_path_setting_key)

    def load_setting(self):
        """
        """

        self.ui_unity_assets_dir_path.load_setting(self.setting, self.unity_asset_dir_path_setting_key)

    def ui_body(self):
        """
        UI要素のみ
        """

        self.ui_unity_assets_dir_path = base_class.ui.data_selector.DataSelector(
            "UnityAssetsパス", None, True, False
        )

        cmds.frameLayout(l=u"転送", cll=0, cl=0, bv=1, mw=5, mh=5)

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('モデル転送', self.transfer_to_unity, ['model'])
        _button_row_layout.set_button('テクスチャ転送', self.transfer_to_unity, ['texture'])
        _button_row_layout.show_layout()

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('モデル、テクスチャ転送', self.transfer_to_unity, ['model', 'texture'])
        _button_row_layout.show_layout()

        cmds.setParent("..")

    def transfer_to_unity(self, transfer_type_list):
        """
        """

        unity_asset_dir_path = self.ui_unity_assets_dir_path.get_path()

        transporter = transfer_to_unity.TransferToUnity()
        transporter.initialize(unity_asset_dir_path, transfer_type_list)
        transporter.transfer_to_unity()
