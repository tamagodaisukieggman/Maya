# -*- coding: utf-8 -*-

import maya.cmds as cmds

def get_shapes(node):
    shape_list = cmds.listRelatives(node, s=True, ni=True)

    if not shape_list:
        shape_list = cmds.ls(node, s=True)

    if shape_list:
        return shape_list
    else:
        return None

def get_transform(node):
    if node:
        if cmds.nodeType(node) == "transform":
            transform = node
        else:
            transform = cmds.listRelatives(node, type="transform", parent=True)[0]

        return transform

    else:
        return None

def get_bounding_box(nodes):
    x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(nodes, ce=True)
    return x1, y1, z1, x2, y2, z2
