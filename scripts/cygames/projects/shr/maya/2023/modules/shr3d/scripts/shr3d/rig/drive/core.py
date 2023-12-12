# -*- coding: utf-8 -*-
from __future__ import absolute_import

#----- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import os
import json

from math import degrees
from maya.api.OpenMaya import MFnTransform, MGlobal, MTransformationMatrix


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


#-- Copy Rotate
def createCopyRotate(src, part='', ro=0, suf='roll'):
    src = pm.PyNode(src)

    #-- locator
    rot = pm.spaceLocator(n=f'{part}_{suf}')
    pm.delete(pm.parentConstraint(src, rot, w=1, mo=False))
   
    #-- constraint
    rot.rotateOrder.set(ro)
    pm.orientConstraint(src, rot, w=1, mo=False)

    #-- Connect Attributes
    connectSelfRotate(rot)

    #-- log
    print(f'Create Drive Type: Copy Rotate: {src.name()} -> {rot.name()}')


#-- Bend Roll
def createBendRoll(src, aim, part='', ax=0, up=0, suf=['bend', 'upv', 'roll']):
    src  = pm.PyNode(src)
    aim  = pm.PyNode(aim)

    #-- locator
    bend = pm.spaceLocator(n=f'{part}_{suf[0]}')
    pm.delete(pm.parentConstraint(src, bend, w=1, mo=False))
    
    upvN = pm.spaceLocator(n=f'{part}_{suf[1]}')
    pm.delete(pm.parentConstraint(src, upvN, w=1, mo=False))
    
    roll = pm.spaceLocator(n=f'{part}_{suf[2]}')
    pm.delete(pm.parentConstraint(src, roll, w=1, mo=False))
    
    #-- parent
    roll.setParent(bend)

    #-- constraint
    aimL = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]
    av   = aimL[ax]
    upv  = aimL[up]
    pm.aimConstraint(aim, bend, w=1, o=(0,0,0), aim=av, wu=upv, u=upv,
                     wut='objectrotation', wuo=upvN)
    pm.orientConstraint(src, roll, w=1, mo=False)

    #-- Connect Attributes
    connectSelfRotate(bend)
    connectSelfRotate(roll)
    connectBendAngle(src, upvN, bend, roll, axis='X')

    #-- log
    print(f'Create Drive Type: Bend Roll: {src.name()} -> {roll.name()}')


#-- Yaw pitch roll
def createYawPitchRoll(src, part='', ro=0, suf=['yaw', 'pitch', 'roll']):
    x  = [(0,0), (1,1), (1,1)]
    y  = [(1,1), (0,0), (1,1)]
    z  = [(1,1), (1,1), (0,0)]
    ov = [(y,z,x), (z,x,y), (x,y,z), (z,y,x), (x,z,y), (y,x,z)]

    src  = pm.PyNode(src)
    
    #-- locator
    yaw   = pm.spaceLocator(n=f'{part}_{suf[0]}') #-- default:Y
    pm.delete(pm.parentConstraint(src, yaw, w=1, mo=False))
    
    pitch = pm.spaceLocator(n=f'{part}_{suf[1]}') #-- default:Z
    pm.delete(pm.parentConstraint(src, pitch, w=1, mo=False))
    
    roll  = pm.spaceLocator(n=f'{part}_{suf[2]}') #-- default:X
    pm.delete(pm.parentConstraint(src, roll, w=1, mo=False))

    #-- parent
    pitch.setParent(yaw)
    roll.setParent(pitch)    

    #-- limit
    pm.transformLimits(yaw,   rx=(0,0),  ry=(0,0),  rz=(0,0), 
        erx=ov[ro][0][0], ery=ov[ro][0][1], erz=ov[ro][0][2]) #-- Y
    pm.transformLimits(pitch, rx=(0,0),  ry=(0,0),  rz=(0,0), 
        erx=ov[ro][1][0], ery=ov[ro][1][1], erz=ov[ro][1][2]) #-- Z
    pm.transformLimits(roll,  rx=(0,0),  ry=(0,0),  rz=(0,0), 
        erx=ov[ro][2][0], ery=ov[ro][2][1], erz=ov[ro][2][2]) #-- X

    #-- constraint
    pm.orientConstraint(src, yaw, w=1, mo=False)
    pm.orientConstraint(src, pitch, w=1, mo=False)
    pm.orientConstraint(src, roll, w=1, mo=False)
    connectYawPitchRoll(yaw, pitch, roll)

    #-- log
    print(f'Create Drive Type: Yaw Pitch Roll: {src.name()} -> {roll.name()}')


#-- Connect Rotate -> float rot attributes
def connectSelfRotate(tgt):
    tgt = pm.PyNode(tgt)
    
    pm.addAttr(tgt, ln='rot', at='double3')
    pm.addAttr(tgt, ln='rotX', at='double', p='rot', dv=0) 
    pm.addAttr(tgt, ln='rotY', at='double', p='rot', dv=0) 
    pm.addAttr(tgt, ln='rotZ', at='double', p='rot', dv=0)   
    pm.setAttr(f'{tgt.name()}.rot', 0,0,0, typ='double3')
    pm.setAttr(f'{tgt.name()}.rot', k=True, e=True)
    pm.setAttr(f'{tgt.name()}.rotX', k=True, e=True)
    pm.setAttr(f'{tgt.name()}.rotY', k=True, e=True)
    pm.setAttr(f'{tgt.name()}.rotZ', k=True, e=True)
        
    tgt.r >> tgt.rot


#-- Connect Bend Angle
def connectBendAngle(tgt, upv, bend, roll, axis='X'):
    tgt  = pm.PyNode(tgt)
    bend = pm.PyNode(bend) 
    upv  = pm.PyNode(upv)
    roll = pm.PyNode(roll)
    
    cpmUpv = pm.createNode('composeMatrix', n=f'{tgt.name()}Upv_cpm')
    cpmBnd = pm.createNode('composeMatrix', n=f'{tgt.name()}Bend_cpm')
    mtm    = pm.createNode('multMatrix', n=f'{tgt.name()}_mtm') 
    dcm    = pm.createNode('decomposeMatrix', n=f'{tgt.name()}_dcm')
    agb    = pm.createNode('angleBetween', n=f'{tgt.name()}_agb')
    
    #-- driver -> composeMatrix
    upv.rotate  >> cpmUpv.inputRotate
    bend.rotate >> cpmBnd.inputRotate
    
    if axis == 'X': cpmUpv.inputTranslateX.set(1)
    if axis == 'Y': cpmUpv.inputTranslateY.set(1)
    if axis == 'Z': cpmUpv.inputTranslateZ.set(1)
      
    #-- composeMatrix -> multMatrix
    cpmUpv.outputMatrix >> mtm.matrixIn[0]
    cpmBnd.outputMatrix >> mtm.matrixIn[1]
    
    #-- multMatrix -> decomposeMatrix
    mtm.matrixSum >> dcm.inputMatrix

    #-- decomposeMatrix -> angleBetween
    dcm.outputTranslate >> agb.vector1
    dcm.outputTranslate // agb.vector1
    dcm.outputTranslate >> agb.vector2
    
    #-- angleBetween -> roll
    if not attributeExists(roll.name(), 'angle'):
        pm.addAttr(roll, ln='angle', at='double', dv=0) 
        pm.setAttr(f'{roll.name()}.angle', k=True, e=True)
    agb.angle >> roll.angle
    

#-- Connect Yaw Pitch Roll
def connectYawPitchRoll(yaw, pitch, roll):
    yaw   = pm.PyNode(yaw)
    pitch = pm.PyNode(pitch)
    roll  = pm.PyNode(roll)
    
    for i in ['yaw', 'pitch', 'roll']:
        pm.addAttr(roll, ln=i, at='double', dv=0) 
        pm.setAttr(f'{roll.name()}.{i}', k=True, e=True)
        
    yaw.ry   >> roll.yaw
    pitch.rz >> roll.pitch
    roll.rx  >> roll.roll


#-------------------------------------------------------------------------------
#-- Create Driven Joint --------------------------------------------------------
def getPartName(name=''):
    tgt = name.split('_')
    res = ''
    if len(tgt) > 2:
        res = f'{tgt[0]}_{tgt[1]}'
    else:
        res = f'{tgt[0]}'
    return res


def createDrivenJoint(src, part='', num='', suf='drv'):
    #-- driven joint name
    src  = pm.PyNode(src)
    rad  = src.radius.get()
    name = f'{part}{num}_{suf}'

    #-- create driven joint
    drv = pm.duplicate(src, po=True)
    if drv:
        djt = pm.PyNode(drv[0])
        djt.rename(name)
        djt.radius.set(rad*1.5)
        return djt.name()
    else:
        return None
     
        
def setDrivenJointAttr(jt):
    jt   = pm.PyNode(jt)
    part = getPartName(jt)

    side = part.split('_')[0]
    if   'L' == side: jt.side.set(1)
    elif 'R' == side: jt.side.set(2)
    else:             jt.side.set(0)

    #-- set attribute
    jt.typ.set(18)
    jt.otp.set()
    jt.useOutlinerColor.set(1)
    jt.outlinerColor.set([1,0,0])
    jt.overrideEnabled.set(1)
    jt.overrideColor.set(13)
    composeRotate(jt)


def createSelectDrivenJoint(part=''):
    num = ''
    suf = 'drv'

    for src in pm.selected(typ='joint'):
        srcp = getPartName(src.name())
        newp = part.replace('{selected}', srcp)
        print(part, srcp)
        jt   = createDrivenJoint(src, newp, num, suf)
        setDrivenJointAttr(jt)

        #-- log
        print(f'Create Driven Joint: {src.name()} -> {jt}')


def createSingleDrivenJoint(src, part=''):
    src = pm.PyNode(src)
    num = ''
    suf = 'drv'

    jt = createDrivenJoint(src, part, num, suf)
    setDrivenJointAttr(jt)

    #-- log
    print(f'Create Driven Joint: {src.name()} -> {jt}')


def createSerialDrivenJoint(src, part='', st='', ed='', num=3):
    src = pm.PyNode(src)
    st  = pm.PyNode(st)
    ed  = pm.PyNode(ed)
    s = pm.xform(st, ws=True, t=True, q=True)
    e = pm.xform(ed, ws=True, t=True, q=True)

    den = num - 1
    oft = 1       #-- 0 or 1
    tip = 1 - oft #-- 0 or 1

    #-- driven joint 1 -> end
    for i in range(0, num + tip):
        x = ((e[0] - s[0]) / den) * i
        y = ((e[1] - s[1]) / den) * i
        z = ((e[2] - s[2]) / den) * i

        jt = createDrivenJoint(src, part, num=i)
        setDrivenJointAttr(jt)
        pm.move(s[0]+x, s[1]+y, s[2]+z, jt, a=True)
        print(f'Create Driven Joint: {src.name()} -> {jt}')


#-------------------------------------------------------------------------------
#-- Hierarchy ------------------------------------------------------------------
def duplicateReplaceName(s='', r='', po=False):
    selObj = pm.selected()
    if selObj:
        for i in selObj:
            orgList = pm.listRelatives(i, ad=True)
            orgList.reverse()
            orgList.insert(0, i)
            resList = [i.name() for i in orgList]
            #-- duplicate
            tgtList = mc.duplicate(i.name(), rc=True, po=po)
            for org, tgt in zip(orgList, tgtList):
                tgt = pm.PyNode(tgt)
                tgt.rename(org.name().replace(s, r))


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


def duplicateParentOnly():
    selObj = pm.selected()
    if selObj:
        for i in selObj:
            pm.duplicate(i, po=True)


#-- Create Node Above
def createNodeAbove(typ='transform', suf='_ax'):
    nodeList = []
    selObj = pm.selected()
    for i in selObj:
        if typ == 'locator':
            node = pm.spaceLocator(n=f'{i.name()}{suf}')
        else:
            node = pm.createNode(typ, n=f'{i.name()}{suf}')
        pm.delete(pm.parentConstraint(i, node, w=1, mo=False))

        pNode = pm.listRelatives(i, p=True)
        if pNode:
            pm.parent(node, pNode)
            pm.parent(i, node)
        else:
            pm.parent(i, node)
        nodeList.append(node)
    return nodeList


#-- Create Node Below
def createNodeBelow(typ='transform', suf='_grp'):
    nodeList = []
    selObj = pm.selected()
    for i in selObj:
        if typ == 'locator':
            node = pm.spaceLocator(n=f'{i.name()}{suf}')
        else:
            node = pm.createNode(typ, n=f'{i.name()}{suf}')
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
    selObj = pm.selected(typ='transform')

    if len(selObj)%2 == 0:
        for i in range(0, len(selObj), 2):
            pm.parent(selObj[i], selObj[i+1])
            pm.select(d=True)
    else:
        pm.warning('Please select even number size. selected size: %d .'%len(selObj))


#-- Array Parent
def arrayParent():
    selObj = pm.selected(typ='transform')
    h = len(selObj)//2
    chList = selObj[:h]
    paList = selObj[h:]
    
    for i in range(len(chList)):
        pm.parent(chList[i].name(), paList[i].name())