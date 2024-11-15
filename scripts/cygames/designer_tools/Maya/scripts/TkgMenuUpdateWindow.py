# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import maya.cmds as cmds

import TkgRefreshTkgMenu

try:
    # Python 2
    reload(TkgRefreshTkgMenu)
except NameError:
    try:
        # Python 3.4+
        from importlib import reload
        reload(TkgRefreshTkgMenu)
    except:
        pass

class TkgMenuUpdateWindow(object):
    """
    """

    def __init__(self):
        """
        """

        self.window_name = 'TkgMenuUpdateWindow'
        self.window = None

    def show_ui(self):
        """
        """

        self.window = cmds.window(self.window_name)
        cmds.window(self.window, e=True, h=20, w=200, sizeable=False)

        cmds.columnLayout(adj=True)

        cmds.button(l=u'TKG Tools Menuを更新する', c=self.__update, h=20)

        cmds.setParent('..')

        cmds.showWindow()

    def __update(self, _):
        """
        """

        result = TkgRefreshTkgMenu.refresh(0)
        if result and cmds.window(self.window, q=True, exists=True):
            cmds.deleteUI(self.window)
