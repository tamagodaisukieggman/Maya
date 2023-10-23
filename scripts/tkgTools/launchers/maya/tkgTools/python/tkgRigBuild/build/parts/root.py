# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.libs.control.ctrl as tkgCtrl
reload(tkgModule)
reload(tkgChain)
reload(tkgCtrl)

class Root(tkgModule.RigModule):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=None,
                 ctrl_color=[0.199, 0.108, 0.315],
                 global_name='global',
                 global_shape="gnomon",
                 root_01_name='root_01',
                 root_02_name='root_02',
                 root_shape="pacman",
                 root_move_name='root_move',
                 root_move_shape='arrow_one_way_z',
                 model_path=None,
                 model_namespace=None,
                 guide_path=None):
        super(Root, self).__init__(side=side,
                                   part=part,
                                   guide_list=guide_list,
                                   ctrl_scale=ctrl_scale,
                                   model_path=model_path,
                                   model_namespace=model_namespace,
                                   guide_path=guide_path)

        if self.guide_list:
            self.root_pose = self.guide_list[0]
        else:
            self.root_pose = (0,0,0)

        self.ctrl_color = ctrl_color

        self.global_name = global_name
        self.global_shape = global_shape
        self.root_01_name = root_01_name
        self.root_02_name = root_02_name
        self.root_shape = root_shape
        self.root_move_name = root_move_name
        self.root_move_shape = root_move_shape

        self.create_module() # buildPartモジュールで使うとき

    def create_module(self):
        super(Root, self).create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()

    def control_rig(self):
        if self.root_pose == (0,0,0):
            group_type = None
        else:
            group_type = 1

        self.global_ctrl = tkgCtrl.Control(parent=self.control_grp,
                                          shape=self.global_shape,
                                          prefix=self.side,
                                          suffix="CTRL",
                                          name=self.global_name,
                                          axis="y",
                                          group_type=group_type,
                                          rig_type=self.global_name,
                                          position=self.root_pose,
                                          rotation=self.root_pose,
                                          ctrl_scale=self.ctrl_scale,
                                          ctrl_color=self.ctrl_color)

        self.root_01 = tkgCtrl.Control(parent=self.global_ctrl.ctrl,
                                          shape=self.root_shape,
                                          prefix=self.side,
                                          suffix="CTRL",
                                          name=self.root_01_name,
                                          axis="y",
                                          group_type="main",
                                          rig_type=self.root_01_name,
                                          position=self.root_pose,
                                          rotation=self.root_pose,
                                          ctrl_scale=self.ctrl_scale * 0.5,
                                          ctrl_color=[0.069, 0.377, 0.694])

        self.root_02 = tkgCtrl.Control(parent=self.root_01.ctrl,
                                          shape=self.root_shape,
                                          prefix=self.side,
                                          suffix="CTRL",
                                          name=self.root_02_name,
                                          axis="y",
                                          group_type="main",
                                          rig_type=self.root_02_name,
                                          position=self.root_pose,
                                          rotation=self.root_pose,
                                          ctrl_scale=self.ctrl_scale * 0.4,
                                          ctrl_color=[0.377, 0.069, 0.694])

        self.root_move = tkgCtrl.Control(parent=self.control_grp,
                                          shape=self.root_move_shape,
                                          prefix=self.side,
                                          suffix="CTRL",
                                          name=self.root_move_name,
                                          axis="y",
                                          group_type="main",
                                          rig_type=self.root_move_name,
                                          position=self.root_pose,
                                          rotation=self.root_pose,
                                          ctrl_scale=self.ctrl_scale,
                                          ctrl_color=[1, 1, 0.24])

    def output_rig(self):
        root_jnt_grp = cmds.group(parent=self.module_grp,
                                  empty=True,
                                  name=self.base_name + "_JNT_GRP")
        cmds.matchTransform(root_jnt_grp, self.root_move.ctrl)
        self.root_jnt = cmds.joint(root_jnt_grp,
                                   name=self.root_move.ctrl.replace("CTRL", "JNT"))

        cmds.parentConstraint(self.root_move.ctrl, self.root_jnt, mo=True)
        cmds.scaleConstraint(self.root_move.ctrl, self.root_jnt, mo=True)

    def skeleton(self):
        self.bind_joints = []
        root_chain = tkgChain.Chain(transform_list=[self.root_jnt],
                             prefix=self.side,
                             suffix="JNT",
                             name=self.part)
        root_chain.create_from_transforms(parent=self.skel, pad=False)
