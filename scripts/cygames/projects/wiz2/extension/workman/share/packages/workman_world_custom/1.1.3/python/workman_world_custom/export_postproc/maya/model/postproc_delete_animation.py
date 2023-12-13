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
        cmds.delete(cmds.ls(type=('animCurveTL', 'animCurveTA', 'animCurveTU')))
        return True

    def getlabel(self):
        return 'Delete Animation'

    def default_checked(self):
        return True

    def is_editable(self):
        return False