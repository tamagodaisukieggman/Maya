# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from . import attribute


def get_long_name(target):

    if not cmds.objExists(target):
        return

    long_name_list = cmds.ls(target, l=True)

    if long_name_list is None:
        return

    if len(long_name_list) == 0:
        return

    if len(long_name_list) > 1:

        cmds.warning("find " + target + " more than two")

        return

    return long_name_list[0]


def get_short_name(target):

    if not cmds.objExists(target):
        return

    if target.find("|") < 0:
        target = get_long_name(target)

    if target is None:
        return

    split_string = target.split("|")

    if split_string is None:
        return target

    if len(split_string) == 0:
        return target

    return split_string[len(split_string) - 1]


def get_mesh_shape(target):

    long_target_name = get_long_name(target)

    if long_target_name is None:
        return

    if cmds.objectType(long_target_name) != "transform":
        return

    shapes = cmds.listRelatives(long_target_name, shapes=True, f=True)

    if shapes is None:
        return

    if len(shapes) == 0:
        return

    long_shape_name = get_long_name(shapes[0])

    if long_shape_name is None:
        return

    if cmds.objectType(long_shape_name) != "mesh":
        return

    return long_shape_name


def get_select_list(target_type=None):

    cmds.select(hi=True)

    select_list = []

    if target_type is None:
        select_list = cmds.ls(sl=True, l=True, fl=True)
    else:
        select_list = cmds.ls(sl=True, type=target_type, l=True, fl=True)

    if select_list is None:
        return []

    if len(select_list) == 0:
        return []

    return select_list


def get_shape_transform_select_list():

    cmds.select(hi=True)

    select_list = cmds.ls(sl=True, type="transform", l=True)

    if select_list is None:
        return []

    if len(select_list) == 0:
        return []

    result_list = []

    for select in select_list:

        if get_mesh_shape(select) is None:
            continue

        result_list.append(select)

    return result_list


def create_group(name, parent):

    new_group = cmds.group(name=name, em=True)

    if new_group is None:
        return

    group_path = "|" + new_group

    if parent is None:
        return group_path

    group_path = parent_object(group_path, parent)

    return group_path


def parent_object(target, parent):

    if not cmds.objExists(target):
        return

    if not cmds.objExists(parent):
        return

    parent_list = cmds.parent(target, parent)

    if parent_list is None:
        return

    if len(parent_list) == 0:
        return

    return parent + "|" + parent_list[len(parent_list) - 1]


def get_material_list(target):

    shape = get_mesh_shape(target)

    if shape is None:
        return

    shading_engine_list = cmds.listConnections(shape, type="shadingEngine")

    if shading_engine_list is None:
        return

    if len(shading_engine_list) == 0:
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

        this_material_list = cmds.listConnections(
            shading_engine + ".surfaceShader")

        if this_material_list is None:
            continue

        if len(this_material_list) == 0:
            continue

        material_list.extend(this_material_list)

    return material_list


def connect_place2d_to_file(place2d_node, file_node):

    if not cmds.objExists(place2d_node):
        return

    if not cmds.objExists(file_node):
        return

    place2d_attr_list = ["outUV",
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

    if len(file_attr_list) != len(place2d_attr_list):
        return

    for cnt in range(0, len(place2d_attr_list)):

        attribute.connect_attr(
            place2d_node, place2d_attr_list[cnt], file_node, file_attr_list[cnt])


def connect_chooser_to_place2d(chooser_node, place2d_node):

    if not cmds.objExists(chooser_node):
        return

    if not cmds.objExists(place2d_node):
        return

    chooser_attr_list = ["outVertexCameraOne",
                         "outVertexUvThree",
                         "outVertexUvTwo",
                         "outVertexUvOne",
                         "outUv"]

    place2d_attr_list = ["vertexCameraOne",
                         "vertexUvThree",
                         "vertexUvTwo",
                         "vertexUvOne",
                         "uvCoord"]

    if len(chooser_attr_list) != len(place2d_attr_list):
        return

    for cnt in range(0, len(chooser_attr_list)):

        attribute.connect_attr(
            chooser_node, chooser_attr_list[cnt], place2d_node, place2d_attr_list[cnt])


def turn_off_hardware_texture(target_material):

    if not cmds.objExists(target_material):
        return

    if not cmds.objectType(target_material, isa="lambert"):
        return

    if not attribute.exist_attr(target_material, "materialInfo"):
        return

    material_info_list = cmds.listConnections(
        target_material, t="materialInfo")

    if material_info_list is None:
        return

    for mat_info in material_info_list:

        if not attribute.exist_attr(mat_info, "texture"):
            continue

        this_connect_list = cmds.listConnections(mat_info + ".texture", p=True)

        if this_connect_list is None:
            continue

        if len(this_connect_list) == 0:
            continue

        if not cmds.isConnected(this_connect_list[0], mat_info + ".texture[0]"):
            continue

        cmds.disconnectAttr(this_connect_list[0], mat_info + ".texture[0]")


def reset_display_mode_for_lightmap(target):

    this_shape = get_mesh_shape(target)

    if this_shape is None:
        return

    cmds.setAttr(this_shape + ".displayColors", 1)
    cmds.setAttr(this_shape + ".displayColorChannel",
                 "Ambient+Diffuse", type="string")
    cmds.setAttr(this_shape + ".materialBlend", 6)


def reset_display_mode(target):

    this_shape = get_mesh_shape(target)

    if this_shape is None:
        return

    cmds.setAttr(this_shape + ".displayColors", 1)
    cmds.setAttr(this_shape + ".displayColorChannel",
                 "Ambient+Diffuse", type="string")
    cmds.setAttr(this_shape + ".materialBlend", 3)


def reset_vtxcolor_for_lightmap(target):

    this_shape = get_mesh_shape(target)

    if this_shape is None:
        return

    cmds.polyColorPerVertex(target, r=0.5, g=0.5, b=0.5)
