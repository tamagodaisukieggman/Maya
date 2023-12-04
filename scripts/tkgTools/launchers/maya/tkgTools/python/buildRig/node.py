# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon

class Node:
    def __init__(self, node=None, parent=None):
        self.node = node
        self.parent = parent

        self.buf_rename = None

        self.wld_pos = None
        self.wld_rot = None
        self.jnt_orient = None

        self.get_values()

    def get_values(self):
        self.get_parent()
        self.get_wld_trs()
        self.get_jo()

    def get_parent(self):
        parent = cmds.listRelatives(self.node, p=True, f=True) or None
        if parent: self.parent = parent[0]

    def rename(self, prefix=None, suffix=None, replace=None):
        self.buf_rename = brCommon.rename(self.node, prefix, suffix, replace)

    def do_rename(self):
        cmds.rename(self.node, self.buf_rename)

    def get_wld_trs(self):
        self.wld_pos = cmds.xform(self.node, q=True, t=True, ws=True)
        self.wld_rot = cmds.xform(self.node, q=True, ro=True, ws=True)

    def get_jo(self):
        if cmds.objectType(self.node) == 'joint':
            self.jnt_orient = cmds.getAttr(self.node+'.jo')[0]

class Nodes:
    def __init__(self, nodes=None):
        self.nodes = nodes
        self.node_list = []
        for n in self.nodes:
            node = Node(n)
            self.node_list.append(node)

    def rename(self, prefix=None, suffix=None, replace=None):
        [node.rename(prefix, suffix, replace) for node in self.node_list]

    def do_rename(self):
        [node.do_rename() for node in self.node_list]
