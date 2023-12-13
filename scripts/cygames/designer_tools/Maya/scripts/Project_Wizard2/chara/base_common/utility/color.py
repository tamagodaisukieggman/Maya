# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from .. import utility


# ===============================================
def is_same(src_color, dst_color, threshold):
    """
    同じカラーかどうか

    :param src_color: カラーA
    :param dst_color: カラーB
    :param threshold: 閾値

    :return: 同じ場合はTrue
    """

    count = -1
    for src_value in src_color:
        count += 1

        if not utility.value.is_same(src_value, dst_color[count], threshold):
            return False

    return True


# ===============================================
def is_round(target_color, digit):
    """
    丸められたカラーかどうか

    :param target_color:対象カラー
    :param digit: 小数点以下の桁数

    :return: 丸まった値の場合はTrue
    """

    for value in target_color:

        if not utility.value.is_round(value, digit):
            return False

    return True
