# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mm

def chkOnCmd(*args):
    mc.button('getNss',e=True, en=True)
    mc.button('deselBtn',e=True, en=True)
    mc.textScrollList('nmspList',e=True, en=True)

def chkOffCmd(*args):
    mc.button('getNss',e=True, en=False)
    mc.button('deselBtn',e=True, en=False)
    mc.textScrollList('nmspList',e=True, removeAll=True)
    mc.textScrollList('nmspList',e=True, en=False)

def bakeOnCmd(*args):
    sts = mc.radioButtonGrp('bakeType', q = True ,select = True)
    if sts == 1:
        mc.button('FKButton',e = True, en = True)
        mc.button('IKButton',e = True, en = False)
        mc.radioButtonGrp('bakeType', e = True ,en = True)
    elif sts == 2:
        mc.button('FKButton',e = True, en = False)
        mc.button('IKButton',e = True, en = True)
        mc.radioButtonGrp('bakeType', e = True ,en = True)
        
def bakeOffCmd(*args):
    mc.button('FKButton',e = True, en = True)
    mc.button('IKButton',e = True, en = True)
    mc.radioButtonGrp('bakeType', e = True ,en = False)
 
def FkButnChk(*args):
    mc.button('FKButton',e = True, en = True)
    mc.button('IKButton',e = True, en = False)

def IkButnChk(*args):
    mc.button('FKButton',e = True, en = False)
    mc.button('IKButton',e = True, en = True)
    
def offLRCmd(*args): #
    mc.radioButtonGrp('sideChk', e=True, en=True) #

def onLRCmd(*args): #
    mc.radioButtonGrp('sideChk', e=True, en=False) #
    
def offArmLegCmd(*args): #
    mc.radioButtonGrp('partsChk', e=True, en=True) #

def onArmLegCmd(*args): #
    mc.radioButtonGrp('partsChk', e=True, en=False) #

def radioChangeHandsLegs(*args):
    handsPrts = mc.radioButtonGrp( 'radioHand',q=True,select=True)
    legsPrts = mc.radioButtonGrp( 'radioLegs',q=True,select=True)
    
    if handsPrts == 1 or handsPrts == 2 and legsPrts == 0:
        mc.radioButtonGrp('partsChk', e=True,select=1)
        mc.radioButtonGrp('sideChk', e=True,select=handsPrts)
        
    elif legsPrts == 1 or legsPrts == 2 and handsPrts == 0:
        mc.radioButtonGrp('partsChk', e=True,select=2)
        mc.radioButtonGrp('sideChk', e=True,select=legsPrts)
        
def radioChangeVis(*args):
    checkedBoxLR = mc.checkBox('boxLR',q=True,v = True)#
    checkedBoxArmLeg = mc.checkBox('boxArmLeg',q=True,v = True)#
    
    if checkedBoxLR == True or checkedBoxArmLeg == True:
        mc.radioButtonGrp( 'radioHand',e=True,vis=False)
        mc.radioButtonGrp( 'radioLegs',e=True,vis=False)    
        mc.radioButtonGrp('partsChk', e=True,vis=True)
        mc.radioButtonGrp('sideChk', e=True,vis=True)

    else:
        mc.radioButtonGrp('partsChk', e=True,vis=False)
        mc.radioButtonGrp('sideChk', e=True,vis=False)
        mc.radioButtonGrp( 'radioHand',e=True,vis=True)
        mc.radioButtonGrp( 'radioLegs',e=True,vis=True)
    
    
    
