# -*- coding: utf-8 -*-

import os
import shutil
import re
import copy
import subprocess

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

from workfile_manager.plugin_utils import OnCommitProcBase, Application
from cylibassetdbutils import assetutils, assetdbutils

class Plugin(OnCommitProcBase, object):
    def __init__(self):
        self.init()
    
    def init(self):
        pass
    
    def apps_executable_on(self):
        return [
            Application.Maya,
            Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        return True

    
    def execute(self, args):
        sel = cmds.ls(sl=True)
        for tr in cmds.ls(tr=True):
            if cmds.objectType(tr) == 'joint':
                continue
            cmds.select(tr, ne=True)
            mel.eval('ResetTransformations')

        if len(sel) > 0:
            cmds.select(sel, ne=True)
        else:
            cmds.select(cl=True)
        return

    def getlabel(self):
        return 'Reset transforms'

    def order(self):
        return 100

    def get_args(self):
        return None

    def default_checked(self):
        return True

    def is_editable(self):
        return False

    def module_path(self):
        return None

    def func_in_error(self):
        pass

