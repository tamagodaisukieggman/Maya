# -*- coding: utf-8 -*-
import re
try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

class Plugin(MayaPreprocBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        return True

    

    def execute(self, args):
        sets = cmds.ls(type='objectSet')
        nodes = []
        for n in sets:
            if re.search('^(([^:]*:)|)textureEditorIsolateSelectSet.*', n):
                nodes.append(n)
        if len(nodes) > 0:
            for n in nodes:
                if not cmds.attributeQuery('memberWireframeColor', ex=True, n=n):
                    continue
                buf = cmds.listConnections(n+'.memberWireframeColor', p=True, c=True, s=False, d=True)
                for i in range(0, len(buf), 2):
                    cmds.disconnectAttr(buf[i], buf[i+1])
                cmds.delete(n)
        
        return True, None
        

    def getlabel(self):
        return 'Delete UVEditor isolate select set'

    def order(self):
        return 1000

    def is_editable(self):
        return False

    def default_checked(self):
        return True
