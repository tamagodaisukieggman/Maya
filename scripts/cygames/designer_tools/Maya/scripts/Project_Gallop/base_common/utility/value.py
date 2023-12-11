# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import math


# ==================================================
def is_same(src_value, dst_value, threshold=0.001):
    """
    同じ値かどうか

    :param src_value: 値A
    :param dst_value: 値B
    :param threshold: 閾値

    :return: 同じ場合はTrue
    TODO: 明らかに違う値でもTrueになる事があるため、正常に動作していない可能性が高い
    (例えば0.0001999999)
    """

    diff_value = float(abs(src_value - dst_value))

    if diff_value < threshold - threshold * 0.00001:
        return True

    return False


# ==================================================
def is_round(target_value, digit):
    """
    丸まった値かどうか

    :param target_value: 値
    :param digit: 小数点以下の桁数

    :return: 丸まっている場合はTrue

    TODO: 丸まった値の定義が不明、また特定の小数桁のみFalseを返す
    (digit桁2の時、target_valueが3~4ならFalse返すがそれ以外はTrueで返ってくる)
    """

    src_value_multi = target_value * pow(10, digit)
    src_value_mod = math.modf(src_value_multi)
    src_value_rest = src_value_mod[0]

    if is_same(src_value_rest, 0, 0.001) or is_same(src_value_rest, 1, 0.001):
        return True

    return False
