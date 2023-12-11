# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import math

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ==================================================
    @staticmethod
    def is_same_value(src_value, dst_value):
        """
        同じ値かどうか

        :param src_value: 値A
        :param dst_value: 値B
        :return: Trueの場合は同じ値
        """

        digit = 5

        src_value_multi = src_value * math.pow(10, digit)
        src_value_int = math.modf(src_value_multi)[1]

        dst_value_multi = dst_value * math.pow(10, digit)
        dst_value_int = math.modf(dst_value_multi)[1]

        if src_value_int == dst_value_int:
            return True

        return False

    # ==================================================
    @staticmethod
    def lerp(src_value, dst_value, lerp_value):
        """
        値を線形補完

        :param src_value: 値A
        :param dst_value: 値B
        :param lerp_value: 補完値
        :return: 補完された値
        """

        result_value = \
            src_value * (1 - lerp_value) + dst_value * lerp_value

        return result_value
