# -*- coding: utf-8 -*-
import math

import maya.cmds as cmds

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point

def mid_point(objA=None, objB=None, percentage=0.5):
    pos1 = cmds.xform(objA, q=True, t=True, ws=True)
    pos2 = cmds.xform(objB, q=True, t=True, ws=True)
    return get_mid_point(pos1, pos2, percentage)

def step_positions(nodes=None, i=1, base_include=False, tip_include=False):
    """
    ノード2点間に配置するための位置を配置予定の数に応じて取得する
    """
    if i == 1:
        step = i / 2
    elif i >= 2:
        step = 1 / (i+1)
        if base_include and not tip_include:
            step = 1 / i
        elif not base_include and tip_include:
            step = 1 / i
        elif base_include and tip_include:
            step = 1 / (i-1)

    positions = []
    for j in range(i):
        percentage = step * (j+1)
        if base_include and not tip_include:
            percentage = step * j
        elif not base_include and tip_include:
            percentage = step * (j+1)
        elif base_include and tip_include:
            percentage = step * j

        mp = mid_point(nodes[0], nodes[1], percentage)
        positions.append(mp)

    return positions