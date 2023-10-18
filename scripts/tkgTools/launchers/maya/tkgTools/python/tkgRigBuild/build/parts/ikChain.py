# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.libs.attribute as tkgAttr
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.build.ik as tkgIk
reload(tkgChain)


class IkChain(tkgModule.RigModule, tkgIk.Ik):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=1,
                 sticky=None,
                 solver=None,
                 pv_guide='auto',
                 offset_pv=0,
                 slide_pv=None,
                 stretchy=True,
                 stretchy_axis='scaleX',
                 twisty=None,
                 twisty_axis='x',
                 bendy=None,
                 bendy_axis='scaleX',
                 segments=None,
                 model_path=None,
                 guide_path=None):
        super(IkChain, self).__init__(side=side, part=part,
                                      guide_list=guide_list,
                                      ctrl_scale=ctrl_scale,
                                      model_path=model_path,
                                      guide_path=guide_path)

        self.sticky = sticky
        self.solver = solver
        self.pv_guide = pv_guide
        self.offset_pv = offset_pv
        self.slide_pv = slide_pv
        self.stretchy = stretchy
        self.stretchy_axis = stretchy_axis
        self.twisty = twisty
        self.twisty_axis = twisty_axis
        self.bendy = bendy
        self.bendy_axis = bendy_axis
        self.segments = segments

        if self.twisty or self.bendy and not self.segments:
            self.segments = 4

        self.create_module()

    def create_module(self):
        super(IkChain, self).create_module()

        self.check_solvers()
        self.check_pv_guide()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        # self.add_plugs()

        if self.pv_guide:
            cmds.parent(self.gde_grp, self.control_grp)

    def control_rig(self):
        self.build_ik_controls()
        cmds.parent(self.ik_ctrl_grp, self.control_grp)

    def output_rig(self):
        self.build_ik_chain()
        self.src_joints = self.ik_joints

        if self.segments:
            self.ik_chain.split_chain(segments=self.segments)
            self.src_joints = []
            for ik_jnt in self.ik_joints[:-1]:
                split_list = self.ik_chain.split_jnt_dict[ik_jnt]
                for s_jnt in split_list:
                    self.src_joints.append(s_jnt)
            self.src_joints.append(self.ik_joints[-1])

        if self.twisty:
            self.ik_chain.twist_chain(start_translate=self.ik_chain.joints[1],
                                      start_rotate=self.ik_chain.joints[0],
                                      end_translate=self.ik_chain.joints[0],
                                      end_rotate=self.ik_chain.joints[0],
                                      twist_bone=self.ik_chain.joints[0],
                                      twist_driver=self.base_ctrl.ctrl,
                                      twist_axis=self.twisty_axis,
                                      reverse=True)
            self.ik_chain.twist_chain(start_translate=self.ik_chain.joints[2],
                                      start_rotate=self.ik_chain.joints[1],
                                      end_translate=self.ik_chain.joints[2],
                                      end_rotate=self.ik_chain.joints[1],
                                      twist_bone=self.ik_chain.joints[1],
                                      twist_driver=self.main_ctrl.ctrl,
                                      twist_axis=self.twisty_axis)

        if self.bendy:
            bend_01 = self.ik_chain.bend_chain(bone=self.ik_chain.joints[0],
                                               ctrl_scale=self.ctrl_scale,
                                               global_scale=self.global_scale.attr,
                                               scale_axis=self.bendy_axis)
            bend_02 = self.ik_chain.bend_chain(bone=self.ik_chain.joints[1],
                                               ctrl_scale=self.ctrl_scale,
                                               global_scale=self.global_scale.attr,
                                               scale_axis=self.bendy_axis)
            cmds.parent(bend_01['control'], bend_02['control'],
                        self.control_grp)
            cmds.parent(bend_01['module'], bend_02['module'], self.module_grp)

        self.build_ikh(scale_attr=self.global_scale)
        cmds.parent(self.ikh, self.ik_joints[0], self.module_grp)

    def skeleton(self):
        ik_chain = tkgChain.Chain(transform_list=self.src_joints,
                                 prefix=self.side,
                                 suffix='JNT',
                                 name=self.part)
        ik_chain.create_from_transforms(orient_constraint=True,
                                        point_constraint=True,
                                        scale_constraint=False,
                                        parent=self.skel)

        self.bind_joints = ik_chain.joints
        self.tag_bind_joints(self.bind_joints[:-1])

    def add_plugs(self):
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['add ik plug here'], name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])
