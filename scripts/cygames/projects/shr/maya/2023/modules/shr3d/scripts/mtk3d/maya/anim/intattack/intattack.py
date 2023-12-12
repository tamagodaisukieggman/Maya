# -*- coding: utf-8 -*-

import maya.mel as mm
import maya.cmds as cmds
import maya.api.OpenMaya as om2

def execute():

    startFrame = cmds.playbackOptions(query=1, minTime=1)
    currentFrame = cmds.currentTime(query=1)
    frameRate = mm.eval('currentTimeUnitToFPS')
    print(startFrame)
    print(currentFrame)
    print(frameRate)

    time = (currentFrame - startFrame) / frameRate
    print(time)

    nodeList = om2.MSelectionList()
    nodeList.add(u'ply00_m_000_000:root02_mtp_ctrl', True)
    targetNode = om2.MFnDagNode(nodeList.getDagPath(0))
    print(targetNode.name())

    nodeList = om2.MSelectionList()
    nodeList.add(u'ply00_m_000_000:move_proxy_jnt', True)
    rootNode = om2.MFnDagNode(nodeList.getDagPath(0))
    print(rootNode.name())

    nodeList = om2.MSelectionList()
    nodeList.add(u'ply00_m_000_000:pelvis01_C_mtp_ctrl', True)
    outNode = om2.MFnDagNode(nodeList.getDagPath(0))
    print(outNode.name())

    cmds.currentTime(startFrame)
    targetMtx = om2.MMatrix(cmds.getAttr(targetNode.fullPathName() + ".matrix"))
    rootMtx = om2.MMatrix(cmds.getAttr(rootNode.fullPathName() + ".matrix"))
    targetTrans = om2.MVector(targetMtx.getElement(3, 0), targetMtx.getElement(3, 1), targetMtx.getElement(3, 2))
    rootTrans = om2.MVector(rootMtx.getElement(3, 0), rootMtx.getElement(3, 1), rootMtx.getElement(3, 2))
    startLen = (targetTrans - rootTrans).length()

    cmds.currentTime(currentFrame)
    targetMtx = om2.MMatrix(cmds.getAttr(targetNode.fullPathName() + ".matrix"))
    rootMtx = om2.MMatrix(cmds.getAttr(rootNode.fullPathName() + ".matrix"))
    targetTrans = om2.MVector(targetMtx.getElement(3, 0), targetMtx.getElement(3, 1), targetMtx.getElement(3, 2))
    rootTrans = om2.MVector(rootMtx.getElement(3, 0), rootMtx.getElement(3, 1), rootMtx.getElement(3, 2))
    endLen = (targetTrans - rootTrans).length()

    # 平行移動にパラメータを代入
    cmds.setAttr(outNode.fullPathName() + ".translateX", time * 100)
    cmds.setAttr(outNode.fullPathName() + ".translateY", startLen)
    cmds.setAttr(outNode.fullPathName() + ".translateZ", (startLen - endLen))
