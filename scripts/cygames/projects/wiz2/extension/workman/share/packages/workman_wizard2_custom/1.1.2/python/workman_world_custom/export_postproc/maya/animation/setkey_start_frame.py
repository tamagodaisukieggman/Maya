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
        min = cmds.playbackOptions(q=True, min=True)
        cmds.currentTime(min)

        ro = cmds.ls(ro=True)
        if ro is None:
            ro = []
        nodes = cmds.ls()
        if nodes is None:
            nodes = []
        nodes = [x for x in nodes if x not in ro]
        if len(nodes) > 0:
            cmds.setKeyframe(nodes)
        
        return True

    def default_checked(self):
        return True

    def getlabel(self):
        return 'Set Keyframe on Start'

    
    
