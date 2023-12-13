# -*- coding: utf-8 -*-

from __future__ import print_function
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
import maya.mel as mel

from .. import utility as base_utility


# ===========================================
def create_lambert_material(material_name):
    """
    マテリアル作成

    :param material_name:マテリアル名
    """

    if material_name and cmds.objExists(material_name):
        return

    shading_engine_name = material_name + 'SG'

    cmds.shadingNode('lambert', asShader=True,
                     name=material_name)

    cmds.sets(
        renderable=True, noSurfaceShader=True, empty=True,
        name=shading_engine_name
    )

    if not cmds.attributeQuery('outColor', node=material_name, exists=True):
        return

    if not cmds.attributeQuery('surfaceShader', node=shading_engine_name, exists=True):
        return

    if cmds.isConnected(material_name + '.' + 'outColor',
                         shading_engine_name + '.' + 'surfaceShader'):
        return

    try:
        cmds.connectAttr(material_name + '.' + 'outColor',
                          shading_engine_name + '.' + 'surfaceShader',
                          force=True)
    except Exception as e:
        print('{0}'.format(e))

# ===========================================
def get_material_list(target_transform):
    """
    マテリアルリスト取得

    :param target_material:対象トランスフォーム
    """

    if not target_transform or not cmds.objExists(target_transform):
        return

    if not cmds.ls(target_transform, typ='transform'):
        return

    long_target_name = cmds.ls(target_transform, l=True, typ='transform')[0]

    shape_list = cmds.listRelatives(long_target_name, shapes=True, f=True)

    if not shape_list:
        return

    shape = shape_list[0]

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

    if not target_material or not cmds.objExists(target_material):
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

        if not p2t_node or not cmds.objExists(p2t_node):
            return

        if not cmds.attributeQuery(p2t_attr_list[cnt], node=p2t_node, exists=True):
            return

        if not file_node or not cmds.objExists(file_node):
            return

        if not cmds.attributeQuery(file_attr_list[cnt], node=file_node, exists=True):
            return

        if cmds.isConnected(p2t_node + '.' + p2t_attr_list[cnt],
                            file_node + '.' + file_attr_list[cnt]):
            return

        try:
            cmds.connectAttr(material_name + '.' + p2t_attr_list[cnt],
                            file_node + '.' + file_attr_list[cnt],
                            force=True)
        except Exception as e:
            print('{0}'.format(e))
