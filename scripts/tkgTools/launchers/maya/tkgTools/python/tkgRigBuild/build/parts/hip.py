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


class Hip(tkgModule.RigModule):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=None,
                 offset_hip=-0.1,
                 model_path=None,
                 guide_path=None):
        super(Hip, self).__init__(side=side, part=part,
                                  guide_list=guide_list,
                                  ctrl_scale=ctrl_scale,
                                  model_path=model_path,
                                  guide_path=guide_path)

        self.offset_hip = offset_hip

        self.create_module()

    def create_module(self):
        super(Hip, self).create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        self.add_plugs()

    def control_rig(self):
        # create controls
        self.hip_01 = tkgCtrl.Control(parent=self.control_grp,
                                     shape='hip',
                                     prefix=self.side,
                                     suffix='CTRL',
                                     name=self.part + '_01',
                                     axis='y',
                                     group_type='main',
                                     rig_type='primary',
                                     position=self.guide_list[0],
                                     rotation=(0, 0, 0),
                                     ctrl_scale=self.ctrl_scale * 0.4)

        self.hip_02 = tkgCtrl.Control(parent=self.hip_01.ctrl,
                                     shape='hip',
                                     prefix=self.side,
                                     suffix='CTRL',
                                     name=self.part + '_02',
                                     axis='y',
                                     group_type='main',
                                     rig_type='secondary',
                                     position=self.guide_list[0],
                                     rotation=(0, 0, 0),
                                     ctrl_scale=self.ctrl_scale * 0.35)

    def output_rig(self):
        hip_jnt_grp = cmds.group(parent=self.module_grp, empty=True,
                                 name=self.base_name + '_JNT_GRP')
        cmds.matchTransform(hip_jnt_grp, self.hip_02.ctrl)
        self.hip_jnt = cmds.joint(hip_jnt_grp,
                                  name=self.hip_02.ctrl.replace('CTRL', 'JNT'))

        cmds.parentConstraint(self.hip_02.ctrl, self.hip_jnt, mo=True)

    def skeleton(self):
        hip_chain = tkgChain.Chain(transform_list=[self.hip_jnt],
                                  prefix=self.side,
                                  suffix='JNT',
                                  name=self.part)
        hip_chain.create_from_transforms(parent=self.skel,
                                         pad=False)
        self.bind_joints = hip_chain.joints

        # offset hip joint for better weight mirroring
        if self.offset_hip:
            cmds.setAttr(
                hip_chain.constraints[0] + '.target[0].targetOffsetTranslateY',
                self.offset_hip)

        self.tag_bind_joints(self.bind_joints)

    def add_plugs(self):
        # add skeleton plugs
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['Cn_root_JNT'], name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])

        # add space plugs
        target_list = ['CHAR', 'Cn_global_CTRL', 'Cn_root_02_CTRL', '2']
        name_list = ['world', 'global', 'root', 'default_value']

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=target_list,
                         name=self.hip_01.ctrl + '_parent',
                         children_name=name_list)
