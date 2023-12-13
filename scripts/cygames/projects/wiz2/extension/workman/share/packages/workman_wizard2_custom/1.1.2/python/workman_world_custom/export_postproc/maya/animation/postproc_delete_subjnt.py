try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
            Application.MotionBuilder,
            Application.Standalone,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False
            
    def order(self):
        return 25
        
    def execute(self, args):
        import re
        buf = cmds.ls('*_subjnt*', type='joint')
        buf = [x for x in buf if re.search('_subjnt(|_\d+)$', x)]

        if len(buf) > 0:
            cmds.delete(buf)

        #cmds.dgdirty(a=True)
        #
        #for i in range(3):
        #    cmds.currentTime(i)

        return True

    def getlabel(self):
        return 'Delete joints named ~subjnt'

    def default_checked(self):
        return True
