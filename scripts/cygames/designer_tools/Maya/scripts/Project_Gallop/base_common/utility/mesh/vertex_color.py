# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

import maya.api.OpenMaya as om

from ... import utility as base_utility

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass


# ==================================================
def get_all_vertex_color_info_list(target_transform):
    """
    全ての頂点カラーを取得

    :param target_transform: 対象トランスフォーム

    :return: [頂点番号, 頂点フェース,[r,g,b,a]]の配列
    """

    if not base_utility.mesh.colorset.get_current(target_transform):
        return

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    om_vtxface_color_list = om_mesh.getFaceVertexColors()

    vertex_face_index_list = \
        base_utility.mesh.get_vertex_face_index_list(target_transform)

    all_info_list = []
    for p in range(len(vertex_face_index_list)):

        this_vertex_index = vertex_face_index_list[p][0]
        this_face_index = vertex_face_index_list[p][1]

        this_vtxface_global_index = \
            om_mesh.getFaceVertexIndex(
                this_face_index, this_vertex_index, False)

        this_om_vtxface_color = \
            om_vtxface_color_list[this_vtxface_global_index]

        this_vtxface_color = [0] * 4

        this_vtxface_color[0] = this_om_vtxface_color.r
        this_vtxface_color[1] = this_om_vtxface_color.g
        this_vtxface_color[2] = this_om_vtxface_color.b
        this_vtxface_color[3] = this_om_vtxface_color.a

        this_info = [
            this_vertex_index,
            this_face_index,
            this_vtxface_color
        ]

        all_info_list.append(this_info)

    all_info_list.sort()

    return all_info_list


# ==================================================
def set_vertex_color_info_list(
    target_transform,
    vertex_color_info_list
):
    """
    頂点カラーを設定

    :param target_transform: 対象トランスフォーム
    :param vertex_color_info_list: 頂点カラーの場合は[頂点番号,[r,g,b,a]],
    頂点フェースカラーの場合は[頂点番号,頂点フェース番号,[r,g,b,a]]とし配列指定
    """

    if not vertex_color_info_list:
        return

    if not base_utility.mesh.colorset.get_current(target_transform):
        return

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    all_info_list = \
        get_all_vertex_color_info_list(target_transform)

    if not all_info_list:
        return

    vertex_count = cmds.polyEvaluate(target_transform, v=True)

    vertex_info_list = [None] * vertex_count

    for p in range(len(all_info_list)):

        this_info = all_info_list[p]

        this_vertex_index = this_info[0]

        if vertex_info_list[this_vertex_index] is None:

            vertex_info_list[this_vertex_index] = [this_info]

        else:

            vertex_info_list[this_vertex_index].append(this_info)

    target_info_list = []

    for p in range(len(vertex_color_info_list)):

        this_info = vertex_color_info_list[p]

        this_vertex_index = None
        this_face_index = None
        this_color = None

        set_vertex_only = False

        if len(this_info) == 2:

            this_vertex_index = this_info[0]
            this_color = this_info[1]
            set_vertex_only = True

        elif len(this_info) == 3:

            this_vertex_index = this_info[0]
            this_face_index = this_info[1]
            this_color = this_info[2]
            set_vertex_only = False

        if this_color is None:
            continue

        if this_vertex_index >= len(vertex_info_list):
            continue

        base_info_list = vertex_info_list[this_vertex_index]

        if not base_info_list:
            continue

        for q in range(len(base_info_list)):

            base_vertex_index = base_info_list[q][0]
            base_face_index = base_info_list[q][1]
            base_value = base_info_list[q][2]

            target_info = None

            if set_vertex_only:

                target_info = [
                    base_vertex_index,
                    base_face_index,
                    this_color
                ]

            else:

                if base_face_index != this_face_index:
                    continue

                target_info = [
                    base_vertex_index,
                    base_face_index,
                    this_color
                ]

            if target_info is None:
                continue

            target_info_list.append(target_info)

    if not target_info_list:
        return

    om_vertex_index_array = om.MIntArray()
    om_face_index_array = om.MIntArray()
    om_color_array = om.MColorArray()

    for p in range(len(target_info_list)):

        this_info = target_info_list[p]

        this_vertex_index = this_info[0]
        this_face_index = this_info[1]
        this_color = this_info[2]

        this_om_color = \
            base_utility.open_maya.get_om_color(this_color)

        om_vertex_index_array.append(this_vertex_index)
        om_face_index_array.append(this_face_index)
        om_color_array.append(this_om_color)

    om_mesh.setFaceVertexColors(
        om_color_array, om_face_index_array, om_vertex_index_array)


# ==================================================
def paste_vertex_color_by_vertex_index(src_vertex_color_info, dst_vertex_color_info):
    """
    頂点カラーを頂点番号でコピー

    :param src_vertex_color_info: コピー元VertexColorInfoクラス
    :param dst_vertex_color_info: コピー先VertexColorInfoクラス
    """

    info_item_pair_list = __get_vertex_color_info_item_pair_list(
        src_vertex_color_info, dst_vertex_color_info)

    if not info_item_pair_list:
        return

    for info_item_pair in info_item_pair_list:

        src_info_item = info_item_pair[0]
        dst_info_item = info_item_pair[1]

        vertex_index_pair_list = \
            base_utility.mesh.get_vertex_index_pair_list_by_index(
                src_info_item.target_vertex_index_list,
                dst_info_item.target_vertex_index_list
            )

        if not vertex_index_pair_list:
            continue

        __paste_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list
        )


# ==================================================
def paste_vertex_color_by_vertex_position(src_vertex_color_info, dst_vertex_color_info):
    """
    頂点カラーを位置でコピー

    :param src_vertex_color_info: コピー元VertexColorInfoクラス
    :param dst_vertex_color_info: コピー先VertexColorInfoクラス
    """

    info_item_pair_list = __get_vertex_color_info_item_pair_list(
        src_vertex_color_info, dst_vertex_color_info)

    if not info_item_pair_list:
        return

    for info_item_pair in info_item_pair_list:

        src_info_item = info_item_pair[0]
        dst_info_item = info_item_pair[1]

        vertex_index_pair_list = \
            base_utility.mesh.get_vertex_index_pair_list_by_position(
                src_info_item.target_vertex_index_list,
                src_info_item.world_vertex_position_info_list,
                dst_info_item.target_vertex_index_list,
                dst_info_item.world_vertex_position_info_list
            )

        if not vertex_index_pair_list:
            continue

        __paste_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list
        )


# ==================================================
def __get_vertex_color_info_item_pair_list(
        src_vertex_color_info,
        dst_vertex_color_info,
):

    if not src_vertex_color_info:
        return

    if not dst_vertex_color_info:
        return

    if not src_vertex_color_info.info_item_list:
        return

    if not dst_vertex_color_info.info_item_list:
        return

    check_transform_name = True
    if len(src_vertex_color_info.info_item_list) == 1:
        if len(dst_vertex_color_info.info_item_list) == 1:
            check_transform_name = False

    if not check_transform_name:

        src_info_item = src_vertex_color_info.info_item_list[0]
        dst_info_item = dst_vertex_color_info.info_item_list[0]

        return [[src_info_item, dst_info_item]]

    info_item_pair_list = []

    for src_info_item in src_vertex_color_info.info_item_list:

        for dst_info_item in dst_vertex_color_info.info_item_list:

            if dst_info_item.target_transform_name != \
                    src_info_item.target_transform_name:
                continue

            info_item_pair_list.append([src_info_item, dst_info_item])
            break

    if not info_item_pair_list:
        return

    return info_item_pair_list


# ==================================================
def __paste_by_vertex_index_pair_list(
        src_vertex_color_info_item, dst_vertex_color_info_item, vertex_index_pair_list):

    if not src_vertex_color_info_item:
        return

    if not dst_vertex_color_info_item:
        return

    if not vertex_index_pair_list:
        return

    target_info_list = []

    for vertex_index_pair in vertex_index_pair_list:

        src_vertex_index = vertex_index_pair[0]
        dst_vertex_index = vertex_index_pair[1]

        target_src_info_list = \
            src_vertex_color_info_item.fix_vertex_color_info_list[src_vertex_index]

        target_dst_info_list = \
            dst_vertex_color_info_item.fix_vertex_color_info_list[dst_vertex_index]

        if not target_src_info_list:
            continue

        if not target_dst_info_list:
            continue

        count = -1
        for this_dst_info in target_dst_info_list:
            count += 1

            this_dst_vertex_index = this_dst_info[0]
            this_dst_face_index = this_dst_info[1]
            this_dst_value = this_dst_info[2]

            target_value = None

            if count < len(target_src_info_list):
                target_value = target_src_info_list[count][2]
            else:
                target_value = target_src_info_list[-1][2]

            if target_value is None:
                continue

            new_info = [
                this_dst_vertex_index,
                this_dst_face_index,
                target_value
            ]

            target_info_list.append(new_info)

    if not target_info_list:
        return

    base_utility.mesh.vertex_color.set_vertex_color_info_list(
        dst_vertex_color_info_item.target_transform,
        target_info_list
    )


# ==================================================
def get_vertex_list_with_unround_color(vertex_color_info, digit):
    """
    頂点カラーが丸められていない頂点リストを取得

    :param vertex_color_info: 対象VertexColorinfoクラス
    :param digit: 桁数

    :return: 頂点リスト
    """

    if not vertex_color_info:
        return

    if not vertex_color_info.info_item_list:
        return

    target_vertex_list = []

    for info_item in vertex_color_info.info_item_list:

        for vertex_color_info in info_item.vertex_color_info_list:

            this_color = vertex_color_info[2]

            if base_utility.color.is_round(
                this_color, digit
            ):
                continue

            this_vtx_index = vertex_color_info[0]
            this_vtx_face = vertex_color_info[1]

            this_vtx = \
                '{0}.vtx[{1}]'.format(
                    info_item.target_transform, this_vtx_index)

            if this_vtx in target_vertex_list:
                continue

            target_vertex_list.append(this_vtx)

    if not target_vertex_list:
        return

    return target_vertex_list


# ==================================================
def get_vertex_list_with_unshared_color(vertex_color_info):
    """
    頂点カラーがUnsharedの頂点リストを取得

    :param vertex_color_info: 対象VertexColorinfoクラス
    :param threshold: しきい値

    :return: 頂点リスト
    """

    if not vertex_color_info:
        return

    if not vertex_color_info.info_item_list:
        return

    target_vertex_list = []

    for info_item in vertex_color_info.info_item_list:

        for fix_vertex_color_info in info_item.fix_vertex_color_info_list:

            if len(fix_vertex_color_info) == 0:
                continue

            if len(fix_vertex_color_info) == 1:
                continue

            first_color = fix_vertex_color_info[0][2]

            is_same_color = True

            for vertex_color_info in fix_vertex_color_info:

                this_vtx_index = vertex_color_info[0]
                this_vtx_face = vertex_color_info[1]
                this_color = vertex_color_info[2]

                if base_utility.color.is_same(
                    first_color, this_color
                ):
                    continue

                is_same_color = False
                break

            if is_same_color:
                continue

            this_vtx = \
                '{0}.vtx[{1}]'.format(
                    info_item.target_transform, this_vtx_index)

            target_vertex_list.append(this_vtx)

    if not target_vertex_list:
        return

    return target_vertex_list
