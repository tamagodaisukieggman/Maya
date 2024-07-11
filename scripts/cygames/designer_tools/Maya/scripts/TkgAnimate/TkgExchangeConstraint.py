# -*- coding: cp932 -*-
#-------------------------------------------------------------------------------------------
#   Author: Daichi Ishikawa
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel
import os

toolName = "TkgExchangeConstraint"
scriptPrefix= toolName + "."
uiPrefix= toolName + "UI"

#-------------------------------------------------------------------------------------------
#   UI
#-------------------------------------------------------------------------------------------
def UI():

    width=250
    height=1
    formWidth=width-5
    
    windowTitle=scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"

    checkDoubleWindow(windowName)
    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=1,mnb=True,mxb=False,rtf=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.checkBox(uiPrefix + "CheckBoxFilter",label="���̃R���X�g���C���g����ێ�����"
                          )
    cmds.separator( style='in',h=15,w=formWidth)
    cmds.button( label="Exchange Constraint",w=formWidth,command=scriptPrefix+"exchangeConstraintRoot()")

    cmds.separator( style='in',h=15,w=formWidth)

    cmds.showWindow(windowName)

#-------------------------------------------------------------------------------------------
#   �E�B���h�E�̓�d�\���`�F�b�N
#-------------------------------------------------------------------------------------------
def checkDoubleWindow(windowName):

    if cmds.window( windowName, exists=True ):
        cmds.deleteUI(windowName, window=True )
    else:
        if cmds.windowPref( windowName, exists=True ):
            cmds.windowPref( windowName, remove=True )
            
#-------------------------------------------------------------------------------------------
#   ���s
#-------------------------------------------------------------------------------------------
def exchangeConstraintRoot():
    
    SelectList = cmds.ls(sl=True)

    for cnt in range (len(SelectList)):
        constraintName = SelectList[cnt]
        constraintObjectType = cmds.objectType(constraintName)

        if constraintObjectType == "pointConstraint":
            constraintType = "Point"

        elif constraintObjectType == "scaleConstraint":
            constraintType = "Scale"
            
        elif constraintObjectType == "orientConstraint":
            constraintType = "Orient"
            
        elif constraintObjectType == "parentConstraint":
            constraintType = "Parent"
        else:
            print("ERROR:�R���X�g���C���g�łȂ��I�u�W�F�N�g���A�Ή����Ă��Ȃ��R���X�g���C���g���I������Ă��܂��B")
            return

        exchangeConstraint(constraintName,constraintType)

#-------------------------------------------------------------------------------------------
#   exchangePointConstraint
#-------------------------------------------------------------------------------------------
def exchangeConstraint(constraintName,constraintType):

    checkBoxFilter = cmds.checkBox(uiPrefix + "CheckBoxFilter", q=True, v=True)
    
    ConstraintAttrList = cmds.listAttr(constraintName,keyable=True)
    ConstraintWeightList = cmds.listAttr(constraintName,userDefined=True)
    if len(ConstraintWeightList) > 1:
        print("ERROR:��Έ�̃R���X�g���C���g�̂݌����ł��܂�")
        return

    #��]�I�u�W�F�N�g�擾
    ConnectList = cmds.listConnections(constraintName,p=True,c=True)
    if ConnectList == None:
        return
    drawInfo =[]
    for cnt in range (len(ConnectList)):
        if '.parentMatrix' in ConnectList[cnt]:
            parentMatrix = ConnectList[cnt]
        elif '.constraintParentInverseMatrix' in ConnectList[cnt]:
            parentInverseMatrix = ConnectList[cnt]
        elif '.drawInfo' in ConnectList[cnt]:
            drawInfo = ConnectList[cnt]
    
    masterName = parentMatrix.split(".")[0]
    servantName = cmds.listConnections(parentInverseMatrix)[0]

    drawInfoName = ""
    if len(drawInfo) > 0:
        drawInfoName = drawInfo.split(".")[0]

    #�R���X�g���C���g�̐e��2�ȏ゠��ۂ̃G���[���
    ConnectList2 = cmds.listConnections(constraintName,s=True)
    ConnectList3 =[]
    
    for cnt in range (len(ConnectList2)):
        if masterName == ConnectList2[cnt] or servantName == ConnectList2[cnt] or constraintName == ConnectList2[cnt] or drawInfoName == ConnectList2[cnt]:
            pass
        else:
            ConnectList3.append(ConnectList2[cnt])

    if len(ConnectList3) > 0:
        print("ERROR:��Έ�̃R���X�g���C���g�̂݌����ł��܂�")
        return

    #�A�g���r���[�g�擾
    constraintNode = cmds.getAttr(constraintName + ".nodeState")
    constraintWeight = cmds.getAttr(constraintName + "." + ConstraintWeightList[0])
    if constraintType == "Orient" or constraintType == "Parent":
        constraintInterp = cmds.getAttr(constraintName + ".interpType")

    #�|�C���g�R���X�g���C���ݒ�쐬
    if constraintType == "Point":
        settingNewConstraint = makeSettingPointConstraint(constraintName,constraintWeight,ConnectList)
    elif constraintType == "Scale":
        settingNewConstraint = makeSettingScaleConstraint(constraintName,constraintWeight,ConnectList)
    elif constraintType == "Orient":
        settingNewConstraint = makeSettingOrientConstraint(constraintName,constraintWeight,ConnectList)
    elif constraintType == "Parent":
        settingNewConstraint = makeSettingParentConstraint(constraintName,constraintWeight,ConnectList)

    #�A�g���r���[�g�����b�N����Ă����ۂ̃G���[���
    axisLock = getAttrlocked(masterName,settingNewConstraint,constraintType)
    if axisLock == False:
        print("ERROR:�ړI�̃A�g���r���[�g�����b�N����Ă��܂�")
        return
    
    #pointConstarint�AorientConstarint�̐e��parentConstraint�ɐڑ�����Ă����ۂ̃G���[���
    if constraintType == "Point" or constraintType == "Orient":
        masterConstraintInfo = getMasterConstraintInfo(masterName)
    else:
        masterConstraintInfo = True
        
    if masterConstraintInfo == False:
        print("ERROR:�I�u�W�F�N�g�͂��łɐڑ�����Ă��܂��B")
        return
    
    #�R���X�g���C���폜
    cmds.delete(constraintName)
    
    #�R���X�g���C���쐬
    newConstraint = makeNewConstraint(masterName,servantName,settingNewConstraint,constraintType)
    
    #�A�g���r���[�g�ݒ�
    cmds.setAttr(masterName + "|" + newConstraint + ".nodeState",constraintNode)    
    if constraintType == "Orient" or constraintType == "Parent":
        cmds.setAttr(masterName + "|" + newConstraint + ".interpType" , constraintInterp)
    if len(drawInfo) > 0:
        cmds.connectAttr(drawInfo, newConstraint + '.drawOverride' )
        
    #�R���X�g���C���I��
    cmds.select(masterName + "|" + newConstraint)
    
    if checkBoxFilter == True:
        cmds.rename(constraintName)

#-------------------------------------------------------------------------------------------
#   makeSettingPointConstraint
#-------------------------------------------------------------------------------------------
def makeSettingPointConstraint(constraintName,constraintWeight,ConnectList):
    settingNewConstraint = [1, 0,0,0, 1,1,1, 1,"",1]

    if  constraintName + '.constraintTranslateX' in  ConnectList:
        settingNewConstraint[4] = 0
    if  constraintName + '.constraintTranslateY' in  ConnectList:
        settingNewConstraint[5] = 0
    if  constraintName + '.constraintTranslateZ' in  ConnectList:
        settingNewConstraint[6] = 0
    
    settingNewConstraint[7] = constraintWeight

    return settingNewConstraint

#-------------------------------------------------------------------------------------------
#   makeSettingScaleConstraint
#-------------------------------------------------------------------------------------------
def makeSettingScaleConstraint(constraintName,constraintWeight,ConnectList):
    settingNewConstraint = [1, 0,0,0, 1,1,1, 1,"",1]

    if  constraintName + '.constraintScaleX' in  ConnectList:
        settingNewConstraint[4] = 0
    if  constraintName + '.constraintScaleY' in  ConnectList:
        settingNewConstraint[5] = 0
    if  constraintName + '.constraintScaleZ' in  ConnectList:
        settingNewConstraint[6] = 0
    
    settingNewConstraint[7] = constraintWeight

    return settingNewConstraint

#-------------------------------------------------------------------------------------------
#   makeSettingOrientConstraint
#-------------------------------------------------------------------------------------------
def makeSettingOrientConstraint(constraintName,constraintWeight,ConnectList):
    settingNewConstraint = [1, 0,0,0, 1,1,1, 1,"",1]

    if  constraintName + '.constraintRotateX' in  ConnectList:
        settingNewConstraint[4] = 0
    if  constraintName + '.constraintRotateY' in  ConnectList:
        settingNewConstraint[5] = 0
    if  constraintName + '.constraintRotateZ' in  ConnectList:
        settingNewConstraint[6] = 0
    
    settingNewConstraint[7] = constraintWeight

    return settingNewConstraint

#-------------------------------------------------------------------------------------------
#   makeSettingParentConstraint
#-------------------------------------------------------------------------------------------
def makeSettingParentConstraint(constraintName,constraintWeight,ConnectList):
    settingNewConstraint = [1, 1,1,1, 1,1,1, 1,"",1]

    if  constraintName + '.constraintTranslateX' in  ConnectList:
        settingNewConstraint[1] = 0
    if  constraintName + '.constraintTranslateY' in  ConnectList:
        settingNewConstraint[2] = 0
    if  constraintName + '.constraintTranslateZ' in  ConnectList:
        settingNewConstraint[3] = 0
    
    if  constraintName + '.constraintRotateX' in  ConnectList:
        settingNewConstraint[4] = 0
    if  constraintName + '.constraintRotateY' in  ConnectList:
        settingNewConstraint[5] = 0
    if  constraintName + '.constraintRotateZ' in  ConnectList:
        settingNewConstraint[6] = 0
    
    settingNewConstraint[7] = constraintWeight

    return settingNewConstraint

#-------------------------------------------------------------------------------------------
#   makeNewConstraint
#-------------------------------------------------------------------------------------------
def makeNewConstraint(masterName,servantName,settingNewConstraint,constraintType):
    cmds.select(servantName, r=True)
    cmds.select(masterName, add=True)


    mel.eval('doCreate' + constraintType + 'ConstraintArgList 1 { "' +str(settingNewConstraint[0])+
                                                               '","' +str(settingNewConstraint[1])+
                                                               '","' +str(settingNewConstraint[2])+
                                                               '","' +str(settingNewConstraint[3])+
                                                               '","' +str(settingNewConstraint[4])+
                                                               '","' +str(settingNewConstraint[5])+
                                                               '","' +str(settingNewConstraint[6])+
                                                               '","' +str(settingNewConstraint[7])+
                                                               '","' +str(settingNewConstraint[8])+
                                                               '","' +str(settingNewConstraint[9])+
                                                               '" };')

    ConnectList = cmds.listConnections(masterName,p=True,d=True)

    if constraintType == "Point":
        selctConstraintType = "pointConstraint"
    elif constraintType == "Scale":
        selctConstraintType = "scaleConstraint"
    elif constraintType == "Orient":
        selctConstraintType = "orientConstraint"
    elif constraintType == "Parent":
        selctConstraintType = "parentConstraint"

        
    for cnt in range (len(ConnectList)):
        if 'constraintParentInverseMatrix' in ConnectList[cnt] and selctConstraintType in ConnectList[cnt]:
            parentInverseMatrix = ConnectList[cnt]

    result = parentInverseMatrix.split(".")[0]
    
    return result
    
#-------------------------------------------------------------------------------------------
#   �ړI�A�g���r���[�g�̃��b�N���i�A�g���r���[�g�����b�N����Ă鎞�̃G���[���
#-------------------------------------------------------------------------------------------
def getAttrlocked(masterName,settingNewConstraint,constraintType):
    
    axisList0 = settingNewConstraint[1]
    axisList1 = settingNewConstraint[2]
    axisList2 = settingNewConstraint[3]
    axisList3 = settingNewConstraint[4]
    axisList4 = settingNewConstraint[5]
    axisList5 = settingNewConstraint[6]
    
    axisList = [axisList0,axisList1,axisList2,axisList3,axisList4,axisList5]
    lockList = [0,0,0,1,1,1]
    
    if constraintType == "Point":
        tx_lock = cmds.getAttr(masterName + '.tx', l = True)
        ty_lock = cmds.getAttr(masterName + '.ty', l = True)
        tz_lock = cmds.getAttr(masterName + '.tz', l = True)

        if tx_lock == False:
            lockList[3] = 0
        if ty_lock == False:
            lockList[4] = 0
        if tz_lock == False:
            lockList[5] = 0

    elif constraintType == "Scale":
        sx_lock = cmds.getAttr(masterName + '.sx', l = True)
        sy_lock = cmds.getAttr(masterName + '.sy', l = True)
        sz_lock = cmds.getAttr(masterName + '.sz', l = True)

        if sx_lock == False:
            lockList[3] = 0
        if sy_lock == False:
            lockList[4] = 0
        if sz_lock == False:
            lockList[5] = 0
        
    elif constraintType == "Orient":
        rx_lock = cmds.getAttr(masterName + '.rx', l = True)
        ry_lock = cmds.getAttr(masterName + '.ry', l = True)
        rz_lock = cmds.getAttr(masterName + '.rz', l = True)

        if rx_lock == False:
            lockList[3] = 0
        if ry_lock == False:
            lockList[4] = 0
        if rz_lock == False:
            lockList[5] = 0
                
    elif constraintType == "Parent":
        tx_lock = cmds.getAttr(masterName + '.tx', l = True)
        ty_lock = cmds.getAttr(masterName + '.ty', l = True)
        tz_lock = cmds.getAttr(masterName + '.tz', l = True)  
        rx_lock = cmds.getAttr(masterName + '.rx', l = True)
        ry_lock = cmds.getAttr(masterName + '.ry', l = True)
        rz_lock = cmds.getAttr(masterName + '.rz', l = True)  

        if tx_lock == True:
            lockList[0] = 1
        if ty_lock == True:
            lockList[1] = 1
        if tz_lock == True:
            lockList[2] = 1
            
        if rx_lock == False:
            lockList[3] = 0
        if ry_lock == False:
            lockList[4] = 0
        if rz_lock == False:
            lockList[5] = 0
    
    result = True
    for cnt in range (6):
        if lockList[cnt] == 1 and axisList[cnt] == 0:
            result = False
    return result

#-------------------------------------------------------------------------------------------
#   pointConstarint�AorientConstarint�̐e��parentConstraint�ɐڑ�����Ă����ۂ̃G���[���
#-------------------------------------------------------------------------------------------
def getMasterConstraintInfo(masterName):
    print(masterName)
    ConnectList=[]
    ParentConstraintList = []
    result = True
    ConnectList = cmds.listConnections(masterName,s=True)
    for cnt in range (len(ConnectList)):
        thisObjectType = cmds.objectType(ConnectList[cnt])
        if thisObjectType == "parentConstraint":
            ParentConstraintList.append(ConnectList[cnt])

    if len(ParentConstraintList)>0:
        result = False

    return result
        

    
    
