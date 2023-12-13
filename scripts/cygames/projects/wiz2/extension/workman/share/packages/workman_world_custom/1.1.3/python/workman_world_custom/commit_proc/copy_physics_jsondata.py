# -*- coding: utf-8 -*-
from __future__ import print_function
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
        if asset.assetgroup == 'environment' and asset.task == 'model':
            return True
        return False

    
    def execute(self, args):
        from workman_world_custom.export_postproc.maya.model import export_collision_settings
        print('filename: ', args['filename'])
        sn = cmds.file(q=True, sn=True)
        print('sn:', sn)
        share_json_filename = export_collision_settings.get_json_path_from_masterfile(sn)
        print('share_json_filename:', share_json_filename)

        output_json_filename = export_collision_settings.get_json_path_from_masterfile(args['engine_output_path'])
        
        print('output_json_filename: ', output_json_filename)
        output_dir = os.path.dirname(output_json_filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if os.path.exists(output_json_filename):
            subprocess.call('attrib -R "%s"' % output_json_filename)
        shutil.copyfile(share_json_filename, output_json_filename)

        return {'submit_files':[output_json_filename]}

    def getlabel(self):
        return 'Copy Physics Jsondata'

    def order(self):
        return 99900

    def get_args(self):
        return None

    def default_checked(self):
        return True

    def is_editable(self):
        return False


