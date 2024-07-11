# -*- coding: cp932 -*-
#-------------------------------------------------------------------------------------------
#   Author: Daichi Ishikawa
#-------------------------------------------------------------------------------------------
try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass


import maya.cmds as cmds
import maya.mel as mel
import os


import TkgCommon.TkgSetting
from TkgCommon.TkgSetting import TkgSetting
reload(TkgCommon.TkgSetting)

toolName = "TkgFrameCutter"
scriptPrefix= toolName + "."
uiPrefix= toolName + "UI"

g_listcouny=40
g_rooplistcouny=6

g_setting = None

g_setManagerInfo = None

#**************************************************************************************************************************
#   UI�֘A
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   ���C��UI
#-------------------------------------------------------------------------------------------
def UI():

    global scriptPrefix
    global g_listcouny
    global g_rooplistcouny
    global g_setting
    global toolName
    global g_setManagerInfo
    
    if g_setManagerInfo == None:
        g_setManagerInfo = SetManagerInfo()
        
    if g_setting == None:
        g_setting = TkgSetting(toolName)
    
    width=800
    height=900
    formWidth=width-20
    
    windowTitle=scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"

    checkDoubleWindow(windowName)
    

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=True,mnb=True,mxb=False,rtf=True)

    #-------------------------
    cmds.columnLayout( adjustableColumn=True )
    cmds.textFieldGrp(uiPrefix + "ExportFolder", label="ExportFolder",
                      cl2=("left","left"), ad2=2, w=formWidth, cw2=[70, formWidth-70],
                      text = g_setting.Load('folderKey0_1'),
                      tcc = scriptPrefix+"SaveSetting(int(0),int(1),'exportFolderKey')")
    cmds.separator( style='in',h=15,w=formWidth)  
    #-------------------------
    cmds.scrollLayout(cr=True,w=formWidth,h=800)
    column1Width=30
    column2Width=30
    column3Width=80
    column4Width=300
    column5Width=30
    
    for cnt in range(g_rooplistcouny):
        cmds.columnLayout( adjustableColumn=True )

        
        cmds.frameLayout(uiPrefix + "frameLayout" + str(cnt),l="Set"+str(cnt+1),cll=1,cl=1,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.textFieldGrp(uiPrefix + "SetMemo"+str(cnt)+"_1",
                          label="Memo:",
                          adj=1,
                          text = g_setting.Load("setMemoKey" + str(cnt) +"_1"),
                          tcc = scriptPrefix+"SaveSetting("+str(cnt)+",1,'exportSetMemoKey')"
                          )
        cmds.rowLayout(nc=5 ,cw5=[column1Width+column2Width,column3Width,100,column4Width,column5Width],ct5=["both","both","both","both","both"],adj=5)
        cmds.text("CheckBox")
        cmds.text("Frame")
        cmds.text("Memo")
        cmds.text("Name")
        cmds.text("�ǉ�Tag")
        cmds.setParent('..')
        
        cmds.rowLayout(nc=5 ,cw5=[column1Width+column2Width,column3Width,100,column4Width,column5Width],ct5=["both","both","both","both","both"],adj=5)
        cmds.button( label="clear/on",command=scriptPrefix+"ClearCheckBox('CheckBoxFilter',"+str(cnt)+")")
        cmds.button( label="clear",command=scriptPrefix+"ClearTextField('ExportTime',"+str(cnt)+")")
        cmds.button( label="clear",command=scriptPrefix+"ClearTextField('Memo',"+str(cnt)+")")
        cmds.button( label="clear",command=scriptPrefix+"ClearTextField('ExportName',"+str(cnt)+")")
        cmds.button( label="clear",command=scriptPrefix+"ClearTextField('ExportFilter',"+str(cnt)+")")
        cmds.setParent('..')
        
        for cnt2 in range(g_listcouny):
            cmds.rowLayout(nc=6 ,cw6=[column1Width,column2Width,column3Width,100,column4Width,column5Width],ct6=["both","both","both","both","both","both"],adj=6)
            cmds.checkBox(uiPrefix + "CheckBoxFilter" + str(cnt) + "_" + str(cnt2),label=""
                          ,cc = scriptPrefix+"SaveSetting(" + str(cnt) + "," + str(cnt2) + ",'checkBoxFilterKey')"
                          )                        
            cmds.text(str(cnt2+1))
            cmds.textFieldGrp(uiPrefix + "ExportTime" + str(cnt) + "_" + str(cnt2),
                              adj=1,
                              text = g_setting.Load("timeKey" + str(cnt) + "_" + str(cnt2)),
                              tcc = scriptPrefix+"SaveSetting(" + str(cnt) + "," + str(cnt2) + ",'exportTimeKey')")
            
            cmds.textFieldGrp(uiPrefix + "Memo" + str(cnt) + "_" + str(cnt2),
                              adj=1,
                              text = g_setting.Load("memoKey" + str(cnt) + "_" + str(cnt2)),
                              tcc = scriptPrefix+"SaveSetting(" + str(cnt) + "," + str(cnt2) + ",'exportMemoKey')"
                              )
        
            cmds.textFieldGrp(uiPrefix + "ExportName" + str(cnt) + "_" + str(cnt2),
                              adj=1,
                              text = g_setting.Load("nameKey" + str(cnt) + "_" + str(cnt2)),
                              tcc = scriptPrefix+"SaveSetting(" +str(cnt) + "," + str(cnt2) + ",'exportNameKey')")
            
            cmds.textFieldGrp(uiPrefix + "ExportFilter" + str(cnt) + "_" + str(cnt2),
                              adj=1,
                              text = g_setting.Load("filterKey" + str(cnt) + "_" + str(cnt2)),
                              tcc = scriptPrefix+"SaveSetting(" + str(cnt) + "," + str(cnt2) + ",'exportFilterKey')")
        
            cmds.setParent('..')
            
        cmds.setParent('..')
        cmds.setParent('..')
        
    cmds.setParent('..')
    cmds.separator( style='in',h=15,w=formWidth)
    #-------------------------
    cmds.rowLayout(nc=4, cw4=[150,150,column1Width,150],ct4=["both","both","both","both"])
    cmds.text("Name������u��")
    cmds.textFieldGrp(uiPrefix + "ReplaceBeforeName", adj=1,
                      text = g_setting.Load("replaceBeforeNameKey0_1"),
                      tcc = scriptPrefix+"SaveSetting(int(0),int(1),'exportReplaceBeforeNameKey')"
                      )
    cmds.text("��")
    cmds.textFieldGrp(uiPrefix + "ReplaceName", adj=1,
                      text = g_setting.Load("replaceNameKey0_1"),
                      tcc = scriptPrefix+"SaveSetting(int(0),int(1),'exportReplaceNameKey')"
                      )
    cmds.setParent('..')
    cmds.separator( style='in',h=15,w=formWidth)
    #-------------------------
    cmds.rowLayout(nc=6, cw6=[150,150,column1Width,150,10,50],ct6=["both","both","both","both","both","both"])
    cmds.text("CopySettingSet")
    cmds.intField(uiPrefix + "masterSetNum", minValue=1, maxValue=6, value=1, step=1)
    cmds.text("��")
    cmds.intField(uiPrefix + "copySetNum", minValue=1, maxValue=6, value=1, step=1)
    cmds.text(" ")
    cmds.button( label="Copy",command=scriptPrefix+"CopySetRoot()")
    cmds.setParent('..')
    cmds.separator( style='in',h=15,w=formWidth)
    #-------------------------
    cmds.rowLayout(nc=4, cw4=[25,150,column1Width,150],ct4=["both","both","both","both"])
    cmds.text("")
    cmds.checkBox(uiPrefix + "DeleteNamespaceFilter",label="Delete Namespace"
                          ,cc = scriptPrefix+"SaveSetting(int(0),int(1),'deleteNamespaceKey')"
                          )                                  
    cmds.setParent('..')
    cmds.separator( style='in',h=15,w=formWidth)
    #-------------------------
    cmds.button( label="Export",w=formWidth,command=scriptPrefix+"ShowConfirmation()")
    #-------------------------

    for cnt in range(g_rooplistcouny):
        for cnt2 in range(g_listcouny):
            thisBool = g_setting.Load("checkBoxKey" + str(cnt) + "_" + str(cnt2))
            if thisBool == "" or thisBool == "True":
                cmds.checkBox(uiPrefix + "CheckBoxFilter" + str(cnt) + "_" + str(cnt2),e=True, v=True)
            elif thisBool == "False":
                cmds.checkBox(uiPrefix + "CheckBoxFilter" + str(cnt) + "_" + str(cnt2),e=True, v=False)
            
    deleteNamespaceBool = g_setting.Load("namespaceKey0_1")
    if  deleteNamespaceBool == "" or deleteNamespaceBool == "True":     
        cmds.checkBox(uiPrefix + "DeleteNamespaceFilter",e=True, v=True)
    elif deleteNamespaceBool == "False":
        cmds.checkBox(uiPrefix + "DeleteNamespaceFilter",e=True, v=False)
    
    cmds.frameLayout(uiPrefix + "frameLayout" + str(0),e=True,cl=0)

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
#   ���s�m�F�E�B���h�E
#-------------------------------------------------------------------------------------------
def ShowConfirmation():
    confirmText="���s�m�F"
    selectObject = cmds.ls(sl=True)
    
    if len(selectObject) == 0:
        cmds.confirmDialog( title=confirmText,
                            message="�����I������Ă��܂���",
                            button=['Cancel'],
                            cancelButton='Cancel',
                            dismissString='Cancel'
                            )
        return
        
    confirm=cmds.confirmDialog( title=confirmText,
                                message="�㏑���ۑ����Ă�����s����܂�",
                                button=['OK','Cancel'],
                                defaultButton='OK',
                                cancelButton='Cancel',
                                dismissString='Cancel'
                                )
    
    if confirm == "OK":
        ExportRoot()
    else:
        return
#-------------------------------------------------------------------------------------------
#  ClearTextField
#-------------------------------------------------------------------------------------------
def ClearTextField(exportType,setCnt):
    global g_listcouny
    for cnt in range(g_listcouny):
        cmds.textFieldGrp(uiPrefix + exportType + str(setCnt) + "_" + str(cnt), e=True, text="")

#-------------------------------------------------------------------------------------------
#  ClearCheckBox
#-------------------------------------------------------------------------------------------
def ClearCheckBox(exportType,setCnt):
    global g_listcouny
    global g_rooplistcouny
    
    trueCheckBoxList = []

    for cnt in range(g_listcouny):
        checkBoxFilter = cmds.checkBox(uiPrefix + exportType + str(setCnt) + "_" + str(cnt), q=True, v=True)
        if checkBoxFilter == True:
            trueCheckBoxList.append(uiPrefix + exportType + str(setCnt) + "_" + str(cnt))

    if len(trueCheckBoxList) > 0:
        for cnt in range(g_listcouny):
            cmds.checkBox(uiPrefix + exportType + str(setCnt) + "_" + str(cnt), e=True, v=False)
            SaveSetting(setCnt,cnt,'checkBoxFilterKey')

    else:
        for cnt in range(g_listcouny):
            cmds.checkBox(uiPrefix + exportType + str(setCnt) + "_" + str(cnt), e=True, v=True)
            SaveSetting(setCnt,cnt,'checkBoxFilterKey')
            
#-------------------------------------------------------------------------------------------
#   RewriteTextField
#-------------------------------------------------------------------------------------------    
def RewriteTextField(setNumber,rowNumber,typeName,thisText):
    cmds.textFieldGrp(uiPrefix + typeName + str(setNumber) + "_" + str(rowNumber),
                      text =thisText,
                      edit=True,)


#-------------------------------------------------------------------------------------------
#   CopySet���s�m�F�E�B���h�E
#-------------------------------------------------------------------------------------------
def CopySetRoot():
    confirmText="���s�m�F"
    Num1 = cmds.intField(uiPrefix + "masterSetNum", q=True, value=True)
    Num2 = cmds.intField(uiPrefix + "copySetNum", q=True, value=True)
        
    confirm=cmds.confirmDialog( title=confirmText,
                                message=" Set" + str(Num1) + " �� Set" + str(Num2) + " �ɃR�s�[���܂����H",
                                button=['OK','Cancel'],
                                defaultButton='OK',
                                cancelButton='Cancel',
                                dismissString='Cancel'
                                )
    
    if confirm == "OK":
        CopySet()
    else:
        return
#-------------------------------------------------------------------------------------------
#   CopySet
#-------------------------------------------------------------------------------------------    
def CopySet():
    global g_setting
    global g_listcouny
    global g_rooplistcouny

    TimeKeyList = []
    NameKeyList = []
    FilterKeyList = []
    MemoKeyList = []

    ClearTimeKeyList = []
    ClearNameKeyList = []
    ClearFilterKeyList = []
    ClearMemoKeyList = []
    
    masterSetNum = cmds.intField(uiPrefix + "masterSetNum", q=True, value=True)-1
    copySetNum = cmds.intField(uiPrefix + "copySetNum", q=True, value=True)-1


    for cnt in range (g_listcouny):
        clearTimeKey = g_setting.Load("timeKey" + str(copySetNum) + "_" + str(cnt))
        clearNameKey = g_setting.Load("nameKey" + str(copySetNum) + "_" + str(cnt))
        clearFilterKey = g_setting.Load("filterKey" + str(copySetNum) + "_" + str(cnt))
        clearMemoKey = g_setting.Load("memoKey" + str(copySetNum) + "_" + str(cnt))
        
        ClearTimeKeyList.append(clearTimeKey)
        ClearNameKeyList.append(clearNameKey)
        ClearFilterKeyList.append(clearFilterKey)
        ClearMemoKeyList.append(clearMemoKey)
        
        timeKey = g_setting.Load("timeKey" + str(masterSetNum) + "_" + str(cnt))
        nameKey = g_setting.Load("nameKey" + str(masterSetNum) + "_" + str(cnt))
        filterKey = g_setting.Load("filterKey" + str(masterSetNum) + "_" + str(cnt))
        memoKey = g_setting.Load("memoKey" + str(masterSetNum) + "_" + str(cnt))
        
        TimeKeyList.append(timeKey)
        NameKeyList.append(nameKey)
        FilterKeyList.append(filterKey)
        MemoKeyList.append(memoKey)

    for cnt in range (g_listcouny):
        if ClearTimeKeyList != "":
            RewriteTextField(copySetNum,cnt,"ExportTime","")
        if ClearNameKeyList != "":
            RewriteTextField(copySetNum,cnt,"ExportName","")
        if ClearFilterKeyList != "":
            RewriteTextField(copySetNum,cnt,"ExportFilter","")
        if ClearMemoKeyList != "":
            RewriteTextField(copySetNum,cnt,"Memo","")

        if TimeKeyList != "":
            RewriteTextField(copySetNum,cnt,"ExportTime",TimeKeyList[cnt])
        if NameKeyList != "":
            RewriteTextField(copySetNum,cnt,"ExportName",NameKeyList[cnt])
        if FilterKeyList != "":
            RewriteTextField(copySetNum,cnt,"ExportFilter",FilterKeyList[cnt])
        if MemoKeyList != "":
            RewriteTextField(copySetNum,cnt,"Memo",MemoKeyList[cnt])    


#**************************************************************************************************************************
#   �Z�[�u���[�h�֘A
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   SaveSetting
#-------------------------------------------------------------------------------------------
def SaveSetting(setNumber,rowNumber,typeName):
    global g_setting
    global uiPrefix
    global g_listcouny
    g_setting = TkgSetting(toolName)

    exportType = ""
    nameText = ""
    
    if typeName == "exportTimeKey":
        xmlKey = "timeKey"
        exportType = cmds.textFieldGrp(uiPrefix + "ExportTime" + str(setNumber) + "_" + str(rowNumber), q=True, text=True)
    elif typeName == "exportNameKey":
        xmlKey = "nameKey"
        exportType = cmds.textFieldGrp(uiPrefix + "ExportName" + str(setNumber) + "_" + str(rowNumber), q=True, text=True)        
    elif typeName == "exportFilterKey":
        xmlKey = "filterKey"
        exportType = cmds.textFieldGrp(uiPrefix + "ExportFilter" + str(setNumber) + "_" + str(rowNumber), q=True, text=True)
    elif typeName == "exportFolderKey":
        xmlKey = "folderKey"
        exportType = cmds.textFieldGrp(uiPrefix + "ExportFolder", q=True, text=True)
    elif typeName == "checkBoxFilterKey":
        xmlKey = "checkBoxKey"
        exportType = str(cmds.checkBox(uiPrefix + "CheckBoxFilter" + str(setNumber) + "_" + str(rowNumber), q=True, v=True))
    elif typeName == "exportReplaceNameKey":
        xmlKey = "replaceNameKey"
        exportType = cmds.textFieldGrp(uiPrefix + "ReplaceName", q=True, text=True)
    elif typeName == "exportReplaceBeforeNameKey":
        xmlKey = "replaceBeforeNameKey"
        exportType = str(cmds.textFieldGrp(uiPrefix + "ReplaceBeforeName", q=True, text=True))
    elif typeName == "deleteNamespaceKey":
        xmlKey = "namespaceKey"
        exportType = str(cmds.checkBox(uiPrefix + "DeleteNamespaceFilter", q=True, v=True))
    elif typeName == "exportMemoKey":
        xmlKey = "memoKey"
        exportType = cmds.textFieldGrp(uiPrefix + "Memo" + str(setNumber) + "_" + str(rowNumber), q=True, text=True)
    elif typeName == "exportSetMemoKey":
        xmlKey = "setMemoKey"
        exportType = cmds.textFieldGrp(uiPrefix+ "SetMemo" + str(setNumber) + "_" + str(rowNumber), q=True, text=True)
    else:
        print("error")

    g_setting.Save(xmlKey+ str(setNumber) + "_" + str(rowNumber),exportType)

#**************************************************************************************************************************
#   �v���O���X�o�[�֘A
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   �v���O���X�o�[�J�n
#-------------------------------------------------------------------------------------------
def StartProgress(titleName):

    cmds.progressWindow(title=titleName,status="",isInterruptable=True, min=0, max=100 )

#-------------------------------------------------------------------------------------------
#   �v���O���X�o�[�X�V
#-------------------------------------------------------------------------------------------
def UpdateProgress(amount,info):

    cmds.progressWindow( edit=True, progress=amount, status=info )

    if cmds.progressWindow( query=True, isCancelled=True ) == True:
        return False

    return True

#-------------------------------------------------------------------------------------------
#   �v���O���X�o�[�I��
#-------------------------------------------------------------------------------------------
def EndProgress():

    cmds.progressWindow(endProgress=1)

#-------------------------------------------------------------------------------------------
#   �����o�����擾
#-------------------------------------------------------------------------------------------
def getFbxLen(exportNumber,transformList):
    exportFlag = False
    exportName1 = cmds.textFieldGrp(uiPrefix + "ExportName" + str(exportNumber), q=True, text=True)
    exportName2 = cmds.textFieldGrp(uiPrefix + "ReplaceName", q=True, text=True)
    exportName3 = cmds.textFieldGrp(uiPrefix + "ReplaceBeforeName", q=True, text=True)
    exportFilter = cmds.textFieldGrp(uiPrefix + "ExportFilter" + str(exportNumber), q=True, text=True)
    checkBoxFilter = cmds.checkBox(uiPrefix + "CheckBoxFilter" + str(exportNumber), q=True, v=True)


    thisExportTime = cmds.textFieldGrp(uiPrefix + "ExportTime" + str(exportNumber), q=True, text=True)    
    if "-" in thisExportTime:
        thisExportTimeList = thisExportTime.split("-")

        firstExportTime = int(thisExportTimeList[0])
        secondExportTime = int(thisExportTimeList[1])
    elif thisExportTime == "":
        return
    else:
        firstExportTime = int(thisExportTime)
        secondExportTime = int(thisExportTime)

    if exportName3=="":
        exportName = exportName1
    else:
        exportName = exportName1.replace(exportName3,exportName2)


    if exportName == "" or checkBoxFilter == False:
        return
    exportFlag = True

    return exportFlag

#**************************************************************************************************************************
#   ���[�e�B���e�B�֘A
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#  ���t�@�����X�ǂݍ���
#-------------------------------------------------------------------------------------------
def ImportRefFile():
    refFiles = cmds.file(q=1,r=1)
    if refFiles:
        for r in refFiles:
            refName = cmds.file(r,q=1,rfn=1)
            cmds.file(r,ir=1)


#**************************************************************************************************************************
#   �N���X�Q
#**************************************************************************************************************************
#-------------------------------------------------------------------------------------------
#   SetManagerInfo
#-------------------------------------------------------------------------------------------
class SetManagerInfo:
    
    #===========================================
    # __init__
    #===========================================
    def __init__(self):
        self.setCount = g_rooplistcouny
        self.allSetList = []
        self.exportTargetList = []
        
        self.transformAttrList = [] #�L�[�ł��l�A�t���[���̃��X�g
        self.setKeyframeTargetList = []  #�L�[�łΏۂ̃��X�g

        self.startFrame = 0
        self.endFrame = 0
        self.timeRange = 0 #�Đ��͈�
        self.exportFolder = ""

        self.tempFile = ""

        self.progressCnt = 0
    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):
        self.MakeList()
        self.allSetList = []
        
        for cnt in range(self.setCount):
            thisSetInfo = SetInfo(cnt)
            self.allSetList.append(thisSetInfo)
            
        self.startFrame = int(cmds.playbackOptions( q=True,minTime=True ))
        self.endFrame = int(cmds.playbackOptions( q=True,maxTime=True ))
        self.timeRange =(self.endFrame - self.startFrame + 1)
        
        for cnt in range(len(self.allSetList)):
            thisSet =  self.allSetList[cnt]
            thisSet.CreateInfo()

    #===========================================
    # ���X�g�쐬
    #===========================================
    def MakeList(self):
        cmds.select(hierarchy=True)  
        selectList = cmds.ls(sl=True)

        if len(selectList) == 0:
            return
        jointList = []
        childList = []
        locatorList = []
        meshList = []
        noSkinClusterMeshList = []
        transformList = []
        constraintList = []
        targetList = []

        for cnt in range(0,len(selectList)):
            if cmds.objectType(selectList[cnt]) == 'orientConstraint' or cmds.objectType(selectList[cnt]) == 'pointConstraint':
                constraintList.append(selectList[cnt])
            else:
                targetList.append(selectList[cnt])

                
        for cnt in range(0,len(selectList)):
            if cmds.objectType(selectList[cnt]) == 'joint':
                jointList.append(selectList[cnt])
            elif cmds.listRelatives(selectList[cnt],c=True) != None:
                childList.append(selectList[cnt])

        for cnt in range(0,len(childList)):
            thisObject = childList[cnt]
            thisNodeList = cmds.listRelatives(thisObject,c=True,f=True)
            
            if cmds.objectType(thisNodeList[0]) == 'locator':
                locatorList.append(thisObject)
            elif cmds.objectType(thisNodeList[0]) == 'mesh':
                meshList.append(thisObject)

        for cnt in range (0,len(meshList)):
            relatedSkinCluster = mel.eval('findRelatedSkinCluster '+meshList[cnt])
            if relatedSkinCluster == "":
                noSkinClusterMeshList.append(meshList[cnt])
        
        transformList.extend(jointList)
        transformList.extend(locatorList)
        transformList.extend(noSkinClusterMeshList)
        self.setKeyframeTargetList = transformList
        self.exportTargetList = targetList
                    
    #===========================================
    # GetAttrSetting
    #===========================================
    def GetAttrSetting(self):
        self.transformAttrList = [[[None for col in range(9)] for row in range(len(self.setKeyframeTargetList))] for row in range(self.timeRange)]

        for frameCount in range(self.timeRange):  

            for targetCount in range(len(self.setKeyframeTargetList)):
                thisSetKeyTarget = self.setKeyframeTargetList[targetCount]

                self.transformAttrList[frameCount][targetCount][0] = cmds.getAttr(thisSetKeyTarget + '.translateX', t=self.startFrame + frameCount)
                self.transformAttrList[frameCount][targetCount][1] = cmds.getAttr(thisSetKeyTarget + '.translateY', t=self.startFrame + frameCount)
                self.transformAttrList[frameCount][targetCount][2] = cmds.getAttr(thisSetKeyTarget + '.translateZ', t=self.startFrame + frameCount)
                
                self.transformAttrList[frameCount][targetCount][3] = cmds.getAttr(thisSetKeyTarget + '.rotateX', t=self.startFrame + frameCount)
                self.transformAttrList[frameCount][targetCount][4] = cmds.getAttr(thisSetKeyTarget + '.rotateY', t=self.startFrame + frameCount)
                self.transformAttrList[frameCount][targetCount][5] = cmds.getAttr(thisSetKeyTarget + '.rotateZ', t=self.startFrame + frameCount)
                
                self.transformAttrList[frameCount][targetCount][6] = cmds.getAttr(thisSetKeyTarget + '.scaleX', t=self.startFrame + frameCount)
                self.transformAttrList[frameCount][targetCount][7] = cmds.getAttr(thisSetKeyTarget + '.scaleY', t=self.startFrame + frameCount)
                self.transformAttrList[frameCount][targetCount][8] = cmds.getAttr(thisSetKeyTarget + '.scaleZ', t=self.startFrame + frameCount)

    #===========================================
    # ExportFBX
    #===========================================
    def ExportFBX(self):
        StartProgress("FBX�����o����")
        for cnt in range(len(self.allSetList)):
            thisSet =  self.allSetList[cnt]
            thisSet.ExportFBX(self.setKeyframeTargetList,self.transformAttrList,self.exportTargetList,self.tempFile)
            if thisSet.escExport == True:
                break
        EndProgress()

#-------------------------------------------------------------------------------------------
#   Set�̃N���X
#-------------------------------------------------------------------------------------------
class SetInfo:
    
    #===========================================
    # __init__
    #===========================================
    def __init__(self, setNumber=0):
        self.setNum = setNumber       
        self.thisSetList = []
        self.rowCount = g_listcouny
        self.escExport = False

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):
        for cnt in range(self.rowCount):
            thisFbxInfo = SingleFbxInfo(self.setNum,cnt)
            self.thisSetList.append(thisFbxInfo)
        
        for cnt in range(len(self.thisSetList)):
            thisFbx = self.thisSetList[cnt]
            thisFbx.CreateInfo()
            
    #===========================================
    # ExportFBX
    #===========================================
    def ExportFBX(self,setKeyframeTargetList = [],transformAttrList = [],exportTargetList = [], tempFile = ""):
        if len(setKeyframeTargetList) == 0:
            return
        
        StartProgress("FBX�����o����")
        for cnt in range(len(self.thisSetList)):
            if UpdateProgress(0,"Paste...") == False:
                EndProgress()
                self.escExport = True
                break
            thisFbx =  self.thisSetList[cnt]
            thisFbx.SetKeyframe(setKeyframeTargetList,transformAttrList,exportTargetList,tempFile)

#-------------------------------------------------------------------------------------------
#   �ŏ��P�ʂ̃N���X
#-------------------------------------------------------------------------------------------
class SingleFbxInfo:
    
    #===========================================
    # __init__
    #===========================================
    def __init__(self, setNumber=0, rowNumber=0, exportFolder = ""):
        self.setNum = setNumber
        self.rowNum = rowNumber

        self.exportName = cmds.textFieldGrp(uiPrefix + "ExportName" + str(setNumber) + "_" + str(rowNumber), q=True, text=True)
        self.exportFilter = cmds.textFieldGrp(uiPrefix + "ExportFilter" + str(setNumber) + "_" + str(rowNumber), q=True, text=True)
        self.checkBoxFilter = cmds.checkBox(uiPrefix + "CheckBoxFilter" + str(setNumber) + "_" + str(rowNumber), q=True, v=True)
               
        self.firstExportTime = 0 #�����t���[�������o���̎��ɕK�v
        self.lastExportTime = 0 #�����t���[�������o���̎��ɕK�v
        
        self.exportFolder = cmds.textFieldGrp(uiPrefix + "ExportFolder", q=True, text=True)
        self.exportFullPath = ""
        
    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):

        thisExportTime = cmds.textFieldGrp(uiPrefix + "ExportTime" + str(self.setNum) + "_" + str(self.rowNum), q=True, text=True)

        if "-" in thisExportTime:
            thisExportTimeList = thisExportTime.split("-")

            self.firstExportTime = int(thisExportTimeList[0])
            self.lastExportTime = int(thisExportTimeList[1])
            
        elif thisExportTime == "":
            return
        
        else:
            self.firstExportTime = int(thisExportTime)
            self.lastExportTime = int(thisExportTime)

        exportName1 = self.exportName
        exportName2 = cmds.textFieldGrp(uiPrefix + "ReplaceName", q=True, text=True)
        exportName3 = cmds.textFieldGrp(uiPrefix + "ReplaceBeforeName", q=True, text=True)

        if exportName3=="":
            self.exportName = exportName1
        else:
            self.exportName = exportName1.replace(exportName3,exportName2)

        self.exportFullPath = self.exportFolder+ "/" + self.exportName

    #===========================================
    # SetKeyframe
    #===========================================
    def SetKeyframe(self, setKeyframeTargetList,transformAttrList,exportTargetList,tempFile = ""):
        
        if len(setKeyframeTargetList) == 0:
            return
        
        #�G���[���
        if self.exportName == "" or self.checkBoxFilter == False:
            return
                
        firstExportTime = self.firstExportTime
        lastExportTime = self.lastExportTime
        exportFilterList = self.exportFilter.split(",")
        

        for targetCount in range(0,len(setKeyframeTargetList)):
            
            thisSetKeyTarget = setKeyframeTargetList[targetCount]

            for filterCount in range(len(exportFilterList)):
                if exportFilterList[filterCount] in thisSetKeyTarget:
                    for frameCount in range(firstExportTime,lastExportTime+1):
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][0], at='translateX', t=frameCount-firstExportTime )
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][1], at='translateY', t=frameCount-firstExportTime )
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][2], at='translateZ', t=frameCount-firstExportTime )
                        
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][3], at='rotateX', t=frameCount-firstExportTime )
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][4], at='rotateY', t=frameCount-firstExportTime )
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][5], at='rotateZ', t=frameCount-firstExportTime )
                        
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][6], at='scaleX', t=frameCount-firstExportTime )
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][7], at='scaleY', t=frameCount-firstExportTime )
                        cmds.setKeyframe( thisSetKeyTarget, v=transformAttrList[frameCount][targetCount][8], at='scaleZ', t=frameCount-firstExportTime )
                else:
                    pass
                    
        #�G�N�X�|�[�g������̂�I��
        cmds.select(exportTargetList)

        #�I�C���[�t�B���^�[����
        cmds.filterCurve(exportTargetList)

        #Delete Namespace
        deleteNamespaceFilter = cmds.checkBox(uiPrefix + "DeleteNamespaceFilter", q=True, v=True)
        
        if deleteNamespaceFilter != False: 
            import TkgDeleteNamespace
            reload(TkgDeleteNamespace)
            TkgDeleteNamespace.Execute()
            
        #�����o����tempFile�ǂݒ���
        cmds.file(self.exportFullPath + ".fbx", force=True,options="v=0;", type="FBX export", pr=True, es=True)
        cmds.file(new=True,force=True)
        cmds.file(tempFile, force=True, open=True)
        
#-------------------------------------------------------------------------------------------
#  ExportRoot
#-------------------------------------------------------------------------------------------
def ExportRoot():
    
    global g_setManagerInfo
    
    #===========================================
    # ���݂̃t�@�C�����㏑���ۑ�
    #===========================================
    currentFile=cmds.file(q=True, sn=True )
    cmds.file(save=True, force=True)
    cmds.file(rename=currentFile + 'temp')
       
    #===========================================
    # exportFoler�𒊏o
    #�ۑ��ׂ͂̃^�C�~���O�������Ǝv��
    #===========================================   
    g_setManagerInfo.exportFolder = cmds.textFieldGrp(uiPrefix + "ExportFolder", q=True, text=True)
    
    if g_setManagerInfo.exportFolder == "":
        return
    if cmds.file(g_setManagerInfo.exportFolder, exists=True,q=True,)== False:
        cmds.sysFile(g_setManagerInfo.exportFolder, makeDir=True )

    #===========================================
    # ���X�g�쐬
    #===========================================
    g_setManagerInfo.CreateInfo()

    if len(g_setManagerInfo.setKeyframeTargetList) == 0:
        return
    g_setManagerInfo.GetAttrSetting()
    
    #===========================================
    # �����L�[�t���[���폜
    #===========================================
    cmds.cutKey ()

    #===========================================
    # �����o���G���[�Ώ��i�R���X�g���C���폜�j
    #������������K�v
    #===========================================
    deleteList = []
    cmds.select(all = True, hi = True)
    allDagList = cmds.ls(sl=True) 
    for cnt in range(0,len(allDagList)):
        if cmds.objectType(allDagList[cnt]) == 'orientConstraint' or cmds.objectType(allDagList[cnt]) == 'pointConstraint':
            deleteList.append(allDagList[cnt])
    if len(deleteList) > 0:
        cmds.delete(deleteList)

    #�C���|�[�g���t�@�����X
    ImportRefFile()

    #===========================================
    # �ꎞ�t�@�C���ۑ�
    #===========================================
    tempFile=cmds.file(save=True, type='mayaBinary', force=True)
    g_setManagerInfo.tempFile = tempFile

    g_setManagerInfo.ExportFBX()


    #���t�@�C���\��       
    cmds.file(new=True,force=True)
    cmds.file(currentFile, force=True, open=True)

    #�ꎞ�t�@�C���폜
    os.remove(tempFile)

    

