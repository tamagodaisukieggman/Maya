# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re
import traceback

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.node as brNode
reload(brCommon)
reload(brNode)

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

class Joints(brNode.Nodes):
    """
import maya.cmds as cmds
from imp import reload

import buildRig.joint as brJnt
reload(brJnt)

sel = cmds.ls(os=True)
jnts = brJnt.Joints(nodes=sel)
jnts.copy()
jnts.rename(prefix='prefix_', suffix=None, replace=None)
jnts.do_rename()
    """
    def __init__(self, nodes=None):
        super(Joints, self).__init__(nodes=nodes)
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

def create_joints(nodes=None, prefix=None, suffix=None, replace=['_copy', '']):
    jnts = Joints(nodes=nodes)
    jnts.copy()
    copy_jnts = Joints(nodes=jnts.copies)
    copy_jnts.rename(prefix=prefix, suffix=suffix, replace=replace)
    copy_jnts.do_rename()
    copy_jnts.get_node_objects()

    return copy_jnts


# jnt.rename(prefix='PrEfIx_', suffix='_suffix', replace=['joint2', 'JNT2'])
# jnt.do_rename()
