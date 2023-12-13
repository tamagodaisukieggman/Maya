# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import os
from ....base_common import classes as base_class


class DataInfo(object):

    # ===============================================
    def __init__(self):
        """
        """

        self.exists = False

        self.__main_id = None
        self.__sub_id = None

        # 個別で取っていない要素用の辞書型
        # 基本的にはchara_dataに記載されているファイルはすべて取ってこれるように
        self.__data_dict = None

        self.skin_id = None
        self.shape_id = None
        self.bust_id = None
        self.mini_bust_id = None
        self.height_id = None
        self.sex_id = None

        self.chara_tail_model_id = None
        self.attachment_model_id = None

        self.dress_head_sub_id = None
        self.dress_tail_model_id = None
        self.dress_tail_model_sub_id = None

        self.dress_param_list = None

        # 利用していない情報が多いためchara_data_text_csvを削除するにあたって
        # self.chara_nameを読み込んでいるモジュールがあるため、空名対応
        self.chara_name = '※名称未登録※'
        self.voice_actor = ''

        self.birth_year = None
        self.birth_month = None
        self.birth_day = None

        self.__chara_data_csv_path = ''
        self.__chara_dress_csv_path = ''

    # ===============================================
    def __create_path(self):
        """
        """

        self.__script_file_path = os.path.abspath(__file__)
        __script_chara_info_path = os.path.dirname(self.__script_file_path)
        self.__script_dir_path = os.path.dirname(__script_chara_info_path)
        self.__script_root_path = os.path.dirname(self.__script_dir_path)

        self.__chara_data_csv_path = self.__script_root_path + '/_resource/chara_info/chara_data.csv'
        self.__chara_dress_csv_path = self.__script_root_path + '/_resource/chara_info/dress_data.csv'

    # ===============================================
    def extra_element(self, target):
        """
        """

        if target not in self.__data_dict:
            return None

        return self.__data_dict[target]

    # ===============================================
    def create_info(self, main_id, sub_id):
        """
        """

        self.__main_id = main_id
        self.__sub_id = sub_id

        self.__create_path()

        self.__create_chara_dress_data()

        if self.__main_id is None or self.__sub_id is None:
            return

        if not self.__create_chara_data():
            return

        self.exists = True

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

            self.skin_id = chara_data_dict['skin']
            self.bust_id = chara_data_dict['bust']

            # miniで使うバストid
            # SS,S=>0, M=>1, L,LL=>2
            if self.bust_id < 2:
                self.mini_bust_id = 0
            elif self.bust_id > 2:
                self.mini_bust_id = 2
            else:
                self.mini_bust_id = 1

            self.shape_id = chara_data_dict['shape']
            self.height_id = chara_data_dict['height']
            self.sex_id = chara_data_dict['sex']

            self.birth_year = chara_data_dict['birth_year']
            self.birth_month = chara_data_dict['birth_month']
            self.birth_day = chara_data_dict['birth_day']

            self.chara_tail_model_id = chara_data_dict['tail_model_id']
            self.attachment_model_id = chara_data_dict['attachment_model_id']

            self.__data_dict = chara_data_dict

            return True

        return False

    # ===============================================
    def __create_chara_dress_data(self):
        """
        """

        if not os.path.exists(self.__chara_dress_csv_path):
            return False

        chara_dress_csv_reader = base_class.csv_reader.CsvReader()
        chara_dress_csv_reader.read(self.__chara_dress_csv_path, 'utf-8')
        chara_dress_csv_reader.update('id', '')
        self.dress_param_list = chara_dress_csv_reader.get_value_dict_list()

        if self.__main_id is None or self.__sub_id is None:
            return False

        for dress_param in self.dress_param_list:

            chara_id = dress_param['chara_id']
            body_type_sub = dress_param['body_type_sub']

            if chara_id == 0:
                continue

            if int(chara_id) == int(self.__main_id) and int(body_type_sub) == int(self.__sub_id):

                # head_sub_idが1桁だと数が合わなくなってしまうので先頭に0を追加する
                tmp_head_sub_id = str(dress_param['head_sub_id'])
                if len(tmp_head_sub_id) < 2:
                    tmp_head_sub_id = '0' * (2 - len(tmp_head_sub_id)) + str(tmp_head_sub_id)
                self.dress_head_sub_id = tmp_head_sub_id

                self.dress_tail_model_id = dress_param['tail_model_id']
                self.dress_tail_model_sub_id = dress_param['tail_model_sub_id']
                return True

        return False
