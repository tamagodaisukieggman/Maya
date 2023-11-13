# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload

import maya.cmds as cmds

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.libs.attribute as tkgAttr
import tkgRigBuild.libs.common as tkgCommon
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.build.ik as tkgIk
import tkgRigBuild.build.fk as tkgFk
reload(tkgModule)
reload(tkgAttr)
reload(tkgChain)
reload(tkgIk)
reload(tkgCommon)
reload(tkgCtrl)
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

            [cmds.parent(n, self.module_grp) for n in self.ik_spline_joints]

            dTwist_up_axis = {
                'x':[20,0,0],
                'y':[0,20,0],
                'z':[0,0,20],
                '-x':[-20,0,0],
                '-y':[0,-20,0],
                '-z':[0,0,-20],
                '-x-':[20,0,0],
                '-y-':[0,20,0],
                '-z-':[0,0,20],
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

            dWorldUp_values = {
                'x':[1,0,0],
                'y':[0,1,0],
                'z':[0,0,1],
                '-x':[-1,0,0],
                '-y':[0,-1,0],
                '-z':[0,0,-1],
            }

            # For Base IK UP Joint
            self.ik_spline_base_up_joint = cmds.duplicate(self.ik_spline_joints[0],
                                                          n='up_'+self.ik_spline_joints[0])[0]
            # cmds.move(*dTwist_up_axis[self.dWorldUpAxis], self.ik_spline_base_up_joint, r=True, os=True, wd=True)
            cmds.matchTransform(self.ik_spline_base_up_joint, self.ik_spline_joints[0])
            pa = cmds.listRelatives(self.ik_spline_base_up_joint, p=True) or None
            if pa: cmds.parent(self.ik_spline_base_up_joint, w=True)
            cmds.parent(self.ik_spline_base_up_joint, self.module_grp)

            # For Main IK UP Joint
            self.ik_spline_main_up_joint = cmds.duplicate(self.ik_spline_joints[-1],
                                                          n='up_'+self.ik_spline_joints[-1])[0]
            # cmds.move(*dTwist_up_axis[self.dWorldUpAxis], self.ik_spline_main_up_joint, r=True, os=True, wd=True)
            cmds.matchTransform(self.ik_spline_main_up_joint, self.ik_spline_joints[-1])
            pa = cmds.listRelatives(self.ik_spline_main_up_joint, p=True) or None
            if pa: cmds.parent(self.ik_spline_main_up_joint, w=True)
            cmds.parent(self.ik_spline_main_up_joint, self.module_grp)

            # Get Loft
            # loft_axis = tkgCommon.get_loft_axis(start=self.ik_spline_joints[0],
            #                                     end=self.ik_spline_joints[-1])
            #
            # self.ik_lofted, self.ik_curve = tkgCommon.create_loft(nodes=self.ik_spline_joints,
            #                                                       name=self.ik_spline_joints[0]+'_loft_suf',
            #                                                       axis=loft_axis)

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
            cmds.setAttr('{0}.dWorldUpType'.format(self.ikh), 4)
            cmds.setAttr('{0}.dForwardAxis'.format(self.ikh), dForward_axis[self.dForwardAxis])
            cmds.setAttr('{0}.dWorldUpAxis'.format(self.ikh), dWorldUp_axis[self.dWorldUpAxis])
            cmds.setAttr('{}.dWorldUpVector'.format(self.ikh), *dWorldUp_values[self.dWorldUpAxis])
            cmds.setAttr('{}.dWorldUpVectorEnd'.format(self.ikh), *dWorldUp_values[self.dWorldUpAxis])
            cmds.setAttr('{}.dWorldUpVectorEnd'.format(self.ikh), *dWorldUp_values[self.dWorldUpAxis])
            cmds.connectAttr('{0}.worldMatrix[0]'.format(self.ik_spline_base_up_joint), '{0}.dWorldUpMatrix'.format(self.ikh))
            cmds.connectAttr('{0}.worldMatrix[0]'.format(self.ik_spline_main_up_joint), '{0}.dWorldUpMatrixEnd'.format(self.ikh))

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

            self.ik_spline_base_up_joint_ctrl = tkgCtrl.Control(shape="cylinder",
                                            prefix=self.side,
                                            suffix="CTRL",
                                            name=self.part + '_IK_rot_base',
                                            axis="y",
                                            group_type="main",
                                            rig_type=self.side+'_'+self.part+'IkMain',
                                            ctrl_scale=self.ctrl_scale,
                                            ctrl_color=self.ctrl_color,
                                            edge_axis=None,
                                            position=self.ik_spline_base_up_joint,
                                            rotation=self.ik_spline_base_up_joint)
            cmds.parent(self.ik_spline_base_up_joint_ctrl.top, self.base_ctrl.ctrl)
            pac_ik_base_up = cmds.parentConstraint(self.ik_spline_base_up_joint_ctrl.ctrl, self.ik_spline_base_up_joint, w=True, mo=True)[0]
            cmds.setAttr(pac_ik_base_up+'.interpType', 2)

            self.ik_spline_main_up_joint_ctrl = tkgCtrl.Control(shape="cylinder",
                                            prefix=self.side,
                                            suffix="CTRL",
                                            name=self.part + '_IK_rot_main',
                                            axis="y",
                                            group_type="main",
                                            rig_type=self.side+'_'+self.part+'IkMain',
                                            ctrl_scale=self.ctrl_scale,
                                            ctrl_color=self.ctrl_color,
                                            edge_axis=None,
                                            position=self.ik_spline_main_up_joint,
                                            rotation=self.ik_spline_main_up_joint)
            cmds.parent(self.ik_spline_main_up_joint_ctrl.top, self.main_ctrl.ctrl)
            pac_ik_main_up = cmds.parentConstraint(self.ik_spline_main_up_joint_ctrl.ctrl, self.ik_spline_main_up_joint, w=True, mo=True)[0]
            cmds.setAttr(pac_ik_main_up+'.interpType', 2)

            crv_sc = cmds.skinCluster(self.ik_spline_joints,
                                       self.ik_spline_crv,
                                       mi=4,
                                       sm=0,
                                       sw=0.5,
                                       n='{}_skinCluster'.format(self.ik_spline_crv))[0]
            crv_bind=cmds.listConnections('{}.bindPose'.format(crv_sc),c=0,d=1,p=0)
            if crv_bind:cmds.delete(crv_bind)

            # cmds.parent(self.ik_spline_joints[0], self.base_ctrl.ctrl)
            # cmds.parent(self.ik_spline_joints[-1], self.main_ctrl.ctrl)

            pac_ik_base = cmds.parentConstraint(self.base_ctrl.ctrl, self.ik_spline_joints[0], w=True, mo=True)[0]
            cmds.setAttr(pac_ik_base+'.interpType', 2)

            pac_ik_main = cmds.parentConstraint(self.main_ctrl.ctrl, self.ik_spline_joints[-1], w=True, mo=True)[0]
            cmds.setAttr(pac_ik_main+'.interpType', 2)

            # Segments
            ik_mid_ctrls = OrderedDict()
            for i, iksj in enumerate(self.ik_spline_joints):
                if i != 0 and i != len(self.ik_spline_joints)-1:
                    self.ik_spline_mid_ctrl = tkgCtrl.Control(shape="handle_2d_4x",
                                                    prefix=self.side,
                                                    suffix="CTRL",
                                                    name=self.part + '_IK_mid_'+str(i).zfill(2),
                                                    axis="y",
                                                    group_type="main",
                                                    rig_type=self.side+'_'+self.part+'IkMain',
                                                    ctrl_scale=self.ctrl_scale,
                                                    ctrl_color=self.ctrl_color,
                                                    edge_axis=None,
                                                    position=iksj,
                                                    rotation=iksj)
                    ik_mid_ctrls[iksj] = self.ik_spline_mid_ctrl
                    pac_ik_mid = cmds.parentConstraint(self.ik_spline_mid_ctrl.ctrl, iksj, w=True, mo=True)[0]
                    cmds.setAttr(pac_ik_mid+'.interpType', 2)

            splited = tkgCommon.split_list([n for n in ik_mid_ctrls.keys()])
            mid_spl = None
            if len(splited) == 2:
                front_spl = splited[0]
                back_spl = splited[1]

            elif len(splited) == 3:
                mid_spl = splited[0]
                front_spl = splited[1]
                back_spl = splited[2]

            for fsp in front_spl:
                cmds.parent(ik_mid_ctrls[fsp].top, self.base_ctrl.ctrl)

            for bsp in back_spl:
                cmds.parent(ik_mid_ctrls[bsp].top, self.main_ctrl.ctrl)

            if mid_spl:
                pac_mid_spl = cmds.parentConstraint(self.base_ctrl.ctrl, ik_mid_ctrls[mid_spl].top, w=True, mo=True)[0]
                pac_mid_spl = cmds.parentConstraint(self.main_ctrl.ctrl, ik_mid_ctrls[mid_spl].top, w=True, mo=True)[0]
                cmds.setAttr(pac_mid_spl+'.interpType', 2)
                cmds.parent(ik_mid_ctrls[mid_spl].top, self.ik_ctrl_grp)

            # Create FK For IK Spline
            self.ik_spline_fk = tkgFk.Fk(side=self.side,
                                            part=self.part,
                                            guide_list=self.guide_list,
                                            gimbal=None,
                                            offset=None,
                                            pad="auto",
                                            fk_ctrl_axis='x',
                                            fk_ctrl_edge_axis='-x',
                                            ctrl_scale=2.4,
                                            ctrl_color=[0.1, 0.4, 0.8],
                                            remove_last=False,
                                            add_joints=True,
                                            fk_shape="cube",
                                            gimbal_shape="circle",
                                            offset_shape="square")
            self.ik_spline_fk.build_fk()

            # FKをメインにしたほうがいいかも
            # for ik_spl, fk in zip(self.ik_chain.joints, self.ik_spline_fk.fk_ctrls):
            #     cmds.connectAttr(ik_spl+'.r', fk.ctrl+'_SDK_GRP.r', f=True)
            #     # cmds.connectAttr(ik_spl+'.' + self.stretchy_axis, fk.ctrl+'_SDK_GRP.' + self.stretchy_axis, f=True)
            #
            # poc_ik_fk = cmds.pointConstraint(self.base_ctrl.ctrl, self.ik_spline_fk.fk_top, w=True, mo=True)[0]

            cmds.parent(self.ik_spline_fk.fk_joints[0], self.module_grp)

            cmds.parent(self.ik_spline_fk.fk_top, self.ik_ctrl_grp)
            cmds.parent(self.base_ctrl.top, self.ik_spline_fk.fk_ctrls[0].ctrl)
            cmds.parent(self.main_ctrl.top, self.ik_spline_fk.fk_ctrls[-1].ctrl)

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
