# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.libs.attribute as tkgAttr
import tkgRigBuild.libs.common as tkgCommon
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.build.ik as tkgIk
import tkgRigBuild.build.fk as tkgFk
reload(tkgModule)
reload(tkgAttr)
reload(tkgChain)
reload(tkgIk)
reload(tkgCommon)
reload(tkgFk)


class IkChain(tkgModule.RigModule, tkgIk.Ik):
    """
# -*- coding: utf-8 -*-
# solvers = ['ikRPsolver', 'ikSCsolver', 'ikSplineSolver', 'ikSpringSolver']
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.parts.ikChain as tkgIkChain
import tkgRigBuild.post.finalize as tkgFinalize
reload(tkgIkChain)
reload(tkgFinalize)

import traceback

sel = cmds.ls(os=True, dag=True) # select 3 joints(start, middle, end)

try:
    tkgIkChain.IkChain(
                    side='A',
                     part=None,
                     guide_list=sel,
                     ctrl_scale=3,
                     ctrl_color=[0.8, 0.5, 0.2],
                     sticky=None,
                     solver='ikSplineSolver',
                     pv_guide='auto',
                     offset_pv=0,
                     slide_pv=None,
                     stretchy=True,
                     stretchy_axis='scaleX',
                     soft_ik=False,
                     twisty=True,
                     twisty_axis='x',
                     bendy=True,
                     segments=1,
                     model_path=None,
                     guide_path=None)
except:
    print(traceback.format_exc())

# tkgFinalize.add_color_attributes()
"""
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=1,
                 ctrl_color=[0.8, 0.5, 0.2],
                 sticky=None,
                 solver=None,
                 pv_guide='auto',
                 offset_pv=0,
                 slide_pv=None,
                 stretchy=True,
                 stretchy_axis='scaleX',
                 soft_ik=None,
                 twisty=None,
                 twisty_axis='x',
                 bendy=None,
                 bendy_axis='scaleY',
                 segments=None,
                 dForwardAxis='x',
                 dWorldUpAxis='z',
                 model_path=None,
                 guide_path=None):
        super(IkChain, self).__init__(side=side, part=part,
                                      guide_list=guide_list,
                                      ctrl_scale=ctrl_scale,
                                      model_path=model_path,
                                      guide_path=guide_path)

        self.sticky = sticky
        self.solver = solver
        self.pv_guide = pv_guide
        self.offset_pv = offset_pv
        self.ctrl_color = ctrl_color
        self.slide_pv = slide_pv
        self.stretchy = stretchy
        self.stretchy_axis = stretchy_axis
        self.twisty = twisty
        self.twisty_axis = twisty_axis
        self.bendy = bendy
        self.bendy_axis = bendy_axis
        self.segments = segments

        self.dForwardAxis = dForwardAxis
        self.dWorldUpAxis = dWorldUpAxis

        self.soft_ik = soft_ik

        if self.twisty or self.bendy and not self.segments:
            self.segments = 4

        self.part_ik_ctrls = []

        self.create_module()

    def create_module(self):
        super(IkChain, self).create_module()

        self.check_solvers()
        self.check_pv_guide()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        # self.add_plugs()

        if self.pv_guide:
            cmds.parent(self.gde_grp, self.control_grp)

    def control_rig(self):
        self.build_ik_controls()
        cmds.parent(self.ik_ctrl_grp, self.control_grp)

    def output_rig(self):
        self.build_ik_chain()
        self.src_joints = self.ik_joints

        if self.segments:
            self.ik_chain.split_chain(segments=self.segments)
            self.src_joints = []
            for ik_jnt in self.ik_joints[:-1]:
                split_list = self.ik_chain.split_jnt_dict[ik_jnt]
                for s_jnt in split_list:
                    self.src_joints.append(s_jnt)
            self.src_joints.append(self.ik_joints[-1])

        if self.twisty:
            self.ik_chain.twist_chain(start_translate=self.ik_chain.joints[1],
                                      start_rotate=self.ik_chain.joints[0],
                                      end_translate=self.ik_chain.joints[0],
                                      end_rotate=self.ik_chain.joints[0],
                                      twist_bone=self.ik_chain.joints[0],
                                      twist_driver=self.base_ctrl.ctrl,
                                      twist_axis=self.twisty_axis,
                                      reverse=True)
            self.ik_chain.twist_chain(start_translate=self.ik_chain.joints[2],
                                      start_rotate=self.ik_chain.joints[1],
                                      end_translate=self.ik_chain.joints[2],
                                      end_rotate=self.ik_chain.joints[1],
                                      twist_bone=self.ik_chain.joints[1],
                                      twist_driver=self.main_ctrl.ctrl,
                                      twist_axis=self.twisty_axis)

        if self.bendy:
            for ikj in self.ik_chain.joints[:-1:]:
                bend = self.ik_chain.bend_chain(bone=ikj,
                                               ctrl_scale=self.ctrl_scale,
                                               global_scale=self.global_scale.attr,
                                               scale_axis=self.bendy_axis)
                cmds.parent(bend['control'], self.control_grp)
                cmds.parent(bend['module'], self.module_grp)

        self.build_ikh(scale_attr=self.global_scale)
        if self.solver in ['ikSplineSolver']:
            cmds.parent(self.ik_spline_crv, self.module_grp)
            self.ik_spline_joints = tkgCommon.duplicate_spl_joints(joints=self.guide_list,
                                           prefix='ik_spline_',
                                           suffix=None,
                                           replace=None)

            dTwist_up_axis = {
                'x':[200000,0,0],
                'y':[0,200000,0],
                'z':[0,0,200000],
                '-x':[-200000,0,0],
                '-y':[0,-200000,0],
                '-z':[0,0,-200000],
                '-x-':[200000,0,0],
                '-y-':[0,200000,0],
                '-z-':[0,0,200000],
            }

            dForward_axis = {
                'x':0,
                'y':2,
                'z':4,
                '-x':1,
                '-y':3,
                '-z':5,
            }

            dWorldUp_axis = {
                'x':6,
                'y':0,
                'z':3,
                '-x':7,
                '-y':1,
                '-z':4,
                '-x-':8,
                '-y-':2,
                '-z-':5
            }

            # For Base IK UP Joint
            self.ik_spline_base_up_joint = cmds.duplicate(self.ik_spline_joints[0],
                                                          n='up_'+self.ik_spline_joints[0])[0]
            cmds.move(*dTwist_up_axis[self.dWorldUpAxis], self.ik_spline_base_up_joint, r=True, os=True, wd=True)
            pa = cmds.listRelatives(self.ik_spline_base_up_joint, p=True) or None
            if pa: cmds.parent(self.ik_spline_base_up_joint, w=True)

            # For Main IK UP Joint
            self.ik_spline_tip_up_joint = cmds.duplicate(self.ik_spline_joints[-1],
                                                          n='up_'+self.ik_spline_joints[0])[0]
            cmds.move(*dTwist_up_axis[self.dWorldUpAxis], self.ik_spline_tip_up_joint, r=True, os=True, wd=True)
            pa = cmds.listRelatives(self.ik_spline_tip_up_joint, p=True) or None
            if pa: cmds.parent(self.ik_spline_tip_up_joint, w=True)

            # Get Loft
            loft_axis = tkgCommon.get_loft_axis(start=self.ik_spline_joints[0],
                                                end=self.ik_spline_joints[-1])

            self.ik_lofted, self.ik_curve = tkgCommon.create_loft(nodes=self.ik_spline_joints,
                                                                  name=self.ik_spline_joints[0]+'_loft_suf',
                                                                  axis=loft_axis)

            # ik_spline_mid_joints = tkgCommon.duplicate_spl_joints(joints=self.guide_list[:-1:],
            #                                prefix='ik_spline_mid_',
            #                                suffix=None,
            #                                replace=None)
            #
            # for isj, ismj in zip(ik_spline_joints[1::], ik_spline_mid_joints):
            #     pos1 = cmds.xform(isj, q=True, t=True, ws=True)
            #     pos2 = cmds.xform(ismj, q=True, t=True, ws=True)
            #     mid_point = tkgCommon.get_mid_point(pos1, pos2, percentage=0.5)
            #     cmds.xform(ismj, t=mid_point, ws=True, a=True)
            #
            # [ik_spline_joints.append(j) for j in ik_spline_mid_joints]

            cmds.setAttr('{0}.dTwistControlEnable'.format(self.ikh), 1)
            cmds.setAttr('{0}.dWorldUpType'.format(self.ikh), 2)
            cmds.setAttr('{0}.dForwardAxis'.format(self.ikh), dForward_axis[self.dForwardAxis])
            cmds.setAttr('{0}.dWorldUpAxis'.format(self.ikh), dWorldUp_axis[self.dWorldUpAxis])
            cmds.connectAttr('{0}.worldMatrix[0]'.format(self.ik_spline_base_up_joint), '{0}.dWorldUpMatrix'.format(self.ikh))
            cmds.connectAttr('{0}.worldMatrix[0]'.format(self.ik_spline_tip_up_joint), '{0}.dWorldUpMatrixEnd'.format(self.ikh))

            cmds.setAttr('{0}.ikFkManipulation'.format(self.ikh), 1)
            # cmds.setAttr('{0}.dTwistValueType'.format(self.ikh), 1)

            ik_spl_pma = cmds.createNode('plusMinusAverage', ss=True)
            ik_spl_pb = cmds.createNode('pairBlend', ss=True)
            cmds.setAttr(ik_spl_pma+'.operation', 2)
            cmds.setAttr(ik_spl_pb+'.weight', 0.5)
            cmds.connectAttr(self.base_ctrl.ctrl+'.r'+self.dForwardAxis.replace('-', ''), ik_spl_pma+'.input1D[0]', f=True)
            cmds.connectAttr(self.main_ctrl.ctrl+'.r'+self.dForwardAxis.replace('-', ''), ik_spl_pma+'.input1D[1]', f=True)
            cmds.connectAttr(ik_spl_pma+'.output1D', ik_spl_pb+'.inRotate'+self.dForwardAxis.replace('-', '').upper()+'2', f=True)
            cmds.connectAttr(ik_spl_pb+'.outRotate'+self.dForwardAxis.replace('-', '').upper(), self.ikh+'.twist', f=True)

            crv_sc = cmds.skinCluster(self.ik_spline_joints,
                                       self.ik_spline_crv,
                                       mi=4,
                                       sm=0,
                                       sw=0.5,
                                       n='{}_skinCluster'.format(self.ik_spline_crv))[0]
            crv_bind=cmds.listConnections('{}.bindPose'.format(crv_sc),c=0,d=1,p=0)
            if crv_bind:cmds.delete(crv_bind)

            cmds.parent(self.ik_spline_joints[0], self.base_ctrl.ctrl)
            cmds.parent(self.ik_spline_joints[-1], self.main_ctrl.ctrl)

            # Create FK For IK Spline
            self.ik_spline_fk = tkgFk.Fk(side=self.side,
                                            part=self.part,
                                            guide_list=self.guide_list,
                                            gimbal=None,
                                            offset=None,
                                            pad="auto",
                                            fk_ctrl_axis='x',
                                            fk_ctrl_edge_axis='-x',
                                            ctrl_scale=1,
                                            ctrl_color=[0.1, 0.4, 0.8],
                                            remove_last=False,
                                            add_joints=True,
                                            fk_shape="cube",
                                            gimbal_shape="circle",
                                            offset_shape="square")
            self.ik_spline_fk.build_fk()

            for ik_spl, fk in zip(self.ik_chain.joints, self.ik_spline_fk.fk_ctrls):
                orc = cmds.orientConstraint(ik_spl, fk.ctrl, w=True, mo=True)[0]
                cmds.setAttr(orc+'.interpType', 2)

        cmds.parent(self.ikh, self.ik_joints[0], self.module_grp)
        if self.soft_ik:
            cmds.parent(self.soft_ik_loc, self.module_grp)

    def skeleton(self):
        ik_chain = tkgChain.Chain(transform_list=self.src_joints,
                                 prefix=self.side,
                                 suffix='JNT',
                                 name=self.part)
        ik_chain.create_from_transforms(orient_constraint=True,
                                        point_constraint=True,
                                        scale_constraint=False,
                                        parent=self.skel)

        self.bind_joints = ik_chain.joints
        self.tag_bind_joints(self.bind_joints[:-1], self.part_grp)

    def add_plugs(self):
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['add ik plug here'], name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])
