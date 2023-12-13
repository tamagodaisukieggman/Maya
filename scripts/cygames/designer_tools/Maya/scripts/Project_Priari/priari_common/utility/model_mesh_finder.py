# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

import os
import re

from ...base_common import utility as base_utility
from . import model_define as model_define

import maya.cmds as cmds

reload(model_define)


# ===============================================
def get_all_base_mesh_list(model_root):
    """
    grp_mesh以下にあるmsh_から始まるアウトライン以外のメッシュリストを返す

    :param model_root: ルートノード
    :return: メッシュリスト
    """

    result_base_mesh_list = []
    all_mesh_list = get_all_mesh_list(model_root)

    for mesh in all_mesh_list:

        if not mesh.endswith(model_define.OUTLINE_SUFFIX):
            result_base_mesh_list.append(mesh)

    return result_base_mesh_list


# ===============================================
def get_all_outline_mesh_list(model_root):
    """
    アウトラインのメッシュリストを返す

    :param model_root: ルートノード
    :return: メッシュリスト
    """

    result_outline_mesh_list = []
    all_mesh_list = get_all_base_mesh_list(model_root)

    for mesh in all_mesh_list:

        if '_Alpha' in mesh:
            continue

        outline_mesh = get_outline_mesh(mesh)

        if outline_mesh:
            result_outline_mesh_list.append(outline_mesh)

    return result_outline_mesh_list


# ===============================================
def get_all_mesh_list(model_root):
    """
    grp_mesh以下にあるmsh_から始まるメッシュリストを返す

    :param model_root: ルートノード
    :return: メッシュリスト
    """

    if not cmds.objExists(model_root):
        return []

    all_transform_list = cmds.listRelatives(model_root, typ='transform', f=True, ad=True)

    if not all_transform_list:
        return []

    result_mesh_list = []
    for transform in all_transform_list:
        short_name = transform.split('|')[-1]
        if short_name.startswith(model_define.MESH_PREFIX):
            result_mesh_list.append(transform)

    return result_mesh_list


# ===============================================
def get_outline_mesh(base_mesh):
    """
    アウトラインメッシュを返す
    ベースと同階層に接尾語がついたものが存在しているはず

    :param base_mesh: ベースメッシュ
    :return: アウトラインメッシュ
    """

    outline_mesh = get_outline_mesh_name(base_mesh)

    if cmds.objExists(outline_mesh):
        return outline_mesh
    else:
        return ''


# ===============================================
def get_outline_mesh_name(base_mesh):
    """
    アウトラインメッシュ名を返す

    :param base_mesh: ベースメッシュ
    :return: アウトラインメッシュ名
    """

    return '{}{}'.format(base_mesh, model_define.OUTLINE_SUFFIX)
