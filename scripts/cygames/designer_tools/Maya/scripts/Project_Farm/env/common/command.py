# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os
import re
import sys
import traceback

import maya.api.OpenMaya as om
import maya.cmds as cmds

from ...base_common import classes as base_class
from ...base_common import utility as base_utility
from ...farm_common import utility as farm_utility

reload(base_class)
reload(base_utility)
reload(farm_utility)

BACKFACE_COLOR = om.MColor((0, 0, 0, 0))
BACKFACE_COLOR_SET = 'backface'
SCENE_NAME_PATTERN = r'^mdl_[^_]{3}_\d{6}\..*$'
MODEL_NAME_PATTERN = r'^(mdl_[^_]{3}_\d{5,6}_\d+|Furniture\d+(_\d{2})?)(_lod\d{1,2})?(_\d{2})?$'


class FaceInfo(object):
    def __init__(self):
        self.setting = False
        self.face_count = 0
        self.backface_count = 0

    def get_text(self):
        setting = u'設定済' if self.backface_count > 0 else '未設定'
        text = u'背面削除: {} | フェース: {} | 出力フェース: {}'
        export_face_count = self.face_count - self.backface_count
        return text.format(setting, self.face_count, export_face_count)


def set_display_color(target_node, state):
    for node in get_shape_transform_nodes(target_node):
        shape = cmds.listRelatives(node, s=True, f=True)[0]
        cmds.setAttr('{}.displayColors'.format(shape), state)


def set_alpha_cut(alpha_cut):
    algorithm = 5 if alpha_cut else 1
    cmds.setAttr('hardwareRenderingGlobals.transparencyAlgorithm', algorithm)


def get_component(target_node):
    sel_list = om.MGlobal.getSelectionListByName(target_node)

    if sel_list.isEmpty():
        return None, None

    return sel_list.getComponent(0)


def get_scene_name(path, show_saved):
    name = os.path.basename(path)
    if show_saved and cmds.file(q=True, modified=True):
        name += u' （未保存）'
    return name


def get_models():
    pattern = re.compile(MODEL_NAME_PATTERN)
    return [node for node in cmds.ls(assemblies=True) if pattern.match(node)]


def get_fbx_path(path, node):
    fbx_name = '{}{}'.format(node, farm_utility.model_define.FBX_EXT)
    fbx_path = '{}/{}'.format(os.path.dirname(path), fbx_name)
    return fbx_path


def delete_color_set(target_node, color_set):
    dag_path, _ = get_component(target_node)

    mesh_fn = om.MFnMesh(dag_path)

    if color_set:
        if color_set in mesh_fn.getColorSetNames():
            mesh_fn.deleteColorSet(color_set)


def exists_color_set(target_node, color_set):
    """カラーセットが存在するかチェック

    :param target_node: 対象ノード名
    :type target_node: str
    :param color_set: カラーセット名
    :type target_node: str
    :return: カラーセットが存在するか
    :rtype: bool
    """

    dag_path, _ = get_component(target_node)

    mesh_fn = om.MFnMesh(dag_path)

    return color_set in mesh_fn.getColorSetNames()


def get_face_by_alpha(target_node, color_set=None):
    """頂点カラーのアルファ値を基にフェースを取得

    :param target_node: 対象ノード名
    :type target_node: str
    :param color_set: カラーセット名
    :type target_node: str
    :return: アルファが0のフェース
    :rtype: MFnSingleIndexedComponent
    """

    dag_path, _ = get_component(target_node)

    mesh_iter = om.MItMeshPolygon(dag_path)
    mesh_fn = om.MFnMesh(dag_path)

    component = om.MFnSingleIndexedComponent()
    component.create(om.MFn.kMeshPolygonComponent)

    while not mesh_iter.isDone():
        mesh_color = mesh_iter.getColor(colorSetName=color_set)
        if mesh_color.a < 0.01:
            component.addElement(int(mesh_iter.index()))
        mesh_iter.next(0)

    return component


def get_shape_transform_nodes(target_node):
    nodes = cmds.listRelatives(
        target_node, ad=True, f=True, typ='transform') or []

    nodes.append(target_node)

    return [node for node in nodes if cmds.listRelatives(node, s=True)]


def get_face_info(target_node):
    face_info = FaceInfo()
    for node in get_shape_transform_nodes(target_node):
        face_info.face_count += cmds.polyEvaluate(node, f=True)
        if exists_color_set(node, BACKFACE_COLOR_SET):
            face_info.setting = True
            backfaces = get_face_by_alpha(node, BACKFACE_COLOR_SET)
            face_info.backface_count += backfaces.elementCount

    return face_info
