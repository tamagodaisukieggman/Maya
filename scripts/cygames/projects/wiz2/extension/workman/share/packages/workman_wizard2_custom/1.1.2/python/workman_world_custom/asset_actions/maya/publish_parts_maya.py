# -*- coding: utf-8 -*-
from __future__ import print_function
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
        if asset.assetgroup != 'character':
            return False

        return True

    def getlabel(self):
        return 'Publish parts'

    
    def is_valid_part(self, part, asset, tags):
        def is_hie(tag_type):
            try:
                parent = [x for x in db.tag_types if x['name']==tag_type][0]['parent']
            except:
                return False

            if parent is None:
                return False

            return True

        tags = list(set(tags))

        tags = copy.deepcopy(tags)
        tags = [x for x in tags if is_hie(x[0])]

        tag_types = [x[0] for x in tags]
        if 'char-part' in tag_types:
            for i, t in enumerate(tags):
                if t[0] == 'char-part':
                    tags[i] = (t[0], part)
        else:
            tags.append(('char-part', part))

        cache = db.find_cache_hie(asset, tags)
        if cache is None:
            return False
        else:
            return True

    def postproc_name(self):
        return 'postproc_publish_parts'
