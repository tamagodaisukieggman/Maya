# -*- coding: utf-8 -*-
import re 

try:
    import maya.cmds as cmds
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



    def init(self):
        super(Plugin, self).init()
        self.types = {
            'transform' : {'postfix': 'gp'}, 
            'mesh' : {'postfix': 'geoShape'},
            'shadingEngine' : {'postfix': 'sg'},
            'joint' : {'postfix': 'jnt'},
        }
        for m in cmds.ls(mat=True):
            tp = cmds.objectType(m)
            if tp not in self.types:
                self.types[tp] = {'postfix': 'mtl'}

        self.undeletables = []
        
        buf = cmds.ls() # "ls -ud" doesn't work. That also returns deleable nodes.
                        # In addition, that causes the scene modification flag to get on.
        for n in buf:
            sn = re.sub('.*[|]', '', n)
            try:
                cmds.rename(n, sn)
            except:
                self.undeletables.append(n)
        

    def execute(self, args):
        for n in cmds.ls():
            res = self.__exec_node(n)
            if res is None:
                continue
            if not res:
                self.results.append(n)
        if len(self.results) == 0:
            return True, None
        else:
            return False, self.results
        

    def getlabel(self):
        return 'Check node name'

    def get_label_jp(self):
        return u'ノード名の確認'

    def order(self):
        return 100

    def default_checked(self):
        return True


    def __exec_node(self, n):
        if n in self.undeletables:
            return True

        tp = cmds.objectType(n)
        if tp not in list(self.types.keys()):
            return None

        sn = re.sub('.*\|', '', n)
        
        postfix = '_' + self.types[tp]['postfix']
        if tp == 'transform':
            buf = cmds.listRelatives(n, c=True, f=True)
            if buf is not None:
                hit = False
                for c in buf:
                    if cmds.objectType(c) in list(self.types.keys()):
                        hit = True
                        break
                if not hit:
                    return None
                buf = [x for x in buf if cmds.objectType(x) == 'mesh']
                if buf is not None and len(buf) > 0:
                    postfix = '_geo'

        #self.info('Checking... ' + sn)
        expr = '^[^0-9_][^_]*(_[^0-9_][^_]*|)(_[0-9]{2,3}|)' + postfix + '$'
        #print 'expr: ', expr
        if not re.search(expr, sn):
            return False
        return True

        