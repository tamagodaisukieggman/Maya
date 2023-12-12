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



#-- Basic Mirror ---------------------------------------------------------------
def setMirror(s='', t=''):
    s  = pm.PyNode(s)
    t  = pm.PyNode(t)
    tv = s.t.get()
    rv = s.r.get()
    
    t.t.set(tv[0]*-1, tv[1], tv[2])
    t.r.set(rv[0], rv[1]*-1, rv[2]*-1)


def duplicateMirror(s='', r='', v=1):
    resList = []
    o = pm.selected()
    if o:
        o = pm.selected()[0]
        org = pm.PyNode(o)
        
        orgList = pm.listRelatives(org, ad=True)
        #orgList.reverse()
        orgList.insert(0, org)
        #resList = [i.name() for i in orgList]
        print(orgList)

        #-- duplicate
        tgt = pm.duplicate(org, rc=True, po=False)[0]
        tgtList = pm.listRelatives(tgt, ad=True)
        #orgList.reverse()
        tgtList.insert(0, tgt)
        print(tgtList)
        
        
        for org, tgt in zip(orgList, tgtList):
            tgt.rename(org.replace(s, r))

            #-- mirror
            tgtType = pm.nodeType(tgt)
            if tgtType == 'transform' or tgtType == 'joint':
                setMirror(org, tgt)

            #-- set side
            if v:
                switchSide(tgt)
    else:
        pm.warning('Please select joint or transform node to mirror.')


#-- behavior -------------------------------------------------------------------
def setBehavior(s='', t=''):
    s = pm.PyNode(s)
    t = pm.PyNode(t)

    pos = pm.spaceLocator(n=f'__{s.name()}__pos')
    pm.delete(pm.parentConstraint(s, pos, mo=False, w=1.0))

    tv = pm.xform(s, ws=True, t=True, q=True)
    rv = pm.xform(s, ws=True, ro=True, q=True)
    
    pos.t.set(tv[0]*-1, tv[1], tv[2])
    pos.r.set(rv[0]-180, rv[1]*-1, rv[2])

    pm.delete(pm.parentConstraint(pos, t, mo=False, w=1.0))
    pm.delete(pos)


def duplicateBehavior(s='', r='', v=1):
    resList = []
    o = pm.selected()
    if o:
        o = pm.selected()[0]
        org = pm.PyNode(o)
        
        if pm.nodeType(org) == 'joint':
            #-- get original hierarchy
            orgList = pm.listRelatives(org, ad=True)
            orgList.insert(0, org)
       
            #-- mirror joint 
            dupList = pm.mirrorJoint(org, myz=True, mb=True)
            tgt = pm.PyNode(dupList[0])
            tgtList = pm.listRelatives(tgt, ad=True)
            tgtList.insert(0, tgt)

            #-- rename and switch side
            for org, tgt in zip(orgList, tgtList):
                tgt.rename(org.replace(s, r))
                switchSide(tgt)
                resList.append(tgt)

        else:
            #-- temporary parent
            pa     = org.getParent() #-- parent of original
            orgTmp = pm.createNode('joint', n='__temp')
            if pa:
                pm.delete(pm.parentConstraint(pa, orgTmp, mo=False, w=1.0))
            org.setParent(orgTmp)    #-- parent to temporary root

            #-- get original hierarchy
            orgList = pm.listRelatives(orgTmp, ad=True)
            #orgList.insert(0, orgTmp)
            print(orgList)
       
            #-- mirror joint 
            dupList = pm.mirrorJoint(orgTmp, myz=True, mb=True)
            dupTmp  = pm.PyNode(dupList[0])
            tgt = pm.PyNode(dupList[1])
            tgtList = pm.listRelatives(dupTmp, ad=True)
            #tgtList.insert(0, dupTmp)
            print(tgtList)

            #-- rename
            for org, tgt in zip(orgList, tgtList):
                tgt.rename(org.replace(s, r))
                switchSide(tgt)
                resList.append(tgt)
                
            #-- set hierarchy
            if pa:
                org.setParent(pa)
                tgt.setParent(pa)
            else:
                org.setParent(w=True)
                tgt.setParent(w=True)
            pm.delete(orgTmp)
            pm.delete(dupTmp)
    else:
        pm.warning('Please select joint or transform node to mirror.')


#-- Swing ----------------------------------------------------------------------
def setSwing(s='', t=''):
    s = pm.PyNode(s)
    t = pm.PyNode(t)

    pos = pm.spaceLocator(n=f'__{s.name()}__pos')
    pm.delete(pm.parentConstraint(s, pos, mo=False, w=1.0))

    tv = pm.xform(s, ws=True, t=True, q=True)
    rv = pm.xform(s, ws=True, ro=True, q=True)
    
    pos.t.set(tv[0]*-1, tv[1], tv[2])
    pos.r.set(180-rv[0], rv[1], -180-rv[2])

    pm.delete(pm.parentConstraint(pos, t, mo=False, w=1.0))
    pm.delete(pos)


def duplicateSwing(s='', r='', v=1):
    resList = []
    o = pm.selected()
    if o:
        o = pm.selected()[0]
        org = pm.PyNode(o)
    
        orgList = pm.listRelatives(org, ad=True)
        orgList.reverse()
        orgList.insert(0, org)
        print(orgList)

        #-- duplicate
        tgt = pm.duplicate(org, rc=True, po=False)[0]
        tgtList = pm.listRelatives(tgt, ad=True)
        tgtList.reverse()
        tgtList.insert(0, tgt)
        print(tgtList)

        #-- rename
        for org, tgt in zip(orgList, tgtList):
            tgt.rename(org.replace(s, r))

            tgtType = pm.nodeType(tgt)
            if tgtType == 'transform' or tgtType == 'joint':
                setSwing(org, tgt)

                #-- set side
                if v:
                    switchSide(tgt)
    else:
        pm.warning('Please select joint or transform node to mirror.')


def switchSide(t=''):
    if pm.nodeType(t) == 'joint':
        jt = pm.PyNode(t)
        side = jt.side.get()
        if side == 1:
            jt.side.set(2)
        elif side == 2:
            jt.side.set(1)

