# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import math

from .. import utility as base_utility


# ==================================================
def clone(target_vector):
    """
    ベクトルを複製

    :param target_vector: 対象ベクトル

    :return: 複製されたベクトル
    """

    clone_vector = [0] * len(target_vector)

    count = -1
    for value in target_vector:
        count += 1

        clone_vector[count] = value

    return clone_vector


# ===============================================
def is_same(src_vector, dst_vector, threshold=0.001):
    """
    同じ値のベクトルかどうか

    :param src_vector: 値A
    :param dst_vector: 値B
    :param threshold: 閾値

    :return: 同じ場合はTrue
    """

    count = -1
    for src_value in src_vector:
        count += 1

        if not base_utility.value.is_same(
                src_value, dst_vector[count], threshold):
            return False

    return True


# ===============================================
def is_round(target_vector, digit):
    """
    丸まったベクトルかどうか

    :param target_vector: 対象ベクトル
    :param digit: 小数点以下の桁数

    :return: 丸まった値の場合はTrue
    """

    for value in target_vector:

        if not base_utility.value.is_round(
                value, digit):
            return False

    return True


# ==================================================
def get_distance(src_vector, dst_vector):
    """
    距離を取得

    :param src_vector: 値A
    :param dst_vector: 値B

    :return: 距離
    """

    distance = get_sqr_distance(src_vector, dst_vector)
    distance = math.sqrt(distance)

    return distance


# ==================================================
def get_sqr_distance(src_vector, dst_vector):
    """
    2乗した距離を取得

    :param src_vector: 値A
    :param dst_vector: 値B

    :return: 距離
    """

    distance = 0

    count = -1
    for src_value in src_vector:
        count += 1

        temp_value = dst_vector[count] - src_value

        distance += temp_value * temp_value

    return distance


# ==================================================
def add(src_vector, dst_vector):
    """
    ベクトルを加算

    :param src_vector: 値A
    :param dst_vector: 値B

    :return: 加算ベクトル
    """

    result_vector = [0] * len(src_vector)

    count = -1
    for src_value in src_vector:
        count += 1

        result_vector[count] = src_value + dst_vector[count]

    return result_vector


# ==================================================
def sub(src_vector, dst_vector):
    """
    ベクトルを減算

    :param src_vector: 値A
    :param dst_vector: 値B

    :return: 減算されたベクトル
    """

    result_vector = [0] * len(src_vector)

    count = -1
    for src_value in src_vector:
        count += 1

        result_vector[count] = src_value - dst_vector[count]

    return result_vector


# ==================================================
def multiply(src_vector, dst_vector):
    """
    ベクトルを乗算

    :param src_vector: 値A
    :param dst_vector: 値B

    :return: 乗算されたベクトル
    """

    result_vector = [0] * len(src_vector)

    count = -1
    for src_value in src_vector:
        count += 1

        result_vector[count] = src_value * dst_vector[count]

    return result_vector


# ==================================================
def multiply_value(src_vector, value):
    """
    ベクトルに値を乗算

    :param src_vector: 値A
    :param value: 乗算値

    :return: 乗算されたベクトル
    """

    result_vector = [0] * len(src_vector)

    count = -1
    for src_value in src_vector:
        count += 1

        result_vector[count] = src_value * value

    return result_vector
