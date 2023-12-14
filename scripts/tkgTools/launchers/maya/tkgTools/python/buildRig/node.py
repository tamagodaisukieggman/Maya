# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.common as brCommon
reload(brCommon)

class Node:
    def __init__(self, node=None, parent=None):
        self.node = node
        self.parent = parent
        self.full_path = None

        self.buf_rename = None

        self.wld_pos = None
        self.wld_rot = None
        self.jnt_orient = None
        self.shapes = None

        if cmds.objExists(self.node):
            self.get_values()

    def get_values(self):
        self.get_parent()
        self.get_full_path()
        self.get_wld_trs()
        self.get_jo()
        self.get_shapes()

    def get_parent(self):
        parent = cmds.listRelatives(self.node, p=True, f=True) or None
        if parent: self.parent = parent[0]

    def get_full_path(self):
        full_path = cmds.ls(self.node, l=True) or None
        if full_path: self.full_path = full_path[0]

    def rename(self, prefix=None, suffix=None, replace=None):
        self.buf_rename = brCommon.rename(self.node, prefix, suffix, replace)
        return self.buf_rename

    def do_rename(self):
        cmds.rename(self.node, self.buf_rename)

    def get_wld_trs(self):
        self.wld_pos = cmds.xform(self.node, q=True, t=True, ws=True)
        self.wld_rot = cmds.xform(self.node, q=True, ro=True, ws=True)

    def get_jo(self):
        if cmds.objectType(self.node) == 'joint':
            self.jnt_orient = cmds.getAttr(self.node+'.jo')[0]

    def get_shapes(self):
        self.shapes = cmds.listRelatives(self.node, s=True) or None

    def freezeTransform(self, pos=True, rot=True, scl=True):
        cmds.makeIdentity(self.node, apply=True, t=pos, r=rot, s=scl, n=False, pn=True)

    def set_preferredAngle(self):
        cmds.joint(self.node, e=True, spa=True, ch=True)

    def unparent(self):
        pa = cmds.listRelatives(self.node, p=True) or None
        if pa:
            cmds.parent(self.node, w=True)


class Nodes:
    def __init__(self, nodes=None):
        self.nodes = nodes
        self.node_list = []
        self.get_node_objects()

    def rename(self, prefix=None, suffix=None, replace=None):
        self.nodes = [node.rename(prefix, suffix, replace) for
                                                    node in self.node_list]

    def do_rename(self):
        [node.do_rename() for node in self.node_list]

    def get_node_objects(self):
        self.node_list = []
        for n in self.nodes:
            node = Node(n)
            self.node_list.append(node)
