# -*- coding: cp932 -*-
#-------------------------------------------------------------------------------------------
#   OdinRefreezeJoint
#-------------------------------------------------------------------------------------------

import gc
import maya.cmds as cmds
import maya.mel as mel
import CyCommon
from CyCommon.CyUtility import CyUtility
from CyCommon.CySetting import CySetting

reload(CyCommon.CyUtility)
reload(CyCommon.CySetting)

toolName = "OdinRefreezeJoint"
scriptPrefix= toolName + "."
uiPrefix= toolName + "UI_"
g_setting = None
#**************************************************************************************************************************
#   UI�֘A
#**************************************************************************************************************************
#-------------------------------------------------------------------------------------------
#   ���C��UI
#-------------------------------------------------------------------------------------------
def UI():

    global scriptPrefix
    global toolName
    global g_setting
    global g_windowName
    
    if g_setting == None:
        g_setting = CySetting(toolName)
        
    width=300
    height=1
    formWidth=width-5
    leftRowColumnWidth = 100

    windowTitle=scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"

    checkDoubleWindow(windowName)

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=True,mnb=True,mxb=False,rtf=True)
    cmds.columnLayout( adjustableColumn=True )
    
    cmds.rowLayout(nc=2 ,cw2=[leftRowColumnWidth,width-leftRowColumnWidth],ct2=["right","both"],adj=2,rat=[1,"top",2])
    cmds.text("�t���[�Y�F")
    
    cmds.columnLayout( adjustableColumn=True )
    cmds.checkBox(uiPrefix + "freezeT",label="�ړ�" , cc=scriptPrefix+"SaveSetting()" )    
    cmds.checkBox(uiPrefix + "freezeR",label="��]" , cc=scriptPrefix+"SaveSetting()" )
    cmds.checkBox(uiPrefix + "freezeS",label="�X�P�[��" , cc=scriptPrefix+"SaveSetting()" )    
    cmds.checkBox(uiPrefix + "freezeJO",label="�W���C���g�̕���" , cc=scriptPrefix+"SaveSetting()" )
    cmds.setParent('..')    
    cmds.setParent('..')
    
    cmds.separator( style='in',h=15,w=formWidth)

    cmds.rowLayout(nc=2 ,cw2=[leftRowColumnWidth,width-leftRowColumnWidth],ct2=["right","both"],adj=2,rat=[1,"top",2])
    cmds.text("�@���̃��b�N�F")

    cmds.columnLayout( adjustableColumn=False )
    cmds.optionMenu(uiPrefix + "freezeN", w=200, cc=scriptPrefix+"SaveSetting()" )
    cmds.menuItem(label=u"��ɃI�t" )
    cmds.menuItem(label=u"�펞" )
    cmds.menuItem(label=u"�񃊃W�b�h �g�����X�t�H�[���̂�")
    cmds.checkBox(uiPrefix + "freezePN",label="�@���̕ێ�" , cc=scriptPrefix+"SaveSetting()" )   
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator( style='in',h=15,w=formWidth)
    
    cmds.button( label="RefreezeJoint",w=formWidth,command=scriptPrefix+"refreezeJointRoot()")

    loadCheckBox("FreezeT","freezeT")
    loadCheckBox("FreezeR","freezeR")
    loadCheckBox("FreezeS","freezeS")
    loadCheckBox("FreezeJO","freezeJO")
    loadOptionMenu()
    loadCheckBox("FreezePN","freezePN")

    cmds.showWindow(windowName)
    
#-------------------------------------------------------------------------------------------
#  checkDoubleWindow
#-------------------------------------------------------------------------------------------
def checkDoubleWindow(windowName):

    if cmds.window( windowName, exists=True ):
        cmds.deleteUI(windowName, window=True )
    else:
        if cmds.windowPref( windowName, exists=True ):
            cmds.windowPref( windowName, remove=True )
            
#-------------------------------------------------------------------------------------------
#  refreezeJointRoot
#-------------------------------------------------------------------------------------------
def refreezeJointRoot():
    
    selectedObj = cmds.ls(sl=True)
    
    confirmText = "�G���[���b�Z�[�W"
    errorMessage1 = "�P��̃O���[�v�����Ă��������B"
    
    if len(selectedObj) != 1:
        print "�����I�����Ă��܂�"
        error1 = cmds.confirmDialog(title=confirmText,message = errorMessage1)
        return
    if cmds.objectType(selectedObj) == "joint":
        print "�W���C���g��I�����Ă��܂�"
        error2 = cmds.confirmDialog(title=confirmText,message = errorMessage1)
        return    
    if cmds.objectType(selectedObj) != "transform":
        print "transform���Ȃ��I�u�W�F�N�g�ł�"
        error3 = cmds.confirmDialog(title=confirmText,message = errorMessage1)
        return

    selectedObjListRelatives = cmds.listRelatives(selectedObj)
    
    if cmds.listRelatives(selectedObj[0]) == None:
        error6 = cmds.confirmDialog(title=confirmText,message = "�O���[�v�̒�����ł�")
        print "��̃O���[�v�ł�"
        return

    reLativesOneType =  cmds.objectType(cmds.listRelatives(selectedObj[0])[0])
    
    if reLativesOneType== "locator":
        print "���P�[�^�[��I�����Ă��܂�"
        error4 = cmds.confirmDialog(title=confirmText,message = errorMessage1)
        return    
    if reLativesOneType== "mesh":
        print "���b�V����I�����Ă��܂�"
        error5 = cmds.confirmDialog(title=confirmText,message = errorMessage1)
        return    
    if reLativesOneType== "camera":
        print "�J������I�����Ă��܂�"
        error6 = cmds.confirmDialog(title=confirmText,message = errorMessage1)
        return
    
    refeezeJoint(selectedObj,selectedObjListRelatives)
    
#-------------------------------------------------------------------------------------------
#  refreezeJoint
#-------------------------------------------------------------------------------------------
def refeezeJoint(selectedObj,selectedObjListRelatives):
    global g_windowName
    
    cmds.duplicate()
    duplicatedObj = cmds.ls(sl=True)
    duplicatedObjListRelatives = cmds.listRelatives(duplicatedObj)

    originalObjList,originalMeshList,originalLocatorList,originalJointList = makeObjList(selectedObj,selectedObjListRelatives)
    duplicatedObjList,duplicatedMeshList,duplicatedLocatorList,duplicatedJointList = makeObjList(duplicatedObj,duplicatedObjListRelatives)

    ##�W���C���g�t���[�Y
    checkFreezeT = cmds.checkBox(uiPrefix + "freezeT" , q=True, v=True)
    checkFreezeR = cmds.checkBox(uiPrefix + "freezeR" , q=True, v=True)
    checkFreezeS = cmds.checkBox(uiPrefix + "freezeS" , q=True, v=True)
    checkFreezeJO = cmds.checkBox(uiPrefix + "freezeJO" , q=True, v=True)
    checkFreezeN = cmds.optionMenu(uiPrefix + "freezeN", q=True, v=True)
    checkFreezePN = cmds.checkBox(uiPrefix + "freezePN" , q=True, v=True)
    checkFreezeN2 = ""

    if checkFreezeN == u"��ɃI�t":
        checkFreezeN2 = 0
    elif checkFreezeN == u"�펞":
        checkFreezeN2 = 1
    elif checkFreezeN == u"�񃊃W�b�h �g�����X�t�H�[���̂�":
        checkFreezeN2 = 2
        
    cmds.select(duplicatedObj, hi=True)
    cmds.makeIdentity( duplicatedJointList[0], a=True, t=checkFreezeT, r=checkFreezeR , s=checkFreezeS, n=checkFreezeN2, pn=checkFreezePN, jo=checkFreezeJO )
    
    ##�X���[�Y�o�C���h
    cmds.select(duplicatedObj, hi=True)
    cmds.SmoothBindSkin()
    
    ##�E�F�C�g�R�s�[
    import CyWeightEditor 
    reload(CyWeightEditor)

    cmds.select(cl=True)
    for i in range(len(originalMeshList)):
        cmds.select(originalMeshList[i],add=True)

    CyWeightEditor.UI()
    CyWeightEditor.CopyWeight()
    
    CyWeightEditor.pasteWeightByIndex2 = pasteWeightByIndex2

    cmds.select(cl=True)
    for i in range(len(duplicatedMeshList)):
        cmds.select(duplicatedMeshList[i],add=True)

    print "1��ڂ̃y�[�X�g"
    CyWeightEditor.pasteWeightByIndex2(CyWeightEditor.g_weightManager)
    print "2��ڂ̃y�[�X�g"
    CyWeightEditor.pasteWeightByIndex2(CyWeightEditor.g_weightManager)

    windowTitle=CyWeightEditor.g_scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"
    closeWindow(windowName)
    
    cmds.delete(selectedObj)
    cmds.rename(duplicatedObj,selectedObj)
    
#-------------------------------------------------------------------------------------------
#   pasteWeightByIndex2
#-------------------------------------------------------------------------------------------
def pasteWeightByIndex2(self):
    
    self.CreateInfo()
    self.PasteWeightByIndex()
    
#-------------------------------------------------------------------------------------------
#  makeObjList
#-------------------------------------------------------------------------------------------
def makeObjList(selectedObj,selectedObjListRelatives):

    originalObjList = []
    for i in range(len(selectedObjListRelatives)):
        cmds.select( str(selectedObj[0]) + "|" + str(selectedObjListRelatives[i]) )
        thisObj = cmds.ls(sl=True)
        originalObjList.append(thisObj)
        
    originalMeshList = []
    originalLocatorList = []
    for i in range(len(originalObjList)):
        if cmds.objectType ( str(originalObjList[i][0]) + "|" + str(cmds.listRelatives(originalObjList[i])[0])) == "mesh":
            originalMeshList.append(originalObjList[i])  
        elif cmds.objectType ( str(originalObjList[i][0]) + "|" + str(cmds.listRelatives(originalObjList[i])[0])) == "locator":
            originalLocatorList.append(originalObjList[i])

    cmds.select(originalLocatorList[0],hi=True)
    originalJointList = cmds.ls(sl=True)

    originalJointList2 = []
    for i in range(len(originalJointList)):
        if cmds.objectType (originalJointList[i]) == "joint":
            originalJointList2.append(originalJointList[i])
            
    return (originalObjList,originalMeshList,originalLocatorList,originalJointList2)

#-------------------------------------------------------------------------------------------
#  closeWindow
#-------------------------------------------------------------------------------------------
def closeWindow(windowName):
    if cmds.window(windowName, exists=True ):
        cmds.deleteUI(windowName, window=True )
        
#-------------------------------------------------------------------------------------------
#   Save Setting
#-------------------------------------------------------------------------------------------
def SaveSetting():

    global uiPrefix
    global g_setting
    
    g_setting = CySetting(toolName)
    FreezeT =str(cmds.checkBox(uiPrefix + "freezeT" , q=True, v=True))
    FreezeR = str(cmds.checkBox(uiPrefix + "freezeR" , q=True, v=True))
    FreezeS = str(cmds.checkBox(uiPrefix + "freezeS" , q=True, v=True))
    FreezeJO = str(cmds.checkBox(uiPrefix + "freezeJO" , q=True, v=True))
    FreezeN = cmds.optionMenu(uiPrefix + "freezeN", q=True, v=True)
    FreezePN = str(cmds.checkBox(uiPrefix + "freezePN" , q=True, v=True))

    g_setting.Save("FreezeT", FreezeT)
    g_setting.Save("FreezeR", FreezeR)
    g_setting.Save("FreezeS", FreezeS)
    g_setting.Save("FreezeJO", FreezeJO)
    g_setting.Save("FreezeN", FreezeN)
    g_setting.Save("FreezePN", FreezePN)
    
#-------------------------------------------------------------------------------------------
#  loadCheckBox
#-------------------------------------------------------------------------------------------
def loadCheckBox(keyName,boxName):
    thisBool = g_setting.Load(keyName)
    if thisBool == "True":
        cmds.checkBox(uiPrefix + boxName,e=True, v=True)
    elif thisBool == "" or thisBool == "False":
        cmds.checkBox(uiPrefix + boxName,e=True, v=False)

#-------------------------------------------------------------------------------------------
#  loadOptionMenu
#-------------------------------------------------------------------------------------------
def loadOptionMenu():
    thisLabel = g_setting.Load("FreezeN")
    print thisLabel
    thisSelect = 1
    if thisLabel == u"��ɃI�t":
        thisSelect = 1
    elif thisLabel == u"�펞":
        thisSelect = 2
    elif thisLabel == u"�񃊃W�b�h �g�����X�t�H�[���̂�":
        thisSelect = 3
    print thisSelect
    cmds.optionMenu(uiPrefix + "freezeN",select = thisSelect, e = True)
    

        
