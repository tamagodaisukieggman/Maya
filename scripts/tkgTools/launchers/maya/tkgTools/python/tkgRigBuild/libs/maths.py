# -*- coding: utf-8 -*-
from imp import reload
import math

import maya.cmds as cmds

def vector_from_two_points(point_a=None, point_b=None):
    pos_a = get_world_pose(point_a)
    pos_b = get_world_pose(point_b)

    return [b-a for a, b in zip(pos_a, pos_b)]


def get_world_pose(pos):
    if isinstance(pos, list) or isinstance(pos, tuple) and len(pos) == 3:
        pass
    elif isinstance(pos, str) or isinstance(pos, unicode):
        pos = cmds.xform(pos,
                         query=True,
                         worldSpace=True,
                         translation=True)
    else:
        cmds.error('Must provide cartesian position or transform node for pos.')

    return pos


def vector_length(vector=[]):
    return pow(sum([pow(n, 2) for n in vector]), 0.5)


def distance_between(point_a=None, point_b=None):
    vector_ab = vector_from_two_points(point_a, point_b)
    distance = vector_length(vector_ab)
    return distance

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def round_value(value=None, digit=3):
    return truncate(round(value, digit), digit)
