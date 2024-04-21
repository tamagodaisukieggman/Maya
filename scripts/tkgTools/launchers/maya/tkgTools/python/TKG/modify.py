# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds
import maya.mel as mel

import TKG.library.rigJoints as tkgRigJoints
import TKG.common as tkgCommon
import TKG.nodes as tkgNodes
import TKG.library.ik as tkgIk
import TKG.library.control.ctrls as tkgCtrls
import TKG.modules.baseModule as tkgModules
import TKG.regulation as tkgRegulation
reload(tkgRigJoints)
reload(tkgCommon)
reload(tkgNodes)
reload(tkgIk)
reload(tkgCtrls)
reload(tkgModules)
reload(tkgRegulation)

def stick_pv_lock(sel=None, aim_axis='x', up_axis='y'):
    if not sel:
        sel = cmds.ls(os=True)
    start = sel[0]
    mid = sel[1]
    end = sel[2]

    stick_locs = []
    for i, obj in enumerate([start, mid, end]):
        loc = cmds.spaceLocator(n=obj+'_STICK_LOC')
        stick_locs.append(loc)
        cmds.matchTransform(loc, obj)
        if i != 0:
            cmds.parent(loc, loc_pa)

        cmds.pointConstraint(loc, obj)

        loc_pa = loc

    pv_pos = tkgNodes.pole_vec(start=start, mid=mid, end=end, move=5, obj=None)

    aim_loc = cmds.spaceLocator(n=mid+'_STICK_PV_LOC')[0]
    cmds.xform(aim_loc, t=pv_pos, ws=True)

    # aim
    aim_con_start = cmds.aimConstraint(stick_locs[1], start,
                       aimVector=tkgRegulation.axis_vector(aim_axis), upVector=tkgRegulation.axis_vector(up_axis),
                       worldUpType='object', worldUpObject=aim_loc)[0]

    aim_con_mid = cmds.aimConstraint(stick_locs[2], mid,
                       aimVector=tkgRegulation.axis_vector(aim_axis), upVector=tkgRegulation.axis_vector(up_axis),
                       worldUpType='object', worldUpObject=aim_loc)[0]

    if not '-' in aim_axis:
        neg_axis = '-'+aim_axis
    else:
        neg_axis = aim_axis.lstrip('-')

    aim_con_end = cmds.aimConstraint(stick_locs[1], end,
                       aimVector=tkgRegulation.axis_vector(neg_axis), upVector=tkgRegulation.axis_vector(up_axis),
                       worldUpType='object', worldUpObject=aim_loc)[0]

    cmds.parent(aim_loc, stick_locs[0])

def create_joints_per_component(sel=None):
    if not sel:
        sel = cmds.ls(os=True, fl=True)
    for i, obj in enumerate(sel):
        jnt = cmds.createNode('joint', ss=True)
        obj_pos = cmds.xform(obj, q=True, t=True, ws=True)
        cor_pos = tkgCommon.calculate_centroid(tkgCommon.get_sublists(obj_pos, 3))
        cmds.xform(jnt, t=cor_pos, ws=True, a=True)
        if i != 0:
            cmds.parent(jnt, jnt_pa)
        jnt_pa = jnt

def aim_component_selection(aim_axis='y', up_axis='x'):
    if not sel:
        sel = cmds.ls(os=True, fl=True)

    component_up = sel[0]
    up_obj = sel[1]

    obj_pos = cmds.xform(component_up, q=True, t=True, ws=True)
    cor_pos = tkgCommon.calculate_centroid(tkgCommon.get_sublists(obj_pos, 3))

    up_loc = cmds.spaceLocator(n=up_obj+'_COMPONENT_UP_LOC')[0]
    cmds.xform(up_loc, t=cor_pos, ws=True, a=True)

    pa = cmds.listRelatives(up_obj, p=True) or None
    if pa:
        aim_loc = cmds.spaceLocator(n=pa[0]+'_COMPONENT_AIM_LOC')[0]
        cmds.matchTransform(aim_loc, pa[0])

    children = cmds.listRelatives(up_obj, c=True) or None
    lock_locs = []
    for chi in children:
        loc = cmds.spaceLocator()[0]
        lock_locs.append(loc)
        cmds.matchTransform(loc, chi)
        cmds.pointConstraint(loc, chi, w=True)

    aim_con_end = cmds.aimConstraint(up_loc, up_obj,
                       aimVector=tkgRegulation.axis_vector(neg_axis), upVector=tkgRegulation.axis_vector(up_axis),
                       worldUpType='vector', worldUpVector=[0,1,0])[0]

def create_bend_base_cage(twist=None, twist_direction='-',
                          inside=None, body_type=None):
    sel = cmds.ls(os=True)

    cylinder = cmds.polyCylinder(r=1, h=2, sx=8, sy=5)

    if twist:
        mel.eval('''
        select -r {0}.vtx[0:7] ;
        rotate -r -p 5.96046e-08cm -1cm 2.98023e-08cm -os -fo 0 {1}45 0 ;

        select -r {0}.vtx[8:15] ;
        rotate -r -p 5.96046e-08cm -0.6cm 2.98023e-08cm -os -fo 0 {1}36 0 ;

        select -r {0}.vtx[16:23] ;
        rotate -r -p 5.96046e-08cm -0.2cm 2.98023e-08cm -os -fo 0 {1}27 0 ;

        select -r {0}.vtx[24:31] ;
        rotate -r -p 5.96046e-08cm 0.2cm 2.98023e-08cm -os -fo 0 {1}18 0 ;

        select -r {0}.vtx[32:39] ;
        rotate -r -p 5.96046e-08cm 0.6cm 2.98023e-08cm -os -fo 0 {1}9 0 ;
        '''.format(cylinder[0], twist_direction))

    cylinderShape = cmds.listRelatives(cylinder[0], s=True) or None
    if cylinderShape:
        cylinderShape = cylinderShape[0]
    mel.eval('''
    delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 30 0.5 -ep 22 0.5 |{0}|{1};  select -cl;
    delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 27 0.5 -ep 19 0.5 |{0}|{1};  select -cl;

    delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 79 1 -ep 30 1 |{0}|{1};  select -cl;
    delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 14 1 -ep 89 0 |{0}|{1};  select -cl;

    delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 35 0 -ep 27 1 |{0}|{1};  select -cl;
    delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 11 0 -ep 92 0 |{0}|{1};  select -cl;
    '''.format(cylinder[0], cylinderShape))

    delEdges= [cylinder[0]+'.e[19]',
     cylinder[0]+'.e[27]',
     cylinder[0]+'.e[88:89]',
     cylinder[0]+'.e[18]',
     cylinder[0]+'.e[23]',
     cylinder[0]+'.e[26]',
     cylinder[0]+'.e[31]',
     cylinder[0]+'.e[16:17]',
     cylinder[0]+'.e[24:25]']

    cmds.polyDelEdge(delEdges, cv=True, ch=1)

    mel.eval('''
    delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 49 0.5 -ep 71 0.5 -ep 55 0.5 -ep 54 0.5 -ep 53 0.5 -ep 52 0.5 -ep 59 0.5 -ep 68 0.5 -ep 51 0.5 -ep 50 0.5 -ep 49 0.5 |{0}|{1};
    delete {0}.f[30:31];
    '''.format(cylinder[0], cylinderShape))

    if inside:
        mel.eval('''
        select -r {0}.e[91] ;
        polySpinEdge -ch 1 -offset -1;

        select -r {0}.e[88] ;
        polySpinEdge -ch 1 -offset 1;

        // polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 3 -ofc 0 -ost 0 -ocr 0 -dv 1 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1 {0};
        '''.format(cylinder[0], cylinderShape))

    if body_type == 'shoulder':
        mel.eval('''
        delete {0}.f[14:16] {0}.f[21:24] {0}.f[29] {0}.f[36:39];

        select -r {0}.e[8:10] {0}.e[15] ;
        polyExtrudeEdge -constructionHistory 1 -keepFacesTogether 1 -pvx 5.960464478e-08 -pvy -0.6000000238 -pvz -0.4999999404 -divisions 1 -twist 0 -taper 1 -offset 0 -thickness 0 -smoothingAngle 30 {0}.e[8:10] {0}.e[15];
        setAttr "polyExtrudeEdge7.localTranslate" -type double3 0 0.335907 0 ;
        move -r -os -wd 0 0.377342 0 ;

        select -r {0}.vtx[39] {0}.vtx[47] ;
        MergeToCenter;

        select -r {0}.vtx[38] {0}.vtx[46] ;
        MergeToCenter;

        select -r {0}.e[77] {0}.e[79:81] ;
        polyExtrudeEdge -constructionHistory 1 -keepFacesTogether 1 -pvx 5.960464478e-08 -pvy -0.1669936366 -pvz -0.4999999776 -divisions 1 -twist 0 -taper 1 -offset 0 -thickness 0 -smoothingAngle 30 {0}.e[77] {0}.e[79:81];
        move -r -os -wd 0 0.306544 -0.540454 ;

        select -r {0}.e[84] {0}.e[86] {0}.e[88] {0}.e[90] ;
        polyExtrudeEdge -constructionHistory 1 -keepFacesTogether 1 -pvx 5.960464478e-08 -pvy 0.1395501941 -pvz -1.040453672 -divisions 1 -twist 0 -taper 1 -offset 0 -thickness 0 -smoothingAngle 30 {0}.e[84] {0}.e[86] {0}.e[88] {0}.e[90];
        move -r -os -wd 0 0.180369 -0.788511 ;

        select -r {0}.e[87] {0}.e[89] {0}.e[96] {0}.e[98] ;
        polyExtrudeEdge -constructionHistory 1 -keepFacesTogether 1 -pvx 5.960464478e-08 -pvy 0.1321274936 -pvz -0.6644824743 -divisions 1 -twist 0 -taper 1 -offset 0 -thickness 0 -smoothingAngle 30 {0}.e[87] {0}.e[89] {0}.e[96] {0}.e[98];

        move -r -os -wd 0 0.710065 0 ;

        select -r {0}.vtx[26] {0}.vtx[58] ;
        MergeToCenter;

        select -r {0}.vtx[22] {0}.vtx[56] ;
        MergeToCenter;

        select -r {0}.e[101] {0}.e[103] {0}.e[105] {0}.e[107] ;
        polyExtrudeEdge -constructionHistory 1 -keepFacesTogether 1 -pvx 5.960464478e-08 -pvy 0.8425088525 -pvz -0.6644824743 -divisions 1 -twist 0 -taper 1 -offset 0 -thickness 0 -smoothingAngle 30 {0}.e[101] {0}.e[103] {0}.e[105] {0}.e[107];

        move -r -os -wd 0 0.408848 0 ;

        select -r {0}.vtx[31] {0}.vtx[62] ;
        MergeToCenter;

        select -r {0}.vtx[27] {0}.vtx[60] ;
        MergeToCenter;

        setAttr "{0}.rotateX" -90;
        setAttr "{0}.rotateY" 90;
        '''.format(cylinder[0]))

    elif body_type == 'hip':
        mel.eval('''
        delete {0}.f[10] {0}.f[20:21] {0}.f[28:31] {0}.f[39:41];
        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 26 0 -ep 20 0.5 -ep 77 0.5 -ep 8 0.5 -ep 32 0.5 -ep 39 0.5 -ep 38 0.5 -ep 13 0.5 -ep 17 0.5 -ep 78 0.5 -ep 19 0.5 -ep 25 0.5 -ep 59 1 |{0}|{1};

        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 91 0.5 -ep 54 1 |{0}|{1};
        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 94 0.5 -ep 0 1 |{0}|{1};
        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 97 0.5 -ep 37 0 |{0}|{1};
        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 102 0.5 -ep 31 0 |{0}|{1};

        select -r {0}.e[82] ;
        polySpinEdge -ch 1 -offset 1;

        select -r {0}.e[13] ;
        polySpinEdge -ch 1 -offset -1;

        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 104 0.3 -ep 80 0.3 -ep 77 0.7 -ep 94 0.3 -ep 83 0.7 -ep 84 0.7 -ep 85 0.7 -ep 107 0.7 -ep 17 0.7 -ep 88 0.3 -ep 19 0.7 -ep 25 0.7 -ep 110 0.3 |{0}|{1};  select -cl;
        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 37 1 -ep 108 0.46404 -ep 5 1 |{0}|{1};  select -cl;

        select -r {0}.vtx[9] {0}.vtx[58] ;
        MergeToCenter;

        delete `polyMoveVertex -ch 1 |{0}|{1}.vtx[0]`; polySplit -ch 1 -sma 180 -ep 37 1 -ep 4 0.620851 |{0}|{1};  select -cl;

        setAttr "{0}.rotateY" 180;

        '''.format(cylinder[0], cylinderShape))

    cmds.select(cylinder[0])
    cmds.DeleteHistory()

    if sel:
        cmds.select(sel, r=True)

    return cylinder
