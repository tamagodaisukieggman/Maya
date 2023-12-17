# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

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
import buildRig.ik as brIk
import buildRig.switch as brSwitch
reload(brCommon)
reload(brConnecter)
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
                 stretchy_axis='x',
                 ik_solver=1,
                 dForwardAxis='-z',
                 dWorldUpAxis='x',
                 roll_fk_axis='x',
                 roll_fk_ctrl_axis=[0,0,0],

                 fk_rig_joints_parent=None,
                 fk_rig_ctrls_parent=None,
                 fk_joints=None,
                 fk_shape='cube',
                 fk_axis='x',
                 fk_scale=10,
                 fk_scale_step=0,

                 switch_rig_joints_parent=None,
                 switch_rig_ctrls_parent=None,
                 switch_rig_type='IKFK',
                 switch_joints=None,
                 switch_shape='switch',
                 switch_axis='x',
                 switch_scale=5):
        """
# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from imp import reload
import traceback

import buildRig.ikfk as brIkfk
reload(brIkfk)


sel = cmds.ls(os=True, type='joint')

try:
    ikfk = brIkfk.Ikfk(module=None,
                     side=None,
                     ik_rig_joints_parent=None,
                     ik_rig_ctrls_parent=None,
                     ik_joints=sel,
                     ik_base_shape='cube',
                     ik_base_axis=[0,0,0],
                     ik_base_scale=1000,
                     ik_main_shape='jack',
                     ik_main_axis=[0,0,0],
                     ik_main_scale=1000,
                     ik_pv_shape='locator_3d',
                     ik_pv_axis=[0,0,0],
                     ik_pv_scale=1000,
                     ik_local_shape='cube',
                     ik_local_axis=[0,0,0],
                     ik_local_scale=700,
                     stretchy_axis='x',
                     ik_solver=1,
                     dForwardAxis='-z',
                     dWorldUpAxis='x',
                     roll_fk_axis='x',
                     roll_fk_ctrl_axis=[0,0,0],

                     fk_rig_joints_parent=None,
                     fk_rig_ctrls_parent=None,
                     fk_joints=sel,
                     fk_shape='cube',
                     fk_axis=[0,0,0],
                     fk_scale=1000,

                     switch_rig_joints_parent=None,
                     switch_rig_ctrls_parent=None,
                     switch_rig_type='IKFK',
                     switch_joints=sel,
                     switch_shape='switch',
                     switch_axis=[0,0,0],
                     switch_scale=500)
except:
    print(traceback.format_exc())
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
        self.stretchy_axis = stretchy_axis
        self.ik_solver = ik_solver
        self.dForwardAxis = dForwardAxis
        self.dWorldUpAxis = dWorldUpAxis
        self.roll_fk_axis = roll_fk_axis
        self.roll_fk_ctrl_axis = roll_fk_ctrl_axis

        # FK module settings
        self.fk_rig_joints_parent = fk_rig_joints_parent
        self.fk_rig_ctrls_parent = fk_rig_ctrls_parent
        self.fk_joints = fk_joints
        self.fk_shape = fk_shape
        self.fk_axis = fk_axis
        self.fk_scale = fk_scale
        self.fk_scale_step = fk_scale_step

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
                     stretchy_axis=self.stretchy_axis,
                     solver=self.ik_solver,
                     dForwardAxis=self.dForwardAxis,
                     dWorldUpAxis=self.dWorldUpAxis,
                     roll_fk_axis = self.roll_fk_axis,
                     roll_fk_ctrl_axis = self.roll_fk_ctrl_axis)

    def create_fk_module(self):
        self.fk = brFk.Fk(module=self.module,
                     side=self.side,
                     rig_joints_parent=self.fk_rig_joints_parent,
                     rig_ctrls_parent=self.fk_rig_ctrls_parent,
                     joints=self.fk_joints,
                     shape=self.fk_shape,
                     axis=self.fk_axis,
                     scale=self.fk_scale,
                     scale_step=self.fk_scale_step)

    def create_switch_module(self):
        self.switch = brSwitch.Switch(module=self.module,
                 side=self.side,
                 rig_joints_parent=self.switch_rig_joints_parent,
                 rig_ctrls_parent=self.switch_rig_ctrls_parent,
                 rig_type=self.switch_rig_type,
                 joints=self.switch_joints,
                 shape=self.switch_shape,
                 axis=self.switch_axis,
                 scale=self.switch_scale,
                 switch_fk_joints=self.fk.jnt_object.nodes,
                 switch_fk_ctrls=self.fk.trs_objects,
                 switch_ik_joints=self.ik.jnt_object.nodes,
                 switch_ik_ctrls=self.ik.trs_objects)

    def connection(self):
        pass

    def base_connection(self, to_nodes=None, pos=True, rot=True, scl=True, mo=True):
        nodes = self.switch.jnt_object.nodes
        if not to_nodes:
            to_nodes=self.switch_joints

        connects = brConnecter.Connecters(nodes=nodes, to_nodes=to_nodes)
        connects.constraints_nodes(pos, rot, scl, mo)
