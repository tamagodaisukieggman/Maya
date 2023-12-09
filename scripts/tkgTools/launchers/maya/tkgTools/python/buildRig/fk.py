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

class Fk(brGrp.RigModule):
    def __init__(self,
                 module=None,
                 side=None,
                 parent_rig_module=True,
                 joints=None,
                 shape='cube',
                 axis='x',
                 scale=5):
        super(Fk, self).__init__(module=module,
                                 side=side)
        self.parent_rig_module = parent_rig_module
        self.joints = joints
        self.shape = shape
        self.axis = axis
        self.scale = scale

        self.jnt_object = None
        self.trs_object = None
        self.trs_objects = []
        self.top_fk_joint_nodes = []
        self.top_fk_ctrl_nodes = []

        # Controller
        self.draw = brDraw.Draw()

        self.create_fk_module()

    def create_fk_module(self):
        self.create_joints()
        self.create_ctrls()
        if self.parent_rig_module:
            self.create_rig_module()

    def create_joints(self):
        self.jnt_object = brJnt.create_joints(nodes=self.joints, prefix='FK_', suffix=None, replace=['_copy', ''])
        for node in self.jnt_object.node_list:
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
        self.trs_module_fk = brTrs.create_transforms(nodes=[self.module_grp, self.module_grp + '_FK'], offsets=False)
        self.trs_ctrl_fk = brTrs.create_transforms(nodes=[self.ctrl_grp, self.ctrl_grp + '_FK'], offsets=False)

        for jnt in self.top_fk_joint_nodes:
            cmds.parent(jnt, self.trs_module_fk.nodes[-1])

        for ctrl in self.top_fk_ctrl_nodes:
            cmds.parent(ctrl, self.trs_ctrl_fk.nodes[-1])
