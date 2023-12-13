# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import os
import sys
import shutil

import pymel.core as pm
import maya.cmds as mc


def attributeExists(node, attr):
    if node == '' or attr == '':
        return False
    if mc.objExists(node) == False:
        return False
    attrList = mc.listAttr(node, sn=True)
    for i in range(len(attrList)):
        if attr == attrList[i]:
            return True
    attrList = mc.listAttr(node)
    for i in range(len(attrList)):
        if attr == attrList[i]:
            return True
    return False



def addSBRAttr():
    attr = 'SimulationBlendRate'
    for i in pm.selected(typ='joint'):
        if not attributeExists(i.name(), attr):
            pm.addAttr(i, ln=attr, at='double', min=0, max=1, dv=1)
            pm.setAttr('{0}.{1}'.format(i.name(), attr), k=True, e=True)
        else:
            print('{0} : {1} attribute already exists.'.format(i.name(), attr))


def deleteSBRAttr():
    attr = 'SimulationBlendRate'
    for i in pm.selected(typ='joint'):
        if attributeExists(i.name(), attr):
            pm.deleteAttr(i, at=attr)


def ishex(v):
    try:
        int(v, 16)
        return True
    except ValueError:
        return False



def getSBRJointlist():
    attr = 'SimulationBlendRate'
    res = []
    for i in pm.ls(typ='joint'):
        if attributeExists(i.name(), attr):
            res.append(i.name())
    return res



def getNameSpace():
    nsList = mc.namespaceInfo(r=True, lon=True)
    nsList.remove(u'UI')
    nsList.remove(u'shared')

    return nsList



def listSort(tgls=[], st=''):
    res = []
    for i in tgls:
        if st in i:
            res.append(i)
    return res



def setKey():
    attr = 'SimulationBlendRate'
    for i in pm.selected(typ='joint'):
        pm.setKeyframe('{0}.{1}'.format(i.name(), attr))


def setKeyValue(v=1):
    attr = 'SimulationBlendRate'
    for i in pm.selected(typ='joint'):
        pm.setAttr('{0}.{1}'.format(i.name(), attr), v)
        pm.setKeyframe('{0}.{1}'.format(i.name(), attr))









