# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
import buildRig.node as brNode

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

class Transforms:
    def __init__(self, nodes=None, offsets=['_offset']):
        self.nodes = nodes
        self.offsets = offsets

    def create(self):
        for n in self.nodes:
            trs = Transform(n)
            trs.create()

    def do_offset(self):
        for n in self.nodes:
            trs = Transform(n, self.offsets)
            trs.do_offset()
