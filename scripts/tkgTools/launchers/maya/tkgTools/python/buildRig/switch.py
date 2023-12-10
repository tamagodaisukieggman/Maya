# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.node as brNode
import buildRig.grps as brGrp
import buildRig.joint as brJnt
import buildRig.libs.control.draw as brDraw
import buildRig.transform as brTrs
reload(brNode)
reload(brGrp)
reload(brJnt)
reload(brDraw)
reload(brTrs)

class Switch(brGrp.RigModule):
    def __init__(self,
                 module=None,
                 side=None,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 rig_type='IKFK',
                 joints=None,
                 shape='switch',
                 axis='x',
                 scale=5,
                 switch_fk_joints=None,
                 switch_fk_ctrls=None,
                 switch_ik_joints=None,
                 switch_ik_ctrls=None):
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
        """
        super(Switch, self).__init__(module=module,
                                 side=side)
        self.rig_joints_parent = rig_joints_parent
        self.rig_ctrls_parent = rig_ctrls_parent
        self.rig_type = rig_type
        self.joints = joints
        self.shape = shape
        self.axis = axis
        self.scale = scale

        self.jnt_object = None
        self.trs_object = None
        self.trs_objects = []
        self.top_switch_joint_nodes = []
        self.top_switch_ctrl_nodes = []

        self.switch_fk_joints = switch_fk_joints
        self.switch_fk_ctrls = switch_fk_ctrls
        self.switch_ik_joints = switch_ik_joints
        self.switch_ik_ctrls = switch_ik_ctrls

        # Controller
        self.draw = brDraw.Draw()

        self.create_switch_module()

    def create_switch_module(self):
        self.create_joints()
        self.create_ctrls()
        self.create_rig_module()
        self.get_ikfk_shapes()
        self.connection()

    def create_joints(self):
        self.jnt_object = brJnt.create_joints(nodes=self.joints, prefix=self.rig_type + '_SWITCH_', suffix=None, replace=['_copy', ''])
        for node in self.jnt_object.node_list:
            node.freezeTransform()
            node.set_preferredAngle()
            node.get_values()
        self.top_switch_joint_nodes.append(self.jnt_object.node_list[0].full_path.split('|')[1])

    def create_ctrls(self):
        # switch
        self.switch = self.jnt_object.node_list[-1]
        self.draw.create_curve(name=self.switch.node + '_CURVE', shape=self.shape, axis=self.axis, scale=self.scale)
        cmds.matchTransform(self.draw.curve, self.switch.node, pos=True, rot=False, scl=False)
        self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                prefix=None, suffix=None, replace=['_CURVE', self.rig_type + '_SWITCH_CTRL'])
        self.trs_objects.append(self.trs_object)
        self.switch_ctrl_object = self.trs_object

        for trs_object in self.trs_objects:
            for node in trs_object.node_list:
                node.get_values()
            self.top_switch_ctrl_nodes.append(trs_object.node_list[0].full_path.split('|')[1])

        self.top_switch_ctrl_nodes = list(set(self.top_switch_ctrl_nodes))

    def create_rig_module(self):
        self.trs_module_switch = brTrs.create_transforms(nodes=[self.module_grp, self.module_grp + '_' + self.rig_type], offsets=False)
        self.trs_ctrl_switch = brTrs.create_transforms(nodes=[self.ctrl_grp, self.ctrl_grp + '_' + self.rig_type], offsets=False)

        # リグ用のジョイントをペアレント化させる
        if not self.rig_joints_parent:
            self.rig_joints_parent = self.trs_module_switch.nodes[-1]

        for jnt in self.top_switch_joint_nodes:
            cmds.parent(jnt, self.rig_joints_parent)

        # コントローラをペアレント化させる
        if not self.rig_ctrls_parent:
            self.rig_ctrls_parent = self.trs_ctrl_switch.nodes[-1]

        for ctrl in self.top_switch_ctrl_nodes:
            cmds.parent(ctrl, self.rig_ctrls_parent)

    def get_ikfk_shapes(self):
        self.fk_ctrl_shapes = []
        self.ik_ctrl_shapes = []
        for fk_trs_object in self.switch_fk_ctrls:
            [node.get_values() for node in fk_trs_object.node_list]
            for fk_node in fk_trs_object.node_list:
                if fk_node.shapes:
                    for fks in fk_node.shapes:
                        if not fks in self.fk_ctrl_shapes:
                            self.fk_ctrl_shapes.append(fks)

        for ik_trs_object in self.switch_ik_ctrls:
            [node.get_values() for node in ik_trs_object.node_list]
            for ik_node in ik_trs_object.node_list:
                if ik_node.shapes:
                    for iks in ik_node.shapes:
                        if not iks in self.ik_ctrl_shapes:
                            self.ik_ctrl_shapes.append(iks)

    def connection(self):
        cmds.pointConstraint(self.jnt_object.nodes[-1], self.top_switch_ctrl_nodes[0], w=True)

        cmds.addAttr(self.switch_ctrl_object.nodes[-1], ln='switch', sn='swh', at='double', dv=0, max=1, min=0, k=True)

        for i, (fk_jnt, ik_jnt, switch_jnt) in enumerate(zip(self.switch_fk_joints, self.switch_ik_joints, self.jnt_object.nodes)):
            pac = cmds.parentConstraint(fk_jnt, switch_jnt, w=True)[0]
            cmds.parentConstraint(ik_jnt, switch_jnt, w=True)[0]
            cmds.setAttr(pac+'.interpType', 2)

            # IK connection
            cmds.connectAttr(self.switch_ctrl_object.nodes[-1]+'.swh', pac+'.w1', f=True)
            [cmds.connectAttr(pac+'.w1', s+'.v', f=True) for s in self.ik_ctrl_shapes]

            # FK connection
            rev = cmds.createNode('reverse', n=switch_jnt + '_REV', ss=True)
            cmds.connectAttr(self.switch_ctrl_object.nodes[-1]+'.swh', rev+'.inputX', f=True)
            cmds.connectAttr(rev+'.outputX', pac+'.w0', f=True)
            [cmds.connectAttr(pac+'.w0', s+'.v', f=True) for s in self.fk_ctrl_shapes]

        # for ctrl_object, jnt in zip(self.trs_objects, self.jnt_object.nodes):
        #     ctrl = ctrl_object.nodes[-1]
        #
        #     # pairBlend
        #     pbn = cmds.createNode('pairBlend', n=jnt+'_PBN', ss=True)
        #
        #     # setAttr
        #     cmds.setAttr(pbn+'.rotInterpolation', 1)
        #
        #     # connectAttr
        #     cmds.connectAttr(ctrl+'.r', pbn+'.inRotate2', f=True)
        #     cmds.connectAttr(pbn+'.outRotate', jnt+'.r', f=True)
        #
        #     cmds.connectAttr(ctrl+'.rotateOrder', jnt+'.rotateOrder', f=True)
        #     cmds.connectAttr(jnt+'.rotateOrder', pbn+'.rotateOrder', f=True)
        #
        #     cmds.connectAttr(ctrl+'.s', jnt+'.s', f=True)
        #
        #     #
        #     cmds.pointConstraint(ctrl, jnt, w=True)
