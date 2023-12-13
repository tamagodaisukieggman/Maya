# -*- coding: utf-8 -*-
try:
    import maya.cmds as cmds
    import maya.mel as mel
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
        if asset.task == 'model':
            return True
        else:
            return False

    def execute(self, args):
        #add collision objectSet
        cmds.select(cmds.ls("col_*",type="objectSet"),add=True,ne=True)
        return (True, None)

    def getlabel(self):
        return 'Select collision sets'

    def get_label_jp(self):
        return u'コリジョン用セットの選択'

    def order(self):
        return 1001

    def default_checked(self):
        return True