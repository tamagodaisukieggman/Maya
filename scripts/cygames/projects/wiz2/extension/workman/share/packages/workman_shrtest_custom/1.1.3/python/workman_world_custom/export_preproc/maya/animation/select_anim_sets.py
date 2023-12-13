# -*- coding: utf-8 -*-
import re 

try:
    import maya.cmds as cmds
    from workfile_manager_maya import assetutils_maya
except:
    pass

from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

class Plugin(MayaPreprocBase, object):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'animation' and asset.assetgroup == 'character':
            return True
        else:
            return False


    def execute(self, args):
        cmds.ls(sl=True)

        buf = cmds.ls('::all_sets')
        if len(buf) > 0:
            #cmds.select(buf, ne=True, add=True)

            #global_args['deselect_in_writing'] = deselect
            global_args = args['global_args']
            self.add_intermediate_selection(global_args, buf)


        return True, None

    def getlabel(self):
        return 'Select animation sets'
    
    def get_label_jp(self):
        return u'アニメーション用のセットの選択'

    def get_discription(self):
        return u''

    def order(self):
        return 999999 # must execute before preproc:preproc_select_postproc_edit_set

    def default_checked(self):
        return True

    def is_editable(self):
        return False


    
        