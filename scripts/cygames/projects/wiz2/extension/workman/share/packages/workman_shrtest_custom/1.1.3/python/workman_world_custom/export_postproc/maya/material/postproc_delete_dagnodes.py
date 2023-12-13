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
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'material':
            return True
        else:
            return False

    def order(self):
        return 100

    def execute(self, args):
        cmds.delete(cmds.ls(dag=True))
        return True

    def getlabel(self):
        return 'Delete Dag'

    def default_checked(self):
        return True

    def is_editable(self):
        return False
        