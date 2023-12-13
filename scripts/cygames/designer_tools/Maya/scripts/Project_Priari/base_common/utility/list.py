# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function


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
    result_list = list([_f for _f in result_list if _f])

    return result_list
