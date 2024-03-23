# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import TKG.library.rigJoints as tkgRigJoints
import TKG.library.ik as tkgIk
import TKG.library.control.ctrls as tkgCtrls
import TKG.modules.baseModule as tkgModules
reload(tkgRigJoints)
reload(tkgIk)
reload(tkgCtrls)
reload(tkgModules)

class Build(tkgModules.Module):
    def __init__(self, module=None, side=None):
        super().__init__(module, side)
        # self.module = module
        # self.side = side

    def create_ik_limb_module(self, nodes=None, pv_idx=1):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []
        ik_joints = tkgRigJoints.create_ik_joints(nodes=nodes)

        ikh = tkgIk.create_RP_ikHandle(ik_joints[0], ik_joints[-1])

        ikBase_ctrl, ikBase_offset = tkgCtrls.create_ikBase_ctrl(node=ik_joints[0], axis=[0,0,0], scale=1)

        ikMain_ctrl, ikMain_offset = tkgCtrls.create_ikMain_ctrl(node=ik_joints[-1], axis=[0,0,0], scale=1)

        ikPv_ctrl, ikPv_offset = tkgCtrls.create_ikPv_ctrl(node=ik_joints[pv_idx], axis=[0,0,0], scale=1)
