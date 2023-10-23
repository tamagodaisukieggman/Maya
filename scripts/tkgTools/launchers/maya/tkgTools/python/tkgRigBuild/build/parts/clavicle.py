# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload


import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.libs.attribute as tkgAttr


class Clavicle(tkgModule.RigModule):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=None,
                 local_orient=False,
                 constrain_skip_axis=['y', 'z'],
                 left_aimVector=(1,0,0),
                 left_upVector=(0,-1,0),
                 right_aimVector=(-1,0,0),
                 right_upVector=(0,1,0),
                 side_list=[['L', 'left', 'Lf'], ['R', 'right', 'Rt']],
                 stretchy_axis='scaleX',
                 twisty_axis='x',
                 model_path=None,
                 guide_path=None):
        """

        """


        super(Clavicle, self).__init__(side=side, part=part,
                                       guide_list=guide_list,
                                       ctrl_scale=ctrl_scale,
                                       model_path=model_path,
                                       guide_path=guide_path)

        self.local_orient = local_orient
        self.constrain_skip_axis = constrain_skip_axis
        self.left_aimVector = left_aimVector
        self.left_upVector = left_upVector
        self.right_aimVector = right_aimVector
        self.right_upVector = right_upVector
        self.side_list = side_list
        self.side_list_sorted = self.sort_side_list(self.side_list)
        self.stretchy_axis = stretchy_axis
        self.twisty_axis = twisty_axis

        self.create_module()

    def create_module(self):
        super(Clavicle, self).create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        # self.add_plugs()

    def control_rig(self):
        if self.local_orient:
            rotation = self.guide_list[0]
        else:
            rotation = (0, 0, 0)

        # create controls
        self.main_ctrl = tkgCtrl.Control(parent=self.control_grp,
                                        shape='cube',
                                        prefix=self.side,
                                        suffix='CTRL',
                                        name='clavicle',
                                        axis='y',
                                        group_type='main',
                                        rig_type='primary',
                                        position=self.guide_list[0],
                                        rotation=rotation,
                                        ctrl_scale=self.ctrl_scale)

        attr_util = tkgAttr.Attribute(add=False)
        attr_util.lock_and_hide(node=self.main_ctrl.ctrl,
                                translate=False,
                                rotate=False)

    def output_rig(self):
        # create clavicle chain
        cnst_grp = cmds.group(empty=True, parent=self.module_grp,
                             name=self.base_name + '_CNST_GRP')
        jnt_grp = cmds.group(empty=True, name=self.base_name + '_JNT_GRP')
        cmds.matchTransform(jnt_grp, self.guide_list[0])
        cmds.matchTransform(cnst_grp, self.guide_list[0])
        self.clav_chain = tkgChain.Chain(transform_list=self.guide_list,
                                        prefix=self.side,
                                        suffix='driver_JNT',
                                        name=self.part)
        self.clav_chain.create_from_transforms(static=True,
                                               parent=jnt_grp)

        # create aim locators
        target_loc = cmds.spaceLocator(name=self.base_name + '_target_LOC')[0]
        up_loc = cmds.spaceLocator(name=self.base_name + '_upV_LOC')[0]
        up_loc_grp = cmds.group(up_loc, name=up_loc + '_GRP')
        cmds.parent(jnt_grp, up_loc_grp, target_loc, cnst_grp)

        # position aim locators
        cmds.matchTransform(target_loc, self.clav_chain.joints[-1])
        cmds.matchTransform(up_loc_grp, self.clav_chain.joints[0])

        cmds.parentConstraint(self.main_ctrl.ctrl, target_loc,
                              maintainOffset=True)
        cmds.orientConstraint(self.main_ctrl.ctrl, up_loc_grp,
                              skip=self.constrain_skip_axis)
        if self.side in self.side_list_sorted[0]:
            av = self.left_aimVector
            uv = self.left_upVector
        elif self.side in self.side_list_sorted[1]:
            av = self.right_aimVector
            uv = self.right_upVector

        cmds.xform(up_loc, objectSpace=True,
                   translation=(uv[0] * self.clav_chain.bone_lengths[0] * 1.1,
                                uv[1] * self.clav_chain.bone_lengths[0] * 1.1,
                                uv[2] * self.clav_chain.bone_lengths[0] * 1.1)
                    )

        cmds.aimConstraint(target_loc, jnt_grp, aimVector=av, upVector=uv,
                           worldUpType='object', worldUpObject=up_loc)

        # add stretch
        tkgAttr.Attribute(node=self.main_ctrl.ctrl,
                         type='separator', name='______')
        stretch = tkgAttr.Attribute(node=self.main_ctrl.ctrl,
                                   type='double', value=0,
                                   min=0, max=1, keyable=True,
                                   name='stretch')
        twist = tkgAttr.Attribute(node=self.main_ctrl.ctrl,
                                 type='double', value=0,
                                 keyable=True, name='twist')

        cmds.connectAttr(twist.attr, self.clav_chain.joints[0] + '.rotate' + self.twisty_axis.upper())
        # create nodes for stretch system
        dist = cmds.createNode('distanceBetween',
                               name=self.base_name + '_stretch_DST')
        mdn = cmds.createNode('multiplyDivide',
                              name=self.base_name + '_stretch_MDN')
        mdl = cmds.createNode('multDoubleLinear',
                              name=self.base_name + '_stretch_MDL')
        bta = cmds.createNode('blendTwoAttr',
                              name=self.base_name + '_stretch_BTA')
        # connect start/end to drive stretch
        cmds.setAttr(mdn + '.operation', 2)
        cmds.connectAttr(self.main_ctrl.top + '.worldMatrix[0]',
                         dist + '.inMatrix1')
        cmds.connectAttr(target_loc + '.worldMatrix[0]',
                         dist + '.inMatrix2')
        cmds.connectAttr(dist + '.distance', mdn + '.input1X')
        d = cmds.getAttr(dist + '.distance')
        # connect attr for global scale
        cmds.connectAttr(self.global_scale.attr, mdl + '.input1')
        cmds.connectAttr(mdl + '.output', mdn + '.input2X')
        cmds.setAttr(mdl + '.input2', d)
        # blend stretch on and off
        cmds.setAttr(bta + '.input[0]', 1)
        cmds.connectAttr(mdn + '.outputX', bta + '.input[1]')
        cmds.connectAttr(stretch.attr,
                         bta + '.attributesBlender')
        # connect final output
        cmds.connectAttr(bta + '.output', self.clav_chain.joints[0] + '.' + self.stretchy_axis)

    def skeleton(self):
        bind_chain = tkgChain.Chain(transform_list=self.clav_chain.joints,
                                   prefix=self.side,
                                   suffix='JNT',
                                   name=self.part)
        bind_chain.create_from_transforms(parent=self.skel)
        self.bind_joints = bind_chain.joints
        self.tag_bind_joints(self.bind_joints[:-1])

    def add_plugs(self):
        # add skeleton plugs
        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=['Cn_chest_JNT'], name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])

        # add parentConstraint rig plugs
        driver_list = ['Cn_chest_02_JNT',
                       'Cn_chest_02_JNT']
        driven_list = [self.side + '_clavicle_CTRL_CNST_GRP',
                       self.side + '_clavicle_CNST_GRP']

        tkgAttr.Attribute(node=self.part_grp, type='plug',
                         value=driver_list, name='pacRigPlugs',
                         children_name=driven_list)
