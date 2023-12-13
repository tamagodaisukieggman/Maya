# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


class Method(object):

    # ===============================================
    @staticmethod
    def check_window(window_name):

        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)

        else:
            if cmds.windowPref(window_name, exists=True):
                cmds.windowPref(window_name, remove=True)
