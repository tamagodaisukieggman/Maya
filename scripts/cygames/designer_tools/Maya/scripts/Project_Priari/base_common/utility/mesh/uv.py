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
def get_all_uv_info_list(target_transform):
    """
    全てのUV座標情報を取得

    :param target_transform: 対象トランスフォーム

    :return: [UV番号,[u,v]]の配列
    """

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    current_uvset = \
        base_utility.mesh.uvset.get_current(target_transform)

    if current_uvset is None:
        return

    om_uv_list = om_mesh.getUVs(current_uvset)

    uv_index_list = \
        base_utility.mesh.get_uv_index_list(target_transform)

    all_info_list = []

    for p in range(len(uv_index_list)):

        uv_index = uv_index_list[p]

        this_uv_u = om_uv_list[0][uv_index]
        this_uv_v = om_uv_list[1][uv_index]

        this_uv_info = [
            uv_index,
            [this_uv_u, this_uv_v]
        ]

        all_info_list.append(this_uv_info)

    all_info_list.sort()

    return all_info_list


# ==================================================
def get_all_uv_info_list_with_vertex_index(target_transform):
    """
    全てのUV座標情報を頂点情報入りで取得

    :param target_transform: 対象トランスフォーム

    :return: [uv番号 ,頂点番号, 頂点フェース番号,[u,v]]の配列
    """

    all_info_list = get_all_uv_info_list(target_transform)

    if not all_info_list:
        return

    new_all_info_list = []

    for this_info in all_info_list:

        this_uv_index = this_info[0]
        this_uv_position = this_info[1]

        this_uv = '{0}.map[{1}]'.format(target_transform, this_uv_index)

        this_vertex_face_list = \
            cmds.polyListComponentConversion(this_uv, tvf=True)

        if not this_vertex_face_list:
            continue

        this_vertex_face_list = cmds.ls(
            this_vertex_face_list,
            l=True, fl=True)

        if not this_vertex_face_list:
            continue

        for this_vertex_face in this_vertex_face_list:

            temp_list = base_utility.mesh.get_vertex_and_face_index(
                this_vertex_face
            )

            vertex_index = temp_list[0]
            vertex_face_index = temp_list[1]

            new_all_info_list.append(
                [this_uv_index, vertex_index, vertex_face_index, this_uv_position]
            )

    return new_all_info_list


# ==================================================
def set_uv_info_list(
        target_transform,
        uv_info_list
):
    """
    UV座標を設定

    :param target_transform: 対象トランスフォーム
    :param uv_info_list: [UV番号,[u,v]]の配列
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    if not uv_info_list:
        return

    current_uvset = base_utility.mesh.uvset.get_current(target_transform)

    if current_uvset is None:
        return

    om_mesh = base_utility.open_maya.get_om_mesh(target_transform)

    if om_mesh is None:
        return

    all_info_list = get_all_uv_info_list(target_transform)

    if not all_info_list:
        return

    for p in range(len(uv_info_list)):

        this_info = uv_info_list[p]

        this_uv_index = this_info[0]

        if this_uv_index >= len(all_info_list):
            continue

        all_info_list[this_uv_index] = this_info

    u_value_list = []
    v_value_list = []

    for p in range(len(all_info_list)):

        u_value_list.append(all_info_list[p][1][0])
        v_value_list.append(all_info_list[p][1][1])

    om_mesh.setUVs(u_value_list, v_value_list, current_uvset)


# ==================================================
def write_info_list_to_xml_element(
        parent_element, uv_info_list):

    if parent_element is None:
        return

    if not uv_info_list:
        return

    root_element = base_utility.xml.add_element(
        parent_element, 'UVInfoList', None)

    for p in range(len(uv_info_list)):

        this_info = uv_info_list[p]

        this_uv_index = this_info[0]
        this_vertex_index = -1
        this_vertexface_index = -1
        this_value = -1

        if len(this_info) == 2:

            this_value = this_info[1]

        else:

            this_vertex_index = this_info[1]
            this_vertexface_index = this_info[2]
            this_value = this_info[3]

        this_info_element = base_utility.xml.add_element(
            root_element, 'UVInfo', None)

        base_utility.xml.add_element(
            this_info_element, 'UVIndex', this_uv_index)

        if this_vertex_index >= 0:
            base_utility.xml.add_element(
                this_info_element, 'VertexIndex', this_vertex_index)

        if this_vertexface_index >= 0:
            base_utility.xml.add_element(
                this_info_element, 'VertexFaceIndex', this_vertexface_index)

        base_utility.xml.add_element(
            this_info_element, 'UVPosition', this_value)


# ==================================================
def read_info_list_from_xml_element(parent_element):

    if parent_element is None:
        return

    root_element = base_utility.xml.search_element(
        parent_element, 'UVInfoList')

    if root_element is None:
        return

    info_element_list = base_utility.xml.search_element_list(
        root_element, 'UVInfo')

    if not info_element_list:
        return

    uv_info_list = []

    for info_element in info_element_list:

        uv_index_element = base_utility.xml.search_element(
            info_element, 'UVIndex')

        if uv_index_element is None:
            continue

        uv_position_element = base_utility.xml.search_element(
            info_element, 'UVPosition')

        if uv_position_element is None:
            continue

        vertex_index_element = base_utility.xml.search_element(
            info_element, 'VertexIndex')

        vertex_face_index_element = base_utility.xml.search_element(
            info_element, 'VertexFaceIndex')

        if vertex_index_element is None:

            temp_string = uv_position_element.replace('[', '')
            temp_string = temp_string.replace(']', '')

            split_str_list = temp_string.split(',')

            uv_position_element_list = []

            for split_str in split_str_list:

                result_list.append(float(split_str))

            uv_info_list.append(
                [
                    int(uv_index_element.text),
                    uv_position_element_list
                ]
            )

        else:

            uv_info_list.append(
                [
                    int(uv_index_element.text),
                    int(vertex_index_element.text),
                    int(vertex_face_index_element.text),
                    uv_position_element_list
                ]
            )

    return uv_info_list
