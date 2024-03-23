# -*- coding: utf-8 -*-
from imp import reload
import math

import maya.cmds as cmds
import maya.mel as mel

import TKG.nodes as tkgNodes
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

    return cmds.ikHandle(**settings)[0]

def stretchy(main_ctrl=None, ikHandle=None, stretchy_axis='x', default_reverse=False):
    # lookdevKitをロードしないといけない

    startJoint = cmds.ikHandle(ikHandle, q=1, startJoint=1)
    endEffector = cmds.ikHandle(ikHandle, q=1, endEffector=1)
    jointList = cmds.ikHandle(ikHandle, q=1, jointList=1)

    cmds.select(endEffector)
    endJoint=cmds.pickWalk(d='up')
    endJoint=cmds.pickWalk(d='down')[0]

    jointList.append(endJoint)

    stretch_nodes=[]

    # get joints distance
    def get_distance(objA, objB):
        gObjA = cmds.xform(objA, q=True, t=True, ws=True)
        gObjB = cmds.xform(objB, q=True, t=True, ws=True)

        return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

    distance = 0.0
    i = 0
    for jnt in jointList:
        if i == 0:
            pass
        else:
            distance += get_distance(jointList[i-1], jnt)
        i += 1

    # Add Attr
    listAttrs = cmds.listAttr(main_ctrl, ud=1)
    if not listAttrs or not 'stretchIK' in listAttrs:
        cmds.addAttr(main_ctrl, ln='stretchIK', at='double', k=1)
        cmds.setAttr('{0}.{1}'.format(main_ctrl, 'stretchIK'), l=1)

    if not listAttrs or not 'stretchy' in listAttrs:
        cmds.addAttr(main_ctrl, ln='stretchy', at='double', min=0, max=1, dv=0, k=1)

    if not listAttrs or not 'nudge' in listAttrs:
        cmds.addAttr(main_ctrl, ln='nudge', at='double', dv=0, k=1)

    if not listAttrs or not 'flexible' in listAttrs:
        cmds.addAttr(main_ctrl, ln='flexible', at='double', min=0, max=1, dv=0, k=1)

    if not listAttrs or not 'stretchType' in listAttrs:
        cmds.addAttr(main_ctrl, ln='stretchType', at='enum', en='Translate:Scale:', k=1)

    if not listAttrs or not 'reverseTranslate' in listAttrs:
        cmds.addAttr(main_ctrl, ln='reverseTranslate', at='enum', en='Off:On:', k=1)

    # # softik relative
    # if softik_bwn != '':
    #     softik_switch_rev=cmds.createNode('reverse', n='{0}_stretch_softik_rev'.format(main_ctrl))
    #     cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.inputX'.format(softik_switch_rev), f=1)
    #     cmds.connectAttr('{0}.outputX'.format(softik_switch_rev), '{0}.{1}'.format(softik_bwn[0][0], softik_bwn[1]), f=1)
    #     stretch_nodes.append(softik_switch_rev)

    # Base Nodes
    stik_dbn = cmds.createNode('distanceBetween', n='{0}_stretch_base_dbn'.format(main_ctrl), ss=1)
    stik_flc = cmds.createNode('floatLogic', n='{0}_stretch_base_flc'.format(main_ctrl), ss=1)

    stik_mdl_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_st_mdl'.format(main_ctrl), ss=1)
    stik_adl_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_nu_adl'.format(main_ctrl), ss=1)
    stik_adl_start_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_start_nu_adl'.format(main_ctrl), ss=1)
    stik_adl_mid_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_mid_nu_adl'.format(main_ctrl), ss=1)
    stik_adl_end_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_end_nu_adl'.format(main_ctrl), ss=1)

    stik_mdl_flx = cmds.createNode('multDoubleLinear', n='{0}_stretch_flx_mdl'.format(main_ctrl), ss=1)

    stik_flcmp_tr_typ = cmds.createNode('floatComposite', n='{0}_stretch_type_tr_flcmp'.format(main_ctrl), ss=1)
    stik_flcmp_sc_typ = cmds.createNode('floatComposite', n='{0}_stretch_type_sc_flcmp'.format(main_ctrl), ss=1)
    stik_rev_sc_typ = cmds.createNode('reverse', n='{0}_stretch_type_sc_rev'.format(main_ctrl), ss=1)

    stik_flcdn_tr_rev = cmds.createNode('floatCondition', n='{0}_stretch_tr_rev_flcdn'.format(main_ctrl), ss=1)

    stretch_nodes.append(stik_dbn)
    stretch_nodes.append(stik_flc)
    stretch_nodes.append(stik_mdl_st)
    stretch_nodes.append(stik_adl_nu)
    stretch_nodes.append(stik_adl_start_nu)
    stretch_nodes.append(stik_adl_mid_nu)
    stretch_nodes.append(stik_adl_end_nu)
    stretch_nodes.append(stik_mdl_flx)
    stretch_nodes.append(stik_flcmp_tr_typ)
    stretch_nodes.append(stik_flcmp_sc_typ)
    stretch_nodes.append(stik_rev_sc_typ)
    stretch_nodes.append(stik_flcdn_tr_rev)

    # setAttr
    cmds.setAttr('{0}.operation'.format(stik_flc), 4)
    cmds.setAttr('{0}.floatA'.format(stik_flc), distance)

    # cmds.setAttr('{0}.input2'.format(stik_mdl_st), 0.5)
    cmds.setAttr('{0}.floatA'.format(stik_flcdn_tr_rev), -0.5)
    cmds.setAttr('{0}.floatB'.format(stik_flcdn_tr_rev), 0.5)

    if default_reverse:
        cmds.setAttr('{0}.floatA'.format(stik_flcdn_tr_rev), 0.5)
        cmds.setAttr('{0}.floatB'.format(stik_flcdn_tr_rev), -0.5)

    cmds.setAttr('{0}.input2'.format(stik_adl_nu), 1)

    cmds.setAttr('{0}.floatA'.format(stik_flcmp_tr_typ), 0)
    cmds.setAttr('{0}.floatB'.format(stik_flcmp_tr_typ), 2)
    cmds.setAttr('{0}.operation'.format(stik_flcmp_tr_typ), 2)

    cmds.setAttr('{0}.floatA'.format(stik_flcmp_sc_typ), 0)
    cmds.setAttr('{0}.floatB'.format(stik_flcmp_sc_typ), 2)
    cmds.setAttr('{0}.operation'.format(stik_flcmp_sc_typ), 2)

    # connect
    startJoint_stretch_parent = '{0}_stretch_parent'.format(startJoint)
    cmds.duplicate(startJoint, n=startJoint_stretch_parent, po=1)
    cmds.connectAttr('{0}.worldMatrix[0]'.format(startJoint_stretch_parent), '{0}.inMatrix1'.format(stik_dbn), f=1)
    cmds.connectAttr('{0}.worldMatrix[0]'.format(main_ctrl), '{0}.inMatrix2'.format(stik_dbn), f=1)
    cmds.connectAttr('{0}.distance'.format(stik_dbn), '{0}.floatB'.format(stik_flc), f=1)

    cmds.connectAttr('{0}.nudge'.format(main_ctrl), '{0}.input1'.format(stik_adl_nu), f=1)
    cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_start_nu), f=1)
    cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_mid_nu), f=1)
    cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_end_nu), f=1)

    cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_tr_rev), '{0}.input2'.format(stik_mdl_st), f=1)


    # Translate Nodes
    stik_fmn_tr = cmds.createNode('floatMath', n='{0}_stretch_tr_fmn'.format(main_ctrl), ss=1)
    stik_cdn_tr_res = cmds.createNode('condition', n='{0}_stretch_tr_res_cdn'.format(main_ctrl), ss=1)

    stik_mdl_mid_tr_res_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_mid_tr_res_st_mdl'.format(main_ctrl), ss=1)
    stik_adl_mid_tr_init = cmds.createNode('addDoubleLinear', n='{0}_stretch_mid_tr_init_adl'.format(main_ctrl), ss=1)
    stik_mdl_mid_tr_fin = cmds.createNode('multDoubleLinear', n='{0}_stretch_mid_tr_fin_mdl'.format(main_ctrl), ss=1)

    stik_mdl_end_tr_res_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_end_tr_res_st_mdl'.format(main_ctrl), ss=1)
    stik_adl_end_tr_init = cmds.createNode('addDoubleLinear', n='{0}_stretch_end_tr_init_adl'.format(main_ctrl), ss=1)
    stik_mdl_end_tr_fin = cmds.createNode('multDoubleLinear', n='{0}_stretch_end_tr_fin_mdl'.format(main_ctrl), ss=1)

    stik_flcdn_mid_tr_init = cmds.createNode('floatCondition', n='{0}_stretch_mid_tr_init_flcdn'.format(main_ctrl), ss=1)
    stik_flcdn_end_tr_init = cmds.createNode('floatCondition', n='{0}_stretch_end_tr_init_flcdn'.format(main_ctrl), ss=1)

    stretch_nodes.append(stik_fmn_tr)
    stretch_nodes.append(stik_cdn_tr_res)
    stretch_nodes.append(stik_mdl_mid_tr_res_st)
    stretch_nodes.append(stik_adl_mid_tr_init)
    stretch_nodes.append(stik_mdl_mid_tr_fin)
    stretch_nodes.append(stik_mdl_end_tr_res_st)
    stretch_nodes.append(stik_adl_end_tr_init)
    stretch_nodes.append(stik_mdl_end_tr_fin)
    stretch_nodes.append(stik_flcdn_mid_tr_init)
    stretch_nodes.append(stik_flcdn_end_tr_init)

    # Translate set
    cmds.setAttr('{0}.operation'.format(stik_fmn_tr), 1)
    cmds.setAttr('{0}.operation'.format(stik_cdn_tr_res), 0)
    cmds.setAttr('{0}.secondTerm'.format(stik_cdn_tr_res), 1)

    # mid_distance = get_distance(jointList[0], jointList[1])
    mid_distance = cmds.getAttr('{0}.t{1}'.format(jointList[1], stretchy_axis))
    cmds.setAttr('{0}.input1'.format(stik_adl_mid_tr_init), mid_distance)
    cmds.setAttr('{0}.floatA'.format(stik_flcdn_mid_tr_init), mid_distance*-1)
    cmds.setAttr('{0}.floatB'.format(stik_flcdn_mid_tr_init), mid_distance)

    # end_distance = get_distance(jointList[-2], jointList[-1])
    end_distance = cmds.getAttr('{0}.t{1}'.format(jointList[-1], stretchy_axis))
    cmds.setAttr('{0}.input1'.format(stik_adl_end_tr_init), end_distance)
    cmds.setAttr('{0}.floatA'.format(stik_flcdn_end_tr_init), end_distance*-1)
    cmds.setAttr('{0}.floatB'.format(stik_flcdn_end_tr_init), end_distance)

    # Translate connect
    cmds.connectAttr('{0}.floatA'.format(stik_flc), '{0}.floatB'.format(stik_fmn_tr), f=1)
    cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.floatA'.format(stik_fmn_tr), f=1)
    cmds.connectAttr('{0}.outBool'.format(stik_flc), '{0}.firstTerm'.format(stik_cdn_tr_res), f=1)

    cmds.connectAttr('{0}.outFloat'.format(stik_fmn_tr), '{0}.colorIfTrueR'.format(stik_cdn_tr_res), f=1)

    cmds.connectAttr('{0}.outFloat'.format(stik_fmn_tr), '{0}.input1'.format(stik_mdl_flx), f=1)
    cmds.connectAttr('{0}.flexible'.format(main_ctrl), '{0}.input2'.format(stik_mdl_flx), f=1)
    cmds.connectAttr('{0}.output'.format(stik_mdl_flx), '{0}.colorIfFalseR'.format(stik_cdn_tr_res), f=1)

    cmds.connectAttr('{0}.outColorR'.format(stik_cdn_tr_res), '{0}.input1'.format(stik_mdl_mid_tr_res_st), f=1)
    cmds.connectAttr('{0}.outColorR'.format(stik_cdn_tr_res), '{0}.input1'.format(stik_mdl_end_tr_res_st), f=1)

    cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.input1'.format(stik_mdl_st), f=1)

    cmds.connectAttr('{0}.output'.format(stik_mdl_st), '{0}.input2'.format(stik_mdl_mid_tr_res_st), f=1)
    cmds.connectAttr('{0}.output'.format(stik_mdl_st), '{0}.input2'.format(stik_mdl_end_tr_res_st), f=1)
    cmds.connectAttr('{0}.output'.format(stik_mdl_mid_tr_res_st), '{0}.input2'.format(stik_adl_mid_tr_init), f=1)
    cmds.connectAttr('{0}.output'.format(stik_mdl_end_tr_res_st), '{0}.input2'.format(stik_adl_end_tr_init), f=1)

    cmds.connectAttr('{0}.output'.format(stik_adl_mid_nu), '{0}.input1'.format(stik_mdl_mid_tr_fin), f=1)
    cmds.connectAttr('{0}.output'.format(stik_adl_end_nu), '{0}.input1'.format(stik_mdl_end_tr_fin), f=1)
    cmds.connectAttr('{0}.output'.format(stik_adl_mid_tr_init), '{0}.input2'.format(stik_mdl_mid_tr_fin), f=1)
    cmds.connectAttr('{0}.output'.format(stik_adl_end_tr_init), '{0}.input2'.format(stik_mdl_end_tr_fin), f=1)

    cmds.connectAttr('{0}.output'.format(stik_mdl_mid_tr_fin), '{0}.t{1}'.format(jointList[-2], stretchy_axis), f=1)
    cmds.connectAttr('{0}.output'.format(stik_mdl_end_tr_fin), '{0}.t{1}'.format(jointList[-1], stretchy_axis), f=1)

    cmds.connectAttr('{0}.stretchType'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_tr_typ), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_tr_typ), '{0}.nodeState'.format(stik_mdl_mid_tr_fin), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_tr_typ), '{0}.nodeState'.format(stik_mdl_end_tr_fin), f=1)

    # cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_mid_tr_init), f=1)
    # cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_mid_tr_init), '{0}.input1'.format(stik_adl_mid_tr_init), f=1)
    #
    # cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_end_tr_init), f=1)
    # cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_end_tr_init), '{0}.input1'.format(stik_adl_end_tr_init), f=1)

    cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_tr_rev), f=1)

    # Scale Nodes
    stik_flcmp_sc_flx = cmds.createNode('floatComposite', n='{0}_stretch_flx_sc_flcmp'.format(main_ctrl), ss=1)
    stik_cdn_sc_res = cmds.createNode('condition', n='{0}_stretch_sc_res_cdn'.format(main_ctrl), ss=1)
    stik_fmn_sc = cmds.createNode('floatMath', n='{0}_stretch_sc_fmn'.format(main_ctrl), ss=1)
    stik_flcmp_st_sc = cmds.createNode('floatComposite', n='{0}_stretch_sc_st_flcmp'.format(main_ctrl), ss=1)
    stik_fmn_start_sc_fin = cmds.createNode('floatMath', n='{0}_stretch_start_sc_fin_fmn'.format(main_ctrl), ss=1)
    stik_fmn_mid_sc_fin = cmds.createNode('floatMath', n='{0}_stretch_mid_sc_fin_fmn'.format(main_ctrl), ss=1)

    stretch_nodes.append(stik_flcmp_sc_flx)
    stretch_nodes.append(stik_cdn_sc_res)
    stretch_nodes.append(stik_fmn_sc)
    stretch_nodes.append(stik_flcmp_st_sc)
    stretch_nodes.append(stik_fmn_start_sc_fin)
    stretch_nodes.append(stik_fmn_mid_sc_fin)

    # Scale setAttr
    cmds.setAttr('{0}.operation'.format(stik_flcmp_sc_flx), 2)
    cmds.setAttr('{0}.operation'.format(stik_cdn_sc_res), 3)
    cmds.setAttr('{0}.operation'.format(stik_fmn_sc), 3)
    cmds.setAttr('{0}.floatB'.format(stik_fmn_sc), distance)
    cmds.setAttr('{0}.operation'.format(stik_flcmp_st_sc), 2)
    cmds.setAttr('{0}.operation'.format(stik_fmn_start_sc_fin), 2)
    cmds.setAttr('{0}.operation'.format(stik_fmn_mid_sc_fin), 2)

    # Scale connect
    cmds.connectAttr('{0}.floatA'.format(stik_flc), '{0}.floatA'.format(stik_flcmp_sc_flx), f=1)
    cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.floatB'.format(stik_flcmp_sc_flx), f=1)
    cmds.connectAttr('{0}.flexible'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_sc_flx), f=1)

    cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.colorIfTrueR'.format(stik_cdn_sc_res), f=1)
    cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.firstTerm'.format(stik_cdn_sc_res), f=1)

    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_flx), '{0}.colorIfFalseR'.format(stik_cdn_sc_res), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_flx), '{0}.secondTerm'.format(stik_cdn_sc_res), f=1)

    cmds.connectAttr('{0}.outColorR'.format(stik_cdn_sc_res), '{0}.floatA'.format(stik_fmn_sc), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_fmn_sc), '{0}.floatB'.format(stik_flcmp_st_sc), f=1)
    cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_st_sc), f=1)

    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_st_sc), '{0}.floatA'.format(stik_fmn_start_sc_fin), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_st_sc), '{0}.floatA'.format(stik_fmn_mid_sc_fin), f=1)

    cmds.connectAttr('{0}.outFloat'.format(stik_fmn_start_sc_fin), '{0}.s{1}'.format(jointList[0], stretchy_axis), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_fmn_mid_sc_fin), '{0}.s{1}'.format(jointList[1], stretchy_axis), f=1)

    cmds.connectAttr('{0}.stretchType'.format(main_ctrl), '{0}.inputX'.format(stik_rev_sc_typ), f=1)
    cmds.connectAttr('{0}.outputX'.format(stik_rev_sc_typ), '{0}.factor'.format(stik_flcmp_sc_typ), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_typ), '{0}.nodeState'.format(stik_fmn_start_sc_fin), f=1)
    cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_typ), '{0}.nodeState'.format(stik_fmn_mid_sc_fin), f=1)

    cmds.connectAttr('{0}.output'.format(stik_adl_start_nu), '{0}.floatB'.format(stik_fmn_start_sc_fin), f=1)
    cmds.connectAttr('{0}.output'.format(stik_adl_mid_nu), '{0}.floatB'.format(stik_fmn_mid_sc_fin), f=1)

    # hide channelbox
    for st_node in stretch_nodes:
        cmds.setAttr('{0}.ihi'.format(st_node), 0)
