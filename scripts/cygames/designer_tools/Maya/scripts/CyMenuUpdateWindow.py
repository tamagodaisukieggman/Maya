# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import maya.cmds as cmds

import CyRefreshCyMenu

try:
    # Python 2
    reload(CyRefreshCyMenu)
except NameError:
    try:
        # Python 3.4+
        from importlib import reload
        reload(CyRefreshCyMenu)
    except:
        pass

class CyMenuUpdateWindow(object):
    """
    """

    def __init__(self):
        """
        """

        self.window_name = 'CyMenuUpdateWindow'
        self.window = None

    def show_ui(self):
        """
        """

        self.window = cmds.window(self.window_name)
        cmds.window(self.window, e=True, h=20, w=200, sizeable=False)

        cmds.columnLayout(adj=True)

        cmds.button(l=u'Cygames Tools Menuを更新する', c=self.__update, h=20)

        cmds.setParent('..')

        cmds.showWindow()

    def __update(self, _):
        """
        """

        result = CyRefreshCyMenu.refresh(0)
        if result and cmds.window(self.window, q=True, exists=True):
            cmds.deleteUI(self.window)
