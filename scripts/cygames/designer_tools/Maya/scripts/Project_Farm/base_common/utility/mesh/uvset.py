# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import range
except:
    pass

import maya.cmds as cmds

from ... import utility as base_utility


# ==================================================
def exists(target_transform, target_uvset):
    """
    UVセットが存在するかどうか

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット

    :return: 存在している場合はTrue
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return False

    uvset_list = cmds.polyUVSet(target_transform, q=True, allUVSets=True)

    if not uvset_list:
        return False

    for cnt in range(0, len(uvset_list)):

        if uvset_list[cnt] == target_uvset:
            return True

    return False


# ==================================================
def get_index(target_transform, target_uvset):
    """
    UVセット番号取得

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット

    :return: UVセット番号
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return -1

    uvset_list = cmds.polyUVSet(target_transform, q=True, allUVSets=True)

    if not uvset_list:
        return -1

    for cnt in range(0, len(uvset_list)):

        if uvset_list[cnt] == target_uvset:
            return cnt

    return -1


# ==================================================
def get_uvset_from_index(target_transform, target_index):
    """
    UVセットを番号から取得

    :param target_transform: 対象トランスフォーム
    :param target_index: 対象UVセット番号

    :return: UVセット名
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return

    uvset_list = cmds.polyUVSet(target_transform, q=True, allUVSets=True)

    if not uvset_list:
        return

    for cnt in range(0, len(uvset_list)):

        if cnt == target_index:
            return uvset_list[cnt]

    return


# ==================================================
def get_uvset_list(target_transform):
    """
    UVセットリストを取得

    :param target_transform: 対象トランスフォーム

    :return: UVセットリスト
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return

    uvset_list = cmds.polyUVSet(target_transform, q=True, allUVSets=True)

    if not uvset_list:
        return

    return uvset_list


# ==================================================
def set_current(target_transform, target_uvset):
    """
    現在のUVセットを設定

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット
    """

    if not exists(target_transform, target_uvset):
        return

    cmds.polyUVSet(target_transform, uvSet=target_uvset, cuv=True)


# ==================================================
def get_current(target_transform):
    """
    現在のUVセットを取得

    :param target_transform: 対象トランスフォーム

    :return: 現在のUVセット
    """

    current_set = cmds.polyUVSet(target_transform, q=True, cuv=True)

    if not current_set:
        return

    return current_set[0]


# ==================================================
def set_current_from_index(target_transform, target_index):
    """
    現在のUVセットを番号から設定

    :param target_transform: 対象トランスフォーム
    :param target_index: 対象UVセット番号
    """

    target_uv = get_uvset_from_index(target_transform, target_index)

    if target_uv is None:
        return

    set_current(target_transform, target_uv)


# ==================================================
def create(target_transform, new_uvset_name):
    """
    新しいUVセットを作成

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット
    """

    if exists(target_transform, new_uvset_name):
        return

    cmds.polyUVSet(target_transform, uvSet=new_uvset_name, create=True)


# ==================================================
def delete(target_transform, target_uvset):
    """
    UVセットを削除

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット
    """

    if not exists(target_transform, target_uvset):
        return

    set_current(target_transform, target_uvset)

    cmds.polyUVSet(target_transform, uvSet=target_uvset, delete=True)


# ==================================================
def rename(target_transform, target_uvset, new_uvset_name):
    """
    UVセットをリネーム

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット
    :param new_uvset_name: 新しいUVセット名
    """

    if not exists(target_transform, target_uvset):
        return

    if exists(target_transform, new_uvset_name):
        return

    cmds.polyUVSet(target_transform, uvSet=target_uvset,
                    newUVSet=new_uvset_name, rn=True)


# ==================================================
def change_index(target_transform, target_uvset, target_index):
    """
    UVセットの番号を変更

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット
    :param target_index: 移動先の番号
    """

    this_uvset_index = \
        get_index(target_transform, target_uvset)

    if this_uvset_index < 0:
        return

    if this_uvset_index == target_index:
        return

    this_dst_uvset = \
        get_uvset_from_index(target_transform, target_index)

    if this_dst_uvset is None:
        return

    temp_uvset_name = "____temp"

    delete(target_transform, temp_uvset_name)

    cmds.polyUVSet(
        target_transform,
        uvSet=this_dst_uvset, newUVSet=temp_uvset_name, cp=True)

    cmds.polyCopyUV(
        target_transform,
        uvi=target_uvset, uvs=this_dst_uvset, ch=False)

    cmds.polyCopyUV(
        target_transform,
        uvi=temp_uvset_name, uvs=target_uvset, ch=False)

    rename(
        target_transform, target_uvset, target_uvset + "____")

    rename(
        target_transform, this_dst_uvset, this_dst_uvset + "____")

    rename(
        target_transform, target_uvset + "____", this_dst_uvset)

    rename(
        target_transform, this_dst_uvset + "____", target_uvset)

    delete(
        target_transform, target_uvset + "____")

    delete(
        target_transform, this_dst_uvset + "_____")

    delete(
        target_transform, temp_uvset_name)


# ==================================================
def is_empty(target_transform, target_uvset):
    """
    UVセットが空かどうか

    :param target_transform: 対象トランスフォーム
    :param target_uvset: 対象UVセット

    :return: 空の場合はTrue
    """

    if not exists(target_transform, target_uvset):
        return True

    set_current(target_transform, target_uvset)

    uv_list = cmds.ls(
        (cmds.polyListComponentConversion(target_transform, tuv=True)),
        l=True,
        fl=True
    )

    if uv_list:

        if len(uv_list) > 1:
            return False

    return True
