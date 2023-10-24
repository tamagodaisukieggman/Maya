# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgModule)
reload(tkgChain)
reload(tkgCtrl)
reload(tkgAttr)

class Chest(tkgModule.RigModule):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 chest_01_name='chest_01',
                 chest_02_name='chest_02',
                 ctrl_scale=None,
                 ctrl_shape="chest",
                 ctrl_color=[1, 1, 0.24],
                 model_path=None,
                 guide_path=None):
        super(Chest, self).__init__(side=side,
                                  part=part,
                                  guide_list=guide_list,
                                  ctrl_scale=ctrl_scale,
                                  model_path=model_path,
                                  guide_path=guide_path)

        self.chest_01_name = chest_01_name
        self.chest_02_name = chest_02_name
        self.ctrl_shape = ctrl_shape
        self.ctrl_color = ctrl_color

        self.part_ctrls = []

        self.create_module()

    def create_module(self):
        super(Chest, self).create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        # self.add_plugs()

    def control_rig(self):
        self.chest_01 = tkgCtrl.Control(parent=self.control_grp,
                                     shape=self.ctrl_shape,
                                     prefix=self.side,
                                     suffix="CTRL",
                                     name=self.chest_01_name,
                                     axis="y",
                                     group_type="main",
                                     rig_type=self.chest_01_name,
                                     position=self.guide_list[0],
                                     rotation=(0,0,0),
                                     ctrl_scale=self.ctrl_scale * 0.4,
                                     ctrl_color=self.ctrl_color)
        self.part_ctrls.append(self.chest_01.ctrl)

        self.chest_02 = tkgCtrl.Control(parent=self.chest_01.ctrl,
                                     shape=self.ctrl_shape,
                                     prefix=self.side,
                                     suffix="CTRL",
                                     name=self.chest_02_name,
                                     axis="y",
                                     group_type="main",
                                     rig_type=self.chest_02_name,
                                     position=self.guide_list[0],
                                     rotation=(0,0,0),
                                     ctrl_scale=self.ctrl_scale * 0.35,
                                     ctrl_color=[v*0.35 for v in self.ctrl_color])
        self.part_ctrls.append(self.chest_02.ctrl)

    def output_rig(self):
        chest_jnt_grp = cmds.group(parent=self.module_grp,
                                  empty=True,
                                  name=self.base_name + "_JNT_GRP")
        cmds.matchTransform(chest_jnt_grp, self.chest_02.ctrl)
        self.chest_jnt = cmds.joint(chest_jnt_grp,
                                   name=self.chest_02.ctrl.replace("CTRL", "JNT"))

        cmds.parentConstraint(self.chest_02.ctrl, self.chest_jnt, mo=True)
        # cmds.scaleConstraint(self.chest_02.ctrl, self.chest_jnt, mo=True)

        self.tag_buid_ctrls(self.part+'Ctrls', self.part_ctrls, self.part_grp)

    def skeleton(self):
        self.bind_joints = []
        chest_chain = tkgChain.Chain(transform_list=[self.chest_jnt],
                             prefix=self.side,
                             suffix="JNT",
                             name=self.part)
        chest_chain.create_from_transforms(parent=self.skel, pad=False)
        self.bind_joints = chest_chain.joints
        self.tag_bind_joints(self.bind_joints, self.part_grp)

    def add_plugs(self):
        # add skeleton plugs
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['cmds.ls("Cn_spine_??_JNT")[-1]'],
                         name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])

        # add delete rig plugs
        delete_list = ['Cn_chest_02_JNT_parentConstraint1',
                       'Cn_spine_tip_CTRL_CNST_GRP_parentConstraint1']
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=[' '.join(delete_list)], name='deleteRigPlugs',
                         children_name=['deleteNodes'])

        # add pointConstraint rig plugs
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['cmds.ls("Cn_spine_??_driver_JNT")[-1]'],
                         name='pocRigPlugs',
                         children_name=[self.chest_jnt + '_point'])

        # add orientConstraint rig plugs
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=[self.chest_02.ctrl],
                         name='orcRigPlugs',
                         children_name=[self.chest_jnt + '_orient'])

        # add space plugs
        target_list = ['CHAR', 'Cn_global_CTRL', 'Cn_root_02_CTRL',
                       'Cn_spine_03_FK_CTRL', '3']
        name_list = ['world', 'global', 'root', 'spine', 'default_value']
        point_names = ['point' + n.title() for n in name_list]
        orient_names = ['orient' + n.title() for n in name_list]

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=target_list,
                         name=self.chest_01.ctrl + '_point',
                         children_name=point_names)

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=target_list,
                         name=self.chest_01.ctrl + '_orient',
                         children_name=orient_names)

        # add transferAttributes plug
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=[self.chest_01.ctrl], name='transferAttributes',
                         children_name=['Cn_spine_tip_CTRL'])
