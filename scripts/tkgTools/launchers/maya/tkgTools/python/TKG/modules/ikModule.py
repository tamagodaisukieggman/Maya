# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import TKG.library.rigJoints as tkgRigJoints
import TKG.library.ik as tkgIk
import TKG.library.control.ctrls as tkgCtrls
reload(tkgRigJoints)
reload(tkgIk)
reload(tkgCtrls)

def create_ik_limb_module(nodes=None):
    if not nodes:
        nodes = cmds.ls(os=True, fl=True) or []
    ik_joints = tkgRigJoints.create_ik_joints(nodes=nodes)

    ikh = tkgIk.create_RP_ikHandle(ik_joints[0], ik_joints[-1])

    ikBase_ctrl, ikBase_offset = tkgCtrls.create_ikBase_ctrl(node=nodes[0], axis=[0,0,0], scale=1)

    ikMain_ctrl, ikMain_offset = tkgCtrls.create_ikMain_ctrl(node=nodes[-1], axis=[0,0,0], scale=1)
