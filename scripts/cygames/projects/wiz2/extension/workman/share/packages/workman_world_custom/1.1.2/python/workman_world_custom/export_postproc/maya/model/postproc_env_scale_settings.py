from __future__ import print_function
try:
    import maya.cmds as cmds
except:
    pass

import json
import os
import re

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def application(self):
        return Application.Maya

    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.assetgroup == 'environment' and asset.task == 'model':
            return True
        else:
            return False

    def order(self):
        return 100

    def execute(self, args):
        selection = args['global_args']['selection']
        parent = []
        rootObjects = []
        for lp in selection:
            if cmds.objExists(lp) == True:
                if cmds.objectType(lp) != "transform" :
                    continue
            else:
                continue
                
            parent = [lp]
            while parent != None:
                if cmds.listRelatives(parent,ap=True,pa=True) == None:
                    break
                parent = cmds.listRelatives(parent,ap=True,pa=True)
            if parent != []:
                if parent[0] not in rootObjects:
                    rootObjects.extend(parent)
        
        if len(rootObjects) >= 1: 
            tempGroup = cmds.group(em=True,name = "__temp_group",w=True)
            cmds.parent(rootObjects,tempGroup)
            cmds.scale(6, 6, 6, r=1)
            rootObjects = cmds.listRelatives(tempGroup,c=True,pa=True)
            cmds.parent(rootObjects,w=1)
            cmds.delete(tempGroup)
            cmds.makeIdentity(rootObjects,n=0, s=1, r=0, t=1, apply=True, pn=1)
        
        else:
            cmds.warning("Target object does not exist.")

    def getlabel(self):
        return 'x6_Scale_Settings'

    def default_checked(self):
        return False

    def is_editable(self):
        return True