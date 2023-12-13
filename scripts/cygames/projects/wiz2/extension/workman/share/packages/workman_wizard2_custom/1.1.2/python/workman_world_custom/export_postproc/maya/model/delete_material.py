from __future__ import print_function
try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils

db = assetdbutils.DB.get_instance()

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
        tags = args['tags']
        for t in tags:
            tag_type, tag_value = t
            if tag_type == 'environment-type' and tag_value == 'col':
                break
        else:
            return False

        print('This is collision asset.')

        buf = cmds.ls(type='shadingEngine')
        if len(buf) > 0:
            cmds.delete(buf)
        buf = cmds.ls(mat=True)
        if len(buf) > 0:
            cmds.delete(buf)

        print('Materials deleted.')

        return True

    def getlabel(self):
        return 'Delete Materials for Collision Asset'

    def default_checked(self):
        return True

    def is_editable(self):
        return False