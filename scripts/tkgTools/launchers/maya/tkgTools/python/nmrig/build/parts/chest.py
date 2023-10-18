# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import nmrig.build.rigModule as nmModule
import nmrig.build.chain as nmChain
import nmrig.libs.control.ctrl as nmCtrl
import nmrig.libs.attribute as nmAttr
reload(nmModule)
reload(nmChain)
reload(nmCtrl)
reload(nmAttr)

class Chest(nmModule.RigModule):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=None,
                 ctrl_shape="chest",
                 model_path=None,
                 guide_path=None):
        super(Chest, self).__init__(side=side,
                                  part=part,
                                  guide_list=guide_list,
                                  ctrl_scale=ctrl_scale,
                                  model_path=model_path,
                                  guide_path=guide_path)

        self.ctrl_shape = ctrl_shape

        self.create_module()

    def create_module(self):
        super(Chest, self).create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()

    def control_rig(self):
        self.chest_01 = nmCtrl.Control(parent=self.control_grp,
                                     shape=self.ctrl_shape,
                                     prefix=self.side,
                                     suffix="CTRL",
                                     name=self.part + "_01",
                                     axis="y",
                                     group_type="main",
                                     rig_type="primary",
                                     position=self.guide_list[0],
                                     rotation=(0,0,0),
                                     ctrl_scale=self.ctrl_scale * 0.4)

        self.chest_02 = nmCtrl.Control(parent=self.chest_01.ctrl,
                                     shape=self.ctrl_shape,
                                     prefix=self.side,
                                     suffix="CTRL",
                                     name=self.part + "_02",
                                     axis="y",
                                     group_type="main",
                                     rig_type="primary",
                                     position=self.guide_list[0],
                                     rotation=(0,0,0),
                                     ctrl_scale=self.ctrl_scale * 0.35)

    def output_rig(self):
        chest_jnt_grp = cmds.group(parent=self.module_grp,
                                  empty=True,
                                  name=self.base_name + "_JNT_GRP")
        cmds.matchTransform(chest_jnt_grp, self.chest_02.ctrl)
        self.chest_jnt = cmds.joint(chest_jnt_grp,
                                   name=self.chest_02.ctrl.replace("CTRL", "JNT"))

        cmds.parentConstraint(self.chest_02.ctrl, self.chest_jnt, mo=True)
        # cmds.scaleConstraint(self.chest_02.ctrl, self.chest_jnt, mo=True)

    def skeleton(self):
        self.bind_joints = []
        chest_chain = nmChain.Chain(transform_list=[self.chest_jnt],
                             prefix=self.side,
                             suffix="JNT",
                             name=self.part)
        chest_chain.create_from_transforms(parent=self.skel, pad=False)
        self.bind_joints = chest_chain.joints
        self.tag_bind_joints(self.bind_joints)
