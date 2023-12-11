# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel

from .. import utility as base_utility

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass


# ===========================================
def create_lambert_material(material_name):
    """
    マテリアル作成

    :param material_name:マテリアル名
    """

    if base_utility.node.exists(material_name):
        return

    shading_engine_name = material_name + 'SG'

    cmds.shadingNode('lambert', asShader=True,
                     name=material_name)

    cmds.sets(
        renderable=True, noSurfaceShader=True, empty=True,
        name=shading_engine_name
    )

    base_utility.attribute.connect(
        material_name, 'outColor',
        shading_engine_name, 'surfaceShader'
    )


# ===========================================
def get_material_list(target_transform):
    """
    マテリアルリスト取得

    :param target_material:対象トランスフォーム
    """

    shape = base_utility.transform.get_shape(target_transform)

    if shape is None:
        return

    shading_engine_list = cmds.listConnections(shape, type="shadingEngine")

    if not shading_engine_list:
        return

    fix_shading_engine_list = []

    for shading_engine in shading_engine_list:

        exist = False
        for fix_shading_engine in fix_shading_engine_list:

            if shading_engine == fix_shading_engine:
                exist = True

        if exist:
            continue

        fix_shading_engine_list.append(shading_engine)

    material_list = []

    for shading_engine in fix_shading_engine_list:

        this_material_list =\
            cmds.listConnections(shading_engine + ".surfaceShader")

        if not this_material_list:
            return

        material_list.extend(this_material_list)

    return material_list


# ==================================================
def get_shading_group(target_material):
    """
    マテリアルからシェーディンググループを取得

    :param target_material:対象マテリアル
    """

    if not base_utility.node.exists(target_material):
        return

    shading_group_list = \
        cmds.listConnections(target_material, t='shadingEngine')

    if not shading_group_list:
        return

    return shading_group_list[0]


# ==================================================
def assign_material(target_material, target_list):
    """
    マテリアルを割り当て

    :param target_material:対象マテリアル
    :param target_list:対象リスト
    """

    material_sg = get_shading_group(target_material)

    if material_sg is None:
        return

    if not target_list:
        return

    cmds.select(target_list, r=True)
    cmds.sets(e=True, forceElement=material_sg)


# ==================================================
def get_node_list_with_material(target_material, target_list=None):
    """
    マテリアルを使用しているノードリストを取得

    :param target_material:対象マテリアル
    :param target_list:対象リスト Noneのときはすべて対象
    """

    cmds.select(cl=True)

    material_sg = get_shading_group(target_material)

    if material_sg is None:
        return

    if not target_list:
        cmds.select(material_sg, r=True, ne=False)
        return cmds.ls(sl=True, l=True, fl=True)

    cmds.select(target_list, r=True)
    cmds.select(target_material, add=True)

    mel.eval("HideUnselectedObjects")

    cmds.select(material_sg, r=True, ne=False)
    cmds.select(vis=True)

    mel.eval("ShowLastHidden")

    return cmds.ls(sl=True, l=True, fl=True)


# ===========================================
def connect_p2t_node_to_file_node(p2t_node, file_node):
    """
    place2dTextureノードをfileノードへ接続

    :param p2t_node:対象place2dTextureノード
    :param file_node:対象ファイルノード
    """

    if not cmds.objExists(p2t_node):
        return

    if not cmds.objExists(file_node):
        return

    p2t_attr_list = ["outUV",
                     "outUvFilterSize",
                     "coverage",
                     "translateFrame",
                     "rotateFrame",
                     "mirrorU",
                     "mirrorV",
                     "stagger",
                     "wrapU",
                     "wrapV",
                     "repeatUV",
                     "vertexUvOne",
                     "vertexUvTwo",
                     "vertexUvThree",
                     "vertexCameraOne",
                     "noiseUV",
                     "offset",
                     "rotateUV"]

    file_attr_list = ["uvCoord",
                      "uvFilterSize",
                      "coverage",
                      "translateFrame",
                      "rotateFrame",
                      "mirrorU",
                      "mirrorV",
                      "stagger",
                      "wrapU",
                      "wrapV",
                      "repeatUV",
                      "vertexUvOne",
                      "vertexUvTwo",
                      "vertexUvThree",
                      "vertexCameraOne",
                      "noiseUV",
                      "offset",
                      "rotateUV"]

    if len(file_attr_list) != len(p2t_attr_list):
        return

    for cnt in range(0, len(p2t_attr_list)):

        base_utility.attribute.connect(
            p2t_node,
            p2t_attr_list[cnt],
            file_node,
            file_attr_list[cnt])
