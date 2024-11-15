﻿# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import TKG.library.rigJoints as tkgRigJoints
import TKG.nodes as tkgNodes
import TKG.library.fk as tkgFk
import TKG.library.control.ctrls as tkgCtrls
import TKG.modules.baseModule as tkgModules
reload(tkgRigJoints)
reload(tkgNodes)
reload(tkgFk)
reload(tkgCtrls)
reload(tkgModules)

class Build(tkgModules.Module):
    def __init__(self, side=None, module=None):
        sel = cmds.ls(os=True, fl=True) or []

        super().__init__(side, module)

        self.create_module_parts('FK')

        if sel:
            cmds.select(sel, r=True)

    def create_fk_limb(self, nodes=None):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []
        fk_joints = tkgRigJoints.create_fk_joints(nodes=nodes)

        fk_offset, fk_ctrls = tkgCtrls.create_fk_ctrls(nodes=fk_joints, axis=[0,0,0], scale=1)

        cmds.parent(fk_joints[0], self.nodes_top)
        cmds.parent(fk_offset, self.ctrls_top)

        # -------------------
        # connection
        
        return fk_joints