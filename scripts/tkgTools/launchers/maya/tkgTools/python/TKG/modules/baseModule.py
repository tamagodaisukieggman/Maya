# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

import TKG.regulation as tkgRegulation
reload(tkgRegulation)

class Module:
    def __init__(self, side=None, module=None):
        if not side:
            self.side = 'Cn'
        else:
            self.side = side

        if not module:
            self.module = 'default'
        else:
            self.module = module

        self.module_parent = '{}_{}_MODULE'.format(self.side, self.module)

        self.rig_top = 'RIG'
        self.base_rig_grps = ['MODULES', 'MODEL', 'SKEL']
        self.rig_modules = self.base_rig_grps[0]
        self.rig_model = self.base_rig_grps[1]
        self.rig_skel = self.base_rig_grps[2]

        if not cmds.objExists(self.rig_top):
            cmds.createNode('transform', n=self.rig_top, ss=True)

        for n in self.base_rig_grps:
            if not cmds.objExists(n):
                cmds.createNode('transform', n=n, ss=True)
                cmds.parent(n, self.rig_top)

        self.nodes_top = None
        self.ctrls_top = None

        self.create()

    def create(self):
        if not cmds.objExists(self.module_parent):
            cmds.createNode('transform', n=self.module_parent, ss=True)
        parent = cmds.listRelatives(self.module_parent, p=True) or None
        if not parent:
            cmds.parent(self.module_parent, self.rig_modules)
        elif not self.rig_modules in parent:
            cmds.parent(self.module_parent, self.rig_modules)

    def create_module_parts(self, module=None):
        self.nodes_top = '{}_'.format(module) + tkgRegulation.node_type_rename(node=self.module_parent, type='nodes_top')
        self.ctrls_top = '{}_'.format(module) + tkgRegulation.node_type_rename(node=self.module_parent, type='ctrls_top')

        self.module_tops = [self.nodes_top, self.ctrls_top]
        for n in self.module_tops:
            if not cmds.objExists(n):
                cmds.createNode('transform', n=n, ss=True)
            parent = cmds.listRelatives(n, p=True) or None
            if not parent:
                cmds.parent(n, self.module_parent)
            elif not self.module_parent in parent:
                cmds.parent(n, self.module_parent)

