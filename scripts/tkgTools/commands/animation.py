# -*- coding: utf-8 -*-
import maya.cmds as cmds

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
