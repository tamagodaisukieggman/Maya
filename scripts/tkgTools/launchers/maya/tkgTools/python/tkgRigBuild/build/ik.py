# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import tkgRigBuild.libs.attribute as tkgAttr
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.libs.transform as tkgXform
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.build.guide as tkgGuide
import tkgRigBuild.build.spline as tkgSpline
reload(tkgAttr)
reload(tkgChain)
reload(tkgCtrl)
reload(tkgGuide)
reload(tkgXform)
reload(tkgSpline)

class Ik:
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=1,
                 ctrl_color=[0.8, 0.5, 0.2],
                 sticky=None,
                 solver=None,
                 pv_guide='auto',
                 offset_pv=0,
                 slide_pv=None,
                 stretchy=None,
                 stretchy_axis="scaleX",
                 soft_ik=None):
        u"""
        import maya.cmds as cmds

        from imp import reload
        import tkgRigBuild.build.ik as tkgIk
        reload(tkgIk)

        ik_util = tkgIk.Ik(side="Lf",
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
        self.ctrl_color = ctrl_color
        self.sticky = sticky
        self.solver = solver
        self.pv_guide = pv_guide
        self.offset_pv = offset_pv
        self.slide_pv = slide_pv
        self.stretchy = stretchy
        self.stretchy_axis = stretchy_axis

        self.soft_ik = soft_ik
        self.for_softik_pac = None

        self.check_solvers()
        self.check_pv_guide()

        if self.guide_list:
            if not isinstance(self.guide_list, list):
                self.guide_list = [self.guide_list]

        self.part_ik_ctrls = []

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
            self.pv_guide = False
        elif self.solver == 'ikSpringSolver':
            self.s_name = 'spring'
        else:
            cmds.error('Invalid solver defined.')

    def check_pv_guide(self):
        if self.pv_guide == 'auto':
            self.pv_guide = tkgGuide.create_pv_guide(guide_list=self.guide_list,
                                                    name=self.base_name,
                                                    slide_pv=self.slide_pv,
                                                    offset_pv=self.offset_pv,
                                                    delete_setup=True)

    def build_ik_controls(self):
        attr_util = tkgAttr.Attribute(add=False)
        self.ik_ctrl_grp = cmds.group(empty=True,
                                      name=self.base_name + '_IK_CTRL_GRP')

        self.base_ctrl = tkgCtrl.Control(parent=self.ik_ctrl_grp,
                                        shape='cube',
                                        prefix=self.side,
                                        suffix='CTRL',
                                        name=self.part + '_IK_base',
                                        axis='y',
                                        group_type='main',
                                        rig_type=self.side+'_'+self.part+'IkBase',
                                        position=self.guide_list[0],
                                        ctrl_scale=self.ctrl_scale,
                                        ctrl_color=self.ctrl_color)
        self.part_ik_ctrls.append(self.base_ctrl.ctrl)
        attr_util.lock_and_hide(node=self.base_ctrl.ctrl,
                                translate=False,
                                rotate=False)

        self.main_ctrl = tkgCtrl.Control(parent=self.ik_ctrl_grp,
                                        shape='jack',
                                        prefix=self.side,
                                        suffix='CTRL',
                                        name=self.part + '_IK_main',
                                        axis='y',
                                        group_type='main',
                                        rig_type=self.side+'_'+self.part+'IkMain',
                                        position=self.guide_list[-1],
                                        ctrl_scale=self.ctrl_scale,
                                        ctrl_color=self.ctrl_color)
        self.part_ik_ctrls.append(self.main_ctrl.ctrl)
        attr_util.lock_and_hide(node=self.main_ctrl.ctrl,
                                translate=False,
                                rotate=False)

        if self.pv_guide:
            self.pv_ctrl = tkgCtrl.Control(parent=self.ik_ctrl_grp,
                                          shape='locator_3d',
                                          prefix=self.side,
                                          suffix='CTRL',
                                          name=self.part + '_IK_pv',
                                          axis='y',
                                          group_type='main',
                                          rig_type=self.side+'_'+self.part+'IkPv',
                                          position=self.pv_guide,
                                          ctrl_scale=self.ctrl_scale,
                                          ctrl_color=self.ctrl_color)
            self.part_ik_ctrls.append(self.pv_ctrl.ctrl)
            attr_util.lock_and_hide(node=self.pv_ctrl.ctrl, translate=False)

    def build_ik_chain(self):
        self.ik_chain = tkgChain.Chain(transform_list=self.guide_list,
                                      prefix=self.side,
                                      suffix=self.s_name + '_JNT',
                                      name=self.part)
        self.ik_chain.create_from_transforms(static=True)
        self.ik_joints = self.ik_chain.joints

    def build_ikh(self, scale_attr=None, constrain=True):
        settings = {
            'name':self.base_name + '_IKH',
            'startJoint':self.ik_joints[0],
            'endEffector':self.ik_joints[-1],
            'sticky':self.sticky,
            'solver':self.solver
        }

        if self.solver in ['ikSplineSolver']:
            spline = tkgSpline.Spline(guide_list=self.guide_list,
                                      side=self.side,
                                      part=self.part)
            spline.build_spline_curve()
            self.ik_spline_crv = spline.crv
            settings['curve'] = self.ik_spline_crv
            # settings['freezeJoints'] = True
            settings['createCurve'] = False
            # settings['snapHandleFlagToggle'] = True
            settings['scv'] = False

        self.ikh = cmds.ikHandle(**settings)[0]

        if constrain:
            cmds.parentConstraint(self.base_ctrl.ctrl, self.ik_joints[0],
                                  maintainOffset=True)
            self.for_softik_pac = cmds.parentConstraint(self.main_ctrl.ctrl, self.ikh,
                                  maintainOffset=True)

        if self.pv_guide:
            cmds.poleVectorConstraint(self.pv_ctrl.ctrl, self.ikh)
            gde = tkgGuide.create_line_guide(a=self.pv_ctrl.ctrl,
                                            b=self.ik_joints[1],
                                            name=self.base_name)
            self.gde_grp = cmds.group(gde['curve'], gde['clusters'],
                                      parent=self.ik_ctrl_grp,
                                      name=self.base_name + '_GDE_GRP')
            cmds.setAttr(gde['curve'] + '.inheritsTransform', 0)

        if self.stretchy:
            if not scale_attr:
                scale_attr = tkgAttr.Attribute(node=self.base_ctrl.ctrl,
                                              type='double', value=1,
                                              keyable=True,
                                              name='globalScale')
            # add attribute to turn on/off stretch
            self.stretch_switch = tkgAttr.Attribute(node=self.main_ctrl.ctrl,
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

        if self.soft_ik:
            self.build_softik()

    def build_softik(self):
        if self.for_softik_pac:
            cmds.delete(self.for_softik_pac[0])
        self.soft_ik_loc = create_softik(ik_ctrl=self.main_ctrl.ctrl, ikhandle=self.ikh)

def get_ikHandle_joints_distance(setHandle):
    endEffector = cmds.ikHandle(setHandle, q=1, endEffector=1)
    jointList = cmds.ikHandle(setHandle, q=1, jointList=1)

    sel = cmds.ls(os=1)
    cmds.select(endEffector)
    endJoint=cmds.pickWalk(d='up')
    endJoint=cmds.pickWalk(d='down')[0]
    cmds.select(sel)

    jointList.append(endJoint)

    length = 0.0
    i = 0
    for jnt in jointList:
        if i == 0:
            pass
        else:
            length += tkgXform.get_distance(jointList[i-1], jnt)
        i += 1

    return length, jointList

def create_softik_locators(start=None, end=None, startMatchFlag=None, endMatchFlag=None):
    startloc = '{0}_softik_st_loc'.format(start)
    endloc = '{0}_softik_ed_loc'.format(end)
    lenloc = '{0}_softik_len_loc'.format(end)

    cmds.spaceLocator(n=startloc)
    cmds.spaceLocator(n=endloc)

    cmds.matchTransform(startloc, start, **startMatchFlag)
    cmds.matchTransform(endloc, end, **endMatchFlag)

    dup_len_loc = cmds.duplicate(endloc, n=lenloc)

    cmds.parent(endloc, startloc)
    cmds.parent(dup_len_loc, startloc)

    return startloc, endloc, dup_len_loc


def create_softik(ik_ctrl=None, ikhandle=None):
    """
    create_softik(ik_ctrl='A_default_IK_main_CTRL', ikhandle='A_default_IKH')
    """
    listAttrs = cmds.listAttr(ik_ctrl, ud=1)
    if not 'softIk' in listAttrs:
        tkgXform.fn_addNumAttr(ik_ctrl, 'softIk', 'sfi', 0, 10, 0)

    listAttrs = cmds.listAttr(ik_ctrl, ud=1)
    if not 'softIkIntencity' in listAttrs:
        tkgXform.fn_addNumAttr(ik_ctrl, 'softIkIntencity', 'sfic', 0, 1, 0.1)

    distance, jointList = get_ikHandle_joints_distance(ikhandle)

    startloc, endloc, dup_len_loc = create_softik_locators(start=jointList[0],
                                                           end=jointList[-1],
                                                           startMatchFlag={'pos':True, 'rot':True},
                                                           endMatchFlag={'pos':True, 'rot':True})


    # constraint
    cmds.aimConstraint(ik_ctrl, startloc, weight=1, upVector=(0, 1, 0), worldUpType="vector", aimVector=(1, 0, 0), worldUpVector=(0, 1, 0))
    cmds.pointConstraint(jointList[0], startloc)

    cmds.pointConstraint(ik_ctrl, dup_len_loc)

    cmds.pointConstraint(endloc, ikhandle)


    # create nodes

    e = 2.718281828459045235360287471352

    sub_len_pma = cmds.createNode('plusMinusAverage', n='{0}_softik_{1}'.format(jointList[-1], 'sub_len_pma'))
    cmds.setAttr('{0}.operation'.format(sub_len_pma), 2)
    cmds.setAttr('{0}.input1D[0]'.format(sub_len_pma), distance)
    cmds.connectAttr('{0}.softIk'.format(ik_ctrl), '{0}.input1D[1]'.format(sub_len_pma), f=1)

    sub_dif_pma = cmds.createNode('plusMinusAverage', n='{0}_softik_{1}'.format(jointList[-1], 'sub_dif_pma'))
    cmds.setAttr('{0}.operation'.format(sub_dif_pma), 2)
    cmds.connectAttr('{0}.tx'.format(dup_len_loc[0]), '{0}.input1D[0]'.format(sub_dif_pma), f=1)
    cmds.connectAttr('{0}.output1D'.format(sub_len_pma), '{0}.input1D[2]'.format(sub_dif_pma), f=1)

    neg_mdl = cmds.createNode('multDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'neg_mdl'))
    cmds.setAttr('{0}.input2'.format(neg_mdl), -1)
    cmds.connectAttr('{0}.output1D'.format(sub_dif_pma), '{0}.input1'.format(neg_mdl), f=1)

    dif_mdl = cmds.createNode('multDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'dif_mdl'))
    cmds.setAttr('{0}.input2'.format(dif_mdl), 0.1)
    cmds.connectAttr('{0}.output'.format(neg_mdl), '{0}.input1'.format(dif_mdl), f=1)
    cmds.connectAttr('{0}.softIkIntencity'.format(ik_ctrl), '{0}.input2'.format(dif_mdl), f=1)

    npr_md = cmds.createNode('multiplyDivide', n='{0}_softik_{1}'.format(jointList[-1], 'npr_md'))
    cmds.setAttr('{0}.operation'.format(npr_md), 3)
    cmds.setAttr('{0}.input1X'.format(npr_md), e)
    cmds.connectAttr('{0}.output'.format(dif_mdl), '{0}.input2X'.format(npr_md), f=1)

    calc_pma = cmds.createNode('plusMinusAverage', n='{0}_softik_{1}'.format(jointList[-1], 'calc_pma'))
    cmds.setAttr('{0}.operation'.format(calc_pma), 2)
    cmds.setAttr('{0}.input1D[0]'.format(calc_pma), 1)
    cmds.connectAttr('{0}.outputX'.format(npr_md), '{0}.input1D[1]'.format(calc_pma), f=1)

    calc_mdl = cmds.createNode('multDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'calc_mdl'))
    cmds.connectAttr('{0}.softIk'.format(ik_ctrl), '{0}.input1'.format(calc_mdl), f=1)
    cmds.connectAttr('{0}.output1D'.format(calc_pma), '{0}.input2'.format(calc_mdl), f=1)

    calc_adl = cmds.createNode('addDoubleLinear', n='{0}_softik_{1}'.format(jointList[-1], 'calc_adl'))
    cmds.connectAttr('{0}.output1D'.format(sub_len_pma), '{0}.input1'.format(calc_adl), f=1)
    cmds.connectAttr('{0}.output'.format(calc_mdl), '{0}.input2'.format(calc_adl), f=1)

    flw_ikh_pos_cdn = cmds.createNode('condition', n='{0}_softik_{1}'.format(jointList[-1], 'flw_ikh_pos_cdn'))
    cmds.connectAttr('{0}.softIk'.format(ik_ctrl), '{0}.firstTerm'.format(flw_ikh_pos_cdn), f=1)
    cmds.connectAttr('{0}.tx'.format(dup_len_loc[0]), '{0}.colorIfTrueR'.format(flw_ikh_pos_cdn), f=1)
    cmds.connectAttr('{0}.output'.format(calc_adl), '{0}.colorIfFalseR'.format(flw_ikh_pos_cdn), f=1)


    effect_cdn = cmds.createNode('condition', n='{0}_softik_{1}'.format(jointList[-1], 'effect_cdn'))
    cmds.setAttr('{0}.operation'.format(effect_cdn), 2)

    cmds.connectAttr('{0}.translateX'.format(dup_len_loc[0]), '{0}.colorIfFalseR'.format(effect_cdn), f=1)
    cmds.connectAttr('{0}.translateX'.format(dup_len_loc[0]), '{0}.firstTerm'.format(effect_cdn), f=1)

    cmds.connectAttr('{0}.output1D'.format(sub_len_pma), '{0}.secondTerm'.format(effect_cdn), f=1)
    cmds.connectAttr('{0}.outColorR'.format(flw_ikh_pos_cdn), '{0}.colorIfTrueR'.format(effect_cdn), f=1)

    cmds.connectAttr('{0}.outColorR'.format(effect_cdn), '{0}.translateX'.format(endloc), f=1)

    cmds.connectAttr('{0}.ty'.format(dup_len_loc[0]), '{0}.ty'.format(endloc), f=1)
    cmds.connectAttr('{0}.tz'.format(dup_len_loc[0]), '{0}.tz'.format(endloc), f=1)

    return startloc
