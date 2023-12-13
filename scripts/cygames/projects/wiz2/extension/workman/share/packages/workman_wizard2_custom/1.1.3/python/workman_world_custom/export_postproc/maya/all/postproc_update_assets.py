# -*- coding: utf-8 -*-
from __future__ import print_function

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils, assetutils

try:
    import maya.cmds as cmds
    import pymel.core as pm
    from workfile_manager_maya import assetutils_maya
except:
    pass

import os, shutil

db = assetdbutils.DB.get_instance()

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya, Application.MotionBuilder, Application.Standalone
        )

    def is_asset_eligible(self, asset):
        return True
            
    def order(self):
        return 999999
    
    def getlabel(self):
        return 'Update assets'

    def default_checked(self):
        return False

    def is_editable(self):
        return False


    def execute(self, args):
        from workfile_manager import cmds as wcmds
        #from workfile_manager import asset_update_utils
        #dccutils = assetutils_maya.MayaUtils.get_instance()
        #updater = asset_update_utils.AssetUpdateUtils(dccutils, force_update=True)

        print('args:', args)
        asset = args['work_asset']
        filename = asset._filename
        print('asset: ', asset.__dict__)
        print('filename: ', filename)
        
        updater = asset.get_updater(filename)
        assert updater is not None

        # p4 sync.
        task = wcmds.Task(interactive=False)
        task.open_workasset(asset, filename, asset.version)
        
        updater.check_update(asset, filename)

        #
        refs = [x['local_path'] for x in db.get_workasset_refs(filename=filename, version=asset.version)]
        files = [filename] + refs
        from workfile_manager import p4utils
        p4u = p4utils.P4Utils.get_instance()
        try:
            p4u.p4_run_xxx('revert', '-a', files)
        except:
            pass

        return True

    
