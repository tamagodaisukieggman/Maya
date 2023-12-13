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
import re

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....glp_common.classes.info import chara_info as chara_info
from ....glp_common.classes.path_finder import path_finder as path_finder

from . import transfer_to_unity
from .. import main_template
from .. import ui as chara_util_ui

reload(chara_info)
reload(path_finder)
reload(transfer_to_unity)


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpTransferToUnity'
        self.tool_label = 'Unity転送'
        self.tool_version = '19112201'

        self.ui_unity_assets_dir_path = None
        self.unity_asset_dir_path_setting_key = 'Setting{}'.format(self.tool_name)
        self.transfer_general_tail_id = None

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

        cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 80), adjustableColumn=1, columnAlign=(1, 'left'))
        self.init_general_tail_list()
        cmds.button(label='現在のシーンに合わせて更新', command=self.init_general_tail_list)
        cmds.setParent("..")

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('モデル、テクスチャ転送', self.transfer_to_unity, 'both')
        _button_row_layout.set_button('モデル転送', self.transfer_to_unity, 'model')
        _button_row_layout.show_layout()

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('テクスチャ転送', self.transfer_to_unity, 'texture')
        _button_row_layout.set_button('クロス転送', self.transfer_to_unity, 'cloth')
        _button_row_layout.show_layout()

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('フレア転送', self.transfer_to_unity, 'flare')
        _button_row_layout.show_layout()

        _button_row_layout = chara_util_ui.button_row_layout.ButtonRowLayout()
        _button_row_layout.set_button('エクステンション転送', self.transfer_to_unity, 'extensions')
        _button_row_layout.show_layout()

        cmds.setParent("..")

    def transfer_to_unity(self, data_type):
        """
        """

        unity_asset_dir_path = self.ui_unity_assets_dir_path.get_path()
        data_type = data_type
        tail_id = cmds.optionMenuGrp(self.transfer_general_tail_id, q=True, value=True)

        transporter = transfer_to_unity.TransferToUnity()
        transporter.initialize(unity_asset_dir_path, data_type, tail_id)
        transporter.transfer_to_unity()

    def init_general_tail_list(self, arg=None):
        """
        """

        org_value = None

        if not self.transfer_general_tail_id:
            self.transfer_general_tail_id = cmds.optionMenuGrp(
                label='※汎用尻尾 転送するキャラID ', columnAlign=[1, 'left'], adjustableColumn=2)
        else:
            # 現在選択中の値を保持
            org_value = cmds.optionMenuGrp(self.transfer_general_tail_id, q=True, value=True)

            # 一度アイテムを消去
            item_list = cmds.optionMenuGrp(self.transfer_general_tail_id, q=True, ill=True)
            if item_list:
                cmds.deleteUI(item_list)

        select_value = None

        # テクスチャのあるidをリストに追加
        id_list = self.__create_file_exist_id_list()
        if not id_list:
            # itemがなければ空を入れる
            cmds.menuItem(label='', parent=(self.transfer_general_tail_id + '|OptionMenu'))
        else:
            for chara_id in id_list:
                cmds.menuItem(label=chara_id, parent=(self.transfer_general_tail_id + '|OptionMenu'))

                if chara_id == org_value:
                    select_value = chara_id

        # 選択の復元
        if select_value:
            cmds.optionMenuGrp(self.transfer_general_tail_id, e=True, value=select_value)

    def __create_file_exist_id_list(self):
        """
        """

        this_info = chara_info.CharaInfo()
        this_info.create_info()

        if not this_info.exists or this_info.data_type.find('general_tail') < 0:
            return []

        tail_main_id = this_info.part_info.main_id
        tail_sub_id = this_info.part_info.sub_id
        tail_data_id = this_info.part_info.data_id

        finder = path_finder.PathFinder('tail', '{}_{}'.format(tail_main_id, tail_sub_id), is_mini=this_info.part_info.is_mini)
        tex_path_list = finder.texture_list

        if not tex_path_list:
            return []

        id_list = []
        for tex_path in tex_path_list:

            tex_file_name = os.path.basename(tex_path)
            match_obj = re.search(tail_data_id + r'_([0-9]{4})_', tex_file_name)

            if not match_obj:
                continue

            this_id = match_obj.group(1)

            if this_id not in id_list:
                id_list.append(this_id)

        return id_list

