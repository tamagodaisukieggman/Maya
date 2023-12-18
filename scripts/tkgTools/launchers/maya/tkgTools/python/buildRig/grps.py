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
        self.rig_grps = ['rig', 'geo_grp', 'module_grp', 'skel_grp']
        self.create()
        self.char_grp = self.rig_grps[0]
        self.model_grp = self.rig_grps[1]
        self.rig_grp = self.rig_grps[2]
        self.skel_grp = self.rig_grps[3]

        # addAttr
        if not cmds.objExists(self.char_grp+'.geoVisibility'):
            cmds.addAttr(self.char_grp, ln="geoVisibility", dv=1, at='double', min=0, max=1, k=1)
            cmds.connectAttr(self.char_grp+'.geoVisibility', '{}.v'.format(self.model_grp), f=1)

        if not cmds.objExists(self.char_grp+'.geoOverrideEnabled'):
            cmds.addAttr(self.char_grp, ln="geoOverrideEnabled", dv=1, at='double', min=0, max=1, k=1)
            cmds.connectAttr(self.char_grp+'.geoOverrideEnabled', '{}.overrideEnabled'.format(self.model_grp), f=1)

        if not cmds.objExists(self.char_grp+'.geoChangeDisplayType'):
            cmds.addAttr(self.char_grp, ln="geoChangeDisplayType", en="Normal:Template:Reference:", at="enum", k=1)
            cmds.connectAttr(self.char_grp+'.geoChangeDisplayType', '{}.overrideDisplayType'.format(self.model_grp), f=1)
            cmds.setAttr(self.char_grp+'.geoChangeDisplayType', 2)

        if not cmds.objExists(self.char_grp+'.jntVisibility'):
            cmds.addAttr(self.char_grp, ln="jntVisibility", dv=1, at='double', min=0, max=1, k=1)
            cmds.setAttr(self.char_grp+'.jntVisibility', 0)
        if not cmds.objExists(self.char_grp+'.jntOverrideEnabled'):
            cmds.addAttr(self.char_grp, ln="jntOverrideEnabled", dv=1, at='double', min=0, max=1, k=1)
        if not cmds.objExists(self.char_grp+'.jntChangeDisplayType'):
            cmds.addAttr(self.char_grp, ln="jntChangeDisplayType", en="Normal:Template:Reference:", at="enum", k=1)

        if not cmds.objExists(self.char_grp+'.rigVisibility'):
            cmds.addAttr(self.char_grp, ln="rigVisibility", dv=1, at='double', min=0, max=1, k=1)
            cmds.connectAttr(self.char_grp+'.rigVisibility', '{}.v'.format(self.rig_grp), f=1)

    def create(self):
        trs = brTrs.Transforms(self.rig_grps)
        trs.create()
        trs.do_parent_root()


class RigModule(RigBase):
    def __init__(self,
                 module=None,
                 side=None):
        super().__init__()
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

        cmds.setAttr(self.module_grp+'.v', 0)
