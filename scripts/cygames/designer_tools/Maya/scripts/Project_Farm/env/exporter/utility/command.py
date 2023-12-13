# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from importlib import reload
except:
    pass

import maya.api.OpenMaya as om
import maya.cmds as cmds

from ...common import command as env_cmd

reload(env_cmd)


def get_cameras():
    cameras = cmds.ls(l=True, typ='camera')
    transforms = [cmds.listRelatives(cam, p=True)[0] for cam in cameras]
    return [cam for cam in transforms if not cmds.camera(cam, q=True, sc=True)]


def get_translate_values(target_node, start=None, end=None):
    if start is None:
        start = int(cmds.playbackOptions(q=True, ast=True))
    if end is None:
        end = int(cmds.playbackOptions(q=True, aet=True))

    values = []

    current_time = cmds.currentTime(q=True)

    for i in range(start, end + 1):
        cmds.currentTime(i)
        v = cmds.xform(target_node, q=True, t=True, ws=True)
        values.append(v)

    cmds.currentTime(current_time)

    return values


def set_backface_color(target_node, positions, add=True, remove=True):
    for node in env_cmd.get_shape_transform_nodes(target_node):
        frontfaces = get_frontfaces(node, positions).getElements()

        if add:
            face_count = cmds.polyEvaluate(node, f=True)
            backfaces = list(set(range(face_count)) - set(frontfaces))
            colors = [env_cmd.BACKFACE_COLOR for _ in backfaces]
            set_face_colors(node, backfaces, colors, env_cmd.BACKFACE_COLOR_SET)

        if remove:
            remove_face_colors(node, frontfaces, env_cmd.BACKFACE_COLOR_SET)


def get_frontfaces(target_node, positions):
    dag_path, _ = env_cmd.get_component(target_node)

    mesh_iter = om.MItMeshPolygon(dag_path)
    mesh_fn = om.MFnMesh(dag_path)

    component = om.MFnSingleIndexedComponent()
    component.create(om.MFn.kMeshPolygonComponent)

    while not mesh_iter.isDone():
        for pos in positions:
            index = int(mesh_iter.index())
            direction = om.MPoint(pos) - mesh_iter.center(om.MSpace.kWorld)
            # MItMeshPolygonから直接ワールドスペースの法線が取得できないためMFnMeshから取得
            normal = mesh_fn.getPolygonNormal(index, om.MSpace.kWorld)
            d = normal * direction
            if d >= 0:
                component.addElement(index)
                break
        mesh_iter.next(0)

    return component


def remove_face_colors(target_node, indices, color_set=None):
    dag_path, _ = env_cmd.get_component(target_node)

    mesh_fn = om.MFnMesh(dag_path)

    if color_set:
        if color_set not in mesh_fn.getColorSetNames():
            return

    if indices:
        mesh_fn.removeFaceColors(indices)


def set_face_colors(target_node, indices, colors, color_set=None):
    dag_path, _ = env_cmd.get_component(target_node)

    mesh_fn = om.MFnMesh(dag_path)

    if color_set:
        if color_set not in mesh_fn.getColorSetNames():
            mesh_fn.createColorSet(color_set, True)
        mesh_fn.setCurrentColorSetName(color_set)

    if indices:
        mesh_fn.setFaceColors(colors, indices)
