# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds

class Module:
    def __init__(self, module=None, side=None):
        if not module:
            self.module = 'default'
        else:
            self.module = module

        if not side:
            self.side = 'Cn'
        else:
            self.side = side

        self.module_name = '{}_{}_MODULE'.format(self.module, self.side)

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

    def create(self):
        if not cmds.objExists(self.module_name):
            cmds.createNode('transform', n=self.module_name, ss=True)