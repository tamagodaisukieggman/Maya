# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om2

def anim_the_world(func):
    def wrapper(*args, **kwargs):
        try:
            cmds.refresh(su=1)

            cur_time=cmds.currentTime(q=1)
            if cmds.autoKeyframe(q=True, st=True):
                autoKeyState = True
            else:
                autoKeyState = False

            cmds.autoKeyframe(state=False)

            start = cmds.playbackOptions(q=True, min=True)
            end = cmds.playbackOptions(q=True, max=True)

            animstart = cmds.playbackOptions(q=True, ast=True)
            animend = cmds.playbackOptions(q=True, aet=True)

            func(*args, **kwargs)

            cmds.currentTime(cur_time)
            cmds.autoKeyframe(state=autoKeyState)

            cmds.playbackOptions(min=start)
            cmds.playbackOptions(max=end)

            cmds.playbackOptions(ast=animstart)
            cmds.playbackOptions(aet=animend)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

    return wrapper

def func_per_frames(func):
    def wrapper(*args, **kwargs):
        try:
            cmds.refresh(su=1)

            cur_time=cmds.currentTime(q=1)
            if cmds.autoKeyframe(q=True, st=True):
                autoKeyState = True
            else:
                autoKeyState = False

            cmds.autoKeyframe(state=False)

            start = cmds.playbackOptions(q=True, min=True)
            end = cmds.playbackOptions(q=True, max=True)

            animstart = cmds.playbackOptions(q=True, ast=True)
            animend = cmds.playbackOptions(q=True, aet=True)

            for i in range (int(start), int(end+1)):
                cmds.currentTime(i, e=True)
                func(*args, **kwargs)

            cmds.currentTime(cur_time)
            cmds.autoKeyframe(state=autoKeyState)

            cmds.playbackOptions(min=start)
            cmds.playbackOptions(max=end)

            cmds.playbackOptions(ast=animstart)
            cmds.playbackOptions(aet=animend)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

    return wrapper

def get_anim_curves(nodes=None):
    connections = cmds.listConnections(nodes, s=True, d=True)
    if not connections:
        return

    connection_lists = om2.MSelectionList()
    [connection_lists.add(connection) for connection in connections]
    iter_ = om2.MItSelectionList(connection_lists, om2.MFn.kAnimCurve)
    anim_curves = list()
    while not iter_.isDone():
        # cmds.delete(iter_.getStrings())
        anim_curves.append(iter_.getStrings()[0])
        iter_.next()

    return anim_curves

def move_anim_start(nodes=None, start=None):
    anim_curves = get_anim_curves(nodes)
    [cmds.keyframe(anc, e=True, iub=True, r=True, o='over', tc=start) for anc in anim_curves]


def delete_anim_curves(nodes=None, delete_types=None):
    anim_curves = get_anim_curves(nodes)

    if delete_types:
        for anim_curve in anim_curves:
            dst_plugs = cmds.listConnections(anim_curve, d=True, p=True)
            for dt in delete_types:
                translate_connects = [p for p in dst_plugs if dt in p]
                if translate_connects:
                    cmds.delete(anim_curve)

    else:
        cmds.delete(anim_curves)
