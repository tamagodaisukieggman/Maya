# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
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
    def add_vector(src_vector, dst_vector):

        result_vector = [0] * min(len(src_vector), len(dst_vector))

        for p in range(0, len(result_vector)):
            result_vector[p] = src_vector[p] + dst_vector[p]

        return result_vector

    # ==================================================
    @staticmethod
    def sub_vector(src_vector, dst_vector):

        result_vector = [0] * min(len(src_vector), len(dst_vector))

        for p in range(len(result_vector)):
            result_vector[p] = src_vector[p] - dst_vector[p]

        return result_vector

    # ==================================================
    @staticmethod
    def multiply_vector(src_vector, dst_vector):

        result_vector = [0] * min(len(src_vector), len(dst_vector))

        for p in range(len(result_vector)):
            result_vector[p] = src_vector[p] * dst_vector[p]

        return result_vector

    # ==================================================
    @staticmethod
    def lerp(src_vector, dst_vector, lerp_value):
        """
        Vectorを線形補完

        :param src_vector: VectorA
        :param dst_vector: VectorB
        :param lerp_value: 補完値
        :return: 補完された値
        """

        result_vector = [0] * min(len(src_vector), len(dst_vector))

        for p in range(0, len(result_vector)):

            result_vector[p] = \
                (1 - lerp_value) * src_vector[p] + lerp_value * dst_vector[p]

        return result_vector
