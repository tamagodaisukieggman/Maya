# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import nmrig.libs.attribute as nmAttr
import nmrig.build.chain as nmChain
import nmrig.libs.control.ctrl as nmCtrl
import nmrig.build.guide as nmGuide
reload(nmAttr)
reload(nmChain)
reload(nmCtrl)
reload(nmGuide)


class Ik:
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
                 stretchy=None,
                 stretchy_axis="scaleX"):
        u"""
        import maya.cmds as cmds

        from imp import reload
        import nmrig.build.ik as nmIk
        reload(nmIk)

        ik_util = nmIk.Ik(side="Lf",
                         part="default",
                         guide_list=cmds.ls(os=True),
                         ctrl_scale=1,
                         sticky=None,
                         solver=None,
                         pv_guide="auto",
                         offset_pv=0,
                         slide_pv=None,
                         stretchy=True)

        ik_util.build_ik()
        """


        self.side = side
        self.part = part
        self.base_name = self.side + '_' + self.part

        self.guide_list = guide_list
        self.ctrl_scale = ctrl_scale
        self.sticky = sticky
        self.solver = solver
        self.pv_guide = pv_guide
        self.offset_pv = offset_pv
        self.slide_pv = slide_pv
        self.stretchy = stretchy
        self.stretchy_axis = stretchy_axis

        self.check_solvers()
        self.check_pv_guide()

        if self.guide_list:
            if not isinstance(self.guide_list, list):
                self.guide_list = [self.guide_list]

    def build_ik(self):
        self.build_ik_controls()
        self.build_ik_chain()
        self.build_ikh()

    def check_solvers(self):
        if not self.sticky:
            self.sticky = 'sticky'
        if not self.solver:
            self.solver = 'ikRPsolver'

        if self.solver == 'ikRPsolver':
            self.s_name = 'RP'
        elif self.solver == 'ikSCsolver':
            self.s_name = 'SC'
            self.pv_guide = False
        elif self.solver == 'ikSplineSolver':
            self.s_name = 'spline'
        elif self.solver == 'ikSpringSolver':
            self.s_name = 'spring'
        else:
            cmds.error('Invalid solver defined.')

    def check_pv_guide(self):
        if self.pv_guide == 'auto':
            self.pv_guide = nmGuide.create_pv_guide(guide_list=self.guide_list,
                                                    name=self.base_name,
                                                    slide_pv=self.slide_pv,
                                                    offset_pv=self.offset_pv,
                                                    delete_setup=True)

    def build_ik_controls(self):
        attr_util = nmAttr.Attribute(add=False)
        self.ik_ctrl_grp = cmds.group(empty=True,
                                      name=self.base_name + '_IK_CTRL_GRP')

        self.base_ctrl = nmCtrl.Control(parent=self.ik_ctrl_grp,
                                        shape='cube',
                                        prefix=self.side,
                                        suffix='CTRL',
                                        name=self.part + '_IK_base',
                                        axis='y',
                                        group_type='main',
                                        rig_type='primary',
                                        position=self.guide_list[0],
                                        ctrl_scale=self.ctrl_scale)
        attr_util.lock_and_hide(node=self.base_ctrl.ctrl,
                                translate=False,
                                rotate=False)

        self.main_ctrl = nmCtrl.Control(parent=self.ik_ctrl_grp,
                                        shape='cube',
                                        prefix=self.side,
                                        suffix='CTRL',
                                        name=self.part + '_IK_main',
                                        axis='y',
                                        group_type='main',
                                        rig_type='primary',
                                        position=self.guide_list[-1],
                                        ctrl_scale=self.ctrl_scale)
        attr_util.lock_and_hide(node=self.main_ctrl.ctrl,
                                translate=False,
                                rotate=False)

        if self.pv_guide:
            self.pv_ctrl = nmCtrl.Control(parent=self.ik_ctrl_grp,
                                          shape='locator_3d',
                                          prefix=self.side,
                                          suffix='CTRL',
                                          name=self.part + '_IK_pv',
                                          axis='y',
                                          group_type='main',
                                          rig_type='pv',
                                          position=self.pv_guide,
                                          ctrl_scale=self.ctrl_scale)
            attr_util.lock_and_hide(node=self.pv_ctrl.ctrl, translate=False)

    def build_ik_chain(self):
        self.ik_chain = nmChain.Chain(transform_list=self.guide_list,
                                      prefix=self.side,
                                      suffix=self.s_name + '_JNT',
                                      name=self.part)
        self.ik_chain.create_from_transforms(static=True)
        self.ik_joints = self.ik_chain.joints

    def build_ikh(self, scale_attr=None, constrain=True):
        self.ikh = cmds.ikHandle(name=self.base_name + '_IKH',
                                 startJoint=self.ik_joints[0],
                                 endEffector=self.ik_joints[-1],
                                 sticky=self.sticky,
                                 solver=self.solver)[0]

        if constrain:
            cmds.parentConstraint(self.base_ctrl.ctrl, self.ik_joints[0],
                                  maintainOffset=True)
            cmds.parentConstraint(self.main_ctrl.ctrl, self.ikh,
                                  maintainOffset=True)

        if self.pv_guide:
            cmds.poleVectorConstraint(self.pv_ctrl.ctrl, self.ikh)
            gde = nmGuide.create_line_guide(a=self.pv_ctrl.ctrl,
                                            b=self.ik_joints[1],
                                            name=self.base_name)
            self.gde_grp = cmds.group(gde['curve'], gde['clusters'],
                                      parent=self.ik_ctrl_grp,
                                      name=self.base_name + '_GDE_GRP')
            cmds.setAttr(gde['curve'] + '.inheritsTransform', 0)

        if self.stretchy:
            if not scale_attr:
                scale_attr = nmAttr.Attribute(node=self.base_ctrl.ctrl,
                                              type='double', value=1,
                                              keyable=True,
                                              name='globalScale')
            # add attribute to turn on/off stretch
            self.stretch_switch = nmAttr.Attribute(node=self.main_ctrl.ctrl,
                                                   type='double', value=1,
                                                   min=0, max=1, keyable=True,
                                                   name='stretch')

            # create nodes for stretch system
            dist = cmds.createNode('distanceBetween',
                                   name=self.base_name + '_stretch_DST')
            mdn = cmds.createNode('multiplyDivide',
                                  name=self.base_name + '_stretch_MDN')
            mdl = cmds.createNode('multDoubleLinear',
                                  name=self.base_name + '_stretch_normalize_MDL')
            cnd = cmds.createNode('condition',
                                  name=self.base_name + '_stretch_CND')
            bta = cmds.createNode('blendTwoAttr',
                                  name=self.base_name + '_stretch_switch_BTA')

            # connect ik controls to drive the distance
            cmds.connectAttr(self.base_ctrl.ctrl + '.worldMatrix[0]',
                             dist + '.inMatrix1')
            cmds.connectAttr(self.main_ctrl.ctrl + '.worldMatrix[0]',
                             dist + '.inMatrix2')

            # connect global scale attribute to MDL to normalize scale
            cmds.connectAttr(scale_attr.attr, mdl + '.input1')
            cmds.setAttr(mdl + '.input2', self.ik_chain.chain_length)

            # connect distanceBetween and
            cmds.connectAttr(dist + '.distance', mdn + '.input1X')
            cmds.connectAttr(mdl + '.output', mdn + '.input2X')
            cmds.setAttr(mdn + '.operation', 2)

            # connect the condition, if start/end len == total len, then stretch
            cmds.connectAttr(dist + '.distance', cnd + '.firstTerm')
            cmds.connectAttr(mdl + '.output', cnd + '.secondTerm')
            cmds.connectAttr(mdn + '.outputX', cnd + '.colorIfTrueR')
            cmds.setAttr(cnd + '.operation', 3)

            # connect the condition to the blend two attr node (stretch on/off)
            cmds.setAttr(bta + '.input[0]', 1)
            cmds.connectAttr(cnd + '.outColorR', bta + '.input[1]')
            cmds.connectAttr(self.stretch_switch.attr,
                             bta + '.attributesBlender')

            # connect stretch output to ik joints (except the last one)
            for jnt in self.ik_joints[:-1]:
                cmds.connectAttr(bta + '.output', jnt + '.' + self.stretchy_axis)
