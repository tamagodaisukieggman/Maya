# -*- coding: utf-8 -*-
try:
    import maya.cmds as cmds
    from workfile_manager_maya import assetutils_maya

except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def application(self):
        return Application.Maya

    def apps_executable_on(self):
        return (
            Application.Maya,
            Application.MotionBuilder,
            Application.Standalone,
        )

    def is_asset_eligible(self, asset):
        return True

    def order(self):
        return 1000

    def execute(self, args):
        dels = []
        types = []

        if cmds.pluginInfo('Turtle', q=True, l=True):
            types.append('ilrOptionsNode')
            types.append('ilrUIOptionsNode')
            types.append('ilrBakeLayerManager')
            types.append('ilrBakeLayer')

        for type_ in types:
            buf = cmds.ls(type=type_)
            dels += buf

        locked = cmds.ls(dels, lockedNodes=True)
        try:
            cmds.lockNode(locked, lock=False)
        except:
            import traceback
            print(traceback.format_exc())
        locked = cmds.ls(dels, lockedNodes=True)
        dels = [x for x in dels if x not in locked]

        if len(dels) > 0:
            cmds.delete(dels)


        #try:
        #    cmds.delete(cmds.ls(type='displayLayer'))
        #except:
        #    pass

        

    def getlabel(self):
        return 'Delete Gabages'

    def default_checked(self):
        return True

    def is_editable(self):
        return False