# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om2

import math

def reset_transform(obj, func):
    wt = cmds.xform(obj, q=True, t=True, ws=True)
    wr = cmds.xform(obj, q=True, ro=True, ws=True)

    func()

    cmds.xform(obj, t=wt, ro=wr, ws=True, a=True)

def quaternionToEuler(obj=None, setkey=None):
    rot = cmds.xform(obj, q=True, ro=True, os=True)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)

    cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=True, a=True)

    if setkey:
        cmds.setKeyframe(obj, at='rotate')

    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)
