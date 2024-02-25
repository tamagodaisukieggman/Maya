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

    def constraints(self, pos=True, rot=True, scl=True, mo=False, stretchy_axis=None):
        options = {
            'mo':mo
        }
        if pos:
            cmds.pointConstraint(self.node, self.to_node, w=True, **options)
        if rot:
            ori_con = cmds.orientConstraint(self.node, self.to_node, w=True, **options)[0]
            cmds.setAttr(ori_con+'.interpType', 2)
        if scl:
            if stretchy_axis:
                skip_ops = ['x', 'y', 'z']
                skip_ops.remove(stretchy_axis)
                options['skip'] = skip_ops

            if cmds.objExists(self.to_node+'.ssc'):
                cmds.setAttr(self.node+'.ssc', cmds.getAttr(self.to_node+'.ssc'))
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

    def constraints_nodes(self, pos=True, rot=True, scl=True, mo=False, stretchy_axis=None):
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

def constraint_from_local_matrix(sel=None, pos=True, rot=True, scl=True, shr=True):
    if not sel:
        sel = cmds.ls(os=1)
    connect_src = sel[0]
    connect_dst = sel[1]

    mmx = cmds.createNode('multMatrix', ss=1)
    dcmx = cmds.createNode('decomposeMatrix', ss=1)

    src_pa = cmds.listRelatives(connect_src, p=1, f=1)
    if src_pa:
        src_parents = src_pa[0].split('|')[::-1]

    else:
        src_parents = None

    dup = cmds.duplicate(connect_dst, po=1)
    cmds.parent(dup[0], connect_src)
    cmds.setAttr('{}.matrixIn[0]'.format(mmx), *cmds.getAttr('{}.matrix'.format(dup[0])),  type='matrix')
    cmds.delete(dup)

    # cmds.setAttr('{}.matrixIn[1]'.format(mmx), *cmds.getAttr('{}.matrix'.format(connect_dst)),  type='matrix')
    cmds.connectAttr('{}.matrix'.format(connect_src), '{}.matrixIn[1]'.format(mmx), f=1)

    if src_parents:
        for i, p in enumerate(src_parents):
            if '' == p:
                pass
            else:
                # print('dst', p)
                # cmds.setAttr('{}.matrixIn[{}]'.format(mmx, i+2), *cmds.getAttr('{}.matrix'.format(p)),  type='matrix')
                cmds.connectAttr('{}.matrix'.format(p), '{}.matrixIn[{}]'.format(mmx, i+2), f=1)

        next_connect = len(src_parents)

    else:
        next_connect = 0


    dst_pa = cmds.listRelatives(connect_dst, p=1, f=1)
    if dst_pa:
        dst_parents = dst_pa[0].split('|')

    else:
        dst_parents = None

    if dst_parents:
        for j, p in enumerate(dst_parents):
            if '' == p:
                pass
            else:
                # print('src', p)
                # cmds.setAttr('{}.matrixIn[{}]'.format(mmx, next_connect+j+1), *cmds.getAttr('{}.matrix'.format(p)),  type='matrix')
                mmx_num = next_connect+j+2
                cmds.connectAttr('{}.inverseMatrix'.format(p), '{}.matrixIn[{}]'.format(mmx, mmx_num), f=1)

    # cmds.connectAttr('{}.inverseMatrix'.format(connect_src), '{}.matrixIn[{}]'.format(mmx, mmx_num+1), f=1)
    cmds.connectAttr('{}.matrixSum'.format(mmx), '{}.inputMatrix'.format(dcmx), f=1)
    if rot:
        cmds.connectAttr('{}.outputRotate'.format(dcmx), '{}.r'.format(connect_dst), f=1)
    if pos:
        cmds.connectAttr('{}.outputTranslate'.format(dcmx), '{}.t'.format(connect_dst), f=1)
    if scl:
        cmds.connectAttr('{}.outputScale'.format(dcmx), '{}.s'.format(connect_dst), f=1)
    if shr:
        cmds.connectAttr('{}.outputShear'.format(dcmx), '{}.shear'.format(connect_dst), f=1)
