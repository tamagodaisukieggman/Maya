# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import os
import sys
import shutil

import pymel.core as pm
import maya.cmds as mc


lUnit = ['mm', 'cm', 'm', 'km', 'in', 'ft', 'yd', 'mi']
aUnit = ['deg', 'rad']
tUnit = ['2fps', '3fps', '4fps', '5fps', '6fps', '8fps', '10fps', 
         '12fps', '15fps', '16fps', '20fps', '23.976fps', '24fps', 
         '25fps', '29.97fps', '29.97df', '30fps', '40fps', '47.952fps', 
         '48fps', '50fps', '59.94fps', '60fps', '75fps', '80fps', 
         '90fps', '100fps', '120fps', '125fps', '150fps', '59.94fps', 
         '200fps', '240fps', '250fps', '300fps', '375fps', '400fps', 
         '500fps', '600fps', '750fps', '1200fps', '1500fps', '2000fps', 
         '3000fps', '6000fps', '44100fps', '48000fps']


# -----------------------------------------------------------------------------
# plugin fuction
# -----------------------------------------------------------------------------
def checkLoadPlugin(plugin=''):
    if not pm.pluginInfo(plugin, l=True, q=True):
        pm.loadPlugin(plugin)
        print ('Plug-in, "{0}", was loaded successfully.'.format(plugin))
    else:
        print ('Plug-in, "{0}", is already loaded. <Skipped>'.format(plugin))


# ---- unload turtle plugin ---------------------------------------------------
def turtleKiller():
    if mc.pluginInfo('Turtle', loaded=True, q=True):
        mc.unloadPlugin('Turtle', f=True)
    for unk in mc.ls('Turtle*'):
        mc.lockNode(unk, l=False)
        mc.delete(unk)
    print ('unloaded turtle plugin and deleted related nodes successfully.')


# -----------------------------------------------------------------------------
# json functions
# -----------------------------------------------------------------------------
def exportJson(path=r'', dict={}):
    f = open(path, 'w')
    json.dump(dict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


def importJson(path=r''):
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp)
    f.close()
    return res


# -----------------------------------------------------------------------------
# directory Functions
# -----------------------------------------------------------------------------
def createDir(path=r''):
    res = pm.promptDialog(t='create template',
                          m='Enter Asset Name:',
                          b=['OK', 'Cancel'],
                         db='OK',
                         st='text',
                         cb='Cancel',
                         ds='Cancel')
    if res == 'OK':
        dirName = pm.promptDialog(tx=True, q=True)
        dPath   = '{0}/{1}'.format(path, dirName)
        os.makedirs(dPath)
        print ('create basebody directory: {0}'.format(dPath))


def dupliacteDir(path=r'', s=''):
    res = pm.promptDialog(t='duplicate template',
                          m='Enter Asset Name:',
                          b=['OK', 'Cancel'],
                         db='OK',
                         st='text',
                         cb='Cancel',
                         ds='Cancel')
    if res == 'OK':
        sPath   = '{0}/{1}'.format(path, s)
        dirName = pm.promptDialog(tx=True, q=True)
        tPath   = '{0}/{1}'.format(path, dirName)
        shutil.copytree(sPath, tPath)
        print ('duplicate directory: \n source: {0} \n target: {1}'.format(sPath, tPath))


# -----------------------------------------------------------------------------
# Common functions
# -----------------------------------------------------------------------------
# ---- current workspace
def getCurrentWorkspace():
    return pm.workspace(rd=True, q=True).replace(os.sep, '/')


# ---- add node
def addNode(t='transform', n='null'):
    log = ''
    if not pm.objExists(n):
        obj  = pm.createNode(t, n=n)
        log += 'create node: <type> {0}, <name> {1}'.format(t, n)
    else:
        obj  = pm.PyNode(n)
        t    = pm.nodeType(n)
        log += 'already exists: <type> {0}, <name> {1}'.format(t, n) 
    print (log)
    return obj


# ---- chain parent
def chainParent(nodes=[]):
    for i in range(0, len(nodes)-1):
        pm.select(d=True)
        pm.parent(nodes[i], nodes[i+1])


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


# ---- set edit 
def setEdit(typ=0, tgtSet=[]):
    '''
    maya object set edit
    Parameters:
    - int typ: type of set edit (0:add, 1:remove, 2:parent, 3:unparent, 4:attribute)
    Returns:
    - : 
    Error:
    - :
    '''
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

    elif typ == 4: # -- add attribute
        atList  = mc.channelBox('mainChannelBox', sma=True, q=True)
        objList = mc.ls(sl=True)
        if tgtSet:
            for tgt in tgtSet:
                if objList:
                    chList = ['{0}.{1}'.format(obj, at) for obj in objList for at in atList]
                    mc.sets(chList, add=tgt)
    mc.select(d=True)


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


def getCenterPostion(sel=[]):
    pm.select(sel, r=True)
    pm.mel.eval('MoveTool;')
    pos = pm.manipMoveContext('Move', p=True, q=True)
    pm.select(d=True)
    return pos


# ------------------------------------------------------------------------------
# Matrix functions
# ------------------------------------------------------------------------------
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
        print ('{0} does\'t have a connection to decomposeMatrix.'.format(src))


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


# ---- create world matrix group
def createWldGp(jtList=[], p='wld_GP'):
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


# -----------------------------------------------------------------------------
# Set Environment Functions
# -----------------------------------------------------------------------------
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


def arrangeJointDisplay(self):
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


def arangeJointAttribute(self):
    log = ''
    kList = ['v', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    for jt in pm.ls(typ='joint'):
        for at in pm.listAttr(jt, k=True, sn=True):
            if not at in kList:
                pm.setAttr('{0}.{1}'.format(jt.name(), at), k=False)
                log += '{0}.{1} : nonkeyable.\n'.format(jt.name(), at)
    print (log)


def arrageMeshDisplay(self):
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




