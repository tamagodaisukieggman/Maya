# -*- coding: utf-8 -*-
import os
import copy

from Qt import QtCore, QtGui, QtWidgets



import workfile_manager.ui.uiutils as uiutils
from cylibassetdbutils import assetdbutils, assetutils

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass
from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

class Plugin(MayaPreprocBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True 
        else:
            return False


    def execute(self, args):
        global_args = args['global_args']
        self.add_intermediate_selection(global_args, cmds.ls(dag=True))
        return True, None
        

    def get_label(self):
        return 'Select DAG nodes'

    def order(self):
        return 1000001 # must not execute before pre-process:preproc_select_postproc_edit_set!!!

    def is_editable(self):
        return False

    def default_checked(self):
        return True

