# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import zip
except:
    pass

import re

import maya.cmds as cmds

from ... import utility as base_utility


# ==================================================
def get_all_normal_info_list(target_transform):
    """
    全ての法線情報を取得

    :param target_transform: 対象トランスフォーム

    :return: [頂点番号,フェース番号,[x,y,z]]の配列
    """

    all_vtx_list = cmds.ls(target_transform + '.vtx[*]', l=True, fl=True)

    if not all_vtx_list:
        return

    all_info_list = []
    for vtx in all_vtx_list:

        this_vtx_index = None

        vtx_match = re.search(r'\.vtx\[(\d+)\]', vtx)
        if vtx_match:
            this_vtx_index = int(vtx_match.group(1))
        else:
            continue

        face_vtx_list = cmds.ls(vtx.replace('vtx[', 'vtxFace[') + '[*]', l=True, fl=True)

        if not face_vtx_list:
            continue

        for face_vtx in face_vtx_list:

            this_face_vtx_index = None
            this_face_vtx_normal = cmds.polyNormalPerVertex(face_vtx, q=True, xyz=True)
            this_face_match = re.search(r'\.vtxFace\[\d+\]\[(\d+)\]', face_vtx)

            if this_face_match:
                this_face_vtx_index = int(this_face_match.group(1))
            else:
                continue

            this_info = [
                this_vtx_index,
                this_face_vtx_index,
                this_face_vtx_normal,
            ]

            all_info_list.append(this_info)

    all_info_list.sort()

    return all_info_list


# ==================================================
def set_normal_info_list(target_transform, normal_info_list):
    """
    法線を設定

    :param target_transform: 対象トランスフォーム
    :param normal_info_list: 頂点法線の場合は[頂点番号,[x,y,z]],
    頂点フェース法線の場合は[頂点番号,フェース番号,[x,y,z]]とし配列指定
    """

    if not normal_info_list or not cmds.objExists(target_transform):
        return

    target_list = []
    set_normal_list = []

    for normal_info in normal_info_list:

        # 頂点法線
        if len(normal_info) == 2:
            target_list.append('{0}.vtx[{1}]'.format(target_transform, normal_info[0]))
            set_normal_list.append(normal_info[1])

        # 頂点フェース法線
        elif len(normal_info) == 3:
            target_list.append('{0}.vtxFace[{1}][{2}]'.format(target_transform, normal_info[0], normal_info[1]))
            set_normal_list.append(normal_info[2])

    cmds.polyNormalPerVertex(target_list, xyz=set_normal_list)


# ==================================================
def paste_normal_by_vertex_index(src_normal_info, dst_normal_info):
    """
    法線を頂点番号でコピー

    :param src_normal_info: コピー元NormalInfoクラス
    :param dst_normal_info: コピー先NormalInfoクラス
    """

    info_item_pair_list = __get_normal_info_item_pair_list(
        src_normal_info, dst_normal_info)

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

        __paste_normal_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list
        )


# ==================================================
def paste_normal_by_list_order(src_normal_info, dst_normal_info):
    """
    法線をtarget_vertex_listの順番でコピー

    :param src_normal_info: コピー元NormalInfoクラス
    :param dst_normal_info: コピー先NormalInfoクラス
    """

    info_item_pair_list = __get_normal_info_item_pair_list(
        src_normal_info, dst_normal_info)

    if not info_item_pair_list:
        return

    for info_item_pair in info_item_pair_list:

        src_info_item = info_item_pair[0]
        dst_info_item = info_item_pair[1]

        vertex_index_pair_list = []

        for src_vtx_index, dst_vtx_index in zip(src_info_item.target_vertex_index_list, dst_info_item.target_vertex_index_list):
            vertex_index_pair_list.append([src_vtx_index, dst_vtx_index])

        if not vertex_index_pair_list:
            continue

        __paste_normal_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list
        )


# ==================================================
def paste_normal_by_vertex_position(src_normal_info, dst_normal_info):
    """
    法線を位置でコピー

    :param src_normal_info: コピー元NormalInfoクラス
    :param dst_normal_info: コピー先NormalInfoクラス
    """

    info_item_pair_list = __get_normal_info_item_pair_list(
        src_normal_info, dst_normal_info)

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

        __paste_normal_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list
        )


# ==================================================
def __get_normal_info_item_pair_list(
        src_normal_info,
        dst_normal_info,
):

    if not src_normal_info:
        return

    if not dst_normal_info:
        return

    if not src_normal_info.info_item_list:
        return

    if not dst_normal_info.info_item_list:
        return

    check_transform_name = True
    if len(src_normal_info.info_item_list) == 1:
        if len(dst_normal_info.info_item_list) == 1:
            check_transform_name = False

    if not check_transform_name:

        src_info_item = src_normal_info.info_item_list[0]
        dst_info_item = dst_normal_info.info_item_list[0]

        return [[src_info_item, dst_info_item]]

    info_item_pair_list = []

    for src_info_item in src_normal_info.info_item_list:

        for dst_info_item in dst_normal_info.info_item_list:

            if dst_info_item.target_transform_name != \
                    src_info_item.target_transform_name:
                continue

            info_item_pair_list.append([src_info_item, dst_info_item])
            break

    if not info_item_pair_list:
        return

    return info_item_pair_list


# ==================================================
def __paste_normal_by_vertex_index_pair_list(
        src_normal_info_item, dst_normal_info_item, vertex_index_pair_list):

    if not src_normal_info_item:
        return

    if not dst_normal_info_item:
        return

    if not vertex_index_pair_list:
        return

    target_info_list = []

    for vertex_index_pair in vertex_index_pair_list:

        src_vertex_index = vertex_index_pair[0]
        dst_vertex_index = vertex_index_pair[1]

        target_src_info_list = \
            src_normal_info_item.fix_normal_info_list[src_vertex_index]

        target_dst_info_list = \
            dst_normal_info_item.fix_normal_info_list[dst_vertex_index]

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

    base_utility.mesh.normal.set_normal_info_list(
        dst_normal_info_item.target_transform,
        target_info_list
    )
