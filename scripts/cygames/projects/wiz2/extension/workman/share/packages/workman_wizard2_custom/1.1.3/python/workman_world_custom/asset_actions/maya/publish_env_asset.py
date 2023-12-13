# -*- coding: utf-8 -*-

try:
    from workman_world_custom.asset_actions.maya import publish_parts_base_maya    
except:
    pass

from workfile_manager import p4utils
from cylibassetdbutils import assetdbutils



from Qt import QtWidgets, QtCore, QtGui
import re, os, shutil, copy

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

class Plugin(publish_parts_base_maya.BasePlugin):
    def is_asset_eligible(self, asset):
        if asset.area() != 'work':
            return False
        if asset.task != 'model':
            return False
        if asset.assetgroup != 'environment':
            return False

        return True

    def getlabel(self):
        return 'Publish'

    
    def is_valid_part(self, part, asset, tags):
        return True

    def postproc_name(self):
        return 'postproc_publish_env_asset'

    def allow_multi_items(self):
        return True