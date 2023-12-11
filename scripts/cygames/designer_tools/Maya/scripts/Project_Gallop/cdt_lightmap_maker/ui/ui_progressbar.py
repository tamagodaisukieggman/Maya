# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel


# ===================================================
def start_progress(title_name=''):
    cmds.progressWindow(
        title=title_name, status='', isInterruptable=True, min=0, max=100)


# ===================================================
def update_progress(amount, info):
    cmds.progressWindow(edit=True, progress=amount * 100.0, status=info)

    if cmds.progressWindow(query=True, isCancelled=True):
        return False

    return True


# ===================================================
def end_progress():
    cmds.progressWindow(endProgress=True)
