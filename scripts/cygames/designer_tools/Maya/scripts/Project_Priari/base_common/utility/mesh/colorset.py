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

import re

import maya.cmds as cmds

from ... import utility as base_utility


# ==================================================
def exists(target_transform, target_colorset):
    """
    カラーセットが存在するかどうか

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット

    :return: Trueの場合は存在
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return False

    colorset_list = cmds.polyColorSet(target_transform, q=True, acs=True)

    if not colorset_list:
        return False

    for colorset in colorset_list:

        if colorset == target_colorset:
            return True

    return False


# ==================================================
def get_colorset_list(target_transform):
    """カラーセットリスト取得

    :param target_transform: 対象となるトランスフォーム

    :return: カラーセット配列
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return

    colorset_list = cmds.polyColorSet(target_transform, q=True, acs=True)

    if not colorset_list:
        return

    return colorset_list


# ==================================================
def search(target_transform, target_colorset):
    """
    カラーセットリストを検索

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット

    :return: カラーセット
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return

    colorset_list = cmds.polyColorSet(target_transform, q=True, acs=True)

    if not colorset_list:
        return

    for colorset in colorset_list:

        if re.search(target_colorset, colorset):
            return colorset

    return


# ==================================================
def get_index(target_transform, target_colorset):
    """
    カラーセット番号を取得

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット

    :return: カラーセット番号
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return -1

    colorset_list = cmds.polyColorSet(target_transform, q=True, acs=True)

    if not colorset_list:
        return

    for cnt in range(0, len(colorset_list)):

        if colorset_list[cnt] == target_colorset:
            return cnt

    return -1


# ==================================================
def get_colorset_from_index(target_transform, target_colorset_index):
    """
    カラーセット番号からカラーセットを取得

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset_index: 対象となるカラーセット番号

    :return: カラーセット
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return

    colorset_list = cmds.polyColorSet(target_transform, q=True, acs=True)

    if not colorset_list:
        return

    for cnt in range(0, len(colorset_list)):

        if cnt == target_colorset_index:
            return colorset_list[cnt]

    return


# ==================================================
def get_current(target_transform):
    """
    現在のカラーセットを取得

    :param target_transform: 対象となるトランスフォーム

    :return: カラーセット
    """

    if base_utility.mesh.get_mesh_shape(target_transform) is None:
        return

    current_colorset = cmds.polyColorSet(
        target_transform, q=True, currentColorSet=True)

    if not current_colorset:
        return

    return current_colorset[0]


# ==================================================
def set_current(target_transform, target_colorset):
    """
    現在のカラーセットを設定

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット
    """

    if not exists(target_transform, target_colorset):
        return

    if get_current(target_transform) == target_colorset:
        return

    cmds.polyColorSet(
        target_transform, colorSet=target_colorset, currentColorSet=True)


# ==================================================
def create(
        target_transform,
        new_colorset_name,
        default_color=[1, 1, 1, 1]):
    """
    カラーセットを作成

    :param target_transform: 対象となるトランスフォーム
    :param new_colorset_name: カラーセット名
    :param default_color: カラー
    """

    if exists(target_transform, new_colorset_name):
        return

    cmds.polyColorSet(target_transform, colorSet=new_colorset_name,
                      cr=True, rpt="RGBA")

    set_current(target_transform, new_colorset_name)

    cmds.polyColorPerVertex(
        target_transform,
        r=default_color[0],
        g=default_color[1],
        b=default_color[2],
        a=default_color[3],
        cdo=True)


# ==================================================
def delete(target_transform, target_colorset):
    """カラーセットを削除

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット
    """

    if not exists(target_transform, target_colorset):
        return

    cmds.polyColorSet(target_transform, colorSet=target_colorset, d=True)


# ==================================================
def rename(target_transform, target_colorset, new_colorset_name):
    """カラーセットをリネーム

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット
    :param new_colorset_name: カラーセット名
    """

    if not exists(target_transform, target_colorset):
        return

    if exists(target_transform, new_colorset_name):
        return

    try:
        cmds.polyColorSet(target_transform, colorSet=target_colorset,
                          nc=new_colorset_name, rn=True)
    except:
        pass


# ==================================================
def blend(
        target_transform, target_colorset, blend_colorset, blend_type):
    """カラーセットをブレンド

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット
    :param blend_colorset: ブレンドするカラーセット名
    :param blend_type:
    multiply:乗算 add:加算 over:ブレンド色 sub:減算
    """

    if not exists(target_transform, blend_colorset):
        return

    if not exists(target_transform, target_colorset):
        create(target_transform, target_colorset)

    if blend_type == "multiply":

        cmds.polyBlendColor(
            target_transform, bcn=target_colorset,
            src=blend_colorset, dst=target_colorset, bfn=7, ch=False)

    elif blend_type == "add":

        cmds.polyBlendColor(
            target_transform, bcn=target_colorset,
            src=blend_colorset, dst=target_colorset, bfn=2, ch=False)

    elif blend_type == "over":

        cmds.polyBlendColor(
            target_transform, bcn=target_colorset,
            src=blend_colorset, dst=target_colorset, bfn=4, blendWeightA=1, ch=False)

    elif blend_type == "sub":

        cmds.polyBlendColor(
            target_transform, bcn=target_colorset,
            src=blend_colorset, dst=target_colorset, bfn=3, ch=False)


# ==================================================
def change_index(
        target_transform, target_colorset, target_index):
    """カラーセットの番号を変更

    :param target_transform: 対象となるトランスフォーム
    :param target_colorset: 対象となるカラーセット
    :param target_index: 対象番号
    """

    this_colorset_index = \
        get_index(target_transform, target_colorset)

    if this_colorset_index < 0:
        return

    if this_colorset_index == target_index:
        return

    this_dst_colorset = \
        get_colorset_from_index(target_transform, target_index)

    if this_dst_colorset is None:
        return

    temp_colorset_name = "____temp"

    delete(target_transform, temp_colorset_name)

    cmds.polyColorSet(
        target_transform,
        cs=this_dst_colorset, nc=temp_colorset_name, cp=True)

    blend(
        target_transform, this_dst_colorset, target_colorset, "over")

    blend(
        target_transform, target_colorset, temp_colorset_name, "over")

    rename(
        target_transform, target_colorset, target_colorset + "____")

    rename(
        target_transform, this_dst_colorset, this_dst_colorset + "____")

    rename(
        target_transform, target_colorset + "____", this_dst_colorset)

    rename(
        target_transform, this_dst_colorset + "____", target_colorset)

    delete(target_transform, target_colorset + "____")
    delete(target_transform, this_dst_colorset + "____")
    delete(target_transform, temp_colorset_name)
