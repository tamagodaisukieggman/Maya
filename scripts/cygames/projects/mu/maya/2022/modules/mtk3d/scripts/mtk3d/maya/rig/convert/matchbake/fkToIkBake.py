# -*- coding: utf-8 -*-
import timeit
import math
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

def fkToIkMatch(startFkCtrl=None, middleFkCtrl=None, endFkCtrl=None, ikHandle=None, clvIkCtrl=None, clvFkCtrl=None, foot=None):
    import maya.api.OpenMaya as om2

    objExists_sts = True
    objList = [startFkCtrl, middleFkCtrl, endFkCtrl, clvFkCtrl, clvIkCtrl]
    for obj in objList:
        if cmds.objExists(obj) == False:
            objExists_sts = False
    if objExists_sts == False:
        print('object not exists...')
        return

    if foot == None:
        clavicleIkRot = cmds.xform(clvIkCtrl, q=1, ro=1, ws=1)
        cmds.xform(clvFkCtrl, ro=clavicleIkRot, a=1, ws=1)

    jntList = cmds.ikHandle(ikHandle, q=1, jointList=1)
    endJnt = cmds.listRelatives(jntList[(len(jntList)-1)], children=1, type='joint')
    jntList.append(endJnt[0])

    srcFks = [startFkCtrl, middleFkCtrl, endFkCtrl]

    # jtdups = [cmds.duplicate(jt, po=1)[0] for jt in jntList]
    # ctldups = [cmds.duplicate(ctrl, po=1)[0] for ctrl in srcFks]
    """
    for ct in ctldups:
        cmds.setAttr('{}.rotateX'.format(ct), k=True, l=0)
        cmds.setAttr('{}.rotateY'.format(ct), k=True, l=0)
        cmds.setAttr('{}.rotateZ'.format(ct), k=True, l=0)
    """
    # [cmds.orientConstraint(jtdups[i], ctldups[i], w=1) for i in range(len(jtdups))]
    # [cmds.xform(srcFks[j], ro=cmds.xform(ctldups[j], q=1, ro=1, ws=1), a=1, ws=1) for j in range(len(srcFks))]

    for j in range(len(jntList)):
        obj = jntList[j]

        selection = om2.MSelectionList()
        selection.add(obj)
        dag = selection.getDagPath(0)

        transform_fn = om2.MFnTransform(dag)
        quat = transform_fn.rotation(om2.MSpace.kWorld, True)
        euler = transform_fn.rotation(om2.MSpace.kTransform, False)
        m_quat = om2.MQuaternion(quat)

        obj2 = srcFks[j]
        selection2 = om2.MSelectionList()
        selection2.add(obj2)
        dag2 = selection2.getDagPath(0)

        transform_fn2 = om2.MFnTransform(dag2)
        transform_fn2.setRotation(m_quat, om2.MSpace.kWorld)

    # cmds.delete(jtdups, ctldups)

    if foot == True:
        clavicleIkRot = cmds.xform(clvIkCtrl, q=1, ro=1, ws=1)
        cmds.xform(clvFkCtrl, ro=clavicleIkRot, a=1, ws=1)

def match():
    nss_in_joints = cmds.ls('*_proxy_jnt', type='joint', r=1)
    nss_buf = ['{}'.format(nss_in.replace(nss_in.split(':')[-1], '')) for nss_in in nss_in_joints]
    nss_list = list(set(nss_buf))
    try:
        nss_list.remove('')
    except:
        pass
    nss = nss_list[0]

    global fkToIkMatch
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

            # fk to ik
            fkToIkMatch(startFkCtrl=fkRigs[1], middleFkCtrl=fkRigs[2], endFkCtrl=fkRigs[3], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[0], foot=None)

            cmds.setKeyframe('{}.rotate'.format(fkRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[1]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[2]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[3]), breakdown=0)

            ############
            ## legs_R ##
            ############

            meta = '{}meta_legs_R'.format(nss)
            proxyJoints = cmds.listConnections('{}.metaProxyJoints'.format(meta), d=True, s=False)
            ikRigs = cmds.listConnections('{}.metaIkRigs'.format(meta), d=True, s=False)
            fkRigs = cmds.listConnections('{}.metaFkRigs'.format(meta), d=True, s=False)
            matchDum = cmds.listConnections('{}.matchDummy'.format(meta), d=True, s=False)

            # fk to ik
            fkToIkMatch(startFkCtrl=fkRigs[0], middleFkCtrl=fkRigs[1], endFkCtrl=fkRigs[2], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[3], foot=True)

            cmds.setKeyframe('{}.rotate'.format(fkRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[1]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[2]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[3]), breakdown=0)

            ############
            ## arms_L ##
            ############

            meta = '{}meta_arms_L'.format(nss)
            proxyJoints = cmds.listConnections('{}.metaProxyJoints'.format(meta), d=True, s=False)
            ikRigs = cmds.listConnections('{}.metaIkRigs'.format(meta), d=True, s=False)
            fkRigs = cmds.listConnections('{}.metaFkRigs'.format(meta), d=True, s=False)

            # fk to ik
            fkToIkMatch(startFkCtrl=fkRigs[1], middleFkCtrl=fkRigs[2], endFkCtrl=fkRigs[3], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[0], foot=None)

            cmds.setKeyframe('{}.rotate'.format(fkRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[1]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[2]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[3]), breakdown=0)

            ############
            ## legs_L ##
            ############

            meta = '{}meta_legs_L'.format(nss)
            proxyJoints = cmds.listConnections('{}.metaProxyJoints'.format(meta), d=True, s=False)
            ikRigs = cmds.listConnections('{}.metaIkRigs'.format(meta), d=True, s=False)
            fkRigs = cmds.listConnections('{}.metaFkRigs'.format(meta), d=True, s=False)
            matchDum = cmds.listConnections('{}.matchDummy'.format(meta), d=True, s=False)

            # fk to ik
            fkToIkMatch(startFkCtrl=fkRigs[0], middleFkCtrl=fkRigs[1], endFkCtrl=fkRigs[2], ikHandle=ikRigs[1], clvIkCtrl=ikRigs[6], clvFkCtrl=fkRigs[3], foot=True)

            cmds.setKeyframe('{}.rotate'.format(fkRigs[0]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[1]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[2]), breakdown=0)
            cmds.setKeyframe('{}.rotate'.format(fkRigs[3]), breakdown=0)

    cmds.currentTime(playmin)
    cmds.refresh(su=0)
    # elapsed = clock() - start
    # print("%.3f s" % (elapsed,))

match()
