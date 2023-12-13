# -*- coding: utf-8 -*-

import re 

try:
    import maya.cmds as cmds
    from workfile_manager_maya import assetutils_maya
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
        if asset.task == 'model' and asset.assetgroup == 'character':
            return True
        else:
            return False


    def execute(self, args):
        poses = cmds.ls(type='dagPose')
        for pose in poses:
            con = cmds.listConnections(pose+'.members', s=True, d=False, c=True, p=True)
            for idx, c in enumerate(con[::2]):
                src = con[idx*2+1]
                src_node, src_attr = src.split('.')
                if cmds.objectType(src_node) != 'joint':
                    dst = con[idx*2]
                    print(('disconnectAttr %s %s' % (src, dst)))
                    cmds.disconnectAttr(src, dst)

        return True, None

    def getlabel(self):
        return 'Disconnect non-joint connections with bindPose'
        #return u'バインドポーズから非ジョイントノードを除去する'
    
    def get_label_jp(self):
        return u'バインドポーズから非ジョイントノードを除去する'

    def order(self):
        return 100

    def default_checked(self):
        return True


    
        