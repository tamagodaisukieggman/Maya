# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class ClothCollisionInfo(object):
    """
    """

    def __init__(self, file_path_list):
        """
        """

        self.file_path_list = file_path_list
        self.cloth_info = []
        self.collision_info = []

    def create_cloth_info(self):
        """
        _cloth.assetの値を格納した配列を作成する
        """

        if not self.file_path_list:
            return

        for file_path in self.file_path_list:
            this_info = self.create_info(file_path, 'springParam:', '_boneName')
            if this_info:
                self.cloth_info.extend(this_info)

    def create_collision_info(self):
        """
        _collision.assetの値を格納した配列を作成する
        """

        if not self.file_path_list:
            return

        for file_path in self.file_path_list:
            this_info = self.create_info(file_path, 'collisionParam:', '_collisionName')
            if this_info:
                self.cloth_info.extend(this_info)

    def create_info(self, file_path, target_element_name, target_header_name):
        """
        """

        element_list = []

        if not os.path.exists(file_path):
            return

        with open(file_path) as f:

            lines = f.readlines()

            elements_flag = False
            elements_depth = 0

            tmp_flag = False
            tmp_key = ''
            tmp_list = []

            child_tmp_flag = False
            child_tmp_key = ''
            child_tmp_list = []

            for line in lines:

                depth = 0

                while re.compile('\s\s' * (depth + 1)).match(line):
                    depth += 1
                    if depth > 10:
                        break

                if line.find(target_element_name) > -1:
                    elements_flag = True
                    elements_depth = depth

                    continue

                if not elements_flag:
                    continue

                line_strip = line.strip()
                line_split = re.split(':', line_strip, 1)

                item_key = ''
                item_value = ''

                if line_strip.startswith('-'):

                    depth += 1

                    if len(line_split) == 1:
                        item_key = ''
                        item_value = re.sub('-', '', line_split[0]).strip()
                    else:
                        item_key = re.sub('-', '', line_split[0]).strip()
                        item_value = line_split[1].strip()

                else:

                    item_key = line_split[0].strip()
                    item_value = line_split[1].strip()

                # ヒットしたelementと同じ階層深さのelementにhitしたら終了する
                if elements_depth != 0 and elements_depth == depth:
                    break

                if item_value.startswith('{'):
                    item_value = self.conversion_str_to_dictionary(item_value)
                elif item_value.startswith('['):
                    item_value = self.conversion_str_to_array(item_value)
                elif self.is_num(item_value):
                    item_value = float(item_value)

                if depth == elements_depth + 1:

                    if tmp_flag:
                        element_list[-1][tmp_key] = tmp_list
                        tmp_flag = False
                        tmp_key = ''
                        tmp_list = []

                    if item_key == target_header_name:
                        element_list.append({})

                    if item_key in ['_collisionNameList', '_childElements']:
                        tmp_flag = True
                        tmp_key = item_key
                        tmp_list = []
                        continue

                    elif not item_key:
                        continue

                    else:
                        element_list[-1][item_key] = item_value

                if depth == elements_depth + 2:

                    if child_tmp_flag:
                        tmp_list[-1][child_tmp_key] = child_tmp_list
                        child_tmp_flag = False
                        child_tmp_key = ''
                        child_tmp_list = []

                    if item_key == target_header_name:
                        tmp_list.append({})

                    if item_key in ['_collisionNameList']:
                        child_tmp_flag = True
                        child_tmp_key = item_key
                        child_tmp_list = []
                        continue

                    if tmp_key == '_collisionNameList':
                        tmp_list.append(item_value)
                    elif tmp_key == '_childElements':
                        tmp_list[-1][item_key] = item_value

                if depth == elements_depth + 3:

                    child_tmp_list.append(item_value)

                if depth < elements_depth:

                    if child_tmp_list:
                        tmp_list[-1][child_tmp_key] = child_tmp_list
                    if tmp_list:
                        element_list[-1][tmp_key] = tmp_list

                    break

        return element_list

    def is_num(self, value):
        """
        渡された値が数字かどうかを判別する
            :param value: 数字かどうか判断したい値
        """

        return value.replace(',', '').replace('.', '').replace('-', '').isnumeric()

    def conversion_str_to_dictionary(self, value):
        """
        str型になっている文字列を辞書型に変換する
            :param value: 辞書型に変換したい文字列
            :return: 辞書型に変換した要素
        """
        replace_value = value.replace('{', '').replace('}', '')
        split_value_list = re.split(',', replace_value)
        str_to_dict = {}
        for split_value in split_value_list:

            item = re.split(':', split_value)

            item_key = item[0].strip()
            item_value = item[1].strip()

            # valueが数値の時はfloat型に変換する
            if self.is_num(item_value):
                item_value = float(item_value)

            str_to_dict[item_key] = item_value

        return str_to_dict

    def conversion_str_to_array(self, value):
        """
        str型になっている文字列を配列に変換する
            :param value: 配列に変換したい文字列
            :return: 配列に変換した要素
        """
        replace_value = value.replace('[', '').replace(']', '')
        split_value_list = re.split(',', replace_value)
        str_to_list = []
        for split_value in split_value_list:

            value = re.sub(r'(\'|\")', '', split_value.strip())
            if not value:
                continue

            str_to_list.append(value)

        return str_to_list

    def get_target_value_list(self, key, target_type, is_get_child=False):
        """
        keyで指定した要素をすべて取得する
        """

        target_value_list = []
        element_list = []

        if target_type == 'cloth':
            element_list = self.cloth_info
        elif target_type == 'col':
            element_list = self.collision_info

        if element_list:
            for element in element_list:
                if key in element:
                    if is_get_child:
                        tmp_list = [element[key]]
                        if '_childElements' in element:
                            for child_element in element['_childElements']:
                                if key not in child_element:
                                    continue
                                tmp_list.append(child_element[key])
                        target_value_list.append(tmp_list)
                    else:
                        target_value_list.append(element[key])

        return target_value_list
