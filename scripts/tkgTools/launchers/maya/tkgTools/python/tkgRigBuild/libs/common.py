# -*- coding: utf-8 -*-
from collections import OrderedDict
import re

import maya.cmds as cmds

import tkgRigBuild.libs.modifyJoints as tkgMJ

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

def create_loft(nodes=None, name='loft_suf', axis='x'):
    if not nodes:
        nodes = cmds.ls(os=True)

    move_axis = {
        'x':[[1, 0, 0], [-1, 0, 0]],
        'y':[[0, 1, 0], [0, -1, 0]],
        'z':[[0, 0, 1], [0, 0, -1]]
    }

    moves = move_axis[axis]

    pts=[cmds.xform(j,q=True,ws=True,t=True) for j in nodes]
    cuC = cmds.curve(ep=pts, d=3, n='{0}_center_crv'.format(nodes[0]))
    cuR = cmds.curve(ep=pts, d=3)
    cmds.move(moves[0][0],moves[0][1],moves[0][2],cuR,ls=True) #+z axis
    cuL = cmds.duplicate(cuR)
    cmds.move(moves[1][0],moves[1][1],moves[1][2],cuL,ls=True) #-z axis
    lofted=cmds.loft(cuR, cuL, ch=False, rn=True, n='{}'.format(name))[0]
    cmds.delete(cuR,cuL)
    cmds.rebuildSurface(lofted, rt=0, kc=0, fr=0, ch=1, end=1, sv=0, su=0, kr=0, dir=2, kcp=0, tol=0.01, dv=0, du=0, rpo=1)
    return lofted, cuC

def get_loft_axis(start=None, end=None):
    loft_axis = None
    start_loc = cmds.spaceLocator()[0]
    cmds.xform(start_loc, t=cmds.xform(start, q=1, t=1, ws=1), ws=1, a=1)
    end_loc = cmds.spaceLocator()[0]
    cmds.xform(start_loc, t=cmds.xform(end, q=1, t=1, ws=1), ws=1, a=1)
    cmds.parent(end_loc, start_loc)
    end_loc_wt = cmds.xform(end_loc, q=1, t=1, os=1)
    if abs(end_loc_wt[1]) > abs(end_loc_wt[0]) or abs(end_loc_wt[2]) > abs(end_loc_wt[0]):
        loft_axis = 'x'
    elif abs(end_loc_wt[0]) > abs(end_loc_wt[1]) or abs(end_loc_wt[2]) > abs(end_loc_wt[1]):
        loft_axis = 'y'
    elif abs(end_loc_wt[0]) > abs(end_loc_wt[2]) or abs(end_loc_wt[1]) > abs(end_loc_wt[2]):
        loft_axis = 'z'
    cmds.delete(start_loc)

    return loft_axis

def create_follicles(mesh=None, points=None):
    fols_renames = OrderedDict()
    for obj in points:
        if 'joint' == cmds.objectType(obj):
            fol_shape = obj
        else:
            fol_shape = cmds.listRelatives(obj, s=1)[0] or None

        if not 'follicle' == cmds.objectType(fol_shape):
            fol_shape = cmds.createNode('follicle', ss=1)
            fol = cmds.listRelatives(fol_shape, p=1)[0]
            cmds.matchTransform(fol, obj, pos=1, rot=1)

        if 'follicle' == cmds.objectType(fol_shape):
            fol = cmds.listRelatives(fol_shape, p=1)[0]
            closest_shape = cmds.listRelatives(mesh, s=1)[0] or None
            if 'mesh' == cmds.objectType(closest_shape):
                cpt = cmds.createNode('closestPointOnMesh', ss=1)
                cmds.connectAttr(closest_shape+'.outMesh', cpt+'.inMesh', f=1)
                cmds.connectAttr(closest_shape+'.outMesh', fol_shape+'.inputMesh', f=1)
                cmds.connectAttr(closest_shape+'.worldMatrix[0]', fol_shape+'.inputWorldMatrix', f=1)

            elif 'nurbsSurface' == cmds.objectType(closest_shape):
                cpt = cmds.createNode('closestPointOnSurface', ss=1)
                cmds.connectAttr(closest_shape+'.worldSpace[0]', cpt+'.inputSurface', f=1)
                cmds.connectAttr(closest_shape+'.worldSpace[0]', fol_shape+'.inputSurface', f=1)

            dcmx = cmds.createNode('decomposeMatrix', ss=1)
            cmds.connectAttr(fol+'.worldMatrix[0]', dcmx+'.inputMatrix', f=1)
            cmds.connectAttr(dcmx+'.outputTranslate', cpt+'.inPosition', f=1)

            cmds.setAttr(fol_shape+'.parameterU', cmds.getAttr(cpt+'.parameterU'))
            cmds.setAttr(fol_shape+'.parameterV', cmds.getAttr(cpt+'.parameterV'))

            cmds.connectAttr(fol_shape+'.outTranslate', fol+'.translate', f=1)
            cmds.connectAttr(fol_shape+'.outRotate', fol+'.rotate', f=1)

            cmds.delete(cpt, dcmx)

        fols_renames[fol] = obj+'_fol'

    [cmds.rename(fol_k, fol_v) for fol_k, fol_v in fols_renames.items()]
    fols = [f for f in fols_renames.values()]

    return fols

def rename(obj=None, prefix=None, suffix=None, replace=None):
    """
    obj=None, prefix=None, suffix=None, replace=None
    """
    # replace
    replace_name = obj
    if replace:
        replace_name = obj.replace(*replace)

    # prefix
    if not prefix:
        prefix = ''
    prefix_name = re.sub("^", prefix, replace_name)

    # suffix
    if not suffix:
        suffix = ''
    renamed = re.sub("$", suffix, prefix_name)

    return renamed

def duplicate_spl_joints(joints=None, prefix='spl_', suffix=None, replace=None):
    joints = cmds.ls(joints, type='joint')
    spls = []
    for jnt in joints:
        new_name = prefix+jnt
        spls.append(new_name)
        dup = cmds.duplicate(jnt, po=True, n=new_name)
        pa = cmds.listRelatives(jnt, p=True) or None
        if pa:
            parent_name = prefix+pa[0]
            if cmds.objExists(parent_name):
                try:
                    cmds.parent(new_name, w=True)
                except:
                    print(traceback.format_exc())

    tkgMJ.merge_joints(spls)

    return spls

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point
