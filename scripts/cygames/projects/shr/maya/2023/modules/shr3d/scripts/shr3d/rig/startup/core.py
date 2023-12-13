# -*- coding: utf-8 -*-
from __future__ import absolute_import

import maya.cmds as mc
import pymel.core as pm
import maya.OpenMaya as om
import os
import glob
import re
import random
import datetime
import json
import socket

import QuadRemesher


#-------------------------------------------------------------------------------
#-- Json -----------------------------------------------------------------------
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


#-------------------------------------------------------------------------------
#-- init -----------------------------------------------------------------------
_dir = os.path.dirname(os.path.abspath(__file__))

#-- category
ctgPath = os.path.join(_dir, r'_data/_json/category.json').replace(os.sep, '/')
aCtg = importJson(ctgPath)

#-- asset path
astPath = os.path.join(_dir, r'_data/_json/assetPath.json').replace(os.sep, '/')
astP = importJson(astPath)

#-- user name
usrPath = os.path.join(_dir, r'_data/_json/user.json').replace(os.sep, '/')
user = importJson(usrPath)


#-- user -----------------------------------------------------------------------
def getUser():
    usr  = None
    host = socket.gethostname()
    if host in user.keys():
        usr = user[host]
    return usr


#-- Turtle ---------------------------------------------------------------------
def turtleKiller():
    #-- unload
    if mc.pluginInfo('Turtle', loaded=True, q=True):
        mc.unloadPlugin('Turtle', f=True)
    for unk in mc.ls('Turtle*'):
        mc.lockNode(unk, l=False)
        mc.delete(unk)
    #-- shelf
    tab = [i for i in pm.lsUI(cl=True) if 'TURTLE' in i]
    if tab:
        pm.deleteUI(tab)


#-------------------------------------------------------------------------------
#-- get ID ---------------------------------------------------------------------
def ishex(v):
    try:
        int(v, 16)
        return True
    except ValueError:
        return False


def getIDFromRoot():
    ID = ''
    for i in pm.ls(typ='transform'):
        if not i.getParent() and len(i.name()) == 7:
            if i[:3].isalpha() and ishex(i[-4:]):
                ID = i.name()
    if ID:
        return ID
    else:
        return None


def getCtg(typ=''):
    for k, v in aCtg.items():
        if typ in v:
            return k


def getAssetInfo(aID='ply0000'):
    path = os.path.join(astP['p4vCh'], '**/')
    cDir = [i.replace(os.sep, '/') for i in glob.glob(path, recursive=True)]

    if cDir:
        ast = [i for i in cDir if aID in i]
        if ast:
            aPath = sorted(ast)[0] #-- asset root path
            #-- get info
            aAll  = [i for i in aPath.split('/') if aID in i]
            aTyp  = aAll[0].split('_')[0][:3]
            aStr  = aAll[0].split('_')[1]
            aCtg  = getCtg(aTyp)
            return [aAll[0], aID, aTyp, aStr, aCtg]
        else:
            return [None, None, None, None, None]
    else:
        return [None, None, None, None, None]


#-------------------------------------------------------------------------------
#-- Work Space -----------------------------------------------------------------
def createDirectory(ctg='', aID='', aSt=''):
    message = ''

    #-- Path model
    mid = getMidPath(ctg, aID, aSt)

    #-- create rigs path
    p4v = astP['p4vRig']
    mtx = rf'{mid}/texture'
    mot = rf'{mid}/outsource'
    mma = rf'{mid}/work/maya'
    mmb = rf'{mid}/work/motionbuilder'
    ddv = rf'{mid}/_data/_drive'
    djs = rf'{mid}/_data/_json'
    dsc = rf'{mid}/_data/_script'
    dmt = rf'{mid}/_data/_material'

    message += f'P4V Rig Path :  {p4v}\n'
    for rp in [mtx, mot, mma, mmb, ddv, djs, dsc, dmt]:
        message += rp + '\n'

    #-- create local work path
    crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
    lma = rf'scenes/{mid}/work/maya'
    lmb = rf'scenes/{mid}/work/motionbuilder'

    message += f'\nLocal Rig Path :  {crp}\n'
    for rp in [lma, lmb]:
        message += rp + '\n'

    #-- create Workman path
    wmp = astP['workman']
    wtx = rf'{mid}/textures'
    wma = rf'{mid}/maya'
    wmb = rf'{mid}/motionbuilder'

    message += f'\nWorkman Path :  {wmp}\n'
    for rp in [wtx, wma, wmb]:
        message += rp + '\n'

    #-- create Data Check path
    dcp = astP['user']
    usr = getUser()
    uma = rf'{usr}/check/{ctg}/{aID}/maya'
    umb = rf'{usr}/check/{ctg}/{aID}/motionbuilder'

    message += f'\nData Check Path : {dcp}\n'
    for rp in [uma, umb]:
        message += rp + '\n'

    #-- Dialog
    v = pm.confirmDialog(t='Create Rig Path', m=message, ann='Check Rig Path',
        b=['OK', 'Cancel'], db='Cancel', cb='Cancel', ds='Cancel')

    #-- Create
    if v == 'OK':
        #-- P4V Main
        print (f'Create Path: P4V rigs path ----------------------------------')
        for rp in [mtx, mot, mma, mmb, ddv, djs, dsc, dmt]:
            p = os.path.join(p4v, rp).replace(os.sep, '/')
            if not os.path.isdir(p):
                os.makedirs(p)
                print (f'Create Directory.        : {p}')
            else:
                print (f'Already exists. [Skipped]: {p}')

        #-- Local
        print (f'Create Path: Local work path --------------------------------')
        for rp in [lma, lmb]:
            p = os.path.join(crp, rp).replace(os.sep, '/')
            if not os.path.isdir(p):
                os.makedirs(p)
                print (f'Create Directory.        : {p}')
            else:
                print (f'Already exists. [Skipped]: {p}')

        #-- Workman
        print (f'Create Path: Workman path -----------------------------------')
        for rp in [wtx, wma, wmb]:
            p = os.path.join(wmp, rp).replace(os.sep, '/')
            if not os.path.isdir(p):
                os.makedirs(p)
                print (f'Create Directory.        : {p}')
            else:
                print (f'Already exists. [Skipped]: {p}')

        #-- Check Data
        print (f'Create Path: Check Data path --------------------------------')
        for rp in [uma, umb]:
            p = os.path.join(dcp, rp).replace(os.sep, '/')
            if not os.path.isdir(p):
                os.makedirs(p)
                print (f'Create Directory.        : {p}')
            else:
                print (f'Already exists. [Skipped]: {p}')


def getMidPath(ctg='', aID='', aSt=''):
    num = aID[4:]      
    typ = aID[0:3]
    mid = os.path.join(ctg, typ, f'{aID}_{aSt}').replace(os.sep, '/')
    return mid


def midPathExists(ctg='', aID='', aSt=''):
    crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
    mid = getMidPath(ctg, aID, aSt)
    lsc = rf'scenes/{mid}/work/maya'
    lma = rf'{crp}/{lsc}'
    if not os.path.isdir(lma):
        return [False, lsc]
    else:
        return [True, lsc]  


def getWorkPath(ctg='', aID='', aSt=''):
    mid = midPathExists(ctg, aID, aSt)
    res = r''
    if mid[0]:
        crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
        res = os.path.join(crp, mid[1]).replace(os.sep, '/')
    return res


def getFileList(path=r'', typ=0, aID=''):
    #-- typ=0: all
    #-- typ=1: asset ID sort
    files = []
    if os.path.isdir(path):
        files = [i for i in os.listdir(path) if os.path.splitext(i)[1] == '.mb']
    if typ == 1:
        files = [i for i in files if aID in i]
    return files


#-- Local Path -----------------------------------------------------------------
def openFile(path=r''):
    if os.path.exists(path):
        v = pm.confirmDialog(t='Open File', m=path, ann='Check File Path',
            b=['Open', 'Cancel'], db='Cancel', cb='Cancel', ds='Cancel')

        if v == 'Open':
            if os.path.exists(path):
                try:
                    mc.file(path, o=True)
                except:
                    fPath   = mc.file(q=True, sn=True)
                    
                    if fPath:
                        message = f'Save changes to: {fPath}'
                    else:
                        message = f'Save changes to untitled scene?'
                    scv = pm.confirmDialog(t='Save Changes', m=message, 
                          b=['Save', 'Don\'t Save', 'Cancel'], 
                          db='Cancel', cb='Cancel', ds='Cancel')

                    if scv == 'Don\'t Save':
                        mc.file(path, o=True, f=True)
                    elif scv == 'Save':
                        pm.mel.eval('SaveScene;')
                        mc.file(path, o=True, f=True)

    else:
        pm.warning(f'File doesn\'t exist.: {path}' )


def saveFile(path=r''):
    v = pm.confirmDialog(t='Save File', m=path, ann='Check File Path',
        b=['Save', 'Cancel'], db='Cancel', cb='Cancel', ds='Cancel')

    if v == 'Save':
        mc.file(rn=path)
        mc.file(s=True, typ='mayaBinary', f=True)


def updateFileName(name='', v=1):
    #-- enm2000_v061_20230106.mb
    fName, ext = os.path.splitext(name)
    nameParts  = fName.split('_')
    resName    = ''

    aID, ver, dat, inf = ['', '', '', '']
    if len(nameParts) == 4:
        aID, ver, dat, inf = fName.split('_')
        newVer  = 'v{0:03d}'.format(int(ver[1:]) + v)
        newName = '_'.join([aID, newVer, dat, inf])
        resName = f'{newName}{ext}'

    elif len(nameParts) == 3:
        aID, ver, dat, = fName.split('_')
        newVer = 'v{0:03d}'.format(int(ver[1:]) + v)
        newName = '_'.join([aID, newVer, dat]) 
        resName = f'{newName}{ext}'

    return resName


def updateDate(name=''):
    #-- enm2000_v061_20230106.mb
    fName, ext = os.path.splitext(name)
    nameParts  = fName.split('_')
    resName    = ''
    d_today    = str(datetime.date.today()).replace('-', '')

    aID, ver, dat, inf = ['', '', '', '']
    if len(nameParts) == 4:
        aID, ver, dat, inf = nameParts.split('_')
        newName = '_'.join([aID, ver, d_today, inf])
        resName = f'{newName}{ext}'

    elif len(nameParts) == 3:
        aID, ver, dat, = fName.split('_')
        newName = '_'.join([aID, ver, d_today]) 
        resName = f'{newName}{ext}'

    return resName


def getVersion(name=''):
    ver = 0
    parts = len(name.split('_'))
    if parts == 3 or parts == 4:
        vPart = name.split('_')[1]
        ver   = int(re.sub(r'\D', '', vPart))
    return ver


def checkVer(path='', aID='', fileName=''):
    res = 2 #-- default value
    if os.path.isdir(path):

        aFiles = [i for i in os.listdir(path) if aID in i]
        aVers  = [getVersion(i) for i in aFiles]

        crtVer = getVersion(fileName)
        maxVer = max(aVers)

        if crtVer == maxVer:   #-- v020 == v020 -- same ver
            res = 0
        elif crtVer > maxVer:  #-- v021 > v020 -- new ver
            res = 1
        elif crtVer < maxVer:  #-- v019 < v020 -- error
            res = -1
    return res


#-------------------------------------------------------------------------------
#-- P4V Path -------------------------------------------------------------------
def midP4VPathExists(prj='', ctg='', aID='', aSt=''):
    #-- enemy/enm/enm2000_firedragon/work/maya
    mid = getMidPath(ctg, aID, aSt)
    lsc = rf'{mid}/work/maya'
    lma = rf'{prj}/{lsc}'
    if not os.path.isdir(lma):
        return [False, lsc]
    else:
        return [True, lsc]  


def getP4VPath(prj='', ctg='', aID='', aSt=''):
    mid = midP4VPathExists(prj, ctg, aID, aSt)
    res = r''
    if mid[0]:
        crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
        res = os.path.join(crp, mid[1]).replace(os.sep, '/')
    return res


def getP4VFileList(path=r'', typ=0, aID=''): #-------------------------------------------------------------------------------
    #-- typ=0: all
    #-- typ=1: asset ID sort
    files = []
    if os.path.isdir(path):
        files = [i for i in os.listdir(path) if os.path.splitext(i)[1] == '.mb']
    if typ == 1:
        files = [i for i in files if aID in i]
    return files


#-- Workman Path ---------------------------------------------------------------
def midWorkmanPathExists(prj='', ctg='', aID='', aSt=''):
    #-- enemy/enm/enm2000_firedragon/maya
    mid = getMidPath(ctg, aID, aSt)
    lsc = rf'{mid}/maya'
    lma = rf'{prj}/{lsc}'
    if not os.path.isdir(lma):
        return [False, lsc]
    else:
        return [True, lsc]  


def getWorkmanPath(prj='', ctg='', aID='', aSt=''):
    mid = midWorkmanPathExists(prj, ctg, aID, aSt)
    res = r''
    if mid[0]:
        crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
        res = os.path.join(crp, mid[1]).replace(os.sep, '/')
    return res



#-- Data Check Path ------------------------------------------------------------
def midDataCheckPathExists(prj='', ctg='', aID='', usr=''):
    #-- check/enemy/enm2000
    prj = r'\\cydrive01\104_projects\149_shenron\30_design\20_rig\00_user'
    mid = rf'{ctg}/{aID}'
    lsc = rf'check/{mid}/maya'
    lma = rf'{prj}/{usr}/{lsc}'
    if not os.path.isdir(lma):
        return [False, lsc]
    else:
        return [True, lsc]  


def getDataCheckPath(prj='', ctg='', aID='', aSt=''):
    mid = midDataCheckPathExists(prj, ctg, aID, aSt)
    res = r''
    if mid[0]:
        crp = pm.workspace(rd=True, q=True).replace(os.sep, '/')
        res = os.path.join(crp, mid[1]).replace(os.sep, '/')
    return res


#-- Convert Texture ------------------------------------------------------------
def checkTextureDir(path=r''):
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        print ('texture path for rigs is already exists.')


#-- repalce to preview material ------------------------------------------------
def replaceToPreviewMaterial(tgt=''):
    #-- tgt is material name (string)
    #-- create low material
    sd = pm.shadingNode('lambert', asShader=True, n='{0}_lowMT'.format(tgt))
    se = pm.sets(nss=True, r=True, em=True)
    sd.outColor >> se.surfaceShader

    #-- get target
    pm.select(tgt, r=True)
    pm.hyperShade(o='')
    pm.sets(se, fe=pm.ls(sl=True))

    #-- get file color texture
    fList = pm.listConnections('{0}.color'.format(tgt), s=True, c=False, 
                               p=False, d=False, t='file')
    
    #-- connection
    if fList:
        for i in fList:
            path = i.fileTextureName.get()
            i.outColor >> sd.color

    #-- deselect
    pm.select(cl=True)


def selectAllMesh():
    #-- select target mesh
    pm.select(pm.listRelatives('mesh', ad=True, typ='mesh'), r=True)
    pm.mel.eval('PickWalkUp')


def assignLowMaterial():
    selectAllMesh()
    #-- replace to preview material
    for obj in pm.selected():
        shp = obj.getShape()
        seList = pm.listConnections(shp, s=False, c=False, p=False, d=True, 
                                    t='shadingEngine')
        for i in seList:
            mtList = pm.listConnections(i.surfaceShader, s=True, c=False, 
                                        p=False, d=False)
            for j in mtList:
                if not '_lowMT' in j.name():
                    print (j.name())
                    replaceToPreviewMaterial(j.name()) 

    #-- delete unused nodes
    pm.mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')


#-- convert file texture -------------------------------------------------------
def convertLowTexture(rPath=r''):
    fList = pm.ls(typ='file')
    w = 256
    h = 256
    img = om.MImage()
    eList = []

    for i in fList:
        fPath = i.fileTextureName.get()
        if os.path.isfile(fPath):
            #-- file permission
            fName = os.path.basename(fPath)
            f = os.path.join(rPath, fName).replace(os.sep, '/')
            if not os.access(f, os.W_OK):
                try:
                    os.chmod(f, stat.S_IWRITE)
                    print('Read only -> writable: {0}'.format(f))
                except:
                    pass
            #-- resize
            img.readFromFile(fPath)
            img.resize(w, h, True)
            img.writeToFile(f, 'tga')
        else:
            eList.append(i.name())

    if eList:
        for i in eList:
            print('file node: {0} is couldn\'t convert.'.format(i.name()))

    #-- replace file path
    for i in fList:
        fPath = i.fileTextureName.get()
        if os.path.isfile(fPath):
            fName = os.path.basename(fPath)
            f = os.path.join(rPath, fName).replace(os.sep, '/')
            #-- replace file path
            i.fileTextureName.set(f)


#-- Create Material Data -------------------------------------------------------
def createLowMTPlanes():
    #-- create plane
    p   = pm.polyPlane(w=1, h=1, sx=1, sy=1, ax=(0,1,0), cuv=2, ch=0, 
                       n='_lowMT_plane')[0]
    psp = p.getShape()
    res = []
    #-- mesh group
    if pm.objExists('_mtMesh_grp'):
        pm.delete('_mtMesh_grp')
        
    grp  = pm.createNode('transform', n='_mtMesh_grp')
    res.append(grp) #-- append group
    msh  = pm.PyNode('mesh')
    lods = pm.listRelatives(msh, c=True)
    
    for i in lods: #-- lod0, lod1, lod2...
        oName = i.name()
        mtGrp = pm.duplicate(i)[0]
        mtGrp.rename(f'{oName}_mt')
        trans = pm.listRelatives(mtGrp, typ='transform', ad=True)
        meshs = pm.listRelatives(mtGrp, typ='mesh', ad=True)
        renamed = [i.rename(f'{i.name()}_mt') for i in trans]
        res.append(mtGrp) #-- append sub group
        mtGrp.setParent(grp)
        for msp in meshs:
            print(msp.name())
            psp.outMesh >> msp.inMesh

    pm.refresh()
    pm.delete(p)

    return res


def setDefaultMaterial():
    v = pm.confirmDialog(t='Set Default Material.', 
        m='Assign lambert1 to all meshes and delete all materials except for _mtMesh_grp', 
        b=['OK', 'Cancel'], db='Cancel', cb='Cancel', ds='Cancel')
    if v == 'OK':
        tops = [i for i in pm.ls(typ='transform') if not i.getParent()]
        tgts = [i for i in tops if not i.name() == '_mtMesh_grp']
        mehs = ()
        for i in tgts:
            mehs = mehs + tuple(pm.listRelatives(i, typ='mesh', ad=True))
        #-- assign lambert1
        pm.sets('initialShadingGroup', fe=mehs)
        pm.mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')


def setMaterialFromData(tgt):
    tgt = pm.PyNode(tgt)
    org = pm.PyNode(f'{tgt}_mt')
    tgtsp = tgt.getShape()
    orgsp = org.getShape()
    
    seList = pm.listConnections(orgsp, s=False, c=False, p=False, d=True, 
                                t='shadingEngine')
    pm.sets(seList[0], fe=tgtsp)
    print(f'Assign Material: {seList[0]} -> {tgtsp}')
    

def assignMaterialFromData():
    res = []
    for i in pm.listRelatives('mesh', ad=True, typ='mesh'):
        res.append(i.getParent())

    res = list(set(res))
    for i in res:
        setMaterialFromData(i)
 

#-- random assgin materials ----------------------------------------------------
def randAssignMT():
    selectObj = mc.ls(sl=True)
    for geo in selectObj :
        mt = mc.shadingNode('lambert', n='randAssignMT#', asShader=True)
        x = random.uniform(0, 1.5)
        y = random.uniform(0, 1.5)
        z = random.uniform(0, 1.5)
        mc.setAttr((mt + '.color'), x, y, z, type='double3')
        mc.select(geo, r=True)
        mc.hyperShade(assign=mt)



#-- Hierarchy ------------------------------------------------------------------
def addNode(typ='', name=''):  
    if not pm.objExists(name):
        res = pm.createNode(typ, n=name)
        print(f'Create Node: type:{typ}, name:{name}')
    else:
        res = None
        print(f'Already Exists: type:{typ}, name:{name}')
    return res


def createBaseHierarchy():
    #-- main
    rig = addNode('transform', 'rig_grp')
    mtx = addNode('transform', 'matrix_grp')
    drv = addNode('transform', 'drvMatrix_grp')
    #-- workbench
    wkb = addNode('transform', 'workbench')
    cag = addNode('transform', 'cage_grp')
    #--parent
    if rig and mtx:
        mtx.setParent(rig)
    if rig and drv:
        drv.setParent(rig)
    if wkb and cag:
        cag.setParent(wkb)


#-- Delete ---------------------------------------------------------------------
def deleteAnimKey():
    log = ''
    animList = pm.ls(typ=['animCurveTA', 'animCurveTL', 'animCurveTU'])
    pm.delete(animList)
    for i in animList:
        log += 'delete animation key : {0} \n'.format(i.name())
    print (log)


#-- Quad Remesher --------------------------------------------------------------
def launchQR():
    qr = QuadRemesher.QuadRemesher()







