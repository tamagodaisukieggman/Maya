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

def get_perpendicular_point(pos1, pos2, obj_pos):
    # 2点間の座標を取得
    # pos1 = cmds.xform(line_point1, q=True, ws=True, t=True)
    # pos2 = cmds.xform(line_point2, q=True, ws=True, t=True)

    # 2点間のベクトル（直線の方向）を計算
    line_vector = [pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2]]

    # 別のオブジェクトの位置を取得
    # obj_pos = cmds.xform(other_object, q=True, ws=True, t=True)

    # オブジェクトから直線への最短距離ベクトルを計算
    obj_vector = [obj_pos[0] - pos1[0], obj_pos[1] - pos1[1], obj_pos[2] - pos1[2]]
    dot_product = sum(p*q for p, q in zip(obj_vector, line_vector))
    line_length_squared = sum(p*p for p in line_vector)
    t = dot_product / line_length_squared

    # 最も近い点を計算
    closest_point = [pos1[0] + t * line_vector[0], pos1[1] + t * line_vector[1], pos1[2] + t * line_vector[2]]

    return closest_point
