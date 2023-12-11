# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.api.OpenMaya as om

from ... import utility as base_utility

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass


# ==================================================
def get_all_vertex_position_info_list(target_transform, is_world):
    """
    全ての頂点位置を取得

    :param target_transform: 対象トランスフォーム
    :param is_world: Trueのときにワールド座標で取得

    :return: [頂点番号,[x,y,z]]の配列
    """

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    om_space = om.MSpace.kObject
    if is_world:
        om_space = om.MSpace.kWorld

    vertex_position_info_list = []

    # om_meshがvertexを有しない場合はREが上がる
    try:
        om_vtx_position_list = om_mesh.getPoints(om_space)
    except RuntimeError:
        return vertex_position_info_list

    for p in range(len(om_vtx_position_list)):

        this_vertex_index = p

        this_om_position = om_vtx_position_list[p]

        this_position = \
            base_utility.open_maya.get_vector(this_om_position)

        this_info = [
            this_vertex_index,
            this_position
        ]

        vertex_position_info_list.append(this_info)

    vertex_position_info_list.sort()

    return vertex_position_info_list


# ==================================================
def set_vertex_position_info_list(
        target_transform,
        vertex_position_info_list,
        is_world):
    """
    頂点位置を設定

    :param target_transform: 対象トランスフォーム
    :param vertex_position_info_list: [頂点番号,[x,y,z]]の配列
    :param is_world: Trueのときにワールド座標で設定
    """

    if not vertex_position_info_list:
        return

    if not target_transform:
        return

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    all_info_list = \
        get_all_vertex_position_info_list(
            target_transform, is_world)

    for p in range(len(vertex_position_info_list)):

        this_info = vertex_position_info_list[p]
        this_vertex_index = this_info[0]
        this_value = this_info[1]

        if this_vertex_index >= len(all_info_list):
            continue

        all_info_list[this_vertex_index][1] = this_value

    all_vertex_position_list = []

    for p in range(len(all_info_list)):

        this_info = vertex_position_info_list[p]
        this_value = this_info[1]

        all_vertex_position_list.append(this_value)

    if not base_utility.transform.exists(target_transform):
        return

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    om_point_list = om.MFloatPointArray()
    om_point_list.setLength(len(all_vertex_position_list))

    for p in range(len(all_vertex_position_list)):

        om_point_list[p].x = all_vertex_position_list[p][0]
        om_point_list[p].y = all_vertex_position_list[p][1]
        om_point_list[p].z = all_vertex_position_list[p][2]

    om_space = om.MSpace.kObject
    if is_world:
        om_space = om.MSpace.kWorld

    om_mesh.setPoints(om_point_list, om_space)


# ==================================================
def paste_position_by_vertex_index(src_vertex_position_info, dst_vertex_position_info):
    """
    頂点位置をindex番号でペースト

    :param src_vertex_position_info: コピー元SkinInfo
    :param dst_vertex_position_info: コピー先SkinInfo
    """

    info_item_pair_list = __get_vertex_position_info_item_pair_list(
        src_vertex_position_info, dst_vertex_position_info
    )

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

        __paste_vertex_position_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list,
        )


# ==================================================
def paste_position_by_uv_position(src_vertex_position_info, dst_vertex_position_info):
    """
    頂点位置をUV位置でペースト

    :param src_vertex_position_info: コピー元SkinInfo
    :param dst_vertex_position_info: コピー先SkinInfo
    """

    info_item_pair_list = __get_vertex_position_info_item_pair_list(
        src_vertex_position_info, dst_vertex_position_info)

    if not info_item_pair_list:
        return

    for info_item_pair in info_item_pair_list:

        src_info_item = info_item_pair[0]
        dst_info_item = info_item_pair[1]

        vertex_index_pair_list = \
            base_utility.mesh.get_vertex_index_pair_list_by_uv_position(
                src_info_item.target_vertex_index_list,
                src_info_item.uv_info_list,
                src_info_item.world_vertex_position_info_list,
                dst_info_item.target_vertex_index_list,
                dst_info_item.uv_info_list,
                dst_info_item.world_vertex_position_info_list
            )

        if not vertex_index_pair_list:
            continue

        __paste_vertex_position_by_vertex_index_pair_list(
            src_info_item,
            dst_info_item,
            vertex_index_pair_list,
        )


# ==================================================
def __get_vertex_position_info_item_pair_list(
        src_vertex_position_info,
        dst_vertex_position_info,
):

    if not src_vertex_position_info:
        return

    if not dst_vertex_position_info:
        return

    if not src_vertex_position_info.info_item_list:
        return

    if not dst_vertex_position_info.info_item_list:
        return

    check_transform_name = True
    if len(src_vertex_position_info.info_item_list) == 1:
        if len(dst_vertex_position_info.info_item_list) == 1:
            check_transform_name = False

    if not check_transform_name:

        src_info_item = src_vertex_position_info.info_item_list[0]
        dst_info_item = dst_vertex_position_info.info_item_list[0]

        return [[src_info_item, dst_info_item]]

    info_item_pair_list = []

    for src_info_item in src_vertex_position_info.info_item_list:

        for dst_info_item in dst_vertex_position_info.info_item_list:

            if dst_info_item.target_transform_name != \
                    src_info_item.target_transform_name:
                continue

            info_item_pair_list.append([src_info_item, dst_info_item])
            break

    if not info_item_pair_list:
        return

    return info_item_pair_list


# ==================================================
def __paste_vertex_position_by_vertex_index_pair_list(
        src_vertex_position_info_item,
        dst_vertex_position_info_item,
        vertex_index_pair_list,
):

    if not src_vertex_position_info_item:
        return

    if not dst_vertex_position_info_item:
        return

    if not vertex_index_pair_list:
        return

    target_transform = dst_vertex_position_info_item.target_transform

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    om_space = om.MSpace.kWorld

    om_vtx_position_list = om_mesh.getPoints(om_space)

    for vertex_index_pair in vertex_index_pair_list:

        src_vertex_index = vertex_index_pair[0]
        dst_vertex_index = vertex_index_pair[1]

        src_loc_position_info = \
            src_vertex_position_info_item.local_vertex_position_info_list[src_vertex_index]

        src_loc_position = src_loc_position_info[1]

        om_vtx_position_list[dst_vertex_index][0] = src_loc_position[0]
        om_vtx_position_list[dst_vertex_index][1] = src_loc_position[1]
        om_vtx_position_list[dst_vertex_index][2] = src_loc_position[2]

    om_mesh.setPoints(om_vtx_position_list, om_space)


# ==================================================
def write_info_list_to_xml_element(
        parent_element,
        vertex_position_info_list,
        is_world):

    if not vertex_position_info_list:
        return

    root_element = base_utility.xml.search_element(
        parent_element, 'VertexPositionInfoList')

    if root_element is None:
        root_element = base_utility.xml.add_element(
            parent_element, 'VertexPositionInfoList', None)

    info_element_list = base_utility.xml.search_element_list(
        root_element, 'VertexPositionInfo')

    info_element_dict = {}
    if info_element_list:

        for info_element in info_element_list:

            index_element = base_utility.xml.search_element(
                info_element, 'VertexIndex')

            if index_element is None:
                continue

            info_element_dict[int(index_element.text)] = info_element

    for p in range(len(vertex_position_info_list)):

        this_info = vertex_position_info_list[p]
        this_vertex_index = this_info[0]
        this_value = this_info[1]

        this_info_element = None

        if this_vertex_index in info_element_dict:
            this_info_element = info_element_dict[this_vertex_index]

        if this_info_element is None:

            this_info_element = base_utility.xml.add_element(
                root_element, 'VertexPositionInfo', None)

            base_utility.xml.add_element(
                this_info_element, 'VertexIndex', this_vertex_index)

        if is_world:
            base_utility.xml.add_element(
                this_info_element, 'WorldPosition', this_value)
        else:
            base_utility.xml.add_element(
                this_info_element, 'LocalPosition', this_value)


# ==================================================
def read_info_list_from_xml_element(
        parent_element, is_world):

    if parent_element is None:
        return

    root_element = base_utility.xml.search_element(
        parent_element, 'VertexPositionInfoList')

    if root_element is None:
        return

    info_element_list = base_utility.xml.search_element_list(
        root_element, 'VertexPositionInfo')

    if not info_element_list:
        return

    vertex_position_info_list = []

    for info_element in info_element_list:

        index_element = base_utility.xml.search_element(
            info_element, 'VertexIndex')

        if index_element is None:
            continue

        value_element = None

        if is_world:
            value_element = base_utility.xml.search_element(
                info_element, 'WorldPosition')

        else:
            value_element = base_utility.xml.search_element(
                info_element, 'LocalPosition')

        if value_element is None:
            continue

        vertex_position_info_list.append(
            [
                int(index_element.text),
                base_utility.list.convert_from_string(value_element.text, float)
            ]
        )

    return vertex_position_info_list
