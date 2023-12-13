try:
    import maya.cmds as cmds
except:
    pass

from workman_world_custom.export_postproc.maya.all import postproc_publish_parts_base_maya

class Plugin(postproc_publish_parts_base_maya.BasePlugin):
    def is_asset_eligible(self, asset):
        if asset.task == 'model':
            return True
        else:
            return False

    def getlabel(self):
        return 'Publish environment asset'
