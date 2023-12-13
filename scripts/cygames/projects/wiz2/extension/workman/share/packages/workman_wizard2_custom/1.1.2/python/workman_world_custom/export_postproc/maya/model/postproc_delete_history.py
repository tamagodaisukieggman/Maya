try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'model':
            return True
        else:
            return False
            
    def order(self):
        return 100

    def execute(self, args):
        from maya import mel
        cmds.select(cmds.ls(type='mesh'))
        mel.eval('doBakeNonDefHistory( 1, {"prePost" })')
        return True

    def getlabel(self):
        return 'Delete History'

    def default_checked(self):
        return True

    def is_editable(self):
        return True