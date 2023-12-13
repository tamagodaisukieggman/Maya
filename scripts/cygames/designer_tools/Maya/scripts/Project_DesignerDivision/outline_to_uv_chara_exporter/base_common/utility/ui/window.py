# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds


# ===============================================
def exists(window_id):

    if cmds.window(window_id, exists=True):
        return True

    return False


# ===============================================
def remove_same_id_window(window_id):

    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id, window=True)

    else:
        if cmds.windowPref(window_id, exists=True):
            cmds.windowPref(window_id, remove=True)
