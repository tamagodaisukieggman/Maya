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

        self.create_module_parts('RIBBON')

        if sel:
            cmds.select(sel, r=True)

    def create_ribbon(self, nodes=None, num=None, base_include=True, tip_include=True):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []

        num_reg = tkgRegulation.NumRegulation()
        if num:
            num_reg.ribbon_num = num

        ribbon_joints, ribbon_segments_list = tkgRigJoints.create_ribbon_joints(nodes,
                                                                                num_reg.ribbon_num,
                                                                                base_include,
                                                                                tip_include)

        # 中間のジョイントを削除する
        delete_segs = {}
        ribbon_segments_list_len = len(ribbon_segments_list)
        for i, ribbon_segments in enumerate(ribbon_segments_list):
            if i < ribbon_segments_list_len - 1:
                del_seg = ribbon_segments[-1]
                delete_segs[i] = del_seg

        for j, _del_seg in delete_segs.items():
            ribbon_segments = ribbon_segments_list[j]
            ribbon_segments.remove(_del_seg)
            cmds.delete(_del_seg)

        bendy_main_offset, bendy_main_ctrls = tkgCtrls.create_bendy_limb_ctrls(nodes=ribbon_joints, axis=[0,0,0], scale=1, type='main')

        for bendy_segments in ribbon_segments_list:
            bendys_offset, bendys_ctrls = tkgCtrls.create_bendy_limb_ctrls(nodes=bendy_segments, axis=[0,0,0], scale=1, type='bendy')

        cmds.parent(ribbon_joints[0], self.nodes_top)
        cmds.parent(bendy_main_offset, self.ctrls_top)

        # skin surfaceの作成
        base_skin_surface = tkgNodes.create_loft_from_curves(nodes=nodes, offset=[5,0,0])

        for ribbon_segments in ribbon_segments_list:
            for node in ribbon_segments:
                tkgNodes.closest_follicle_on_surface(node, base_skin_surface)