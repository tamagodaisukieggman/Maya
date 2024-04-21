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

        bendy_main_offset, bendy_main_ctrls, bendy_main_offsets = tkgCtrls.create_bendy_limb_ctrls(nodes=ribbon_joints, axis=[0,0,0], scale=1, type='main')

        ribbons_offset_list = []
        ribbons_ctrls_list = []
        for ribbon_segments in ribbon_segments_list:
            ribbons_offset, ribbons_ctrls, ribbon_offsets = tkgCtrls.create_bendy_limb_ctrls(nodes=ribbon_segments, axis=[0,0,0], scale=1, type='bendy')

            ribbons_offset_list.append(ribbon_offsets)
            ribbons_ctrls_list.append(ribbons_ctrls)

        cmds.parent(ribbon_joints[0], self.nodes_top)
        cmds.parent(bendy_main_offset, self.ctrls_top)

        # skin surfaceの作成
        first_skin_surface = tkgNodes.create_loft_from_curves(nodes=nodes, offset=[5,0,0])

        base_ribbon_jnt = ribbon_segments_list[0][0]
        tip_ribbon_jnt = ribbon_segments_list[-1][-1]

        first_skin_surface_sc = cmds.skinCluster([base_ribbon_jnt, tip_ribbon_jnt],
                                    first_skin_surface,
                                    n='{}_skinCluster'.format(first_skin_surface),
                                    tsb=True)[0]
        crv_bind=cmds.listConnections('{}.bindPose'.format(first_skin_surface_sc),c=0,d=1,p=0)
        if crv_bind:cmds.delete(crv_bind)

        cmds.parent(first_skin_surface, self.nodes_top)

        # follicleのnullをoffsetの親にする
        flat_ribbons_offset_list = []
        for ribbon_offsets in ribbons_offset_list:
            for ribbon_offset in ribbon_offsets:
                flat_ribbons_offset_list.append(ribbon_offset)

        k = 0
        for ribbon_segments in ribbon_segments_list:
            for node in ribbon_segments:
                fol = tkgNodes.closest_follicle_on_surface(node, first_skin_surface)
                fol_nul = cmds.createNode('transform', n='OFF_'+fol, ss=True)
                cmds.matchTransform(fol_nul, fol)

                ribbons_offset_pa = cmds.listRelatives(flat_ribbons_offset_list[k], p=True) or None
                if ribbons_offset_pa:
                    ribbons_offset_pa = ribbons_offset_pa[0]
                    cmds.parent(fol_nul, ribbons_offset_pa)
                    cmds.parent(flat_ribbons_offset_list[k], fol_nul)

                if not node == base_ribbon_jnt and not node == tip_ribbon_jnt:
                    # cmds.parentConstraint(fol, fol_nul, w=True)
                    tkgNodes.matrix_constraint(src=fol, dst=fol_nul)

                cmds.parent(fol, self.nodes_top)

                k += 1