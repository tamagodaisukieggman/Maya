# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   TkgNormalEditor
#-------------------------------------------------------------------------------------------


try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel
import math

import TkgCommon.TkgUtility


from TkgCommon.TkgUtility import TkgUtility
from TkgCommon.TkgSetting import TkgSetting

reload(TkgCommon.TkgUtility)
reload(TkgCommon.TkgSetting)

g_version = "0.1.0"
g_toolName = "TkgNormalEditor"
g_scriptPrefix= g_toolName + "."
g_uiPrefix= g_toolName + "UI_"
g_setting = None

g_normalManager = None

#**************************************************************************************************************************
#   UI関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   メインUI
#-------------------------------------------------------------------------------------------
def UI():

    global g_toolName
    global g_scriptPrefix
    global g_uiPrefix
    global g_normalManager
    global g_setting

    cmds.selectPref(tso=True)

    if g_normalManager == None:
        g_normalManager = NormalManager()

    if g_setting == None:
        g_setting = TkgSetting(g_toolName)

    width=250
    height=1
    formWidth=width-5

    windowTitle=g_scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"

    TkgUtility.CheckWindow(windowName)

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=1,mnb=True,mxb=False,rtf=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.frameLayout(l="Copy And Paste Normal",cll=1,cl=0,bv=1,bs="etchedIn",mw=10,mh=10)
    cmds.columnLayout(adjustableColumn = True, rs=5)

    cmds.button( label="Copy Normal",bgc=[0.8,0.5,0.5],command=g_scriptPrefix+"CopyNormal()")
    cmds.button( label="Copy Normal From Edge Direction",bgc=[0.8,0.5,0.5],command=g_scriptPrefix+"CopyNormalFromEdgeDirection()")
    cmds.separator( style='none',h=5,w=formWidth)
    cmds.button( label="Paste Normal By SelectOrder",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteNormalBySelectOrder()")
    cmds.button( label="Paste Normal By Index",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteNormalByIndex()")
    cmds.button( label="Paste Normal By Position",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PaseteNormalByPosition()")

    cmds.separator( style='none',h=5,w=formWidth)

    cmds.button( label="Paste Normal By Mirror X",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteNormalByMirror(0)")
    cmds.button( label="Paste Normal By Mirror Y",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteNormalByMirror(1)")
    cmds.button( label="Paste Normal By Mirror Z",bgc=[0.8,0.8,0.5],command=g_scriptPrefix+"PasteNormalByMirror(2)")

    cmds.separator( style='none',h=5,w=formWidth)

    cmds.floatSliderGrp(g_uiPrefix + "PasteDistance", label='Paste Distance', field=True, minValue=0.0, maxValue=1000, fmn=0.0, fmx=1000, value=5, cw3=[80,50,0], cl3=["left","center","center"], cc=g_scriptPrefix+"SaveSetting()")
    cmds.checkBox(g_uiPrefix + "InvertNormal", label="Invert normal", v=False, cc=g_scriptPrefix+"SaveSetting()")
 
    cmds.setParent( ".." )
    cmds.setParent( ".." )

    cmds.separator( style='in',h=15,w=formWidth)
    cmds.button( label="About",w=formWidth,command=g_scriptPrefix + "ShowAbout()")
 
    cmds.showWindow(windowName)

    LoadSetting()

#-------------------------------------------------------------------------------------------
#   CopyNormal
#-------------------------------------------------------------------------------------------
def CopyNormal():

    global g_normalManager

    g_normalManager.CreateInfo(True)

#-------------------------------------------------------------------------------------------
#   CopyNormalFromEdgeDirection
#-------------------------------------------------------------------------------------------
def CopyNormalFromEdgeDirection():

    global g_normalManager

    g_normalManager.CreateInfoFromEdgeDirection()

#-------------------------------------------------------------------------------------------
#   PasteWeightByIndex
#-------------------------------------------------------------------------------------------
def PasteNormalByIndex():

    global g_normalManager

    if cmds.confirmDialog(t="Confirm", m="Paste Weight By Index ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_normalManager.CreateInfo()
    g_normalManager.PasteNormalByIndex()

#-------------------------------------------------------------------------------------------
#   PasteNormalBySelectOrder
#-------------------------------------------------------------------------------------------
def PasteNormalBySelectOrder():

    global g_normalManager

    if cmds.confirmDialog(t="Confirm", m="Paste Weight By SelectOrder ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_normalManager.CreateInfo()
    g_normalManager.PasteNormalBySelectOrder()

#-------------------------------------------------------------------------------------------
#   PasteWeightByPosition
#-------------------------------------------------------------------------------------------
def PaseteNormalByPosition():

    global g_normalManager

    if cmds.confirmDialog(t="Confirm", m="Paste Weight By Position ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_normalManager.CreateInfo()
    g_normalManager.PaseteNormalByPosition()

#-------------------------------------------------------------------------------------------
#   PasteNormalByMirror
#-------------------------------------------------------------------------------------------
def PasteNormalByMirror(typ = 0):

    global g_normalManager

    if cmds.confirmDialog(t="Confirm",m="Paste Weight By Mirror ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_normalManager.CreateInfo()

    if typ == 0:
        g_normalManager.PasteNormalByMirror(True,False,False)
    elif typ == 1:
        g_normalManager.PasteNormalByMirror(False,True,False)
    elif typ == 2:
        g_normalManager.PasteNormalByMirror(False,False,True)



#-------------------------------------------------------------------------------------------
#   情報
#-------------------------------------------------------------------------------------------
def ShowAbout():

    global g_toolName
    global g_version

    TkgUtility.ShowAbout(g_toolName, g_version, "")

#**************************************************************************************************************************
#   セーブロード関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   ロード
#-------------------------------------------------------------------------------------------
def LoadSetting():

    global g_setting
    global g_uiPrefix

    pasteDistance = g_setting.Load("PasteDistance","float")
    invertNormal = g_setting.Load("InvertNormal","bool")

    if pasteDistance != 0:
        cmds.floatSliderGrp(g_uiPrefix + "PasteDistance",e=True,v=pasteDistance)

    cmds.checkBox(g_uiPrefix + "InvertNormal",e=True,v=invertNormal)

#-------------------------------------------------------------------------------------------
#   セーブ
#-------------------------------------------------------------------------------------------
def SaveSetting():

    global g_setting
    global g_uiPrefix

    pasteDistance = cmds.floatSliderGrp(g_uiPrefix + "PasteDistance",q=True,v=True)
    invertNormal = cmds.checkBox(g_uiPrefix + "InvertNormal",q=True,v=True)

    g_setting.Save("PasteDistance", str(pasteDistance))
    g_setting.Save("InvertNormal", str(invertNormal))

#**************************************************************************************************************************
#   ユーティリティ関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   GetSelectList
#-------------------------------------------------------------------------------------------
def GetSelectList():

    selectList=[]
    
    selectList=cmds.ls(os=True,l=True,fl=True)

    if selectList != None:
        if len(selectList) != 0:
            return selectList

    selectList=cmds.ls(sl=True,l=True,fl=True)

    if selectList == None:
        return []

    if len(selectList) == 0:
        return []

    return selectList

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
#   頂点からメッシュ取得
#-------------------------------------------------------------------------------------------
def GetMeshNameFromVertex(vertexName):

    if vertexName.find(".") == -1:
        return vertexName

    meshName=vertexName.split(".")[0]
        
    return meshName

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
#   頂点フェース番号取得
#-------------------------------------------------------------------------------------------
def GetVertexFaceIndex(vertexFaceName):

    if vertexFaceName.rfind("[") == -1:
        return

    if vertexFaceName.rfind("]") == -1:
        return

    startIndex = vertexFaceName.rfind("[") + 1
    endIndex = vertexFaceName.rfind("]")

    return int(vertexFaceName[startIndex:endIndex])

#-------------------------------------------------------------------------------------------
#   GetDistance
#-------------------------------------------------------------------------------------------
def GetDistance(value0, value1):

    if len(value0) != len(value1):
        return 10000000

    result = 0
    for p in range(len(value0)):

        result += (value1[p] - value0[p]) * (value1[p] - value0[p])

    return result

#-------------------------------------------------------------------------------------------
#   CopyPosition
#-------------------------------------------------------------------------------------------
def CopyPosition(value):

    result = [value[0],value[1],value[2]]

    return result

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
#   SetSoftEdge
#-------------------------------------------------------------------------------------------
def SetSoftEdge(target):

    selectList = cmds.ls(sl=True,l=True)

    cmds.polySoftEdge(target, a=180, ch=0)

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    cmds.select(selectList,r=True)

#**************************************************************************************************************************
#   プログレスバー関連
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   プログレスバー開始
#-------------------------------------------------------------------------------------------
def StartProgress(titleName):

    cmds.progressWindow(title=titleName,status="",isInterruptable=True, min=0, max=100 )

#-------------------------------------------------------------------------------------------
#   プログレスバー更新
#-------------------------------------------------------------------------------------------
def UpdateProgress(amount,info):

    cmds.progressWindow( edit=True, progress=amount * 100.0, status=info )

    if cmds.progressWindow( query=True, isCancelled=True ) == True:
        return False

    return True

#-------------------------------------------------------------------------------------------
#   プログレスバー終了
#-------------------------------------------------------------------------------------------
def EndProgress():

    cmds.progressWindow(endProgress=1)

#**************************************************************************************************************************
#   クラス群
#**************************************************************************************************************************

#-------------------------------------------------------------------------------------------
#   メッシュウェイト情報クラス
#-------------------------------------------------------------------------------------------
class NormalManager(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self):

        self.targetVtxInfoList = []
        self.copyVtxInfoList = []

        self.pasteDistance = 5.0
        self.invertNormal = False

    #===========================================
    # GetVertexList
    #===========================================
    def GetVertexList(self):

        selectList=GetSelectList()

        if len(selectList) == 0:
            return []

        vtxList=[]

        for thisSel in selectList:
            
            cmds.select(thisSel, r=True)

            mel.eval("PolySelectConvert 3")

            thisVtxList = cmds.ls(sl=True,l=True,fl=True)

            if thisVtxList == None:
                continue

            if len(thisVtxList) == 0:
                continue

            thisVtxList.reverse()

            vtxList.extend(thisVtxList)
        
        cmds.select(selectList, r=True)

        selectList = None

        return vtxList

    #===========================================
    # GetVtxInfoListFromShortMeshName
    #===========================================
    def GetVtxInfoListFromShortMeshName(self, shortMeshName, vtxInfoList):

        result = []

        for p in range(len(vtxInfoList)):

            tempVtxInfo = vtxInfoList[p]
            
            if shortMeshName != tempVtxInfo.shortMeshName:
                continue

            result.append(tempVtxInfo)

        if len(result) == 0:
            return vtxInfoList

        return result

    #===========================================
    # GetClosestVtxInfo
    #===========================================
    def GetClosestVtxInfo(self, targetPosition, vtxInfoList, maxDistance = 5):

        result = None
        minDistance = 10000000

        for p in range(len(vtxInfoList)):

            thisDistance = GetDistance(targetPosition, vtxInfoList[p].position)

            if thisDistance > maxDistance:
                continue

            if thisDistance < minDistance:
                result = vtxInfoList[p]
                minDistance = thisDistance

        if result != None:
            result = result.Clone()

        return result

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self, useCopyList=False):

        self.GetValueFromUI()

        vtxList = self.GetVertexList()

        if len(vtxList)==0:
            mel.eval("warning \"Cannot get target vertices!\"")
            return

        info = "Create Normal Info"
        if useCopyList == True:
            info = "Copy Normal"
            self.copyVtxInfoList = []
        else:
            self.targetVtxInfoList = []

        StartProgress(info)

        for p in range(len(vtxList)):

            if UpdateProgress(float(p) / float(len(vtxList)), info + "...") == False:
                EndProgress()
                break

            thisVertex = vtxList[p]
            
            thisVtxInfo = VertexInfo(thisVertex, self)

            if thisVtxInfo.shortName == "":
                continue

            if useCopyList == True:
                self.copyVtxInfoList.append(thisVtxInfo)
            else:
                self.targetVtxInfoList.append(thisVtxInfo)

        EndProgress()

    #===========================================
    # CreateInfoFromEdgeDirection
    #===========================================
    def CreateInfoFromEdgeDirection(self):

        self.CreateInfo(True)

        if len(self.copyVtxInfoList)==0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return
        
        newVtxInfoList = []

        copyVtxInfoListLength = len(self.copyVtxInfoList)

        maxLength = 0

        if(copyVtxInfoListLength%2 == 0):
            maxLength = int(copyVtxInfoListLength * 0.5)
        else:
            maxLength = int(math.floor(copyVtxInfoListLength * 0.5))

        for p in range(0,maxLength):

            startVtxInfo = self.copyVtxInfoList[2*p]
            endVtxInfo = self.copyVtxInfoList[2*p+1]

            thisDirection = [0,0,0]
            thisDirection[0] = endVtxInfo.position[0] - startVtxInfo.position[0]
            thisDirection[1] = endVtxInfo.position[1] - startVtxInfo.position[1]
            thisDirection[2] = endVtxInfo.position[2] - startVtxInfo.position[2]

            thisLength = thisDirection[0] * thisDirection[0] + thisDirection[1] * thisDirection[1] + thisDirection[2] * thisDirection[2]
            thisLength = math.sqrt(thisLength)

            thisDirection[0] /= thisLength
            thisDirection[1] /= thisLength
            thisDirection[2] /= thisLength

            thisPosition = [0,0,0]
            thisPosition[0] = (endVtxInfo.position[0] + startVtxInfo.position[0]) * 0.5
            thisPosition[1] = (endVtxInfo.position[1] + startVtxInfo.position[1]) * 0.5
            thisPosition[2] = (endVtxInfo.position[2] + startVtxInfo.position[2]) * 0.5

            newVtxInfo = endVtxInfo.Clone()

            newVtxInfo.position = thisPosition

            newVtxInfo.baseNormal = thisDirection
            newVtxInfo.sameNormal = True

            newVtxInfo.baseFreeze = True
            newVtxInfo.sameFreeze = True

            newVtxInfoList.append(newVtxInfo)

        self.copyVtxInfoList = newVtxInfoList

    #===========================================
    # GetValueFromUI
    #===========================================
    def GetValueFromUI(self):

        global g_uiPrefix

        self.pasteDistance = cmds.floatSliderGrp(g_uiPrefix + "PasteDistance",q=True,v=True)
        self.invertNormal = cmds.checkBox(g_uiPrefix + "InvertNormal",q=True,v=True)

    #===========================================
    # PasteNormalByIndex
    #===========================================
    def PasteNormalByIndex(self):

        if len(self.copyVtxInfoList)==0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList)==0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        StartProgress("Paste Normal By Index")

        for p in range(len(self.targetVtxInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxInfo = self.targetVtxInfoList[p]

            tempVtxInfoList = self.GetVtxInfoListFromShortMeshName(thisVtxInfo.shortMeshName, self.copyVtxInfoList)
            
            if len(tempVtxInfoList) == 0:
                continue

            targetVtxInfo = None
            for q in range(len(tempVtxInfoList)):

                tempVtxInfo = tempVtxInfoList[q]
                
                if thisVtxInfo.index != tempVtxInfo.index:
                    continue

                targetVtxInfo = tempVtxInfo.Clone()                
                break
            
            if targetVtxInfo == None:
                continue

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdateNormal()

        EndProgress()

    #===========================================
    # PasteNormalBySelectOrder
    #===========================================
    def PasteNormalBySelectOrder(self):

        if len(self.copyVtxInfoList)==0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList)==0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        StartProgress("Paste Normal By SelectOrder")

        for p in range(len(self.targetVtxInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxInfo = self.targetVtxInfoList[p]

            tempVtxInfoList = self.GetVtxInfoListFromShortMeshName(thisVtxInfo.shortMeshName, self.copyVtxInfoList)
            
            if len(tempVtxInfoList) == 0:
                continue

            thisIndex = p
            if p >= len(tempVtxInfoList):
                thisIndex = len(tempVtxInfoList) - 1

            targetVtxInfo = tempVtxInfoList[thisIndex].Clone()
            
            if targetVtxInfo == None:
                continue

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdateNormal()

        EndProgress()

    #===========================================
    # PaseteNormalByPosition
    #===========================================
    def PaseteNormalByPosition(self):

        if len(self.copyVtxInfoList)==0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList)==0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        StartProgress("Pasete Weight By Position")

        for p in range(len(self.targetVtxInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxInfo = self.targetVtxInfoList[p]

            tempVtxInfoList = self.GetVtxInfoListFromShortMeshName(thisVtxInfo.shortMeshName, self.copyVtxInfoList)
            
            if len(tempVtxInfoList) == 0:
                continue

            tempVtxInfo = self.GetClosestVtxInfo(thisVtxInfo.position, tempVtxInfoList, self.pasteDistance)

            if tempVtxInfo == None:
                continue

            targetVtxInfo = tempVtxInfo.Clone()

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdateNormal()

        EndProgress()

    #===========================================
    # PasteNormalByMirror
    #===========================================
    def PasteNormalByMirror(self, isX, isY, isZ):

        if len(self.copyVtxInfoList)==0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList)==0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        StartProgress("Paste Normal By Mirror")

        for p in range(len(self.targetVtxInfoList)):

            if UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") == False:
                EndProgress()
                break

            thisVtxInfo = self.targetVtxInfoList[p]

            tempVtxInfoList = self.GetVtxInfoListFromShortMeshName(thisVtxInfo.shortMeshName, self.copyVtxInfoList)
            
            if len(tempVtxInfoList) == 0:
                continue

            tempPosition = CopyPosition(thisVtxInfo.position)

            if isX == True:
                tempPosition[0] *= -1

            if isY == True:
                tempPosition[1] *= -1

            if isZ == True:
                tempPosition[2] *= -1

            tempVtxInfo = self.GetClosestVtxInfo(tempPosition, tempVtxInfoList, self.pasteDistance)

            if tempVtxInfo == None:
                continue

            targetVtxInfo = tempVtxInfo.Clone()

            if isX == True:
                targetVtxInfo.baseNormal[0] *= -1

            if isY == True:
                targetVtxInfo.baseNormal[1] *= -1

            if isZ == True:
                targetVtxInfo.baseNormal[2] *= -1

            for p in range(len(targetVtxInfo.vtxFaceInfoList)):

                thisVtxFaceInfo = targetVtxInfo.vtxFaceInfoList[p]

                if isX == True:
                    thisVtxFaceInfo.normal[0] *= -1

                if isY == True:
                    thisVtxFaceInfo.normal[1] *= -1

                if isZ == True:
                    thisVtxFaceInfo.normal[2] *= -1

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdateNormal()

        EndProgress()

#-------------------------------------------------------------------------------------------
#   頂点情報クラス
#-------------------------------------------------------------------------------------------
class VertexInfo(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self, name="", manager=None):

        self.manager = manager

        self.name = name        
        self.shortName = ""

        self.meshName = ""
        self.shortMeshName = ""

        self.index = 0

        self.position = [0,0,0]

        self.baseNormal = [0,0,0]
        self.sameNormal = True

        self.baseFreeze = False
        self.sameFreeze = True

        self.vtxFaceInfoList = []

        if self.name == "":
            return

        self.CreateInfo()

    #===========================================
    # Clone
    #===========================================
    def Clone(self):

        cloneVertexInfo = VertexInfo()

        cloneVertexInfo.manager = self.manager

        cloneVertexInfo.name = self.name
        cloneVertexInfo.shortName = self.shortName

        cloneVertexInfo.meshName = self.meshName
        cloneVertexInfo.shortMeshName = self.shortMeshName

        cloneVertexInfo.index = self.index
        
        cloneVertexInfo.position = CopyPosition(self.position)

        cloneVertexInfo.baseNormal = CopyPosition(self.baseNormal)
        cloneVertexInfo.sameNormal = self.sameNormal
        
        cloneVertexInfo.baseFreeze = self.baseFreeze
        cloneVertexInfo.sameFreeze = self.sameFreeze

        cloneVertexInfo.vtxFaceInfoList = []
        for p in range(len(self.vtxFaceInfoList)):

            cloneVertexInfo.vtxFaceInfoList.append(self.vtxFaceInfoList[p].Clone(cloneVertexInfo))

        return cloneVertexInfo

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):

        self.name = GetLongName(self.name)

        if cmds.objExists(self.name) == False:
            return

        self.index = GetVertexIndex(self.name)

        self.shortName = GetShortName(self.name)

        self.meshName = GetMeshNameFromVertex(self.name)
        self.shortMeshName = GetShortName(self.meshName)
        
        self.position = cmds.pointPosition(self.name,w=True)

        #VertexFace
        tempStr = self.name.replace("vtx[","vtxFace[")
        tempStr += "[*]"

        vtxFaceList = cmds.ls(tempStr,fl=True,l=True)

        self.vtxFaceList = []
        for p in range(len(vtxFaceList)):

            vtxFaceInfo = VertexFaceInfo(vtxFaceList[p], self)

            if vtxFaceInfo.shortName == "":
                continue

            self.vtxFaceInfoList.append(vtxFaceInfo)

        if len(self.vtxFaceInfoList) == 0:
            return

        self.baseNormal = self.vtxFaceInfoList[0].normal
        self.baseFreeze = self.vtxFaceInfoList[0].freeze
        self.sameNormal = True
        self.sameFreeze = True

        for p in range(0, len(self.vtxFaceInfoList)):

            thisVtxInfo = self.vtxFaceInfoList[p]

            if SameVector(self.baseNormal, thisVtxInfo.normal) == False:
                self.sameNormal = False
                break

        for p in range(0, len(self.vtxFaceInfoList)):

            thisVtxInfo = self.vtxFaceInfoList[p]

            if thisVtxInfo.freeze != self.baseFreeze:
                self.sameFreeze = False
                break

    #===========================================
    # RewriteNormal
    #===========================================
    def RewriteNormal(self, newVtxFaceInfoList):

        if len(newVtxFaceInfoList) == 0:
            return

        for p in range(len(self.vtxFaceInfoList)):

            thisIndex = p
            if p >= len(newVtxFaceInfoList):
                thisIndex = len(newVtxFaceInfoList) - 1

            self.vtxFaceInfoList[p].normal = CopyPosition(newVtxFaceInfoList[thisIndex].normal)

    #===========================================
    # RewriteData
    #===========================================
    def RewriteData(self, targetVtxInfo):

        self.baseNormal = CopyPosition(targetVtxInfo.baseNormal)
        self.sameNormal = targetVtxInfo.sameNormal
        
        self.baseFreeze = targetVtxInfo.baseFreeze
        self.sameFreeze = targetVtxInfo.sameFreeze

        for p in range(len(self.vtxFaceInfoList)):

            thisIndex = p
            if p >= len(targetVtxInfo.vtxFaceInfoList):
                thisIndex = len(targetVtxInfo.vtxFaceInfoList) - 1

            self.vtxFaceInfoList[p].normal = CopyPosition(targetVtxInfo.vtxFaceInfoList[thisIndex].normal)
            self.vtxFaceInfoList[p].freeze = targetVtxInfo.vtxFaceInfoList[thisIndex].freeze

    #===========================================
    # UpdateNormal
    #===========================================
    def UpdateNormal(self):

        if self.sameNormal == False:
            for p in range(len(self.vtxFaceInfoList)):
                self.vtxFaceInfoList[p].UpdateNormal()
        else:
            if self.manager.invertNormal == False:
                cmds.polyNormalPerVertex(self.name,e=True,x=self.baseNormal[0],y=self.baseNormal[1],z=self.baseNormal[2])
            else:
                cmds.polyNormalPerVertex(self.name,e=True,x=-self.baseNormal[0],y=-self.baseNormal[1],z=-self.baseNormal[2])

            SetSoftEdge(self.name)

        if self.sameFreeze == False or self.sameNormal == False:
            for p in range(len(self.vtxFaceInfoList)):
                self.vtxFaceInfoList[p].UpdateFreeze()
        else:
            if self.baseFreeze == False:
                cmds.polyNormalPerVertex(self.name,e=True,ufn=True)
            
        
#-------------------------------------------------------------------------------------------
#   頂点フェース情報クラス
#-------------------------------------------------------------------------------------------
class VertexFaceInfo(object):

    #===========================================
    # __init__
    #===========================================
    def __init__(self, name="", vertexInfo = None):

        self.vertexInfo = vertexInfo

        self.name = name
        self.shortName = ""

        self.index = 0

        self.normal = [0,0,0]

        self.freeze = False
        
        if self.name == "":
            return

        self.CreateInfo()

    #===========================================
    # Clone
    #===========================================
    def Clone(self, newVertexInfo):

        cloneVertexFaceInfo = VertexFaceInfo()

        cloneVertexFaceInfo.vertexInfo = newVertexInfo

        cloneVertexFaceInfo.name = self.name
        cloneVertexFaceInfo.shortName = self.shortName

        cloneVertexFaceInfo.index = self.index
        
        cloneVertexFaceInfo.normal = CopyPosition(self.normal)

        cloneVertexFaceInfo.freeze = self.freeze

        return cloneVertexFaceInfo

    #===========================================
    # CreateInfo
    #===========================================
    def CreateInfo(self):

        self.name = GetLongName(self.name)

        if cmds.objExists(self.name) == False:
            return

        self.index = GetVertexFaceIndex(self.name)

        self.shortName = GetShortName(self.name)

        self.normal = cmds.polyNormalPerVertex(self.name,q=True,x=True,y=True,z=True)

        self.freeze = cmds.polyNormalPerVertex(self.name,q=True,fn=True)[0]

    #===========================================
    # UpdateNormal
    #===========================================
    def UpdateNormal(self):

        if self.vertexInfo.manager.invertNormal == False:
            cmds.polyNormalPerVertex(self.name,e=True,x=self.normal[0],y=self.normal[1],z=self.normal[2])
        else:
            cmds.polyNormalPerVertex(self.name,e=True,x=-self.normal[0],y=-self.normal[1],z=-self.normal[2])

    #===========================================
    # UpdateFreeze
    #===========================================
    def UpdateFreeze(self):

        if self.freeze == False:
            cmds.polyNormalPerVertex(self.name,e=True,ufn=True)

        
