# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.transform as brTrs
reload(brTrs)

class RigBase:
    def __init__(self):
        self.rig_grps = ['CHAR', 'MODEL', 'RIG', 'SKEL']
        self.create()
        self.char_grp = self.rig_grps[0]
        self.model_grp = self.rig_grps[1]
        self.rig_grp = self.rig_grps[2]
        self.skel_grp = self.rig_grps[3]

    def create(self):
        trs = brTrs.Transforms(self.rig_grps)
        trs.create()
        trs.do_parent_root()

class RigModule(RigBase):
    def __init__(self,
                 module=None,
                 side=None):
        super(RigModule, self).__init__()
        self.module = module
        self.side = side

        if not self.module:
            self.module = 'default'
        if not self.side:
            self.side = 'Cn'

        self.module_base_grp = '{}_{}'.format(self.side, self.module)
        self.module_grp = self.module_base_grp + '_MODULE'
        self.ctrl_grp = self.module_base_grp + '_CONTROL'

        trs = brTrs.Transforms([self.rig_grp, self.module_base_grp])
        trs.create()
        trs.do_parent_root()

        trs = brTrs.Transforms([self.module_base_grp, self.module_grp, self.ctrl_grp])
        trs.create()
        trs.do_parent_root()
