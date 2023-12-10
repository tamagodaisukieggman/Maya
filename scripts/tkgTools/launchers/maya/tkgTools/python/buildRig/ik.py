# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.node as brNode
import buildRig.grps as brGrp
import buildRig.joint as brJnt
import buildRig.libs.control.draw as brDraw
import buildRig.transform as brTrs
import buildRig.aim as brAim
import buildRig.fk as brFk
reload(brCommon)
reload(brNode)
reload(brGrp)
reload(brJnt)
reload(brDraw)
reload(brTrs)
reload(brAim)
reload(brFk)

class Ik(brGrp.RigModule):
    def __init__(self,
                 module=None,
                 side=None,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 joints=None,
                 ik_base_shape='cube',
                 ik_base_axis='x',
                 ik_base_scale=5,
                 ik_main_shape='jack',
                 ik_main_axis='x',
                 ik_main_scale=5,
                 ik_pv_shape='locator_3d',
                 ik_pv_axis='x',
                 ik_pv_scale=5,
                 ik_local_shape='cube',
                 ik_local_axis='x',
                 ik_local_scale=5,
                 solver=1,
                 dForwardAxis='x',
                 dWorldUpAxis='z'):
        """
        Params:
        module = string<モジュール名を指定する>
        side = string<中央、右、左がわかる識別子を指定する>
        rig_joints_parent = string<ジョイントをペアレントする親を指定する>
        rig_ctrls_parent = string<コントローラをペアレントする親を指定する>
        joints = list[string]<ベースになるジョイントのリストを指定する>
        shape = string<コントローラのタイプを指定する>
        axis = string<コントローラの向き'x', 'y', 'z'のどれかを指定する>
        scale = float<コントローラのサイズを指定する>

ik = brIk.Ik(module=None,
             side=None,
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             joints=sel,
             ik_base_shape='cube',
             ik_base_axis='x',
             ik_base_scale=1000,
             ik_main_shape='jack',
             ik_main_axis='x',
             ik_main_scale=1000,
             ik_pv_shape='locator_3d',
             ik_pv_axis='x',
             ik_pv_scale=1000,
             ik_local_shape='cube',
             ik_local_axis='x',
             ik_local_scale=1000,
             solver=1)

ik = brIk.Ik(module=None,
             side=None,
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             joints=sel,
             ik_base_shape='cube',
             ik_base_axis='x',
             ik_base_scale=1000,
             ik_main_shape='jack',
             ik_main_axis='x',
             ik_main_scale=1000,
             ik_pv_shape='locator_3d',
             ik_pv_axis='x',
             ik_pv_scale=1000,
             ik_local_shape='cube',
             ik_local_axis='x',
             ik_local_scale=1000,
             solver=2,
             dForwardAxis='-z',
             dWorldUpAxis='x')
        """
        super(Ik, self).__init__(module=module,
                                 side=side)
        self.rig_joints_parent = rig_joints_parent
        self.rig_ctrls_parent = rig_ctrls_parent
        self.joints = joints
        self.ik_base_shape = ik_base_shape
        self.ik_base_axis = ik_base_axis
        self.ik_base_scale = ik_base_scale
        self.ik_main_shape = ik_main_shape
        self.ik_main_axis = ik_main_axis
        self.ik_main_scale = ik_main_scale
        self.ik_pv_shape = ik_pv_shape
        self.ik_pv_axis = ik_pv_axis
        self.ik_pv_scale = ik_pv_scale
        self.ik_local_shape = ik_local_shape
        self.ik_local_axis = ik_local_axis
        self.ik_local_scale = ik_local_scale

        self.jnt_object = None
        self.trs_object = None
        self.trs_objects = []
        self.top_ik_joint_nodes = []
        self.top_ik_ctrl_nodes = []

        self.solvers = {
            0: 'ikSCsolver',
            1: 'ikRPsolver',
            2: 'ikSplineSolver',
            3: 'ikSpringSolver'
        }
        self.solver = self.solvers[solver]

        self.dForwardAxis = dForwardAxis
        self.dWorldUpAxis = dWorldUpAxis

        # Controller
        self.draw = brDraw.Draw()

        self.create_ik_module()

    def create_ik_module(self):
        self.create_joints()
        self.create_ik()
        self.create_ctrls()
        self.create_rig_module()
        if self.solver in ['ikSplineSolver']:
            self.create_ikSpline_for_fk()
            self.create_ikSpline_sineDeformer()

        self.connection()

    def create_joints(self):
        self.jnt_object = brJnt.create_joints(nodes=self.joints, prefix='IK_', suffix=None, replace=['_copy', ''])
        self.ik_joints = self.jnt_object.nodes

        for node in self.jnt_object.node_list:
            node.freezeTransform()
            node.set_preferredAngle()
            node.get_values()
        self.top_ik_joint_nodes.append(self.jnt_object.node_list[0].full_path.split('|')[1])

        if self.solver in ['ikSplineSolver']:
            self.ik_spline_jnt_object = brJnt.create_joints(nodes=self.joints, prefix='IKSPLINE_', suffix=None, replace=['_copy', ''])
            self.ik_spline_joints = self.ik_spline_jnt_object.nodes

            for node in self.ik_spline_jnt_object.node_list:
                node.unparent()

            self.ik_spline_jnt_object.merge_rotation()
            for node in self.ik_spline_jnt_object.node_list:
                node.set_preferredAngle()
                node.get_values()
                self.top_ik_joint_nodes.append(node.full_path)

    def create_ik(self):
        settings = {
            'name':self.ik_joints[-1] + '_IKH',
            'startJoint':self.ik_joints[0],
            'endEffector':self.ik_joints[-1],
            'sticky':'sticky',
            'solver':self.solver
        }

        if self.solver in ['ikSplineSolver']:
            # print('tkgXform.get_distance', tkgXform.get_distance(self.ik_joints[-1], self.ik_joints[-2]))
            pos1 = cmds.xform(self.ik_joints[-1], q=True, t=True, ws=True)
            pos2 = cmds.xform(self.ik_joints[-2], q=True, t=True, ws=True)
            mid_point = brCommon.get_mid_point(pos1, pos2, percentage=-0.1)

            ik_end_jnt = self.ik_joints[-1]+'_END'
            cmds.createNode('joint', n=ik_end_jnt, ss=True)
            cmds.xform(ik_end_jnt, t=mid_point, ws=True, a=True)
            cmds.parent(ik_end_jnt, self.ik_joints[-1])
            guide_ik_joints = [j for j in self.ik_joints]
            guide_ik_joints.append(ik_end_jnt)

            self.ik_spline_crv = brCommon.create_curve_on_nodes(nodes=guide_ik_joints, name=self.ik_joints[-1] + '_CRV')

            settings['endEffector'] = ik_end_jnt
            settings['curve'] = self.ik_spline_crv
            settings['freezeJoints'] = True
            settings['createCurve'] = False
            # settings['snapHandleFlagToggle'] = True
            settings['scv'] = False
            settings['rtm'] = True

            self.crv_sc = cmds.skinCluster(self.ik_spline_joints,
                                       self.ik_spline_crv,
                                       mi=4,
                                       sm=0,
                                       sw=0.5,
                                       n='{}_skinCluster'.format(self.ik_spline_crv))[0]
            crv_bind=cmds.listConnections('{}.bindPose'.format(self.crv_sc),c=0,d=1,p=0)
            if crv_bind:cmds.delete(crv_bind)

            self.top_ik_joint_nodes.append(self.ik_spline_crv)

        self.ikh = cmds.ikHandle(**settings)[0]
        self.top_ik_joint_nodes.append(self.ikh)

    def create_ctrls(self):
        # base
        self.ik_base = self.jnt_object.node_list[0]
        self.draw.create_curve(name=self.ik_base.node + '_CURVE', shape=self.ik_base_shape, axis=self.ik_base_axis, scale=self.ik_base_scale)
        cmds.matchTransform(self.draw.curve, self.ik_base.node)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=['_CURVE', '_BASE_CTRL'])
        self.trs_objects.append(self.trs_object)
        self.ik_base_ctrl_object = self.trs_object

        # main
        self.ik_main = self.jnt_object.node_list[-1]
        self.draw.create_curve(name=self.ik_main.node + '_CURVE', shape=self.ik_main_shape, axis=self.ik_main_axis, scale=self.ik_main_scale)
        cmds.matchTransform(self.draw.curve, self.ik_main.node, pos=True, rot=False, scl=False)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=['_CURVE', '_MAIN_CTRL'])
        self.trs_objects.append(self.trs_object)
        self.ik_main_ctrl_object = self.trs_object

        # local
        self.ik_local = self.jnt_object.node_list[-1]
        self.draw.create_curve(name=self.ik_local.node + '_CURVE', shape=self.ik_local_shape, axis=self.ik_local_axis, scale=self.ik_local_scale)
        cmds.matchTransform(self.draw.curve, self.ik_local.node)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=['_CURVE', '_LOCAL_CTRL'])
        self.trs_objects.append(self.trs_object)
        self.ik_local_ctrl_object = self.trs_object

        cmds.parent(self.ik_local_ctrl_object.nodes[0], self.ik_main_ctrl_object.nodes[-1])

        # ikSplineSolverかそうでないときの処理
        if not self.solver in ['ikSplineSolver']:
            # poleVector
            self.draw.create_curve(name=self.ik_joints[1] + '_CURVE', shape=self.ik_pv_shape, axis=self.ik_pv_axis, scale=self.ik_pv_scale)
            self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                    prefix=None, suffix=None, replace=['_CURVE', '_PV_CTRL'])
            self.trs_objects.append(self.trs_object)

            distance = brCommon.distance_between(self.ik_joints[0], self.ik_joints[2])
            brAim.set_pole_vec(start=self.ik_joints[0],
                               mid=self.ik_joints[1],
                               end=self.ik_joints[2],
                               move=distance / 1.5,
                               obj=self.trs_object.nodes[0])
            cmds.xform(self.trs_object.nodes[0], ro=[0,0,0], a=True)
            self.ik_pv_ctrl_object = self.trs_object

        elif self.solver in ['ikSplineSolver']:
            cmds.parent(self.ik_main_ctrl_object.nodes[0], self.ik_base_ctrl_object.nodes[-1])
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

            cmds.setAttr('{0}.dTwistControlEnable'.format(self.ikh), 1)
            cmds.setAttr('{0}.dWorldUpType'.format(self.ikh), 4)
            cmds.setAttr('{0}.dForwardAxis'.format(self.ikh), dForward_axis[self.dForwardAxis])
            cmds.setAttr('{0}.dWorldUpAxis'.format(self.ikh), dWorldUp_axis[self.dWorldUpAxis])
            cmds.setAttr('{}.dWorldUpVector'.format(self.ikh), *dWorldUp_values[self.dWorldUpAxis])
            cmds.setAttr('{}.dWorldUpVectorEnd'.format(self.ikh), *dWorldUp_values[self.dWorldUpAxis])
            cmds.setAttr('{}.dWorldUpVectorEnd'.format(self.ikh), *dWorldUp_values[self.dWorldUpAxis])
            cmds.connectAttr('{0}.worldMatrix[0]'.format(self.ik_base_ctrl_object.nodes[-1]), '{0}.dWorldUpMatrix'.format(self.ikh))
            cmds.connectAttr('{0}.worldMatrix[0]'.format(self.ik_local_ctrl_object.nodes[-1]), '{0}.dWorldUpMatrixEnd'.format(self.ikh))

            cmds.setAttr('{0}.ikFkManipulation'.format(self.ikh), 1)
            cmds.setAttr('{0}.dTwistValueType'.format(self.ikh), 1)

            ik_spl_pma = cmds.createNode('plusMinusAverage', ss=True)
            ik_spl_pb = cmds.createNode('pairBlend', ss=True)
            cmds.setAttr(ik_spl_pma+'.operation', 2)
            cmds.setAttr(ik_spl_pb+'.weight', 0.5)
            cmds.connectAttr(self.ik_base_ctrl_object.nodes[-1]+'.r'+self.dForwardAxis.replace('-', ''), ik_spl_pma+'.input1D[0]', f=True)
            cmds.connectAttr(self.ik_local_ctrl_object.nodes[-1]+'.r'+self.dForwardAxis.replace('-', ''), ik_spl_pma+'.input1D[1]', f=True)
            cmds.connectAttr(ik_spl_pma+'.output1D', ik_spl_pb+'.inRotate'+self.dForwardAxis.replace('-', '').upper()+'2', f=True)
            cmds.connectAttr(ik_spl_pb+'.outRotate'+self.dForwardAxis.replace('-', '').upper(), self.ikh+'.twist', f=True)

            pac_ik_base = cmds.parentConstraint(self.ik_base_ctrl_object.nodes[-1], self.ik_spline_joints[0], w=True, mo=True)[0]
            cmds.setAttr(pac_ik_base+'.interpType', 2)

            pac_ik_main = cmds.parentConstraint(self.ik_local_ctrl_object.nodes[-1], self.ik_spline_joints[-1], w=True, mo=True)[0]
            cmds.setAttr(pac_ik_main+'.interpType', 2)

            # Segments
            ik_mid_ctrls = OrderedDict()
            for i, iksj in enumerate(self.ik_spline_joints):
                if i != 0 and i != len(self.ik_spline_joints)-1:
                    self.draw.create_curve(name=iksj + '_CURVE', shape='octahedron', axis='y', scale=self.ik_main_scale / 1.5)
                    cmds.matchTransform(self.draw.curve, iksj)
                    self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                            prefix=None, suffix=None, replace=['_CURVE', '_MID_'+str(i).zfill(2)+'_CTRL'])

                    self.ik_spline_mid_ctrl = self.trs_object

                    ik_mid_ctrls[iksj] = self.ik_spline_mid_ctrl
                    pac_ik_mid = cmds.parentConstraint(self.ik_spline_mid_ctrl.nodes[-1], iksj, w=True, mo=True)[0]
                    cmds.setAttr(pac_ik_mid+'.interpType', 2)

            splited = brCommon.split_list([n for n in ik_mid_ctrls.keys()])
            mid_spl = None
            if len(splited) == 2:
                front_spl = splited[0]
                back_spl = splited[1]

            elif len(splited) == 3:
                mid_spl = splited[0]
                front_spl = splited[1]
                back_spl = splited[2]

            for fsp in front_spl:
                cmds.parent(ik_mid_ctrls[fsp].nodes[0], self.ik_base_ctrl_object.nodes[-1])

            for bsp in back_spl:
                cmds.parent(ik_mid_ctrls[bsp].nodes[0], self.ik_main_ctrl_object.nodes[-1])

            if mid_spl:
                pac_mid_spl = cmds.parentConstraint(self.ik_base_ctrl_object.nodes[-1], ik_mid_ctrls[mid_spl].nodes[0], w=True, mo=True)[0]
                pac_mid_spl = cmds.parentConstraint(self.ik_main_ctrl_object.nodes[-1], ik_mid_ctrls[mid_spl].nodes[0], w=True, mo=True)[0]
                cmds.setAttr(pac_mid_spl+'.interpType', 2)
                cmds.parent(ik_mid_ctrls[mid_spl].nodes[0], self.rig_ctrls_parent)

        #
        for trs_object in self.trs_objects:
            for node in trs_object.node_list:
                node.get_values()
            self.top_ik_ctrl_nodes.append(trs_object.node_list[0].full_path.split('|')[1])

        self.top_ik_ctrl_nodes = list(set(self.top_ik_ctrl_nodes))

    def create_rig_module(self):
        self.trs_module_ik = brTrs.create_transforms(nodes=[self.module_grp, self.module_grp + '_IK'], offsets=False)
        self.trs_ctrl_ik = brTrs.create_transforms(nodes=[self.ctrl_grp, self.ctrl_grp + '_IK'], offsets=False)

        # リグ用のジョイントをペアレント化させる
        if not self.rig_joints_parent:
            self.rig_joints_parent = self.trs_module_ik.nodes[-1]

        for jnt in self.top_ik_joint_nodes:
            cmds.parent(jnt, self.rig_joints_parent)

        # コントローラをペアレント化させる
        if not self.rig_ctrls_parent:
            self.rig_ctrls_parent = self.trs_ctrl_ik.nodes[-1]

        for ctrl in self.top_ik_ctrl_nodes:
            cmds.parent(ctrl, self.rig_ctrls_parent)

    def create_ikSpline_for_fk(self):
        fk = brFk.Fk(module=self.module,
                         side=self.side,
                         rig_joints_parent=self.rig_joints_parent,
                         rig_ctrls_parent=self.rig_ctrls_parent,
                         joints=self.ik_joints,
                         shape='cube',
                         axis='x',
                         scale=self.ik_main_scale / 2)

        for ik_jnt, trs_object in zip(self.ik_joints, fk.trs_objects):
            pbn = cmds.createNode('pairBlend', n=trs_object.nodes[1]+'_PBN', ss=True)
            cmds.setAttr(pbn+'.rotInterpolation', 1)

            cmds.connectAttr(ik_jnt+'.r', pbn+'.inRotate2', f=True)
            cmds.connectAttr(pbn+'.outRotate', trs_object.nodes[1]+'.r', f=True)

    def create_ikSpline_sineDeformer(self):
        type = 'sine'
        nonLinDef = cmds.nonLinear(self.ik_spline_crv, type=type, n=type.upper()+'_'+self.ik_spline_crv)
        cmds.setAttr(nonLinDef[0]+'.dropoff', 1)
        aim_con = cmds.aimConstraint(self.ik_main_ctrl_object.nodes[-1], nonLinDef[1], aimVector=[0,1,0], upVector=[0,0,1], worldUpType='vector', worldUpVector=[0,1,0])[0]
        cmds.delete(aim_con)

        self.draw.create_curve(name=nonLinDef[0] + '_CURVE', shape='sphere', axis='y', scale=self.ik_main_scale / 1.5)

        # addAttr
        cmds.addAttr(self.draw.curve, ln='envelope', at='double', dv=1, max=1, min=0, k=True)
        cmds.addAttr(self.draw.curve, ln='amplitude', at='double', dv=0, max=5, min=-5, k=True)
        cmds.addAttr(self.draw.curve, ln='wavelength', at='double', dv=2, max=2, min=0.1, k=True)
        cmds.addAttr(self.draw.curve, ln='offset', at='double', dv=0, max=10, min=-10, k=True)
        cmds.addAttr(self.draw.curve, ln='dropoff', at='double', dv=1, max=1, min=-1, k=True)
        cmds.addAttr(self.draw.curve, ln='lowBound', at='double', dv=-1, max=0, min=-10, k=True)
        cmds.addAttr(self.draw.curve, ln='highBound', at='double', dv=1, max=10, min=0, k=True)

        # connectAttr
        cmds.connectAttr(self.draw.curve+'.envelope', nonLinDef[0]+'.envelope', f=True)
        cmds.connectAttr(self.draw.curve+'.amplitude', nonLinDef[0]+'.amplitude', f=True)
        cmds.connectAttr(self.draw.curve+'.wavelength', nonLinDef[0]+'.wavelength', f=True)
        cmds.connectAttr(self.draw.curve+'.offset', nonLinDef[0]+'.offset', f=True)
        cmds.connectAttr(self.draw.curve+'.dropoff', nonLinDef[0]+'.dropoff', f=True)
        cmds.connectAttr(self.draw.curve+'.lowBound', nonLinDef[0]+'.lowBound', f=True)
        cmds.connectAttr(self.draw.curve+'.highBound', nonLinDef[0]+'.highBound', f=True)

        cmds.matchTransform(self.draw.curve, nonLinDef[1], pos=True, rot=True, scl=False)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=[nonLinDef[0]+'_CURVE', nonLinDef[0]+'_CTRL'])


        self.ik_spline_sine_ctrl = self.trs_object

        cmds.parent(self.ik_spline_sine_ctrl.nodes[0], self.ik_base_ctrl_object.nodes[-1])
        cmds.parent(nonLinDef[1], self.trs_module_ik.nodes[-1])
        cmds.parentConstraint(self.ik_spline_sine_ctrl.nodes[-1], nonLinDef[1], w=True)


    def connection(self):
        if not self.solver in ['ikSplineSolver']:
            # base
            cmds.pointConstraint(self.ik_base_ctrl_object.nodes[-1], self.ik_joints[0], w=True)

            # main
            cmds.pointConstraint(self.ik_main_ctrl_object.nodes[-1], self.ikh, w=True)

            # poleVector
            cmds.poleVectorConstraint(self.ik_pv_ctrl_object.nodes[-1], self.ikh, w=True)

            # local
            ori_con = cmds.orientConstraint(self.ik_local_ctrl_object.nodes[-1], self.ik_joints[-1], w=True)[0]
            cmds.setAttr(ori_con+'.interpType', 2)

            switch_ori_con = cmds.orientConstraint(self.ik_joints[1], self.ik_local_ctrl_object.nodes[2], w=True, mo=True)[0]
            cmds.setAttr(switch_ori_con+'.interpType', 2)
            cmds.disconnectAttr(switch_ori_con+'.constraintRotateX', self.ik_local_ctrl_object.nodes[2]+'.rx')
            cmds.disconnectAttr(switch_ori_con+'.constraintRotateY', self.ik_local_ctrl_object.nodes[2]+'.ry')
            cmds.disconnectAttr(switch_ori_con+'.constraintRotateZ', self.ik_local_ctrl_object.nodes[2]+'.rz')

            # local pairBlend
            pbn = cmds.createNode('pairBlend', n=self.ik_local_ctrl_object.nodes[2]+'_PBN', ss=True)
            cmds.setAttr(pbn+'.rotInterpolation', 1)

            cmds.connectAttr(switch_ori_con+'.constraintRotate', pbn+'.inRotate2', f=True)
            cmds.connectAttr(pbn+'.outRotate', self.ik_local_ctrl_object.nodes[2]+'.r', f=True)

            # local pairBlend addAttr
            cmds.addAttr(self.ik_local_ctrl_object.nodes[-1], ln='autoPose', sn='ap', at='double', dv=0, max=1, min=0, k=True)
            cmds.connectAttr(self.ik_local_ctrl_object.nodes[-1]+'.ap', pbn+'.weight', f=True)
