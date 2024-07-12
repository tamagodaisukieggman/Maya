# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

import maya.cmds as cmds
import maya.mel as mel

import gc
import math
import re
import sys

from imp import reload

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
    from past.utils import old_div
except Exception:
    pass

g_lr_pattern = '_L$|_l$|_R$|_r$|_L_\d*$|_l_\d*$|_R_\d*$|_r_\d*$|_L\d*$|_l\d*$|_R\d*$|_r\d*$'
g_lr_replace_string = 'XXXXXXXX'


class VertexWeightInfo(object):
    def __init__(self, name=""):
        self.name = name
        self.index = 0
        self.meshName = ""
        self.shortMeshName = ""
        self.clusterName = ""
        self.jointRootName = ""
        
        self.position = [0,0,0]
        
        self.weightInfoList = []

        if self.name == "":
            return

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):

        self.name = GetLongName(self.name)

        if cmds.objExists(self.name) == False:
            return

        self.index = GetVertexIndex(self.name)
        self.meshName = GetMeshNameFromVertex(self.name)
        self.shortMeshName = RemoveNamespace(GetShortName(self.meshName))
        
        meshNameForCluster = GetNameForSkinCluster(self.meshName)
        self.clusterName=mel.eval("findRelatedSkinCluster "+meshNameForCluster)

        if self.clusterName=="":
            return

        jointList=cmds.skinPercent(self.clusterName,self.name, query=True, t=None )
        weightList = cmds.skinPercent(self.clusterName,self.name, query=True, value=True )

        if len(jointList) == 0:
            return

        if len(jointList) != len(weightList):
            return

        self.jointRootName = GetRootName(jointList[0])

        for i in range(len(jointList)):

            if weightList[i] == 0:
                continue

            newWeightInfo = WeightInfo(jointList[i],weightList[i])

            self.weightInfoList.append(newWeightInfo)

        self.SortWeightInfo()

        #Position
        self.position = cmds.pointPosition(self.name,w=True)

        jointList = None
        weightList = None

    #===========================================
    # SortWeightInfo
    #===========================================
    def SortWeightInfo(self):

        newWeightInfoList = []

        while len(self.weightInfoList) != 0:

            weightInfo = self.GetMinWeightInfo()

            self.weightInfoList.remove(weightInfo)
            newWeightInfoList.append(weightInfo)

        self.weightInfoList =[]
        for i in range(len(newWeightInfoList)):
            self.weightInfoList.append(newWeightInfoList[len(newWeightInfoList) - 1 - i])

        newWeightInfoList = None

    #===========================================
    # GetMinWeightInfo
    #===========================================
    def GetMinWeightInfo(self):

        result = self.weightInfoList[0]
        minWeight = 10000
        for weightInfo in self.weightInfoList:

            if weightInfo.weight < minWeight:
                result = weightInfo
                minWeight = weightInfo.weight

        return result

    #===========================================
    # SetMaxInfluence
    #===========================================
    def SetMaxInfluence(self,n):

        self.SortWeightInfo()

        print('self.weightInfoList', self.weightInfoList)
        print('self.weightInfoList[i].weight', self.weightInfoList[0].weight)

        restWeight = 0
        for i in range(len(self.weightInfoList)):

            if i < n:
                continue

            restWeight += self.weightInfoList[i].weight
            self.weightInfoList[i].weight = 0

        weightSum = 0
        for weight in self.weightInfoList:
            weightSum += weight.weight

        for weight in self.weightInfoList:
            if sys.version_info.major == 2:
                weight.weight += restWeight * weight.weight / weightSum
            else:
                # for Maya 2022-
                weight.weight += old_div(restWeight * weight.weight, weightSum)

        self.NormalizeWeight(0)

        self.UpdateWeight()

    def NormalizeWeight(self, typ):

        weightSum = 0

        for weightInfo in self.weightInfoList:
            
            weightSum += weightInfo.weight

        weightDef = weightSum - 1.0;

        if typ == 0:
            
            for weightInfo in self.weightInfoList:

                weightInfo.weight /= weightSum

        elif typ == 1:

            for weightInfo in self.weightInfoList:

                if weightInfo.weight <= 0:
                    continue

                weightInfo.weight -= weightDef
                break

    #===========================================
    # UpdateWeight
    #===========================================
    def UpdateWeight(self):

        self.FixJointName()

        self.FixWeight()

        transformValue = self.CreateTransformValue()

        try:
            cmds.skinPercent(self.clusterName,self.name,tv=transformValue,nrm=True)
        except:
            test = 0

        transformValue = None

    #===========================================
    # FixJointName
    #===========================================
    def FixJointName(self):

        for weightInfo in self.weightInfoList:

            targetJointNameList = cmds.ls(weightInfo.jointInfo.shortName,l=True,fl=True)

            for jointName in targetJointNameList:

                jointRootName = GetRootName(jointName)

                if self.jointRootName == jointRootName:
                    weightInfo.jointInfo = JointInfo(jointName)
                    break

    #===========================================
    # FixWeight
    #===========================================
    def FixWeight(self):

        weightSum = 0

        for weightInfo in self.weightInfoList:
            
            weightSum += weightInfo.weight

        weightDef = weightSum - 1.0;

        if weightDef == 0:
            return

        for weightInfo in self.weightInfoList:

            if weightInfo.weight <= 0:
                continue

            if weightInfo.weight <= weightDef:
                continue

            weightInfo.weight -= weightDef
            break

    #===========================================
    # CreateTransformValue
    #===========================================
    def CreateTransformValue(self):
     
        transformValue=[]

        for weightInfo in self.weightInfoList:
            
            transformValue.append((weightInfo.jointInfo.name,weightInfo.weight))
     
        return transformValue

    #===========================================
    # Delete
    #===========================================
    def Delete(self):

        for weightInfo in self.weightInfoList:

            weightInfo.Delete()

            weight = None


#-------------------------------------------------------------------------------------------
#   ウェイト情報クラス
#-------------------------------------------------------------------------------------------
class WeightInfo(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self, jointName="", weight=0):

        self.jointInfo = JointInfo(jointName)
        self.weight = weight

    #===========================================
    # Clone
    #===========================================
    def Clone(self):

        cloneWeightInfo = WeightInfo()

        cloneWeightInfo.jointInfo = self.jointInfo.Clone()
        cloneWeightInfo.weight = self.weight

        return cloneWeightInfo

    #===========================================
    # ExistRoundWeight
    #===========================================
    def ExistRoundWeight(self,n):

        tempFullValue = self.weight * pow(10,n)
        tempValue = math.modf(tempFullValue);

        if tempValue[0] < 0.01 or tempValue[0] > 0.99:
            return False

        return True

    #===========================================
    # Round
    #===========================================
    def Round(self,n):

        self.weight = round(self.weight,n)
        
    #===========================================
    # Delete
    #===========================================
    def Delete(self):

        self.jointInfo = None

#-------------------------------------------------------------------------------------------
#   ジョイント情報クラス
#-------------------------------------------------------------------------------------------
class JointInfo(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self, name=""):
        
        self.name = name        
        self.shortName = ""
        self.removeLRName = ""
        self.lrSuffix = ""
        self.position = [0,0,0]

        if self.name == "":
            return

        self.CreateInfo()

    #===========================================
    # Clone
    #===========================================
    def Clone(self):

        cloneJointInfo = JointInfo()

        cloneJointInfo.name = self.name
        cloneJointInfo.shortName = self.shortName
        cloneJointInfo.removeLRName = self.removeLRName
        cloneJointInfo.lrSuffix = self.lrSuffix
        cloneJointInfo.position = CopyPosition(self.position)

        return cloneJointInfo

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):

        self.name = GetLongName(self.name)

        if cmds.objExists(self.name) == False:
            return

        self.shortName = RemoveNamespace(GetShortName(self.name))
        self.removeLRName, self.lrSuffix = GetRemoveLRName(self.shortName)
        
        self.position = cmds.xform(self.name,q=True,ws=True,t=True)

    #===========================================
    # Delete
    #===========================================
    def Delete(self):

        self.name = None
        self.shortName = None
        self.removeLRName = None
        self.position = None


#-------------------------------------------------------------------------------------------
#   GetShortName
#-------------------------------------------------------------------------------------------
def GetShortName(name):

    longName = GetLongName(name)

    if longName == "":
        return ""

    if longName.find("|") == -1:
        return longName

    splitStr = longName.split("|")

    return splitStr[len(splitStr) - 1]

#-------------------------------------------------------------------------------------------
#   GetLongName
#-------------------------------------------------------------------------------------------
def GetLongName(name):

    longName = cmds.ls(name,l=True)

    if longName == None:
        return ""

    if len(longName) == 0:
        return ""

    return longName[0]

#-------------------------------------------------------------------------------------------
#   頂点番号取得
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
#   頂点からメッシュ取得
#-------------------------------------------------------------------------------------------
def GetMeshNameFromVertex(vertexName):

    if vertexName.find(".") == -1:
        return vertexName

    meshName=vertexName.split(".")[0]
        
    return meshName

#-------------------------------------------------------------------------------------------
#   GetRootName
#-------------------------------------------------------------------------------------------
def GetRootName(name):

    longName = GetLongName(name)

    if longName == "":
        return ""

    if longName.find("|") == -1:
        return longName

    splitStr = longName.split("|")

    return splitStr[1]

#-------------------------------------------------------------------------------------------
#   RemoveNamespace
#-------------------------------------------------------------------------------------------
def RemoveNamespace(name):

    if name.find("|") == -1:
        return RemoveNamespaceBase(name)

    splitStrList = name.split("|")
    resultName = ""
    for p in range(0,len(splitStrList)):
        
        fixName = RemoveNamespaceBase(splitStrList[p])

        resultName += fixName

        if p == len(splitStrList) - 1:
            continue

        resultName += "|"

    return resultName

#-------------------------------------------------------------------------------------------
#   RemoveNamespace
#-------------------------------------------------------------------------------------------
def RemoveNamespaceBase(name):

    if name.find(":") == -1:
        return name

    splitStr = name.split(":")

    return splitStr[len(splitStr) - 1]

#-------------------------------------------------------------------------------------------
#   メッシュ名からスキンクラスタ用の名前取得
#-------------------------------------------------------------------------------------------
def GetNameForSkinCluster(meshName):
     
    result=meshName
 
    split=meshName.split("|")
 
    if meshName[0]=="|" and len(split)>2:
        result=meshName.replace("|","",1)
 
    return result

#-------------------------------------------------------------------------------------------
#   CopyPosition
#-------------------------------------------------------------------------------------------
def CopyPosition(value):

    result = [value[0],value[1],value[2]]

    return result

#-------------------------------------------------------------------------------------------
#   GetRemoveLRName
#-------------------------------------------------------------------------------------------
def GetRemoveLRName(name):

    global g_lr_pattern
    global g_lr_replace_string

    match_obj = re.search(g_lr_pattern, name)

    if match_obj is None:
        return name, ''

    replace_string = match_obj.group()
    replace_name = re.sub(g_lr_pattern, g_lr_replace_string, name)

    return replace_name, replace_string

#-------------------------------------------------------------------------------------------
#   最大影響範囲設定
#-------------------------------------------------------------------------------------------
def SetMaxInfluence(influenceNum):

    global g_uiPrefix
    global g_weightManager

    # if cmds.confirmDialog(t="Confirm", m="Set max influence ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
    #     return

    # influenceNum = cmds.intSliderGrp(g_uiPrefix + "InfluenceNum",q=True,v=True)

    sel = cmds.ls(os=True)

    vwi = VertexWeightInfo(sel[0])

    vwi.CreateInfo()
    vwi.SetMaxInfluence(influenceNum)
    vwi.Delete()

    gc.collect()
