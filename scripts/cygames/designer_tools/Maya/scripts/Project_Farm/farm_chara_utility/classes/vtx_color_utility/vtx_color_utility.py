# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
    from importlib import reload
except:
    pass

import re
import operator

import maya.cmds as cmds
import maya.api.OpenMaya as om

from ....base_common.classes import vertex
from ....base_common.classes import kd_tree

reload(vertex)
reload(kd_tree)


def set_color_to_selected_vtx(color_rgb):
    """選択頂点にカラーをセット

    Args:
        color_rgb (list): セットするrgb
    """

    obj_vtx_list = __get_selected_obj_vtx_list()

    if not obj_vtx_list:
        return

    set_om_color = om.MColor()
    set_om_color.r = color_rgb[0]
    set_om_color.g = color_rgb[1]
    set_om_color.b = color_rgb[2]

    for obj_vtx_dict in obj_vtx_list:
        obj = obj_vtx_dict['obj']
        ids = obj_vtx_dict['ids']
        __set_vtx_color(obj, ids, set_om_color)


def replace_vtx_color(target_rgb, set_rgb, torelance=0.0001):
    """頂点カラーの置き換え

    Args:
        target_rgb (list): 置き換え対象のrgb
        set_rgb (list): 置き換えるrgb
        torelance (float, optional): 一致判定の範囲. Defaults to 0.0001.
    """

    obj_vtx_list = __get_selected_obj_vtx_list()

    if not obj_vtx_list:
        return

    set_om_color = om.MColor()
    set_om_color.r = set_rgb[0]
    set_om_color.g = set_rgb[1]
    set_om_color.b = set_rgb[2]

    for obj_vtx_dict in obj_vtx_list:

        obj = obj_vtx_dict['obj']
        ids = obj_vtx_dict['ids']

        colors = __get_vtx_colors(obj, ids)

        match_color_ids = []

        for id, color in zip(ids, colors):

            is_match = True

            for i in range(3):
                if (color[i] < target_rgb[i] - torelance) or (target_rgb[i] + torelance < color[i]):
                    is_match = False
                    break

            if is_match:
                match_color_ids.append(id)

        __set_vtx_color(obj, match_color_ids, set_om_color)


def symmetry_vtx_color(symmetry_axis='x', is_positive_src=True, torelance=0.001):
    """頂点カラーのミラーリング

    Args:
        symmetry_axis (str, optional): 対称軸. 'x','y' or 'z' Defaults to 'x'.
        is_positive_src (bool, optional): 検索元は対称軸正方向か. Defaults to True.
        torelance (float, optional): 対称頂点と判定する距離. Defaults to 0.001.
    """

    obj_vtx_list = __get_selected_obj_vtx_list()

    if not obj_vtx_list:
        return

    for obj_vtx_dict in obj_vtx_list:

        obj = obj_vtx_dict['obj']
        ids = obj_vtx_dict['ids']
        colors = __get_vtx_colors(obj, ids)

        src_dst_pair_list = __get_symmetry_src_dst(obj, ids, symmetry_axis, is_positive_src, torelance)

        set_ids = []
        set_colors = []

        for src_dst_pair in src_dst_pair_list:
            src_id = src_dst_pair[0]
            dst_id = src_dst_pair[1]

            for id, color in zip(ids, colors):
                if id == src_id:
                    set_ids.append(dst_id)
                    set_colors.append(color)

        __set_vtx_colors(obj, set_ids, set_colors)


def __get_vtx_colors(target_obj, ids):
    """対象の頂点のカラーを取得

    Args:
        target_obj (str): 対象オブジェクト
        ids (list): 頂点番号のintのリスト

    Returns:
        list: 対象頂点のMColorのリスト
    """

    if not cmds.objExists(target_obj):
        return []

    current_colorsets = cmds.polyColorSet(target_obj, q=True, currentColorSet=True)

    if not current_colorsets:
        return []

    om_select_list = om.MSelectionList()
    om_select_list.add(target_obj)
    om_dag_path = om_select_list.getDagPath(0)
    om_mesh = om.MFnMesh(om_dag_path)

    om_colors = om_mesh.getVertexColors(current_colorsets[0])

    result_list = []
    for i, om_color in enumerate(om_colors):
        if i in ids:
            result_list.append(om.MColor(om_color))

    return result_list


def __set_vtx_color(target_obj, ids, om_color):
    """対象の頂点にカラーをセット

    Args:
        target_obj (str): 対象オブジェクト
        ids (list): 頂点番号のintのリスト
        om_color (MColor): セットするMColor
    """

    if not cmds.objExists(target_obj) or not ids:
        return

    vtxs = ['{}.vtx[{}]'.format(target_obj, str(x)) for x in ids]

    cmds.polyColorPerVertex(vtxs, r=om_color[0], g=om_color[1], b=om_color[2], cdo=True)


def __set_vtx_colors(target_obj, ids, om_colors):
    """対象の頂点にカラーをセット

    Args:
        target_obj (str): 対象オブジェクト
        ids (list): 頂点番号のintのリスト
        om_colors (list): idsに対応したセットするMColorのリスト
    """

    if not cmds.objExists(target_obj):
        return

    for id, om_color in zip(ids, om_colors):
        cmds.polyColorPerVertex('{}.vtx[{}]'.format(target_obj, str(id)), rgb=[om_color[0], om_color[1], om_color[2]])


def __get_selected_obj_vtx_list():
    """選択しているオブジェクトと頂点番号情報の取得

    Returns:
        list: [{'obj': オブジェクト名, 'ids': [頂点番号のリスト]} ,,,,]
    """

    obj_vtx_dict_list = []
    selections = cmds.ls(sl=True)

    if not selections:
        return obj_vtx_dict_list

    vtxs = cmds.ls(cmds.polyListComponentConversion(selections, tv=True), fl=True, l=True)

    for vtx in vtxs:

        m = re.search(r'(.+)\.vtx\[(\d+)\]$', vtx)

        if not m:
            continue

        obj = m.group(1)
        id = int(m.group(2))

        is_hit = False

        for obj_vtx_dict in obj_vtx_dict_list:
            if obj_vtx_dict['obj'] == obj:
                obj_vtx_dict['ids'].append(id)
                is_hit = True
                break

        if not is_hit:
            obj_vtx_dict_list.append({'obj': obj, 'ids': [id]})

    return obj_vtx_dict_list


def __get_symmetry_src_dst(target_obj, src_ids, symmetry_axis='x', is_positive_src=True, torelance=0.001):
    """指定した頂点と軸対称にある頂点を検索

    Args:
        target_obj (str): 検索対象のオブジェクト
        src_ids (list): 検索元となる頂点番号のリスト
        symmetry_axis (str, optional): 対称軸.'x','y' or 'z' Defaults to 'x'.
        is_positive_src (bool, optional): 検索元は対称軸正方向か. Defaults to True.
        torelance (float, optional): 対称頂点と判定する距離. Defaults to 0.001.

    Returns:
        list: [[検索元の頂点番号, 対称の頂点番号],,,,]
    """

    src_dst_id_pair_list = []

    if not cmds.objExists(target_obj):
        return src_dst_id_pair_list

    # 対称の中心位置を取得
    center_pos = cmds.xform(target_obj, q=True, t=True, ws=True)
    center_value = 0

    if symmetry_axis == 'x':
        center_value = center_pos[0]
    elif symmetry_axis == 'y':
        center_value = center_pos[1]
    elif symmetry_axis == 'z':
        center_value = center_pos[2]

    # 全頂点の位置座標を取得
    all_vtx_datas = vertex.get_vtx_datas([target_obj])

    # 全頂点から検索元と検索対象を選別する
    base_datas = []  # 検索元の頂点データを格納するリスト.
    target_datas = []  # 検索対象の頂点データを格納するリスト.
    this_tree = None

    for data in all_vtx_datas:

        vtx_value = 0

        if symmetry_axis == 'x':
            vtx_value = data.position[0]
        elif symmetry_axis == 'y':
            vtx_value = data.position[1]
        elif symmetry_axis == 'z':
            vtx_value = data.position[2]

        if is_positive_src:

            if vtx_value - center_value > 0 and data.index in src_ids:
                base_datas.append(data)
            elif vtx_value - center_value < 0:
                target_datas.append(data)

        else:

            if vtx_value - center_value < 0 and data.index in src_ids:
                base_datas.append(data)
            elif vtx_value - center_value > 0:
                target_datas.append(data)

    this_tree = kd_tree.KDTree(target_datas, operator.attrgetter('position'), 3)

    for base_data in base_datas:

        mirror_pos = __get_mirror_pos(base_data.position, center_pos, symmetry_axis)
        mirror_datas = this_tree.search_radius(om.MPoint(mirror_pos), torelance)

        if mirror_datas:
            for mirror_data in mirror_datas:
                src_dst_id_pair_list.append([base_data.index, mirror_data.index])

    return src_dst_id_pair_list


def __get_mirror_pos(pos, center_pos, symmetry_axis):
    """対称位置の取得

    Args:
        pos (list): 元の位置. [x, y, z]
        center_pos (list): 対称の基準点. [x, y, z]
        symmetry_axis (str): 対称軸. 'x','y' or 'z'

    Returns:
        list: 対称位置. [x, y, z]
    """

    if symmetry_axis == 'x':
        return [center_pos[0] + (center_pos[0] - pos[0]), pos[1], pos[2]]
    elif symmetry_axis == 'y':
        return [pos[0], center_pos[1] + (center_pos[1] - pos[1]), pos[2]]
    elif symmetry_axis == 'z':
        return [pos[0], pos[1], center_pos[2] + (center_pos[2] - pos[2])]
    else:
        return pos
