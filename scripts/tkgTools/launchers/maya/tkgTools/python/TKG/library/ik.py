# -*- coding: utf-8 -*-
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

def stretchy(main_ctrl=None, start=None, end=None):
    # start = 'IK_Arm_L'
    # end = 'IK_Hand_L'
    # main_ctrl = 'CTL_IK_Hand_L'

    crv = tkgNodes.create_curve_on_nodes(nodes=[start, end],
                                         name=end+'_STRETCH_CRV',
                                         d=1)

    crv_shape = tkgNodes.get_shapes(crv)[0]

    crv_info = cmds.createNode('curveInfo', ss=True)
    stretch_md = cmds.createNode('multiplyDivide', ss=True)
    stretch_dbn = cmds.createNode('distanceBetween', ss=True)
    stretch_cdn = cmds.createNode('condition', ss=True)

    cmds.setAttr(stretch_md+'.operation', 2)
    cmds.setAttr(stretch_cdn+'.secondTerm', 1)
    cmds.setAttr(stretch_cdn+'.operation', 2)

    cmds.connectAttr(crv_shape+'.worldSpace[0]', crv_info+'.inputCurve', f=True)

    start_stretch_parent = '{0}_stretch_parent'.format(start)
    cmds.duplicate(start, n=start_stretch_parent, po=True)
    cmds.connectAttr(start_stretch_parent+'.worldMatrix[0]', stretch_dbn+'.inMatrix1', f=True)
    cmds.connectAttr(main_ctrl+'.worldMatrix[0]', stretch_dbn+'.inMatrix2', f=True)

    cmds.connectAttr(crv_info+'.arcLength', stretch_md+'.input2X', f=True)
    cmds.connectAttr(crv_info+'.arcLength', stretch_cdn+'.secondTerm', f=True)

    cmds.connectAttr(stretch_dbn+'.distance', stretch_md+'.input1X', f=True)

    cmds.connectAttr(stretch_md+'.outputX', stretch_cdn+'.firstTerm', f=True)
    cmds.connectAttr(stretch_md+'.outputX', stretch_cdn+'.colorIfTrueR', f=True)

    return crv, stretch_cdn, start_stretch_parent

# def stretchy(main_ctrl=None, ikHandle=None, stretchy_axis='x', default_reverse=False):
#     # lookdevKitをロードしないといけない

#     startJoint = cmds.ikHandle(ikHandle, q=1, startJoint=1)
#     endEffector = cmds.ikHandle(ikHandle, q=1, endEffector=1)
#     jointList = cmds.ikHandle(ikHandle, q=1, jointList=1)

#     cmds.select(endEffector)
#     endJoint=cmds.pickWalk(d='up')
#     endJoint=cmds.pickWalk(d='down')[0]

#     jointList.append(endJoint)

#     stretch_nodes=[]

#     # get joints distance
#     def get_distance(objA, objB):
#         gObjA = cmds.xform(objA, q=True, t=True, ws=True)
#         gObjB = cmds.xform(objB, q=True, t=True, ws=True)

#         return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

#     distance = 0.0
#     i = 0
#     for jnt in jointList:
#         if i == 0:
#             pass
#         else:
#             distance += get_distance(jointList[i-1], jnt)
#         i += 1

#     # Add Attr
#     listAttrs = cmds.listAttr(main_ctrl, ud=1)
#     if not listAttrs or not 'stretchIK' in listAttrs:
#         cmds.addAttr(main_ctrl, ln='stretchIK', at='double', k=1)
#         cmds.setAttr('{0}.{1}'.format(main_ctrl, 'stretchIK'), l=1)

#     if not listAttrs or not 'stretchy' in listAttrs:
#         cmds.addAttr(main_ctrl, ln='stretchy', at='double', min=0, max=1, dv=0, k=1)

#     if not listAttrs or not 'nudge' in listAttrs:
#         cmds.addAttr(main_ctrl, ln='nudge', at='double', dv=0, k=1)

#     if not listAttrs or not 'flexible' in listAttrs:
#         cmds.addAttr(main_ctrl, ln='flexible', at='double', min=0, max=1, dv=0, k=1)

#     if not listAttrs or not 'stretchType' in listAttrs:
#         cmds.addAttr(main_ctrl, ln='stretchType', at='enum', en='Translate:Scale:', k=1)

#     if not listAttrs or not 'reverseTranslate' in listAttrs:
#         cmds.addAttr(main_ctrl, ln='reverseTranslate', at='enum', en='Off:On:', k=1)

#     # # softik relative
#     # if softik_bwn != '':
#     #     softik_switch_rev=cmds.createNode('reverse', n='{0}_stretch_softik_rev'.format(main_ctrl))
#     #     cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.inputX'.format(softik_switch_rev), f=1)
#     #     cmds.connectAttr('{0}.outputX'.format(softik_switch_rev), '{0}.{1}'.format(softik_bwn[0][0], softik_bwn[1]), f=1)
#     #     stretch_nodes.append(softik_switch_rev)

#     # Base Nodes
#     stik_dbn = cmds.createNode('distanceBetween', n='{0}_stretch_base_dbn'.format(main_ctrl), ss=1)
#     stik_flc = cmds.createNode('floatLogic', n='{0}_stretch_base_flc'.format(main_ctrl), ss=1)

#     stik_mdl_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_st_mdl'.format(main_ctrl), ss=1)
#     stik_adl_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_nu_adl'.format(main_ctrl), ss=1)
#     stik_adl_start_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_start_nu_adl'.format(main_ctrl), ss=1)
#     stik_adl_mid_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_mid_nu_adl'.format(main_ctrl), ss=1)
#     stik_adl_end_nu = cmds.createNode('addDoubleLinear', n='{0}_stretch_end_nu_adl'.format(main_ctrl), ss=1)

#     stik_mdl_flx = cmds.createNode('multDoubleLinear', n='{0}_stretch_flx_mdl'.format(main_ctrl), ss=1)

#     stik_flcmp_tr_typ = cmds.createNode('floatComposite', n='{0}_stretch_type_tr_flcmp'.format(main_ctrl), ss=1)
#     stik_flcmp_sc_typ = cmds.createNode('floatComposite', n='{0}_stretch_type_sc_flcmp'.format(main_ctrl), ss=1)
#     stik_rev_sc_typ = cmds.createNode('reverse', n='{0}_stretch_type_sc_rev'.format(main_ctrl), ss=1)

#     stik_flcdn_tr_rev = cmds.createNode('floatCondition', n='{0}_stretch_tr_rev_flcdn'.format(main_ctrl), ss=1)

#     stretch_nodes.append(stik_dbn)
#     stretch_nodes.append(stik_flc)
#     stretch_nodes.append(stik_mdl_st)
#     stretch_nodes.append(stik_adl_nu)
#     stretch_nodes.append(stik_adl_start_nu)
#     stretch_nodes.append(stik_adl_mid_nu)
#     stretch_nodes.append(stik_adl_end_nu)
#     stretch_nodes.append(stik_mdl_flx)
#     stretch_nodes.append(stik_flcmp_tr_typ)
#     stretch_nodes.append(stik_flcmp_sc_typ)
#     stretch_nodes.append(stik_rev_sc_typ)
#     stretch_nodes.append(stik_flcdn_tr_rev)

#     # setAttr
#     cmds.setAttr('{0}.operation'.format(stik_flc), 4)
#     cmds.setAttr('{0}.floatA'.format(stik_flc), distance)

#     # cmds.setAttr('{0}.input2'.format(stik_mdl_st), 0.5)
#     cmds.setAttr('{0}.floatA'.format(stik_flcdn_tr_rev), -0.5)
#     cmds.setAttr('{0}.floatB'.format(stik_flcdn_tr_rev), 0.5)

#     if default_reverse:
#         cmds.setAttr('{0}.floatA'.format(stik_flcdn_tr_rev), 0.5)
#         cmds.setAttr('{0}.floatB'.format(stik_flcdn_tr_rev), -0.5)

#     cmds.setAttr('{0}.input2'.format(stik_adl_nu), 1)

#     cmds.setAttr('{0}.floatA'.format(stik_flcmp_tr_typ), 0)
#     cmds.setAttr('{0}.floatB'.format(stik_flcmp_tr_typ), 2)
#     cmds.setAttr('{0}.operation'.format(stik_flcmp_tr_typ), 2)

#     cmds.setAttr('{0}.floatA'.format(stik_flcmp_sc_typ), 0)
#     cmds.setAttr('{0}.floatB'.format(stik_flcmp_sc_typ), 2)
#     cmds.setAttr('{0}.operation'.format(stik_flcmp_sc_typ), 2)

#     # connect
#     startJoint_stretch_parent = '{0}_stretch_parent'.format(startJoint)
#     cmds.duplicate(startJoint, n=startJoint_stretch_parent, po=1)
#     cmds.connectAttr('{0}.worldMatrix[0]'.format(startJoint_stretch_parent), '{0}.inMatrix1'.format(stik_dbn), f=1)
#     cmds.connectAttr('{0}.worldMatrix[0]'.format(main_ctrl), '{0}.inMatrix2'.format(stik_dbn), f=1)
#     cmds.connectAttr('{0}.distance'.format(stik_dbn), '{0}.floatB'.format(stik_flc), f=1)

#     cmds.connectAttr('{0}.nudge'.format(main_ctrl), '{0}.input1'.format(stik_adl_nu), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_start_nu), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_mid_nu), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_adl_nu), '{0}.input1'.format(stik_adl_end_nu), f=1)

#     cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_tr_rev), '{0}.input2'.format(stik_mdl_st), f=1)


#     # Translate Nodes
#     stik_fmn_tr = cmds.createNode('floatMath', n='{0}_stretch_tr_fmn'.format(main_ctrl), ss=1)
#     stik_cdn_tr_res = cmds.createNode('condition', n='{0}_stretch_tr_res_cdn'.format(main_ctrl), ss=1)

#     stik_mdl_mid_tr_res_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_mid_tr_res_st_mdl'.format(main_ctrl), ss=1)
#     stik_adl_mid_tr_init = cmds.createNode('addDoubleLinear', n='{0}_stretch_mid_tr_init_adl'.format(main_ctrl), ss=1)
#     stik_mdl_mid_tr_fin = cmds.createNode('multDoubleLinear', n='{0}_stretch_mid_tr_fin_mdl'.format(main_ctrl), ss=1)

#     stik_mdl_end_tr_res_st = cmds.createNode('multDoubleLinear', n='{0}_stretch_end_tr_res_st_mdl'.format(main_ctrl), ss=1)
#     stik_adl_end_tr_init = cmds.createNode('addDoubleLinear', n='{0}_stretch_end_tr_init_adl'.format(main_ctrl), ss=1)
#     stik_mdl_end_tr_fin = cmds.createNode('multDoubleLinear', n='{0}_stretch_end_tr_fin_mdl'.format(main_ctrl), ss=1)

#     stik_flcdn_mid_tr_init = cmds.createNode('floatCondition', n='{0}_stretch_mid_tr_init_flcdn'.format(main_ctrl), ss=1)
#     stik_flcdn_end_tr_init = cmds.createNode('floatCondition', n='{0}_stretch_end_tr_init_flcdn'.format(main_ctrl), ss=1)

#     stretch_nodes.append(stik_fmn_tr)
#     stretch_nodes.append(stik_cdn_tr_res)
#     stretch_nodes.append(stik_mdl_mid_tr_res_st)
#     stretch_nodes.append(stik_adl_mid_tr_init)
#     stretch_nodes.append(stik_mdl_mid_tr_fin)
#     stretch_nodes.append(stik_mdl_end_tr_res_st)
#     stretch_nodes.append(stik_adl_end_tr_init)
#     stretch_nodes.append(stik_mdl_end_tr_fin)
#     stretch_nodes.append(stik_flcdn_mid_tr_init)
#     stretch_nodes.append(stik_flcdn_end_tr_init)

#     # Translate set
#     cmds.setAttr('{0}.operation'.format(stik_fmn_tr), 1)
#     cmds.setAttr('{0}.operation'.format(stik_cdn_tr_res), 0)
#     cmds.setAttr('{0}.secondTerm'.format(stik_cdn_tr_res), 1)

#     # mid_distance = get_distance(jointList[0], jointList[1])
#     mid_distance = cmds.getAttr('{0}.t{1}'.format(jointList[1], stretchy_axis))
#     cmds.setAttr('{0}.input1'.format(stik_adl_mid_tr_init), mid_distance)
#     cmds.setAttr('{0}.floatA'.format(stik_flcdn_mid_tr_init), mid_distance*-1)
#     cmds.setAttr('{0}.floatB'.format(stik_flcdn_mid_tr_init), mid_distance)

#     # end_distance = get_distance(jointList[-2], jointList[-1])
#     end_distance = cmds.getAttr('{0}.t{1}'.format(jointList[-1], stretchy_axis))
#     cmds.setAttr('{0}.input1'.format(stik_adl_end_tr_init), end_distance)
#     cmds.setAttr('{0}.floatA'.format(stik_flcdn_end_tr_init), end_distance*-1)
#     cmds.setAttr('{0}.floatB'.format(stik_flcdn_end_tr_init), end_distance)

#     # Translate connect
#     cmds.connectAttr('{0}.floatA'.format(stik_flc), '{0}.floatB'.format(stik_fmn_tr), f=1)
#     cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.floatA'.format(stik_fmn_tr), f=1)
#     cmds.connectAttr('{0}.outBool'.format(stik_flc), '{0}.firstTerm'.format(stik_cdn_tr_res), f=1)

#     cmds.connectAttr('{0}.outFloat'.format(stik_fmn_tr), '{0}.colorIfTrueR'.format(stik_cdn_tr_res), f=1)

#     cmds.connectAttr('{0}.outFloat'.format(stik_fmn_tr), '{0}.input1'.format(stik_mdl_flx), f=1)
#     cmds.connectAttr('{0}.flexible'.format(main_ctrl), '{0}.input2'.format(stik_mdl_flx), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_mdl_flx), '{0}.colorIfFalseR'.format(stik_cdn_tr_res), f=1)

#     cmds.connectAttr('{0}.outColorR'.format(stik_cdn_tr_res), '{0}.input1'.format(stik_mdl_mid_tr_res_st), f=1)
#     cmds.connectAttr('{0}.outColorR'.format(stik_cdn_tr_res), '{0}.input1'.format(stik_mdl_end_tr_res_st), f=1)

#     cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.input1'.format(stik_mdl_st), f=1)

#     cmds.connectAttr('{0}.output'.format(stik_mdl_st), '{0}.input2'.format(stik_mdl_mid_tr_res_st), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_mdl_st), '{0}.input2'.format(stik_mdl_end_tr_res_st), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_mdl_mid_tr_res_st), '{0}.input2'.format(stik_adl_mid_tr_init), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_mdl_end_tr_res_st), '{0}.input2'.format(stik_adl_end_tr_init), f=1)

#     cmds.connectAttr('{0}.output'.format(stik_adl_mid_nu), '{0}.input1'.format(stik_mdl_mid_tr_fin), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_adl_end_nu), '{0}.input1'.format(stik_mdl_end_tr_fin), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_adl_mid_tr_init), '{0}.input2'.format(stik_mdl_mid_tr_fin), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_adl_end_tr_init), '{0}.input2'.format(stik_mdl_end_tr_fin), f=1)

#     cmds.connectAttr('{0}.output'.format(stik_mdl_mid_tr_fin), '{0}.t{1}'.format(jointList[-2], stretchy_axis), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_mdl_end_tr_fin), '{0}.t{1}'.format(jointList[-1], stretchy_axis), f=1)

#     cmds.connectAttr('{0}.stretchType'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_tr_typ), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_tr_typ), '{0}.nodeState'.format(stik_mdl_mid_tr_fin), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_tr_typ), '{0}.nodeState'.format(stik_mdl_end_tr_fin), f=1)

#     # cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_mid_tr_init), f=1)
#     # cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_mid_tr_init), '{0}.input1'.format(stik_adl_mid_tr_init), f=1)
#     #
#     # cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_end_tr_init), f=1)
#     # cmds.connectAttr('{0}.outFloat'.format(stik_flcdn_end_tr_init), '{0}.input1'.format(stik_adl_end_tr_init), f=1)

#     cmds.connectAttr('{0}.reverseTranslate'.format(main_ctrl), '{0}.condition'.format(stik_flcdn_tr_rev), f=1)

#     # Scale Nodes
#     stik_flcmp_sc_flx = cmds.createNode('floatComposite', n='{0}_stretch_flx_sc_flcmp'.format(main_ctrl), ss=1)
#     stik_cdn_sc_res = cmds.createNode('condition', n='{0}_stretch_sc_res_cdn'.format(main_ctrl), ss=1)
#     stik_fmn_sc = cmds.createNode('floatMath', n='{0}_stretch_sc_fmn'.format(main_ctrl), ss=1)
#     stik_flcmp_st_sc = cmds.createNode('floatComposite', n='{0}_stretch_sc_st_flcmp'.format(main_ctrl), ss=1)
#     stik_fmn_start_sc_fin = cmds.createNode('floatMath', n='{0}_stretch_start_sc_fin_fmn'.format(main_ctrl), ss=1)
#     stik_fmn_mid_sc_fin = cmds.createNode('floatMath', n='{0}_stretch_mid_sc_fin_fmn'.format(main_ctrl), ss=1)

#     stretch_nodes.append(stik_flcmp_sc_flx)
#     stretch_nodes.append(stik_cdn_sc_res)
#     stretch_nodes.append(stik_fmn_sc)
#     stretch_nodes.append(stik_flcmp_st_sc)
#     stretch_nodes.append(stik_fmn_start_sc_fin)
#     stretch_nodes.append(stik_fmn_mid_sc_fin)

#     # Scale setAttr
#     cmds.setAttr('{0}.operation'.format(stik_flcmp_sc_flx), 2)
#     cmds.setAttr('{0}.operation'.format(stik_cdn_sc_res), 3)
#     cmds.setAttr('{0}.operation'.format(stik_fmn_sc), 3)
#     cmds.setAttr('{0}.floatB'.format(stik_fmn_sc), distance)
#     cmds.setAttr('{0}.operation'.format(stik_flcmp_st_sc), 2)
#     cmds.setAttr('{0}.operation'.format(stik_fmn_start_sc_fin), 2)
#     cmds.setAttr('{0}.operation'.format(stik_fmn_mid_sc_fin), 2)

#     # Scale connect
#     cmds.connectAttr('{0}.floatA'.format(stik_flc), '{0}.floatA'.format(stik_flcmp_sc_flx), f=1)
#     cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.floatB'.format(stik_flcmp_sc_flx), f=1)
#     cmds.connectAttr('{0}.flexible'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_sc_flx), f=1)

#     cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.colorIfTrueR'.format(stik_cdn_sc_res), f=1)
#     cmds.connectAttr('{0}.floatB'.format(stik_flc), '{0}.firstTerm'.format(stik_cdn_sc_res), f=1)

#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_flx), '{0}.colorIfFalseR'.format(stik_cdn_sc_res), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_flx), '{0}.secondTerm'.format(stik_cdn_sc_res), f=1)

#     cmds.connectAttr('{0}.outColorR'.format(stik_cdn_sc_res), '{0}.floatA'.format(stik_fmn_sc), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_fmn_sc), '{0}.floatB'.format(stik_flcmp_st_sc), f=1)
#     cmds.connectAttr('{0}.stretchy'.format(main_ctrl), '{0}.factor'.format(stik_flcmp_st_sc), f=1)

#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_st_sc), '{0}.floatA'.format(stik_fmn_start_sc_fin), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_st_sc), '{0}.floatA'.format(stik_fmn_mid_sc_fin), f=1)

#     cmds.connectAttr('{0}.outFloat'.format(stik_fmn_start_sc_fin), '{0}.s{1}'.format(jointList[0], stretchy_axis), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_fmn_mid_sc_fin), '{0}.s{1}'.format(jointList[1], stretchy_axis), f=1)

#     cmds.connectAttr('{0}.stretchType'.format(main_ctrl), '{0}.inputX'.format(stik_rev_sc_typ), f=1)
#     cmds.connectAttr('{0}.outputX'.format(stik_rev_sc_typ), '{0}.factor'.format(stik_flcmp_sc_typ), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_typ), '{0}.nodeState'.format(stik_fmn_start_sc_fin), f=1)
#     cmds.connectAttr('{0}.outFloat'.format(stik_flcmp_sc_typ), '{0}.nodeState'.format(stik_fmn_mid_sc_fin), f=1)

#     cmds.connectAttr('{0}.output'.format(stik_adl_start_nu), '{0}.floatB'.format(stik_fmn_start_sc_fin), f=1)
#     cmds.connectAttr('{0}.output'.format(stik_adl_mid_nu), '{0}.floatB'.format(stik_fmn_mid_sc_fin), f=1)

#     # hide channelbox
#     for st_node in stretch_nodes:
#         cmds.setAttr('{0}.ihi'.format(st_node), 0)

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
