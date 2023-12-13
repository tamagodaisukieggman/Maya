# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # maya 2022-
    from builtins import str
except Exception:
    pass


# ===============================================
def get_fix_length_list(target_list, max_length, default_value):
    """
    同じ長さのリストを取得

    :param target_list: 対象リスト
    :param max_length: 最大の長さ
    :param default_value: 長さが足りない場合のデフォルト値

    :return: 長さをmax_lengthとしたリスト
    """

    if not target_list:
        return [default_value] * max_length

    fix_list = [default_value] * max_length

    count = -1
    for target in target_list:
        count += 1

        if count >= len(fix_list):
            break

        fix_list[count] = target

    return fix_list


# ===============================================
def get_unique_list(target_list):
    """
    重複していないリストを取得

    :param target_list: 対象リスト

    :return: 重複していないリスト
    """

    if target_list is None:
        return

    if len(target_list) <= 1:
        return target_list

    result_list = [None] * len(target_list)
    result_dict = {}

    count = -1
    for target in target_list:
        count += 1

        if target in result_dict:
            continue

        result_list[count] = target
        result_dict[target] = target

    result_dict = None

    result_list = result_list[0:count + 1]

    return result_list


# ===============================================
def convert_from_string(target_string, target_type=None):
    """
    文字列からリストへ変換

    :param target_list: 対象文字列
    :param target_type: 対象タイプ

    :return: 変換されたリスト
    """

    if not target_string:
        return

    temp_string = target_string.replace('[', '')
    temp_string = temp_string.replace(']', '')

    split_str_list = temp_string.split(',')

    result_list = []

    for split_str in split_str_list:

        if target_type == str:
            result_list.append(str(split_str))
        elif target_type == int:
            result_list.append(int(split_str))
        elif target_type == float:
            result_list.append(float(split_str))
        elif target_type == bool:
            result_list.append(bool(split_str))
        else:
            result_list.append(split_str)

    return result_list
