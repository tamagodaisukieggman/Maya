# -*- coding: utf-8 -*-

from workfile_manager import p4utils
from workfile_manager.plugin_utils import Application
from cylibassetdbutils import assetdbutils

try:
    from workman_world_custom.asset_actions.maya import publish_parts_base_maya
except:
    pass

from Qt import QtWidgets, QtCore, QtGui

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

class Plugin(publish_parts_base_maya.BasePlugin):
    def apps_executable_on(self):
        return [Application.Maya,
            Application.Standalone,]

    def is_asset_eligible(self, asset):
        if asset.area() != 'work':
            return False
        if asset.task != 'animation':
            return False

        return True

    def getlabel(self):
        return 'Publish animations'

    
    def is_valid_part(self, part, asset, tags):
        return True

    def postproc_name(self):
        return 'postproc_publish_split_motion_maya'

    def allow_multi_items(self):
        return True

    def additional_args(self, args):
        args['frame_range'] = None
        args['frame_rate'] = None
