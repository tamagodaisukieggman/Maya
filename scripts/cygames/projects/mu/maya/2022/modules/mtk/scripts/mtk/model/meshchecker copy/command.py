# -*- coding: utf-8 -*-
u"""1行説明

:詳細: file:///Z:/mtku/tools/maya/doc/manual/sources/window/meshchecker.rst


:TestScene:
>>> maya_scene = 'Z:/mtku/work/env/bossBattlle/scenes/boss_battle_concept03.ma'
>>> cmds.file(maya_scene, f=True, o=True)
u'Z:/mtku/work/env/bossBattlle/scenes/boss_battle_concept03.ma'
"""
import math

import maya.cmds as cmds

import mtku.maya.utils.plugin
from mtku.maya.mtklog import MtkLog


logger = MtkLog(__name__)


def get_edge_length(edge):
    u"""エッジの長さの取得

    :param edge: エッジ
    :return: 長さ(cm)

    :example:
    >>> get_edge_length('pCube54.e[184]')
    872.4302800268722
    """
    vertices = cmds.ls(cmds.polyListComponentConversion(edge, tv=True), fl=True)
    pos1 = cmds.pointPosition(vertices[0], w=True)
    pos2 = cmds.pointPosition(vertices[1], w=True)
    vector = (pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2])

    length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])

    return length


def get_face_angle(face, axis):
    u"""faceの法線と指定した軸がなす角度(degree)を取得

    :param face: face
    :param axis: 軸
    :return: degree

    :example:
    >>> get_face_angle('polySurface30.f[33]', 'x')
    0.0
    """
    mtku.maya.utils.plugin.load('polyfaceangle')
    if axis == 'x':
        face, angle = cmds.mtkPolyFaceAngle(face, x=True)
    elif axis == 'z':
        face, angle = cmds.mtkPolyFaceAngle(face, z=True)
    else:
        face, angle = cmds.mtkPolyFaceAngle(face, y=True)

    return angle
