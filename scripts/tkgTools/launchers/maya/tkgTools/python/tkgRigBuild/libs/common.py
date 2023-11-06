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

def set_rgb_color(ctrl=None, color=[1,1,1]):
    rgb = ("R","G","B")
    shape = cmds.listRelatives(ctrl, s=True, f=True)[0]
    cmds.setAttr(shape + ".overrideEnabled",1)
    cmds.setAttr(shape + ".overrideRGBColors",1)
    for channel, color in zip(rgb, color):
        cmds.setAttr(shape + ".overrideColor{}".format(channel), color)

def set_obj_color(obj=None, color=[0.5, 0.5, 0.5], outliner=None):
    cmds.setAttr(obj+'.useObjectColor', 2)
    cmds.setAttr(obj+'.wireColorRGB', *color)

    if outliner:
        cmds.setAttr(obj+'.useOutlinerColor', 1)
        cmds.setAttr(obj+'.outlinerColor', *color)

def merge_curves(sel=None):
    if not sel:
        sel = cmds.ls(os=True)
    # cmds.select(sel[0], r=True)
    # cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
    if not sel:
        return
    shape = cmds.listRelatives(sel[0], s=True, f=True) or list()
    # cmds.select(sel[0], r=True)
    # mel.eval('channelBoxCommand -freezeAll;')
    if shape:
        for sh in shape:
            cmds.parent(sh, sel[1], s=True, r=True)

    cmds.delete(sel[0])

    cmds.select(sel[1], r=True)
