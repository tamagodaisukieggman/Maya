# -*- coding: utf-8 -*-
from __future__ import absolute_import

# ----------------------------------
# Project : Common
# Name    : Maya Bootstrap Commands (mbc)
# Author  : ryo kanda
# Version : 0.0.1
# Updata  : 2022/09/18 19:14:41
# ----------------------------------

import json
import xml.etree.ElementTree as ET
import os
import sys
import shutil
import time
import datetime

import pymel.core as pm
import maya.cmds as mc

#from . import gui
#import importlib
#importlib.reload(gui)


linearUnit = ['mm', 'cm', 'm', 'km', 'in', 'ft', 'yd', 'mi']
angleUnit  = ['deg', 'rad']
timeUnit   = ['2fps', '3fps', '4fps', '5fps', '6fps', '8fps', '10fps', 
              '12fps', '15fps', '16fps', '20fps', '23.976fps', '24fps', 
              '25fps', '29.97fps', '29.97df', '30fps', '40fps', '47.952fps', 
              '48fps', '50fps', '59.94fps', '60fps', '75fps', '80fps', 
              '90fps', '100fps', '120fps', '125fps', '150fps', '59.94fps', 
              '200fps', '240fps', '250fps', '300fps', '375fps', '400fps', 
              '500fps', '600fps', '750fps', '1200fps', '1500fps', '2000fps', 
              '3000fps', '6000fps', '44100fps', '48000fps']

#-------------------------------------------------------------------------------
#-- Plugin Fuctions
#-------------------------------------------------------------------------------

#-- check plugin
def checkLoadPlugin(plugin=''):
    log = ''
    if not pm.pluginInfo(plugin, l=True, q=True):
        pm.loadPlugin(plugin)
        res = True
        log += 'Plug-in: \'{0}\' was loaded successfully.'.format(plugin)
    else:
        log += 'Plug-in: \'{0}\' is already loaded. <Skipped>'.format(plugin)
    print (log)


#-- unload turtle plugin 
def turtleKiller():
    log = ''
    #-- unload plugin 
    if pm.pluginInfo('Turtle', l=True, q=True):
        pm.unloadPlugin('Turtle', f=True)
        log += 'Unloaded turtle plugin successfully.\n'
    else:
        log += 'Turtle plugin is not loaded in the current scene.\n'

    #-- check turtle nodes.
    for unk in pm.ls('Turtle*'):
        pm.lockNode(unk, l=False)
        pm.delete(unk)
        log += 'Delete related nodes successfully.\n'
    print (log)


#-------------------------------------------------------------------------------
#-- Json Functions
#-------------------------------------------------------------------------------

#-- export json file
def exportJson(path=r'', dict={}):
    log = ''
    f = open(path, 'w')
    json.dump(dict, f, ensure_ascii=False, indent=4, 
              sort_keys=True, separators=(',', ': '))
    f.close()
    log += 'Export Json File: \'{0}\''.format(path)
    print (log)


#-- import json file
def importJson(path=r''):
    log = ''
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp)
    f.close()
    log += 'Import Json File: \'{0}\''.format(path)
    print (log)
    return res


#-- get skin information from json
def getSkinInfoFromJson(path=r''):
    info = importJson(path)
    jts = [i['source'] for i in info['deformerWeight']['weights']]
    inf = [i['deformer'] for i in info['deformerWeight']['weights']][0]
    geo = [i['shape'] for i in info['deformerWeight']['weights']][0]
    return [jts, inf, geo]


#-------------------------------------------------------------------------------
#-- Xml Functions
#-------------------------------------------------------------------------------

#-- get skin information from xml
def getSkinInfoFromXml(path=r''):
    tree = ET.parse(path)
    root = tree.getroot()
    #-- info
    #head = root[0].attrib
    #shape = root[1].attrib
    info = []
    #-- weight
    for child in root[2:]:
        info.append(child.attrib)
    jts = [i['source'] for i in info]
    inf = [i['deformer'] for i in info][0]
    geo = [i['shape'] for i in info][0]
    return [jts, inf, geo]


#-- get skin info
def getSkinInfo(path=r''):
    ext = os.path.splitext(path)[1]
    if ext == '.json':
        return getSkinInfoFromJson(path)
    elif ext == '.xml':
        return getSkinInfoFromXml(path)


#-------------------------------------------------------------------------------
#-- Directory Functions
#-------------------------------------------------------------------------------

#-- Create Directory
def createDir(path=r''):
    log = ''
    res = pm.promptDialog(t='Create Directory', m='Enter Directory Name:',
                          b=['Create', 'Cancel'], db='Create', st='text', 
                          cb='Cancel', ds='Cancel')
    if res == 'Create':
        dirName = pm.promptDialog(tx=True, q=True)
        dPath   = '{0}/{1}'.format(path, dirName).replace('\\', '/')
        #-- check directory
        if not os.path.exists(dPath):
            os.makedirs(dPath)
            log += 'Create Directory: {0}'.format(dPath)
            print (log)
        else:
            log += '\'{0}\' is already exists. <Skipped>'.format(dPath)
            pm.warning(log)
    return dPath


#-- Duplicate Directory
def dupliacteDir(path=r'', src=''):
    log = ''
    res = pm.promptDialog(t='Duplicate Director', m='Enter Directory Name:',
                          b=['Duplicate', 'Cancel'], db='OK', st='text',
                          cb='Cancel', ds='Cancel')
    if res == 'Duplicate':
        sPath   = '{0}/{1}'.format(path, src).replace('\\', '/')
        dirName = pm.promptDialog(tx=True, q=True)
        tPath   = '{0}/{1}'.format(path, dirName).replace('\\', '/')
        #-- check directory
        if not os.path.exists(tPath):
            shutil.copytree(sPath, tPath)
            log += 'Duplicate Directory: \n'
            log += 'Source Path: {0} \n'.format(sPath)
            log += 'Target Path: {0}'.format(tPath)
            print (log)
        else:
            log += '\'{0}\' is already exists. <Skipped>'.format(tPath)
            pm.warning(log)
    return tPath
    

#-- Current Workspace
def getCurrentWorkspace():
    return pm.workspace(rd=True, q=True).replace(os.sep, '/')


#-- Get Dialog
def getDialog(stPath=r''):
    fileFilter = 'Weight File Directory'
    if not stPath:
        stPath = mbc.getCurrentWorkspace()
    path = pm.fileDialog2(ff=fileFilter, ds=2, fm=3, spe=False, dir=stPath, 
                          cc='Cancel', okc='Accept', cap='Set Directory')
    if path: 
        path = path[0]
    return path


#-- import file
def openFile(path=r''):
    root, fileName = os.path.split(path)
    con = mc.confirmDialog(t='Confirm Open File', b=['Open','Cancel'], 
                           m='Do you open {0} File?'.format(fileName), 
                           db='Cancel', cb='Cancel', ds='Cancel')
    if con == 'Open' and '.mb' in fileName:
        mc.file(path, f=True, op='v=0;', iv=True, typ='mayaBinary', o=True)
    elif con == 'Open' and '.fbx' in fileName:
        mc.file(path, f=True, op='fbx', iv=True, typ='FBX', o=True)


def importFile(path=r'', ns=''):
    root, fileName = os.path.split(path)
    con = mc.confirmDialog(t='Confirm Import File', b=['Import','Cancel'], 
                           m='Do you import {0} File?'.format(fileName), 
                           db='Cancel', cb='Cancel', ds='Cancel')
    if ns:
        if con == 'Import' and '.mb' in fileName:
            mc.file(path, i=True, typ='mayaBinary', iv=True, ra=True,
                    mnc=False, ns=ns, op='v=0;', pr=True, ifr=False, itr='keep')
        elif con == 'Import' and '.fbx' in fileName:
            mc.file(path, i=True, typ='FBX', iv=True, ra=True, mnc=False,
                    ns=ns, op='fbx', pr=True, ifr=False, itr='keep') 
    else:
        if con == 'Import' and '.mb' in fileName:
            mc.file(path, i=True, typ='mayaBinary', iv=True, mnc=True,
                    rpr=ns, op='v=0;', pr=True, ifr=False, itr='keep')
        elif con == 'Import' and '.fbx' in fileName:
            mc.file(path, i=True, typ='FBX', iv=True, mnc=True, rpr=ns,
                    op='fbx', pr=True, ifr=False, itr='keep')


def referenceFile(path=r'', ns=''):
    root, fileName = os.path.split(path)
    con = mc.confirmDialog(t='Confirm Reference File', b=['Reference','Cancel'], 
                           m='Do you reference {0} File?'.format(fileName), 
                           db='Cancel', cb='Cancel', ds='Cancel')
    if con == 'Reference' and '.mb' in fileName:
        mc.file(path, r=True, typ='mayaBinary', iv=True, gl=True,
                mnc=False, ns=ns, op='v=0;')
    elif con == 'Reference' and '.fbx' in fileName:
        mc.file(path, r=True, typ='FBX', iv=True, gl=True,
                mnc=False, ns=ns, op='fbx')


#-------------------------------------------------------------------------------
#-- Time Fuctions
#-------------------------------------------------------------------------------

def getStartTime():
    return time.perf_counter()


def getExeTime(sTime=0.0):
    eTime = time.perf_counter()
    t = eTime - sTime
    print (t)
    return t


def backupFile(path=r''):
    dt_now = datetime.datetime.now()
    dt = dt_now.strftime('%Y%m%d_%H%M%S')
    p, f = os.path.splitext(path)
    bkPath = p + '_{0}{1}'.format(dt, f)
    try:
        os.rename(path, bkPath)
    except:
        os.remove(bkPath)
        os.rename(path, bkPath)
        print ('Delete old file which has been exists: {0}'.format(bkPath))
    return bkPath


#-- Common functions -----------------------------------------------------------
#-- Add Node
def addNode(t='transform', n='null'):
    log = ''
    if not pm.objExists(n):
        if not t == 'locator':
            obj = pm.createNode(t, n=n)
        else:
            obj = pm.spaceLocator(n=n)
        log += 'Create Node: <type> {0}, <name> {1}'.format(t, n)
    else:
        obj  = pm.PyNode(n)
        t    = pm.nodeType(n)
        log += 'Already Exists: <type> {0}, <name> {1}'.format(t, n) 
    print (log)
    return obj


#-- Duplicate Relace Name
def duplicateReplaceName(s='', r=''):
    selObj = pm.selected()
    if selObj:
        for i in selObj:
            orgList = pm.listRelatives(i, ad=True)
            orgList.reverse()
            orgList.insert(0, i)
            resList = [i.name() for i in orgList]
            #-- duplicate
            tgtList = mc.duplicate(i.name(), rc=True)
            for org, tgt in zip(orgList, tgtList):
                tgt = pm.PyNode(tgt)
                tgt.rename(org.name().replace(s, r))


#-- Switch Selection
def switchSelection(s='', r=''):
    selObj = pm.selected()
    res = []
    if selObj:
        for obj in selObj:
            if s in obj.name():
                res.append(obj.replace(s, r))
            elif r in obj.name():
                res.append(obj.replace(r, s))
    mc.select(res, r=True)


#-- Duplicate Parent Only
def duplicateParentOnly():
    selObj = pm.selected()
    if selObj:
        for i in selObj:
            pm.duplicate(i, po=True)


#-- Create Node Above
def createNodeAbove(node='', suf=''):
    nodeList = []
    for i in pm.selected():
        node = pm.createNode(node, n='{0}{1}'.format(i.name(), suf))
        pNode = pm.listRelatives(i, p=True)

        pm.parent(node, i)
        node.t.set(0,0,0)
        node.r.set(0,0,0)
        node.s.set(1,1,1)
        if pNode:
            pm.parent(node, pNode)
            pm.parent(i, node)
        else:
            pm.parent(node, w=True)
            pm.parent(i, node)
        nodeList.append(node)
    return nodeList


#-- Create Node Below
def createNodeBelow(node='', suf=''):
    nodeList = []
    for i in pm.selected():
        node = pm.createNode(node, n='{0}{1}'.format(i.name(), suf))
        pm.parent(node, i)
        node.t.set(0,0,0)
        node.r.set(0,0,0)
        node.s.set(1,1,1)
        nodeList.append(node)
    return nodeList


#-- Chain Parent  
def chainParent(rev=False):
    objs = pm.selected(typ='transform')
    pm.select(d=True)
    
    #-- list order
    if rev: 
        objs.reverse()
        #-- unparent
        for i in objs:
            try:
                pm.parent(i, w=True)
            except:
                pass
    
    for i in range(0, len(objs)-1):
        pm.parent(objs[i], objs[i+1])


#-- One by one Parent
def oneByOneParent():
    log = ''
    selObj = pm.selected(typ='transform')

    if len(selObj)%2 == 0:
        for i in range(0, len(selObj), 2):
            pm.parent(selObj[i], selObj[i+1])
            pm.select(d=True)
            log += 'Parent: {0} -> {1} \n'.format(selObj[i], selObj[i+1])
        print (log)
    else:
        log += 'Please select even number size.\n'
        log += 'selected size: {0} .'.format(len(selObj))
        pm.warning(log)


#-- Array Parent
def arrayParent():
    log = ''
    selObj = pm.selected(typ='transform')
    h = len(selObj)//2
    chList = selObj[:h]
    paList = selObj[h:]
    
    for i in range(len(chList)):
        pm.parent(chList[i], paList[i])
        log += 'Parent: {0} -> {1} \n'.format(selObj[i], selObj[i+1])
    print (log)


#-- Extract Hierarchy
def extractHierarchy(tgt=''):
    p = pm.listRelatives(tgt, p=True)
    c = pm.listRelatives(tgt, c=True)
    if p:
        for i in c:
            i.setParent(p[0])
    else:
        for i in c:
            i.setParent(w=True)
    pm.parent(tgt, w=True)
    pm.select(d=True)


#-- Get Center Position
def getCenterPostion(sel=[]):
    pm.select(sel, r=True)
    pm.mel.eval('MoveTool;')
    pos = pm.manipMoveContext('Move', p=True, q=True)
    pm.select(d=True)
    return pos


#-- Attribute Exists 
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


#-- Create null mesh
def createNullMesh():
    tr = pm.polyCube(n='_null_mesh', ch=False)[0]
    sp = tr.getShape()
    return [tr, sp] #-- return pynode objects


#-- Skin Functions -------------------------------------------------------------
#-- Get Skin Cluster Form Skin
def getSkinClusterFromSkin(skin=[]):
    scList = []
    if skin:
        for i in skin:
            sc = pm.mel.eval('findRelatedSkinCluster {0};'.format(i))
            if sc:
                scList.append(sc)
    return scList


#-- Select Skin Cluster Form Skin
def selectSkinClusterFormSkin():
    skin = mc.ls(sl=True)
    scList = getSkinClusterFromSkin(skin)
    mc.select(scList, r=True)
    return scList


#-- Get Joints From Skin Cluster
def getJointFromSkinCluster(sc=[]):
    jtList = []
    for i in sc:
        jts = mc.listConnections('{0}.matrix'.format(i), 
                                 s=1, d=0, t='joint', sh=1)
        if jts:
            for j in jts:
                if not j in jtList: #-- check redundant 
                    jtList.append(j)
    return jtList


#-- Select Joints From Skin Cluster
def selectJointsFromSkinCluster():
    sc = mc.ls(sl=True, typ='skinCluster')
    jtList = getJointFromSkinCluster(sc)
    mc.select(jtList, r=True)
    return jtList


#-- Select Mesh From Skin Cluster
def getMeshFromSkinCluster(sc=[]):
    mList = []
    for i in sc:
        mesh = mc.listConnections(i, c=False, d=True, 
                                  p=False, s=False, t='mesh')
        if mesh:
            for m in mesh:
                if not m in mList: #-- check redundant 
                    mList.append(m)
    return mList


#-- Select Mesh From Skin Cluster
def selectMeshFromSkinCluster():
    sc = mc.ls(sl=True, typ='skinCluster')
    mList = getMeshFromSkinCluster(sc)
    pm.select(mList, r=True)
    return mList


#-- Disconnect Joint Color
def disconnectJointColor():
    jts = mc.ls(typ='joint')
    for jo in jts:
        # -- disconnecting
        skinClsAttrList = mc.listConnections('%s.objectColorRGB'%jo, d=True, p=True, s=False, c=False)
        if not skinClsAttrList == None:
            for skinCls in skinClsAttrList:
                mc.disconnectAttr('%s.objectColorRGB'%jo, skinCls)


#-- Reset PreBindMatrix Skin
def resetPreBindMatrixSkin(tgt=''):
    tgt = pm.PyNode(tgt)
    sc = pm.mel.eval('findRelatedSkinCluster {0}'.format(tgt.name()))
    sc = pm.PyNode(sc)
    infList = pm.listConnections('{0}.matrix'.format(sc.name()))
    for i in infList:
        clList = pm.connectionInfo('{0}.worldMatrix[0]'.format(i.name()), dfs=1)
        for j, cl in enumerate(clList):
            if sc.name() in cl:
                num = pm.connectionInfo('{0}.worldMatrix[0]'.format(i.name()), dfs=1)[j].split('[')[1].split(']')[0]

        mtx = i.worldInverseMatrix.get()
        sc.bindPreMatrix[num].set(mtx)


#-- Reset PreBindMatrix Joint
def resetPreBindMatrixJoint(jt=''):
    jt = pm.PyNode(jt)
    scList = pm.listConnections('{0}.worldMatrix[0]'.format(jt.name()), t='skinCluster')
    for sc in scList:
        infList = pm.listConnections('{0}.matrix'.format(sc.name()))
        for i in infList:
            clList = pm.connectionInfo('{0}.worldMatrix[0]'.format(i.name()), dfs=1)
            for j, cl in enumerate(clList):
                if sc.name() in cl: 
                    num = pm.connectionInfo('{0}.worldMatrix[0]'.format(i.name()), dfs=1)[j].split('[')[1].split(']')[0]

            mtx = i.worldInverseMatrix.get()
            sc.bindPreMatrix[num].set(mtx)


#-- set edit 
def setEdit(typ=0, tgtSet=[]):
    #-- 0:add, 1:remove, 2:parent, 3:unparent, 4:add attribute to set
    if typ == 0: # -- add to target set
        if tgtSet:
            for tgt in tgtSet:
                mc.sets(mc.ls(sl=True), add=tgt)
        else:
            mc.warning('Please fill in new set name.')

    elif typ == 1: # -- remove from target set
        if tgtSet:
            for tgt in tgtSet:
                mc.sets(mc.ls(sl=True), rm=tgt)
        else:
            mc.warning('Please fill in new set name.')

    elif typ == 2: # -- simple parent set
        selectObj = mc.ls(sl=True)
        if mc.nodeType(selectObj[-1]) == 'objectSet':
            selectObj = mc.ls(sl=True)
            mc.sets(selectObj[:-1], add=selectObj[-1])
        else :
            mc.warning('Please select objectSet node at the end.')

    elif typ == 3: # -- simple unparent set
        selectObj = mc.ls(sl=True)
        if mc.nodeType(selectObj[-1]) == 'objectSet':
            mc.sets(selectObj[:-1], rm=selectObj[-1])
        else :
            mc.warning('Please select objectSet node at the end.')

    elif typ == 4: # -- add attribute to set
        atList  = mc.channelBox('mainChannelBox', sma=True, q=True)
        objList = mc.ls(sl=True)
        if tgtSet:
            for tgt in tgtSet:
                if objList:
                    chList = ['{0}.{1}'.format(obj, at) for obj in objList for at in atList]
                    mc.sets(chList, add=tgt)
    mc.select(d=True)


#-- Matrix functions -----------------------------------------------------------
#-- Create Decompose Matrix
def createDecomposeMatrix(src=''):
    srcN = pm.PyNode(src)
    dmat = '{0}_dmat'.format(src)
    if pm.objExists(dmat):
        dmat = pm.PyNode(dmat)
    else:
        dmat = pm.createNode('decomposeMatrix', n=dmat)
        srcN.worldMatrix >> dmat.inputMatrix
    return dmat


#-- get decompose matrix
def getDecomposeMatrix(src=''):
    dmat = pm.listConnections(src, 
                              s=False, c=False, d=True, p=False, 
                              t='decomposeMatrix')
    if dmat:
        return dmat[0]
    else:
        print ('{0} does\'t have a connection to decomposeMatrix.'.format(src))


#-- World Connection
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
def wldMatrix(tgt=[], suf='wld'):
    log = ''
    res = []
    if tgt:
        for i in tgt:
            src = pm.PyNode(i)
            wld = f'{src.name()}_{suf}'
            if not pm.objExists(wld):
                wld = pm.createNode('transform', n=f'{i}_{suf}')
                worldConnection(i, wld)
            else:
                log += f'world connection : {src.name()} already exists.\n'
                continue
            
            log += f'world connection : {src.name()} -> {wld.name()}\n'
        res.append(wld)
        print(log)

    else:
        log += 'Please select some transform nodes to create matrix connection.'
        print(log)
    return res


#-- World Disconnection
def worldDisconnect(tgt=''):
    tgtNode = pm.PyNode(tgt)
    cnList  = pm.listConnections(tgt, 
                                 s=True, c=True, p=True, d=False, 
                                 t='decomposeMatrix')
    for cn in cnList:
        cn[0].set(l=False)
        cn[1] // cn[0]
        tgtNode.useOutlinerColor.set(0)
        tgtNode.outlinerColor.set(0.0,0.0,0.0)


#-- create world matrix group
'''
def createWldrp(jtList=[], p='wld_GP'):
    log = ''
    for jt in jtList:
        if p == 'ch_wld_GP':
            wld = addNode('transform', 'ch{0}_wld'.format(jt))
            pos = addNode('transform', 'ch{0}_wld_pos'.format(jt))
        else:
            wld = addNode('transform', '{0}_wld'.format(jt))
            pos = addNode('transform', '{0}_wld_pos'.format(jt))
        pos.setParent(wld)
        wld.setParent(p)
        worldConnection(jt, wld)
        log += 'world matrix node : {0} parent to {1} \n'.format(wld.name(), p)
    print (log)
'''


def convertSelectionWldtoJoint():
    gpList = pm.selected(typ='transform')
    jtList = []
    for gp in gpList:
        dmat = list(set(pm.listConnections(gp, 
                                           s=True, 
                                           c=False, 
                                           p=False, 
                                           d=False, 
                                           t='decomposeMatrix')))
        if dmat:
            jt = pm.listConnections(dmat[0], 
                                    s=True, 
                                    c=False, 
                                    p=False, 
                                    d=False, 
                                    t='joint')
            if jt:
                jtList.append(jt[0])
    pm.select(jtList, r=True)


def convertSelectionJointToWld(ch=True):
    jtList = pm.selected(typ='joint')
    gpList = []
    for jt in jtList:
        dmat = pm.listConnections(jt, 
                                  s=False, 
                                  c=False, 
                                  p=False, 
                                  d=True, 
                                  t='decomposeMatrix')
        if dmat:
            gp = list(set(pm.listConnections(dmat[0], 
                                             s=False, 
                                             c=False, 
                                             p=False, 
                                             d=True, 
                                             t='transform')))
            if gp:
                if ch == True:
                    gp = [i for i in gp if 'ch' in i.name()]
                else:
                    gp = [i for i in gp if not 'ch' in i.name()]
                gpList.append(gp[0])
    pm.select(gpList, r=True)


#-- Set Environment Functions --------------------------------------------------
def setGrid(s=200, sp=50, d=5):
    pm.grid(s=s, sp=sp, d=d)
    print ('set grid: size={0}, spacin={1}, division={2}'.format(s, sp, d))


def setCam(fl=50):
    pm.setAttr('perspShape.focalLength', fl)
    print ('set camera: focalLength={0}'.format(fl))


def setJointSize(s=1.0):
    pm.jointDisplayScale(s)
    print ('set joint display size: {0}'.format(s))


def setSmoothWireframe(v=8):
    pm.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    pm.setAttr('hardwareRenderingGlobals.multiSampleCount', v)
    print ('smooth multi sample anti-aliasing: ON count={0}'.format(v))


def arrangeJointDisplay():
    uocLog = ''
    dlaLog = ''
    for jt in pm.ls(typ='joint'):
        uocVal = jt.uoc.get()
        if uocVal: 
            jt.uoc.set(0)
            uocLog += 'use object color off : {0} \n'.format(jt.name())
        
        dlaVal = jt.dla.get()
        if dlaVal:
            jt.dla.set(0)
            dlaLog += 'display local lotation axis off : {0} \n'.format(jt.name())
    
    # -- hide null 
    pm.setAttr('null.drawStyle', 2)
    
    # -- log
    print ('null drawStype : none')
    print (uocLog)
    print (dlaLog)


def arangeJointAttribute():
    log = ''
    kList = ['v', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    for jt in pm.ls(typ='joint'):
        for at in pm.listAttr(jt, k=True, sn=True):
            if not at in kList:
                pm.setAttr('{0}.{1}'.format(jt.name(), at), k=False)
                log += '{0}.{1} : nonkeyable.\n'.format(jt.name(), at)
    print (log)


def arrageMeshDisplay():
    csLog = ''
    deLog = ''
    for mesh in pm.ls(typ='mesh'):
        # ---- delete vertex color
        csList = pm.polyColorSet(mesh, acs=True, q=True)
        if csList:
            for cs in csList:
                pm.polyColorSet(mesh, cs=cs, d=True)
                csLog += 'delete color set : {0} \n'.format(cs)

        # ---- edge display standard
        deVal = mesh.displayEdges.get()
        if not deVal == 0:
            mesh.displayEdges.set(0)
            deLog += 'mesh display edge standard : {0} \n'.format(mesh.name())


def setTimeRange(s=0, e=10):
    pm.playbackOptions(min=s, max=e, ast=s, aet=e, e=True)
    pm.currentTime(s)
    log = 'set time range         : start={0}, end={1}\n'.format(s, e)
    return log


def setSceneUnit(l='cm', a='deg', t='60fps'):
    pm.currentUnit(l=l, a=a, t=t)
    log = 'set scene unit         : lniear={0}, angular={1}, time={2}\n'.format(l, a, t)
    return log


#-- GUI functions --------------------------------------------------------------
def optionMenuItems(item=[]):
    opm = []
    for i in item:
        opm.append(pm.menuItem(l=i))
    return opm


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# ---- set display layers
def setDisplayLayers():
    log = ''
    for i in pm.ls(typ='displayLayer'):
        if not i.name() == 'defaultLayer':
            pm.delete(i)
            log += 'delete display layer : {0} \n'.format(i.name())
    if pm.objExists('LOD0'):
        if not pm.objExists('geo'):
            pm.select('LOD0', r=True)
            pm.createDisplayLayer(n='geo', num=1, nr=True)
            log += 'create display layer : geo'
            pm.select(d=True)
    print (log)


# ---- create rig hierarchy
def createRigHierarchy():
    rigGP = addNode('transform', 'rig_GP')
    mtxGP = addNode('transform', 'matrix_GP')
    chwGP = addNode('transform', 'ch_wld_GP')
    wldGP = addNode('transform', 'wld_GP')
    lclGP = addNode('transform', 'lcl_GP')
    mtxGP.setParent(rigGP)
    chwGP.setParent(mtxGP)
    wldGP.setParent(mtxGP)
    lclGP.setParent(mtxGP)



# -----------------------------------------------------------------------------
# guide I/O
# -----------------------------------------------------------------------------
def importFile(d=r'', f='', ext='.mb'):
    path = '{0}/{1}{2}'.format(d, f, ext)
    ns   = ''
    mc.file(path,
            i = True, 
          typ = 'mayaBinary',
           iv = True,
          mnc = False,
          rpr = d,
           op = 'v=0;',
           pr = True,
          ifr = False,
          itr = 'keep') 


def importGuide(d=r'', f=''):
    path = '{0}/{1}'.format(d, f)
    ns   = ''
    v = pm.confirmDialog(t='import guide', 
                         m='import file: {0}'.format(path), 
                         b=['Yes','No'], 
                        db='No', 
                        cb='No', 
                        ds='No')
    if v == 'Yes':
        mc.file(path, i = True, 
                    typ = 'mayaBinary',
                     iv = True,
                    mnc = False,
                    rpr = d,
                     op = 'v=0;',
                     pr = True,
                    ifr = False,
                    itr = 'keep') 


def exportGuide(d=r'', f='', tgt=''):
    path = '{0}/{1}'.format(d, f)
    v = pm.confirmDialog(t='export guide', 
                         m='export file: {0}'.format(path), 
                         b=['Yes','No'], 
                        db='No', 
                        cb='No', 
                        ds='No')
    if v == 'Yes':
        if pm.objExists(tgt):
            pm.select(tgt, r=True)
            mc.file(path, 
                f=True, op='v=0;', typ='mayaBinary', pr=True, es=True)



# ------------------------------------------------------------------------------
# Setup Functions
# ------------------------------------------------------------------------------
def setPreserveChildren(val=True):
    mc.manipMoveContext('Move', pcp=val, e=True)


# ------------------------------------------------------------------------------
# character definition: 
# ------------------------------------------------------------------------------
def createCharacterDefinition(n=''):
    pm.mel.eval('hikCreateCharacter("{0}_character");'.format(n))
    pm.mel.eval('hikUpdateCharacterList();')
    pm.mel.eval('hikSelectDefinitionTab();')


def setCharacterDefinition(n='', info={}):
    # ---- set Definition : setCharacterObject("_000","Character1",1,0);
    chNode = pm.PyNode(n)
    if chNode.type() == 'HIKCharacterNode' and pm.objExists(n):
        for k, v in info.items():
            if pm.objExists(v[0]): 
                pm.mel.eval('setCharacterObject("{0}", "{1}", {2}, 0);'.format(v[0], chNode.name(), int(k)))
        pm.mel.eval('hikOnSwitchContextualTabs; hikUpdateContextualUI;')

    else:
        pm.warning('{0} is not HIKCharacter node or not exists in this scene.'.format(n))


# ------------------------------------------------------------------------------
# T-pose: 
# ------------------------------------------------------------------------------
def deleteAnimKey(self):
    log = ''
    animList = pm.ls(typ=['animCurveTA', 'animCurveTL', 'animCurveTU'])
    pm.delete(animList)
    for i in animList:
        log += 'delete animation key : {0} \n'.format(i.name())
    print (log)


def setTimeSlider(info={}):
    # -- set playback
    pm.playbackOptions(ast=0, aet=10, min=0, max=10, e=True)
    pm.currentTime(0)

    # -- set preffered angle
    pm.joint(info['001'][0], apa=True, ch=True, e=True)

    # -- set key
    for k, v in info.items():
        if v[0]:
            if pm.objExists(v[0]):
                pm.setKeyframe('{0}.rx'.format(v[0]))
                pm.setKeyframe('{0}.ry'.format(v[0]))
                pm.setKeyframe('{0}.rz'.format(v[0]))
    
    # -- set T-pose
    pm.currentTime(10)
    aList = setTPose(info)

    # -- set key
    for k, v in info.items():
        if v[0]:
            if pm.objExists(v[0]):
                pm.setKeyframe('{0}.rx'.format(v[0]))
                pm.setKeyframe('{0}.ry'.format(v[0]))
                pm.setKeyframe('{0}.rz'.format(v[0]))
    pm.delete(aList)


def setTPose(info={}):
    inJt   = ['146', '147', '148', '149', '150', '151', 
              '152', '153', '154', '155', '156', '157']
    thList = ['050', '051', '052', 
              '074', '075', '076']
    lfList = ['054', '058', '062', '066']
    rfList = ['078', '082', '086', '090']
    aList  = []
    for k, v in info.items():
        if v[0]:
            if not k in inJt: # -- not inhand
                if pm.objExists(v[0]):
                    pm.setAttr('{0}.rx'.format(v[0]), 0)
                    pm.setAttr('{0}.ry'.format(v[0]), 0)
                    pm.setAttr('{0}.rz'.format(v[0]), 0)
                else:
                    print ('pass ID:{0} set rotation.'.format(k))
    # ---- thumb
    for i in thList:
        jt = info[i][0]
        if pm.objExists(jt):
            pm.setAttr('{0}.rx'.format(jt), 0)
            pm.setAttr('{0}.ry'.format(jt), 0)
            pm.setAttr('{0}.rz'.format(jt), 0)
        else:
            print ('pass ID:{0} set rotation.'.format(i))

    # ---- T stance : fingers
    for i in lfList:
        jt  = info[i][0]
        aim = pm.createNode('transform', n='{0}_fingerAim'.format(jt))
        pos = pm.xform(jt, ws=True, t=True, q=True)
        pm.move(pos[0]*2, pos[1], pos[2], aim, a=True)
        pm.aimConstraint(aim, jt, o = (0,0,0),
                                  w = 1.0,
                                aim = (1,0,0),
                                  u = (0,1,0),
                                wut = 'vector', 
                                 wu = (0,1,0))
        aList.append(aim)
    
    for i in rfList:
        jt  = info[i][0]
        aim = pm.createNode('transform', n='{0}_fingerAim'.format(jt))
        pos = pm.xform(jt, ws=True, t=True, q=True)
        pm.move(pos[0]*2, pos[1], pos[2], aim, a=True)
        pm.aimConstraint(aim, jt, o = (0,0,0),
                                  w = 1.0,
                                aim = (-1,0,0),
                                  u = (0,1,0),
                                wut = 'vector', 
                                 wu = (0,1,0))
        aList.append(aim)
    return aList


# ------------------------------------------------------------------------------
# export definition json: 
# ------------------------------------------------------------------------------
def toggleMirrorComponent(typ='worldx'):
    c = pm.ls(sl=True, fl=True)
    pm.mel.eval('reflectionSetMode {0};'.format(typ))
    b = pm.ls(sl=True, fl=True)
    o = list(set(b) - set(c))
    pm.mel.eval('reflectionSetMode none;')
    pm.select(o, r=True)


# -----------------------------------------------------------------------------
# Browser: 
# -----------------------------------------------------------------------------
def toggleJointIcon(n=''):
    res = 0
    if pm.objExists(n):
        if n in mc.ls(sl=True):
            res = 2
        else:
            res = 1
    return res


# -----------------------------------------------------------------------------
# scriptJob: 
# -----------------------------------------------------------------------------
def killScriptJob(n=0):
    if pm.scriptJob(ex=n):
        pm.scriptJob(k=n)
        print ('Script job of number "{0}" was killed successfully.'.format(n))
    else:
        pm.warning('Script job of number "{0}" does\'t exist in the current maya environment.'.format(n))




