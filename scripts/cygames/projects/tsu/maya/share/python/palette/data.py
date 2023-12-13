# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc

import os
import subprocess
import datetime
import json

#-- ID -------------------------------------------------------------------------
def ishex(v):
    try:
        int(v, 16)
        return True
    except ValueError:
        return False


def getIDFromRoot():
    ID = ''
    for i in pm.ls(typ='transform'):
        if not i.getParent() and len(i.name()) == 6:
            if i[:2].isalpha() and ishex(i[-4:]):
                ID = i.name()
    if ID:
        return ID
    else:
        return None



#-- Create Directory -----------------------------------------------------------
#-- open directory
def openFolder(path):
    resPath, file = os.path.split(path)
    print("subprocess.call('explorer {0}')".format(resPath.replace('/', '\\')))
    subprocess.call('explorer {0}'.format(resPath.replace('/', '\\')))


def openDir(path):
    print("subprocess.call('explorer {0}')".format(path.replace('/', '\\')))
    subprocess.call('explorer {0}'.format(path.replace('/', '\\')))


def P4VDirectory():
    assetID = getIDFromRoot()
    if assetID:
        astType = assetID[:2]
        p4Path  = r'D:/cygames/tsubasa/work/chara/{0}/{1}'.format(astType, assetID)
    else:
        p4Path  = r'D:/cygames/tsubasa/work/chara'
    return p4Path


def LclDirectory():
    assetID = getIDFromRoot()
    if assetID:
        astType = assetID[:2]
        lcPath  = r'{0}scenes/{1}/{2}'.format(pm.workspace(q=True, rd=True), astType, assetID)
    else:
        lcPath  = r'{0}scenes'.format(pm.workspace(q=True, rd=True))
    return lcPath


def createDataDirectory(rootPath):
    log = ''
    _daPath  = r'{0}/_data'.format(rootPath)
    _dsPath  = r'{0}/scenes'.format(_daPath)
    _dmaPath = r'{0}/scenes/maya'.format(_daPath)
    _dmbPath = r'{0}/scenes/motionbuilder'.format(_daPath)
    _diPath  = r'{0}/sourceimages'.format(_daPath)
    _dnPath  = r'{0}/_assistdrive'.format(_daPath)
    _drPath  = r'{0}/_relation'.format(_daPath)

    #-- data directory
    for i in [_daPath, _dsPath, _dmaPath, _dmbPath, _diPath, _dnPath, _drPath]:
        if not os.path.exists(i):
            try:
                os.mkdir(i)
                log += 'create directory : {0}\n'.format(i)
            except:
                pass
        else:
            log += 'already exists.  : {0}\n'.format(i)
    return log


def createP4VDirectory():
    log = '------------------- Create P4V Directory -------------------------\n'
    p4vPath = P4VDirectory()
    rigPath = '{0}/rig'.format(p4vPath)
    maPath  = r'{0}/motionbuilder'.format(rigPath)
    mbPath  = r'{0}/maya'.format(rigPath)

    #-- Perforce directory
    for i in [p4vPath, rigPath, maPath, mbPath]:
        if not os.path.exists(i):
            try:
                os.mkdir(i)
                log += 'create directory : {0}\n'.format(i)
            except:
                pass
        else:
            log += 'already exists.  : {0}\n'.format(i)

    #-- data directory
    log += createDataDirectory(rigPath)
    print(log)
    return log


def createLclDirectory():
    log = '------------------- Create Local Directory -----------------------\n'
    lclPath = LclDirectory()
    maPath  = r'{0}/motionbuilder'.format(lclPath)
    mbPath  = r'{0}/maya'.format(lclPath)

    #-- Local directory
    for i in [lclPath, maPath, mbPath]:
        if not os.path.exists(i):
            os.mkdir(i)
            log += 'create directory : {0}\n'.format(i)
        else:
            log += 'already exists.  : {0}\n'.format(i)

    #-- data directory
    log += createDataDirectory(lclPath)
    print(log)
    return log


def getData():
    t = datetime.datetime.today()
    return '{0}{1}{2}'.format(t.year, t.month, t.day)



#-- Clean data -----------------------------------------------------------------
def turtleKiller():
    log = ''
    if mc.pluginInfo('Turtle.mll', loaded=True, q=True):
        mc.unloadPlugin('Turtle.mll', f=True)
    for unk in mc.ls('Turtle*'):
        mc.lockNode(unk, l=False)
        mc.delete(unk)
    log = 'unload plugin          : Turtle\n'
    print(log)
    return log


def deleteIGPUCS():
    log = ''
    for script in pm.ls(type="script"):
        if "IGPUCS" in script:
            log = 'delete script node     : (0))\n'.format(script)
            pm.delete(script)
    print(log)
    return log


def _get_script_node():
    log = ''
    f = lambda n: True if mc.getAttr("{}.st".format(n)) != 3 and mc.getAttr("{}.st".format(n)) != 6 else False
    script_nodes = [node for node in mc.ls(typ="script") if f(node)]
    if script_nodes:
        pm.select(script_nodes, r=True)
        pm.sets(n='script_nodes_set')
        log = 'check script node      : ' + ', '.join(script_nodes)
    else:
        log = 'check script node      : doesn\'t exists.\n'
    print(log)
    return log



def cleanupData(path):
    print(path)
    log = '------------------- Clean Data -----------------------------------\n'
    log += turtleKiller()
    log += deleteIGPUCS()
    log += _get_script_node()
    log += exportSelCleanup(path)
    print(log)
    return log



#-- Animation Key --------------------------------------------------------------
def deleteAnimKey():
    log = '------------------- Delete Animation Key -------------------------\n'
    animList = pm.ls(typ=[i for i in pm.listNodeTypes('animation') if 'animCurve' in i])
    pm.delete(animList)
    if animList:
        for i in animList:
            log += 'delete animation key : {0} \n'.format(i.name())
    else:
        log += 'delete animation key   : No Animation Key in the scene. \n'
    print(log)
    return log



#-- Clean Mesh -----------------------------------------------------------------
def cleanMesh(gp='LOD0'):
    objList = pm.select(gp, hi=True, r=True)
    
    for i in pm.ls(sl=True, typ='transform'):
        skinCls = pm.mel.eval('findRelatedSkinCluster {0};'.format(i.name()))
        if skinCls:
            pm.skinCluster(i, ub=True, e=True)
            pm.mel.eval('DeleteHistory;')
        pm.move(0,0,0, i.sp, i.rp, rpr=True)
        #pm.mel.eval('ResetDisplay;')
        i.useObjectColor.set(0)
        #-- unlock
        i.t.set(l=False)
        i.r.set(l=False)
        i.s.set(l=False)
        i.tx.set(l=False)
        i.ty.set(l=False)
        i.tz.set(l=False)
        i.rx.set(l=False)
        i.ry.set(l=False)
        i.rz.set(l=False)
        i.sx.set(l=False)
        i.sy.set(l=False)
        i.sz.set(l=False)



def cleanSkin():
    log = '------------------- Delete Skin Cluster --------------------------\n'
    skList = pm.ls(typ='skinCluster')
    for i in skList:
        i.envelope.set(0)

    if pm.objExists('LOD0'):
        cleanMesh(gp='LOD0')
        log += 'LOD0 | Unbind Mesh     : Done.\n'

    if pm.objExists('COL'):
        cleanMesh(gp='COL')
        log += 'COL | Unbind Mesh      : Done.\n'

    #-- delete bindpose
    mc.delete(mc.ls(typ='dagPose'))
    log += 'Delete Bind Pose       : Done.\n'
    #-- deselect
    pm.select(d=True)
    print(log)
    return log



def deleteSkeleton():
    log = '------------------- Delete Skaleton ------------------------------\n'
    if pm.objExists('null'):
        pm.delete('null')
    log += 'Reset Skeleton         : Done. \n'
    print(log)
    return log



def resetMeshDispaly(gp='LOD0'):
    log = '------------------- Reset Mesh Dispaly ---------------------------\n'
    if pm.objExists(gp):
        pm.select(gp, r=True)
        pm.mel.eval('ResetDisplay;')
    log += 'Reset Mesh Dispaly     : Done. \n'
    print(log)
    return log



#-- Freeze Object --------------------------------------------------------------
def freezeMesh():
    objList = mc.ls(sl=True)
    mc.makeIdentity(a=True, t=True, r=True, s=True, n=0, pn=True) 
    mc.lattice(dv=(2,2,2), oc=True, ldv=(2,2,2))
    mc.select(objList, r=True)
    pm.mel.eval('DeleteHistory;')



def freezeObj():
    log = '------------------- Freeze Mesh ----------------------------------\n'
    if pm.objExists('LOD0'):
        lMesh = list(set([i.getParent() for i in pm.ls('LOD0', dag=True, typ='mesh')]))
        pm.select(lMesh, r=True)
        freezeMesh()
        log += 'LOD0 | Freeze Mesh     : Done.\n'
    if pm.objExists('COL'):
        cMesh = list(set([i.getParent() for i in pm.ls('COL', dag=True, typ='mesh')]))
        pm.select(cMesh, r=True)
        freezeMesh()
        log += 'COL | Freeze Mesh      : Done.\n'
    print(log)
    return log



#-- check unnecessary shape ----------------------------------------------------
def checkUnnecessaryMesh():
    log = '------------------- Unnecessary Shape Check ----------------------\n'
    tgtMesh = []
    if pm.objExists('LOD0'):
        lMesh = list(set([i.getParent() for i in pm.ls('LOD0', dag=True, typ='mesh')]))
        if lMesh:
            tgtMesh = [i for i in lMesh if len(pm.listRelatives(i, c=True, typ='mesh')) > 1]

    if tgtMesh:
        if pm.objExists('LOD0_unnecessary_shape_set'):
            pm.delete('LOD0_unnecessary_shape_set')
        pm.select(tgtMesh, r=True)
        pm.sets(n='LOD0_unnecessary_shape_set')
        log += 'LOD0 | Shape Check     : LOD0_unnecessary_shape_set.\n'

    tgtMesh = []
    if pm.objExists('COL'):
        cMesh = list(set([i.getParent() for i in pm.ls('COL', dag=True, typ='mesh')]))
        if cMesh:
            tgtMesh = [i for i in cMesh if len(pm.listRelatives(i, c=True, typ='mesh')) > 1]

    if pm.objExists('COL_unnecessary_shape_set'):
        pm.delete('COL_unnecessary_shape_set')

    if tgtMesh:
        pm.select(tgtMesh, r=True)
        pm.sets(n='COL_unnecessary_shape_set')
        log += 'COL | Shape Check      : COL_unnecessary_shape_set.\n'
    else:
        log += 'Shape Check            : Done.\n'

    print(log)
    return log



#-- Chack Overlapping Node  ----------------------------------------------------
def checkSameNameNode():
    log = '------------------- Overlapping Name Check -----------------------\n'
    nodeList = []
    pathList = []
    
    # -- check scene
    for obj in mc.ls():
        if '|' in obj:
            nodeList.append(obj.split('|')[-1])
            pathList.append(obj)
    
    if mc.objExists('sameName_set'):
        mc.delete('sameName_set')
    
    if not len(nodeList) == 0:
        # -- print node names
        for i in range(len(nodeList)):
            log += '{0} : {1} \n'.format(nodeList[i], pathList[i])
        # -- create set
        mc.sets(pathList, n='sameName_set')
        
    else:
        log += 'Check node name        : doesn\'t exist in the scene.\n'

    print(log)
    return log



#-- Chack Texture  -------------------------------------------------------------
def checkTextureExist():
    log = '------------------- Texture Check --------------------------------\n'
    res = 0 
    fList = [i for i in pm.ls(typ='file')]
    eList = []
    for i in fList:
        tx     = i.fileTextureName.get()
        if not os.path.exists(tx):
            eList.append(i)
            pTx =  'Texture Error'
            log += '{0}: {1}\n'.format(pTx.ljust(20), i.name())

    if pm.objExists('error_texture_set'):
        pm.delete('error_texture_set')

    if eList:
        pm.select(eList, r=True)
        pm.sets(n='error_texture_set')
    else:
        log += 'Check Texture Path     : Done.\n'

    print(log)
    return log



#-- Export Selection -----------------------------------------------------------
def exportSelCleanup(d=r''):
    log = '------------------- Export Scene Cleanup -------------------------\n'
    #-- Get Target
    wTrs = [i for i in pm.ls(typ='transform') 
            if i.getParent() == None and not pm.nodeType(i.getShape()) == 'camera']

    #-- path
    f    = '{0}_cleanup.mb'.format(getIDFromRoot())
    path = r'{0}/{1}'.format(d, f).replace('\\', '/')

    #-- Export
    pm.select(wTrs, r=True)
    mc.file(path, es=True, f=True, op='v=0;', typ='mayaBinary', pr=True)

    #-- Open
    mc.file(path, f=True, op='v=0;', typ='mayaBinary', esn=False, iv=True, o=True)

    #-- Reorder
    for i in ['side', 'front', 'top', 'persp']:
        pm.reorder(i, f=True)

    #-- ;og
    log = 'Cleanup Data           : \'{0}\'\n'.format(pm.Env().sceneName())
    print(log)
    return log



#-------------------------------------------------------------------------------
#-- Export
#-------------------------------------------------------------------------------

#-- Create Bind Pose -----------------------------------------------------------
def createBindPose(gp=''):
    mc.dagPose(gp, s=True, bp=True, n='bindPose_{0}\n'.format(gp))
    return 'create bind pose       : bindPose_{0}\n'.format(gp)


def collectSingleBindPose():
    log = '------------------- Collect Single Bind Pose ---------------------\n'
    mc.delete(mc.ls(typ='dagPose'))
    # -- create bind pose
    ID = getIDFromRoot()
    if ID:
        log += createBindPose(ID)

    print(log)
    return log


#-- Chack Segment Scale --------------------------------------------------------
def checkSSC():
    log = '------------------- Check Segment Scale --------------------------\n'
    jtList = [i for i in pm.ls(typ='joint') if i.ssc.get()]

    for i in jtList:
        log += 'check segment scale    : {0}\n'.format(i.name())

    if pm.objExists('segmentScale_set'):
        pm.delete('segmentScale_set')

    if jtList:
        pm.select(jtList, r=True)
        pm.sets(n='segmentScale_set')

    pm.select(d=True)
    print(log)
    return log


#-- Chack Joint Orient ------------------------------------
def checkJO():
    log = '------------------- Check Joint Orient ---------------------------\n'
    jtList = [i for i in pm.ls('null', dag=True, typ='joint') if any(i.jo.get())]

    for i in jtList:
        log += 'check joint orient     : {0}\n'.format(i.name())

    if pm.objExists('jointOrient_set'):
        pm.delete('jointOrient_set')

    if jtList:
        pm.select(jtList, r=True)
        pm.sets(n='jointOrient_set')

    pm.select(d=True)
    print(log)
    return log



#-- dekete unused material -------------------------------------------
def deleteUnusedMaterial():
    log = '------------------- Delete Unused Material -----------------------\n'
    pm.mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    log += 'Delete Unused Nodes    : Done.\n'

    print(log)
    return log



def deleteDisplayLayer():
    log = '------------------- Delete Display Layer -------------------------\n'
    for i in pm.ls(typ='displayLayer'):
        if not i.name() == 'defaultLayer':
            pm.delete(i)
            log += 'delete display layer   : {0}\n'.format(i.name())

    print(log)
    return log


def deleteRigGroup():
    log = '------------------- Delete rig_GP --------------------------------\n'
    ID  = getIDFromRoot()
    if ID:
        if 'null' in pm.listRelatives(ID, c=True, typ='joint'):
            for i in [i for i in pm.ls('null', dag=True, typ='constraint')]:
                pm.delete(i)
                log += 'delete constraint      : {0}\n'.format(i.name())

        if 'rig_GP' in pm.listRelatives(ID, c=True, typ='transform'):
            pm.delete('rig_GP')
            log += 'delete Hierarchy       : {0}\n'.format('rig_GP')

    print(log)
    return log



def getFaceSetList():
    return [i for i in pm.ls(set=True) if i.name().lower().replace('_', '') == 'faceset']


def deleteFaceGroup():
    log = '------------------- Delete Face ----------------------------------\n'
    faceSetList = getFaceSetList()
    if faceSetList:
        for s in faceSetList:
            member = pm.sets(s, q=True)
            pm.sets(s, remove=member)
            pm.delete(member)
        log += 'delete Face_set       : Done.\n'

    lodList = [i for i in pm.ls('LOD0', dag=True, typ='transform') if i.name() == 'Face_LOD0']
    jtList  = [i for i in pm.ls('null', dag=True, typ='joint') if i.name() == '_005']
    if lodList:
        pm.delete(lodList)
        log += 'delete Face_LOD0       : Done.\n'
        if jtList:
            jaw = [i for i in jtList[0].getChildren() if i.name() =='_300']
            if jaw:
                pm.delete(jaw) 
                log += 'delete jaw joint       : Done.\n'

    print(log)
    return log


def getRigInformation(path):
    f = open(path, 'r')
    tmp = f.read()
    rig_info_dict = json.loads(tmp)
    f.close()

    rig_info_set = rig_info_dict['rig_info_set_name']
    fase_set = rig_info_dict['face_set_name']
    exp_pose_at = rig_info_dict['export_pose_frame_attr_name']

    return rig_info_set, fase_set, exp_pose_at


def deleteAnimAtExportFrame():
    log = '------------------- Delete Anim ----------------------------------\n'
    rig_info_dict = getRigInformation(
        '{0}/_json/_rig_info.json'.format(os.path.dirname(os.path.abspath(__file__)))
    )
    rig_info_set = rig_info_dict[0]
    if pm.objExists(rig_info_set):
        exp_pose_at = rig_info_dict[2]
        exp_frame = pm.getAttr(rig_info_set + '.' + exp_pose_at)
        if exp_frame != 0:
            pm.currentTime(exp_frame, e=True)
            pm.cutKey(pm.ls('null', dag=True, type='joint'))
            pm.currentTime(0, e=True)
            log += 'delete Anim       : Done.\n'
    else:
        log += 'not exists {}.\n'.format(rig_info_set)

    print(log)
    return log


#-- Material replace -------------------------------------------
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



def replaceLowMT(tgt=''):
    #-- create shader for MB
    sd = pm.shadingNode('lambert', asShader=True, n='{0}_lowMT'.format(tgt))
    se = pm.sets(nss=True, r=True, em=True)
    sd.outColor >> se.surfaceShader

    #-- get target
    pm.select(tgt, r=True)
    pm.hyperShade(objects='')
    pm.sets(se, fe=pm.ls(sl=True))

    #-- orverride
    atex = attributeExists(tgt, 'g_IsOverrideAlbedo')

    #-- get file color texture
    fList = []
    val   = False
    if not atex or not pm.getAttr('{0}.g_IsOverrideAlbedo'.format(tgt)):
        if not val:
            try:
                fList = pm.listConnections('{0}.g_AlbedoMap'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                val   = True
            except:
                pass
    
        if not val:
            try:
                fList = pm.listConnections('{0}.g_AlbedoMap0'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                val   = True
            except:
                pass
    
        if not val:
            try:
                fList = pm.listConnections('{0}.g_AlbedoMap1'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                val   = True
            except:
                pass
    
        if not val:
            try:
                fList = pm.listConnections('{0}.g_EyeIrisTexture'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                val   = True
            except:
                pass
       
        if not val:
            try:
                fList = pm.listConnections('{0}.g_AlbedoTex0'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                val   = True
            except:
                pass
    
        if not val:
            try:
                fList = pm.listConnections('{0}.g_AlbedoTex1'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                val   = True
            except:
                pass
    
        #-- connection
        if fList:
            for i in fList:
                path = i.fileTextureName.get()
                i.outColor >> sd.color

    #-- simple color
    elif atex and pm.getAttr('{0}.g_IsOverrideAlbedo'.format(tgt)):
        col = pm.getAttr('{0}.g_OverrideAlbedoColor'.format(tgt))
        pm.setAttr('{0}.color'.format(sd.name()), col, typ='double3')

    #-- deselect
    pm.select(cl=True)

    #-- return
    return sd.name()


def deleteVertexColor():
    log = '------------------- Delete Vertex Color --------------------------\n'
    for mesh in pm.ls(typ='mesh'):
        # ---- delete vertex color
        csList = pm.polyColorSet(mesh, acs=True, q=True)
        if csList:
            for cs in csList:
                pm.polyColorSet(mesh, cs=cs, d=True)
    print(log)
    return log


def normalUnlock():
    log = '------------------- Unlock Normal --------------------------------\n'
    meshList = list(set([i.getParent() for i in pm.ls('LOD0', dag=True, typ='mesh')]))
    log = ''
    for i in meshList:
        if any(pm.polyNormalPerVertex('{0}.vtx[*]'.format(i), fn=True, q=True)):
            log += 'unlock normal : {0}'.format(i.name())
            pm.polyNormalPerVertex(i, ufn=True)
    print(log)
    return log


def runReplaceLowMT():
    log = '------------------- Replace Materials ----------------------------\n'
    mtList = pm.ls(typ='dx11Shader')
    if mtList:
        for i in mtList:
            lMT = replaceLowMT(i.name())
            log += 'Replace Material : {0} -> {1}'.format(i, lMT)
    pm.mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    print(log)
    return log


def replaceResizedTxPath():
    log = ''
    assetID = getIDFromRoot()
    astType = assetID[:2]
    pfPath  = r'D:\cygames\tsubasa\work\chara\{0}\{1}\rig'.format(astType, assetID)
    maPath  = r'{0}\motionbuilder'.format(pfPath)
    mbPath  = r'{0}\maya'.format(pfPath)
    daPath  = r'{0}\_data'.format(pfPath)

    siPath  = r'{0}\sourceimages'.format(daPath).replace('\\', '/')
    fList   = [i for i in pm.ls(typ='file')]

    for i in fList:
        tx     = i.fileTextureName.get().split('/')[-1].replace('.tga', '.jpg')
        txPath = r'{0}/{1}'.format(siPath, tx)
        try:
            i.fileTextureName.set(txPath)
        except:
            pass
    pm.mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    print(log)
    return log

