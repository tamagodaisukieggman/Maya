# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import math
import re
import traceback

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.connecter as brConnecter
import buildRig.node as brNode
import buildRig.grps as brGrp
import buildRig.joint as brJnt
import buildRig.libs.control.draw as brDraw
import buildRig.transform as brTrs
import buildRig.aim as brAim
import buildRig.fk as brFk
reload(brCommon)
reload(brConnecter)
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
                 ik_base_axis=[0,0,0],
                 ik_base_scale=5,
                 ik_main_shape='jack',
                 ik_main_axis=[0,0,0],
                 ik_main_scale=5,
                 ik_pv_shape='locator_3d',
                 ik_pv_axis=[0,0,0],
                 ik_pv_scale=5,
                 ik_local_shape='cube',
                 ik_local_axis=[0,0,0],
                 ik_local_scale=5,
                 stretchy_axis='x',
                 softik=None,
                 solver=1,
                 dForwardAxis='x',
                 dWorldUpAxis='z',
                 roll_fk_axis='z',
                 roll_fk_ctrl_axis=[0,90,0]):

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

        # ikSplineFkCtrls
        self.ik_spline_fk_ctrls = []
        self.ik_spline_fkik_jnts = []

        # stretchy
        self.stretchy_axis = stretchy_axis

        # softik
        self.softik = softik

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

        # roll fk
        self.roll_fk_axis = roll_fk_axis
        self.roll_fk_ctrl_axis = roll_fk_ctrl_axis

        # Controller
        self.draw = brDraw.Draw()

        # モジュールのノードを追加
        self.trs_module_ik = brTrs.create_transforms(nodes=[self.module_grp, self.module_grp + '_IK'], offsets=False)
        self.trs_ctrl_ik = brTrs.create_transforms(nodes=[self.ctrl_grp, self.ctrl_grp + '_IK'], offsets=False)

        self.create_ik_module()

    def create_ik_module(self):
        self.create_joints()
        self.create_ik()
        self.create_ctrls()
        self.create_rig_module()
        if self.solver in ['ikSplineSolver']:
            self.create_ikSpline_for_fk()
            self.create_ikSpline_sineDeformer()

        if self.stretchy_axis:
            # self.stretchy()
            self.multi_stretchy()

        self.connection()

        if self.softik:
            ik_ctrl = self.ik_main_ctrl_object.nodes[-1]
            ikhandle = self.ikh

            self.soft_ik_start_loc = create_softik(ik_ctrl, ikhandle)
            cmds.parent(self.soft_ik_start_loc, self.trs_module_ik.nodes[-1])

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
        self.draw.joint_shape()
        cmds.matchTransform(self.draw.curve, self.ik_base.node)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=['_CURVE', '_BASE_CTRL'])
        self.trs_objects.append(self.trs_object)
        self.ik_base_ctrl_object = self.trs_object

        # main
        self.ik_main = self.jnt_object.node_list[-1]
        self.draw.create_curve(name=self.ik_main.node + '_CURVE', shape=self.ik_main_shape, axis=self.ik_main_axis, scale=self.ik_main_scale)
        self.draw.joint_shape()
        cmds.matchTransform(self.draw.curve, self.ik_main.node, pos=True, rot=False, scl=False)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=['_CURVE', '_MAIN_CTRL'])
        self.trs_objects.append(self.trs_object)
        self.ik_main_ctrl_object = self.trs_object

        self.ikh_const_node = cmds.createNode('transform', n=self.ikh+'_CONST_NODE', ss=True)
        cmds.matchTransform(self.ikh_const_node, self.ik_main_ctrl_object.nodes[-1])
        cmds.parent(self.ikh_const_node, self.ik_main_ctrl_object.nodes[-1])

        # local
        self.ik_local = self.jnt_object.node_list[-1]
        self.draw.create_curve(name=self.ik_local.node + '_CURVE', shape=self.ik_local_shape, axis=self.ik_local_axis, scale=self.ik_local_scale)
        self.draw.joint_shape()
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
            self.draw.joint_shape()
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
                    self.draw.create_curve(name=iksj + '_CURVE', shape='octahedron', axis=[0,0,0], scale=self.ik_main_scale / 1.5)
                    self.draw.joint_shape()
                    cmds.matchTransform(self.draw.curve, iksj)
                    self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                            prefix=None, suffix=None, replace=['_CURVE', '_MID_'+str(i).zfill(2)+'_CTRL'])

                    self.ik_spline_mid_ctrl = self.trs_object
                    self.trs_objects.append(self.trs_object)

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
                cmds.parent(ik_mid_ctrls[bsp].nodes[0], self.ik_base_ctrl_object.nodes[-1])

            # """
            # constしないほうがいい？
            # back constraint
            # if front_spl:
            #     back_const_fsp = front_spl[len(front_spl) - 1]
            #     back_const_node = ik_mid_ctrls[back_const_fsp].nodes[-1]
            #     back_parent_ctrl = None
            #     for bsp in back_spl[::-1]:
            #         if back_parent_ctrl:
            #             cmds.pointConstraint(back_parent_ctrl, ik_mid_ctrls[bsp].nodes[0], w=True, mo=True)
            #             cmds.pointConstraint(back_const_node, ik_mid_ctrls[bsp].nodes[0], w=True, mo=True)
            #         back_parent_ctrl = ik_mid_ctrls[bsp].nodes[-1]

            #     keys = list(ik_mid_ctrls.keys())
            #     last_key = keys[-1]
            #     last_mid_const_node = ik_mid_ctrls[last_key].nodes[0]
            #     cmds.pointConstraint(self.ik_main_ctrl_object.nodes[-1], last_mid_const_node, w=True, mo=True)
            #     cmds.pointConstraint(back_const_node, last_mid_const_node, w=True, mo=True)
            #     # print('ik_mid_ctrls', ik_mid_ctrls[last_key])
            #     # """

            if mid_spl:
                pac_mid_spl = cmds.parentConstraint(self.ik_base_ctrl_object.nodes[-1], ik_mid_ctrls[mid_spl].nodes[0], w=True, mo=True)[0]
                # pac_mid_spl = cmds.parentConstraint(self.ik_main_ctrl_object.nodes[-1], ik_mid_ctrls[mid_spl].nodes[0], w=True, mo=True)[0]
                cmds.setAttr(pac_mid_spl+'.interpType', 2)
                cmds.parent(ik_mid_ctrls[mid_spl].nodes[0], self.trs_ctrl_ik.nodes[-1])

            # addAttr roll
            cmds.addAttr(self.ik_main_ctrl_object.nodes[-1], ln='roll', at='double', dv=0, k=True)
            cmds.connectAttr(self.ik_main_ctrl_object.nodes[-1]+'.roll', self.ikh+'.roll', f=True)

        # addAttr twist
        cmds.addAttr(self.ik_main_ctrl_object.nodes[-1], ln='twist', at='double', dv=0, k=True)
        cmds.connectAttr(self.ik_main_ctrl_object.nodes[-1]+'.twist', self.ikh+'.twist', f=True)

        #
        for trs_object in self.trs_objects:
            for node in trs_object.node_list:
                node.get_values()
            self.top_ik_ctrl_nodes.append(trs_object.node_list[0].full_path.split('|')[1])

        self.top_ik_ctrl_nodes = list(set(self.top_ik_ctrl_nodes))

    def create_rig_module(self):
        # リグ用のジョイントをペアレント化させる
        if not self.rig_joints_parent:
            self.rig_joints_parent = self.trs_module_ik.nodes[-1]

        for jnt in self.top_ik_joint_nodes:
            cmds.parent(jnt, self.rig_joints_parent)

        # コントローラをペアレント化させる
        if not self.rig_ctrls_parent:
            self.rig_ctrls_parent = self.trs_ctrl_ik.nodes[-1]

        for ctrl in self.top_ik_ctrl_nodes:
            # ctrl_pa = cmds.listRelatives(ctrl, p=True) or None
            # parent用に例外処理
            try:
                cmds.parent(ctrl, self.rig_ctrls_parent)
            except:
                # print(traceback.format_exc())
                pass

    def stretchy(self):
        base_ctrl = self.ik_base_ctrl_object.nodes[-1]
        main_ctrl = self.ik_main_ctrl_object.nodes[-1]
        # main_ctrl = self.ikh_const_node
        ik_chain_length = brCommon.chain_length(chain_list=self.ik_joints)

        mdns = []
        for stretch_node, length in zip(self.ik_joints[:-1:], ik_chain_length):
            mdn = cmds.createNode('multiplyDivide', n=stretch_node+'_STRETCH_MDN', ss=True)
            cmds.setAttr(mdn+'.input1X', length)
            mdns.append(mdn)

        dbn = cmds.createNode('distanceBetween', n=main_ctrl+'_DBN', ss=True)
        cmds.connectAttr(base_ctrl+'.worldMatrix[0]', dbn+'.inMatrix1', f=True)
        cmds.connectAttr(self.ikh_const_node+'.worldMatrix[0]', dbn+'.inMatrix2', f=True)
        cmds.addAttr(dbn, ln='stretchLength', sn='sl',
                     at='double', dv=sum(ik_chain_length), max=sum(ik_chain_length), min=sum(ik_chain_length))

        goal_mdn = cmds.createNode('multiplyDivide', n=self.ik_joints[-1]+'_STRETCH_MDN', ss=True)
        cmds.setAttr(goal_mdn+'.input1X', sum(ik_chain_length))
        cmds.setAttr(goal_mdn+'.operation', 2)

        if self.solver in ['ikSplineSolver']:
            adn = cmds.createNode('addDoubleLinear', n=main_ctrl+'_ADN', ss=True)
            dif = sum(ik_chain_length) - cmds.getAttr(dbn+'.distance')
            cmds.setAttr(adn+'.input2', dif)

            cdn = cmds.createNode('condition', n=main_ctrl+'_STRETCH_CDN', ss=True)
            cmds.setAttr(cdn+'.operation', 3)
            cmds.setAttr(cdn+'.colorIfTrueR', 1)
            cmds.connectAttr(dbn+'.distance', adn+'.input1', f=True)
            cmds.connectAttr(adn+'.output', cdn+'.secondTerm', f=True)
            cmds.connectAttr(dbn+'.stretchLength', cdn+'.firstTerm', f=True)

            pma = cmds.createNode('plusMinusAverage', n=main_ctrl+'_STRETCH_PMA', ss=True)
            for i, mdn in enumerate(mdns):
                cmds.connectAttr(mdn+'.outputX', pma+'.input1D[{}]'.format(i), f=True)
            cmds.connectAttr(adn+'.output', goal_mdn+'.input1X', f=True)
            cmds.connectAttr(pma+'.output1D', goal_mdn+'.input2X', f=True)

        else:
            cdn = cmds.createNode('condition', n=main_ctrl+'_STRETCH_CDN', ss=True)
            cmds.setAttr(cdn+'.operation', 3)
            cmds.setAttr(cdn+'.colorIfTrueR', 1)
            cmds.connectAttr(dbn+'.distance', cdn+'.secondTerm', f=True)
            cmds.connectAttr(dbn+'.stretchLength', cdn+'.firstTerm', f=True)

            pma = cmds.createNode('plusMinusAverage', n=main_ctrl+'_STRETCH_PMA', ss=True)
            for i, mdn in enumerate(mdns):
                cmds.connectAttr(mdn+'.outputX', pma+'.input1D[{}]'.format(i), f=True)
            cmds.connectAttr(dbn+'.distance', goal_mdn+'.input1X', f=True)
            cmds.connectAttr(pma+'.output1D', goal_mdn+'.input2X', f=True)
            # ikrp

        stretch_bta = cmds.createNode('blendTwoAttr', n=main_ctrl+'_STRETCH_BTA', ss=True)
        cmds.setAttr(stretch_bta+'.input[0]', 1)
        cmds.connectAttr(goal_mdn+'.outputX', stretch_bta+'.input[1]', f=True)
        cmds.connectAttr(stretch_bta+'.output', cdn+'.colorIfFalseR', f=True)

        shrink_bta = cmds.createNode('blendTwoAttr', n=main_ctrl+'_SHRINK_BTA', ss=True)
        cmds.setAttr(shrink_bta+'.input[0]', 1)
        cmds.connectAttr(goal_mdn+'.outputX', shrink_bta+'.input[1]', f=True)
        cmds.connectAttr(shrink_bta+'.output', cdn+'.colorIfTrueR', f=True)

        for ikj in self.ik_joints:
            if not ikj == self.ik_joints[-1]:
                cmds.connectAttr(cdn+'.outColorR', ikj+'.s'+self.stretchy_axis, f=True)

        # addAttr
        cmds.addAttr(main_ctrl, ln='stretchy', at='double', dv=0, max=1, min=0, k=True)
        cmds.addAttr(main_ctrl, ln='shrink', at='double', dv=0, max=1, min=0, k=True)
        cmds.connectAttr(main_ctrl+'.stretchy', stretch_bta+'.attributesBlender', f=True)
        cmds.connectAttr(main_ctrl+'.shrink', shrink_bta+'.attributesBlender', f=True)

    def multi_stretchy(self, default_reverse=False):
        # lookdevKitをロードしないといけない

        main_ctrl = self.ik_main_ctrl_object.nodes[-1]
        softik_bwn = ''

        startJoint = cmds.ikHandle(self.ikh, q=1, startJoint=1)
        endEffector = cmds.ikHandle(self.ikh, q=1, endEffector=1)
        jointList = cmds.ikHandle(self.ikh, q=1, jointList=1)

        cmds.select(endEffector)
        endJoint=cmds.pickWalk(d='up')
        endJoint=cmds.pickWalk(d='down')[0]

        jointList.append(endJoint)

        stretch_nodes=[]

        # get joints distance
        def get_distance(objA, objB):
            gObjA = cmds.xform(objA, q=True, t=True, ws=True)
            gObjB = cmds.xform(objB, q=True, t=True, ws=True)

            return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

        distance = 0.0
        i = 0
        for jnt in jointList:
            if i == 0:
                pass
            else:
                distance += get_distance(jointList[i-1], jnt)
            i += 1

        # Add Attr
        listAttrs = cmds.listAttr(main_ctrl, ud=1)
        if not listAttrs or not 'stretchIK' in listAttrs:
            cmds.addAttr(main_ctrl, ln='stretchIK', at='double', k=1)
            cmds.setAttr('{0}.{1}'.format(main_ctrl, 'stretchIK'), l=1)

        if not listAttrs or not 'stretchy' in listAttrs:
            cmds.addAttr(main_ctrl, ln='stretchy', at='double', min=0, max=1, dv=0, k=1)

        if not listAttrs or not 'nudge' in listAttrs:
            cmds.addAttr(main_ctrl, ln='nudge', at='double', dv=0, k=1)

        if not listAttrs or not 'flexible' in listAttrs:
            cmds.addAttr(main_ctrl, ln='flexible', at='double', min=0, max=1, dv=0, k=1)

        if not listAttrs or not 'stretchType' in listAttrs:
            cmds.addAttr(main_ctrl, ln='stretchType', at='enum', en='Translate:Scale:', k=1)

        if not listAttrs or not 'reverseTranslate' in listAttrs:
            cmds.addAttr(main_ctrl, ln='reverseTranslate', at='enum', en='Off:On:', k=1)

        # softik relative
        if softik_bwn != '':
            softik_switch_rev=cmds.createNode('reverse', n='{0}_stretch_softik_rev'.format(main_ctrl))
            cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.inputX'.format(softik_switch_rev), f=1)
            cmds.connectAttr('{0}.outputX'.format(softik_switch_rev), '{0}.{1}'.format(softik_bwn[0][0], softik_bwn[1]), f=1)
            stretch_nodes.append(softik_switch_rev)


        # Base Nodes
        stik_dbn = cmds.createNode('distanceBetween', n='{0}_stretch_base_dbn'.format(main_ctrl), ss=1)
        stik_flc = cmds.createNode('floatLogic', n='{0}_stretch_base_flc'.format(main_ctrl), ss=1)

        stik_mdl_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_st_mdl'.format(main_ctrl), ss=1)
        stik_adl_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_nu_adl'.format(main_ctrl), ss=1)
        stik_adl_start_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_start_nu_adl'.format(main_ctrl), ss=1)
        stik_adl_mid_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_mid_nu_adl'.format(main_ctrl), ss=1)
        stik_adl_end_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_end_nu_adl'.format(main_ctrl), ss=1)

        stik_mdl_flx = cmds.createNode('multDoubleLinear', n='{0}_stretch_flx_mdl'.format(main_ctrl), ss=1)

        stik_flcmp_tr_typ = cmds.createNode('floatComposite', n='{0}_stretch_type_tr_flcmp'.format(main_ctrl), ss=1)
        stik_flcmp_sc_typ = cmds.createNode('floatComposite', n='{0}_stretch_type_sc_flcmp'.format(main_ctrl), ss=1)
        stik_rev_sc_typ = cmds.createNode('reverse', n='{0}_stretch_type_sc_rev'.format(main_ctrl), ss=1)

        stik_flcdn_tr_rev = cmds.createNode('floatCondition', n='{0}_stretch_tr_rev_flcdn'.format(main_ctrl), ss=1)

        stretch_nodes.append(stik_dbn)
        stretch_nodes.append(stik_flc)
        stretch_nodes.append(stik_mdl_st)
        stretch_nodes.append(stik_adl_nu)
        stretch_nodes.append(stik_adl_start_nu)
        stretch_nodes.append(stik_adl_mid_nu)
        stretch_nodes.append(stik_adl_end_nu)
        stretch_nodes.append(stik_mdl_flx)
        stretch_nodes.append(stik_flcmp_tr_typ)
        stretch_nodes.append(stik_flcmp_sc_typ)
        stretch_nodes.append(stik_rev_sc_typ)
        stretch_nodes.append(stik_flcdn_tr_rev)

        # setAttr
        cmds.setAttr('{0}.operation'.format(stik_flc), 4)
        cmds.setAttr('{0}.floatA'.format(stik_flc), distance)

        # cmds.setAttr('{0}.input2'.format(stik_mdl_st), 0.5)
        cmds.setAttr('{0}.floatA'.format(stik_flcdn_tr_rev), -0.5)
        cmds.setAttr('{0}.floatB'.format(stik_flcdn_tr_rev), 0.5)

        if default_reverse:
            cmds.setAttr('{0}.floatA'.format(stik_flcdn_tr_rev), 0.5)
            cmds.setAttr('{0}.floatB'.format(stik_flcdn_tr_rev), -0.5)

        cmds.setAttr('{0}.input2'.format(stik_adl_nu), 1)

        cmds.setAttr('{0}.floatA'.format(stik_flcmp_tr_typ), 0)
        cmds.setAttr('{0}.floatB'.format(stik_flcmp_tr_typ), 2)
        cmds.setAttr('{0}.operation'.format(stik_flcmp_tr_typ), 2)

        cmds.setAttr('{0}.floatA'.format(stik_flcmp_sc_typ), 0)
        cmds.setAttr('{0}.floatB'.format(stik_flcmp_sc_typ), 2)
        cmds.setAttr('{0}.operation'.format(stik_flcmp_sc_typ), 2)

        # connect
        startJoint_stretch_parent = '{0}_stretch_parent'.format(startJoint)
        cmds.duplicate(startJoint, n=startJoint_stretch_parent, po=1)
        cmds.connectAttr('{0}.worldMatrix[0]'.format(startJoint_stretch_parent), '{0}.inMatrix1'.format(stik_dbn), f=1)
        cmds.connectAttr('{0}.worldMatrix[0]'.format(main_ctrl), '{0}.inMatrix2'.format(stik_dbn), f=1)
        cmds.connectAttr('{0}.distance'.format(stik_dbn), '{0}.floatB'.format(stik_flc), f=1)

        cmds.connectAttr('{0}.nudge'.format(main_ctrl), '{0}.input1'.format(stik_adl_nu), f=1)
        cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_start_nu), f=1)
        cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_mid_nu), f=1)
        cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_end_nu), f=1)

        cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_tr_rev), '{0}.input2'.format(stik_mdl_st), f=1)


        # Translate Nodes
        stik_fmn_tr = cmds.createNode('floatMath', n='{0}_stretch_tr_fmn'.format(main_ctrl), ss=1)
        stik_cdn_tr_res = cmds.createNode('condition', n='{0}_stretch_tr_res_cdn'.format(main_ctrl), ss=1)

        stik_mdl_mid_tr_res_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_mid_tr_res_st_mdl'.format(main_ctrl), ss=1)
        stik_adl_mid_tr_init = cmds.createNode('addDoubleLinear', n='{0}_stretch_mid_tr_init_adl'.format(main_ctrl), ss=1)
        stik_mdl_mid_tr_fin = cmds.createNode('multDoubleLinear', n='{0}_stretch_mid_tr_fin_mdl'.format(main_ctrl), ss=1)

        stik_mdl_end_tr_res_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_end_tr_res_st_mdl'.format(main_ctrl), ss=1)
        stik_adl_end_tr_init = cmds.createNode('addDoubleLinear', n='{0}_stretch_end_tr_init_adl'.format(main_ctrl), ss=1)
        stik_mdl_end_tr_fin = cmds.createNode('multDoubleLinear', n='{0}_stretch_end_tr_fin_mdl'.format(main_ctrl), ss=1)

        stik_flcdn_mid_tr_init = cmds.createNode('floatCondition', n='{0}_stretch_mid_tr_init_flcdn'.format(main_ctrl), ss=1)
        stik_flcdn_end_tr_init = cmds.createNode('floatCondition', n='{0}_stretch_end_tr_init_flcdn'.format(main_ctrl), ss=1)

        stretch_nodes.append(stik_fmn_tr)
        stretch_nodes.append(stik_cdn_tr_res)
        stretch_nodes.append(stik_mdl_mid_tr_res_st)
        stretch_nodes.append(stik_adl_mid_tr_init)
        stretch_nodes.append(stik_mdl_mid_tr_fin)
        stretch_nodes.append(stik_mdl_end_tr_res_st)
        stretch_nodes.append(stik_adl_end_tr_init)
        stretch_nodes.append(stik_mdl_end_tr_fin)
        stretch_nodes.append(stik_flcdn_mid_tr_init)
        stretch_nodes.append(stik_flcdn_end_tr_init)

        # Translate set
        cmds.setAttr('{0}.operation'.format(stik_fmn_tr), 1)
        cmds.setAttr('{0}.operation'.format(stik_cdn_tr_res), 0)
        cmds.setAttr('{0}.secondTerm'.format(stik_cdn_tr_res), 1)

        # mid_distance = get_distance(jointList[0], jointList[1])
        mid_distance = cmds.getAttr('{0}.t{1}'.format(jointList[1], self.stretchy_axis))
        cmds.setAttr('{0}.input1'.format(stik_adl_mid_tr_init), mid_distance)
        cmds.setAttr('{0}.floatA'.format(stik_flcdn_mid_tr_init), mid_distance*-1)
        cmds.setAttr('{0}.floatB'.format(stik_flcdn_mid_tr_init), mid_distance)

        # end_distance = get_distance(jointList[-2], jointList[-1])
        end_distance = cmds.getAttr('{0}.t{1}'.format(jointList[-1], self.stretchy_axis))
        cmds.setAttr('{0}.input1'.format(stik_adl_end_tr_init), end_distance)
        cmds.setAttr('{0}.floatA'.format(stik_flcdn_end_tr_init), end_distance*-1)
        cmds.setAttr('{0}.floatB'.format(stik_flcdn_end_tr_init), end_distance)

        # Translate connect
        cmds.connectAttr('{0}.floatA'.format(stik_flc), '{0}.floatB'.format(stik_fmn_tr), f=1)
        cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.floatA'.format(stik_fmn_tr), f=1)
        cmds.connectAttr('{0}.outBool'.format(stik_flc), '{0}.firstTerm'.format(stik_cdn_tr_res), f=1)

        cmds.connectAttr('{0}.outFloat'.format(stik_fmn_tr), '{0}.colorIfTrueR'.format(stik_cdn_tr_res), f=1)

        cmds.connectAttr('{0}.outFloat'.format(stik_fmn_tr), '{0}.input1'.format(stik_mdl_flx), f=1)
        cmds.connectAttr('{0}.flexible'.format(main_ctrl), '{0}.input2'.format(stik_mdl_flx), f=1)
        cmds.connectAttr('{0}.output'.format(stik_mdl_flx), '{0}.colorIfFalseR'.format(stik_cdn_tr_res), f=1)

        cmds.connectAttr('{0}.outColorR'.format(stik_cdn_tr_res), '{0}.input1'.format(stik_mdl_mid_tr_res_st), f=1)
        cmds.connectAttr('{0}.outColorR'.format(stik_cdn_tr_res), '{0}.input1'.format(stik_mdl_end_tr_res_st), f=1)

        cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.input1'.format(stik_mdl_st), f=1)

        cmds.connectAttr('{0}.output'.format(stik_mdl_st), '{0}.input2'.format(stik_mdl_mid_tr_res_st), f=1)
        cmds.connectAttr('{0}.output'.format(stik_mdl_st), '{0}.input2'.format(stik_mdl_end_tr_res_st), f=1)
        cmds.connectAttr('{0}.output'.format(stik_mdl_mid_tr_res_st), '{0}.input2'.format(stik_adl_mid_tr_init), f=1)
        cmds.connectAttr('{0}.output'.format(stik_mdl_end_tr_res_st), '{0}.input2'.format(stik_adl_end_tr_init), f=1)

        cmds.connectAttr('{0}.output'.format(stik_adl_mid_nu), '{0}.input1'.format(stik_mdl_mid_tr_fin), f=1)
        cmds.connectAttr('{0}.output'.format(stik_adl_end_nu), '{0}.input1'.format(stik_mdl_end_tr_fin), f=1)
        cmds.connectAttr('{0}.output'.format(stik_adl_mid_tr_init), '{0}.input2'.format(stik_mdl_mid_tr_fin), f=1)
        cmds.connectAttr('{0}.output'.format(stik_adl_end_tr_init), '{0}.input2'.format(stik_mdl_end_tr_fin), f=1)

        cmds.connectAttr('{0}.output'.format(stik_mdl_mid_tr_fin), '{0}.t{1}'.format(jointList[-2], self.stretchy_axis), f=1)
        cmds.connectAttr('{0}.output'.format(stik_mdl_end_tr_fin), '{0}.t{1}'.format(jointList[-1], self.stretchy_axis), f=1)

        cmds.connectAttr('{0}.stretchType'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_tr_typ), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_tr_typ), '{0}.nodeState'.format(stik_mdl_mid_tr_fin), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_tr_typ), '{0}.nodeState'.format(stik_mdl_end_tr_fin), f=1)

        # cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_mid_tr_init), f=1)
        # cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_mid_tr_init), '{0}.input1'.format(stik_adl_mid_tr_init), f=1)
        #
        # cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_end_tr_init), f=1)
        # cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_end_tr_init), '{0}.input1'.format(stik_adl_end_tr_init), f=1)

        cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_tr_rev), f=1)

        # Scale Nodes
        stik_flcmp_sc_flx = cmds.createNode('floatComposite', n='{0}_stretch_flx_sc_flcmp'.format(main_ctrl), ss=1)
        stik_cdn_sc_res = cmds.createNode('condition', n='{0}_stretch_sc_res_cdn'.format(main_ctrl), ss=1)
        stik_fmn_sc = cmds.createNode('floatMath', n='{0}_stretch_sc_fmn'.format(main_ctrl), ss=1)
        stik_flcmp_st_sc = cmds.createNode('floatComposite', n='{0}_stretch_sc_st_flcmp'.format(main_ctrl), ss=1)
        stik_fmn_start_sc_fin = cmds.createNode('floatMath', n='{0}_stretch_start_sc_fin_fmn'.format(main_ctrl), ss=1)
        stik_fmn_mid_sc_fin = cmds.createNode('floatMath', n='{0}_stretch_mid_sc_fin_fmn'.format(main_ctrl), ss=1)

        stretch_nodes.append(stik_flcmp_sc_flx)
        stretch_nodes.append(stik_cdn_sc_res)
        stretch_nodes.append(stik_fmn_sc)
        stretch_nodes.append(stik_flcmp_st_sc)
        stretch_nodes.append(stik_fmn_start_sc_fin)
        stretch_nodes.append(stik_fmn_mid_sc_fin)

        # Scale setAttr
        cmds.setAttr('{0}.operation'.format(stik_flcmp_sc_flx), 2)
        cmds.setAttr('{0}.operation'.format(stik_cdn_sc_res), 3)
        cmds.setAttr('{0}.operation'.format(stik_fmn_sc), 3)
        cmds.setAttr('{0}.floatB'.format(stik_fmn_sc), distance)
        cmds.setAttr('{0}.operation'.format(stik_flcmp_st_sc), 2)
        cmds.setAttr('{0}.operation'.format(stik_fmn_start_sc_fin), 2)
        cmds.setAttr('{0}.operation'.format(stik_fmn_mid_sc_fin), 2)

        # Scale connect
        cmds.connectAttr('{0}.floatA'.format(stik_flc), '{0}.floatA'.format(stik_flcmp_sc_flx), f=1)
        cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.floatB'.format(stik_flcmp_sc_flx), f=1)
        cmds.connectAttr('{0}.flexible'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_sc_flx), f=1)

        cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.colorIfTrueR'.format(stik_cdn_sc_res), f=1)
        cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.firstTerm'.format(stik_cdn_sc_res), f=1)

        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_flx), '{0}.colorIfFalseR'.format(stik_cdn_sc_res), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_flx), '{0}.secondTerm'.format(stik_cdn_sc_res), f=1)

        cmds.connectAttr('{0}.outColorR'.format(stik_cdn_sc_res), '{0}.floatA'.format(stik_fmn_sc), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_fmn_sc), '{0}.floatB'.format(stik_flcmp_st_sc), f=1)
        cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_st_sc), f=1)

        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_st_sc), '{0}.floatA'.format(stik_fmn_start_sc_fin), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_st_sc), '{0}.floatA'.format(stik_fmn_mid_sc_fin), f=1)

        cmds.connectAttr('{0}.outFloat'.format(stik_fmn_start_sc_fin), '{0}.s{1}'.format(jointList[0], self.stretchy_axis), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_fmn_mid_sc_fin), '{0}.s{1}'.format(jointList[1], self.stretchy_axis), f=1)

        cmds.connectAttr('{0}.stretchType'.format(main_ctrl), '{0}.inputX'.format(stik_rev_sc_typ), f=1)
        cmds.connectAttr('{0}.outputX'.format(stik_rev_sc_typ), '{0}.factor'.format(stik_flcmp_sc_typ), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_typ), '{0}.nodeState'.format(stik_fmn_start_sc_fin), f=1)
        cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_typ), '{0}.nodeState'.format(stik_fmn_mid_sc_fin), f=1)

        cmds.connectAttr('{0}.output'.format(stik_adl_start_nu), '{0}.floatB'.format(stik_fmn_start_sc_fin), f=1)
        cmds.connectAttr('{0}.output'.format(stik_adl_mid_nu), '{0}.floatB'.format(stik_fmn_mid_sc_fin), f=1)

        # hide channelbox
        for st_node in stretch_nodes:
            cmds.setAttr('{0}.ihi'.format(st_node), 0)

    # create_stretch(default_reverse=False)

    # def create_softik(self):
    #     if self.ik_main_pac:
    #         cmds.delete(self.ik_main_pac)
    #     self.soft_ik_loc = create_softik(ik_ctrl=self.ik_main_ctrl_object.nodes[-1], ikhandle=self.ikh)

    def create_ikSpline_for_fk(self):
        # segment fk
        seg_fk = brFk.Fk(module=self.module,
                         side=self.side,
                         rig_joints_parent=self.rig_joints_parent,
                         rig_ctrls_parent=self.rig_ctrls_parent,
                         joints=self.ik_joints,
                         shape='cube',
                         axis=[0,0,0],
                         scale=self.ik_main_scale / 2,
                         prefix='SEG_FK_',
                         offsets_type='joint',
                         override_offsets=['_SCL'],
                         scale_constraint=True,
                         decompose_scl_rot_constraint=False)

        [self.trs_objects.append(trs_object) for trs_object in seg_fk.trs_objects]
        # for trs_object in seg_fk.trs_objects:
        #     try:
        #         cmds.parent(trs_object.nodes[0], self.trs_ctrl_ik.nodes[-1])
        #     except:
        #         pass

        top_fk_trs_object = seg_fk.trs_objects[0]

        ik_scale_con_jnts = []
        for i, (ik_jnt, trs_object) in enumerate(zip(self.ik_joints, seg_fk.trs_objects)):
            self.ik_spline_fk_ctrls.append(trs_object.nodes[-1])

            cmds.makeIdentity(trs_object.nodes[0], apply=True, t=True, r=True, s=True, n=False, pn=True)

            cmds.connectAttr(ik_jnt+'.r', trs_object.nodes[0]+'.r', f=True)
            cmds.connectAttr(ik_jnt+'.s', trs_object.nodes[0]+'.s', f=True)
            cmds.connectAttr(ik_jnt+'.shear', trs_object.nodes[0]+'.shear', f=True)

            cmds.connectAttr(trs_object.nodes[0]+'.s', trs_object.nodes[1]+'.s', f=True)

            # children = cmds.listRelatives(trs_object.nodes[0], c=True, f=True) or list()
            #
            # ik_scale_con_jnt = cmds.createNode('joint', n='{}_SCL_CON'.format(ik_jnt), ss=True)
            # cmds.matchTransform(ik_scale_con_jnt, ik_jnt)
            # cmds.parent(ik_scale_con_jnt, trs_object.nodes[1])
            #
            # cmds.makeIdentity(ik_scale_con_jnt, apply=True, t=True, r=True, s=True, n=False, pn=True)
            #
            # if children:
            #     for c in children:
            #         cmds.parent(c, ik_scale_con_jnt)
            #
            # cmds.connectAttr(ik_jnt+'.r', ik_scale_con_jnt+'.r', f=True)
            # cmds.connectAttr(ik_jnt+'.s', ik_scale_con_jnt+'.s', f=True)
            # # cmds.connectAttr(ik_jnt+'.shear', ik_scale_con_jnt+'.shear', f=True)
            #
            if ik_scale_con_jnts:
                cmds.connectAttr(ik_scale_con_jnts[i-1]+'.s', trs_object.nodes[0]+'.inverseScale', f=True)

            ik_scale_con_jnts.append(trs_object.nodes[0])

        self.ik_spline_fkik_jnts = seg_fk.jnt_object.nodes

        # # roll fk
        # roll_fk = brFk.Fk(module=self.module,
        #                  side=self.side,
        #                  rig_joints_parent=self.rig_joints_parent,
        #                  rig_ctrls_parent=self.rig_ctrls_parent,
        #                  joints=self.ik_joints,
        #                  shape='cylinder',
        #                  axis=self.roll_fk_ctrl_axis,
        #                  scale=self.ik_main_scale / 1.2,
        #                  prefix='ROLL_')

        # [self.trs_objects.append(trs_object) for trs_object in seg_fk.trs_objects]

        # # self.ik_spline_fkik_jnts = roll_fk.jnt_object.nodes

        # roll_fk_ctrl = None
        # roll_fk_length = len(roll_fk.trs_objects)
        # for i, (seg_trs_object, roll_trs_object) in enumerate(zip(seg_fk.trs_objects, roll_fk.trs_objects)):
        #     try:
        #         cmds.parent(roll_trs_object.nodes[0], self.trs_ctrl_ik.nodes[-1])
        #     except:
        #         pass

        #     cmds.parentConstraint(seg_trs_object.nodes[-1], roll_trs_object.nodes[0], w=True, mo=True)

        #     if roll_fk_ctrl:
        #         for j in range(roll_fk_length - i):
        #             roll_space_parent = roll_fk.trs_objects[roll_fk_length-(j+1)].nodes[0]

        #             roll_space = brTrs.create_transforms(nodes=['PARENT_{}_GRP'.format(str(i).zfill(2)), roll_fk.trs_objects[roll_fk_length-(j+1)].nodes[1]], offsets=True,
        #                                 prefix=None, suffix=None, replace=None)

        #             cmds.parent(roll_space.nodes[0], roll_space_parent)
        #             cmds.parent(roll_space.nodes[1], roll_space.nodes[0])

        #             cmds.connectAttr(roll_fk_ctrl+'.r'+self.roll_fk_axis, roll_space.nodes[0]+'.r'+self.roll_fk_axis, f=True)

        #         roll_fk_spaces = cmds.listRelatives(roll_trs_object.nodes[0], c=True)
        #         roll_fk_spaces.sort()
        #         roll_fk_parent = None
        #         for rfs in roll_fk_spaces:
        #             if roll_fk_parent:
        #                 cmds.parent(rfs, roll_fk_parent)
        #             roll_fk_parent = rfs

        #     roll_fk_ctrl = roll_trs_object.nodes[-1]

    def create_ikSpline_sineDeformer(self):
        type = 'sine'
        nonLinDef = cmds.nonLinear(self.ik_spline_crv, type=type, n=type.upper()+'_'+self.ik_spline_crv)
        cmds.setAttr(nonLinDef[0]+'.dropoff', 1)
        aim_con = cmds.aimConstraint(self.ik_main_ctrl_object.nodes[-1], nonLinDef[1], aimVector=[0,1,0], upVector=[0,0,1], worldUpType='vector', worldUpVector=[0,1,0])[0]
        cmds.delete(aim_con)

        self.draw.create_curve(name=nonLinDef[0] + '_CURVE', shape='sphere', axis=[0,0,0], scale=self.ik_main_scale / 1.5)
        self.draw.joint_shape()

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
        self.trs_objects.append(self.trs_object)

        cmds.parent(self.ik_spline_sine_ctrl.nodes[0], self.ik_base_ctrl_object.nodes[-1])
        cmds.parent(nonLinDef[1], self.trs_module_ik.nodes[-1])
        cmds.parentConstraint(self.ik_spline_sine_ctrl.nodes[-1], nonLinDef[1], w=True)


    def connection(self):
        if not self.solver in ['ikSplineSolver']:
            # base
            ik_base_dcmx = cmds.createNode('decomposeMatrix', n=self.ik_base_ctrl_object.nodes[-1]+'_DCMX', ss=True)
            cmds.connectAttr(self.ik_base_ctrl_object.nodes[-1]+'.worldMatrix[0]', ik_base_dcmx+'.inputMatrix', f=True)
            cmds.connectAttr(ik_base_dcmx+'.outputTranslate', self.ik_joints[0]+'.t', f=True)

            # cmds.pointConstraint(self.ik_base_ctrl_object.nodes[-1], self.ik_joints[0], w=True)

            # main
            ikh_mmx = cmds.createNode('multMatrix', n=self.ikh+'_MMX', ss=True)
            ikh_dcmx = cmds.createNode('decomposeMatrix', n=self.ikh+'_DCMX', ss=True)

            cmds.connectAttr(self.ikh_const_node+'.worldMatrix[0]', ikh_mmx+'.matrixIn[0]', f=True)
            cmds.connectAttr(self.ikh+'.parentInverseMatrix[0]', ikh_mmx+'.matrixIn[1]', f=True)
            cmds.connectAttr(ikh_mmx+'.matrixSum', ikh_dcmx+'.inputMatrix', f=True)
            cmds.connectAttr(ikh_dcmx+'.outputTranslate', self.ikh+'.t', f=True)

            # self.ik_main_pac = cmds.pointConstraint(self.ik_main_ctrl_object.nodes[-1], self.ikh, w=True)[0]

            # poleVector
            ik_pv_dcmx = cmds.createNode('decomposeMatrix', n=self.ik_pv_ctrl_object.nodes[-1]+'_PV_DCMX', ss=True)
            ik_base_pv_dcmx = cmds.createNode('decomposeMatrix', n=self.ik_base_ctrl_object.nodes[-1]+'_PV_DCMX', ss=True)
            ik_pv_pma = cmds.createNode('plusMinusAverage', n=self.ik_pv_ctrl_object.nodes[-1]+'_PV_PMA', ss=True)
            cmds.setAttr(ik_pv_pma+'.operation', 2)

            cmds.connectAttr(self.ik_pv_ctrl_object.nodes[-1]+'.worldMatrix[0]', ik_pv_dcmx+'.inputMatrix', f=True)
            cmds.connectAttr(ik_pv_dcmx+'.outputTranslate', ik_pv_pma+'.input3D[0]', f=True)

            cmds.connectAttr(self.ik_base_ctrl_object.nodes[-1]+'.worldMatrix[0]', ik_base_pv_dcmx+'.inputMatrix', f=True)
            cmds.connectAttr(ik_base_pv_dcmx+'.outputTranslate', ik_pv_pma+'.input3D[1]', f=True)

            cmds.connectAttr(ik_pv_pma+'.output3D', self.ikh+'.poleVector', f=True)

            # cmds.poleVectorConstraint(self.ik_pv_ctrl_object.nodes[-1], self.ikh, w=True)

            # local
            ori_con = cmds.orientConstraint(self.ik_local_ctrl_object.nodes[-1], self.ik_joints[-1], w=True)[0]
            cmds.setAttr(ori_con+'.interpType', 2)

            self.switch_ori_con = cmds.orientConstraint(self.ik_joints[1], self.ik_local_ctrl_object.nodes[2], w=True, mo=True)[0]
            cmds.setAttr(self.switch_ori_con+'.interpType', 2)
            cmds.disconnectAttr(self.switch_ori_con+'.constraintRotateX', self.ik_local_ctrl_object.nodes[2]+'.rx')
            cmds.disconnectAttr(self.switch_ori_con+'.constraintRotateY', self.ik_local_ctrl_object.nodes[2]+'.ry')
            cmds.disconnectAttr(self.switch_ori_con+'.constraintRotateZ', self.ik_local_ctrl_object.nodes[2]+'.rz')

            # local pairBlend
            pbn = cmds.createNode('pairBlend', n=self.ik_local_ctrl_object.nodes[2]+'_PBN', ss=True)
            cmds.setAttr(pbn+'.rotInterpolation', 1)

            cmds.connectAttr(self.switch_ori_con+'.constraintRotate', pbn+'.inRotate2', f=True)
            cmds.connectAttr(pbn+'.outRotate', self.ik_local_ctrl_object.nodes[2]+'.r', f=True)

            # local pairBlend addAttr
            cmds.addAttr(self.ik_local_ctrl_object.nodes[-1], ln='autoPose', sn='ap', at='double', dv=0, max=1, min=0, k=True)
            cmds.connectAttr(self.ik_local_ctrl_object.nodes[-1]+'.ap', pbn+'.weight', f=True)

    def base_connection(self, to_nodes=None, pos=True, rot=True, scl=True, mo=True, stretchy_axis='x'):
        if not self.solver in ['ikSplineSolver']:
            nodes = self.ik_joints
        else:
            nodes = self.ik_spline_fkik_jnts
        if not to_nodes:
            to_nodes=self.joints

        connects = brConnecter.Connecters(nodes=nodes, to_nodes=to_nodes)
        connects.constraints_nodes(pos, rot, scl, mo, self.stretchy_axis)


def create_softik_locators(start=None, end=None, startMatchFlag=None, endMatchFlag=None):
    startloc = '{0}_softik_st_loc'.format(start)
    endloc = '{0}_softik_ed_loc'.format(end)
    lenloc = '{0}_softik_len_loc'.format(end)

    cmds.spaceLocator(n=startloc)
    cmds.spaceLocator(n=endloc)

    cmds.matchTransform(startloc, start, **startMatchFlag)
    cmds.matchTransform(endloc, end, **endMatchFlag)

    dup_len_loc = cmds.duplicate(endloc, n=lenloc)

    cmds.parent(endloc, startloc)
    cmds.parent(dup_len_loc, startloc)

    return startloc, endloc, dup_len_loc

def get_ikHandle_joints_distance(setHandle):
    endEffector = cmds.ikHandle(setHandle, q=1, endEffector=1)
    jointList = cmds.ikHandle(setHandle, q=1, jointList=1)

    sel = cmds.ls(os=1)
    cmds.select(endEffector)
    endJoint=cmds.pickWalk(d='up')
    endJoint=cmds.pickWalk(d='down')[0]
    cmds.select(sel)

    jointList.append(endJoint)

    length = brCommon.chain_length(chain_list=jointList)

    return sum(length), jointList

def create_softik(ik_ctrl=None, ikhandle=None):
    """
    create_softik(ik_ctrl='A_default_IK_main_CTRL', ikhandle='A_default_IKH')
    """

    listAttrs = cmds.listAttr(ik_ctrl, ud=1)
    if not 'softIk' in listAttrs:
        brCommon.fn_addNumAttr(ik_ctrl, 'softIk', 'sfi', 0, 10, 0)

    listAttrs = cmds.listAttr(ik_ctrl, ud=1)
    if not 'softIkIntensity' in listAttrs:
        brCommon.fn_addNumAttr(ik_ctrl, 'softIkIntensity', 'sfis', 0, 1, 0.1)

    distance, jointList = get_ikHandle_joints_distance(ikhandle)

    startloc, endloc, dup_len_loc = create_softik_locators(start=jointList[0],
                                                           end=jointList[-1],
                                                           startMatchFlag={'pos':True, 'rot':True},
                                                           endMatchFlag={'pos':True, 'rot':True})


    # constraint
    cmds.aimConstraint(ik_ctrl, startloc, weight=1, upVector=(0, 1, 0), worldUpType="vector", aimVector=(1, 0, 0), worldUpVector=(0, 1, 0))
    cmds.pointConstraint(jointList[0], startloc)

    cmds.pointConstraint(ik_ctrl, dup_len_loc)

    cmds.pointConstraint(endloc, ikhandle)


    # create nodes

    e = 2.718281828459045235360287471352

    sub_len_pma = cmds.createNode('plusMinusAverage', n='{0}_softik_{1}'.format(jointList[-1], 'sub_len_pma'))
    cmds.setAttr('{0}.operation'.format(sub_len_pma), 2)
    cmds.setAttr('{0}.input1D[0]'.format(sub_len_pma), distance)
    cmds.connectAttr('{0}.softIk'.format(ik_ctrl), '{0}.input1D[1]'.format(sub_len_pma), f=1)

    sub_dif_pma = cmds.createNode('plusMinusAverage', n='{0}_softik_{1}'.format(jointList[-1], 'sub_dif_pma'))
    cmds.setAttr('{0}.operation'.format(sub_dif_pma), 2)
    cmds.connectAttr('{0}.tx'.format(dup_len_loc[0]), '{0}.input1D[0]'.format(sub_dif_pma), f=1)
    cmds.connectAttr('{0}.output1D'.format(sub_len_pma), '{0}.input1D[2]'.format(sub_dif_pma), f=1)

    neg_mdl = cmds.createNode('multDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'neg_mdl'))
    cmds.setAttr('{0}.input2'.format(neg_mdl), -1)
    cmds.connectAttr('{0}.output1D'.format(sub_dif_pma), '{0}.input1'.format(neg_mdl), f=1)

    dif_mdl = cmds.createNode('multDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'dif_mdl'))
    cmds.setAttr('{0}.input2'.format(dif_mdl), 0.1)
    cmds.connectAttr('{0}.output'.format(neg_mdl), '{0}.input1'.format(dif_mdl), f=1)
    cmds.connectAttr('{0}.softIkIntensity'.format(ik_ctrl), '{0}.input2'.format(dif_mdl), f=1)

    npr_md = cmds.createNode('multiplyDivide', n='{0}_softik_{1}'.format(jointList[-1], 'npr_md'))
    cmds.setAttr('{0}.operation'.format(npr_md), 3)
    cmds.setAttr('{0}.input1X'.format(npr_md), e)
    cmds.connectAttr('{0}.output'.format(dif_mdl), '{0}.input2X'.format(npr_md), f=1)

    calc_pma = cmds.createNode('plusMinusAverage', n='{0}_softik_{1}'.format(jointList[-1], 'calc_pma'))
    cmds.setAttr('{0}.operation'.format(calc_pma), 2)
    cmds.setAttr('{0}.input1D[0]'.format(calc_pma), 1)
    cmds.connectAttr('{0}.outputX'.format(npr_md), '{0}.input1D[1]'.format(calc_pma), f=1)

    calc_mdl = cmds.createNode('multDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'calc_mdl'))
    cmds.connectAttr('{0}.softIk'.format(ik_ctrl), '{0}.input1'.format(calc_mdl), f=1)
    cmds.connectAttr('{0}.output1D'.format(calc_pma), '{0}.input2'.format(calc_mdl), f=1)

    calc_adl = cmds.createNode('addDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'calc_adl'))
    cmds.connectAttr('{0}.output1D'.format(sub_len_pma), '{0}.input1'.format(calc_adl), f=1)
    cmds.connectAttr('{0}.output'.format(calc_mdl), '{0}.input2'.format(calc_adl), f=1)

    flw_ikh_pos_cdn = cmds.createNode('condition', n='{0}_softik_{1}'.format(jointList[-1], 'flw_ikh_pos_cdn'))
    cmds.connectAttr('{0}.softIk'.format(ik_ctrl), '{0}.firstTerm'.format(flw_ikh_pos_cdn), f=1)
    cmds.connectAttr('{0}.tx'.format(dup_len_loc[0]), '{0}.colorIfTrueR'.format(flw_ikh_pos_cdn), f=1)
    cmds.connectAttr('{0}.output'.format(calc_adl), '{0}.colorIfFalseR'.format(flw_ikh_pos_cdn), f=1)


    effect_cdn = cmds.createNode('condition', n='{0}_softik_{1}'.format(jointList[-1], 'effect_cdn'))
    cmds.setAttr('{0}.operation'.format(effect_cdn), 2)

    cmds.connectAttr('{0}.translateX'.format(dup_len_loc[0]), '{0}.colorIfFalseR'.format(effect_cdn), f=1)
    cmds.connectAttr('{0}.translateX'.format(dup_len_loc[0]), '{0}.firstTerm'.format(effect_cdn), f=1)

    cmds.connectAttr('{0}.output1D'.format(sub_len_pma), '{0}.secondTerm'.format(effect_cdn), f=1)
    cmds.connectAttr('{0}.outColorR'.format(flw_ikh_pos_cdn), '{0}.colorIfTrueR'.format(effect_cdn), f=1)

    cmds.connectAttr('{0}.outColorR'.format(effect_cdn), '{0}.translateX'.format(endloc), f=1)

    cmds.connectAttr('{0}.ty'.format(dup_len_loc[0]), '{0}.ty'.format(endloc), f=1)
    cmds.connectAttr('{0}.tz'.format(dup_len_loc[0]), '{0}.tz'.format(endloc), f=1)

    return startloc

def add_roll(space=None, ctrl=None, roll_attr=None, space_at=None,
            inputMin=0, inputMax=0, outputMin=0, outputMax=0):
    if not cmds.objExists(ctrl+'.'+roll_attr):
        cmds.addAttr(ctrl, ln=roll_attr, at='double', dv=0, max=10, min=-10, k=True)

    space_rmv = cmds.createNode('remapValue', n=space+'_RMV', ss=True)
    cmds.setAttr(space_rmv+'.inputMin', inputMin)
    cmds.setAttr(space_rmv+'.inputMax', inputMax)
    cmds.setAttr(space_rmv+'.outputMin', outputMin)
    cmds.setAttr(space_rmv+'.outputMax', outputMax)

    cmds.connectAttr(ctrl+'.'+roll_attr, space_rmv+'.inputValue', f=True)
    cmds.connectAttr(space_rmv+'.outValue', space+'.'+space_at, f=True)

def create_roll(in_piv = 'in_piv',
                out_piv = 'out_piv',
                heel_piv = 'heel_piv',
                toe_piv = 'toe_piv',
                ball = 'Character1_LeftToeBase',
                ankle = 'Character1_LeftFoot',
                ik_ctrl = 'IK_Character1_LeftFoot_MAIN_CTRL',
                roll_parent = 'IK_Character1_LeftFoot_LOCAL_CTRL',
                foot_roll_joints = ['left_ankle', 'left_ball'],
                create_foot_roll_end = True
                ):
    ball_piv = cmds.spaceLocator(n='ball_piv')[0]
    cmds.matchTransform(ball_piv, ball, pos=True, rot=False, scl=False)

    ankle_piv = cmds.spaceLocator(n='ankle_piv')[0]
    cmds.matchTransform(ankle_piv, ankle, pos=True, rot=False, scl=False)

    toe_piv_sweivel = cmds.spaceLocator(n=toe_piv+'_sweivel')[0]
    cmds.matchTransform(toe_piv_sweivel, toe_piv, pos=True, rot=False, scl=False)

    ball_sweivel = cmds.spaceLocator(n=ball+'_sweivel')[0]
    cmds.matchTransform(ball_sweivel, ball, pos=True, rot=False, scl=False)

    roll_list = [
        toe_piv_sweivel,
        ball_sweivel,
        heel_piv,
        in_piv,
        out_piv,
        toe_piv,
        ball_piv,
        ankle_piv
    ]

    roll_jnts = []
    parent = None
    for n in roll_list:
        roll_jnt = cmds.createNode('joint', n=n+'_rot', ss=True)
        roll_jnts.append(roll_jnt)
        cmds.matchTransform(roll_jnt, n, pos=True, rot=False, scl=False)
        if parent:
            cmds.parent(roll_jnt, parent)

        parent = roll_jnt

    cmds.makeIdentity(roll_jnts[0], apply=True, t=True, r=True, s=True, n=False, pn=True)

    # create ctrls
    roll_fk = brFk.Fk(module='roll',
                side='Dummy',
                rig_joints_parent=None,
                rig_ctrls_parent=roll_parent,
                rig_ctrls_parent_const=None,
                joints=roll_jnts,
                namespace=None,
                shape='double_circle_locator',
                axis=[0,0,0],
                scale=1,
                scale_step=0,
                prefix='ROLL_',
                override_offsets=['GRP', 'OFFSET', 'BANK', 'ROLL', 'SWIVEL', 'BEND'])

    # foot roll
    heel_roll_space = roll_fk.trs_objects[2].nodes[2]
    ball_roll_space = roll_fk.trs_objects[6].nodes[2]

    add_roll(space=heel_roll_space, ctrl=ik_ctrl, roll_attr='footRoll', space_at='rx',
            inputMin=0, inputMax=-10, outputMin=0, outputMax=-90)

    add_roll(space=ball_roll_space, ctrl=ik_ctrl, roll_attr='footRoll', space_at='rx',
            inputMin=0, inputMax=10, outputMin=0, outputMax=90)


    # banking
    in_roll_space = roll_fk.trs_objects[3].nodes[2]
    out_roll_space = roll_fk.trs_objects[4].nodes[2]

    add_roll(space=in_roll_space, ctrl=ik_ctrl, roll_attr='banking', space_at='rz',
            inputMin=0, inputMax=-10, outputMin=0, outputMax=90)

    add_roll(space=out_roll_space, ctrl=ik_ctrl, roll_attr='banking', space_at='rz',
            inputMin=0, inputMax=10, outputMin=0, outputMax=-90)


    # tip
    toe_roll_space = roll_fk.trs_objects[5].nodes[3]

    add_roll(space=toe_roll_space, ctrl=ik_ctrl, roll_attr='tip', space_at='rx',
            inputMin=-10, inputMax=10, outputMin=-90, outputMax=90)

    # heel
    heel_roll_space = roll_fk.trs_objects[2].nodes[3]

    add_roll(space=heel_roll_space, ctrl=ik_ctrl, roll_attr='heel', space_at='rx',
            inputMin=-10, inputMax=10, outputMin=90, outputMax=-90)


    # heel
    heel_sweivel_space = roll_fk.trs_objects[2].nodes[4]

    add_roll(space=heel_sweivel_space, ctrl=ik_ctrl, roll_attr='heelSweivel', space_at='ry',
            inputMin=-10, inputMax=10, outputMin=-90, outputMax=90)


    # ball
    ball_sweivel_space = roll_fk.trs_objects[1].nodes[4]

    add_roll(space=ball_sweivel_space, ctrl=ik_ctrl, roll_attr='ballSweivel', space_at='ry',
            inputMin=-10, inputMax=10, outputMin=-90, outputMax=90)


    # tip
    toe_sweivel_space = roll_fk.trs_objects[0].nodes[4]

    add_roll(space=toe_sweivel_space, ctrl=ik_ctrl, roll_attr='tipSweivel', space_at='ry',
            inputMin=-10, inputMax=10, outputMin=-90, outputMax=90)

    # ankle
    ankle_sweivel_space = roll_fk.trs_objects[6].nodes[4]

    add_roll(space=ankle_sweivel_space, ctrl=ik_ctrl, roll_attr='ankleSweivel', space_at='ry',
            inputMin=-10, inputMax=10, outputMin=-90, outputMax=90)

    # ankle bend
    ankle_bend_space = roll_fk.trs_objects[6].nodes[5]

    add_roll(space=ankle_bend_space, ctrl=ik_ctrl, roll_attr='ankleBend', space_at='rx',
            inputMin=-10, inputMax=10, outputMin=-90, outputMax=90)


    # foot roll ik
    ball = foot_roll_joints[-1]
    ball_wt = cmds.xform(ball, q=True, t=True, ws=True)
    toe_wt = cmds.xform(toe_piv, q=True, t=True, ws=True)

    if create_foot_roll_end:
        ball_end = cmds.createNode('joint', n=ball+'_END', ss=True)
        cmds.matchTransform(ball_end, ball, pos=True, rot=True, scl=False)
        cmds.xform(ball_end, t=[0, 0, toe_wt[2]-ball_wt[2]], r=True, ws=True)
        cmds.parent(ball_end, ball)
        foot_roll_joints.append(ball_end)

    else:
        ball_end = foot_roll_joints[-1]

    foot_roll_prefix = 'IK_FOOT_ROLL_'
    jnt_object = brJnt.create_joints(namespace=None,
                                    nodes=foot_roll_joints,
                                    prefix=foot_roll_prefix,
                                    suffix=None,
                                    replace=['_copy', ''])

    for node in jnt_object.node_list:
        node.freezeTransform()
        node.set_preferredAngle()
        node.get_values()

    # ball piv ctrlに下のball ikhを入れる
    ball_piv_ctrl = roll_fk.trs_objects[6].nodes[-1]
    ball_ikh = cmds.ikHandle(n=jnt_object.nodes[1]+'_IKH',
                            sj=jnt_object.nodes[0],
                            ee=jnt_object.nodes[1],
                            sol='ikSCsolver',
                            s='sticky')[0]
    cmds.parent(ball_ikh, ball_piv_ctrl)

    # toe piv ctrlの中にtoe ctrlのgrpごと入れて下のball end ikhを入れる
    ball_end_ikh = cmds.ikHandle(n=jnt_object.nodes[2]+'_IKH',
                            sj=jnt_object.nodes[1],
                            ee=jnt_object.nodes[2],
                            sol='ikSCsolver',
                            s='sticky')

    # roll ik jointsのペアレント
    ankle_piv_ctrl = roll_fk.trs_objects[-1].nodes[-1]
    cmds.parent(jnt_object.nodes[0], ankle_piv_ctrl)

    # ikhandleコンスト用のノードをankle_piv_rot_ctrlに入れてもいいが、
    # IK_left_ankle_LOCAL_CTRLのSPACEのコンストとAutoPoseをオフにしておく必要がある
