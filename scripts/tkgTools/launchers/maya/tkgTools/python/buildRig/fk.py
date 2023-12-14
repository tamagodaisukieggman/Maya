# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.connecter as brConnecter
import buildRig.node as brNode
import buildRig.grps as brGrp
import buildRig.joint as brJnt
import buildRig.libs.control.draw as brDraw
import buildRig.transform as brTrs
reload(brConnecter)
reload(brNode)
reload(brGrp)
reload(brJnt)
reload(brDraw)
reload(brTrs)

class Fk(brGrp.RigModule):
    def __init__(self,
                 module=None,
                 side=None,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 joints=None,
                 shape='cube',
                 axis=[0,0,0],
                 scale=5,
                 prefix='FK_'):
        """
        Params:
        module = string<モジュール名を指定する>
        side = string<中央、右、左がわかる識別子を指定する>
        rig_joints_parent = string<ジョイントをペアレントする親を指定する>
        rig_ctrls_parent = string<コントローラをペアレントする親を指定する>
        joints = list[string]<ベースになるジョイントのリストを指定する>
        shape = string<コントローラのタイプを指定する>
        axis = list[float, float, float]
        scale = float<コントローラのサイズを指定する>
        """
        super(Fk, self).__init__(module=module,
                                 side=side)
        self.rig_joints_parent = rig_joints_parent
        self.rig_ctrls_parent = rig_ctrls_parent
        self.joints = joints
        self.shape = shape
        self.axis = axis
        self.scale = scale
        self.prefix = prefix

        self.jnt_object = None
        self.trs_object = None
        self.trs_objects = []
        self.top_fk_joint_nodes = []
        self.top_fk_ctrl_nodes = []

        # Controller
        self.draw = brDraw.Draw()

        # モジュールのノードを追加
        self.trs_module_fk = brTrs.create_transforms(nodes=[self.module_grp, self.module_grp + '_FK'], offsets=False)
        self.trs_ctrl_fk = brTrs.create_transforms(nodes=[self.ctrl_grp, self.ctrl_grp + '_FK'], offsets=False)

        self.create_fk_module()

    def create_fk_module(self):
        self.create_joints()
        self.create_ctrls()
        self.create_rig_module()
        self.connection()

    def create_joints(self):
        self.jnt_object = brJnt.create_joints(nodes=self.joints, prefix=self.prefix, suffix=None, replace=['_copy', ''])
        for node in self.jnt_object.node_list:
            node.freezeTransform()
            node.set_preferredAngle()
            node.get_values()
        self.top_fk_joint_nodes.append(self.jnt_object.node_list[0].full_path.split('|')[1])

    def create_ctrls(self):
        for i, jnt in enumerate(self.jnt_object.node_list):
            self.draw.create_curve(name=jnt.node + '_CURVE', shape=self.shape, axis=self.axis, scale=self.scale)
            cmds.matchTransform(self.draw.curve, jnt.node)
            self.trs_object = brTrs.create_transforms(nodes=['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV', self.draw.curve], offsets=True,
                                                    prefix=None, suffix=None, replace=['_CURVE', '_CTRL'])
            self.trs_objects.append(self.trs_object)
            if jnt.parent:
                parent_ctrl = jnt.parent.split('|')[-1] + '_CTRL'
                if cmds.objExists(parent_ctrl):
                    cmds.parent(self.trs_object.nodes[0], parent_ctrl)

        for trs_object in self.trs_objects:
            for node in trs_object.node_list:
                node.get_values()
            self.top_fk_ctrl_nodes.append(trs_object.node_list[0].full_path.split('|')[1])

        self.top_fk_ctrl_nodes = list(set(self.top_fk_ctrl_nodes))

    def create_rig_module(self):
        # リグ用のジョイントをペアレント化させる
        if not self.rig_joints_parent:
            self.rig_joints_parent = self.trs_module_fk.nodes[-1]

        for jnt in self.top_fk_joint_nodes:
            cmds.parent(jnt, self.rig_joints_parent)

        # コントローラをペアレント化させる
        if not self.rig_ctrls_parent:
            self.rig_ctrls_parent = self.trs_ctrl_fk.nodes[-1]

        for ctrl in self.top_fk_ctrl_nodes:
            cmds.parent(ctrl, self.rig_ctrls_parent)

    def connection(self):
        for ctrl_object, jnt in zip(self.trs_objects, self.jnt_object.nodes):
            ctrl = ctrl_object.nodes[-1]

            """
            splineIKのFKコントローラが機能しないので普通にコンストしてみる
            # pairBlend
            pbn = cmds.createNode('pairBlend', n=jnt+'_PBN', ss=True)

            # setAttr
            cmds.setAttr(pbn+'.rotInterpolation', 1)

            # connectAttr
            cmds.connectAttr(ctrl+'.r', pbn+'.inRotate2', f=True)
            cmds.connectAttr(pbn+'.outRotate', jnt+'.r', f=True)

            cmds.connectAttr(ctrl+'.rotateOrder', jnt+'.rotateOrder', f=True)
            cmds.connectAttr(jnt+'.rotateOrder', pbn+'.rotateOrder', f=True)

            cmds.connectAttr(ctrl+'.s', jnt+'.s', f=True)
            """

            #
            cmds.pointConstraint(ctrl, jnt, w=True)
            cmds.orientConstraint(ctrl, jnt, w=True)

            cmds.connectAttr(ctrl+'.s', jnt+'.s', f=True)
            cmds.connectAttr(ctrl+'.shear', jnt+'.shear', f=True)
            # cmds.scaleConstraint(ctrl, jnt, w=True)

    def base_connection(self, to_nodes=None, pos=True, rot=True, scl=True, mo=True):
        if not to_nodes:
            to_nodes=self.joints

        connects = brConnecter.Connecters(nodes=self.jnt_object.nodes, to_nodes=to_nodes)
        connects.constraints_nodes(pos, rot, scl, mo)
