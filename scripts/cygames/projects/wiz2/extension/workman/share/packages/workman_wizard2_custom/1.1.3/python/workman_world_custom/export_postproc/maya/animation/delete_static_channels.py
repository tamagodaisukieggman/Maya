try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return [Application.Maya, 
                Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False
            
    def order(self):
        return 9
        
    def execute(self, args):
        cmds.delete(staticChannels=True, unitlessAnimationCurves=False, hierarchy='below', controlPoints=0, shape=1)
        
        return True

    def default_checked(self):
        return True

    def getlabel(self):
        return 'Delete Static Channels'

    