# -*- coding: utf-8 -*-

import maya.mel as mm
import maya.cmds as cmds
import maya.api.OpenMaya as om2


def _delete_anim_curves(nodes):
    # アニメーションカーブの削除
    connections = cmds.listConnections(nodes.fullPathName(), s=True, d=True)
    if not connections:
        return

    list_ = om2.MSelectionList()
    for c in connections:
        list_.add(c)
    iter_ = om2.MItSelectionList(list_)
    iter_.setFilter(om2.MFn.kAnimCurve)
    iter_.itemType()
    while not iter_.isDone():
        if iter_.itemType() == om2.MItSelectionList.kDNselectionItem:
            cmds.delete(iter_.getStrings())
        iter_.next()


def _get_node(name):
    nodeList = om2.MSelectionList()
    nodeList.add(name, True)
    return om2.MFnDagNode(nodeList.getDagPath(0))


def _get_target_node(name):
    nodeList = om2.MSelectionList()
    nodeList.add(name, True)
    for i in range(nodeList.length()):
        path = nodeList.getDagPath(i)
        if 'ply00_m_000_000' not in str(path):
            return om2.MFnDagNode(path)

    return om2.MFnDagNode()


def main():
    print('player stealth kill script')

    startFrame = cmds.playbackOptions(query=1, minTime=1)
    currentFrame = cmds.currentTime(query=1)
    frameRate = mm.eval('currentTimeUnitToFPS')
    print('startFrame   : {0}'.format(startFrame))
    print('currentFrame : {0}'.format(currentFrame))
    print('frameRate    : {0}'.format(frameRate))
    time = (currentFrame - startFrame) / frameRate

    # root01 に相手をアタッチする位置を仕込む
    targetAttachNode = _get_node(u'ply00_m_000_000:root01_mtp_ctrl')
    # 相手の move_ctrl と一致させたいのでノードを接続する
    _delete_anim_curves(targetAttachNode)
    targetMoveNode = _get_target_node(u'*:move_ctrl')
    for type in ['.translate', '.rotate']:
        cmds.connectAttr(targetMoveNode.fullPathName() + type, targetAttachNode.fullPathName() + type, f=True)

    # root02 には開始時点での相手の位置を記録する
    cmds.currentTime(startFrame)
    targetNode = _get_node(u'ply00_m_000_000:root02_mtp_ctrl')
    _delete_anim_curves(targetNode)
    for type in ['.translate', '.rotate']:
        for axis in ['X', 'Y', 'Z']:
            name = type + axis
            cmds.setAttr(targetNode.fullPathName() + name, cmds.getAttr(targetMoveNode.fullPathName() + name))

    # プレイヤーのルート
    rootNode = _get_node(u'ply00_m_000_000:move_proxy_jnt')

    # 開始位置の距離を計算
    cmds.currentTime(startFrame)
    targetMtx = om2.MMatrix(cmds.getAttr(targetAttachNode.fullPathName() + '.worldMatrix'))
    rootMtx = om2.MMatrix(cmds.getAttr(rootNode.fullPathName() + '.worldMatrix'))
    targetTrans = om2.MVector(targetMtx.getElement(3, 0), targetMtx.getElement(3, 1), targetMtx.getElement(3, 2))
    rootTrans = om2.MVector(rootMtx.getElement(3, 0), rootMtx.getElement(3, 1), rootMtx.getElement(3, 2))
    startLen = (targetTrans - rootTrans).length()
    print('startRoot    : {0}'.format(rootTrans))
    print('startTarget  : {0}'.format(targetTrans))
    print('startTrans   : {0}'.format(targetTrans - rootTrans))

    # つかみ位置の時間に設定
    cmds.currentTime(currentFrame)

    # つかみ位置の距離を計算
    targetMtx = om2.MMatrix(cmds.getAttr(targetAttachNode.fullPathName() + '.worldMatrix'))
    rootMtx = om2.MMatrix(cmds.getAttr(rootNode.fullPathName() + '.worldMatrix'))
    targetTrans = om2.MVector(targetMtx.getElement(3, 0), targetMtx.getElement(3, 1), targetMtx.getElement(3, 2))
    rootTrans = om2.MVector(rootMtx.getElement(3, 0), rootMtx.getElement(3, 1), rootMtx.getElement(3, 2))
    endLen = (targetTrans - rootTrans).length()
    print('endRoot      : {0}'.format(rootTrans))
    print('endTarget    : {0}'.format(targetTrans))
    print('endTrans     : {0}'.format(targetTrans - rootTrans))

    # pelvis01 の平行移動にパラメータを代入
    outNode = _get_node(u'ply00_m_000_000:pelvis01_C_mtp_ctrl')
    _delete_anim_curves(outNode)
    cmds.setAttr(outNode.fullPathName() + '.translateX', time * 100)  # 単位をメートルにして格納しておく
    cmds.setAttr(outNode.fullPathName() + '.translateY', startLen)
    cmds.setAttr(outNode.fullPathName() + '.translateZ', (startLen - endLen))

    # root03 にはつかみ時点での自分の位置を記録する
    holdTargetNode = _get_node(u'ply00_m_000_000:root03_mtp_ctrl')
    _delete_anim_curves(holdTargetNode)
    rootMtx = om2.MMatrix(cmds.getAttr(rootNode.fullPathName() + '.worldMatrix'))
    targetTrans = om2.MVector(rootMtx.getElement(3, 0), rootMtx.getElement(3, 1), rootMtx.getElement(3, 2))
    cmds.select(holdTargetNode.fullPathName(), r=True)
    cmds.move(targetTrans.x, targetTrans.y, targetTrans.z, ws=True)
    rot = om2.MQuaternion()
    rot.setValue(rootMtx)
    rot = rot.asEulerRotation().asVector()
    cmds.rotate(rot.x, rot.y, rot.z, ws=True, forceOrderXYZ=True)


if __name__ == '__main__':
    main()
