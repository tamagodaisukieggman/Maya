# -*- coding: utf-8 -*-
from __future__ import print_function
try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass
from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

class Plugin(MayaPreprocBase, object):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'model':
            return True
        else:
            return False

    def execute(self, args):
        all_node = cmds.listRelatives(cmds.ls(sl=True),ad=True,type="transform",pa=True)
        if all_node is None:
            return (True, None) 
        
        for lp in cmds.ls(sl=True):
            if cmds.objectType(lp) == "transform":
                all_node.append(lp)

            error_transforms = []
            for node in all_node:
                if cmds.listRelatives(node,c=True,pa=True) == None:
                    continue
                has_transform = False
                has_shape = False
                for lp in cmds.listRelatives(node,c=True,pa=True):
                    if cmds.objectType(lp) == "transform":
                        has_transform = True
                    
                    elif cmds.objectType(lp) == "mesh":
                        has_shape = True
                    
                if has_transform and has_shape:
                    error_transforms.append(node)
                        
            if error_transforms != []:
                for lp in error_transforms:
                    cmds.warning("{} >> There is a problem with the hierarchy".format(lp))
                return (False, error_transforms)

            else:
                return (True, None)    
        


    def getlabel(self):
        return 'Check_Transform_Hierarchy'

    def get_label_jp(self):
        return u'トランスフォームの階層構造のチェック'

    def get_discription(self):
        return u'シェイプのトランスフォームの子に別のシェイプのトランスフォームが存在した場合、UE4の仕様上エラーとなるためこれをエラーとして返します。'

    def order(self):
        return 1001

    def default_checked(self):
        return True