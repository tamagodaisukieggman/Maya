# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os
from dccUserMayaSharePythonLib import ui


class WindowManageUi(object):

    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

    def delOverwrapWindow(self):
        if pm.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        self.w = pm.window(self.window_name, t=self.window_name)
        pm.columnLayout(adj=True)
        pm.rowLayout(nc=2)
        pm.button(l='minimized', w=220, c=pm.Callback(self._minimized))
        pm.button(l='reset', w=100, c=pm.Callback(self._reset))
        pm.setParent('..')
        pm.rowLayout(nc=2)
        pm.button(l='active', w=220, c=pm.Callback(self._active))
        pm.button(l='delete', w=100, c=pm.Callback(self._delete))

    def _initWm(self):
        self.wm = ui.WindowManage([self.window_name])

    def _minimized(self):
        self._initWm()
        self.wm.minimized()

    def _active(self):
        self._initWm()
        self.wm.active()

    def _reset(self):
        self._initWm()
        y, x = pm.window(self.window_name, q=True, topLeftCorner=True)
        self.wm.reset(x, y, 100, 100)

    def _delete(self):
        if pm.confirmDialog(
            title='Confirm', message='Delete all windows?', button=['Yes', 'No'],
            defaultButton='Yes', cancelButton='No', dismissString='No',
                p=self.window_name):
            self._initWm()
            self.wm.delete()


def main():
    wm = WindowManageUi()
    wm.initUi()
    wm.w.show()
