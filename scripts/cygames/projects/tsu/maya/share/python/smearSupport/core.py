# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import os
import sys
import shutil

import pymel.core as pm
import maya.cmds as mc

from . import command
#reload(command)


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


def getMesh():
    res = ''
    obj = pm.selected()
    if obj:
        msh = obj[0].getShape()
        if pm.nodeType(msh) == 'mesh':
            res = obj[0].name()
    return res


def createBendCage(mesh=''):
    bbv = pm.xform(mesh, bb=True, q=True)
    lng = bbv[5] - bbv[2]
    wid = bbv[3] - bbv[0]

    blm = pm.polyPlane(w=wid, h=lng, sx=1, sy=10, ax=(0,1,0), cuv=2, ch=1, n='bend_cage')
    pm.select(mesh, r=True)
    pm.mel.eval('PolySelectConvert 1;')

    pm.mel.eval('MoveTool;')
    pos = pm.manipMoveContext('Move', p=True, q=True)

    pm.move(0, 0, pos[2], blm[0], a=True)
    pm.select(d=True)
    return blm[0].name()


def createBlurACage(mesh=''):
    obj = pm.PyNode(mesh)
    shp = obj.getShape()

    bat = pm.polyCube(n='blurA_cage', ch=False)
    bas = bat[0].getShape()
    shp.outMesh >> bas.inMesh
    pm.refresh()
    shp.outMesh // bas.inMesh

    deleteHalfMesh(bat[0])
    return bat[0].name()



def createBlurBCage(blurA=''):
    bb = pm.duplicate(blurA, rr=True, n='blurB_cage')
    return bb[0].name()



def deleteHalfMesh(mesh=''):
    res = []
    pm.mel.eval('MoveTool;')
    for i in pm.ls('{0}.f[*]'.format(mesh), fl=True):
        pm.select(i, r=True)
        pos = pm.manipMoveContext('Move', p=True, q=True)
        if pos[1] < 0.0:
            res.append(i)
    pm.select(res, r=True)
    pm.delete()



def bindBendCage(mesh='', jt=[]):
    obj = pm.PyNode(mesh)
    pm.select(obj, r=True)
    pm.select(jt, add=True)
    mc.skinCluster(tsb=True, bm=0, sm=0, nw=1, wd=0)


def selectJoint():
    pm.select(d=True)
    if pm.objExists('_000'):
        pm.select('_000', r=True)

    if pm.objExists('_300'):
        pm.select('_300', add=True)

    if pm.objExists('_301'):
        pm.select('_301', add=True)

    if pm.objExists('_302'):
        pm.select('_302', add=True)

    if pm.objExists('_500'):
        pm.select('_500', add=True)

    if pm.objExists('_501'):
        pm.select('_501', add=True)

    if pm.objExists('_502'):
        pm.select('_502', add=True)


def setJointLabel():
    jtList = pm.selected()

    if len(jtList) == 4:
        for i in jtList:
            if i.name() == '_000':
                i.side.set(0)
                i.typ.set(18)
                i.otherType.set('base')

            if i.name() == '_300' or i.name() == '_500':
                i.rename('_300')
                i.side.set(0)
                i.typ.set(18)
                i.otherType.set('bend')

            if i.name() == '_301' or i.name() == '_501':
                i.rename('_301')
                i.side.set(0)
                i.typ.set(18)
                i.otherType.set('blurA')

            if i.name() == '_302' or i.name() == '_502':
                i.rename('_302')
                i.side.set(0)
                i.typ.set(18)
                i.otherType.set('blurB') 

    else:
        pm.warning('Please select these joints _000, _300, _301, _302.')



def createCtrl():
    jt = pm.PyNode('_000')
    j0 = pm.PyNode('_300')
    j1 = pm.PyNode('_301')
    j2 = pm.PyNode('_302')

    #-- rig_GP
    if not pm.objExists('rig_GP'):
        rg = pm.createNode('transform', n='rig_GP')

    #-- all_ctrl
    if not pm.objExists('all_ctrl'):
        ax = pm.createNode('transform', n='all_ctrl_ax')
        cn = pm.createNode('transform', n='all_ctrl_cnst')
        ac = pm.spaceLocator(n='all_ctrl')
        
        ac.setParent(cn)
        cn.setParent(ax)

        pm.parentConstraint('all_ctrl', '_000', mo=False)
        pm.scaleConstraint('all_ctrl', '_000', mo=False)
        
        ax.setParent('rig_GP')

    #-- smear ctrl
    bax = pm.createNode('transform', n='bend_ctrl_ax')
    bnc = pm.spaceLocator(n='bend_ctrl')
    bac = pm.spaceLocator(n='blurA_ctrl')
    bbc = pm.spaceLocator(n='blurB_ctrl')

    bbc.setParent(bac)
    bac.setParent(bnc)
    bnc.setParent(bax)
    bax.t.set(0,0,100)

    #--parent 
    bax.setParent('all_ctrl')


def setConstraint():
    j1 = pm.PyNode('_301')
    j2 = pm.PyNode('_302')
    bac = pm.PyNode('blurA_ctrl')
    bbc = pm.PyNode('blurB_ctrl')

    #-- connect
    pm.aimConstraint('bend_ctrl', '_300', w=1, aim=(0,0,1), mo=True,
                     u=(0,1,0), wut='objectrotation', wu=(0,1,0), wuo='bend_ctrl_ax')

    bac.t >> j1.t
    bbc.t >> j2.t


def selectSkinClusterFormSkin():
    objList  = pm.ls(sl=True)
    sClsList = []
    for obj in objList:
        skinCls = pm.mel.eval('findRelatedSkinCluster {0};'.format(obj.name()))
        if skinCls:
            sClsList.append(skinCls)
    if len(sClsList) > 1:
        sClsList = list(set(sClsList))
    mc.select(sClsList, r=True)
    return sClsList


def selectJointsFromSkinCluster(disconnect=0):
    selSkinClsList = pm.ls(sl=True, typ='skinCluster')
    mc.select(cl=True)
    for skinCls in selSkinClsList:
        bindJtList = mc.listConnections('{0}.matrix'.format(skinCls.name()), s=1, d=0, t='joint', sh=1)
        mc.select(bindJtList, add=True)
        # -- disconnect objectColorRGB
        if disconnect == True:
            allJtList  = mc.listConnections(skinCls.name(), s=1, d=0, t='joint', sh=1)
            disconnectJtList = list(set(allJtList) - set(bindJtList))
            for jt in disconnectJtList:
                tgtAttrList = mc.listConnections('{0}.objectColorRGB'.format(jt), s=False, p=True, d=True, c=False, t='skinCluster')
                for attr in tgtAttrList:
                    if skinCls.name() in attr:
                        mc.disconnectAttr('{0}.objectColorRGB'.format(jt), attr)
    return [i.name() for i in pm.selected()]



def selectJointsFromSkin():
    res = []
    scs = pm.ls(sl=True, typ='skinCluster')
    if scs:
        for sc in scs:
            scj = mc.listConnections('{0}.matrix'.format(sc), s=1, d=0, t='joint', sh=1)
            for i in scj:
                res.append(i)
        

    obs = pm.ls(sl=True, typ='transform')
    if obs:
        for ob in obs:
            sc  = pm.mel.eval('findRelatedSkinCluster {0};'.format(ob.name()))
            scj = mc.listConnections('{0}.matrix'.format(sc), s=1, d=0, t='joint', sh=1)
            for i in scj:
                res.append(i)

    if res:
        pm.select(list(set(res)), r=True)



def weightDistributer():
    selectSkin = mc.ls(sl=True)
    srcSkin = selectSkin[0]
    for i in range(1, len(selectSkin)):
        mc.select(srcSkin, r=True)
        mc.select(selectSkin[i], add=True)
        mc.copySkinWeights(ia=['label', 'closestJoint'], sa='closestPoint', nm=True)



def bindAndCopy():
    objList = pm.ls(sl=True)
    for i in range(0, len(objList), 2):
        # -- bind
        mc.select(objList[i].name(), r=True)
        skinCls = selectSkinClusterFormSkin()
        selectJointsFromSkinCluster(disconnect=0)
        mc.select(objList[i+1].name(), add=True)
        mc.skinCluster(tsb=True, bm=0, sm=0, nw=1, wd=0)
        # -- weight copy
        mc.select(objList[i].name(), r=True)
        mc.select(objList[i+1].name(), add=True)
        mc.copySkinWeights(ia=['label', 'closestJoint'], sa='closestPoint', nm=True)



def getWeight():
    vt  = pm.filterExpand(sm=31)
    obj = vt[0].split('.')[0]
    sc  = pm.mel.eval('findRelatedSkinCluster {0};'.format(obj))
    jts = pm.skinCluster(sc, inf=True, q=True)
    wts = pm.skinPercent(sc, vt[-1], v=True, q=True)
    
    jwd = {}
    for j, w in zip(jts, wts):
        jwd[j.name()] = w
        
    return jwd


def setWeight(jwd={}):
    vt  = pm.filterExpand(sm=31)
    obj = vt[0].split('.')[0]
    sc  = pm.mel.eval('findRelatedSkinCluster {0};'.format(obj))

    tvl = []
    for j, w in jwd.items():
        tvl.append((j, w))

    for v in vt:
        pm.skinPercent(sc, v, tv=tvl)



def copyWeight(mesh='', sc='', jt=''):
    pm.select(sc, r=True)
    jtList = selectJointsFromSkinCluster()

    obj = pm.PyNode(mesh)
    vt  = pm.ls('{0}.vtx[*]'.format(obj.name()), fl=True)
    sc  = pm.PyNode(sc)

    wt  = {}
    wt['influence'] = jt

    for v in vt:
        wt[v.name()] = pm.skinPercent(sc, v, t=jt, q=True)

    return wt


def getRate(wts={}, wtt={}):
    wv1 = [i for i in wts.values() if isinstance(i, float)] #-- blurB
    wv0 = [i for i in wtt.values() if isinstance(i, float)] #-- blurA

    max_s = max(wv1) #-- blurB
    max_t = max(wv0) #-- blurA

    rate = max_t / max_s

    return rate


def pasetWeight(mesh='', sc='', wts={}, tjt=''):
    obj = pm.PyNode(mesh)
    vt  = pm.ls('{0}.vtx[*]'.format(obj.name()), fl=True)
    sc  = pm.PyNode(sc)
    tjt = pm.PyNode(tjt)

    #-- add influence
    njt = wts['influence']
    try:
        pm.skinCluster(sc, lw=True, wt=0, dr=4, ai=njt, e=True)
    except:
        pass

    wtt = {}
    #-- get wtt
    for v in vt:
        wtt[v.name()] = pm.skinPercent(sc, v, t=tjt, q=True)

    #-- get rate
    rate = getRate(wts, wtt)
    print(rate)

    #-- weight lock
    pm.select(sc, r=True)
    jtList = selectJointsFromSkinCluster()
    for i in jtList:
        pm.setAttr('{0}.liw'.format(i), 1)

    tjt.liw.set(0) #-- target joint
    pm.setAttr('{0}.liw'.format(njt), 0) #--org joint
    

    #-- set weight
    for k, v in wts.items():
        if '.' in k:
            vtx = '{0}.{1}'.format(obj.name(), k.split('.')[-1])
            pm.skinPercent(sc, vtx, tv=(njt, v*rate))








