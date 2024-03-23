# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import TKG.library.rigJoints as tkgRigJoints
import TKG.nodes as tkgNodes
import TKG.library.ik as tkgIk
import TKG.library.control.ctrls as tkgCtrls
import TKG.modules.baseModule as tkgModules
reload(tkgRigJoints)
reload(tkgNodes)
reload(tkgIk)
reload(tkgCtrls)
reload(tkgModules)

class Build(tkgModules.Module):
    def __init__(self, side=None, module=None):
        sel = cmds.ls(os=True, fl=True) or []

        super().__init__(side, module)

        self.ik_nodes_top = 'IK_NODES_{}'.format(self.module_parent)
        self.ik_ctrls_top = 'IK_CTLS_{}'.format(self.module_parent)

        self.module_tops = [self.ik_nodes_top, self.ik_ctrls_top]
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

    def create_ik_limb(self, nodes=None, pv_idx=1, pv_move=20):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []
        ik_joints = tkgRigJoints.create_ik_joints(nodes=nodes)

        ikh = tkgIk.create_RP_ikHandle(ik_joints[0], ik_joints[-1])

        ikBase_ctrl, ikBase_offset = tkgCtrls.create_ikBase_ctrl(node=ik_joints[0], axis=[0,0,0], scale=1)

        ikMain_ctrl, ikMain_offset = tkgCtrls.create_ikMain_ctrl(node=ik_joints[-1], axis=[0,0,0], scale=1)

        ikAutoRot_ctrl, ikAutoRot_offset = tkgCtrls.create_ikAutoRot_ctrl(node=ik_joints[-1], axis=[0,0,0], scale=1)

        ikPv_ctrl, ikPv_offset = tkgCtrls.create_ikPv_ctrl(node=ik_joints[pv_idx], axis=[0,0,0], scale=1)
        tkgNodes.pole_vec(start=ik_joints[0], mid=ik_joints[pv_idx], end=ik_joints[-1], move=pv_move, obj=ikPv_offset)
        cmds.xform(ikPv_offset, ro=[0,0,0], ws=True, a=True)

        cmds.parent(ik_joints[0], self.ik_nodes_top)
        cmds.parent(ikh, self.ik_nodes_top)

        cmds.parent(ikBase_offset, self.ik_ctrls_top)
        cmds.parent(ikMain_offset, ikBase_ctrl)
        cmds.parent(ikPv_offset, ikBase_ctrl)
        cmds.parent(ikAutoRot_offset, ikMain_ctrl)

        # -------------------
        # connection
        po_con = cmds.pointConstraint(ikMain_ctrl, ikh, w=True)[0]
        cmds.poleVectorConstraint(ikPv_ctrl, ikh, w=True)
        ori_con = cmds.orientConstraint(ikAutoRot_ctrl, ik_joints[-1], w=True, mo=True)[0]
        cmds.setAttr(ori_con+'.interpType', 2)

        # -------------------
        # ikAutoRot connection
        autoRot = cmds.listRelatives(ikAutoRot_ctrl, p=True)[0]
        autoRot_ori_con = cmds.orientConstraint(ik_joints[pv_idx], autoRot, w=True, mo=True)[0]
        cmds.setAttr(autoRot_ori_con+'.interpType', 2)
        cmds.disconnectAttr(autoRot_ori_con+'.constraintRotateX', autoRot+'.rx')
        cmds.disconnectAttr(autoRot_ori_con+'.constraintRotateY', autoRot+'.ry')
        cmds.disconnectAttr(autoRot_ori_con+'.constraintRotateZ', autoRot+'.rz')

        # local pairBlend
        pbn = cmds.createNode('pairBlend', n=autoRot+'_PBN', ss=True)
        cmds.setAttr(pbn+'.rotInterpolation', 1)

        cmds.connectAttr(autoRot_ori_con+'.constraintRotate', pbn+'.inRotate2', f=True)
        cmds.connectAttr(pbn+'.outRotate', autoRot+'.r', f=True)

        # local pairBlend addAttr
        cmds.addAttr(ikAutoRot_ctrl, ln='autoPose', sn='ap', at='double', dv=0, max=1, min=0, k=True)
        cmds.connectAttr(ikAutoRot_ctrl+'.ap', pbn+'.weight', f=True)

        # --------------------
        # stretchy
        tkgIk.stretchy(main_ctrl=ikMain_ctrl, ikHandle=ikh, stretchy_axis='x', default_reverse=False)

        # --------------------
        # softik
        cmds.delete(po_con)
        softik_st_loc = tkgIk.create_softik(ik_ctrl=ikMain_ctrl, ikHandle=ikh)
        cmds.parent(softik_st_loc, self.ik_nodes_top)

        # --------------------
        # pv aim

        return ik_joints