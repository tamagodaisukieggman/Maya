# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re
import traceback

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.node as brNode
import buildRig.transform as brTrs
reload(brCommon)
reload(brNode)
reload(brTrs)

class Joint(brNode.Node):
    def __init__(self, node=None):
        super(Joint, self).__init__(node=node)

    def create(self):
        if not cmds.objExists(self.node):
            cmds.createNode('joint', n=self.node, ss=True)

    def merge_rotation(self):
        set_wr = cmds.xform(self.node, q=True, ro=True, ws=True)
        cmds.setAttr('{}.jo'.format(self.node), *(0, 0, 0))
        cmds.xform(self.node, ro=set_wr, ws=True, a=True)

    def set_ssc(self, set_bool=False):
        cmds.setAttr(self.node+'.ssc', set_bool)

    def duplicate(self, new_name=['', '_dup', None]):
        self.rename(*new_name)
        self.dups = cmds.duplicate(self.node, rc=True, n=self.buf_rename)
        if len(self.dups) > 1:
            cmds.delete(self.dups[1::])
        self.dup = self.dups[0]
        if self.parent:
            cmds.parent(self.dup, w=True)

class Joints:
    def __init__(self, nodes=None):
        self.nodes = nodes
        self.copies = []

    def copy(self, new_name=['', '_copy', None]):
        for j in self.nodes:
            jnt = Joint(j)
            jnt.duplicate(new_name)
            if jnt.parent:
                dup_pa = brCommon.rename(jnt.parent.split('|')[-1], *new_name)
                if cmds.objExists(dup_pa):
                    cmds.parent(jnt.dup, dup_pa)

            self.copies.append(jnt.dup)

    def merge_rotation(self):
        for j in self.nodes:
            jnt = Joint(j)
            jnt.merge_rotation()

    def set_ssc(self):
        for j in self.nodes:
            jnt = Joint(j)
            jnt.set_ssc()


# jnt.rename(prefix='PrEfIx_', suffix='_suffix', replace=['joint2', 'JNT2'])
# jnt.do_rename()
