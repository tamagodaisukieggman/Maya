# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.node as brNode
reload(brCommon)
reload(brNode)

class Transform(brNode.Node):
    def __init__(self, node=None, offsets=['_offset']):
        super(Transform, self).__init__(node=node)
        self.offsets = offsets

    def create(self):
        if not cmds.objExists(self.node):
            cmds.createNode('transform', n=self.node, ss=True)

    def do_offset(self):
        for offset in self.offsets:
            node_offset = self.node + offset

            if not cmds.objExists(node_offset):
                cmds.createNode('transform', n=node_offset, ss=True)

            cmds.matchTransform(node_offset, self.node)

            if self.parent:
                cmds.parent(node_offset, self.parent)

            cmds.parent(self.node, node_offset)

class Transforms(brNode.Nodes):
    """
    import maya.cmds as cmds
    from imp import reload

    import buildRig.transform as brTrs
    reload(brTrs)

    trs = brTrs.Transforms(nodes=['grp', 'offset', 'space', 'mocap', 'drv'])
    trs.nodes_rename(prefix='prefix_', suffix=None, replace=None)
    trs.node_rename_list # Result: ['prefix_grp', 'prefix_offset', 'prefix_space', 'prefix_mocap', 'prefix_drv'] #
    trs.create()
    """
    def __init__(self, nodes=None, offsets=['_offset']):
        super(Transforms, self).__init__(nodes=nodes)
        self.offsets = offsets

    def create(self):
        for n in self.nodes:
            trs = Transform(n)
            trs.create()

    def do_offset(self):
        for n in self.nodes:
            trs = Transform(n, self.offsets)
            trs.do_offset()

    def do_parent(self, reverse=False):
        parent = None
        if reverse:
            nodes = [n for n in self.nodes[::-1]]
        else:
            nodes = [n for n in self.nodes]
        for i, n in enumerate(nodes):
            if i == 0:
                pass
            else:
                cmds.parent(n, parent)
            parent = n

    def nodes_rename(self, prefix=None, suffix=None, replace=None):
        self.rename(prefix, suffix, replace)
        if self.node_rename_list:
            self.nodes = self.node_rename_list
            self.get_node_objects()
