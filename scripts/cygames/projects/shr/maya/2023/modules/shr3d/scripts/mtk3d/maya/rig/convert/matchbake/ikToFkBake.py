# -*- coding: utf-8 -*-
import timeit
import math
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

def ikToFkMatch(startjnt=None, middleJnt=None, endJnt=None, ikCtrl=None, ikPvCtrl=None, ikRotCtrl=None, clvFkCtrl=None, clvIkCtrl=None, foot=0, ballFkCtrl=None, ballIkCtrl=None, matchDum=None, matchOffset=None, move=20):
    start = cmds.xform(startjnt ,q= 1 ,ws = 1,t =1 )
    mid = cmds.xform(middleJnt ,q= 1 ,ws = 1,t =1 )
    end = cmds.xform(endJnt ,q= 1 ,ws = 1,t =1 )
    startV = om.MVector(start[0] ,start[1],start[2])
    midV = om.MVector(mid[0] ,mid[1],mid[2])
    endV = om.MVector(end[0] ,end[1],end[2])

    cmds.xform(ikCtrl, t=[endV.x, endV.y, endV.z], a=1, ws=1)

    startEnd = endV - startV
    startMid = midV - startV

    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj

    arrowV = startMid - projV
    arrowV*= 0.5
    finalV = arrowV + midV

    cross1 = startEnd ^ startMid
    cross1.normalize()

    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()

    matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,cross1.x ,cross1.y , cross1.z , 0 ,cross2.x , cross2.y , cross2.z , 0,0,0,0,1]

    matrixM = om.MMatrix()

    om.MScriptUtil.createMatrixFromList(matrixV , matrixM)

    matrixFn = om.MTransformationMatrix(matrixM)

    rot = matrixFn.eulerRotation()

    cmds.xform(ikPvCtrl , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
    cmds.xform('{}_tfn'.format(ikPvCtrl) , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    cmds.select(ikPvCtrl)
    cmds.move(move, 0, 0, r=1, os=1, wd=1)

    if foot == 1:
        ori = cmds.orientConstraint(matchDum, ikCtrl, w=1, offset=matchOffset)
        ikCtrlVal = cmds.xform(ikCtrl, q=1, ro=1, ws=1)
        cmds.delete(ori)
        cmds.xform(ikCtrl, ro=ikCtrlVal, ws=1)

        rVal = cmds.xform(ballFkCtrl, ws=1, q=1, ro=1)
        cmds.xform(ballIkCtrl, ro=rVal, ws=1, a=1)

    elif foot == 0:
        rVal = cmds.xform(endJnt, ws=1, q=1, ro=1)
        cmds.xform(ikRotCtrl, ro=rVal, ws=1, a=1)

        clavicleFkRot = cmds.xform(clvFkCtrl, q=1, ro=1, ws=1)
        rotOrderA = cmds.getAttr('{}.rotateOrder'.format(clvFkCtrl))
        rotOrderB = cmds.getAttr('{}.rotateOrder'.format(clvIkCtrl))
        euler = om.MEulerRotation(math.radians(clavicleFkRot[0]), math.radians(clavicleFkRot[1]), math.radians(clavicleFkRot[2]), rotOrderA)
        r = euler.reorder(rotOrderB)
        cmds.xform(clvIkCtrl, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], a=1, ws=1)


'''
clock = timeit.default_timer
start = clock()
cmds.refresh(su=1)
animation.correctAnimationKeys()
cmds.refresh(su=0)
elapsed = clock() - start
print("%.3f s" % (elapsed,))


clock = timeit.default_timer
start = clock()
animation.correctAnimationKeys()
elapsed = clock() - start
print("%.3f s" % (elapsed,))

animation.correctOneAxis(start=ikRigs[0], middle=fkRigs[2], end=fkRigs[3], axis='Y')
'''

def match():
    nss_in_joints = cmds.ls('*_proxy_jnt', type='joint', r=1)
    nss_buf = ['{}'.format(nss_in.replace(nss_in.split(':')[-1], '')) for nss_in in nss_in_joints]
    nss_list = list(set(nss_buf))
    try:
        nss_list.remove('')
    except:
        pass
    nss = nss_list[0]

    global ikToFkMatch
    global om
    global math

    # clock = timeit.default_timer
    # start = clock()

    playmin = cmds.playbackOptions(q=1, min=1)
    playmax = cmds.playbackOptions(q=1, max=1)


    cmds.refresh(su=1)
    x = int(playmin)
    for i in range(int(playmax)+1):
        f = i + x
        if f == int(playmax)+1:
            break
        else:
            cmds.currentTime(f)

            ############
            ## arms_R ##
            ############

            meta = '{}meta_arms_R'.format(nss)
            proxyJoints = cmds.listConnections('{}.metaProxyJoints'.format(meta), d=True, s=False)
            ikRigs = cmds.listConnections('{}.metaIkRigs'.format(meta), d=True, s=False)
            fkRigs = cmds.listConnections('{}.metaFkRigs'.format(meta), d=True, s=False)

            # ik to fk
            ikToFkMatch(startjnt=fkRigs[1], middleJnt=fkRigs[2], endJnt=fkRigs[3], ikCtrl=ikRigs[0], ikPvCtrl=ikRigs[4], ikRotCtrl=ikRigs[2], clvFkCtrl=fkRigs[0], clvIkCtrl=ikRigs[6], foot=0, ballFkCtrl=None, ballIkCtrl=None, matchDum=None, matchOffset=None, move=-20)

            cmds.setKeyframe('{}.translate'.format(ikRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[2]), breakdown=0)
            cmds.setKeyframe('{}.translate'.format(ikRigs[4]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[6]), breakdown=0)


            # fk to ik
            # animation.fkToIkMatch(startFkCtrl=fkRigs[1], middleFkCtrl=fkRigs[2], endFkCtrl=fkRigs[3], ikCtrl=ikRigs[0], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[0], space='ws', rotateOrders=1)

            ############
            ## legs_R ##
            ############

            meta = '{}meta_legs_R'.format(nss)
            proxyJoints = cmds.listConnections('{}.metaProxyJoints'.format(meta), d=True, s=False)
            ikRigs = cmds.listConnections('{}.metaIkRigs'.format(meta), d=True, s=False)
            fkRigs = cmds.listConnections('{}.metaFkRigs'.format(meta), d=True, s=False)
            matchDum = cmds.listConnections('{}.matchDummy'.format(meta), d=True, s=False)

            # ik to fk again
            ikToFkMatch(startjnt=proxyJoints[0], middleJnt=proxyJoints[1], endJnt=proxyJoints[2], ikCtrl=ikRigs[0], ikPvCtrl=ikRigs[4], ikRotCtrl=ikRigs[2], clvFkCtrl=fkRigs[0], clvIkCtrl=ikRigs[6], foot=1, ballFkCtrl=fkRigs[3], ballIkCtrl=ikRigs[6], matchDum=matchDum[0], matchOffset=[0, 0, 180], move=-20)

            cmds.setKeyframe('{}.translate'.format(ikRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.translate'.format(ikRigs[4]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[6]), breakdown=0)


            # fk
            # animation.fkToIkMatch(startFkCtrl=fkRigs[0], middleFkCtrl=fkRigs[1], endFkCtrl=fkRigs[2], ikCtrl=ikRigs[0], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[3], space='ws', rotateOrders=1)


           ############
            ## arms_L ##
            ############

            meta = '{}meta_arms_L'.format(nss)
            proxyJoints = cmds.listConnections('{}.metaProxyJoints'.format(meta), d=True, s=False)
            ikRigs = cmds.listConnections('{}.metaIkRigs'.format(meta), d=True, s=False)
            fkRigs = cmds.listConnections('{}.metaFkRigs'.format(meta), d=True, s=False)

            # ik to fk
            ikToFkMatch(startjnt=fkRigs[1], middleJnt=fkRigs[2], endJnt=fkRigs[3], ikCtrl=ikRigs[0], ikPvCtrl=ikRigs[4], ikRotCtrl=ikRigs[2], clvFkCtrl=fkRigs[0], clvIkCtrl=ikRigs[6], foot=0, ballFkCtrl=None, ballIkCtrl=None, matchDum=None, matchOffset=None)

            cmds.setKeyframe('{}.translate'.format(ikRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[2]), breakdown=0)
            cmds.setKeyframe('{}.translate'.format(ikRigs[4]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[6]), breakdown=0)


            # fk to ik
            # animation.fkToIkMatch(startFkCtrl=fkRigs[1], middleFkCtrl=fkRigs[2], endFkCtrl=fkRigs[3], ikCtrl=ikRigs[0], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[0], space='ws', rotateOrders=1)

            ############
            ## legs_L ##
            ############

            meta = '{}meta_legs_L'.format(nss)
            proxyJoints = cmds.listConnections('{}.metaProxyJoints'.format(meta), d=True, s=False)
            ikRigs = cmds.listConnections('{}.metaIkRigs'.format(meta), d=True, s=False)
            fkRigs = cmds.listConnections('{}.metaFkRigs'.format(meta), d=True, s=False)
            matchDum = cmds.listConnections('{}.matchDummy'.format(meta), d=True, s=False)

            # ik to fk again
            ikToFkMatch(startjnt=proxyJoints[0], middleJnt=proxyJoints[1], endJnt=proxyJoints[2], ikCtrl=ikRigs[0], ikPvCtrl=ikRigs[4], ikRotCtrl=ikRigs[2], clvFkCtrl=fkRigs[0], clvIkCtrl=ikRigs[6], foot=1, ballFkCtrl=fkRigs[3], ballIkCtrl=ikRigs[6], matchDum=matchDum[0], matchOffset=[0, 0, 0])

            cmds.setKeyframe('{}.translate'.format(ikRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.translate'.format(ikRigs[4]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(ikRigs[6]), breakdown=0)

            # fk to ik
            # animation.fkToIkMatch(startFkCtrl=fkRigs[0], middleFkCtrl=fkRigs[1], endFkCtrl=fkRigs[2], ikCtrl=ikRigs[0], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[3], space='ws', rotateOrders=1)


    cmds.currentTime(playmin)
    cmds.refresh(su=0)

    # elapsed = clock() - start
    # print("%.3f s" % (elapsed,))

match()
