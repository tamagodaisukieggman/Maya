# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.api.OpenMaya as om2

from .. import utility


# ===============================================
def is_same(src_color, dst_color, threshold=None):
    """
    同じカラーかどうか

    :param src_color: カラーA
    :param dst_color: カラーB
    :param threshold: 閾値

    :return: 同じ場合はTrue
    """

    src_vector = om2.MFloatPoint(src_color)
    dst_vector = om2.MFloatPoint(dst_color)

    if threshold is None:
        return src_vector == dst_vector
    else:
        return src_vector.isEquivalent(dst_vector, threshold)


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
