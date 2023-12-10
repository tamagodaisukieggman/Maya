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
import buildRig.ik as brIk
import buildRig.switch as brSwitch
reload(brCommon)
reload(brNode)
reload(brGrp)
reload(brJnt)
reload(brDraw)
reload(brTrs)
reload(brAim)
reload(brFk)
reload(brIk)
reload(brSwitch)

class Ikfk(brGrp.RigModule):
    def __init__(self,
                 module=None,
                 side=None,
                 ik_rig_joints_parent=None,
                 ik_rig_ctrls_parent=None,
                 ik_joints=None,
                 ik_base_shape='cube',
                 ik_base_axis='x',
                 ik_base_scale=10,
                 ik_main_shape='jack',
                 ik_main_axis='x',
                 ik_main_scale=10,
                 ik_pv_shape='locator_3d',
                 ik_pv_axis='x',
                 ik_pv_scale=10,
                 ik_local_shape='cube',
                 ik_local_axis='x',
                 ik_local_scale=10,
                 ik_solver=1,

                 fk_rig_joints_parent=None,
                 fk_rig_ctrls_parent=None,
                 fk_joints=None,
                 fk_shape='cube',
                 fk_axis='x',
                 fk_scale=10,

                 switch_rig_joints_parent=None,
                 switch_rig_ctrls_parent=None,
                 switch_rig_type='IKFK',
                 switch_joints=None,
                 switch_shape='cube',
                 switch_axis='x',
                 switch_scale=5):
        """
        """
        super(Ikfk, self).__init__(module=module,
                                 side=side)

        # IK module settings
        self.ik_rig_joints_parent = ik_rig_joints_parent
        self.ik_rig_ctrls_parent = ik_rig_ctrls_parent
        self.ik_joints = ik_joints
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
        self.ik_solver = ik_solver

        # FK module settings
        self.fk_rig_joints_parent = fk_rig_joints_parent
        self.fk_rig_ctrls_parent = fk_rig_ctrls_parent
        self.fk_joints = fk_joints
        self.fk_shape = fk_shape
        self.fk_axis = fk_axis
        self.fk_scale = fk_scale

        # Switch module settings
        self.switch_rig_joints_parent = switch_rig_joints_parent
        self.switch_rig_ctrls_parent = switch_rig_ctrls_parent
        self.switch_rig_type = switch_rig_type
        self.switch_joints = switch_joints
        self.switch_shape = switch_shape
        self.switch_axis = switch_axis
        self.switch_scale = switch_scale

        self.create_ikfk_module()

    def create_ikfk_module(self):
        self.create_ik_module()
        self.create_fk_module()
        self.create_switch_module()
        # self.connection()

    def create_ik_module(self):
        self.ik = brIk.Ik(module=self.module,
                     side=self.side,
                     rig_joints_parent=self.ik_rig_joints_parent,
                     rig_ctrls_parent=self.ik_rig_ctrls_parent,
                     joints=self.ik_joints,
                     ik_base_shape=self.ik_base_shape,
                     ik_base_axis=self.ik_base_axis,
                     ik_base_scale=self.ik_base_scale,
                     ik_main_shape=self.ik_main_shape,
                     ik_main_axis=self.ik_main_axis,
                     ik_main_scale=self.ik_main_scale,
                     ik_pv_shape=self.ik_pv_shape,
                     ik_pv_axis=self.ik_pv_axis,
                     ik_pv_scale=self.ik_pv_scale,
                     ik_local_shape=self.ik_local_shape,
                     ik_local_axis=self.ik_local_axis,
                     ik_local_scale=self.ik_local_scale,
                     solver=self.ik_solver)

    def create_fk_module(self):
        self.fk = brFk.Fk(module=self.module,
                     side=self.side,
                     rig_joints_parent=self.fk_rig_joints_parent,
                     rig_ctrls_parent=self.fk_rig_ctrls_parent,
                     joints=self.fk_joints,
                     shape=self.fk_shape,
                     axis=self.fk_axis,
                     scale=self.fk_scale)

    def create_switch_module(self):
        self.switch = brSwitch.Switch(module=self.module,
                 side=self.side,
                 rig_joints_parent=self.switch_rig_joints_parent,
                 rig_ctrls_parent=self.switch_rig_ctrls_parent,
                 rig_type=self.switch_rig_type,
                 joints=self.switch_joints,
                 shape=self.switch_shape,
                 axis=self.switch_axis,
                 scale=self.switch_scale)

    def connection(self):
        pass
