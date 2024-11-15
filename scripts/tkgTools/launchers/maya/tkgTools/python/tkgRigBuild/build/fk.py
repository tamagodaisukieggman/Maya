# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.libs.control.ctrl as tkgCtrl
reload(tkgChain)
reload(tkgCtrl)

class Fk:
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 gimbal=None,
                 offset=None,
                 pad="auto",
                 fk_ctrl_axis='x',
                 fk_ctrl_edge_axis='-x',
                 ctrl_scale=1,
                 ctrl_color=[0.1, 0.4, 0.8],
                 remove_last=True,
                 add_joints=True,
                 fk_shape="cube",
                 gimbal_shape="circle",
                 offset_shape="square"):
        self.side = side
        self.part = part
        self.base_name = self.side + "_" + self.part

        self.guide_list = guide_list
        self.gimbal = gimbal
        self.offset = offset
        self.pad = pad
        self.fk_ctrl_axis = fk_ctrl_axis
        self.fk_ctrl_edge_axis = fk_ctrl_edge_axis
        self.ctrl_scale = ctrl_scale
        self.ctrl_color = ctrl_color
        self.remove_last = remove_last
        self.add_joints = add_joints
        self.fk_shape = fk_shape
        self.gimbal_shape = gimbal_shape
        self.offset_shape = offset_shape

        self.fk_top = None

        self.part_fk_main_ctrls = []
        self.part_fk_gimbal_ctrls = []
        self.part_fk_offset_ctrls = []

        if self.pad == "auto":
            self.pad = len(str(len(self.guide_list))) + 1

        if self.guide_list:
            if not isinstance(self.guide_list, list):
                self.guide_list = [self.guide_list]

    def build_fk(self):
        self.build_fk_controls()

        if self.add_joints:
            self.build_fk_chain()

        if self.remove_last:
            cmds.delete(self.fk_ctrls[-1].top)

    def build_fk_controls(self):
        self.fk_ctrls = []
        self.gim_ctrls = []
        self.off_ctrls = []

        for i, pose in enumerate(self.guide_list):
            num = str(i + 1).zfill(self.pad)
            if pose == self.guide_list[0]:
                par = None
            fk = tkgCtrl.Control(parent=par,
                                shape=self.fk_shape,
                                prefix=self.side,
                                suffix="CTRL",
                                name=self.part + "_" + num + "_fk",
                                axis=self.fk_ctrl_axis,
                                group_type="main",
                                rig_type=self.side+'_'+self.part+"Fk",
                                position=pose,
                                rotation=pose,
                                ctrl_scale=self.ctrl_scale,
                                ctrl_color=self.ctrl_color,
                                edge_axis=self.fk_ctrl_edge_axis)

            if not self.fk_top:
                self.fk_top = fk.top

            self.part_fk_main_ctrls.append(fk.ctrl)
            par = fk.ctrl
            self.fk_ctrls.append(fk)
            self.output_ctrls = self.fk_ctrls

            if self.gimbal:
                gim = tkgCtrl.Control(parent=par,
                                     shape=self.gimbal_shape,
                                     prefix=self.side,
                                     suffix="CTRL",
                                     name=self.part + "_" + num + "_gimbal",
                                     axis=self.fk_ctrl_axis,
                                     group_type="main",
                                     rig_type=self.side+'_'+self.part+"FkGimbal",
                                     position=pose,
                                     rotation=pose,
                                     ctrl_scale=self.ctrl_scale * 0.8,
                                     ctrl_color=self.ctrl_color)
                self.part_fk_gimbal_ctrls.append(gim.ctrl)
                par = gim.ctrl
                self.gim_ctrls.append(gim)
                self.output_ctrls = self.gim_ctrls

            if self.offset:
                off = tkgCtrl.Control(parent=par,
                                     shape=self.offset_shape,
                                     prefix=self.side,
                                     suffix="CTRL",
                                     name=self.part + "_" + num + "_offset",
                                     axis=self.fk_ctrl_axis,
                                     group_type="main",
                                     rig_type=self.side+'_'+self.part+"FkOffset",
                                     position=pose,
                                     rotation=pose,
                                     ctrl_scale=self.ctrl_scale * 0.55,
                                     ctrl_color=self.ctrl_color)
                self.part_fk_offset_ctrls.append(off.ctrl)
                self.off_ctrls.append(off)
                self.output_ctrls = self.off_ctrls

    def build_fk_chain(self):
        transform_list = [oc.ctrl for oc in self.output_ctrls]
        self.fk_chain = tkgChain.Chain(transform_list=transform_list,
                                      prefix=self.side,
                                      suffix="fk_JNT",
                                      name=self.part)
        self.fk_chain.create_from_transforms(parent_constraint=True,
                                             scale_constraint=False)
        self.fk_joints = self.fk_chain.joints
