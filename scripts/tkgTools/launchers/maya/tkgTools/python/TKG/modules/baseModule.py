# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

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

        self.create()

    def create(self):
        if not cmds.objExists(self.module_parent):
            cmds.createNode('transform', n=self.module_parent, ss=True)
        parent = cmds.listRelatives(self.module_parent, p=True) or None
        if not parent:
            cmds.parent(self.module_parent, self.rig_modules)
        elif not self.rig_modules in parent:
            cmds.parent(self.module_parent, self.rig_modules)