# -*- coding: utf-8 -*-
# This file copied from glp_chara_exporter.utility.normal_to_uv

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys

import maya.cmds as cmds

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

try:
    # maya 2022-
    from builtins import range
    from importlib import reload
except Exception:
    pass

reload(base_common)


def transfer_normal_to_uvset(
    src_transform,
    dst_transform,
    xy_uvset,
    zw_uvset
):
    """
    法線情報を別のメッシュの2つのUVセットに転写
    """

    # Current UVSetの記憶
    current_set = cmds.polyUVSet(dst_transform, q=True, cuv=True)[0]

    # UV3のチェック
    dst_uv_list = base_utility.mesh.uvset.get_uvset_list(dst_transform)

    uv3_set = None
    if dst_uv_list:
        if len(dst_uv_list) >= 3:
            uv3_set = dst_uv_list[2]

    # 転送用UVSetの作成

    base_utility.mesh.uvset.create(dst_transform, xy_uvset)
    base_utility.mesh.uvset.set_current(dst_transform, xy_uvset)

    cmds.polyAutoProjection(dst_transform)

    # Python3系のMayaで複製したメッシュにpolyMapSewを使用するとヒストリー削除時にマテリアルが崩れる問題対応
    # polyMapSewを行わなくても最終的な描画に変化はないが、UV数が変ってしまうため2系では処理を変えない
    if sys.version_info.major == 2:
        cmds.polyMapSew(dst_transform)

    cmds.polyMapCut(dst_transform)

    base_utility.mesh.uvset.create(dst_transform, zw_uvset)
    base_utility.mesh.uvset.set_current(dst_transform, zw_uvset)

    cmds.polyAutoProjection(dst_transform)

    # Python3系のMayaで複製したメッシュにpolyMapSewを使用するとヒストリー削除時にマテリアルが崩れる問題対応
    # polyMapSewを行わなくても最終的な描画に変化はないが、UV数が変ってしまうため2系では処理を変えない
    if sys.version_info.major == 2:
        cmds.polyMapSew(dst_transform)

    cmds.polyMapCut(dst_transform)

    cmds.delete(dst_transform, ch=True)

    # 法線取得
    src_normal_info = base_class.mesh.normal_info.NormalInfo()
    src_normal_info.create_info([src_transform])

    dst_normal_info = base_class.mesh.normal_info.NormalInfo()
    dst_normal_info.create_info([dst_transform])

    src_all_normal_info_list = \
        src_normal_info.info_item_list[0].fix_normal_info_list

    dst_all_normal_info_list = \
        dst_normal_info.info_item_list[0].fix_normal_info_list

    # 結合UV洗い出し
    # SRC側の結合UV洗い出し
    src_merge_vertex_index_list = []
    for src_normal_info in src_all_normal_info_list:

        if len(src_normal_info) == 0:
            continue

        first_normal_info = src_normal_info[0]
        first_normal = first_normal_info[2]

        same_normal = True
        for q in range(len(src_normal_info)):

            this_normal_info = src_normal_info[q]
            this_normal = this_normal_info[2]

            if not base_utility.vector.is_same(first_normal, this_normal):
                same_normal = False
                break

        if not same_normal:
            continue

        src_merge_vertex_index_list.append(first_normal_info[0])

    # DST側の結合UV洗い出し
    dst_merge_vertex_index_list = []
    for dst_normal_info in dst_all_normal_info_list:

        if len(dst_normal_info) == 0:
            continue

        first_normal_info = dst_normal_info[0]
        first_normal = first_normal_info[2]

        same_normal = True
        for q in range(len(dst_normal_info)):

            this_normal_info = dst_normal_info[q]
            this_normal = this_normal_info[2]

            if not base_utility.vector.is_same(first_normal, this_normal):
                same_normal = False
                break

        if not same_normal:
            continue

        dst_merge_vertex_index_list.append(first_normal_info[0])

    # マージする頂点をSRC側、DST側の共通のものとする
    fix_merge_vertex_list = []
    for dst_vertex_index in dst_merge_vertex_index_list:

        for src_vertex_index in src_merge_vertex_index_list:

            if src_vertex_index == dst_vertex_index:
                fix_merge_vertex_list.append(
                    '{0}.vtx[{1}]'.format(dst_transform, dst_vertex_index)
                )
                break

    # UV縫い直し
    if len(fix_merge_vertex_list) > 0:
        for uv_set in (xy_uvset, zw_uvset):
            cmds.polyUVSet(dst_transform, uvs=uv_set, cuv=True)
            cmds.polyMergeUV(fix_merge_vertex_list, d=0.001)

    # 速度対策: Historyを削除
    cmds.delete(dst_transform, ch=True)

    # UVの転送
    uv_xy_info_list = []
    uv_zw_info_list = []

    for p in range(len(src_all_normal_info_list)):

        for q in range(len(src_all_normal_info_list[p])):

            this_info = src_all_normal_info_list[p][q]

            this_vertex_index = this_info[0]
            this_face_index = this_info[1]
            this_normal = this_info[2]

            this_uv_index = __get_uv_index_from_vertex_face(
                dst_transform, this_vertex_index, this_face_index
            )

            if this_uv_index < 0:
                continue

            uv_xy_info_list.append([
                this_uv_index,
                [this_normal[0], this_normal[1]]
            ])

            uv_zw_info_list.append([
                this_uv_index,
                [this_normal[2], 1]
            ])

    base_utility.mesh.uvset.set_current(dst_transform, xy_uvset)
    base_utility.mesh.uv.set_uv_info_list(dst_transform, uv_xy_info_list)

    base_utility.mesh.uvset.set_current(dst_transform, zw_uvset)
    base_utility.mesh.uv.set_uv_info_list(dst_transform, uv_zw_info_list)

    cmds.delete(dst_transform, ch=True)

    base_utility.mesh.uvset.set_current(dst_transform, current_set)

    if uv3_set is not None:

        base_utility.mesh.uvset.set_current(dst_transform, uv3_set)

        uv_list = cmds.ls(
            (cmds.polyListComponentConversion(dst_transform, tuv=True)),
            l=True,
            fl=True
        )

        if len(uv_list) > 1:  # UV展開されていなくてもmap[0]が返されている

            base_utility.mesh.uvset.set_current(dst_transform, uv3_set)
            cmds.select(uv_list, r=True)
            cmds.polyEditUV(uv_list, u=2, v=2)

            base_utility.mesh.uvset.set_current(dst_transform, uv3_set)
            cmds.select(uv_list, r=True)
            cmds.polyCopyUV(
                uv_list, uvSetNameInput=uv3_set, uvSetName=xy_uvset, ch=1)

            base_utility.mesh.uvset.set_current(dst_transform, uv3_set)
            cmds.select(uv_list, r=True)
            cmds.polyCopyUV(
                uv_list, uvSetNameInput=uv3_set, uvSetName=zw_uvset, ch=1)

    cmds.delete(dst_transform, ch=True)

    base_utility.mesh.uvset.set_current(dst_transform, current_set)


def __get_uv_index_from_vertex_face(target_transform, vertex_index, face_index):

    this_vertex_face = \
        "{0}.vtxFace[{1}][{2}]".format(
            target_transform, vertex_index, face_index)

    uv_list = cmds.ls(
        (cmds.polyListComponentConversion(this_vertex_face, tuv=True)),
        l=True,
        fl=True
    )

    if not uv_list:
        return -1

    this_uv = uv_list[0]

    uv_index = base_utility.mesh.get_uv_index(this_uv)

    return uv_index
