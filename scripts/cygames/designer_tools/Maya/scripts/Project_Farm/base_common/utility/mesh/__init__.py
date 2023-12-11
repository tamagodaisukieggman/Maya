# -*- coding: utf-8 -*-

from __future__ import absolute_import as __absolute_import
from __future__ import unicode_literals as __unicode_literals
from __future__ import division as _division
from __future__ import print_function as __print_function

import maya.cmds as cmds

from ... import utility as base_utility


# ==================================================
def get_mesh_shape(target_transform):
    """
    シェープノードを取得

    :param target_transform: 対象トランスフォーム

    :return: メッシュシェープ名
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    long_name_list = cmds.ls(target_transform, l=True, typ='transform')

    if not long_name_list:
        long_target_name = target_transform

    long_target_name = long_name_list[0]

    if not long_target_name:
        return

    shape_list = cmds.listRelatives(long_target_name, shapes=True, f=True)

    if not shape_list:
        return

    long_shape_name = shape_list[0]

    this_type = cmds.objectType(long_shape_name)

    for target_type in ['mesh']:

        if target_type == this_type:
            return long_shape_name

    return


# ==================================================
def get_transform_from_vertex(vertex_name):
    """
    トランスフォームを頂点名から取得

    :param vertex_face: 対象頂点名など

    :return トランスフォーム
    """

    transform = vertex_name.split('.')[0]

    return transform


# ==================================================
def get_vertex_index(vertex_name):
    """
    頂点名から頂点番号を取得

    :param vertex_name: 対象頂点名

    :return: 頂点番号
    """

    start_index = vertex_name.find('[') + 1
    end_index = vertex_name.find(']')

    return int(vertex_name[start_index:end_index])


# ==================================================
def get_vertex_list(target_transform):
    """
    頂点リストを取得

    :param target_transform: 対象トランスフォーム

    :return: 頂点リスト取得
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    vertex_list = cmds.ls(
        (cmds.polyListComponentConversion(target_transform, tv=True)),
        l=True,
        fl=True
    )

    if not vertex_list:
        return

    return vertex_list


# ==================================================
def get_vertex_index_list(target_transform):
    """
    頂点番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: 頂点番号の配列
    """

    vertex_list = get_vertex_list(target_transform)

    if not vertex_list:
        return

    vertex_index_list = []

    for vertex in vertex_list:

        vertex_index = get_vertex_index(vertex)

        vertex_index_list.append(vertex_index)

    return vertex_index_list


# ==================================================
def get_edge_index(edge_name):
    """
    エッジ名から頂点番号を取得

    :param vertex_name: 対象エッジ名

    :return: エッジ番号
    """

    start_index = edge_name.find('[') + 1
    end_index = edge_name.find(']')

    return int(edge_name[start_index:end_index])


# ==================================================
def get_edge_list(target_transform):
    """
    エッジリストを取得

    :param target_transform: 対象トランスフォーム

    :return: エッジリスト取得
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    edge_list = cmds.ls(
        (cmds.polyListComponentConversion(target_transform, te=True)),
        l=True,
        fl=True
    )

    if not edge_list:
        return

    return edge_list


# ==================================================
def get_edge_index_list(target_transform):
    """
    エッジ番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: エッジ番号の配列
    """

    edge_list = get_edge_list(target_transform)

    if not edge_list:
        return

    edge_index_list = []

    for edge in edge_list:

        edge_index = get_edge_index(edge)

        edge_index_list.append(edge_index)

    return edge_index_list


# ==================================================
def get_face_index(face_name):
    """
    フェース名から頂点番号を取得

    :param vertex_name: 対象フェース名

    :return: フェース番号
    """

    start_index = face_name.find('[') + 1
    end_index = face_name.find(']')

    return int(face_name[start_index:end_index])


# ==================================================
def get_face_list(target_transform):
    """
    フェースリストを取得

    :param target_transform: 対象トランスフォーム

    :return: フェースリスト取得
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    face_list = cmds.ls(
        (cmds.polyListComponentConversion(target_transform, tf=True)),
        l=True,
        fl=True
    )

    if not face_list:
        return

    return face_list


# ==================================================
def get_face_index_list(target_transform):
    """
    フェース番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: フェース番号の配列
    """

    face_list = get_face_list(target_transform)

    if not face_list:
        return

    face_index_list = []

    for face in face_list:

        face_index = get_face_index(face)

        face_index_list.append(face_index)

    return face_index_list


# ==================================================
def get_vertex_and_face_index(vertex_face_name):
    """
    頂点フェース名から頂点フェース番号を取得

    :param vertex_face_name: 対象頂点フェース名

    :return [頂点番号, フェース番号]
    """

    vtx_face_string = vertex_face_name.split('.')[-1]

    vtx_face_string = vtx_face_string.replace('vtxFace[', '')
    vtx_face_string = vtx_face_string.replace(']', '')

    split_string = vtx_face_string.split('[')

    vertex_index = split_string[0]
    face_index = split_string[1]

    return [int(vertex_index), int(face_index)]


# ==================================================
def get_vertex_face_list(target_transform):
    """
    頂点フェースリストを取得

    :param target_transform: 対象トランスフォーム

    :return: 頂点フェースリスト取得
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    vertex_face_list = cmds.ls(
        (cmds.polyListComponentConversion(target_transform, tvf=True)),
        l=True,
        fl=True
    )

    if not vertex_face_list:
        return

    return vertex_face_list


# ==================================================
def get_vertex_face_index_list(target_transform):
    """
    頂点フェース番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: [頂点番号,フェース番号]の配列
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    vertex_face_list = get_vertex_face_list(target_transform)

    if not vertex_face_list:
        return

    vertex_face_index_list = []
    for vertex_face in vertex_face_list:

        vtx_and_face_index = get_vertex_and_face_index(vertex_face)

        vertex_face_index_list.append(
            [vtx_and_face_index[0], vtx_and_face_index[1]])

    return vertex_face_index_list


# ==================================================
def get_uv_index(uv_name):
    """
    UV名からUV番号を取得

    :param uv_name: 対象UV名

    :return: UV番号
    """

    start_index = uv_name.find('[') + 1
    end_index = uv_name.find(']')

    return int(uv_name[start_index:end_index])


# ==================================================
def get_uv_list(target_transform):
    """
    UVリストを取得

    :param target_transform: 対象トランスフォーム

    :return: UVリスト取得
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    uv_list = cmds.ls(
        (cmds.polyListComponentConversion(target_transform, tuv=True)),
        l=True,
        fl=True
    )

    if not uv_list:
        return

    return uv_list


# ==================================================
def get_uv_index_list(target_transform):
    """
    UV番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: UV番号の配列
    """

    uv_list = get_uv_list(target_transform)

    if not uv_list:
        return

    uv_index_list = []

    for uv in uv_list:

        uv_index = get_uv_index(uv)

        uv_index_list.append(uv_index)

    return uv_index_list


# ==================================================
def get_vertex_index_pair_list_by_index(
    src_vertex_index_list,
    dst_vertex_index_list,
):
    """
    頂点番号によって対応する頂点番号ペアリストを取得

    :param src_vertex_index_list: 元頂点番号リスト
    :param dst_vertex_index_list: 先頂点番号リスト

    :return: [元頂点番号,先頂点番号]の配列
    """

    if not src_vertex_index_list:
        return

    if not dst_vertex_index_list:
        return

    vertex_index_pair_list = [None] * len(src_vertex_index_list)

    count = 0
    for src_vertex_index in src_vertex_index_list:

        for dst_vertex_index in dst_vertex_index_list:

            if src_vertex_index != dst_vertex_index:
                continue

            vertex_index_pair_list[count] = \
                [src_vertex_index, dst_vertex_index]

            count += 1

            break

    if count == 0:
        return

    vertex_index_pair_list = vertex_index_pair_list[0:count]

    return vertex_index_pair_list


# ==================================================
def get_vertex_index_pair_list_by_position(
    src_vertex_index_list,
    src_all_vertex_position_info_list,
    dst_vertex_index_list,
    dst_all_vertex_position_info_list
):
    """
    頂点の位置が近い頂点ペアリストを取得

    :param src_vertex_index_list: コメント
    :param src_all_vertex_position_info_list: コメント
    :param dst_vertex_index_list: コメント
    :param dst_all_vertex_position_info_list: コメント

    :return: 頂点ペアリスト
    """

    vertex_index_near_list = \
        get_vertex_index_near_list(
            src_vertex_index_list,
            src_all_vertex_position_info_list,
            dst_vertex_index_list,
            dst_all_vertex_position_info_list
        )

    if not vertex_index_near_list:
        return

    vertex_index_pair_list = [None] * len(vertex_index_near_list)

    count = 0
    for vertex_index_near in vertex_index_near_list:

        dst_vertex_index = vertex_index_near[0]
        src_vertex_index_list = vertex_index_near[1]
        distance_list = vertex_index_near[2]

        src_vertex_index = src_vertex_index_list[0]

        vertex_index_pair_list[count] = \
            [src_vertex_index, dst_vertex_index]

        count += 1

    return vertex_index_pair_list


# ==================================================
def get_vertex_index_near_list(
    src_vertex_index_list,
    src_all_vertex_position_info_list,
    dst_vertex_index_list,
    dst_all_vertex_position_info_list
):
    """
    コメント
    """

    if not src_vertex_index_list:
        return

    if not src_all_vertex_position_info_list:
        return

    if not dst_vertex_index_list:
        return

    if not dst_all_vertex_position_info_list:
        return

    src_all_position_info_dict = {}
    for position_info in src_all_vertex_position_info_list:
        src_all_position_info_dict[position_info[0]] = position_info

    dst_all_position_info_dict = {}
    for position_info in dst_all_vertex_position_info_list:
        dst_all_position_info_dict[position_info[0]] = position_info

    vertex_index_near_list = [None] * len(dst_vertex_index_list)

    count0 = 0
    for dst_vertex_index in dst_vertex_index_list:

        if dst_vertex_index not in dst_all_position_info_dict:
            continue

        dst_position_info = dst_all_position_info_dict[dst_vertex_index]

        dst_vertex_position = dst_position_info[1]

        src_position_info_list = __get_vertex_position_info_list_in_range(
            dst_vertex_position, src_all_vertex_position_info_list, 1
        )

        if not src_position_info_list:
            continue

        src_position_info_dict = {}
        for position_info in src_position_info_list:
            src_position_info_dict[position_info[0]] = position_info

        distance_and_vertex_index_list = [None] * len(src_vertex_index_list)

        count1 = 0
        for src_vertex_index in src_vertex_index_list:

            if src_vertex_index not in src_position_info_dict:
                continue

            src_position_info = src_position_info_dict[src_vertex_index]

            src_vertex_position = src_position_info[1]

            this_distance = base_utility.vector.get_sqr_distance(
                dst_vertex_position, src_vertex_position
            )

            distance_and_vertex_index_list[count1] = [
                this_distance, src_vertex_index]

            count1 += 1

        if count1 == 0:
            continue

        distance_and_vertex_index_list = distance_and_vertex_index_list[0:count1]
        distance_and_vertex_index_list.sort()

        vertex_index_near_list[count0] = [0, None, None]

        vertex_index_near_list[count0][0] = dst_vertex_index
        vertex_index_near_list[count0][1] = \
            [0] * len(distance_and_vertex_index_list)
        vertex_index_near_list[count0][2] = \
            [0] * len(distance_and_vertex_index_list)

        count2 = 0
        for distance_and_vertex in distance_and_vertex_index_list:

            vertex_index_near_list[count0][1][count2] = distance_and_vertex[1]
            vertex_index_near_list[count0][2][count2] = distance_and_vertex[0]

            count2 += 1

        count0 += 1

    vertex_index_near_list = vertex_index_near_list[0:count0]

    return vertex_index_near_list


# ==================================================
def get_vertex_index_pair_list_by_uv_position(
    src_vertex_index_list,
    src_all_vertex_position_info_list,
    src_all_uv_info_list,
    dst_vertex_index_list,
    dst_all_vertex_position_info_list,
    dst_all_uv_info_list
):
    """
    コメント
    """

    vertex_index_near_list = \
        get_vertex_index_near_list_by_uv_position(
            src_vertex_index_list,
            src_all_vertex_position_info_list,
            src_all_uv_info_list,
            dst_vertex_index_list,
            dst_all_vertex_position_info_list,
            dst_all_uv_info_list
        )

    if not vertex_index_near_list:
        return

    vertex_index_pair_list = [None] * len(vertex_index_near_list)

    count = 0
    for vertex_index_near in vertex_index_near_list:

        dst_vertex_index = vertex_index_near[0]
        src_vertex_index_list = vertex_index_near[1]
        dst_uv_distance_list = vertex_index_near[2]
        dst_vertex_distance_list = vertex_index_near[3]

        src_vertex_index = src_vertex_index_list[0]

        vertex_index_pair_list[count] = \
            [src_vertex_index, dst_vertex_index]

        count += 1

    return vertex_index_pair_list


# ==================================================
def get_vertex_index_near_list_by_uv_position(
    src_vertex_index_list,
    src_all_vertex_position_info_list,
    src_all_uv_info_list,
    dst_vertex_index_list,
    dst_all_vertex_position_info_list,
    dst_all_uv_info_list
):
    """
    コメント
    """

    if not src_vertex_index_list:
        return

    if not src_all_vertex_position_info_list:
        return

    if not src_all_uv_info_list:
        return

    if not dst_vertex_index_list:
        return

    if not dst_all_vertex_position_info_list:
        return

    if not dst_all_uv_info_list:
        return

    src_all_position_info_dict = {}
    for position_info in src_all_vertex_position_info_list:
        src_all_position_info_dict[position_info[0]] = position_info

    dst_all_position_info_dict = {}
    for position_info in dst_all_vertex_position_info_list:
        dst_all_position_info_dict[position_info[0]] = position_info

    src_all_uv_info_dict = {}
    for uv_info in src_all_uv_info_list:
        src_all_uv_info_dict[uv_info[1]] = uv_info

    dst_all_uv_info_dict = {}
    for uv_info in dst_all_uv_info_list:
        dst_all_uv_info_dict[uv_info[1]] = uv_info

    vertex_index_near_list = [None] * len(dst_vertex_index_list)

    count0 = 0
    for dst_vertex_index in dst_vertex_index_list:

        if dst_vertex_index not in dst_all_uv_info_dict:
            continue

        if dst_vertex_index not in dst_all_position_info_dict:
            continue

        dst_uv_info = dst_all_uv_info_dict[dst_vertex_index]

        dst_uv_position = dst_uv_info[3]

        dst_vertex_position = dst_all_position_info_dict[dst_vertex_index][1]

        src_uv_info_list = __get_uv_info_list_in_range(
            dst_uv_position, src_all_uv_info_list, 0.01
        )

        if not src_uv_info_list:
            continue

        src_uv_info_dict = {}
        for uv_info in src_uv_info_list:
            src_uv_info_dict[uv_info[1]] = uv_info

        distance_and_vertex_index_list = [None] * len(src_vertex_index_list)

        count1 = 0
        for src_vertex_index in src_vertex_index_list:

            if src_vertex_index not in src_uv_info_dict:
                continue

            if src_vertex_index not in src_all_position_info_dict:
                continue

            src_uv_info = src_uv_info_dict[src_vertex_index]

            src_uv_position = src_uv_info[3]

            src_vertex_position = src_all_position_info_dict[src_vertex_index][1]

            this_uv_distance = base_utility.vector.get_sqr_distance(
                dst_uv_position, src_uv_position
            )

            this_vertex_distance = base_utility.vector.get_sqr_distance(
                dst_vertex_position, src_vertex_position
            )

            distance_and_vertex_index_list[count1] = [
                this_uv_distance, this_vertex_distance, src_vertex_index
            ]

            count1 += 1

        if count1 == 0:
            continue

        distance_and_vertex_index_list = distance_and_vertex_index_list[0:count1]
        distance_and_vertex_index_list.sort()

        vertex_index_near_list[count0] = [0, None, None, None]

        vertex_index_near_list[count0][0] = dst_vertex_index
        vertex_index_near_list[count0][1] = [0] * \
            len(distance_and_vertex_index_list)
        vertex_index_near_list[count0][2] = [0] * \
            len(distance_and_vertex_index_list)
        vertex_index_near_list[count0][3] = [0] * \
            len(distance_and_vertex_index_list)

        count2 = 0
        for distance_and_vertex in distance_and_vertex_index_list:

            vertex_index_near_list[count0][1][count2] = distance_and_vertex[2]
            vertex_index_near_list[count0][2][count2] = distance_and_vertex[0]
            vertex_index_near_list[count0][3][count2] = distance_and_vertex[1]

            count2 += 1

        count0 += 1

    vertex_index_near_list = vertex_index_near_list[0:count0]

    return vertex_index_near_list


# ==================================================
def __get_vertex_position_info_list_in_range(
    target_vertex_position,
    target_vertex_position_info_list,
    search_range,
):
    """
    コメント
    """

    if not target_vertex_position:
        return

    if not target_vertex_position_info_list:
        return

    vertex_position_info_list = []

    for position_info in target_vertex_position_info_list:

        this_vertex_position = position_info[1]

        is_in_range = True

        count = -1
        for this_value in this_vertex_position:
            count += 1

            target_value = target_vertex_position[count]

            this_distance = abs(this_value - target_value)

            if this_distance > search_range:
                is_in_range = False
                break

        if not is_in_range:
            continue

        vertex_position_info_list.append(position_info)

    if not vertex_position_info_list:

        vertex_position_info_list = \
            __get_vertex_position_info_list_in_range(
                target_vertex_position,
                target_vertex_position_info_list,
                search_range + search_range
            )

    return vertex_position_info_list


# ==================================================
def __get_uv_info_list_in_range(
    target_uv_position,
    target_uv_info_list,
    search_range,
):
    """
    コメント
    """

    if not target_uv_position:
        return

    if not target_uv_info_list:
        return

    result_uv_info_list = []

    for uv_info in target_uv_info_list:

        this_uv_position = uv_info[3]

        is_in_range = True

        count = -1
        for this_value in this_uv_position:
            count += 1

            this_distance = abs(this_value - target_uv_position[count])

            if this_distance > search_range:
                is_in_range = False
                break

        if not is_in_range:
            continue

        result_uv_info_list.append(uv_info)

    if not result_uv_info_list:

        result_uv_info_list = \
            __get_uv_info_list_in_range(
                target_uv_position,
                target_uv_info_list,
                search_range + search_range
            )

    return result_uv_info_list
