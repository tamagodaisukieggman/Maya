# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import codecs

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CsvReader(object):

    # ===============================================
    def __init__(self):

        self.__header_index = 0

        self.__list_separator = '|'

        self.__read_line_list = None

        self.__header_dict = None

        self.__type_dict = None

        self.__all_value_list = None

    # ===============================================
    def read(self, csv_file_path, encoding='Shift-jis'):

        self.__create_read_line_list(csv_file_path, encoding)

    # ===============================================
    def update(self,
               header_define_name,
               value_end_define_name,
               header_index_offset=0,
               type_index_offset=1,
               value_start_index_offset=1):

        self.__header_dict = None
        self.__all_value_list = None

        if not self.__read_line_list:
            return

        self.__create_header_dict(
            header_define_name,
            header_index_offset,
            type_index_offset
        )

        if not self.__header_dict:
            return

        self.__create_all_value_list(
            value_start_index_offset,
            value_end_define_name,
            type_index_offset
        )

    # ===============================================
    def __create_read_line_list(self, csv_file_path, encoding):

        self.__read_line_list = None

        if not csv_file_path:
            return

        if not os.path.isfile(csv_file_path):
            return

        fopen = codecs.open(csv_file_path, 'r', encoding, 'ignore')
        csv_data = fopen.read()
        fopen.close()

        if not csv_data:
            return

        csv_data = csv_data.replace('\r', '')

        self.__read_line_list = csv_data.split('\n')

    # ===============================================
    def __create_header_dict(self,
                             header_define_name,
                             header_index_offset,
                             type_index_offset):

        self.__header_dict = None
        self.__header_index = 0

        if not self.__read_line_list:
            return

        # header_define_nameが見つからなかったら値を入れずに返す
        is_header_define = False

        if header_define_name:

            for p in range(len(self.__read_line_list)):

                this_read_line = self.__read_line_list[p]

                if this_read_line.find(header_define_name) < 0:
                    continue

                self.__header_index = p
                is_header_define = True

                break

        if not is_header_define:
            return

        self.__header_index += header_index_offset

        if self.__header_index >= len(self.__read_line_list):
            return

        header_string_list = \
            self.__read_line_list[self.__header_index].split(',')

        if not header_string_list:
            return

        self.__header_dict = {}

        for p in range(len(header_string_list)):

            header_string = header_string_list[p]

            if header_string in self.__header_dict:
                continue

            self.__header_dict[header_string] = p

        if type_index_offset < 1:
            return

        type_index = self.__header_index + type_index_offset

        if type_index >= len(self.__read_line_list):
            return

        type_string_list = \
            self.__read_line_list[type_index].split(',')

        self.__type_dict = {}

        for p in range(len(type_string_list)):

            header_string = header_string_list[p]
            type_string = type_string_list[p]

            if header_string in self.__type_dict:
                continue

            self.__type_dict[header_string] = type_string

    # ===============================================
    def __create_all_value_list(self,
                                value_start_index_offset,
                                value_end_define_name,
                                type_index_offset):

        self.__all_value_list = None

        if not self.__read_line_list:
            return

        if not self.__header_dict:
            return

        value_start_index = self.__header_index + type_index_offset + value_start_index_offset

        if value_start_index >= len(self.__read_line_list):
            return

        temp_value_list = []

        for p in range(value_start_index, len(self.__read_line_list)):

            if p < value_start_index:
                continue

            read_line = self.__read_line_list[p]

            if not read_line:
                continue

            if value_end_define_name:

                if read_line.find(value_end_define_name) >= 0:
                    break

            split_list = read_line.split(',')

            if not split_list:
                continue

            temp_value_list.append(split_list)

        if not temp_value_list:
            return

        self.__all_value_list = []

        for p in range(len(temp_value_list)):

            this_value_list = temp_value_list[p]

            for q in range(len(this_value_list)):

                this_value = this_value_list[q]

                if self.__type_dict is not None:
                    header = self.__get_key_from_value(self.__header_dict, q)
                    if header:
                        value_type = self.__type_dict[header]
                        this_value = self.__convert_variable_type(this_value, value_type)

                if q >= len(self.__all_value_list):
                    self.__all_value_list.append([])

                self.__all_value_list[q].append(this_value)

    # ===============================================
    def __get_key_from_value(self, d, val):
        keys = [k for k, v in list(d.items()) if v == val]
        if keys:
            return keys[0]

    # ===============================================
    def __convert_variable_type(self, value, value_type):
        """
        """

        try:

            if value_type.find('int') >= 0:
                value = int(value)

            elif value_type.find('float') >= 0:
                value = float(value)

            elif value_type.find('list') >= 0:
                value = value.split(self.__list_separator)

        except Exception:

            pass

        return value

    # ===============================================
    def get_index_from_value(self, header, value):

        this_value_list = self.get_value_list(header)

        if not this_value_list:
            return -1

        for p in range(len(this_value_list)):

            if this_value_list[p] != value:
                continue

            return p

        return -1

    # ===============================================
    def get_value_from_index(self, header, index):

        this_value_list = self.get_value_list(header)

        if not this_value_list:
            return

        for p in range(len(this_value_list)):

            if p != index:
                continue

            return this_value_list[p]

        return

    # ===============================================
    def get_value_list(self, header):

        if not self.__header_dict:
            return

        if not self.__all_value_list:
            return

        if not header:
            return

        if header not in self.__header_dict:
            return

        header_index = self.__header_dict[header]

        if header_index >= len(self.__all_value_list):
            return

        value_list = self.__all_value_list[header_index]

        return value_list

    # ===============================================
    def get_value_dict_list(self):

        if not self.__header_dict:
            return

        if not self.__all_value_list:
            return

        value_dict_list = []
        value_length = len(self.__all_value_list[0])
        for i in range(value_length):
            value_dict_list.append({})

        for header_string in list(self.__header_dict.keys()):

            if header_string == '':
                continue

            header_index = self.__header_dict[header_string]

            value_list = self.__all_value_list[header_index]
            for i in range(value_length):
                value_dict_list[i][header_string] = value_list[i]

        return value_dict_list
