# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc


#-- world matrix ---------------------------------------------------------------
def createDecomposeMatrix(src=''):
    srcN = pm.PyNode(src)
    dmat = '{0}_dmat'.format(src)
    if pm.objExists(dmat):
        dmat = pm.PyNode(dmat)
    else:
        dmat = pm.createNode('decomposeMatrix', n=dmat)
        srcN.worldMatrix >> dmat.inputMatrix
    return dmat

# ---- get decompose matrix
def getDecomposeMatrix(src=''):
    dmat = pm.listConnections(src, 
                              s=False, c=False, d=True, p=False, 
                              t='decomposeMatrix')
    if dmat:
        return dmat[0]
    else:
        print (createDecomposeMatrix(src))

# ----- world connection
def worldConnection(src='', tgt=''):
    # -- target node
    srcNode = pm.PyNode(src)
    tgtNode = pm.PyNode(tgt)

    dmat = getDecomposeMatrix(src)
    if not dmat:
        dmat = createDecomposeMatrix(src)

    for at in ['t', 'r', 's']:
        for ax in ['x', 'y', 'z']:
            pm.setAttr('{0}.{1}{2}'.format(tgtNode.name(), at, ax), l=False)
            pm.connectAttr('{0}.o{1}{2}'.format(dmat.name(), at, ax), 
                           '{0}.{1}{2}'.format(tgtNode.name(), at, ax), f=True)
            pm.setAttr('{0}.{1}{2}'.format(tgtNode.name(), at, ax), l=True)

    tgtNode.shxy.set(l=False)
    tgtNode.shxz.set(l=False)
    tgtNode.shyz.set(l=False)
    dmat.oshx >> tgtNode.shxy
    dmat.oshy >> tgtNode.shxz
    dmat.oshz >> tgtNode.shyz
    tgtNode.shxy.set(l=True)
    tgtNode.shxz.set(l=True)
    tgtNode.shyz.set(l=True)
    
    tgtNode.useOutlinerColor.set(1)
    tgtNode.outlinerColor.set(0.87,0.87,0.37)


#-- run
def wldMatrix(tgt=[]):
    log = ''
    if tgt:
        for i in pm.ls(sl=True):
            wld = '{0}_wld'.format(i.name())
            if not pm.objExists(wld):
                wld = pm.createNode('transform', n='{0}_wld'.format(i))
            worldConnection(i, wld)
            log += 'wld connection         : {0} -> {1}\n'.format(i.name(), wld.name())
    print (log)
    return log



#-- Joint Label ----------------------------------------------------------------


def setJointLabel(tgt='', s=0, t=0, l=''):
    tgt = pm.PyNode(tgt)
    tgt.side.set(s)
    tgt.typ.set(t)
    if t == 18:
        tgt.otherType.set(l)


