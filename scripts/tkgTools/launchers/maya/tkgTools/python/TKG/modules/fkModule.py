# -*- coding: utf-8 -*-
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

        self.fk_nodes_top = 'FK_NODES_{}'.format(self.module_parent)
        self.fk_ctrls_top = 'FK_CTLS_{}'.format(self.module_parent)

        self.module_tops = [self.fk_nodes_top, self.fk_ctrls_top]
        for n in self.module_tops:
            if not cmds.objExists(n):
                cmds.createNode('transform', n=n, ss=True)
            parent = cmds.listRelatives(n, p=True) or None
            if not parent:
                cmds.parent(n, self.module_parent)
            elif not self.module_parent in parent:
                cmds.parent(n, self.module_parent)

        if sel:
            cmds.select(sel, r=True)

    def create_fk_limb(self, nodes=None):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []
        fk_joints = tkgRigJoints.create_fk_joints(nodes=nodes)

        fk_offset, fk_ctrls = tkgCtrls.create_fk_ctrls(nodes=fk_joints, axis=[0,0,0], scale=1)

        cmds.parent(fk_joints[0], self.fk_nodes_top)
        cmds.parent(fk_offset, self.fk_ctrls_top)
