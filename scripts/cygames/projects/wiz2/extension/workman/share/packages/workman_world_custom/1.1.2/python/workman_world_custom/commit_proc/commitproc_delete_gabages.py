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
    def apps_executable_on(self):
        return [
            Application.Maya,
            Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        return True

    
    def execute(self, args):
        buf = cmds.ls(type='displayLayer')
        try:
            cmds.delete(buf)
        except:
            pass
        return

    def getlabel(self):
        return 'Delete Gabages'

    def order(self):
        return 10000

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

