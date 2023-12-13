# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import math
import maya.cmds as cmds

from ....base_common import utility as base_utility
from ...utility import model_id_finder as model_id_finder
from ...utility import model_define as model_define
from .. import uv_facial_part as uv_facial_part


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialInfo(object):
    """
    """

    # ===============================================
    def __init__(self):

        # ------------------------------
        # facial_item_dict_list
        # 形式は以下で統一
        # {'index': ,'label': ,'part_dict_list': [{'part_name': ,'value': }, ]}

        # unit
        self.__unit_facial_item_dict_list = [
            {'index': 0, 'label': '通常', 'part_dict_list': [{'part_name': 'unt_all', 'value': 0}, ]},
            {'index': 1, 'label': '笑顔', 'part_dict_list': [{'part_name': 'unt_all', 'value': 1}, ]},
            {'index': 2, 'label': '怒り', 'part_dict_list': [{'part_name': 'unt_all', 'value': 2}, ]},
            {'index': 3, 'label': '悲しい', 'part_dict_list': [{'part_name': 'unt_all', 'value': 3}, ]},
            {'index': 4, 'label': '照れ', 'part_dict_list': [{'part_name': 'unt_all', 'value': 4}, ]},
            {'index': 5, 'label': '驚き', 'part_dict_list': [{'part_name': 'unt_all', 'value': 5}, ]},
            {'index': 6, 'label': 'ダメージ', 'part_dict_list': [{'part_name': 'unt_all', 'value': 6}, ]},
            {'index': 7, 'label': 'スタン', 'part_dict_list': [{'part_name': 'unt_all', 'value': 7}, ]},
            {'index': 8, 'label': '綴じ目', 'part_dict_list': [{'part_name': 'unt_all', 'value': 8}, ]},
        ]

        # avatar
        self.__avatar_facial_item_dict_list = [
        ]

        # enemy
        self.__enemy_facial_item_dict_list = [
        ]

        # ------------------------------
        # 各パーツクラスのイニシャライズ情報

        # unt_all
        self.__unt_all_target = 'msh_face'
        self.__unt_all_part_tex_row = 4
        self.__unt_all_part_tex_col = 4
        self.__unt_all_part_dict_list = [
            {'index': 0, 'label': 'face01'},
            {'index': 1, 'label': 'face02'},
            {'index': 2, 'label': 'face03'},
            {'index': 3, 'label': 'face04'},
            {'index': 4, 'label': 'face05'},
            {'index': 5, 'label': 'face06'},
            {'index': 6, 'label': 'face07'},
            {'index': 7, 'label': 'face08'},
            {'index': 8, 'label': 'face09'},
        ]

        self.file_path = ''
        self.data_type = ''
        self.facial_item_list = []

        self.facial_item_dict_list = []
        self.facial_part_dict = {}

    # ===============================================
    def create_info(self):

        self.file_path = cmds.file(q=True, sn=True)
        data_types = model_id_finder.get_data_types(self.file_path)
        self.data_type = data_types[0]

        this_facial_item_dict_list = None

        if self.data_type == model_define.UNIT_DATA_TYPE:
            self.facial_item_dict_list = self.__unit_facial_item_dict_list
        elif self.data_type == model_define.AVATAR_DATA_TYPE:
            self.facial_item_dict_list = self.__avatar_facial_item_dict_list
        elif self.data_type == model_define.ENEMY_DATA_TYPE:
            self.facial_item_dict_list = self.__enemy_facial_item_dict_list
        else:
            return

        for facial_item_dict in self.facial_item_dict_list:

            part_dict_list = facial_item_dict.get('part_dict_list')

            if not part_dict_list:
                continue

            for part_value_dict in part_dict_list:

                part_name = part_value_dict.get('part_name', '')
                facial_part = None

                if part_name == 'unt_all':
                    facial_part = self.__create_uv_facial_part(
                        'unt_all',
                        self.__unt_all_target,
                        self.__unt_all_part_tex_row,
                        self.__unt_all_part_tex_col,
                        self.__unt_all_part_dict_list,
                    )

                self.facial_part_dict[part_name] = facial_part

    # ===============================================
    def get_current_item(self):

        current_item_dict = None

        if not self.facial_item_dict_list:
            return current_item_dict

        for facial_item_dict in self.facial_item_dict_list:

            is_current_facial = True
            part_dict_list = facial_item_dict['part_dict_list']

            for part_value_dict in part_dict_list:

                part_name = part_value_dict.get('part_name', '')
                value = part_value_dict.get('value', None)
                current_value = None

                # facial_partのクラス名ごとに現在のvalueの取得の仕方を定義
                facial_part = self.facial_part_dict.get(part_name)

                if facial_part.__class__.__name__ == 'UvFacialPart':
                    current_value = facial_part.current_index

                if not current_value == value:
                    is_current_facial = False
                    break

            if is_current_facial:
                current_item_dict = facial_item_dict
                break

        return current_item_dict

    # ===============================================
    def apply_facial(self, index):

        if not self.facial_item_dict_list or not self.facial_part_dict:
            return

        target_item_dict = None
        for facial_item_dict in self.facial_item_dict_list:

            this_index = facial_item_dict.get('index', '')

            if this_index == index:
                target_item_dict = facial_item_dict
                break

        if not target_item_dict:
            return

        part_dict_list = target_item_dict['part_dict_list']

        for part_value_dict in part_dict_list:

            part_name = part_value_dict.get('part_name', '')
            value = part_value_dict.get('value', None)

            # facial_partのクラス名ごとに現在のvalueの取得の仕方を定義
            facial_part = self.facial_part_dict.get(part_name)

            if not facial_part:
                continue

            if facial_part.__class__.__name__ == 'UvFacialPart':
                current_value = facial_part.apply_value(value)

    # ===============================================
    def __create_uv_facial_part(self, label, target_name, row_count, col_count, index_label_dict_list):

        target_meshs = cmds.ls(target_name, type='transform', l=True)

        if not target_meshs:
            return

        target_mesh = target_meshs[0]

        part = uv_facial_part.UvFacialPart()
        part.create_info(
            label='unt_all',
            target_mesh=target_mesh,
            row_count=row_count,
            col_count=col_count,
            index_label_dict_list=index_label_dict_list,
        )

        return part
