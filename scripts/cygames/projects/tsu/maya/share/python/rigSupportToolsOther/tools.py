# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : rigSupportToolsOther.tools
# Author  : toi
# Version : 0.1.0
# Updata  : 2022/6/13
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
#import maya.mel as mm
import pymel.core as pm
#import os
#import sys
#import stat
#from collections import OrderedDict
#from rigSupportTools import ui as rstui
#from dccUserMayaSharePythonLib import ui
#from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import tsubasa_dumspl as tsubasa
#from dccUserMayaSharePythonLib import common as cm


def addNamespaceAllNodes():
    result = cmds.promptDialog(
        title='AddNamespace', message='Namespace:', button=['OK', 'Cancel'],
        defaultButton='OK',	cancelButton='Cancel', dismissString='Cancel',
        tx=tsubasa.getId(cmds.file(q=True, sn=True)) + '_00')

    if result == 'OK':
        ns = cmds.promptDialog(q=True, text=True)
        if not cmds.namespace(ex=ns):
            cmds.namespace(add=ns)

        ns = ns + ':'

        for n in cmds.ls():
            try:
                if not n.startswith(ns):
                    cmds.rename(n, ns + n)
            except:
                pass


def attrWatcher(node):
    def main():
        w = '{0}___{1}'.format('attr_watcher', node)
        if cmds.window(w, ex=True):
            cmds.deleteUI(w)

        cmds.window(w, t=w, w=300)
        cmds.columnLayout(adj=True)

        set_attrs = cmds.textScrollList(tsl, q=True, selectItem=True)
        for at in set_attrs:
            try:
                cmds.attrControlGrp(a=node + '.' + at)
            except:
                pass
        cmds.showWindow(w)

    priority_attr = ['translate', 'rotate', 'scale']
    attrs = [x for x in cmds.listAttr(node, visible=1) if x not in priority_attr]

    w = 'set_attr_watcher'
    if cmds.window(w, ex=True):
        cmds.deleteUI(w)

    cmds.window(w, t=w, w=300)
    cmds.columnLayout(adj=True)
    tsl = cmds.textScrollList(append=priority_attr, ams=True, selectIndexedItem=(1, 2, 3), h=600)
    cmds.textScrollList(tsl, e=True, append=attrs)
    cmds.button(l='boot window', c=pm.Callback(main))
    cmds.showWindow(w)


def markingColor(nodes, set_color):

    for node in nodes:
        node.useOutlinerColor.set(set_color)
        node.outlinerColor.set((1, 0.43, 0.43))
        node.overrideEnabled.set(set_color)
        node.overrideColor.set(20)

        shape = node.getShape()
        if shape:
            shape.overrideEnabled.set(set_color)
            shape.overrideColor.set(18)


def createJointHierarchy(axis, num):
    target_joint_name = 'joint_hierarchy'
    sels = cmds.ls(sl=True)
    select_joint = [x for x in sels if target_joint_name in x]

    joint_root = ''
    if select_joint:
        joint_root = pm.PyNode(select_joint[0]).root().name()
    else:
        joint_root = cmds.joint(n=target_joint_name)
        cmds.setAttr(joint_root + '.segmentScaleCompensate', False)

    if num == 0:
        cmds.delete(joint_root)
        return

    joints = cmds.ls(joint_root, dag=True)
    bottom_joint = joints[-1]
    cmds.select(bottom_joint)

    joints_num = len(joints)
    if num >= joints_num:
        while num > joints_num:
            new_joint = cmds.joint(n=target_joint_name)
            set_val = 10 if axis[0] == '+' else -10
            cmds.setAttr('{0}.t{1}'.format(new_joint, axis[1]), set_val)

            joints = cmds.ls(joint_root, dag=True)
            joints_num = len(joints)
    else:
        while num < joints_num:
            joints = pm.ls(joint_root, dag=True)
            pm.setAttr(joint_root + '.segmentScaleCompensate', False)
            bottom_joint = joints[-1]
            pm.delete(bottom_joint)

            joints = pm.ls(joint_root, dag=True)
            bottom_joint = joints[-1]
            pm.select(bottom_joint)
            joints_num = len(joints)


