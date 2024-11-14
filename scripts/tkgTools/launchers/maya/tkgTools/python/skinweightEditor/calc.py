# -*- coding: utf-8 -*-
import math

import maya.cmds as cmds
import maya.mel as mel

def get_distance(obj_A=None, obj_B=None, gobj_A=None, gobj_B=None):
    if not gobj_A:
        gobj_A = cmds.xform(obj_A, q=True, t=True, ws=True)

    if not gobj_B:
        gobj_B = cmds.xform(obj_B, q=True, t=True, ws=True)

    x = math.pow(gobj_A[0] - gobj_B[0], 2)
    y = math.pow(gobj_A[1] - gobj_B[1], 2)
    z = math.pow(gobj_A[2] - gobj_B[2], 2)

    return math.sqrt(x + y + z)