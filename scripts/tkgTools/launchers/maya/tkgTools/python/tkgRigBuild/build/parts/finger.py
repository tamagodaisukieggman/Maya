# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.libs.attribute as tkgAttr
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.build.fk as tkgFk
reload(tkgModule)
reload(tkgAttr)
reload(tkgChain)
reload(tkgFk)

class Finger(tkgModule.RigModule, tkgFk.Fk):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 fk_ctrl_axis='x',
                 fk_ctrl_edge_axis='-x',
                 ctrl_scale=None,
                 ctrl_color=[0.2, 0.65, 0.72],
                 model_path=None,
                 guide_path=None,
                 pad='auto',
                 remove_last=True,
                 fk_shape='arrowOctagon'):
        super(Finger, self).__init__(side=side, part=part,
                                     guide_list=guide_list,
                                     ctrl_scale=ctrl_scale,
                                     model_path=model_path,
                                     guide_path=guide_path)

        self.pad = pad
        self.remove_last = remove_last
        self.fk_shape = fk_shape
        self.gimbal = None
        self.offset = None
        self.fk_ctrl_axis = fk_ctrl_axis
        self.fk_ctrl_edge_axis = fk_ctrl_edge_axis
        self.ctrl_color = ctrl_color

        if self.pad == 'auto':
            self.pad = len(str(len(self.guide_list))) + 1

        self.create_module()

    def create_module(self):
        super(Finger, self).create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        # self.add_plugs()

    def control_rig(self):
        # create controls
        self.build_fk_controls()
        cmds.parent(self.fk_ctrls[0].top, self.control_grp)

    def output_rig(self):
        self.build_fk_chain()
        cmds.parent(self.fk_joints[0], self.module_grp)

    def skeleton(self):
        fk_chain = tkgChain.Chain(transform_list=self.fk_joints,
                                 prefix=self.side,
                                 suffix='JNT',
                                 name=self.part)
        fk_chain.create_from_transforms(parent=self.skel,
                                        scale_constraint=False)

        if self.remove_last:
            cmds.delete(self.fk_ctrls[-1].top)
            self.bind_joints = fk_chain.joints[:-1]
        else:
            self.bind_joints = fk_chain.joints

        self.tag_bind_joints(self.bind_joints)

    def add_plugs(self):
        # add skeleton plugs
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=[self.side + '_hand_JNT'], name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])

        # add parentConstraint rig plugs
        driver_list = [self.side + '_hand_01_switch_JNT']
        driven_list = [self.base_name + '_01_fk_CTRL_CNST_GRP']

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=driver_list, name='pacRigPlugs',
                         children_name=driven_list)
