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
        def merge_color_set(mesh, css):
            if css is None or len(css) < 2:
                return
            
            cmds.polyBlendColor(mesh, bcn=css[0], src=css[1], dst=css[1], bfn=2, bwa=0, bwb=0, bwc=0, bwd=0)
            cmds.polyColorSet(mesh, delete=True, colorSet=css[0])

            css = css[1:]
            merge_color_set(mesh, css)

        for mesh in cmds.ls(type='mesh'):
            css = cmds.polyColorSet(mesh, q=True, acs=True)
            merge_color_set(mesh, css)

        return

    def getlabel(self):
        return 'Merge color sets'

    def order(self):
        return 100

    def get_args(self):
        return None

    def default_checked(self):
        return True

    def is_editable(self):
        return False


