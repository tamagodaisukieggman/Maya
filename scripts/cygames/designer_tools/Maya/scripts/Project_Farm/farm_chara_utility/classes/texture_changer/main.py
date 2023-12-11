# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import glob
import re
from functools import partial

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility

from ....farm_common.classes.info import chara_info
from ....farm_common.classes.info import facial_info
from ....farm_common.classes.info import general_data_info

from ....farm_common.utility import model_id_finder
from ....farm_common.utility import model_define

from ..move_chara_light import move_chara_light

from . import texture_changer
from .. import main_template


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'FarmCharaUtilityTextureChanger'
        self.tool_label = 'テクスチャ・シェーダーの切り替え'
        self.tool_version = '19121901'

        self.texture_changer = texture_changer.TextureChanger(self)
        self.move_chara_light_class = move_chara_light.MoveCharaLight()

        self.dirt_rate_list = [0, 0, 0]

    def ui_body(self):
        """
        UI要素のみ
        """

        form = cmds.formLayout(numberOfDivisions=100)

        tex_layout = cmds.rowLayout(
            numberOfColumns=4, columnWidth4=(50, 50, 50, 100),
            columnAttach4=['left', 'left', 'left', 'left'],
            columnOffset4=[0, 0, 0, 50])
        base_class.ui.button.Button(
            'TGA', self.change_texture, 'default', width=50)
        base_class.ui.button.Button(
            'PSD', self.change_texture, 'psd', width=50)
        base_class.ui.button.Button(
            'CGFX', self.change_texture, 'cgfx', width=50)
        base_class.ui.button.Button(
            u"テクスチャリロード", self.reload_texture, width=100)
        cmds.setParent("..")

        outline_check_layout = cmds.rowLayout(numberOfColumns=4)
        cmds.text(label='アウトラインCGFX【確認用】', align='left', width=130)
        base_class.ui.button.Button(
            'ON', self.change_outline, 'cgfx_outline', width=50)
        base_class.ui.button.Button(
            'OFF', self.change_outline, 'cgfx_outline_default', width=50)
        cmds.text(label='※viewport2.0下ではCGFXと併用推奨')
        cmds.setParent("..")

        cmds.formLayout(
            form, e=True,
            attachForm=[
                (tex_layout, 'top', 0),
                (tex_layout, 'left', 0),
                (outline_check_layout, 'left', 0),
            ],
            attachControl=[
                (outline_check_layout, 'top', 5, tex_layout),
            ]
        )

        cmds.setParent("..")

    def change_texture(self, change_type):

        # テクスチャ切り替え
        base_utility.select.save_selection()
        self.texture_changer.change_texture(change_type)

        # cgfx表示ではないときはcharaLightRigを削除する
        if change_type not in ['cgfx']:
            self.move_chara_light_class.delete_chara_light_Rig()

        base_utility.select.load_selection()

    def change_outline(self, change_type):

        # アウトラインはフェイシャル関係ないので、シェーダーテクスチャ切り替えのみ
        base_utility.select.save_selection()
        self.texture_changer.change_texture(change_type)
        base_utility.select.load_selection()

    def reload_texture(self):

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            return

        file_node_list = cmds.ls(type="file", l=True)

        if not file_node_list:
            return

        for file_node in file_node_list:

            texture_file_path = cmds.getAttr(file_node + ".fileTextureName")
            texture_file_name = os.path.basename(texture_file_path)

            fix_texture_file_path = '{0}/{1}'.format(
                _chara_info.part_info.maya_sourceimages_dir_path,
                texture_file_name
            )

            if not os.path.isfile(fix_texture_file_path):
                continue

            cmds.setAttr(file_node + '.fileTextureName', fix_texture_file_path, type='string')
