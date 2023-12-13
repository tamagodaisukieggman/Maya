# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm

import mtk.utils.wrapper as wrapper

import cyllistaClipConfig
import cyllistaJointInfo

if not cmds.pluginInfo('fbxmaya', q=True, l=True):
    cmds.loadPlugin("fbxmaya")


def changeMoveDistanceRateFromAnimationEvent(mdrInfos):
    roots = cmds.ls(cyllistaClipConfig.ROOT_JOINT_NAME, recursive=1)

    joints, mtp, move = cyllistaJointInfo.collectJoints(rootJoint=roots[0])

    mdrInfoTuples = mdrInfos.split(",")
    for mdrInfoTuple in mdrInfoTuples:
        if not mdrInfoTuple:
            continue
        start, end, scale_ = mdrInfoTuple.split()
        start = int(start)
        end = int(end)
        scale_ = 1.0 / float(scale_)
        # move distance rate
        cmds.scaleKey(joints[0], iub=True, t=(start, end), vs=scale_, vp=0, at="translateZ")
        cmds.scaleKey(move[0], iub=True, t=(start, end), vs=scale_, vp=0, at="translateZ")


def changeMotionSpeedFromAnimationEvent(msInfos):
    roots = cmds.ls(cyllistaClipConfig.ROOT_JOINT_NAME, recursive=1)
    cmds.select(roots[0], hierarchy=True)
    selected = cmds.ls(sl=True)

    msInfoTuples = msInfos.split(",")
    maxFrame = cmds.playbackOptions(q=True, max=True)
    lastMaxFrame = maxFrame
    moveEnd = 0.0
    for msInfoTuple in msInfoTuples:
        if not msInfoTuple:
            continue
        start, end, scale_ = msInfoTuple.split()
        start = int(start) - moveEnd
        end = int(end) - moveEnd
        scale_ = 1.0 / float(scale_)

        if scale_ > 1.0:
            moveEnd = (scale_ - 1.0) * (end - start)
            lastMaxFrame = lastMaxFrame + moveEnd
        else:
            moveEnd = end - (end - start) * scale_
            lastMaxFrame = lastMaxFrame - moveEnd

        for s in selected:
            animAttributes = cmds.listAnimatable(s)
            for a in animAttributes:
                # scale key
                if scale_ > 1.0:
                    cmds.playbackOptions(aet=lastMaxFrame)
                    cmds.playbackOptions(max=lastMaxFrame)
                    cmds.keyframe(s, edit=True, t=(end, maxFrame), r=True, tc=moveEnd, at=a)
                    cmds.scaleKey(s, iub=True, t=(start, end), tp=start, ts=scale_, fp=start, fs=scale_, vs=1, vp=0, at=a)
                else:
                    cmds.scaleKey(s, iub=True, t=(start, end), tp=start, ts=scale_, fp=start, fs=scale_, vs=1, vp=0,
                                  at=a)
                    cmds.keyframe(s, edit=True, t=(end, maxFrame), r=True, tc=-moveEnd, at=a)


    # 変わった分 playback を更新する
    cmds.playbackOptions(max=lastMaxFrame)


def main(namespace, msInfos, mdrInfos):
    print("namespace: %s, motionSpeed: %s, moveDistanceRate: %s" % (namespace, msInfos, mdrInfos))
    mayaPath = wrapper.getCurrentSceneFilePath() # mayaPath = cmds.file(q=True, sn=True)のMaya2022におけるバグ回避
    if not mayaPath:
        print("failed scaling keys from aevt")
        return
    # import reference
    _importReference()

    # Remove the specified namespace
    _removeSpecifiedNamespace(ns=namespace)

    # select joints
    roots = cmds.ls(cyllistaClipConfig.ROOT_JOINT_NAME, recursive=1)
    cmds.select(roots[0], hierarchy=True)

    # change top root name
    _changeTransformRootName()

    # bake
    import mtku.maya.menus.animation.bakesimulation as bakesimulation
    bakesimulation.main()

    # change motion speed/move distance rate
    changeMotionSpeedFromAnimationEvent(msInfos)
    changeMoveDistanceRateFromAnimationEvent(mdrInfos)

    # export fbx
    OUTPUT_FOLDER_NAME = "scaled_keys_fbx"
    work_directory = os.path.dirname(mayaPath)
    output_directory = work_directory + "/" + OUTPUT_FOLDER_NAME
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    baseName = os.path.basename(mayaPath)
    baseName, ext = os.path.splitext(baseName)
    basePath = output_directory + "/" + baseName
    filePath = basePath + ".fbx"
    mm.eval('FBXExport -f "{}" -s '.format(filePath))

    # Save the scene as ma data and close
    cmds.file(f=True, new=True)


def _removeSpecifiedNamespace(ns):
    cmds.namespace(mergeNamespaceWithParent=True, removeNamespace=ns)


def _importReference():
    while True:
        refs = [f for f in cmds.file(q=1, r=1) if cmds.referenceQuery(f, il=1)]
        nums = len(refs)
        if nums == 0:
            break
        else:
            for i in range(nums):
                cmds.file(refs[i], ir=1)


def _changeTransformRootName():
    sel = pm.ls("root")
    num = len(sel)
    for i in range(num):
        if sel[i].type() == "joint":
            pass
        else:
            cmds.rename("|root", "root_")
