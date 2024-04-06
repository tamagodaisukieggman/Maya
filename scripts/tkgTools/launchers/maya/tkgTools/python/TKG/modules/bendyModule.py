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

        self.create_module_parts('BENDY')

        if sel:
            cmds.select(sel, r=True)

    def create_bendy_limb(self, nodes=None):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []

        num_reg = tkgRegulation.NumRegulation()

        bendy_joints, bendy_segments_list = tkgRigJoints.create_bendy_joints(nodes, num_reg.bendy_limb_num)

        bendy_main_offset, bendy_main_ctrls = tkgCtrls.create_bendy_ctrls(nodes=bendy_joints, axis=[0,0,0], scale=1)

        for bendy_segments in bendy_segments_list:
            bendys_offset, bendys_ctrls = tkgCtrls.create_bendy_ctrls(nodes=bendy_segments, axis=[0,0,0], scale=1)

        cmds.parent(bendy_joints[0], self.nodes_top)
        cmds.parent(bendy_main_offset, self.ctrls_top)
