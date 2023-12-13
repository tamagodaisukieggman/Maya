# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mm



# arm  Ik To Fk
def armIkToFk(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
    side = mc.radioButtonGrp( 'sideChk',q=True,select=True )
    if side == 1:
        LR = 'L'
    else:
        LR = 'R'
    # printLR
    armIKctrl = ['hand_ _Ctrl', 'arm_ _PVCtrl']
    armIKPrxctrl = ['arm_ _IkDummyPosLoc', 'arm_ _PVCtrlDummyPoLoc']
    n=len(armIKPrxctrl)
    for i in xrange(0, n ,1):            
        prxSide = armIKPrxctrl[i].split(' ')
        ctrlSide = armIKctrl[i].split(' ')
        if LR == 'L' and NNsp is not None:
            prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]
        elif LR == 'R' and NNsp is not None:
            prxctrl = NNsp + prxSide[0] + 'R' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1]
        elif LR == 'L' and NNsp is None:
            prxctrl = prxSide[0] + 'L' + prxSide[1]
            ctrl =  ctrlSide[0] + 'L' + ctrlSide[1]
        elif LR == 'R' and NNsp is None:
            prxctrl = prxSide[0] + 'R' + prxSide[1]
            ctrl = ctrlSide[0] + 'R' + ctrlSide[1]
        value = mc.xform(prxctrl, q=True, t=True)
        mc.setAttr(( ctrl + '.translate') , *value)
		
# arm Fk To Ik
def armFkToIk(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
    side = mc.radioButtonGrp( 'sideChk',q=True,select=True )
    if side == 1:
        LR = 'L'
    else:
        LR = 'R'
    # printLR
    armFKctrl = ['upArm_ _fkCtrl', 'arm_ _fkCtrl']
    armFKPrxctrl = ['j15_arm_ _rigProxyJt', 'j16_foreArm_ _rigProxyJt']
    n=len(armFKPrxctrl)
    for i in xrange(0, n ,1):            
        prxSide = armFKPrxctrl[i].split(' ')
        ctrlSide = armFKctrl[i].split(' ')
        if LR == 'L' and NNsp is not None:
            prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]        
        elif LR == 'R' and NNsp is not None:
            prxctrl = NNsp + prxSide[0].replace('j1','j3') + 'R' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1]
        elif LR == 'L' and NNsp is None:
            prxctrl =  prxSide[0] + 'L' + prxSide[1]
            ctrl =  ctrlSide[0] + 'L' + ctrlSide[1]
        elif LR == 'R' and NNsp is None:
            prxctrl = prxSide[0].replace('j1','j3') + 'R' + prxSide[1]
            ctrl = ctrlSide[0] + 'R' + ctrlSide[1]

        if prxctrl.count('_R_') == 1:
            value = mc.xform(prxctrl.replace('j1','j3'), q=True, ro=True)
        else:
            value = mc.xform(prxctrl, q=True, ro=True)
        
        fkJntRotOrder = mc.getAttr('%s.rotateOrder'%prxctrl)
        fkCtrlRotOrder = mc.getAttr('%s.rotateOrder'%ctrl)
        
        if fkJntRotOrder != fkCtrlRotOrder:
            sel = mc.ls(sl=True)
            multMat = mc.createNode('multMatrix',n='multMatrix_armFk')
            decoMat = mc.createNode('decomposeMatrix',n='decomposeMatrix_armFk')
            quatToEuler = mc.createNode('quatToEuler',n='quatToEuler_armFk')

            mc.connectAttr('%s.worldMatrix[0]'%prxctrl,'%s.matrixIn[0]'%multMat)
            mc.connectAttr('%s.matrixSum'%multMat,'%s.inputMatrix'%decoMat)
            mc.connectAttr('%s.outputQuat'%decoMat,'%s.inputQuat'%quatToEuler)
            mc.connectAttr('%s.RotateOrder'%ctrl,'%s.inputRotateOrder'%quatToEuler)
            mc.connectAttr('%s.parentInverseMatrix[0]'%ctrl,'%s.matrixIn[1]'%multMat)

            changeRotValue = mc.getAttr('%s.outputRotate'%quatToEuler)
            
            mc.setAttr(( ctrl + '.rotate') , *changeRotValue[0])
            
            mc.delete(multMat,decoMat,quatToEuler)
            
            mc.select(sel,r=True)
            
        elif fkJntRotOrder == fkCtrlRotOrder:
            mc.setAttr(( ctrl + '.rotate') , *value)
	
# leg Ik To Fk
def legIkToFk(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
    side = mc.radioButtonGrp( 'sideChk',q=True,select=True )
    if side == 1:
        LR = 'L'
    else:
        LR = 'R'
    # printLR
    legIKctrl = ['leg_ _Ctrl', 'leg_ _PVCtrl', 'toe_ _Ctrl']
    legIKPrxctrl = ['leg_ _CtrlDummyPosLoc', 'leg_ _PVCtrlDummyPoLoc', 'toe_ _fkCtrl']
    n=len(legIKctrl)
    for i in xrange(0, n, 1):
        prxSide = legIKPrxctrl[i].split(' ')
        ctrlSide = legIKctrl[i].split(' ')
        if LR == 'L' and NNsp is not None:
            prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]        
        elif LR == 'R' and NNsp is not None:
            prxctrl = NNsp + prxSide[0] + 'R' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1] 
        elif LR == 'L' and NNsp is None:
            prxctrl = prxSide[0] + 'L' + prxSide[1]
            ctrl = ctrlSide[0] + 'L' + ctrlSide[1]
        elif LR == 'R' and NNsp is None:
            prxctrl = prxSide[0] + 'R' + prxSide[1]
            ctrl = ctrlSide[0] + 'R' + ctrlSide[1]
        if i == 0:                     
            valueTr = mc.xform(prxctrl, q=True, t=True)
            valueRo = mc.xform(prxctrl, q=True, ro=True)
            mc.setAttr(( ctrl + '.translate') , *valueTr)           
            mc.setAttr(( ctrl + '.rotate') , *valueRo)
        elif i == 1:
            valueTr = mc.xform(prxctrl, q=True, t=True)
            mc.setAttr(( ctrl + '.translate') , *valueTr)
        elif i == 2:
            valueRo= mc.xform(prxctrl, q=True, ro=True)
            mc.setAttr(( ctrl + '.rotate') , *valueRo) 
			
# leg Fk To Ik
def legFkToIk(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
    side = mc.radioButtonGrp( 'sideChk',q=True,select=True )
    if side == 1:
        LR = 'L'
    else:
        LR = 'R'
        
    # printLR
    legFKctrl = ['upLeg_ _fkCtrl', 'leg_ _fkCtrl', 'foot_ _fkCtrl', 'toe_ _fkCtrl']
    legFKPrxctrl = ['j02_upleg_ _rigProxyJt', 'j03_leg_ _rigProxyJt', 'j04_foot_ _rigProxyJt', 'j05_toe_ _rigProxyJt']
    n=len(legFKPrxctrl)
    for i in xrange(0, n ,1):            
        prxSide = legFKPrxctrl[i].split(' ')
        ctrlSide = legFKctrl[i].split(' ')
        if LR == 'L' and NNsp is not None:
            prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]        
        elif LR == 'R' and NNsp is not None:
            prxctrl = NNsp + prxSide[0] + 'R' + prxSide[1]
            ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1]
        elif LR == 'L' and NNsp is None:
            prxctrl =  prxSide[0] + 'L' + prxSide[1]
            ctrl =  ctrlSide[0] + 'L' + ctrlSide[1]
        elif LR == 'R' and NNsp is None:
            prxctrl = prxSide[0] + 'R' + prxSide[1]
            ctrl = ctrlSide[0] + 'R' + ctrlSide[1]
		
        if prxctrl.count('_R_') == 1:
            if prxctrl.count('_upleg_') == 1:
                value = mc.xform(prxctrl.replace('j02','j06'), q=True, ro=True)
                prxctrl = prxctrl.replace('j02','j06')
            elif prxctrl.count('_leg_') == 1:
                value = mc.xform(prxctrl.replace('j03','j07'), q=True, ro=True)
                prxctrl = prxctrl.replace('j03','j07')
            elif prxctrl.count('_foot_') == 1:
                value = mc.xform(prxctrl.replace('j04','j08'), q=True, ro=True)
                prxctrl = prxctrl.replace('j04','j08')
            elif prxctrl.count('_toe_') == 1:
                value = mc.xform(prxctrl.replace('j05','j09'), q=True, ro=True)
                prxctrl = prxctrl.replace('j05','j09')
				
        else:
            value = mc.xform(prxctrl, q=True, ro=True)
		
        
        fkJntRotOrder = mc.getAttr('%s.rotateOrder'%prxctrl)
        fkCtrlRotOrder = mc.getAttr('%s.rotateOrder'%ctrl)
        
        if fkJntRotOrder != fkCtrlRotOrder:
            sel = mc.ls(sl=True)
            multMat = mc.createNode('multMatrix',n='multMatrix_armFk')
            decoMat = mc.createNode('decomposeMatrix',n='decomposeMatrix_armFk')
            quatToEuler = mc.createNode('quatToEuler',n='quatToEuler_armFk')

            mc.connectAttr('%s.worldMatrix[0]'%prxctrl,'%s.matrixIn[0]'%multMat)
            mc.connectAttr('%s.matrixSum'%multMat,'%s.inputMatrix'%decoMat)
            mc.connectAttr('%s.outputQuat'%decoMat,'%s.inputQuat'%quatToEuler)
            mc.connectAttr('%s.RotateOrder'%ctrl,'%s.inputRotateOrder'%quatToEuler)
            mc.connectAttr('%s.parentInverseMatrix[0]'%ctrl,'%s.matrixIn[1]'%multMat)

            changeRotValue = mc.getAttr('%s.outputRotate'%quatToEuler)
            
            mc.setAttr(( ctrl + '.rotate') , *changeRotValue[0])
            
            mc.delete(multMat,decoMat,quatToEuler)
            
            mc.select(sel,r=True)
            
        elif fkJntRotOrder == fkCtrlRotOrder:
            mc.setAttr(( ctrl + '.rotate') , *value)

        
"""
####LR対応版###
"""
# arm  Ik To Fk
def armIkToFkLR(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
    
    lr = ['L','R']#
    
    for LR in lr: #
        armIKctrl = ['hand_ _Ctrl', 'arm_ _PVCtrl']
        armIKPrxctrl = ['arm_ _IkDummyPosLoc', 'arm_ _PVCtrlDummyPoLoc']
        n=len(armIKPrxctrl)
        for i in xrange(0, n ,1):            
            prxSide = armIKPrxctrl[i].split(' ')
            ctrlSide = armIKctrl[i].split(' ')
            if LR == 'L' and NNsp is not None:
                prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]
            elif LR == 'R' and NNsp is not None:
                prxctrl = NNsp + prxSide[0] + 'R' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1]
            elif LR == 'L' and NNsp is None:
                prxctrl = prxSide[0] + 'L' + prxSide[1]
                ctrl =  ctrlSide[0] + 'L' + ctrlSide[1]
            elif LR == 'R' and NNsp is None:
                prxctrl = prxSide[0] + 'R' + prxSide[1]
                ctrl = ctrlSide[0] + 'R' + ctrlSide[1]
            value = mc.xform(prxctrl, q=True, t=True)
            mc.setAttr(( ctrl + '.translate') , *value)


# arm Fk To Ik
def armFkToIkLR(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
        
    lr = ['L','R']#
    
    for LR in lr: #
        armFKctrl = ['upArm_ _fkCtrl', 'arm_ _fkCtrl']
        armFKPrxctrl = ['j15_arm_ _rigProxyJt', 'j16_foreArm_ _rigProxyJt']
        n=len(armFKPrxctrl)
        for i in xrange(0, n ,1):            
            prxSide = armFKPrxctrl[i].split(' ')
            ctrlSide = armFKctrl[i].split(' ')
            if LR == 'L' and NNsp is not None:
                prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]        
            elif LR == 'R' and NNsp is not None:
                prxctrl = NNsp + prxSide[0].replace('j1','j3') + 'R' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1]
            elif LR == 'L' and NNsp is None:
                prxctrl =  prxSide[0] + 'L' + prxSide[1]
                ctrl =  ctrlSide[0] + 'L' + ctrlSide[1]
            elif LR == 'R' and NNsp is None:
                prxctrl = prxSide[0].replace('j1','j3') + 'R' + prxSide[1]
                ctrl = ctrlSide[0] + 'R' + ctrlSide[1]

            if prxctrl.count('_R_') == 1:
                value = mc.xform(prxctrl.replace('j1','j3'), q=True, ro=True)
            else:
                value = mc.xform(prxctrl, q=True, ro=True)

            fkJntRotOrder = mc.getAttr('%s.rotateOrder'%prxctrl)
            fkCtrlRotOrder = mc.getAttr('%s.rotateOrder'%ctrl)
            
            if fkJntRotOrder != fkCtrlRotOrder:
                sel = mc.ls(sl=True)
                multMat = mc.createNode('multMatrix',n='multMatrix_armFk')
                decoMat = mc.createNode('decomposeMatrix',n='decomposeMatrix_armFk')
                quatToEuler = mc.createNode('quatToEuler',n='quatToEuler_armFk')

                mc.connectAttr('%s.worldMatrix[0]'%prxctrl,'%s.matrixIn[0]'%multMat)
                mc.connectAttr('%s.matrixSum'%multMat,'%s.inputMatrix'%decoMat)
                mc.connectAttr('%s.outputQuat'%decoMat,'%s.inputQuat'%quatToEuler)
                mc.connectAttr('%s.RotateOrder'%ctrl,'%s.inputRotateOrder'%quatToEuler)
                mc.connectAttr('%s.parentInverseMatrix[0]'%ctrl,'%s.matrixIn[1]'%multMat)

                changeRotValue = mc.getAttr('%s.outputRotate'%quatToEuler)
                
                mc.setAttr(( ctrl + '.rotate') , *changeRotValue[0])
                
                mc.delete(multMat,decoMat,quatToEuler)
                
                mc.select(sel,r=True)
                
            elif fkJntRotOrder == fkCtrlRotOrder:
                mc.setAttr(( ctrl + '.rotate') , *value)
            
            
	
# leg Ik To Fk
def legIkToFkLR(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
        
    lr = ['L','R']#
    
    for LR in lr: #
        legIKctrl = ['leg_ _Ctrl', 'leg_ _PVCtrl', 'toe_ _Ctrl']
        legIKPrxctrl = ['leg_ _CtrlDummyPosLoc', 'leg_ _PVCtrlDummyPoLoc', 'toe_ _fkCtrl']
        n=len(legIKctrl)
        for i in xrange(0, n, 1):
            prxSide = legIKPrxctrl[i].split(' ')
            ctrlSide = legIKctrl[i].split(' ')
            if LR == 'L' and NNsp is not None:
                prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]        
            elif LR == 'R' and NNsp is not None:
                prxctrl = NNsp + prxSide[0] + 'R' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1] 
            elif LR == 'L' and NNsp is None:
                prxctrl = prxSide[0] + 'L' + prxSide[1]
                ctrl = ctrlSide[0] + 'L' + ctrlSide[1]
            elif LR == 'R' and NNsp is None:
                prxctrl = prxSide[0] + 'R' + prxSide[1]
                ctrl = ctrlSide[0] + 'R' + ctrlSide[1]
            if i == 0:                     
                valueTr = mc.xform(prxctrl, q=True, t=True)
                valueRo = mc.xform(prxctrl, q=True, ro=True)
                mc.setAttr(( ctrl + '.translate') , *valueTr)           
                mc.setAttr(( ctrl + '.rotate') , *valueRo)
            elif i == 1:
                valueTr = mc.xform(prxctrl, q=True, t=True)
                mc.setAttr(( ctrl + '.translate') , *valueTr)
            elif i == 2:
                valueRo= mc.xform(prxctrl, q=True, ro=True)
                mc.setAttr(( ctrl + '.rotate') , *valueRo) 
			
# leg Fk To Ik
def legFkToIkLR(*args):
    nmsp = mc.textScrollList('nmspList',q=True,si=True)
    if nmsp is not None:
        NNsp = nmsp[0] + ':'
    else:
        NNsp = None
        
    lr = ['L','R']#
    
    for LR in lr: #
        legFKctrl = ['upLeg_ _fkCtrl', 'leg_ _fkCtrl', 'foot_ _fkCtrl', 'toe_ _fkCtrl']
        legFKPrxctrl = ['j02_upleg_ _rigProxyJt', 'j03_leg_ _rigProxyJt', 'j04_foot_ _rigProxyJt', 'j05_toe_ _rigProxyJt']
        n=len(legFKPrxctrl)
        for i in xrange(0, n ,1):            
            prxSide = legFKPrxctrl[i].split(' ')
            ctrlSide = legFKctrl[i].split(' ')
            if LR == 'L' and NNsp is not None:
                prxctrl = NNsp + prxSide[0] + 'L' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'L' + ctrlSide[1]        
            elif LR == 'R' and NNsp is not None:
                prxctrl = NNsp + prxSide[0] + 'R' + prxSide[1]
                ctrl = NNsp + ctrlSide[0] + 'R' + ctrlSide[1]
            elif LR == 'L' and NNsp is None:
                prxctrl =  prxSide[0] + 'L' + prxSide[1]
                ctrl =  ctrlSide[0] + 'L' + ctrlSide[1]
            elif LR == 'R' and NNsp is None:
                prxctrl = prxSide[0] + 'R' + prxSide[1]
                ctrl = ctrlSide[0] + 'R' + ctrlSide[1]
            
            if prxctrl.count('_R_') == 1:
                if prxctrl.count('_upleg_') == 1:
                    value = mc.xform(prxctrl.replace('j02','j06'), q=True, ro=True)
                    prxctrl = prxctrl.replace('j02','j06')
                elif prxctrl.count('_leg_') == 1:
                    value = mc.xform(prxctrl.replace('j03','j07'), q=True, ro=True)
                    prxctrl = prxctrl.replace('j03','j07')
                elif prxctrl.count('_foot_') == 1:
                    value = mc.xform(prxctrl.replace('j04','j08'), q=True, ro=True)
                    prxctrl = prxctrl.replace('j04','j08')
                elif prxctrl.count('_toe_') == 1:
                    value = mc.xform(prxctrl.replace('j05','j09'), q=True, ro=True)
                    prxctrl = prxctrl.replace('j05','j09')
                    
            else:
                value = mc.xform(prxctrl, q=True, ro=True)
            
            fkJntRotOrder = mc.getAttr('%s.rotateOrder'%prxctrl)
            fkCtrlRotOrder = mc.getAttr('%s.rotateOrder'%ctrl)
            
            if fkJntRotOrder != fkCtrlRotOrder:
                sel = mc.ls(sl=True)
                multMat = mc.createNode('multMatrix',n='multMatrix_armFk')
                decoMat = mc.createNode('decomposeMatrix',n='decomposeMatrix_armFk')
                quatToEuler = mc.createNode('quatToEuler',n='quatToEuler_armFk')

                mc.connectAttr('%s.worldMatrix[0]'%prxctrl,'%s.matrixIn[0]'%multMat)
                mc.connectAttr('%s.matrixSum'%multMat,'%s.inputMatrix'%decoMat)
                mc.connectAttr('%s.outputQuat'%decoMat,'%s.inputQuat'%quatToEuler)
                mc.connectAttr('%s.RotateOrder'%ctrl,'%s.inputRotateOrder'%quatToEuler)
                mc.connectAttr('%s.parentInverseMatrix[0]'%ctrl,'%s.matrixIn[1]'%multMat)

                changeRotValue = mc.getAttr('%s.outputRotate'%quatToEuler)
                
                mc.setAttr(( ctrl + '.rotate') , *changeRotValue[0])
                
                mc.delete(multMat,decoMat,quatToEuler)
                
                mc.select(sel,r=True)
                
            elif fkJntRotOrder == fkCtrlRotOrder:
                mc.setAttr(( ctrl + '.rotate') , *value)

	