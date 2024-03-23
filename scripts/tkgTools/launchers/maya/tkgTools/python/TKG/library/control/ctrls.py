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

def create_ctrl(name='default', shape='', axis=[0,0,0], scale=1):
    draw_util.create_curve(name, shape, axis, scale)
    draw_util.joint_shape()
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
    for n in nodes:
        ctrl, offset = create_fk_ctrl(n, axis, scale)

        if pa_ctrl:
            cmds.parent(offset, pa_ctrl)

        pa_ctrl = ctrl

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
