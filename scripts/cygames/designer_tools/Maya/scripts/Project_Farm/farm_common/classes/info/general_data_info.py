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

import os

from Project_Farm.base_common import classes as base_class


class GeneralDataInfo(object):

    # ===============================================
    def __init__(self):
        """
        """

        self.exists = False

        self.__script_file_path = ''
        self.__script_dir_path = ''
        self.__script_root_path = ''

        self.__chara_data_csv_path = ''
        self.__chara_data_text_csv_path = ''
        self.__chara_dress_csv_path = ''

        self.chara_data_param_list = []
        self.chara_text_param_list = []
        self.dress_param_list = []

        self.chara_id_list = []

    # ===============================================
    def __reset_param_list(self):
        """
        """

        self.chara_data_param_list = []
        self.chara_text_param_list = []
        self.dress_param_list = []

    # ===============================================
    def create_info(self):
        """
        """

        self.__create_path()

        if not self.__create_chara_data():
            self.__reset_param_list()
            return

        if not self.__create_chara_text_data():
            self.__reset_param_list()
            return

        if not self.__create_chara_dress_data():
            self.__reset_param_list()
            return

        self.exists = True

    # ===============================================
    def __create_path(self):
        """
        """

        self.__script_file_path = os.path.abspath(__file__)
        __script_chara_info_path = os.path.dirname(self.__script_file_path)
        self.__script_dir_path = os.path.dirname(__script_chara_info_path)
        self.__script_root_path = os.path.dirname(self.__script_dir_path)

        self.__chara_data_csv_path = self.__script_root_path + '/_resource/chara_info/chara_data.csv'
        self.__chara_data_text_csv_path = self.__script_root_path + '/_resource/chara_info/chara_data_text.csv'
        self.__chara_dress_csv_path = self.__script_root_path + '/_resource/chara_info/dress_data.csv'

    # ===============================================
    def __create_chara_data(self):
        """
        """

        if not os.path.exists(self.__chara_data_csv_path):
            return False

        chara_data_csv_reader = base_class.csv_reader.CsvReader()
        chara_data_csv_reader.read(self.__chara_data_csv_path, 'utf-8')
        chara_data_csv_reader.update('id', '')
        self.chara_data_param_list = chara_data_csv_reader.get_value_dict_list()

        for chara_data_param in self.chara_data_param_list:

            # 先に取っておきたい情報はここでまとめて取る
            if 'id' in chara_data_param:
                self.chara_id_list.append(chara_data_param['id'])

        return True

    # ===============================================
    def __create_chara_text_data(self):
        """
        """

        if not os.path.exists(self.__chara_data_text_csv_path):
            return False

        chara_text_csv_reader = base_class.csv_reader.CsvReader()
        chara_text_csv_reader.read(self.__chara_data_text_csv_path, 'utf-8')
        chara_text_csv_reader.update('id', '')
        self.chara_text_param_list = chara_text_csv_reader.get_value_dict_list()

        for chara_text_param in self.chara_text_param_list:

            # 先に取っておきたい情報はここでまとめて取る
            pass

        return True

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

        for dress_param in self.dress_param_list:

            # 先に取っておきたい情報はここでまとめて取る
            pass

        return True
