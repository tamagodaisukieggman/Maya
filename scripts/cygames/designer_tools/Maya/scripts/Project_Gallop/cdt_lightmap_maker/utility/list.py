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

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ==================================================
    @staticmethod
    def exist_list(target_list):
        """リストが存在するかどうか"""

        if target_list is None:
            return False

        if type(target_list) != list:
            return False

        if len(target_list) == 0:
            return False

        return True

    # ==================================================
    @staticmethod
    def get_fix_length_list(target_list, target_length):

        if len(target_list) == target_length:
            return target_list

        is_add = False
        if len(target_list) < target_length:
            is_add = True

        length_diff = abs(target_length - len(target_list))

        for p in range(length_diff):

            if is_add:
                target_list.append(target_list[-1])
            else:
                target_list.pop(-1)

        return target_list
