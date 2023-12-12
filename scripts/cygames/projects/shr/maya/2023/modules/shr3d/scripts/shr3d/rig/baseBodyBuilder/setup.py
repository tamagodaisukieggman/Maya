# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc

from math import degrees
from maya.api.OpenMaya import MFnTransform, MGlobal, MTransformationMatrix


#-- world matrix --------------------------------------------
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
    res = []
    if tgt:
        for i in tgt:
            src = pm.PyNode(i)
            wld = '{0}_wld'.format(src.name())
            if not pm.objExists(wld):
                wld = pm.createNode('transform', n='{0}_wld'.format(i))
                worldConnection(i, wld)
            else:
                log += f'wld connection : {src.name()} already exists.\n'
                continue
            
            log += f'wld connection : {src.name()} -> {wld.name()}\n'
        res.append(wld)
        print(log)

    else:
        log += 'Please select some transform nodes to create matrix connection.'
        print(log)
    return res


#-- compose joint orient
def composeJointOrient(tgt): #-- rotate --> joint orient
    #-- joint list
    jtList = pm.ls(tgt, typ='joint')

    #-- unselected
    if not jtList:
        print ('Please select joint node to compose joint orient.')
        return

    #-- compose rotation
    for jt in jtList:
        #-- get rotate value
        t = MFnTransform(MGlobal.getSelectionListByName(jt.name()).getDagPath(0))
        t_mtx = MTransformationMatrix(t.transformationMatrix())

        #-- rotateOrder
        e_rot = t_mtx.rotation()
        n_rot = [degrees(e_rot.x), degrees(e_rot.y), degrees(e_rot.z)]

        #-- set rotate
        jt.r.set(0,0,0)
        jt.ra.set(0,0,0)
        jt.jo.set(*n_rot)


#-- compose rotation
def composeRotate(tgt): #-- joint orient --> rotate
    #-- joint list
    jtList = pm.ls(tgt, typ='joint')

    #-- unselected
    if not jtList:
        print ('Please select joint node to compose rotaion.')
        return

    #-- compose rotation
    for jt in jtList:
        #-- get rotate value
        t = MFnTransform(MGlobal.getSelectionListByName(jt.name()).getDagPath(0))
        t_mtx = MTransformationMatrix(t.transformationMatrix())

        #-- rotateOrder
        t_mtx.reorderRotation(t.rotationOrder())
        e_rot = t_mtx.rotation()
        n_rot = [degrees(e_rot.x), degrees(e_rot.y), degrees(e_rot.z)]

        #-- set rotate
        jt.jo.set(0,0,0)
        jt.ra.set(0,0,0)
        jt.r.set(*n_rot)


