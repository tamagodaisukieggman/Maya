# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import TKG.library.rigJoints as tkgRigJoints
import TKG.nodes as tkgNodes
import TKG.library.fk as tkgFk
import TKG.library.control.ctrls as tkgCtrls
import TKG.modules.baseModule as tkgModules
import TKG.regulation as tkgRegulation
reload(tkgRigJoints)
reload(tkgNodes)
reload(tkgFk)
reload(tkgCtrls)
reload(tkgModules)
reload(tkgRegulation)

class Build(tkgModules.Module):
    def __init__(self, side=None, module=None):
        sel = cmds.ls(os=True, fl=True) or []

        super().__init__(side, module)

        self.create_module_parts('BLEND')

        if sel:
            cmds.select(sel, r=True)

    def create_blend_limb(self, nodes=None):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []

        blend_limb_joints = tkgRigJoints.create_blend_joints(nodes)

        cmds.parent(blend_limb_joints[0], self.nodes_top)
