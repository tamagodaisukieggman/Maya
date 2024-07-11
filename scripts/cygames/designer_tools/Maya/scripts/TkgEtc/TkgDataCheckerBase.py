# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   TkgDataCheckerBase
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel

import os
import math

import TkgCommon.TkgUtility
import TkgCommon.TkgVector
import TkgCommon.TkgSetting

from TkgCommon.TkgUtility import TkgUtility
from TkgCommon.TkgVector import TkgVector
from TkgCommon.TkgSetting import TkgSetting

reload(TkgCommon.TkgUtility)
reload(TkgCommon.TkgVector)
reload(TkgCommon.TkgSetting)

g_version = "0.1.0"
g_toolName = "TkgDataCheckerBase"
g_scriptPrefix= g_toolName + "."
g_uiPrefix= g_toolName + "UI_"

g_defaultSetting = None

g_main = None
g_checkerProcessor = None

#-------------------------------------------------------------------------------------------
#   CheckerProcessor
#-------------------------------------------------------------------------------------------
class CheckerProcessor():

    def __init__(self):

        self.logList = []

    def OnPostprocess(self):

        print ""


#-------------------------------------------------------------------------------------------
#   Initialize
#-------------------------------------------------------------------------------------------
def Initialize(scriptFilePath):

    global g_defaultSetting
    global g_toolName

    scriptPath = os.path.abspath(scriptFilePath)
    scriptDirPath = os.path.dirname(scriptPath)
    scriptName = os.path.basename(scriptPath)
    g_toolName = os.path.splitext(scriptName)[0]

    if g_defaultSetting == None:
        g_defaultSetting = TkgSetting(g_toolName,scriptDirPath)

#-------------------------------------------------------------------------------------------
#   UI
#-------------------------------------------------------------------------------------------
def UI():

    global g_main
    global g_defaultSetting

    if g_main == None:
        g_main = CheckManager("DIRECT")

    g_main.defaultSetting = g_defaultSetting
    g_main.Create()

#-------------------------------------------------------------------------------------------
#   UI
#-------------------------------------------------------------------------------------------
def BatchCheck(targetFolderPath, filterString, logFilePath):

    global g_main
    global g_defaultSetting
    global g_checkerProcessor

    if g_main == None:        
        g_main = CheckManager(targetFolderPath)

    g_main.filterString = filterString
    g_main.logFilePath = logFilePath        
    g_main.defaultSetting = g_defaultSetting

    g_main.Create()
    g_main.Check()
    g_main.Log()
    
#-------------------------------------------------------------------------------------------
#   ExecuteDirectCheck
#-------------------------------------------------------------------------------------------
def ExecuteDirectCheck():

    global g_main

    g_main.Check()
    g_main.Log()

#-------------------------------------------------------------------------------------------
#   ExecuteCheckButton
#-------------------------------------------------------------------------------------------
def ExecuteCheckButton(buttonName):

    global g_main

    g_main.ExecuteCheckButton(buttonName)

#-------------------------------------------------------------------------------------------
#   ToggleCheck
#-------------------------------------------------------------------------------------------
def ToggleCheck(buttonName):

    global g_main

    g_main.ToggleCheck(buttonName)

#-------------------------------------------------------------------------------------------
#   ChangeLabelValue
#-------------------------------------------------------------------------------------------
def ChangeLabelValue(buttonName):

    global g_main

    g_main.ChangeLabelValue(buttonName)

#-------------------------------------------------------------------------------------------
#   GetShortName
#-------------------------------------------------------------------------------------------
def GetShortName(name):

    if name.find("|") == -1:
        return name

    splitStr = name.split("|")

    return splitStr[len(splitStr) - 1]

#-------------------------------------------------------------------------------------------
#   TupleToList
#-------------------------------------------------------------------------------------------
def TupleToList(valueList):

    result = []

    for p in range(0,len(valueList)):
        result.append(valueList[p])

    return result

#-------------------------------------------------------------------------------------------
#   RoundValue
#-------------------------------------------------------------------------------------------
def RoundValue(value0):

    accuracy = 100000.0

    value0 *= accuracy
    value0 = round(value0)

    return value0 / accuracy

#-------------------------------------------------------------------------------------------
#   SameValue
#-------------------------------------------------------------------------------------------
def SameValue(value0,value1):

    accuracy = 100000

    value0 *= accuracy
    value0 = round(value0)

    value1 *= accuracy
    value1 = round(value1)

    if value0 == value1:
        return True

    return False

#-------------------------------------------------------------------------------------------
#   SameVector
#-------------------------------------------------------------------------------------------
def SameVector(valueList0, valueList1):

    if len(valueList0) != len(valueList1):
        return False

    for p in range(len(valueList0)):

        if SameValue(valueList0[p], valueList1[p]) == False:
            return False

    return True

#-------------------------------------------------------------------------------------------
#   WriteLogA
#-------------------------------------------------------------------------------------------
def WriteLogA(nodeType, name, info):

    shortName = GetShortName(name)

    return "\t" + GetUnicode(nodeType) + "\t\t" + GetUnicode(shortName) + "\t\t\t\t\t\t" + GetUnicode(info)

#-------------------------------------------------------------------------------------------
#   GetUnicode
#-------------------------------------------------------------------------------------------
def GetUnicode(target):

    thisType = type(target)

    if thisType == unicode:

        return target

    return unicode(target,"utf-8")

#-------------------------------------------------------------------------------------------
#   GetNameForSkinCluster
#-------------------------------------------------------------------------------------------
def GetNameForSkinCluster(meshName):
     
        result=meshName
     
        split=meshName.split("|")
     
        if meshName[0]=="|" and len(split)>2:
            result=meshName.replace("|","",1)
     
        return result

#-------------------------------------------------------------------------------------------
#   GetVertexIndex
#-------------------------------------------------------------------------------------------
def GetVertexIndex(vertexName):

    if vertexName.find("[") == -1:
        return

    if vertexName.find("]") == -1:
        return

    startIndex = vertexName.find("[") + 1
    endIndex = vertexName.find("]")

    return int(vertexName[startIndex:endIndex])

#-------------------------------------------------------------------------------------------
#   GetAllRootTransform
#-------------------------------------------------------------------------------------------
def GetAllRootTransform(selected):

    resultList = []

    allTransform = cmds.ls(sl=selected,l=True,fl=True,typ="transform")

    if allTransform == None:
        return resultList

    if len(allTransform) == 0:
        return resultList

    for trans in allTransform:

        if trans.find("|") == -1:
            continue

        if trans.find("|",1) != -1:
            continue

        resultList.append(trans)

    return resultList

#-------------------------------------------------------------------------------------------
#   GetAllMeshTransform
#-------------------------------------------------------------------------------------------
def GetAllMeshTransform(selected):

    resultList = []

    allTransform = cmds.ls(sl=selected,l=True,fl=True,typ="transform")

    if allTransform == None:
        return resultList

    if len(allTransform) == 0:
        return resultList

    cmds.select(allTransform,r=True,hi=True)

    allTransform = cmds.ls(sl=selected,l=True,fl=True,typ="transform")

    if allTransform == None:
        return resultList

    if len(allTransform) == 0:
        return resultList

    for trans in allTransform:

        thisShapes = cmds.listRelatives(trans, shapes = True, f=True)

        if thisShapes == None:
            continue

        if len(thisShapes) == 0:
            continue

        existShape = False
        for shape in thisShapes:

            thisType = cmds.objectType(shape)

            if thisType == "mesh":
                existShape = True
                break

        if existShape == False:
            continue

        resultList.append(trans)

    return resultList

#-------------------------------------------------------------------------------------------
#   CheckManager
#-------------------------------------------------------------------------------------------
class CheckManager:

    #===========================================
    # コンストラクタ
    #===========================================
    def __init__(self,rootPath=""):

        self.toolName = "TkgDataCheckerBase"
        self.scriptPrefix = self.toolName + "."
        self.uiPrefix = self.toolName + "UI_"

        self.defaultSetting = None

        self.replaceFileName = "____FileName"
        self.replaceFlag = ".replace"

        self.isDirect = False

        if rootPath == "DIRECT":
            self.isDirect = True

        self.rootPath = rootPath

        self.filterString = ""
        self.filterList = []

        self.logFilePath = ""

        self.resultDict = {}
        
        self.dataList = []

        self.logList = []

        self.uiExistModelFile = "ExistMayaFile"
        self.uiExistTextureFile = "ExistTextureFile"

        self.uiExistGroup = "ExistGroup"
        self.uiExistMesh = "ExistMesh"
        self.uiExistLocator = "ExistLocator"
        self.uiExistJoint = "ExistJoint"
        self.uiExistMaterial = "ExistMaterial"

        self.uiPosGroup = "PositionGroup"
        self.uiPosMesh = "PositionMesh"
        self.uiPosLocator = "PositionLocator"
        self.uiPosJoint = "PositionJoint"

        self.uiModelUVNum = "ModelUVNum"
        self.uiModelUVName = "ModelUVName"
        self.uiModelUVRange = "ModelUVRange"

        self.uiVCColorSetNum = "VtxColorColorSetNum"
        self.uiVCColorSetName = "VtxColorColorSetName"
        self.uiVCUnshared = "VtxColorUnshared"

        self.uiWeightRound = "WeightRound"
        self.uiWeightInfluence = "WeightInfluence"
        self.uiWeightJointFreeze = "WeightJointFreeze"

        self.uiClean4Side = "Clean4Side"
        self.uiCleanConcave = "CleanConcave"
        self.uiCleanHole = "CleanHole"
        self.uiCleanLamina = "CleanLamina"
        self.uiCleanNonmanifold = "CleanNonmanifold"
        self.uiCleanZeroEdge = "CleanZeroEdge"

        self.settingDataList = []

    #===========================================
    # GetFirstShapeType
    #===========================================
    def GetObjectInList(self, target, rootList):

        if cmds.objExists(target) == False:
            return

        targetName = GetShortName(target)

        for root in rootList:

            cmds.select(root, r=True, hi=True)

            thisChildList = cmds.ls(sl=True,l=True,fl=True)

            if thisChildList == None:
                continue

            if len(thisChildList) == 0:
                continue

            for child in thisChildList:

                childName = GetShortName(child)

                if childName == targetName:
                    
                    return child
        return

    #===========================================
    # GetFirstShapeType
    #===========================================
    def GetFirstShapeType(self, target):

        if cmds.objExists(target) == False:
            return

        thisShapeList = cmds.listRelatives(target,s=True,f=True)

        if thisShapeList == None:
            return cmds.objectType(target)

        if len(thisShapeList) == 0:
            return cmds.objectType(target)

        return cmds.objectType(thisShapeList[0])

    #===========================================
    # GetReplaceName
    #===========================================
    def GetReplaceName(self, target):

        currentFilePath = cmds.file(q=True, sn=True)
        thisFileName = os.path.basename(currentFilePath)
        thisFileNameNoExt = thisFileName.split(".")[0]

        target = target.replace(self.replaceFileName, thisFileNameNoExt)

        target = self.ReplaceNameFromFlag(target, 0)
        target = self.ReplaceNameFromFlag(target, 1)
        target = self.ReplaceNameFromFlag(target, 2)
        target = self.ReplaceNameFromFlag(target, 3)
        target = self.ReplaceNameFromFlag(target, 4)

        return target

    #===========================================
    # ReplaceNameFromFlag
    #===========================================
    def ReplaceNameFromFlag(self, target, index):

        thisFlag = self.replaceFlag + str(index)

        if target.find(thisFlag) == -1:
            return target

        repStartIndex = target.index(thisFlag)

        startIndex = repStartIndex + len(thisFlag) + 1
        endIndex = target.index(")", startIndex)

        thisAllStr = target[repStartIndex:endIndex + 1]
        thisValueListStr = target[startIndex:endIndex]
        thisValueList = thisValueListStr.split(".")

        target = target.replace(thisAllStr,"")

        if len(thisValueList) != 2:
            return target
        
        target = target.replace(thisValueList[0],thisValueList[1])

        return target

    #===========================================
    # CreateData
    #===========================================
    def CreateSettingDataList(self):

        self.settingDataList = []

        self.CreateSettingData(self.uiExistModelFile, u"モデル", u"リスト", "")
        self.CreateSettingData(self.uiExistTextureFile, u"テクスチャ", u"リスト", "")

        self.CreateSettingData(self.uiExistGroup, u"グループ", u"リスト", "")
        self.CreateSettingData(self.uiExistMesh, u"メッシュ", u"リスト", "")
        self.CreateSettingData(self.uiExistLocator, u"ロケータ", u"リスト", "")
        self.CreateSettingData(self.uiExistJoint, u"ジョイント", u"リスト", "")
        self.CreateSettingData(self.uiExistMaterial, u"マテリアル", u"リスト", "")

        self.CreateSettingData(self.uiPosGroup, u"グループ", u"リスト", "")
        self.CreateSettingData(self.uiPosMesh, u"メッシュ", u"リスト", "")
        self.CreateSettingData(self.uiPosLocator, u"ロケータ", u"リスト", "")
        self.CreateSettingData(self.uiPosJoint, u"ジョイント", u"リスト", "")

        self.CreateSettingData(self.uiModelUVNum, u"UV数", u"数", "")
        self.CreateSettingData(self.uiModelUVName, u"UV名", u"リスト", "")
        self.CreateSettingData(self.uiModelUVRange, u"UV範囲", u"範囲", "")

        self.CreateSettingData(self.uiVCColorSetNum, u"カラーセット数", u"数", "")
        self.CreateSettingData(self.uiVCColorSetName, u"カラーセット名", u"リスト", "")
        self.CreateSettingData(self.uiVCUnshared, u"Unshared頂点カラー", u"", "")

        self.CreateSettingData(self.uiWeightInfluence, u"インフルエンス数", u"精度", "")
        self.CreateSettingData(self.uiWeightRound, u"ウェイト精度", u"桁数", "")
        self.CreateSettingData(self.uiWeightJointFreeze, u"ジョイントオリエント", u"", "")

        self.CreateSettingData(self.uiClean4Side, u"5辺以上のフェース", u"", "")
        self.CreateSettingData(self.uiCleanConcave, u"凹型フェース", u"", "")
        self.CreateSettingData(self.uiCleanHole, u"穴のあるフェース", u"", "")
        self.CreateSettingData(self.uiCleanLamina, u"ラミナフェース", u"", "")
        self.CreateSettingData(self.uiCleanNonmanifold, u"非多様体ジオメトリ", u"", "")
        self.CreateSettingData(self.uiCleanZeroEdge, u"長さが0のエッジ", u"", "")

    #===========================================
    # CreateData
    #===========================================
    def CreateSettingData(self, name, title, label, labelValue):

        newData = SettingData(self, name)

        newData.title = title

        newData.label = label
        newData.labelValue = labelValue

        self.settingDataList.append(newData)

    #===========================================
    # セッティングデータ取得
    #===========================================
    def GetSettingData(self,name):

        for data in self.settingDataList:

            if data.name == name:
                return data

        return None

    #===========================================
    # 設定データからUI作成
    #===========================================
    def CreateUIFromData(self, name, labelValue):

        data = self.GetSettingData(name)

        if data == None:
            return

        data.CreateUI()

    #===========================================
    # ラベル値の更新
    #===========================================
    def SetLabelValue(self, name, labelValue):

        data = self.GetSettingData(name)

        if data == None:
            return

        data.SetLabelValue(labelValue)

    #===========================================
    # ラベル値の取得
    #===========================================
    def GetLabelValue(self, name, typ = "string"):

        data = self.GetSettingData(name)

        if data == None:
            return u""

        value = data.labelValue

        if typ == "string":

            try:
                return str(value)
            except:
                return u""

        elif typ == "int":

            try:
                return int(value)
            except:
                return 0

        elif typ == "float":

            try:
                return float(value)
            except:
                return 0.0

        return u""

    #===========================================
    # EnableCheckButton
    #===========================================
    def EnableCheckButton(self, name, enable):

        data = self.GetSettingData(name)

        if data == None:
            return

        data.EnableCheckButton(enable)

    #===========================================
    # ExecuteSelectButton
    #===========================================
    def ExecuteCheckButton(self, name):

        data = self.GetSettingData(name)

        if data == None:
            return

        data.ExecuteCheckButton()

    #===========================================
    # IsChecked
    #===========================================
    def IsChecked(self, name):

        data = self.GetSettingData(name)

        if data == None:
            return

        return data.check

    #===========================================
    # ToggleCheck
    #===========================================
    def ToggleCheck(self, name):

        data = self.GetSettingData(name)

        if data == None:
            return

        data.ToggleCheck()

    #===========================================
    # ChangeLabelValue
    #===========================================
    def ChangeLabelValue(self, name):

        data = self.GetSettingData(name)

        if data == None:
            return

        data.ChangeLabelValue()

    #===========================================
    # SetResult
    #===========================================
    def SetResult(self, name, targetList):

        data = self.GetSettingData(name)

        if data == None:
            return

        data.resultList = targetList

        if len(data.resultList) == 0:
            self.EnableCheckButton(name, False)
            return

        self.EnableCheckButton(name, True)

    #===========================================
    # Create
    #===========================================
    def Create(self):

        self.CreateSettingDataList()

        self.CreateUI()

        self.LoadSetting()

    #===========================================
    # CreateUI
    #===========================================
    def CreateUI(self):

        if self.isDirect == False:
            return

        global g_toolName
        global g_scriptPrefix
        global g_uiPrefix

        width=400
        height=1
        formWidth=width-5

        windowTitle=g_scriptPrefix.replace(".","")
        windowName=windowTitle+"Win"

        TkgUtility.CheckWindow(windowName)

        cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=False,mnb=True,mxb=False,rtf=True)

        cmds.columnLayout(adjustableColumn=True)

        cmds.scrollLayout(g_uiPrefix + "LayerScrollList",verticalScrollBarThickness=5, h=500, cr=True)

        cmds.frameLayout(l=u"ファイル存在確認系",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        self.CreateUIFromData(self.uiExistModelFile,"")
        self.CreateUIFromData(self.uiExistTextureFile,"")

        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.frameLayout(l=u"ノード存在確認系",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        self.CreateUIFromData(self.uiExistGroup,"")
        self.CreateUIFromData(self.uiExistMesh,"")
        self.CreateUIFromData(self.uiExistLocator,"")
        self.CreateUIFromData(self.uiExistJoint,"")
        self.CreateUIFromData(self.uiExistMaterial,"")

        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.frameLayout(l=u"座標確認系",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        self.CreateUIFromData(self.uiPosGroup,"")
        self.CreateUIFromData(self.uiPosMesh,"")
        self.CreateUIFromData(self.uiPosLocator,"")
        self.CreateUIFromData(self.uiPosJoint,"")
        
        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.frameLayout(l=u"UV系",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        self.CreateUIFromData(self.uiModelUVNum,"")
        self.CreateUIFromData(self.uiModelUVName,"")
        self.CreateUIFromData(self.uiModelUVRange,"")

        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.frameLayout(l=u"頂点カラー系",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        self.CreateUIFromData(self.uiVCColorSetNum,"")
        self.CreateUIFromData(self.uiVCColorSetName,"")
        self.CreateUIFromData(self.uiVCUnshared,"")

        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.frameLayout(l=u"スキン系",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        self.CreateUIFromData(self.uiWeightInfluence,"")
        self.CreateUIFromData(self.uiWeightRound,"")
        self.CreateUIFromData(self.uiWeightJointFreeze,"")

        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.frameLayout(l=u"クリーンアップ系",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
        cmds.columnLayout(adjustableColumn=True)

        self.CreateUIFromData(self.uiClean4Side,"")
        self.CreateUIFromData(self.uiCleanConcave,"")
        self.CreateUIFromData(self.uiCleanHole,"")
        self.CreateUIFromData(self.uiCleanLamina,"")
        self.CreateUIFromData(self.uiCleanNonmanifold,"")
        self.CreateUIFromData(self.uiCleanZeroEdge,"")
        
        cmds.setParent( ".." )
        cmds.setParent( ".." )

        cmds.setParent( ".." )

        cmds.button( label="Check", bgc=(0.8,0.5,0.5) ,w=formWidth, h=40, command="import TkgDataCheckerBase;TkgDataCheckerBase.ExecuteDirectCheck()")

        cmds.separator( style='in',h=15,w=formWidth)
        
        cmds.button( label="About",w=formWidth,command=g_scriptPrefix + "ShowAbout()")

        cmds.setParent( ".." )
     
        cmds.showWindow(windowName)

        self.ResetUI()

    #===========================================
    # ResetUI
    #===========================================
    def ResetUI(self):

        self.EnableCheckButton(self.uiExistModelFile, False)
        self.EnableCheckButton(self.uiExistTextureFile, False)

        self.EnableCheckButton(self.uiExistGroup, False)
        self.EnableCheckButton(self.uiExistMesh, False)
        self.EnableCheckButton(self.uiExistLocator, False)
        self.EnableCheckButton(self.uiExistJoint, False)
        self.EnableCheckButton(self.uiExistMaterial, False)

        self.EnableCheckButton(self.uiPosGroup, False)
        self.EnableCheckButton(self.uiPosMesh, False)
        self.EnableCheckButton(self.uiPosLocator, False)
        self.EnableCheckButton(self.uiPosJoint, False)

        self.EnableCheckButton(self.uiModelUVNum, False)
        self.EnableCheckButton(self.uiModelUVName, False)
        self.EnableCheckButton(self.uiModelUVRange, False)

        self.EnableCheckButton(self.uiVCColorSetNum, False)
        self.EnableCheckButton(self.uiVCColorSetName, False)
        self.EnableCheckButton(self.uiVCUnshared, False)

        self.EnableCheckButton(self.uiWeightRound, False)
        self.EnableCheckButton(self.uiWeightInfluence, False)
        self.EnableCheckButton(self.uiWeightJointFreeze, False)

        self.EnableCheckButton(self.uiClean4Side, False)
        self.EnableCheckButton(self.uiCleanConcave, False)
        self.EnableCheckButton(self.uiCleanHole, False)
        self.EnableCheckButton(self.uiCleanLamina, False)
        self.EnableCheckButton(self.uiCleanNonmanifold, False)
        self.EnableCheckButton(self.uiCleanZeroEdge, False)

    #===========================================
    # LoadSetting
    #===========================================
    def LoadSetting(self):

        if self.defaultSetting == None:
            return

        self.SetLabelValue(self.uiExistModelFile,self.defaultSetting.Load("ExistModelFile"))
        self.SetLabelValue(self.uiExistTextureFile,self.defaultSetting.Load("ExistTextureFile"))

        self.SetLabelValue(self.uiExistGroup,self.defaultSetting.Load("ExistGroup"))
        self.SetLabelValue(self.uiExistMesh,self.defaultSetting.Load("ExistMesh"))
        self.SetLabelValue(self.uiExistLocator,self.defaultSetting.Load("ExistLocator"))
        self.SetLabelValue(self.uiExistJoint,self.defaultSetting.Load("ExistJoint"))
        self.SetLabelValue(self.uiExistMaterial,self.defaultSetting.Load("ExistMaterial"))

        self.SetLabelValue(self.uiPosGroup,self.defaultSetting.Load("PosGroup"))
        self.SetLabelValue(self.uiPosMesh,self.defaultSetting.Load("PosMesh"))
        self.SetLabelValue(self.uiPosLocator,self.defaultSetting.Load("PosLocator"))
        self.SetLabelValue(self.uiPosJoint,self.defaultSetting.Load("PosJoint"))

        self.SetLabelValue(self.uiModelUVNum,self.defaultSetting.Load("UVNum"))
        self.SetLabelValue(self.uiModelUVName,self.defaultSetting.Load("UVName"))
        self.SetLabelValue(self.uiModelUVRange,self.defaultSetting.Load("UVRange"))

        self.SetLabelValue(self.uiVCColorSetNum,self.defaultSetting.Load("ColorSetNum"))
        self.SetLabelValue(self.uiVCColorSetName,self.defaultSetting.Load("ColorSetName"))
        self.SetLabelValue(self.uiVCUnshared,self.defaultSetting.Load("UnsharedVtxColor"))

        self.SetLabelValue(self.uiWeightInfluence,self.defaultSetting.Load("WeightInfluenceNum"))
        self.SetLabelValue(self.uiWeightRound,self.defaultSetting.Load("WeightDigit"))
        self.SetLabelValue(self.uiWeightJointFreeze,self.defaultSetting.Load("JointFreeze"))

        self.SetLabelValue(self.uiClean4Side,self.defaultSetting.Load("CleanMore4Side"))
        self.SetLabelValue(self.uiCleanConcave,self.defaultSetting.Load("CleanConcaveFace"))
        self.SetLabelValue(self.uiCleanHole,self.defaultSetting.Load("CleanHole"))
        self.SetLabelValue(self.uiCleanLamina,self.defaultSetting.Load("CleanLaminaFace"))
        self.SetLabelValue(self.uiCleanNonmanifold,self.defaultSetting.Load("CleanNonmanifold"))
        self.SetLabelValue(self.uiCleanZeroEdge,self.defaultSetting.Load("CleanZeroEdge"))
    
    #===========================================
    # Initialize
    #===========================================
    def Initialize(self):

        if self.filterString != "":
            self.filterList = self.filterString.split(",")

        self.resultDict = {}
        
        self.dataList = []

        #ログ登録
        self.logList = []

        self.logList.append("")

        self.logList.append("********************************************************")
        self.logList.append(u"データチェック")
        self.logList.append("********************************************************")

        self.logList.append("")

        self.logList.append(u"\tモデルファイル存在確認")
        self.logList.append(u"\tテクスチャファイル存在確認")

        self.logList.append(u"\tグループノード存在確認")
        self.logList.append(u"\tメッシュノード存在確認")
        self.logList.append(u"\tロケータノード存在確認")
        self.logList.append(u"\tジョイントノード存在確認")
        self.logList.append(u"\tマテリアルノード存在確認")

        self.logList.append(u"\tグループの位置と回転とスケール確認")
        self.logList.append(u"\tメッシュの位置と回転とスケール確認")
        self.logList.append(u"\tロケータの位置と回転とスケール確認")
        self.logList.append(u"\tジョイントの位置と回転とスケール確認")
        
        self.logList.append(u"\tUVセットの数確認")
        self.logList.append(u"\tUVセットの名前確認")
        self.logList.append(u"\tUVセットの範囲確認")

        self.logList.append(u"\tカラーセットの数確認")
        self.logList.append(u"\tカラーセットの名前確認")
        self.logList.append(u"\t頂点カラーのUnshared確認")

        self.logList.append(u"\tインフルエンス数確認")
        self.logList.append(u"\tウェイト精度確認")
        self.logList.append(u"\tジョイントの回転、スケール、オリエント確認")
        
        self.logList.append(u"\t5辺以上のフェース")
        self.logList.append(u"\t凹型フェース")
        self.logList.append(u"\t穴のあるフェース")
        self.logList.append(u"\tラミナフェース(すべてのエッジを共有するフェース)")
        self.logList.append(u"\t非多様体ジオメトリ(法線とジオメトリ)")
        self.logList.append(u"\t0エッジの確認")

        self.ResetUI()
        
    #===========================================
    # Check
    #===========================================
    def Check(self):

        self.Initialize()

        childFolderList = []

        if self.isDirect == False:
            
            childFolderList = os.listdir(self.rootPath)

            for childFolder in childFolderList:

                newCheckData = CheckData(self)
                newCheckData.rootPath = self.rootPath + "/" + childFolder

                self.dataList.append(newCheckData)
            
        else:

            currentFilePath = cmds.file(q=True, sn=True)
            sceneFolderPath = os.path.dirname(currentFilePath)
            rootFolderPath = os.path.dirname(sceneFolderPath)

            newCheckData = CheckData(self)
            newCheckData.rootPath = rootFolderPath

            self.dataList.append(newCheckData)

        for p in range(0,len(self.dataList)):

            self.dataList[p].Check()

    #===========================================
    # Log
    #===========================================
    def Log(self):

        existRoot = False
        for p in range(0,len(self.dataList)):

            if len(self.dataList[p].rootList) != 0:
                existRoot = True

            self.dataList[p].Log()

        if existRoot == False:
            return

        if self.isDirect == False:

            thisFile = open(self.logFilePath,"w")

            for p in range(0,len(self.logList)):
                thisFile.write(self.logList[p].encode("utf-8") + "\n")

            thisFile.close()

        else:

            logStr = ""

            for p in range(0,len(self.logList)):
                print(self.logList[p])

                logStr += self.logList[p] + "\n"

            mel.eval("ScriptEditor;")

    #===========================================
    # CheckExistNode
    #===========================================
    def CheckExistNode(self, name, rootList):

        if self.IsChecked(name) == False:
            return

        if rootList == None:
            return

        if len(rootList) == 0:
            return

        notExistList = []
        logList = []

        targetType = ""
        targetTypeName = ""
        
        if name == self.uiExistMesh:
            targetType = "mesh"
            targetTypeName = u"メッシュ"
        elif name == self.uiExistLocator:
            targetType = "locator"
            targetTypeName = u"ロケータ"
        elif name == self.uiExistJoint:
            targetType = "joint"
            targetTypeName = u"ジョイント"
        elif name == self.uiExistGroup:
            targetType = "transform"
            targetTypeName = u"グループ"
        elif name == self.uiExistMaterial:
            targetType = "lambert"
            targetTypeName = u"マテリアル"

        if targetType == "":
            return

        objectNameListStr = self.GetLabelValue(name, "string")

        objectNameList = objectNameListStr.split(",")

        if len(objectNameList) == 0:
            return

        for objectName in objectNameList:

            if objectName == None:
                continue

            if objectName == "":
                continue

            objectName = self.GetReplaceName(objectName)

            thisObject = ""
            if targetType != "lambert":
                thisObject = self.GetObjectInList(objectName, rootList)
            else:
                thisObject = objectName

            if thisObject != None:
                
                if self.GetFirstShapeType(thisObject) == targetType:                    
                    continue

            notExistList.append(objectName)
            logList.append(WriteLogA(targetTypeName, objectName, u"存在しない"))
            
        if len(notExistList) == 0:
            return

        return logList, notExistList

    #===========================================
    # CheckExistNode
    #===========================================
    def CheckExistFile(self, name):

        if self.IsChecked(name) == False:
            return

        notExistList = []
        logList = []

        currentFilePath = cmds.file(q=True, sn=True)
        sceneFolderPath = os.path.dirname(currentFilePath)
        rootFolderPath = os.path.dirname(sceneFolderPath)

        targetType = ""
        searchRootPath = ""
        targetTypeName = ""
        
        if name == self.uiExistTextureFile:
            targetType = "texture"
            searchRootPath = rootFolderPath + "/sourceimages"
            targetTypeName = u"テクスチャ"
        elif name == self.uiExistModelFile:
            targetType = "maya"
            searchRootPath = rootFolderPath + "/scenes"
            targetTypeName = u"モデル"

        fileNameListStr = self.GetLabelValue(name, "string")

        fileNameList = fileNameListStr.split(",")

        if len(fileNameList) == 0:
            return

        for fileName in fileNameList:

            if fileName == None:
                continue

            if fileName == "":
                continue

            fileName = self.GetReplaceName(fileName)

            thisFilePath = searchRootPath + "/" + fileName

            if os.path.isfile(thisFilePath) == False:
                notExistList.append(fileName)
                logList.append(WriteLogA(targetTypeName, fileName, u"存在しない"))

        if len(notExistList) == 0:
            return

        return logList, notExistList

    #===========================================
    # CheckPos
    #===========================================
    def CheckPosition(self, name, rootList):

        if self.IsChecked(name) == False:
            return

        if rootList == None:
            return

        if len(rootList) == 0:
            return

        notWrongList = []
        logList = []

        targetType = ""
        targetTypeName = ""
        
        if name == self.uiPosMesh:
            targetType = "mesh"
            targetTypeName = u"メッシュ"
        elif name == self.uiPosLocator:
            targetType = "locator"
            targetTypeName = u"ロケータ"
        elif name == self.uiPosJoint:
            targetType = "joint"
            targetTypeName = u"ジョイント"
        elif name == self.uiPosGroup:
            targetType = "transform"
            targetTypeName = u"グループ"

        if targetType == "":
            return

        objectNameListStr = self.GetLabelValue(name, "string")

        objectNameList = objectNameListStr.split(",")

        if len(objectNameList) == 0:
            return

        for objectName in objectNameList:

            if objectName == None:
                continue

            if objectName == "":
                continue

            objectName = self.GetReplaceName(objectName)
            fixObjectName = self.GetFixName(objectName)

            thisObject = self.GetObjectInList(fixObjectName, rootList)

            if thisObject == None:
                continue
                
            if self.GetFirstShapeType(thisObject) != targetType:                    
                continue

            posCheckFlag = self.GetPosCheckFlag(objectName)

            thisLogList = self.CheckPositionBase(thisObject, targetTypeName, posCheckFlag[0], posCheckFlag[1], posCheckFlag[2], posCheckFlag[3], posCheckFlag[4], posCheckFlag[5], posCheckFlag[6], posCheckFlag[7], posCheckFlag[8])

            if len(thisLogList) != 0:

                notWrongList.append(fixObjectName)
                logList.extend(thisLogList)

        if len(notWrongList) == 0:
            return

        return logList, notWrongList

    #===========================================
    # GetFixName
    #===========================================
    def GetFixName(self, target):

        if target.find(".") == -1:
            return target

        splitStr = target.split(".")

        return splitStr[0]

    #===========================================
    # GetCheckFlag
    #===========================================
    def GetPosCheckFlag(self, target):

        result = [True,True,True,True,True,True,True,True,True]

        if target.find(".") == -1:
            return result

        if target.find(".tx") != -1:
            result[0] = False

        if target.find(".ty") != -1:
            result[1] = False

        if target.find(".tz") != -1:
            result[2] = False

        if target.find(".ta") != -1:
            result[0] = False
            result[1] = False
            result[2] = False

        if target.find(".rx") != -1:
            result[3] = False

        if target.find(".ry") != -1:
            result[4] = False

        if target.find(".rz") != -1:
            result[5] = False

        if target.find(".ra") != -1:
            result[3] = False
            result[4] = False
            result[5] = False

        if target.find(".sx") != -1:
            result[6] = False

        if target.find(".sy") != -1:
            result[7] = False

        if target.find(".sz") != -1:
            result[8] = False

        if target.find(".sa") != -1:
            result[6] = False
            result[7] = False
            result[8] = False

        return result

    #===========================================
    # CheckPosition
    #===========================================
    def CheckPositionBase(self, target, nodeType, transX, transY, transZ, rotateX, rotateY, rotateZ, scaleX, scaleY, scaleZ):

        logList = []

        if cmds.objExists(target) == False:
            return logList

        thiszTransValue = TupleToList(cmds.getAttr(target + ".translate")[0])
        thiszRotateValue = TupleToList(cmds.getAttr(target + ".rotate")[0])
        thiszScaleValue = TupleToList(cmds.getAttr(target + ".scale")[0])

        thiszTransValue[0] = RoundValue(thiszTransValue[0])
        thiszTransValue[1] = RoundValue(thiszTransValue[1])
        thiszTransValue[2] = RoundValue(thiszTransValue[2])

        thiszRotateValue[0] = RoundValue(thiszRotateValue[0])
        thiszRotateValue[1] = RoundValue(thiszRotateValue[1])
        thiszRotateValue[2] = RoundValue(thiszRotateValue[2])

        thiszScaleValue[0] = RoundValue(thiszScaleValue[0])
        thiszScaleValue[1] = RoundValue(thiszScaleValue[1])
        thiszScaleValue[2] = RoundValue(thiszScaleValue[2])

        if transX == True and transY == True and transZ == True:
            if thiszTransValue[0] != 0 or thiszTransValue[1] != 0 or thiszTransValue[2] != 0:
                logList.append(WriteLogA(nodeType,target,"位置が0ではない"))
        else:
            if thiszTransValue[0] != 0 and transX == True:
                logList.append(WriteLogA(nodeType,target,"X位置が0ではない"))

            if thiszTransValue[1] != 0 and transY == True:
                logList.append(WriteLogA(nodeType,target,"Y位置が0ではない"))

            if thiszTransValue[2] != 0 and transZ == True:
                logList.append(WriteLogA(nodeType,target,"Z位置が0ではない"))

        if rotateX == True and rotateY == True and rotateZ == True:
            if thiszRotateValue[0] != 0 or thiszRotateValue[1] != 0 or thiszRotateValue[2] != 0:
                logList.append(WriteLogA(nodeType,target,"回転が0ではない"))
        else:
            if thiszRotateValue[0] != 0 and rotateX == True:
                logList.append(WriteLogA(nodeType,target,"X回転が0ではない"))

            if thiszRotateValue[1] != 0 and rotateY == True:
                logList.append(WriteLogA(nodeType,target,"Y回転が0ではない"))

            if thiszRotateValue[2] != 0 and rotateZ == True:
                logList.append(WriteLogA(nodeType,target,"Z回転が0ではない"))

        if scaleX == True and scaleY == True and scaleZ == True:
            if thiszScaleValue[0] != 1 or thiszScaleValue[1] != 1 or thiszScaleValue[2] != 1:
                logList.append(WriteLogA(nodeType,target,"スケールが1ではない"))
        else:
            if thiszScaleValue[0] != 1 and scaleX == True:
                logList.append(WriteLogA(nodeType,target,"Xスケールが1ではない"))

            if thiszScaleValue[1] != 1 and scaleY == True:
                logList.append(WriteLogA(nodeType,target,"Yスケールが1ではない"))

            if thiszScaleValue[2] != 1 and scaleZ == True:
                logList.append(WriteLogA(nodeType,target,"Zスケールが1ではない"))

        shapeNodeList = cmds.listRelatives(target,s=True)

        if shapeNodeList != None:
            
            if len(shapeNodeList) != 0:

                shapeNode = shapeNodeList[0]
                
                if cmds.objectType(shapeNode) == "locator":
                    
                    thiszScalePivotValue = TupleToList(cmds.getAttr(target + ".rotatePivot")[0])

                    thiszLocPosValue = [0,0,0]
                    thiszLocScaleValue = [0,0,0]
                    
                    thiszLocPosValue[0] = cmds.getAttr(target + ".localPositionX")
                    thiszLocPosValue[1] = cmds.getAttr(target + ".localPositionY")
                    thiszLocPosValue[2] = cmds.getAttr(target + ".localPositionZ")
                    
                    thiszLocScaleValue[0] = cmds.getAttr(target + ".localScaleX")
                    thiszLocScaleValue[1] = cmds.getAttr(target + ".localScaleY")
                    thiszLocScaleValue[2] = cmds.getAttr(target + ".localScaleZ")

                    differPivitPos = False
                    if thiszScalePivotValue[0] != 0 or thiszScalePivotValue[1] != 0 or thiszScalePivotValue[2] != 0:
                        logList.append(WriteLogA(nodeType,target,"ロケータのセンター位置がずれています"))
                        differPivitPos = True

                    if differPivitPos == False:
                        if thiszLocPosValue[0] != 0 or thiszLocPosValue[1] != 0 or thiszLocPosValue[2] != 0:
                            logList.append(WriteLogA(nodeType,target,"ロケータのローカル移動値が入っています"))
                            differPivitPos = True

                    if differPivitPos == False:
                        if thiszLocScaleValue[0] != 1 or thiszLocScaleValue[1] != 1 or thiszLocScaleValue[2] != 1:
                            logList.append(WriteLogA(nodeType,target,"ロケータのローカルスケール値が入っています"))
                            differPivitPos = True

        return logList

    #===========================================
    # CheckColorSetNum
    #===========================================
    def CheckColorSetNum(self, targetList):

        if self.IsChecked(self.uiVCColorSetNum) == False:
            return

        colorSetNum = self.GetLabelValue(self.uiVCColorSetNum, "int")

        resultList = []
        logList = []

        for p in range(0, len(targetList)):

            thisResult = self.CheckColorSetNumBase(targetList[p], colorSetNum)

            if thisResult != None:
                resultList.extend(thisResult[0])
                logList.extend(thisResult[1])

        return resultList, logList 

    #===========================================
    # CheckColorSetNumBase
    #===========================================
    def CheckColorSetNumBase(self, target, colorSetNum):

        resultList = []
        logList =[]

        if self.GetFirstShapeType(target) != "mesh":
            return

        thisColorSets = cmds.polyColorSet(target,q=True,allColorSets=True)

        if thisColorSets == None:
            resultList.append(target)
            logList.append(WriteLogA("メッシュ",target,"カラーセットが0個"))
            return resultList, logList

        if len(thisColorSets) == colorSetNum:
            return

        resultList.append(target)
        logList.append(WriteLogA("メッシュ",target,"カラーセットが" + str(len(thisColorSets)) + "個存在"))
        
        return resultList, logList

    #===========================================
    # CheckColorSetName
    #===========================================
    def CheckColorSetName(self, targetList):

        if self.IsChecked(self.uiVCColorSetName) == False:
            return

        colorSetName = self.GetLabelValue(self.uiVCColorSetName, "string")

        colorSetNameList = colorSetName.split(",")

        if len(colorSetNameList) == 0:
            return

        resultList = []
        logList = []

        for p in range(0, len(targetList)):

            thisResult = self.CheckColorSetNameBase(targetList[p], colorSetNameList)

            if thisResult != None:
                resultList.extend(thisResult[0])
                logList.extend(thisResult[1])

        return resultList, logList 

    #===========================================
    # CheckColorSetNameBase
    #===========================================
    def CheckColorSetNameBase(self, target, colorNameList):

        resultList = []
        logList =[]

        if self.GetFirstShapeType(target) != "mesh":
            return

        thisColorSets = cmds.polyColorSet(target,q=True,allColorSets=True)

        if thisColorSets == None:
            resultList.append(target)
            logList.append(WriteLogA("メッシュ",target,"カラーセットが存在していない"))
            return resultList, logList

        for colorSetName in colorNameList:

            existColor = False
            for colorSet in thisColorSets:

                if colorSet == colorSetName:
                    existColor = True
                    break

            if existColor == True:
                continue

            resultList.append(target)
            logList.append(WriteLogA("メッシュ", target, u"カラーセット " + colorSetName + u" が存在していない"))
        
        return resultList, logList

    #===========================================
    # CheckUVSetNum
    #===========================================
    def CheckUVSetNum(self, targetList):

        if self.IsChecked(self.uiModelUVNum) == False:
            return

        uvNum = self.GetLabelValue(self.uiModelUVNum, "int")

        resultList = []
        logList = []

        for p in range(0,len(targetList)):

            thisResult = self.CheckUVSetNumBase(targetList[p], uvNum)

            if thisResult != None:
                resultList.extend(thisResult[0])
                logList.extend(thisResult[1])

        return resultList, logList

    #===========================================
    # CheckUVSetNumBase
    #===========================================
    def CheckUVSetNumBase(self, target, uvNum):

        resultList = []
        logList = []

        if self.GetFirstShapeType(target) != "mesh":
            return

        thisUVSets = cmds.polyUVSet(target,q=True,allUVSets=True)

        if thisUVSets == None:
            resultList.append(target)
            logList.append(WriteLogA("メッシュ",target,"UVセットが0個"))
            return resultList, logList

        if len(thisUVSets) == uvNum:
            return

        resultList.append(target)
        logList.append(WriteLogA("メッシュ",target, "UVセットが" + str(len(thisUVSets)) + "個存在"))

        return resultList, logList

    #===========================================
    # CheckUVSetName
    #===========================================
    def CheckUVSetName(self, targetList):

        if self.IsChecked(self.uiModelUVName) == False:
            return

        uvName = self.GetLabelValue(self.uiModelUVName, "string")

        resultList = []
        logList = []

        for p in range(0,len(targetList)):

            thisResult = self.CheckUVSetNameBase(targetList[p], uvName)

            if thisResult != None:
                resultList.extend(thisResult[0])
                logList.extend(thisResult[1])

        return resultList, logList

    #===========================================
    # CheckUVSetNameBase
    #===========================================
    def CheckUVSetNameBase(self, target, uvName):

        resultList = []
        logList = []

        if self.GetFirstShapeType(target) != "mesh":
            return

        uvNameList = uvName.split(",")

        if len(uvNameList) == 0:
            return

        thisUVSets = cmds.polyUVSet(target,q=True,allUVSets=True)

        if thisUVSets == None:
            resultList.append(target)
            logList.append(WriteLogA("メッシュ",target,"UVセットが存在していない"))
            return resultList, logList

        for uvName in uvNameList:

            existUV = False
            for uvSet in thisUVSets:

                if uvSet == uvName:
                    existUV = True
                    break

            if existUV:
                continue

            resultList.append(target)
            logList.append(WriteLogA("メッシュ", target, u"UVセット " + uvName + u" が存在していない"))

        return resultList, logList

    #===========================================
    # CheckUVSetRange
    #===========================================
    def CheckUVSetRange(self, targetList):

        if self.IsChecked(self.uiModelUVRange) == False:
            return

        uvRange = self.GetLabelValue(self.uiModelUVRange, "string")

        uvRangeList = uvRange.split(",")

        if len(uvRangeList) != 2:
            return

        resultList = []
        logList = []

        for p in range(0,len(targetList)):

            thisResult = self.CheckUVSetRangeBase(targetList[p], float(uvRangeList[0]), float(uvRangeList[1]))

            if thisResult != None:
                resultList.extend(thisResult[0])
                logList.extend(thisResult[1])

        return resultList, logList

    #===========================================
    # CheckUVSetRangeBase
    #===========================================
    def CheckUVSetRangeBase(self, target, minRange, maxRange):

        resultList = []
        logList = []

        if self.GetFirstShapeType(target) != "mesh":
            return

        thisUVSets = cmds.polyUVSet(target,q=True,allUVSets=True)

        if thisUVSets == None:
            resultList.append(target)
            logList.append(WriteLogA("メッシュ",target,"UVがないので、範囲判定不可"))
            return resultList, logList

        for uvSet in thisUVSets:

            cmds.polyUVSet( currentUVSet=True,  uvSet=uvSet)
            cmds.select(target, r=True)

            mel.eval("PolySelectConvert 4;")

            uvList = cmds.ls(sl=True,fl=True,l=True)

            if uvList == None:
                resultList.append(target)
                continue

            if len(uvList) == 0:
                resultList.append(target)
                continue

            for uv in uvList:

                uvValue = cmds.polyEditUV(uv, query=True)

                if uvValue == None:
                    resultList.append(uv)
                    continue

                if len(uvValue) == 0:
                    resultList.append(uv)
                    continue

                if uvValue[0] >= minRange and uvValue[0] <= maxRange and uvValue[1] >= minRange and uvValue[1] <= maxRange:
                    continue

                resultList.append(uv)

        if len(resultList) > 0:
            logList.append(WriteLogA("メッシュ",target,"UVが " + str(minRange) + "～" + str(maxRange) + " の範囲外"))

        return resultList, logList

    #===========================================
    # CheckWeight
    #===========================================
    def CheckWeight(self, targetList):

        resultOutRoundVtxList = []
        resultOutInfluenceVtxList = []
        resultLogList = []

        for p in range(0,len(targetList)):

            result = self.CheckWeightBase(targetList[p])

            if result == None:
                continue

            resultLogList.extend(result[0])
            resultOutRoundVtxList.extend(result[1])
            resultOutInfluenceVtxList.extend(result[2])

        if len(resultOutRoundVtxList) == 0 and len(resultOutInfluenceVtxList) == 0 and len(resultLogList) == 0 :
            return

        return resultLogList, resultOutRoundVtxList, resultOutInfluenceVtxList

    #===========================================
    # CheckWeightBase
    #===========================================
    def CheckWeightBase(self, target):

        outRoundVtxList = []
        outInfluenceVtxList = []
        logList = []

        if cmds.objExists(target) == False:
            return

        clusterName=mel.eval("findRelatedSkinCluster "+target)

        if clusterName=="":
            return

        cmds.select(target,r=True)

        selectList=cmds.ls(sl=True,l=True)
     
        mel.eval("PolySelectConvert 3")
        
        vtxList=cmds.ls(sl=True,l=True,fl=True)

        if len(vtxList)==0:
            return

        existOutRound = False
        existOutInfluence = False

        enableRound = self.IsChecked(self.uiWeightRound)
        enableInfluence = self.IsChecked(self.uiWeightInfluence)

        roundNum = self.GetLabelValue(self.uiWeightRound, "int")
        influenceNum = self.GetLabelValue(self.uiWeightInfluence, "int")

        if enableRound == False and enableInfluence == False:
            return

        for p in range(0,len(vtxList)):

            thisVertex = vtxList[p]
            thisVertexIndex = GetVertexIndex(thisVertex)
            
            jointList=cmds.skinPercent(clusterName,thisVertex, query=True, t=None )
            weightList = cmds.skinPercent(clusterName,thisVertex, query=True, value=True )

            if len(jointList) != len(weightList):
                return

            fixJointList = []
            fixWeightList = []
            for q in range(len(jointList)):

                if int(weightList[q]*10000) == 0:
                    continue

                fixJointList.append(jointList[q])
                fixWeightList.append(weightList[q])

            if enableRound == True:
                
                for q in range(len(fixWeightList)):

                    thisWeight = fixWeightList[q]
                    thisWeightMulti = thisWeight * math.pow(10,roundNum)

                    tempValue = math.modf(thisWeightMulti);

                    if tempValue[0] < 0.01 or tempValue[0] > 0.99:
                        continue

                    existOutRound = True
                    outRoundVtxList.append(thisVertex)

            if len(fixJointList) > influenceNum and enableInfluence == True:
                existOutInfluence = True
                outInfluenceVtxList.append(thisVertex)

        if existOutRound == True:
            logList.append(WriteLogA(u"メッシュ", target, u"ウェイト精度が少数" + str(roundNum) + u"桁ではない"))

        if existOutInfluence == True:
            logList.append(WriteLogA(u"メッシュ", target, u"インフルエンス数が" + str(influenceNum) + u"ではない"))


        return  logList, outRoundVtxList, outInfluenceVtxList


    #===========================================
    # CheckJoint
    #===========================================
    def CheckJointFreeze(self, targetList):

        resultList = []
        logList = []

        for p in range(0,len(targetList)):

            thisResult = self.CheckJointFreezeBase(targetList[p])

            if thisResult != None:
                resultList.extend(thisResult[0])
                logList.extend(thisResult[1])

        return resultList, logList

    #===========================================
    # CheckJoint
    #===========================================
    def CheckJointFreezeBase(self, target):

        resultList = []
        logList = []

        if cmds.objExists(target) == False:
            return

        cmds.select(target,r=True,hi=True)

        selectList = cmds.ls(sl=True,l=True,typ="joint")

        if selectList == None:
            return

        if len(selectList) == 0:
            return

        for p in range(0,len(selectList)):

            thiszTransValue = cmds.getAttr(selectList[p] + ".translate")[0]
            thiszRotateValue = cmds.getAttr(selectList[p] + ".rotate")[0]
            thiszScaleValue = cmds.getAttr(selectList[p] + ".scale")[0]
            thiszOrientValue = cmds.getAttr(selectList[p] + ".jointOrient")[0]

            shortName = GetShortName(selectList[p])

            if SameValue(thiszRotateValue[0],0)==False or SameValue(thiszRotateValue[1],0)==False or SameValue(thiszRotateValue[2],0)==False:
                resultList.append(selectList[p])
                logList.append(WriteLogA("ジョイント",shortName,"回転値が0ではない"))

            if SameValue(thiszScaleValue[0],1)==False or SameValue(thiszScaleValue[1],1)==False or SameValue(thiszScaleValue[2],1)==False:
                resultList.append(selectList[p])
                logList.append(WriteLogA("ジョイント",shortName,"スケール値が1ではない"))

            if SameValue(thiszOrientValue[0],0)==False or SameValue(thiszOrientValue[1],0)==False or SameValue(thiszOrientValue[2],0)==False:
                resultList.append(selectList[p])
                logList.append(WriteLogA("ジョイント",shortName,"オリエントが0ではない"))

        if len(logList) == 0:
            return

        return resultList, logList

    #===========================================
    # CheckUnsharedVertexColor
    #===========================================
    def CheckUnsharedVertexColor(self, targetList):

        if self.IsChecked(self.uiVCUnshared) == False:
            return

        resultList = []
        logList = []

        for p in range(0,len(targetList)):

            thisResult = self.CheckUnsharedVertexColorBase(targetList[p])

            if thisResult != None:
                resultList.extend(thisResult[0])
                logList.extend(thisResult[1])

        return resultList, logList

    #===========================================
    # CheckUnsharedVertexColorBase
    #===========================================
    def CheckUnsharedVertexColorBase(self, target):

        resultList = []
        logList = []

        if self.GetFirstShapeType(target) != "mesh":
            return

        thisColorSets = cmds.polyColorSet(target,q=True,allColorSets=True)

        if thisColorSets == None:
            return

        if len(thisColorSets) == 0:
            return
        
        targetVertexLog = ""

        for colorSet in thisColorSets:

            cmds.polyColorSet(currentColorSet=True, colorSet= colorSet )

            cmds.select(target,r=True)

            selectList=cmds.ls(sl=True,l=True)
         
            mel.eval("PolySelectConvert 3")
            
            vtxList=cmds.ls(sl=True,l=True,fl=True)

            if len(vtxList)==0:
                continue

            shortName = GetShortName(target)

            for p in range(0,len(vtxList)):

                thisVertex = vtxList[p]

                thisVtxColor = cmds.polyColorPerVertex(thisVertex,q=True,r=True,g=True,b=True,a=True)

                replaceVtxName = thisVertex.replace("vtx[","vtxFace[")

                thisVtxFaceList = cmds.ls(replaceVtxName + "[*]",l=True,fl=True)

                if len(thisVtxFaceList) <= 1:
                    continue

                thisBaseVtxColor = cmds.polyColorPerVertex(thisVtxFaceList[0],q=True,r=True,g=True,b=True,a=True)

                for q in range(1,len(thisVtxFaceList)):

                    thisVtxFaceColor = cmds.polyColorPerVertex(thisVtxFaceList[q],q=True,r=True,g=True,b=True,a=True)

                    if SameVector(thisBaseVtxColor, thisVtxFaceColor) == False:
                        resultList.append(thisVertex)
                        targetVertexLog += str(GetVertexIndex(thisVertex)) + ","
                        break

        if targetVertexLog == "":
            return

        logList.append(WriteLogA("メッシュ",shortName,"頂点カラー UnsharedIndex : " + targetVertexLog))

        return resultList, logList

    #===========================================
    # CheckCleanup
    #===========================================
    def CheckCleanup(self, targetList):

        resultLogList = []
        face4SideList = []
        concaveList = []
        holeList = []
        laminaList = []
        nonmanifoldList = []
        zeroEdgeList = []

        enable4Side = self.IsChecked(self.uiClean4Side)
        enableConcave = self.IsChecked(self.uiCleanConcave)
        enableHole = self.IsChecked(self.uiCleanHole)
        enableLamina = self.IsChecked(self.uiCleanLamina)
        enableNonmanifold = self.IsChecked(self.uiCleanNonmanifold)
        enableZeroEdge = self.IsChecked(self.uiCleanZeroEdge)
        
        for p in range(0,len(targetList)):

            if cmds.objExists(targetList[p]) == False:
                continue

            thisMesh = targetList[p]

            shortName = GetShortName(thisMesh)

            result4Side = self.CheckFaceWithMore4Side(thisMesh)
            resulConcave = self.CheckConcaveFace(thisMesh)
            resultHole = self.CheckFaceWithHole(thisMesh)
            resultLamina = self.CheckLaminaFace(thisMesh)
            resultNonmanifold = self.CheckNonmanifold(thisMesh)
            resultZeroEdge = self.CheckZeroEdge(thisMesh)

            if result4Side != None and enable4Side == True: 
                face4SideList.extend(result4Side)
                resultLogList.append(WriteLogA("メッシュ",shortName,u"5辺以上のフェースが存在"))

            if resulConcave != None and enableConcave == True:
                concaveList.extend(resulConcave)
                resultLogList.append(WriteLogA("メッシュ",shortName,u"凹型フェースが存在"))

            if resultHole != None and enableHole == True:
                holeList.extend(resultHole)
                resultLogList.append(WriteLogA("メッシュ",shortName,u"穴のあるフェースが存在"))

            if resultLamina != None and enableLamina == True:
                laminaList.extend(resultLamina)
                resultLogList.append(WriteLogA("メッシュ",shortName,u"ラミナフェース(すべてのエッジを共有するフェース)が存在"))

            if resultNonmanifold != None and enableNonmanifold == True:
                nonmanifoldList.extend(resultNonmanifold)
                resultLogList.append(WriteLogA("メッシュ",shortName,u"非多様体ジオメトリ(法線とジオメトリ)が存在"))

            if resultZeroEdge != None and enableZeroEdge == True:
                zeroEdgeList.extend(resultZeroEdge)
                resultLogList.append(WriteLogA("メッシュ",shortName,u"長さが0のエッジが存在"))

        return resultLogList, face4SideList, concaveList, holeList, laminaList, nonmanifoldList, zeroEdgeList

    #===========================================
    # CheckFaceWithMore4Side
    #===========================================
    def CheckFaceWithMore4Side(self, target):

        cmds.select(target,r=True)
        
        result = mel.eval("polyCleanupArgList 3 { \"0\",\"2\",\"1\",\"0\",\"1\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }")

        if result == None:
            return

        if len(result) == 0:
            return

        return result

    #===========================================
    # CheckConcaveFace
    #===========================================
    def CheckConcaveFace(self, target):

        cmds.select(target,r=True)
        
        result = mel.eval("polyCleanupArgList 3 { \"0\",\"2\",\"1\",\"0\",\"0\",\"1\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }")

        if result == None:
            return

        if len(result) == 0:
            return

        return result

    #===========================================
    # CheckFaceWithHole
    #===========================================
    def CheckFaceWithHole(self, target):

        cmds.select(target,r=True)
        
        result = mel.eval("polyCleanupArgList 3 { \"0\",\"2\",\"1\",\"0\",\"0\",\"0\",\"1\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }")

        if result == None:
            return

        if len(result) == 0:
            return

        return result

    #===========================================
    # CheckLaminaFace
    #===========================================
    def CheckLaminaFace(self, target):

        cmds.select(target,r=True)
        
        result = mel.eval("polyCleanupArgList 3 { \"0\",\"2\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"1\" }")

        if result == None:
            return

        if len(result) == 0:
            return

        return result

    #===========================================
    # CheckLaminaFace
    #===========================================
    def CheckNonmanifold(self, target):

        cmds.select(target,r=True)
        
        result = mel.eval("polyCleanupArgList 3 { \"0\",\"2\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1\",\"0\" }")

        if result == None:
            return

        if len(result) == 0:
            return

        return result

    #===========================================
    # CheckZeroEdge
    #===========================================
    def CheckZeroEdge(self, target):

        cmds.select(target,r=True)
        
        result = mel.eval("polyCleanupArgList 3 { \"0\",\"2\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"1\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }")

        if result == None:
            return

        if len(result) == 0:
            return

        return result

#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------
class SettingData:

    #===========================================
    # 初期化
    #===========================================
    def __init__(self, main, name):

        self.name = name
        
        self.main = main

        self.uiPrefix = self.main.uiPrefix + self.name

        self.title = ""

        self.check = False

        self.label = ""
        self.labelValue = ""

        self.enableSelect = False

        self.resultList = []

    #===========================================
    # UI作成
    #===========================================
    def CreateUI(self):

        if self.main.isDirect == False:
            return

        cmds.rowLayout(numberOfColumns=4, columnWidth4=(100, 100, 25, 70), adj=2)

        cmds.text(label=self.title)

        enableValue = True
        if self.label == "":
            enableValue = False
            self.labelValue = ""
            
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(25, 75), adj=2, vis=enableValue)
        cmds.text(label=self.label, al="right")
        cmds.textField(self.uiPrefix + "_Value", text=self.labelValue,cc=self.main.scriptPrefix + "ChangeLabelValue(\"" + self.name + "\")")
        cmds.setParent( ".." )

        cmds.checkBox(self.uiPrefix + "_Check", l="", v=False, cc=self.main.scriptPrefix + "ToggleCheck(\"" + self.name + "\")")

        cmds.button(self.uiPrefix + "_CheckButton", label="Check", command=self.main.scriptPrefix + "ExecuteCheckButton(\"" + self.name + "\")")

        cmds.setParent( ".." )

    #===========================================
    # 
    #===========================================
    def SetLabelValue(self, labelValue):

        self.labelValue = labelValue

        if self.labelValue == "":
            self.check = False
        else:
            self.check = True

        if self.main.isDirect == False:
            return

        cmds.checkBox(self.uiPrefix + "_Check", e=True, v=self.check)            
        cmds.textField(self.uiPrefix + "_Value", e=True, text=self.labelValue)

    #===========================================
    # EnableCheckButton
    #===========================================
    def EnableCheckButton(self, enableSelect):

        self.enableSelect = enableSelect

        if self.main.isDirect == False:
            return

        cmds.button(self.uiPrefix + "_CheckButton", e=True, en=self.enableSelect)

    #===========================================
    # ExecuteCheckButton
    #===========================================
    def ExecuteCheckButton(self):

        if self.main.isDirect == False:
            return

        if len(self.resultList) == 0:
            return

        try:

            cmds.select(self.resultList, r=True)

        except:

            resultStr = ""
            for value in self.resultList:
                resultStr += value + "\n"

            cmds.confirmDialog(m=resultStr)

    #===========================================
    # ToggleCheck
    #===========================================
    def ToggleCheck(self):

        if self.main.isDirect == False:
            return

        self.check = cmds.checkBox(self.uiPrefix + "_Check", q=True, v=True)

        print self.check

    #===========================================
    # ChangeLabelValue
    #===========================================
    def ChangeLabelValue(self):

        if self.main.isDirect == False:
            return

        self.labelValue =  cmds.textField(self.uiPrefix + "_Value", q=True, text=True)

        print self.labelValue

#-------------------------------------------------------------------------------------------
#   CheckData
#-------------------------------------------------------------------------------------------
class CheckData:

    #===========================================
    # __init__
    #===========================================
    def __init__(self,manager):

        self.manager = manager
        
        self.rootPath = ""
        self.scenePath = ""
        self.sourceimagePath = ""

        self.id = ""

        self.filePathList = []

        self.rootList = []
        
        self.meshList = []

        self.logList = []

    #===========================================
    # Initialize
    #===========================================
    def Initialize(self):

        self.id = os.path.basename(self.rootPath)

        self.scenePath = self.rootPath + "/scenes"
        self.sourceimagePath = self.rootPath + "/sourceimages"

        if self.manager.isDirect == False:

            if os.path.isdir(self.scenePath) == False:
                return
            
            fileList = os.listdir(self.scenePath)
            for p in range(0,len(fileList)):

                thisFileName, thisFileExt = os.path.splitext(fileList[p])

                existFilter = False
                for filt in self.manager.filterList:

                    if thisFileName.find(filt) == -1:
                        continue

                    existFilter = True
                    break

                if len(self.manager.filterList) == 0:
                    existFilter = True

                if existFilter == False:
                    continue

                if thisFileExt != ".mb" and thisFileExt != ".ma" :
                    continue

                self.filePathList.append(self.scenePath + "/" + thisFileName + thisFileExt)

        else:

            currentFilePath = cmds.file(q=True, sn=True)
            self.filePathList.append(currentFilePath)

        if len(self.filePathList) == 0:
            return

        self.logList.append("")
        self.logList.append("---------------------------------------")
        self.logList.append(self.id)
        self.logList.append("---------------------------------------")
        self.logList.append("")

    #===========================================
    # Check
    #===========================================
    def Check(self):

        global g_checkerProcessor

        self.Initialize()

        for p in range(0, len(self.filePathList)):

            thisFilePath = self.filePathList[p]

            print "---------------------------------------"
            print "Checking... " + os.path.basename(thisFilePath)

            if os.path.exists(thisFilePath) == False:
                self.logList.append("   " + os.path.basename(thisFilePath) + " do not exist !")
                continue

            self.logList.append("\t**************************")
            self.logList.append("\t" + os.path.basename(thisFilePath))
            self.logList.append("\t**************************")
            self.logList.append("")

            selectList = []

            if self.manager.isDirect == False:
                cmds.file(thisFilePath,f=True,options="v=0;",o=True)

                self.rootList = GetAllRootTransform(False)
                self.meshList = GetAllMeshTransform(False)

            else:

                selectList = cmds.ls(sl=True,l=True,fl=True)

                self.rootList = GetAllRootTransform(True)
                self.meshList = GetAllMeshTransform(True)

                if len(self.rootList) == 0:
                    cmds.confirmDialog(m=u"チェックしたいオブジェクトを選択してください")
                    return

            self.CheckExistFile()
            self.CheckExistNode()
            self.CheckPosition()
            self.CheckUV()
            self.CheckVertexColor()
            self.CheckSkin()
            self.CheckCleanup()

            if g_checkerProcessor != None:
                cmds.select(self.rootList,r=True)
                g_checkerProcessor.OnPostprocess()
                self.logList.extend(g_checkerProcessor.logList)

            self.logList.append("")

            if selectList == None:
                continue

            if len(selectList) == 0:
                continue

            cmds.select(selectList,r=True)

    #===========================================
    # CheckExistFile
    #===========================================
    def CheckExistFile(self):

        existModelFileResult = self.manager.CheckExistFile(self.manager.uiExistModelFile)

        if existModelFileResult != None:
            self.manager.SetResult(self.manager.uiExistModelFile, existModelFileResult[1])
            self.logList.extend(existModelFileResult[0])

        existTextureFileResult = self.manager.CheckExistFile(self.manager.uiExistTextureFile)

        if existTextureFileResult != None:
            self.manager.SetResult(self.manager.uiExistTextureFile, existTextureFileResult[1])
            self.logList.extend(existTextureFileResult[0])

    #===========================================
    # CheckExistNode
    #===========================================
    def CheckExistNode(self):
        
        existMeshResult = self.manager.CheckExistNode(self.manager.uiExistMesh, self.rootList)

        if existMeshResult != None:
            self.manager.SetResult(self.manager.uiExistMesh, existMeshResult[1])
            self.logList.extend(existMeshResult[0])

        existLocatorResult = self.manager.CheckExistNode(self.manager.uiExistLocator, self.rootList)

        if existLocatorResult != None:
            self.manager.SetResult(self.manager.uiExistLocator, existLocatorResult[1])
            self.logList.extend(existLocatorResult[0])

        existJointResult = self.manager.CheckExistNode(self.manager.uiExistJoint, self.rootList)

        if existJointResult != None:
            self.manager.SetResult(self.manager.uiExistJoint, existJointResult[1])
            self.logList.extend(existJointResult[0])

        existGroupResult = self.manager.CheckExistNode(self.manager.uiExistGroup, self.rootList)

        if existGroupResult != None:
            self.manager.SetResult(self.manager.uiExistGroup, existGroupResult[1])
            self.logList.extend(existGroupResult[0])

        existMaterialResult = self.manager.CheckExistNode(self.manager.uiExistMaterial, self.rootList)

        if existMaterialResult != None:
            self.manager.SetResult(self.manager.uiExistMaterial, existMaterialResult[1])
            self.logList.extend(existMaterialResult[0])

    #===========================================
    # CheckPosition
    #===========================================
    def CheckPosition(self):

        posGroupResult = self.manager.CheckPosition(self.manager.uiPosGroup, self.rootList)

        if posGroupResult != None:
            self.manager.SetResult(self.manager.uiPosGroup, posGroupResult[1])
            self.logList.extend(posGroupResult[0])

        posMeshResult = self.manager.CheckPosition(self.manager.uiPosMesh, self.rootList)

        if posMeshResult != None:
            self.manager.SetResult(self.manager.uiPosMesh, posMeshResult[1])
            self.logList.extend(posMeshResult[0])

        posLocatorResult = self.manager.CheckPosition(self.manager.uiPosLocator, self.rootList)

        if posLocatorResult != None:
            self.manager.SetResult(self.manager.uiPosLocator, posLocatorResult[1])
            self.logList.extend(posLocatorResult[0])

        posJointResult = self.manager.CheckPosition(self.manager.uiPosJoint, self.rootList)

        if posJointResult != None:
            self.manager.SetResult(self.manager.uiPosJoint, posJointResult[1])
            self.logList.extend(posJointResult[0])

    #===========================================
    # CheckUV
    #===========================================
    def CheckUV(self):

        uvNumResult = self.manager.CheckUVSetNum(self.meshList)

        if uvNumResult != None:
            self.manager.SetResult(self.manager.uiModelUVNum, uvNumResult[0])
            self.logList.extend(uvNumResult[1])

        uvNameResult = self.manager.CheckUVSetName(self.meshList)

        if uvNameResult != None:
            self.manager.SetResult(self.manager.uiModelUVName, uvNameResult[0])
            self.logList.extend(uvNameResult[1])

        uvRangeResult = self.manager.CheckUVSetRange(self.meshList)

        if uvRangeResult != None:
            self.manager.SetResult(self.manager.uiModelUVRange, uvRangeResult[0])
            self.logList.extend(uvRangeResult[1])

    #===========================================
    # CheckVertexColor
    #===========================================
    def CheckVertexColor(self):

        colorSetNumResult = self.manager.CheckColorSetNum(self.meshList)

        if colorSetNumResult != None:
            self.manager.SetResult(self.manager.uiVCColorSetNum, colorSetNumResult[0])
            self.logList.extend(colorSetNumResult[1])

        colorSetNameResult = self.manager.CheckColorSetName(self.meshList)

        if colorSetNameResult != None:
            self.manager.SetResult(self.manager.uiVCColorSetName, colorSetNameResult[0])
            self.logList.extend(colorSetNameResult[1])

        unsharedVertexColorResult = self.manager.CheckUnsharedVertexColor(self.meshList)

        if unsharedVertexColorResult != None:
            self.manager.SetResult(self.manager.uiVCUnshared, unsharedVertexColorResult[0])
            self.logList.extend(unsharedVertexColorResult[1])

    #===========================================
    # CheckSkin
    #===========================================
    def CheckSkin(self):

        jointFreezeResult = self.manager.CheckJointFreeze(self.rootList)

        if jointFreezeResult != None:
            self.manager.SetResult(self.manager.uiWeightJointFreeze, jointFreezeResult[0])
            self.logList.extend(jointFreezeResult[1])

        weightResult = self.manager.CheckWeight(self.meshList)

        if weightResult != None:
            
            self.manager.SetResult(self.manager.uiWeightRound, weightResult[1])
            self.manager.SetResult(self.manager.uiWeightInfluence, weightResult[2])
            
            self.logList.extend(weightResult[0])


    #===========================================
    # CheckCleanup
    #===========================================
    def CheckCleanup(self):

        cleanupResult = self.manager.CheckCleanup(self.meshList)

        if cleanupResult != None:

            self.manager.SetResult(self.manager.uiClean4Side, cleanupResult[1])
            self.manager.SetResult(self.manager.uiCleanConcave, cleanupResult[2])
            self.manager.SetResult(self.manager.uiCleanHole, cleanupResult[3])
            self.manager.SetResult(self.manager.uiCleanLamina, cleanupResult[4])
            self.manager.SetResult(self.manager.uiCleanNonmanifold, cleanupResult[5])
            self.manager.SetResult(self.manager.uiCleanZeroEdge, cleanupResult[6])
            
            self.logList.extend(cleanupResult[0])
        

    #===========================================
    # Log
    #===========================================
    def Log(self):

        self.manager.logList.extend(self.logList)

    
