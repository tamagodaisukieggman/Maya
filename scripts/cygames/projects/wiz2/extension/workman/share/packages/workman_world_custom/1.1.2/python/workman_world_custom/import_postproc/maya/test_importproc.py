# -*- coding: utf-8 -*-
from __future__ import print_function

from cylibassetdbutils import assetdbutils
from workfile_manager.plugin_utils import ImportPostprocBase, PluginType, Application
from workfile_manager import p4utils
from workfile_manager.ui import uiutils, ui_table_engine

from Qt import QtWidgets

try:
    from workfile_manager_ue import assetutils_ue, cmds
except:
    pass

try:
    import unreal
    alib = unreal.EditorAssetLibrary()
except:
    pass

import os


db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()


class Plugin(ImportPostprocBase):
    def application(self):
        return Application.UnrealEngine

    def getlabel(self):
        return 'TEST PROC'

    def _is_asset_to_blueprintify(self, adata):
        return True
        

    def execute(self, args):
        print ('xxxxx args:', args)
            
        return True


    


    def apps_executable_on(self):
        return [Application.Maya]

    def is_asset_eligible(self, asset):
        return True
