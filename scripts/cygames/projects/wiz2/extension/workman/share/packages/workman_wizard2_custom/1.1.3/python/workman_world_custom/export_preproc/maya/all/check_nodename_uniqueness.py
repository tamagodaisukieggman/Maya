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
        return True


    def execute(self, args):
        buf = cmds.ls(sl=True, l=True)
        if len(buf) == 0:
            return True, None
            
        clds = cmds.listRelatives(buf, ad=True, f=True)
        if type(clds) is list:
            buf += clds
        
        his = cmds.listHistory(buf)
        
        if type(his) is list:
            buf += cmds.ls(his, l=True)

        buf = list(set(buf))

        nodes = {}
        dup = []
        expr = re.compile('[^|:]+:')
        for n_org in buf:
            n = n_org
            n = expr.sub('', n)
            
            if n not in list(nodes.keys()):
                nodes[n] = []
            else:
                dup.append(n)
            
            nodes[n].append(n_org)
            
        if len(dup) > 0:
            for d in dup:
                print(('%s duplicated.' % d , cmds.ls(nodes[d])))
                self.results += nodes[d]

            return False, self.results

        else:
            return True, None
    
        

    def getlabel(self):
        return 'Check node name uniqueness'

    def get_label_jp(self):
        return u'ノード名の一意性を確認'

    def get_discription(self):
        return u''

    def order(self):
        return 100

    def default_checked(self):
        return True


    
        