# -*- coding: utf-8 -*-
import re
try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import Application
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

class Plugin(MayaPreprocBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        return True

    def execute(self, args):
        global_args = args['global_args']
        export_sets = [x for x in cmds.ls(sl=True, type='objectSet') \
            if cmds.attributeQuery('postproc_edit_set', n=x, ex=True) and cmds.getAttr(x+'.postproc_edit_set')]
        global_args['export_postproc_sets'] = export_sets

        return True, None
        

    def get_label(self):
        return 'Export post-proc set self'

    def order(self):
        return 100000

    def is_editable(self):
        return False

    def default_checked(self):
        return True

    
