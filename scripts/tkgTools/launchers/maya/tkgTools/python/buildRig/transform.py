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
    def __init__(self, node=None, type='transform'):
        super(Transform, self).__init__(node=node)

        self.type = type

    def create(self):
        if not cmds.objExists(self.node):
            if self.type == 'transform':
                cmds.createNode('transform', n=self.node, ss=True)
            elif self.type == 'joint':
                cmds.createNode('joint', n=self.node, ss=True)
                cmds.setAttr(self.node+'.drawStyle', 2)

class Transforms(brNode.Nodes):
    """
import maya.cmds as cmds
from imp import reload

import buildRig.transform as brTrs
reload(brTrs)

# 新規作成
trs = brTrs.Transforms(nodes=['grp', 'offset', 'space', 'mocap', 'drv'], offsets=False)
trs.nodes_rename(prefix='prefix_', suffix=None, replace=None)
trs.create()
trs.do_parent(reverse=False)

# Transformしたら実行すると値が更新される
for node_object in trs.node_list:
    node_object.get_values()

# コントローラのオフセットノード作成
sel = cmds.ls(os=True)
trs = brTrs.Transforms(nodes=['grp', 'offset', 'space', 'mocap', 'drv', sel[0]], offsets=True)
trs.nodes_rename(prefix=None, suffix=None, replace=['CTL', 'ctrl'])
trs.create()
trs.do_parent(reverse=False)
    """
    def __init__(self, nodes=None, offsets=False, type='transform'):
        super(Transforms, self).__init__(nodes=nodes)
        self.offsets = offsets
        self.type = type

        if self.offsets:
            buf_nodes = []
            ctrl = self.nodes[-1]
            for i, n in enumerate(self.nodes):
                if i == len(self.nodes)-1:
                    buf_nodes.append(n)
                else:
                    buf_nodes.append('{}_{}'.format(ctrl, n))

            self.nodes = buf_nodes
            self.get_node_objects()

    def create(self):
        for i, n in enumerate(self.nodes):
            trs = Transform(n, self.type)
            if self.offsets and i == len(self.nodes)-1:
                if self.node_list[i].buf_rename:
                    self.node_list[i].do_rename()
            else:
                trs.create()

        self.get_node_objects()

        if self.offsets:
            ctrl = self.node_list[-1].node
            for i, n in enumerate(self.node_list[:-1:]):
                cmds.matchTransform(n.node, ctrl)

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
                pa = cmds.listRelatives(n, p=True) or None
                if not pa:
                    cmds.parent(n, parent)
                    if self.type == 'joint':
                        cmds.makeIdentity(n, apply=True, t=True, r=True, s=True, n=False, pn=True)
            parent = n

    def do_parent_root(self):
        for i, n in enumerate(self.nodes):
            if i == 0:
                pass
            else:
                n_pa = cmds.listRelatives(n, p=True) or []
                if not self.nodes[0] in n_pa:
                    cmds.parent(n, self.nodes[0])

    def nodes_rename(self, prefix=None, suffix=None, replace=None):
        self.rename(prefix, suffix, replace)

def create_transforms(nodes=['grp', 'offset', 'space', 'mocap', 'drv', 'ctrl'], offsets=True,
                      prefix=None, suffix=None, replace=None, type='transform'):
    trs = Transforms(nodes=nodes, offsets=offsets, type=type)
    trs.nodes_rename(prefix=prefix, suffix=suffix, replace=replace)
    trs.create()
    trs.do_parent(reverse=False)
    return trs
