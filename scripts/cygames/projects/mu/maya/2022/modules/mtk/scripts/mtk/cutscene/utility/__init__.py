# -*- coding: utf-8 -*-
"""description"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import re

from maya import cmds

from . import dialog
from . import panel
from . import qt
from . import mevent


def create_unique_object_name(base_name, search_type):
    """固有のオブジェクト名を作成する

    :param base_name: 生成する名前のベース名
    :type base_name: str
    :param search_type: 検索するノード名
    :type base_name: str
    :return: 存在しなければ、base_name, 存在していれば、[base_name]_[1, 2 ,3etc]
    :rtype: str
    """
    hit_object_list = cmds.ls(base_name + "*")
    hit_transform = []
    for target in hit_object_list:
        shape = cmds.listRelatives(target, shapes=True)
        if not shape:
            continue

        if cmds.objectType(shape[0], isType=search_type):
            hit_transform.append(target)

    if not hit_transform:
        return base_name

    if hit_transform:
        unique_name = "{}_{}".format(base_name, len(hit_transform))
        return unique_name


def extract_data_types(data_list, target_type):
    """データタイプで抽出する

    :param data_list: ノードリスト
    :type data_list: list
    :param target_type: 抽出したいノードタイプ
    :type target_type: str
    :return: 抽出したノードリスト
    :rtype: list
    """

    extracted_data_list = []
    for data in data_list:
        if cmds.objectType(data) == target_type:
            extracted_data_list.append(data)

    return extracted_data_list


def zero_fill(int_number, digits):
    return str(int_number).zfill(digits)


class NumberIdentifyer(object):
    # [数字]抽出用
    NUMBER_REGEX = re.compile(r'[0-9]+$')

    def __init__(self, search_name, number):
        self.search_name = search_name
        self.number = int(number)
        self.digits = len(number)

    def __extract_hit_name(self, search_list):

        base_name = self.search_name
        target_regex = "{base_name}[0-9]{digits}$".format(base_name=base_name, digits="{" + str(self.digits) + "}")

        search_regex = re.compile(target_regex)

        hit_list = []
        for exists_file in search_list:
            result = search_regex.match(exists_file)

            if result:
                hit_list.append(exists_file)

        return hit_list

    def identify__max_number_from_file_name(self, search_list):
        """ファイルネームから最大値を識別する

        :param search_list: 検索対象のリスト
        :type search_list: list
        :return: 最大値に+1した値
        :rtype: str
        """
        hit_list = self.__extract_hit_name(search_list)

        number_list = self.__extract_number(hit_list)

        if number_list == []:
            return zero_fill(self.number, self.digits)

        candidate_max_number = max(number_list)
        if candidate_max_number > self.number:
            before_digits = len(zero_fill(candidate_max_number, self.digits))

            count_up = zero_fill(candidate_max_number + 1, self.digits)

            count_up_digits = len(count_up)
            if before_digits < count_up_digits:
                # 値繰り上がりの為、桁数を増やし、このループから抜け再実行
                self.digits += 1
                self.number = int(count_up)

            else:
                return count_up
        elif candidate_max_number == self.number:
            return zero_fill(self.number + 1, self.digits)
        else:
            return zero_fill(self.number, self.digits)

        return self.identify__max_number_from_file_name(search_list)

    def __extract_number(self, target_list):
        number_list = []
        for target_name in target_list:
            number = self.NUMBER_REGEX.search(target_name).group()

            number = int(number)
            number_list.append(number)

        return number_list
