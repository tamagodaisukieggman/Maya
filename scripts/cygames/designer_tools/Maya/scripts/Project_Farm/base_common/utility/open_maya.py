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
import maya.api.OpenMaya as om

import maya.OpenMaya as om_old
import maya.OpenMayaAnim as om_anim_old

from .. import utility as base_utility


# ==================================================
def get_om_dag_path(target_node):
    """
    OpenMayaパス取得
    """

    if not target_node or not cmds.objExists(target_node):
        return

    om_select_list = om.MSelectionList()
    om_select_list.add(target_node)

    om_dag_path = om_select_list.getDagPath(0)

    return om_dag_path


# ==================================================
def get_om_object(target_node):
    """OpenMayaオブジェクト取得"""

    if not target_node or not cmds.objExists(target_node):
        return

    om_select_list = om.MSelectionList()
    om_select_list.add(target_node)

    om_object = om_select_list.getDependNode(0)

    return om_object


# ==================================================
def get_om_mesh(target_transform):
    """OpenMayaメッシュ取得"""

    om_dag_path = get_om_dag_path(target_transform)

    if om_dag_path is None:
        return

    om_mesh = om.MFnMesh(om_dag_path)

    return om_mesh


# ==================================================
def get_om_color(color):
    """配列ColorからOpenMayaColorへ変換"""

    om_color = om.MColor()

    om_color.r = color[0]
    om_color.g = color[1]
    om_color.b = color[2]
    om_color.a = color[3]

    return om_color


# ==================================================
def get_color(om_color):
    """OpenMayaColorから配列Colorへ変換"""

    color = [0] * 4

    color[0] = om_color.r
    color[1] = om_color.g
    color[2] = om_color.b
    color[3] = om_color.a

    return color


# ==================================================
def get_om_vector(vector):
    """配列VectorからOpenMayaVectorへ変換"""

    om_vector = om.MVector()

    om_vector.x = vector[0]
    om_vector.y = vector[1]
    om_vector.z = vector[2]

    return om_vector


# ==================================================
def get_vector(om_vector):
    """OpenMayaVectorから配列Vectorへ変換"""

    vector = [0] * 3

    vector[0] = om_vector.x
    vector[1] = om_vector.y
    vector[2] = om_vector.z

    return vector


# ==================================================
def get_om_old_dag_path(target_node):
    """
    パス取得 (OpenMaya1.0)

    :param target_node:対象ノード

    :return: パス (OpenMaya1.0)
    """

    if not target_node or not cmds.objExists(target_node):
        return

    om_select_list = om_old.MSelectionList()
    om_select_list.add(target_node)

    om_dag_path = om_old.MDagPath()

    om_select_list.getDagPath(0, om_dag_path)

    return om_dag_path


# ==================================================
def get_om_old_object(target_node):
    """
    オブジェクト取得 (OpenMaya1.0)

    :param target_node:対象ノード

    :return: オブジェクト (OpenMaya1.0)
    """

    if not target_node or not cmds.objExists(target_node):
        return

    om_select_list = om_old.MSelectionList()
    om_select_list.add(target_node)

    om_object = om_old.MObject()

    om_select_list.getDependNode(0, om_object)

    return om_object


# ==================================================
def get_om_old_mesh(target_transform):
    """
    メッシュ取得 (OpenMaya1.0)

    :param target_node:対象トランスフォーム

    :return: メッシュ (OpenMaya1.0)
    """

    om_dag_path = get_om_old_dag_path(target_transform)

    if om_dag_path is None:
        return

    om_mesh = om_old.MFnMesh(om_dag_path)

    return om_mesh


# ==================================================
def get_om_old_skin_cluster(skin_cluster):
    """
    スキンクラスター取得 (OpenMaya1.0)

    :param target_node:対象スキンクラスター

    :return: スキンクラスター (OpenMaya1.0)
    """

    if not skin_cluster or not cmds.objExists(skin_cluster):
        return

    om_select_list = om_old.MSelectionList()
    om_select_list.add(skin_cluster)

    om_cluster = om_old.MObject()
    om_select_list.getDependNode(0, om_cluster)

    om_skin_cluster = om_anim_old.MFnSkinCluster(om_cluster)

    return om_skin_cluster


# ==================================================
def get_om_old_joint_dag_path_list(om_skin_cluster):
    """
    ジョイントパスリスト取得 (OpenMaya1.0)

    :param om_skin_cluster:対象スキンクラスター

    :return: ジョイントパス (OpenMaya1.0)
    """

    if om_skin_cluster is None:
        return

    om_joint_dag_path_list = om_old.MDagPathArray()
    om_skin_cluster.influenceObjects(om_joint_dag_path_list)

    return om_joint_dag_path_list


# ==================================================
def get_om_old_joint_index_list(om_skin_cluster):
    """
    ジョイント番号リスト取得 (OpenMaya1.0)

    :param om_skin_cluster:対象スキンクラスター

    :return: ジョイント番号リスト (OpenMaya1.0)
    """

    if om_skin_cluster is None:
        return

    om_joint_dag_path_list = \
        get_om_old_joint_dag_path_list(om_skin_cluster)

    om_joint_index_list = om_old.MIntArray(
        om_joint_dag_path_list.length(), 0)

    for p in range(om_joint_dag_path_list.length()):
        om_joint_index_list[p] = \
            int(om_skin_cluster.indexForInfluenceObject(
                om_joint_dag_path_list[p]))

    return om_joint_index_list


# ==================================================
def get_om_old_joint_physical_index_list(om_skin_cluster):
    """
    ジョイントフィジカル番号リスト取得 (OpenMaya1.0)

    :param om_skin_cluster:対象スキンクラスター

    :return: ジョイント番号リスト (OpenMaya1.0)
    """

    if om_skin_cluster is None:
        return

    om_joint_dag_path_list = \
        get_om_old_joint_dag_path_list(om_skin_cluster)

    om_joint_index_list = om_old.MIntArray(
        om_joint_dag_path_list.length(), 0)

    for p in range(om_joint_dag_path_list.length()):
        om_joint_index_list[p] = p

    return om_joint_index_list


# ==================================================
def get_om_old_weight_list(target_transform):
    """
    OpenMaya1.0でのウェイトリスト取得

    :param target_transform: 対象トランスフォーム

    :return: OpenMaya1.0でのウェイトリスト
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    mesh_shape = base_utility.mesh.get_mesh_shape(target_transform)

    if mesh_shape is None:
        return

    skin_cluster = \
        base_utility.mesh.skin.get_skin_cluster(target_transform)

    if skin_cluster is None:
        return

    om_object = get_om_old_object(target_transform)
    om_dag_path = get_om_old_dag_path(mesh_shape)
    om_skin_cluster = get_om_old_skin_cluster(skin_cluster)

    om_weight_list = om_old.MDoubleArray()

    om_mesh_vertex = om_old.MItMeshVertex(om_object)
    om_vertex_index_list = om_old.MIntArray(om_mesh_vertex.count(), 0)
    for p in range(om_vertex_index_list.length()):
        om_vertex_index_list[p] = p

    om_single_Id_comp = om_old.MFnSingleIndexedComponent()
    vertex_comp = om_single_Id_comp.create(om_old.MFn.kMeshVertComponent)

    inf_count_util = om_old.MScriptUtil(0)
    inf_count_ptr = inf_count_util.asUintPtr()

    om_skin_cluster.getWeights(
        om_dag_path, vertex_comp, om_weight_list, inf_count_ptr)

    return om_weight_list
