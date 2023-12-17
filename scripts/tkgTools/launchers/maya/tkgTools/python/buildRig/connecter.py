# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.node as brNode
import buildRig.grps as brGrp
import buildRig.joint as brJnt
import buildRig.libs.control.draw as brDraw
import buildRig.transform as brTrs
reload(brNode)
reload(brGrp)
reload(brJnt)
reload(brDraw)
reload(brTrs)

class Connecter(brNode.Node):
    def __init__(self, node=None, to_node=None):
        super(Connecter, self).__init__(node=node)
        self.to_node = to_node

    def connect_same_attrs(self, attrs=None):
        for at in attrs:
            cmds.connectAttr(self.node+'.{}'.format(at), self.to_node+'.{}'.format(at), f=True)

    def constraints(self, pos=True, rot=True, scl=True, mo=False, stretchy_axis='x'):
        options = {
            'mo':mo
        }
        if pos:
            cmds.pointConstraint(self.node, self.to_node, w=True, **options)
        if rot:
            ori_con = cmds.orientConstraint(self.node, self.to_node, w=True, **options)[0]
            cmds.setAttr(ori_con+'.interpType', 2)
        if scl:
            skip_ops = ['x', 'y', 'z']
            skip_ops.remove(stretchy_axis)
            options['skip'] = skip_ops
            cmds.scaleConstraint(self.node, self.to_node, w=True, **options)

class Connecters:
    def __init__(self, nodes=None, to_nodes=None):
        self.nodes = nodes
        self.to_nodes = to_nodes

    def connect_same_attrs_nodes(self, attrs=None):
        if len(self.nodes) == 1:
            for tn in self.to_nodes:
                for n in self.nodes:
                    connecter = Connecter(n, tn)
                    connecter.connect_same_attrs(attrs)
        else:
            for n, tn in zip(self.nodes, self.to_nodes):
                connecter = Connecter(n, tn)
                connecter.connect_same_attrs(attrs)

    def constraints_nodes(self, pos=True, rot=True, scl=True, mo=False, stretchy_axis='x'):
        if len(self.nodes) == 1:
            for tn in self.to_nodes:
                for n in self.nodes:
                    connecter = Connecter(n, tn)
                    connecter.constraints(pos, rot, scl, mo, stretchy_axis)
        else:
            for n, tn in zip(self.nodes, self.to_nodes):
                connecter = Connecter(n, tn)
                connecter.constraints(pos, rot, scl, mo, stretchy_axis)

    def connect_inverse_scale(self, ):
        parent_fk = None
        for n in self.nodes:
            if parent_fk:
                
                cmds.connectAttr(parent_fk+'.inverseMatrix', n+'.offsetParentMatrix', f=True)
            parent_fk = n