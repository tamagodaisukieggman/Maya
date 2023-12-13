# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mm
import mtk3d.maya.rig.cyMatchController.module.bakeCmds as bake
import mtk3d.maya.rig.cyMatchController.module.matchFuncs as match

reload(bake)
reload(match)

def exeIKFK(*args):
    bakSts=mc.checkBox( 'bakeOnOff',q=True,v=True )
    Prts = mc.radioButtonGrp( 'partsChk',q=True,select=True )
    
    #LRチェックボックスの正誤
    boolLR = mc.checkBox('boxLR',q=True,v=True)
    #ArmLegチェックボックスの正誤
    boolArmLeg = mc.checkBox('boxArmLeg',q=True,v=True)
    
    if bakSts == 1:
        print 'bake'
        bake.bakeCmds()    
    elif boolArmLeg == False and boolLR == False:#
        print 'batch IK'
        if Prts == 1:
            match.armIkToFk()
        elif Prts == 2:
            match.legIkToFk()
    
    #LRチェックボックスがOn,ArmLegチェックボックスがOff,Armを選択しているとき
    elif boolLR == True and boolArmLeg == False and Prts == 1:#
        match.armIkToFkLR()
    
    #LRチェックボックスがOn,ArmLegチェックボックスがOff,Legを選択しているとき
    elif boolLR == True and boolArmLeg == False and Prts == 2:#
        match.legIkToFkLR()
    
    #LRチェックボックスがOff,ArmLegチェックボックスがOnのとき
    elif boolLR == False and boolArmLeg == True:#
        match.armIkToFk()
        match.legIkToFk()
    
    #LRチェックボックスがOn,ArmLegチェックボックスがOnのとき
    elif boolLR == True and boolArmLeg == True:#
        match.armIkToFkLR()
        match.legIkToFkLR()


def exeFKIK(*args):
    bakSts=mc.checkBox( 'bakeOnOff',q=True,v=True )
    Prts = mc.radioButtonGrp( 'partsChk',q=True,select=True )
    
    boolLR = mc.checkBox('boxLR',q=True,v=True)
    boolArmLeg = mc.checkBox('boxArmLeg',q=True,v=True)
    
    if bakSts == 1:
        print 'bake'
        bake.bakeCmds()    
    elif boolArmLeg == False and boolLR == False:#
        print 'batch IK'
        if Prts == 1:
            match.armFkToIk()
        elif Prts == 2:
            match.legFkToIk()
            
    elif boolLR == True and boolArmLeg == False and Prts == 1:#
        match.armFkToIkLR()
        
    elif boolLR == True and boolArmLeg == False and Prts == 2:#
        match.legFkToIkLR()
        
    elif boolLR == False and boolArmLeg == True:#
        match.armFkToIk()
        match.legFkToIk()
        
    elif boolLR == True and boolArmLeg == True:#
        match.armFkToIkLR()
        match.legFkToIkLR()
