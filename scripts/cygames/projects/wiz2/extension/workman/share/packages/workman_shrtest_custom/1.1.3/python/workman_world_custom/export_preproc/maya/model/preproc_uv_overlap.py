# -*- coding: utf-8 -*-
try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase, object):
    def application(self):
        return Application.Maya

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
        if not cmds.pluginInfo('utilcmds', q=True, l=True):
            cmds.loadPlugin('utilcmds')

        buf = cmds.ls(sl=True)
        cmds.select(cmds.ls(type='mesh', ni=True))
        res = mel.eval('findUvOverlappedFaces')
            
        if res and len(res) > 0:
            cmds.select(res)
            self.results = cmds.ls(sl=True)
            cmds.select(buf, ne=True)
            return False, self.results
        else:
            cmds.select(buf, ne=True)
        return True, None

    def getlabel(self):
        return 'Check uv overlap'
    
    def get_label_jp(self):
        return u'uv overlapの確認'

    def order(self):
        return 1000