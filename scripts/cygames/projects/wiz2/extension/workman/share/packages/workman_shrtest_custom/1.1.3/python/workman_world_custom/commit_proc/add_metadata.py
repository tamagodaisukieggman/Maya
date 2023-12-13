# -*- coding: utf-8 -*-

import os
import shutil
import re
import copy
import subprocess

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

from workfile_manager.plugin_utils import OnCommitProcBase, Application

class Plugin(OnCommitProcBase, object):
    def __init__(self):
        self.init()
    
    def init(self):
        pass
    
    def apps_executable_on(self):
        return [
            Application.Maya,
            Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        return True

    
    def execute(self, args):
        sel_org = cmds.ls(sl=True)

        meshtr_done = []
        for mesh in cmds.ls(type='mesh'):
            meshtr = cmds.listRelatives(mesh, p=True, pa=True)[0]
            if meshtr in meshtr_done:
                continue
            
            leafname = meshtr
            attrname = 'workman_maya_nodename'
            try:
                cmds.addAttr(meshtr, ln=attrname, dt='string')
            except:
                pass
            cmds.setAttr('%s.%s' % (meshtr, attrname), leafname, type='string')    

            meshtr_done.append(meshtr)

        #
        gls = cmds.ls(type='GLSLShader')
        if gls is None:
            gls = []
        attrname = 'Constant_Normal_Vector'
        for n in gls:
            src = cmds.getAttr(n+'.shader')
            if 'WorldSkin.ogsfx' not in src:
                continue
            #if not cmds.attributeQuery(attrname, ex=True, n=n):
            #    cmds.addAttr(n, ln=attrname, at='bool', ct='HW_shader_parameter')
            v = cmds.getAttr(n+'.Use_Normal_Map')
            #print('v:', v)
            cmds.setAttr(n+'.'+attrname, not v)

        cmds.select(sel_org, ne=True)

    def getlabel(self):
        return 'Add Metadata'

    def order(self):
        return 99999

    def get_args(self):
        return None

    def default_checked(self):
        return True

    def is_editable(self):
        return False


