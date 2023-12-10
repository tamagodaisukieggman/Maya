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
                 solver=1):
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

        # Controller
        self.draw = brDraw.Draw()

        self.create_ik_module()

    def create_ik_module(self):
        self.create_joints()
        self.create_ik()
        self.create_ctrls()
        self.create_rig_module()
        self.connection()

    def create_joints(self):
        self.jnt_object = brJnt.create_joints(nodes=self.joints, prefix='IK_', suffix=None, replace=['_copy', ''])
        for node in self.jnt_object.node_list:
            node.freezeTransform()
            node.set_preferredAngle()
            node.get_values()
        self.top_ik_joint_nodes.append(self.jnt_object.node_list[0].full_path.split('|')[1])

    def create_ik(self):
        self.ik_joints = self.jnt_object.nodes
        settings = {
            'name':self.ik_joints[-1] + '_IKH',
            'startJoint':self.ik_joints[0],
            'endEffector':self.ik_joints[-1],
            'sticky':'sticky',
            'solver':self.solver
        }

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

        # local
        self.ik_local = self.jnt_object.node_list[-1]
        self.draw.create_curve(name=self.ik_local.node + '_CURVE', shape=self.ik_local_shape, axis=self.ik_local_axis, scale=self.ik_local_scale)
        cmds.matchTransform(self.draw.curve, self.ik_local.node)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=['_CURVE', '_LOCAL_CTRL'])
        self.trs_objects.append(self.trs_object)
        self.ik_local_ctrl_object = self.trs_object

        cmds.parent(self.ik_local_ctrl_object.nodes[0], self.ik_main_ctrl_object.nodes[-1])

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

    def connection(self):
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
