# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload


import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.libs.attribute as tkgAttr


class Head(tkgModule.RigModule):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=None,
                 ctrl_color=[0.743, 0.179, 0.041],
                 model_path=None,
                 guide_path=None):
        super(Head, self).__init__(side=side, part=part,
                                   guide_list=guide_list,
                                   ctrl_scale=ctrl_scale,
                                   model_path=model_path,
                                   guide_path=guide_path)

        self.ctrl_color = ctrl_color

        self.create_module()

    def create_module(self):
        super().create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        # self.add_plugs()

    def control_rig(self):
        # create controls
        self.head_01 = tkgCtrl.Control(parent=self.control_grp,
                                      shape='arrowFourWayCurved',
                                      prefix=self.side,
                                      suffix='CTRL',
                                      name=self.part + '_01',
                                      axis='y',
                                      group_type='main',
                                      rig_type=self.part + '_01',
                                      position=self.guide_list[0],
                                      rotation=(0, 0, 0),
                                      ctrl_scale=self.ctrl_scale,
                                      ctrl_color=self.ctrl_color)

        self.head_02 = tkgCtrl.Control(parent=self.head_01.ctrl,
                                      shape='arrowFourWayCurved',
                                      prefix=self.side,
                                      suffix='CTRL',
                                      name=self.part + '_02',
                                      axis='y',
                                      group_type='main',
                                      rig_type=self.part + '_02',
                                      position=self.guide_list[0],
                                      rotation=(0, 0, 0),
                                      ctrl_scale=self.ctrl_scale * 0.95,
                                      ctrl_color=[v*0.95 for v in self.ctrl_color])

    def output_rig(self):
        self.head_jnt = cmds.joint(self.head_01.ctrl,
                                   name=self.head_01.ctrl.replace('CTRL',
                                                                  'JNT'))
        cmds.group(self.head_jnt, parent=self.module_grp,
                   name=self.base_name + '_JNT_GRP')

        cmds.pointConstraint(self.head_02.ctrl, self.head_jnt,
                             maintainOffset=True)
        cmds.orientConstraint(self.head_02.ctrl, self.head_jnt,
                              maintainOffset=True)
        cmds.scaleConstraint(self.head_02.ctrl, self.head_jnt,
                             maintainOffset=True)

    def skeleton(self):
        jnt = cmds.joint(self.skel, name=self.base_name + '_JNT')
        cmds.parentConstraint(self.head_jnt, jnt, maintainOffset=False)
        cmds.scaleConstraint(self.head_jnt, jnt, maintainOffset=False)
        self.bind_joints = [jnt]
        self.tag_bind_joints(self.bind_joints, self.part_grp)

    def add_plugs(self):
        # add skeleton plugs
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['cmds.ls("' + self.side + '_neck_??_JNT")[-1]'],
                         name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])

        # add space plugs
        target_list = ['CHAR', 'Cn_global_CTRL', 'Cn_root_02_CTRL',
                       'Cn_chest_01_CTRL', 'Cn_chest_02_CTRL',
                       'Cn_neck_base_CTRL', '5']
        name_list = ['world', 'global', 'root', 'chest01', 'chest02', 'neck',
                     'default_value']
        point_names = ['point' + n.title() for n in name_list]
        orient_names = ['orient' + n.title() for n in name_list]

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=target_list,
                         name=self.head_01.ctrl + '_point',
                         children_name=point_names)

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=target_list,
                         name=self.head_01.ctrl + '_orient',
                         children_name=orient_names)

        # add delete rig plugs
        delete_list = [self.base_name + '_01_JNT_pointConstraint1']
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=[' '.join(delete_list)], name='deleteRigPlugs',
                         children_name=['deleteNodes'])

        # add transferAttributes plug
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=[self.head_01.ctrl], name='transferAttributes',
                         children_name=['Cn_neck_tip_CTRL'])

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['cmds.ls("Cn_neck_??_driver_JNT", "Cn_neck_??_fk_offset_CTRL")[-1]'],
                         name='pocRigPlugs',
                         children_name=[self.head_jnt])
