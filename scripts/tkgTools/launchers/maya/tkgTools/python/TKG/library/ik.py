﻿# -*- coding: utf-8 -*-
from imp import reload
import math

import maya.cmds as cmds
import maya.mel as mel

import TKG.nodes as tkgNodes
import TKG.common as tkgCommon
import TKG.regulation as tkgRegulation
import TKG.library.rigJoints as tkgRigJoints
reload(tkgNodes)
reload(tkgRegulation)
reload(tkgRigJoints)

def ik_settings(solver=None):
    solvers = {
        0: 'ikSCsolver',
        1: 'ikRPsolver',
        2: 'ikSplineSolver',
        3: 'ikSpringSolver'
    }

    settings = {
        'name':None,
        'startJoint':None,
        'endEffector':None,
        'sticky':'sticky',
        'solver':solvers[solver]
    }

    return settings

def create_SC_ikHandle(start=None, end=None):
    settings = ik_settings(solver=0)
    settings['name'] = tkgRegulation.node_type_rename(end, 'ikHandle')
    settings['startJoint'] = start
    settings['endEffector'] = end
    return cmds.ikHandle(**settings)[0]

def create_RP_ikHandle(start=None, end=None):
    settings = ik_settings(solver=1)
    settings['name'] = tkgRegulation.node_type_rename(end, 'ikHandle')
    settings['startJoint'] = start
    settings['endEffector'] = end
    return cmds.ikHandle(**settings)[0]

def create_spline_ikHandle(start=None, end=None):
    settings = ik_settings(solver=2)
    settings['name'] = tkgRegulation.node_type_rename(end, 'ikHandle')
    settings['startJoint'] = start
    ik_spline_end_jnt = tkgRigJoints.create_end_joint(end)
    settings['endEffector'] = ik_spline_end_jnt

    ik_spline_joints = tkgNodes.get_ancestors(start=start,
                                              end=ik_spline_end_jnt,
                                              parents=[])[::-1]

    ik_spline_crv = tkgNodes.create_curve_on_nodes(nodes=ik_spline_joints,
                                   name=tkgRegulation.node_type_rename(end, 'ikSplineCrv'))

    settings['curve'] = ik_spline_crv
    settings['freezeJoints'] = True
    settings['createCurve'] = False
    # settings['snapHandleFlagToggle'] = True
    settings['scv'] = False
    settings['rtm'] = True

    return cmds.ikHandle(**settings)[0], ik_spline_crv

def create_stable_ik_pv(nodes=None, aim_axis='x', up_axis='y', freeze=None):
    sc_ik_joints = tkgRigJoints.create_sc_ik_joints(nodes=nodes,
                                                    aim_axis=aim_axis,
                                                    up_axis=up_axis,
                                                    freeze=freeze)

    [cmds.setAttr(n+'.drawStyle', 2) for n in sc_ik_joints]

    sc_ikh = create_SC_ikHandle(*sc_ik_joints)

    sc_pv_node = cmds.createNode('transform', n='PV_'+sc_ikh, ss=True)
    cmds.parent(sc_pv_node, sc_ik_joints[0])

    cmds.pointConstraint(sc_ik_joints[0], sc_ikh, sc_pv_node, w=True)
    ori_con = cmds.orientConstraint(sc_ik_joints[0], sc_pv_node, w=True)[0]
    cmds.setAttr(ori_con+'.interpType', 2)

    return sc_ik_joints, sc_pv_node, sc_ikh

class StretchSoftIK:
    def __init__(self, main_ctrl=None, ikhandle=None, start=None, end=None, axis='x'):
        # start = 'IK_Arm_L'
        # end = 'IK_Hand_L'
        # main_ctrl = 'CTL_IK_Hand_L'

        self.main_ctrl = main_ctrl
        self.ikhandle = ikhandle
        self.start = start
        self.end = end
        self.axis = axis
        self.stretch_cdn = None
        self.stretch_dbn = None
        self.stretch_value_pb = None
        self.crv_info = None
        self.dis_pma = None
        self.crv = None
        self.start_stretch_parent = None
        self.softik_aim_loc = None

        self.ik_joints = tkgNodes.get_ancestors(start=self.start,
                                                end=self.end,
                                                parents=[])[::-1]

    def stretch_between(self, objA=None, objB=None):
        self.stretch_dbn = cmds.createNode('distanceBetween',
                                           n=tkgRegulation.node_type_rename(objB, 'distanceBetween'),
                                           ss=True)
        self.start_stretch_parent = '{0}_stretch_parent'.format(objA)
        cmds.duplicate(objA, n=self.start_stretch_parent, po=True)
        cmds.setAttr(self.start_stretch_parent+'.drawStyle', 2)
        cmds.connectAttr(self.start_stretch_parent+'.worldMatrix[0]', self.stretch_dbn+'.inMatrix1', f=True)
        cmds.connectAttr(objB+'.worldMatrix[0]', self.stretch_dbn+'.inMatrix2', f=True)

    def stretch_base(self):
        self.crv = tkgNodes.create_curve_on_nodes(nodes=self.ik_joints,
                                            name=self.end+'_STRETCH_CRV',
                                            d=1)

        crv_shape = tkgNodes.get_shapes(self.crv)[0]

        self.crv_info = cmds.createNode('curveInfo',
                                        n='STRETCH_'+tkgRegulation.node_type_rename(self.crv, 'curveInfo'),
                                        ss=True)
        stretch_md = cmds.createNode('multiplyDivide',
                                     n='STRETCH_'+tkgRegulation.node_type_rename(self.main_ctrl, 'multiplyDivide'),
                                     ss=True)
        self.stretch_cdn = cmds.createNode('condition',
                                           n='STRETCH_'+tkgRegulation.node_type_rename(self.main_ctrl, 'condition'),
                                           ss=True)
        self.stretch_value_pb = cmds.createNode('pairBlend',
                                                n='STRETCH_'+tkgRegulation.node_type_rename(self.main_ctrl, 'pairBlend'),
                                                ss=True)

        cmds.setAttr(stretch_md+'.operation', 2)
        cmds.setAttr(self.stretch_cdn+'.operation', 3)
        cmds.setAttr(self.stretch_value_pb+'.inTranslateX1', 1)

        cmds.connectAttr(crv_shape+'.worldSpace[0]', self.crv_info+'.inputCurve', f=True)

        if not self.stretch_dbn:
            self.stretch_between(self.start, self.main_ctrl)

        cmds.connectAttr(self.stretch_dbn+'.distance', self.stretch_cdn+'.firstTerm', f=True)
        cmds.connectAttr(self.stretch_dbn+'.distance', self.stretch_cdn+'.colorIfTrueR', f=True)
        cmds.connectAttr(self.crv_info+'.arcLength', self.stretch_cdn+'.colorIfFalseR', f=True)
        cmds.connectAttr(self.crv_info+'.arcLength', self.stretch_cdn+'.secondTerm', f=True)

        cmds.connectAttr(self.stretch_cdn+'.outColorR', stretch_md+'.input1X', f=True)
        cmds.connectAttr(self.crv_info+'.arcLength', stretch_md+'.input2X', f=True)

        if not cmds.objExists(self.main_ctrl+'.stretch'):
            cmds.addAttr(self.main_ctrl, ln='stretch', at='double', min=0, max=1, dv=0, k=True)

        cmds.connectAttr(stretch_md+'.outputX', self.stretch_value_pb+'.inTranslateX2', f=True)
        cmds.connectAttr(self.main_ctrl+'.stretch', self.stretch_value_pb+'.weight', f=True)

    def softik_base(self, max_value=10):
        self.softik_aim_loc = cmds.spaceLocator(n=self.start+'_softik_aim_loc')
        self.softik_pos = cmds.createNode('transform', n=self.start+'_self.softik_pos', ss=True)

        cmds.pointConstraint(self.start, self.softik_aim_loc, w=True)
        cmds.aimConstraint(self.main_ctrl,
                        self.softik_aim_loc,
                        weight=1,
                        upVector=(0, 1, 0),
                        worldUpType='vector',
                        aimVector=(1, 0, 0),
                        worldUpVector=(0, 1, 0))

        cmds.matchTransform(self.softik_pos, self.softik_aim_loc)
        cmds.parent(self.softik_pos, self.softik_aim_loc)

        # softik calcs
        e = 2.718281828459045235360287471352

        length = tkgCommon.chain_length(self.ik_joints)

        if not cmds.objExists(self.main_ctrl+'.soft'):
            cmds.addAttr(self.main_ctrl, ln='soft', at='double', min=0.0001, max=max_value, dv=0.0001, k=True)

        self.dis_pma = cmds.createNode('plusMinusAverage',
                                       n='SOFT_DIS_'+tkgRegulation.node_type_rename(self.main_ctrl, 'plusMinusAverage'),
                                       ss=True)
        dis_range_pma = cmds.createNode('plusMinusAverage',
                                        n='SOFT_RANGE_'+tkgRegulation.node_type_rename(self.main_ctrl, 'plusMinusAverage'),
                                        ss=True)
        remap_md = cmds.createNode('multiplyDivide',
                                   n='SOFT_REMAP_'+tkgRegulation.node_type_rename(self.main_ctrl, 'multiplyDivide'),
                                   ss=True)
        pow_md = cmds.createNode('multiplyDivide',
                                 n='SOFT_POWER_'+tkgRegulation.node_type_rename(self.main_ctrl, 'multiplyDivide'),
                                 ss=True)
        rev_pma = cmds.createNode('plusMinusAverage',
                                  n='SOFT_REVERSE_'+tkgRegulation.node_type_rename(self.main_ctrl, 'plusMinusAverage'),
                                  ss=True)
        soft_mdl = cmds.createNode('multDoubleLinear',
                                   n='SOFT_'+tkgRegulation.node_type_rename(self.main_ctrl, 'multDoubleLinear'),
                                   ss=True)
        soft_adl = cmds.createNode('addDoubleLinear',
                                   n='SOFT_'+tkgRegulation.node_type_rename(self.main_ctrl, 'addDoubleLinear'),
                                   ss=True)
        soft_cdn = cmds.createNode('condition',
                                   n='SOFT_'+tkgRegulation.node_type_rename(self.main_ctrl, 'condition'),
                                   ss=True)

        if not self.stretch_dbn:
            self.stretch_between(self.start, self.main_ctrl)

        cmds.setAttr(self.dis_pma+'.input1D[0]', sum(length))
        cmds.setAttr(self.dis_pma+'.operation', 2)

        cmds.setAttr(dis_range_pma+'.operation', 2)

        cmds.setAttr(remap_md+'.operation', 2)

        cmds.setAttr(pow_md+'.operation', 3)
        cmds.setAttr(pow_md+'.input1X', e)

        cmds.setAttr(rev_pma+'.operation', 2)
        cmds.setAttr(rev_pma+'.input1D[0]', 1)

        cmds.setAttr(soft_cdn+'.operation', 2)

        # 
        cmds.connectAttr(self.main_ctrl+'.soft', self.dis_pma+'.input1D[1]')

        cmds.connectAttr(self.dis_pma+'.output1D', dis_range_pma+'.input1D[0]')
        cmds.connectAttr(self.stretch_dbn+'.distance', dis_range_pma+'.input1D[1]')

        cmds.connectAttr(dis_range_pma+'.output1D', remap_md+'.input1X')
        cmds.connectAttr(self.main_ctrl+'.soft', remap_md+'.input2X')

        cmds.connectAttr(remap_md+'.outputX', pow_md+'.input2X')

        cmds.connectAttr(pow_md+'.outputX', rev_pma+'.input1D[1]')

        cmds.connectAttr(self.main_ctrl+'.soft', soft_mdl+'.input1')
        cmds.connectAttr(rev_pma+'.output1D', soft_mdl+'.input2')

        cmds.connectAttr(soft_mdl+'.output', soft_adl+'.input1')
        cmds.connectAttr(self.dis_pma+'.output1D', soft_adl+'.input2')

        cmds.connectAttr(self.stretch_dbn+'.distance', soft_cdn+'.firstTerm')
        cmds.connectAttr(self.dis_pma+'.output1D', soft_cdn+'.secondTerm')
        cmds.connectAttr(self.stretch_dbn+'.distance', soft_cdn+'.colorIfFalseR')
        cmds.connectAttr(soft_adl+'.output', soft_cdn+'.colorIfTrueR')

        cmds.connectAttr(soft_cdn+'.outColorR', self.softik_pos+'.tx')

    def stretch_connection(self):
        length = len(self.ik_joints)
        for i, ikj in enumerate(self.ik_joints):
            cmds.setAttr(ikj+'.ssc', True)
            if not i == length - 1:
                cmds.connectAttr(self.stretch_value_pb+'.outTranslateX', ikj+'.s'+self.axis, f=True)

    def softik_connection(self, ikh_con=None):
        if ikh_con:
            cmds.delete(ikh_con)
        cmds.pointConstraint(self.softik_pos, self.ikhandle, w=True)

        pbn = cmds.createNode('pairBlend',
                              n='SOFT_CONNECT_'+tkgRegulation.node_type_rename(self.main_ctrl, 'pairBlend'),
                              ss=True)

        cmds.connectAttr(self.main_ctrl+'.stretch', pbn+'.weight', f=True)
        cmds.connectAttr(self.crv_info+'.arcLength', pbn+'.inTranslateX1', f=True)
        cmds.connectAttr(self.stretch_cdn+'.outColorR', pbn+'.inTranslateX2', f=True)

        cmds.connectAttr(pbn+'.outTranslateX', self.dis_pma+'.input1D[0]', f=True)

def get_ikHandle_joints_distance(setHandle):
    endEffector = cmds.ikHandle(setHandle, q=1, endEffector=1)
    jointList = cmds.ikHandle(setHandle, q=1, jointList=1)

    sel = cmds.ls(os=1)
    cmds.select(endEffector)
    endJoint=cmds.pickWalk(d='up')
    endJoint=cmds.pickWalk(d='down')[0]
    cmds.select(sel)

    jointList.append(endJoint)

    length = tkgCommon.chain_length(chain_list=jointList)

    return sum(length), jointList

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


def create_softik(ik_ctrl=None, ikHandle=None):
    """
    create_softik(ik_ctrl='A_default_IK_main_CTRL', ikhandle='A_default_IKH')
    """

    listAttrs = cmds.listAttr(ik_ctrl, ud=1)
    if not 'softIk' in listAttrs:
        tkgNodes.fn_addNumAttr(ik_ctrl, 'softIk', 'sfi', 0, 10, 0)

    listAttrs = cmds.listAttr(ik_ctrl, ud=1)
    if not 'softIkIntensity' in listAttrs:
        tkgNodes.fn_addNumAttr(ik_ctrl, 'softIkIntensity', 'sfis', 0, 1, 0.1)

    distance, jointList = get_ikHandle_joints_distance(ikHandle)

    startloc, endloc, dup_len_loc = create_softik_locators(start=jointList[0],
                                                           end=jointList[-1],
                                                           startMatchFlag={'pos':True, 'rot':True},
                                                           endMatchFlag={'pos':True, 'rot':True})


    # constraint
    cmds.aimConstraint(ik_ctrl, startloc, weight=1, upVector=(0, 1, 0), worldUpType="vector", aimVector=(1, 0, 0), worldUpVector=(0, 1, 0))
    cmds.pointConstraint(jointList[0], startloc)

    cmds.pointConstraint(ik_ctrl, dup_len_loc)

    cmds.pointConstraint(endloc, ikHandle)


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
    cmds.connectAttr('{0}.softIkIntensity'.format(ik_ctrl), '{0}.input2'.format(dif_mdl), f=1)

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
