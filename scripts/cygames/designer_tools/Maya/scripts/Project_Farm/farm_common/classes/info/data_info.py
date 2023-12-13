# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except:
    pass

import os

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility
from ...utility import model_id_finder as model_id_finder
from ...utility import model_define as model_define

reload(model_id_finder)
reload(model_define)


class DataInfo(object):

    # ===============================================
    def __init__(self):
        """
        """

        self.exists = False

        self.__main_id = None
        self.__sub_id = None
        self.__data_id = None
        self.__data_type = None

        # 個別で取っていない要素用の辞書型
        # 基本的にはchara_dataに記載されているファイルはすべて取ってこれるように
        self.__data_dict = None

        self.has_weapon = None
        self.weapon_parts_count = None
        self.model_size = None
        self.bust_size = None

        self.__chara_data_csv_path = ''

    # ===============================================
    def __create_path(self):
        """
        """

        self.__script_file_path = os.path.abspath(__file__)
        __script_chara_info_path = os.path.dirname(self.__script_file_path)
        self.__script_dir_path = os.path.dirname(__script_chara_info_path)
        self.__script_root_path = os.path.dirname(self.__script_dir_path)

        self.__chara_data_csv_path = self.__script_root_path + '/_resource/chara_info/chara_data.csv'

    # ===============================================
    # TODO: 引数が増えてしまったのでCharaInfoごと受け取りたい
    def create_info(self, main_id, sub_id, data_type, data_id, is_all):
        """
        """

        self.__main_id = main_id
        self.__sub_id = sub_id
        self.__data_type = data_type
        self.__data_id = data_id

        self.__create_path()

        if not self.__create_chara_data():
            return

        if self.has_weapon:
            self.__load_weapon_data(is_all)

        self.exists = True

    def update_info(self, option={}):
        """指定されたオプションと一致する名前の変数を更新する
        """

        var_list = vars(self)

        for opt in option:
            for var in var_list:
                if var == opt:
                    setattr(self, var, option[opt])

    # ===============================================
    def __create_chara_data(self):
        """
        """

        if not os.path.exists(self.__chara_data_csv_path):
            return False

        chara_data_csv_reader = base_class.csv_reader.CsvReader()
        chara_data_csv_reader.read(self.__chara_data_csv_path, 'utf-8')
        chara_data_csv_reader.update('id', '')
        chara_data_dict_list = chara_data_csv_reader.get_value_dict_list()

        for chara_data_dict in chara_data_dict_list:

            if 'id' not in chara_data_dict:
                continue

            chara_id = chara_data_dict['id']

            if not str(chara_id).startswith(self.__main_id):
                continue

            self.has_weapon = chara_data_dict['has_weapon']
            self.model_size = chara_data_dict['model_size']
            self.bust_size = chara_data_dict['bust_size']

            self.__data_dict = chara_data_dict

            return True

        return False

    # ===============================================
    def __load_weapon_data(self, is_all):
        """
        """

        # CharaInfoのデータタイプがweaponであるか、
        # もしくはすべてのPartInfoを作成する場合のみ
        # 武器モデルデータからパーツ数を取得
        if self.__data_type == model_define.WEAPON_DATA_TYPE:
            wpn_root = '{}{}'.format(model_define.MODEL_PREFIX, self.__data_id)
            self.weapon_parts_count = self.__get_child_count(wpn_root)
        elif is_all:
            # 武器モデルデータの読み込み
            wpn_file = model_id_finder.create_scene_name(
                model_define.WEAPON_DATA_TYPE,
                self.__main_id,
                self.__sub_id)
            wpn_path = model_id_finder.get_maya_file_path(wpn_file)

            wpn_namespace = 'temp_check_wpn'
            # TODO: RootNodeの取得を関数化（要IDFinder修正）
            wpn_root = '{}:{}'.format(wpn_namespace,
                                      os.path.splitext(wpn_file)[0])

            if not os.path.exists(wpn_path):
                cmds.warning(u'Weapon file does not exist: {}'.format(wpn_path))
                return

            base_utility.reference.load(wpn_path, wpn_namespace)

            if base_utility.reference.exists(wpn_path, wpn_namespace):
                self.weapon_parts_count = self.__get_child_count(wpn_root)

            base_utility.reference.unload(wpn_path, wpn_namespace)

    # ===============================================
    def __get_child_count(self, root_node):
        """
        """

        if not root_node or not cmds.objExists(root_node):
            return 0

        return len(cmds.listRelatives(root_node))
