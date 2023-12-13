# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from .. import utility as base_utility

try:
    from builtins import range
except Exception:
    pass


# ===============================================
def exists(target_transform):
    """
    トランスフォームが存在するかどうか

    :param target_transform: 対象トランスフォーム
    """

    return base_utility.node.exists(target_transform, 'transform')


# ==================================================
def get_shape(target_transform, target_type_list=None):
    """
    シェープノードを取得

    :param target_transform: 対象トランスフォーム
    :param target_type_list: タイプリスト

    :return: シェープ名
    """

    if not exists(target_transform):
        return

    long_target_name = base_utility.name.get_long_name(target_transform)

    if not long_target_name:
        return

    shape_list = cmds.listRelatives(long_target_name, shapes=True, f=True)

    if not shape_list:
        return

    long_shape_name = base_utility.name.get_long_name(shape_list[0])

    if not long_shape_name:
        return

    if not target_type_list:
        return long_shape_name

    this_type = cmds.objectType(long_shape_name)

    for target_type in target_type_list:

        if target_type == this_type:
            return long_shape_name

    return


# ==================================================
def get_parent(target_transform):

    long_name = base_utility.name.get_long_name(target_transform)

    if not exists(long_name):
        return

    if long_name.find('|') < 0:
        return

    split = long_name.split('|')

    parent_node = ''
    for p in range(len(split) - 1):

        parent_node += split[p]

        if p < len(split) - 2:

            parent_node += '|'

    return parent_node
