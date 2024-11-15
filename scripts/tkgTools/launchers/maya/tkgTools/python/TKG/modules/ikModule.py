﻿# -*- coding: utf-8 -*-
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

        self.create_module_parts('IK')

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

        # ik pv
        ikPv_ctrl, ikPv_offset = tkgCtrls.create_ikPv_ctrl(node=ik_joints[pv_idx], axis=[0,0,0], scale=1)
        tkgNodes.pole_vec(start=ik_joints[0], mid=ik_joints[pv_idx], end=ik_joints[-1], move=pv_move, obj=ikPv_offset)
        cmds.xform(ikPv_offset, ro=[0,0,0], ws=True, a=True)

        # stable ik pv
        sc_ik_joints, sc_pv_node, sc_ikh = tkgIk.create_stable_ik_pv(nodes=nodes, aim_axis='x', up_axis='y', freeze=True)
        scIkPv_ctrl, scIkPv_offset = tkgCtrls.create_scIkPv_ctrl(node=sc_pv_node, axis=[0,0,0], scale=2)
        cmds.parent(sc_ikh, ikBase_ctrl)
        cmds.parent(scIkPv_offset, sc_pv_node)
        cmds.parent(ikPv_offset, scIkPv_ctrl)

        # 
        cmds.parent(ik_joints[0], self.nodes_top)
        cmds.parent(sc_ik_joints[0], self.nodes_top)
        cmds.parent(ikh, self.nodes_top)

        cmds.parent(ikBase_offset, self.ctrls_top)
        cmds.parent(ikMain_offset, ikBase_ctrl)
        # cmds.parent(ikPv_offset, ikBase_ctrl)
        cmds.parent(ikAutoRot_offset, ikMain_ctrl)

        # -------------------
        # connection
        po_con = cmds.pointConstraint(ikMain_ctrl, ikh, w=True)[0]
        cmds.poleVectorConstraint(ikPv_ctrl, ikh, w=True)
        ori_con = cmds.orientConstraint(ikAutoRot_ctrl, ik_joints[-1], w=True, mo=True)[0]
        cmds.setAttr(ori_con+'.interpType', 2)

        cmds.pointConstraint(ikMain_ctrl, sc_ikh, w=True)[0]

        cmds.pointConstraint(ikBase_ctrl, ik_joints[0], w=True)[0]
        cmds.pointConstraint(ikBase_ctrl, sc_ik_joints[0], w=True)[0]

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
        # stretchy and softik
        stretch_and_soft = tkgIk.StretchSoftIK(main_ctrl=ikMain_ctrl, ikhandle=ikh, start=ik_joints[0], end=ik_joints[-1], axis='x')
        stretch_and_soft.stretch_base()
        stretch_and_soft.stretch_connection()

        stretch_and_soft.softik_base(max_value=10)
        stretch_and_soft.softik_connection(ikh_con=po_con)

        cmds.parent(stretch_and_soft.start_stretch_parent, ikBase_ctrl)

        cmds.parent(stretch_and_soft.crv, self.nodes_top)
        cmds.parent(stretch_and_soft.softik_aim_loc, self.nodes_top)

        # --------------------
        # softik
        # cmds.delete(po_con)
        # softik_st_loc = tkgIk.create_softik(ik_ctrl=ikMain_ctrl, ikHandle=ikh)
        # cmds.parent(softik_st_loc, self.nodes_top)

        # --------------------
        # pv aim

        return ik_joints

    def create_ik_spline(self, nodes=None, aim_axis='+y', up_axis='+z'):
        if not nodes:
            nodes = cmds.ls(os=True, fl=True) or []
        ik_joints = tkgRigJoints.create_ik_joints(nodes=nodes)

        ikh, ik_spline_crv = tkgIk.create_spline_ikHandle(ik_joints[0], ik_joints[-1])

        ikBase_ctrl, ikBase_offset = tkgCtrls.create_ikBase_ctrl(node=ik_joints[0], axis=[0,0,90], scale=1)

        ikMain_ctrl, ikMain_offset = tkgCtrls.create_ikMain_ctrl(node=ik_joints[-1], axis=[0,0,0], scale=1)

        cmds.parent(ik_joints[0], self.nodes_top)
        cmds.parent(ikh, self.nodes_top)
        cmds.parent(ik_spline_crv, self.nodes_top)
        cmds.parent(ikBase_offset, self.ctrls_top)
        cmds.parent(ikMain_offset, self.ctrls_top)

        # advanced twist
        dForward_axis = {
            '+x':0,
            '-x':1,
            '+y':2,
            '-y':3,
            '+z':4,
            '-z':5
        }

        dWorldUp_axis = {
            '+y':0,
            '-y':1,
            '*y':2,
            '+z':3,
            '-z':4,
            '*z':5,
            '+x':6,
            '-x':7,
            '*x':8
        }

        up_axis_vectors = {
            '+y':[0,1,0],
            '-y':[0,-1,0],
            '*y':[0,1,0],
            '+z':[0,0,1],
            '-z':[0,0,-1],
            '*z':[0,0,1],
            '+x':[1,0,0],
            '-x':[-1,0,0],
            '*x':[1,0,0]
        }

        cmds.setAttr('{}.dTwistControlEnable'.format(ikh), 1)
        cmds.setAttr('{}.dWorldUpType'.format(ikh), 4)
        cmds.setAttr('{}.dForwardAxis'.format(ikh), dForward_axis[aim_axis])
        cmds.setAttr('{}.dWorldUpAxis'.format(ikh), dWorldUp_axis[up_axis])
        cmds.setAttr('{}.dWorldUpVector'.format(ikh), *up_axis_vectors[up_axis])
        cmds.setAttr('{}.dWorldUpVectorEnd'.format(ikh), *up_axis_vectors[up_axis])

        cmds.connectAttr('{}.worldMatrix[0]'.format(ikBase_ctrl), '{}.dWorldUpMatrix'.format(ikh))
        cmds.connectAttr('{}.worldMatrix[0]'.format(ikMain_ctrl), '{}.dWorldUpMatrixEnd'.format(ikh))

        # skin bind
        # ik_spline_skin_joints = tkgRigJoints.create_start_end_joints(ik_joints)
        skin_ik_spline_sc = cmds.skinCluster([ikBase_ctrl, ikMain_ctrl],
                                    ik_spline_crv,
                                    n='{}_skinCluster'.format(ik_spline_crv),
                                    tsb=True)[0]
        crv_bind=cmds.listConnections('{}.bindPose'.format(skin_ik_spline_sc),c=0,d=1,p=0)
        if crv_bind:cmds.delete(crv_bind)

        # --------------------
        # stretchy and softik
        stretch_and_soft = tkgIk.StretchSoftIK(main_ctrl=ikMain_ctrl,
                                               ikhandle=ikh,
                                               start=ik_joints[0],
                                               end=ik_joints[-1],
                                               axis='y')
        stretch_and_soft.stretch_base()
        stretch_and_soft.stretch_connection()
