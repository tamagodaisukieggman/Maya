# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import TKG.common as tkgCommon
import TKG.nodes as tkgNodes
import TKG.regulation as tkgRegulation
import TKG.library.control.draw as tkgDraw
reload(tkgCommon)
reload(tkgNodes)
reload(tkgRegulation)
reload(tkgDraw)

draw_util = tkgDraw.Draw()

def create_controller_node(ctrl=None):
    ctrler_sets = tkgRegulation.absolute_name('controller_node_sets')
    if not cmds.objExists(ctrler_sets):
        cmds.sets(em=True, n=ctrler_sets)
    if not cmds.objExists(ctrler_sets+'.ctrlMouseVisibility'):
        cmds.addAttr(ctrler_sets, ln='ctrlMouseVisibility', sn='cmv', at='bool', k=True)

    ctrler_sets_cdn = tkgRegulation.ctrl_type_rename(ctrler_sets, 'condition')
    if not cmds.objExists(ctrler_sets_cdn):
        cmds.createNode('condition', n=ctrler_sets_cdn, ss=True)

        cmds.setAttr(ctrler_sets_cdn+'.secondTerm', 1)
        cmds.setAttr(ctrler_sets_cdn+'.colorIfTrueR', 2)
        cmds.setAttr(ctrler_sets_cdn+'.colorIfFalseR', 0)

        cmds.connectAttr(ctrler_sets+'.ctrlMouseVisibility', ctrler_sets_cdn+'.firstTerm', f=True)

    ctrler = tkgRegulation.ctrl_type_rename(ctrl, 'controller')
    if not cmds.objExists(ctrler):
        cmds.createNode('controller', n=ctrler, ss=True)
        cmds.sets(ctrler, add=ctrler_sets)

        cmds.connectAttr(ctrler_sets_cdn+'.outColorR', ctrler+'.visibilityMode', f=True)
        cmds.connectAttr(ctrl+'.message', ctrler+'.controllerObject', f=True)

def create_ctrl(name='default', shape='', axis=[0,0,0], scale=1):
    draw_util.create_curve(name, shape, axis, scale)
    draw_util.joint_shape()

    create_controller_node(draw_util.curve)

    return draw_util.curve

# FK ctrl
def create_fk_ctrl(node=None, axis=[0,0,0], scale=1):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    shape = tkgRegulation.shape_type('fk')
    name = tkgRegulation.ctrl_type_rename(node)
    ctrl = create_ctrl(name, shape, axis, scale)
    offset = tkgNodes.offsets(ctrl, ['Global', 'Local'])
    cmds.matchTransform(offset, node)
    return ctrl, offset

def create_fk_ctrls(nodes=None, axis=[0,0,0], scale=1):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []
    pa_ctrl = None
    pa_offset = None
    ctrls = []
    for i, n in enumerate(nodes):
        ctrl, offset = create_fk_ctrl(n, axis, scale)
        ctrls.append(ctrl)

        if pa_ctrl:
            cmds.parent(offset, pa_ctrl)

        pa_ctrl = ctrl

        if i == 0:
            pa_offset = offset
    return pa_offset, ctrls

# IK ctrl
def create_ikBase_ctrl(node=None, axis=[0,0,0], scale=1):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    shape = tkgRegulation.shape_type('ikBase')
    name = tkgRegulation.ctrl_type_rename(node)
    ctrl = create_ctrl(name, shape, axis, scale)
    offset = tkgNodes.offsets(ctrl, ['Global', 'Local'])
    cmds.matchTransform(offset, node)
    return ctrl, offset

def create_ikMain_ctrl(node=None, axis=[0,0,0], scale=1):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    shape = tkgRegulation.shape_type('ikMain')
    name = tkgRegulation.ctrl_type_rename(node)
    ctrl = create_ctrl(name, shape, axis, scale)
    offset = tkgNodes.offsets(ctrl, ['Global', 'Local'])
    cmds.matchTransform(offset, node, pos=True, rot=False)
    return ctrl, offset

def create_ikPv_ctrl(node=None, axis=[0,0,0], scale=1):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    shape = tkgRegulation.shape_type('ikPv')
    name = tkgRegulation.ctrl_type_rename(node)
    ctrl = create_ctrl(name, shape, axis, scale)
    offset = tkgNodes.offsets(ctrl, ['Global', 'Local'])
    cmds.matchTransform(offset, node, pos=True, rot=False)
    return ctrl, offset

def create_ikAutoRot_ctrl(node=None, axis=[0,0,0], scale=1):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    shape = tkgRegulation.shape_type('fk')
    name = tkgRegulation.ctrl_type_rename(node, 'Local')
    ctrl = create_ctrl(name, shape, axis, scale)
    offset = tkgNodes.offsets(ctrl, ['Global', 'Auto'])
    cmds.matchTransform(offset, node)
    return ctrl, offset

def create_scIkPv_ctrl(node=None, axis=[0,0,0], scale=1):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    shape = tkgRegulation.shape_type('scIkPv')
    name = tkgRegulation.ctrl_type_rename(node, 'Local')
    ctrl = create_ctrl(name, shape, axis, scale)
    offset = tkgNodes.offsets(ctrl, ['Global', 'Auto'])
    cmds.matchTransform(offset, node)
    return ctrl, offset

# bendy limb ctrl
def create_bendy_limb_ctrl(node=None, axis=[0,0,0], scale=1, type='bendy'):
    if not node:
        node = cmds.ls(os=True, fl=True)[0] or []
    if type == 'bendy':
        shape = tkgRegulation.shape_type('bendy_limb')
    elif type == 'main':
        shape = tkgRegulation.shape_type('bendy_limb_main')
    name = tkgRegulation.ctrl_type_rename(node)
    ctrl = create_ctrl(name, shape, axis, scale)
    offset = tkgNodes.offsets(ctrl, ['Global', 'Local'])
    cmds.matchTransform(offset, node)

    virtual_parent_ctrl = None
    parent = cmds.listRelatives(node, p=True) or None
    if parent:
        virtual_parent_ctrl = tkgRegulation.ctrl_type_rename(parent[0])

    if virtual_parent_ctrl:
        if cmds.objExists(virtual_parent_ctrl):
            cmds.parent(offset, virtual_parent_ctrl)

    return ctrl, offset

def create_bendy_limb_ctrls(nodes=None, axis=[0,0,0], scale=1, type='bendy'):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []

    pa_offset = None
    ctrls = []
    offsets = []
    for i, n in enumerate(nodes):
        ctrl, offset = create_bendy_limb_ctrl(n, axis, scale, type)
        ctrls.append(ctrl)
        offsets.append(offset)

        if i == 0:
            pa_offset = offset

    return pa_offset, ctrls, offsets

