# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

# -------------------------------------------------------------------------------------------
#   CyVertexPositionEditor
# -------------------------------------------------------------------------------------------

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

import CyCommon.CyUtility
import CyCommon.CyVector
import CyCommon.CySetting

from CyCommon.CyUtility import CyUtility
from CyCommon.CyVector import CyVector
from CyCommon.CySetting import CySetting

reload(CyCommon.CyUtility)
reload(CyCommon.CyVector)
reload(CyCommon.CySetting)

g_version = "0.1.0"
g_toolName = "CyVertexPositionEditor"
g_scriptPrefix = g_toolName + "."
g_uiPrefix = g_toolName + "UI_"
g_setting = None

g_vtxPositonManager = None

# **************************************************************************************************************************
#   UI関連
# **************************************************************************************************************************

# -------------------------------------------------------------------------------------------
#   メインUI
# -------------------------------------------------------------------------------------------


def UI():

    global g_toolName
    global g_scriptPrefix
    global g_uiPrefix
    global g_vtxPositonManager
    global g_setting

    cmds.selectPref(tso=True)

    if g_vtxPositonManager is None:
        g_vtxPositonManager = VertexPositionManager()

    if g_setting is None:
        g_setting = CySetting(g_toolName)

    width = 250
    height = 1
    formWidth = width - 5

    windowTitle = g_scriptPrefix.replace(".", "")
    windowName = windowTitle + "Win"

    CyUtility.CheckWindow(windowName)

    cmds.window(windowName, title=windowTitle, widthHeight=(width, height), s=1, mnb=True, mxb=False, rtf=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.frameLayout(l="Copy And Paste Vertex Position", cll=1, cl=0, bv=1, bs="etchedIn", mw=10, mh=10)
    cmds.columnLayout(adjustableColumn=True, rs=5)

    cmds.button(label="Copy Vertex Position", bgc=[0.8, 0.5, 0.5], command=g_scriptPrefix + "CopyPosition()")
    cmds.separator(style='none', h=5, w=formWidth)
    cmds.button(label="Paste Position By SelectOrder", bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + "PastePositionBySelectOrder()")
    cmds.button(label="Paste Position By Index", bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + "PastePositionByIndex()")
    cmds.button(label="Paste Position By Position", bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + "PastePositionByPosition()")

    cmds.separator(style='none', h=5, w=formWidth)

    cmds.button(label="Paste Position By Mirror X", bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + "PastePositionByMirror(0)")
    cmds.button(label="Paste Position By Mirror Y", bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + "PastePositionByMirror(1)")
    cmds.button(label="Paste Position By Mirror Z", bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + "PastePositionByMirror(2)")

    cmds.separator(style='none', h=5, w=formWidth)

    cmds.floatSliderGrp(g_uiPrefix + "PasteDistance", label='Paste Distance', field=True,
                        minValue=0.0, maxValue=1000, fmn=0.0, fmx=1000, value=5,
                        cw3=[80, 50, 0], cl3=["left", "center", "center"],
                        cc=g_scriptPrefix + "SaveSetting()")

    cmds.setParent("..")
    cmds.setParent("..")

    cmds.separator(style='in', h=15, w=formWidth)
    cmds.button(label="About", w=formWidth, command=g_scriptPrefix + "ShowAbout()")

    cmds.showWindow(windowName)

    LoadSetting()

# -------------------------------------------------------------------------------------------
#   CopyPosition
# -------------------------------------------------------------------------------------------


def CopyPosition():

    global g_vtxPositonManager

    g_vtxPositonManager.CreateInfo(True)

# -------------------------------------------------------------------------------------------
#   PastePositionByIndex
# -------------------------------------------------------------------------------------------


def PastePositionByIndex():

    global g_vtxPositonManager

    if cmds.confirmDialog(t="Confirm", m="Paste Position By Index ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_vtxPositonManager.CreateInfo()
    g_vtxPositonManager.PastePositionByIndex()

# -------------------------------------------------------------------------------------------
#   PastePositionBySelectOrder
# -------------------------------------------------------------------------------------------


def PastePositionBySelectOrder():

    global g_vtxPositonManager

    if cmds.confirmDialog(t="Confirm", m="Paste Position By SelectOrder ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_vtxPositonManager.CreateInfo()
    g_vtxPositonManager.PastePositionBySelectOrder()

# -------------------------------------------------------------------------------------------
#   PastePositionByPosition
# -------------------------------------------------------------------------------------------


def PastePositionByPosition():

    global g_vtxPositonManager

    if cmds.confirmDialog(t="Confirm", m="Paste Position By Position ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_vtxPositonManager.CreateInfo()
    g_vtxPositonManager.PastePositionByPosition()

# -------------------------------------------------------------------------------------------
#   PastePositionByMirror
# -------------------------------------------------------------------------------------------


def PastePositionByMirror(typ=0):

    global g_vtxPositonManager

    if cmds.confirmDialog(t="Confirm", m="Paste Position By Mirror ?", b=["OK", "Cancel"], db="OK", cb="Cancel", ds="Cancel", ma="center") == "Cancel":
        return

    g_vtxPositonManager.CreateInfo()

    if typ == 0:
        g_vtxPositonManager.PastePositionByMirror(True, False, False)
    elif typ == 1:
        g_vtxPositonManager.PastePositionByMirror(False, True, False)
    elif typ == 2:
        g_vtxPositonManager.PastePositionByMirror(False, False, True)

# -------------------------------------------------------------------------------------------
#   情報
# -------------------------------------------------------------------------------------------


def ShowAbout():

    global g_toolName
    global g_version

    CyUtility.ShowAbout(g_toolName, g_version, "")

# **************************************************************************************************************************
#   セーブロード関連
# **************************************************************************************************************************

# -------------------------------------------------------------------------------------------
#   ロード
# -------------------------------------------------------------------------------------------


def LoadSetting():

    global g_setting
    global g_uiPrefix

    pasteDistance = g_setting.Load("PasteDistance", "float")

    if pasteDistance != 0:
        cmds.floatSliderGrp(g_uiPrefix + "PasteDistance", e=True, v=pasteDistance)


# -------------------------------------------------------------------------------------------
#   セーブ
# -------------------------------------------------------------------------------------------


def SaveSetting():

    global g_setting
    global g_uiPrefix

    pasteDistance = cmds.floatSliderGrp(g_uiPrefix + "PasteDistance", q=True, v=True)

    g_setting.Save("PasteDistance", str(pasteDistance))

# **************************************************************************************************************************
#   クラス群
# **************************************************************************************************************************

# -------------------------------------------------------------------------------------------
#   VertexPositionManager
# -------------------------------------------------------------------------------------------


class VertexPositionManager(object):

    # ===========================================
    # __init__
    # ===========================================
    def __init__(self):

        self.targetVtxInfoList = []
        self.copyVtxInfoList = []

        self.pasteDistance = 5.0

    # ===========================================
    # GetVertexList
    # ===========================================
    def GetVertexList(self):

        selectList = CyUtility.GetSelectList()

        if len(selectList) == 0:
            return []

        vtxList = []

        for thisSel in selectList:

            cmds.select(thisSel, r=True)

            mel.eval("PolySelectConvert 3")

            thisVtxList = cmds.ls(sl=True, l=True, fl=True)

            if thisVtxList is None:
                continue

            if len(thisVtxList) == 0:
                continue

            thisVtxList.reverse()

            vtxList.extend(thisVtxList)

        cmds.select(selectList, r=True)

        selectList = None

        return vtxList

    # ===========================================
    # GetVtxInfoListFromShortMeshName
    # ===========================================
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

    # ===========================================
    # GetClosestVtxInfo
    # ===========================================
    def GetClosestVtxInfo(self, targetPosition, vtxInfoList, maxDistance=5):

        result = None
        minDistance = 10000000

        for p in range(len(vtxInfoList)):

            thisDistance = CyVector.GetSqrtDistance(targetPosition, vtxInfoList[p].position)

            if thisDistance > maxDistance:
                continue

            if thisDistance < minDistance:
                result = vtxInfoList[p]
                minDistance = thisDistance

        if result is not None:
            result = result.Clone()

        return result

    # ===========================================
    # CreateInfo
    # ===========================================
    def CreateInfo(self, useCopyList=False):

        self.GetValueFromUI()

        vtxList = self.GetVertexList()

        if len(vtxList) == 0:
            mel.eval("warning \"Cannot get target vertices!\"")
            return

        info = "Create Vertex Position Info"
        if useCopyList is True:
            info = "Copy Vertex Position"
            self.copyVtxInfoList = []
        else:
            self.targetVtxInfoList = []

        CyUtility.StartProgress(info)

        for p in range(len(vtxList)):

            if CyUtility.UpdateProgress(float(p) / float(len(vtxList)), info + "...") is False:
                CyUtility.EndProgress()
                break

            thisVertex = vtxList[p]

            thisVtxInfo = VertexInfo(thisVertex, self)

            if thisVtxInfo.shortName == "":
                continue

            if useCopyList is True:
                self.copyVtxInfoList.append(thisVtxInfo)
            else:
                self.targetVtxInfoList.append(thisVtxInfo)

        CyUtility.EndProgress()

    # ===========================================
    # GetValueFromUI
    # ===========================================
    def GetValueFromUI(self):

        global g_uiPrefix

        self.pasteDistance = cmds.floatSliderGrp(g_uiPrefix + "PasteDistance", q=True, v=True)

    # ===========================================
    # PastePositionByIndex
    # ===========================================
    def PastePositionByIndex(self):

        if len(self.copyVtxInfoList) == 0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        CyUtility.StartProgress("Paste Position By Index")

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") is False:
                CyUtility.EndProgress()
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

            if targetVtxInfo is None:
                continue

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdatePosition()

        CyUtility.EndProgress()

    # ===========================================
    # PastePositionBySelectOrder
    # ===========================================
    def PastePositionBySelectOrder(self):

        if len(self.copyVtxInfoList) == 0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        CyUtility.StartProgress("Paste Position By SelectOrder")

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") is False:
                CyUtility.EndProgress()
                break

            thisVtxInfo = self.targetVtxInfoList[p]

            tempVtxInfoList = self.GetVtxInfoListFromShortMeshName(thisVtxInfo.shortMeshName, self.copyVtxInfoList)

            if len(tempVtxInfoList) == 0:
                continue

            thisIndex = p
            if p >= len(tempVtxInfoList):
                thisIndex = len(tempVtxInfoList) - 1

            targetVtxInfo = tempVtxInfoList[thisIndex].Clone()

            if targetVtxInfo is None:
                continue

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdatePosition()

        CyUtility.EndProgress()

    # ===========================================
    # PastePositionByPosition
    # ===========================================
    def PastePositionByPosition(self):

        if len(self.copyVtxInfoList) == 0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        CyUtility.StartProgress("Pasete Position By Position")

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") is False:
                CyUtility.EndProgress()
                break

            thisVtxInfo = self.targetVtxInfoList[p]

            tempVtxInfoList = self.GetVtxInfoListFromShortMeshName(thisVtxInfo.shortMeshName, self.copyVtxInfoList)

            if len(tempVtxInfoList) == 0:
                continue

            tempVtxInfo = self.GetClosestVtxInfo(thisVtxInfo.position, tempVtxInfoList, self.pasteDistance)

            if tempVtxInfo is None:
                continue

            targetVtxInfo = tempVtxInfo.Clone()

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdatePosition()

        CyUtility.EndProgress()

    # ===========================================
    # PastePositionByMirror
    # ===========================================
    def PastePositionByMirror(self, isX, isY, isZ):

        if len(self.copyVtxInfoList) == 0:
            mel.eval("warning \"Cannot get copy vertex info!\"")
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval("warning \"Cannot get paste vertex info!\"")
            return

        CyUtility.StartProgress("Paste Position By Mirror")

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), "Pasting...") is False:
                CyUtility.EndProgress()
                break

            thisVtxInfo = self.targetVtxInfoList[p]

            tempVtxInfoList = self.GetVtxInfoListFromShortMeshName(thisVtxInfo.shortMeshName, self.copyVtxInfoList)

            if len(tempVtxInfoList) == 0:
                continue

            tempPosition = CyUtility.CopyList(thisVtxInfo.position)

            if isX is True:
                tempPosition[0] *= -1

            if isY is True:
                tempPosition[1] *= -1

            if isZ is True:
                tempPosition[2] *= -1

            tempVtxInfo = self.GetClosestVtxInfo(tempPosition, tempVtxInfoList, self.pasteDistance)

            if tempVtxInfo is None:
                continue

            targetVtxInfo = tempVtxInfo.Clone()

            if isX is True:
                targetVtxInfo.position[0] *= -1

            if isY is True:
                targetVtxInfo.position[1] *= -1

            if isZ is True:
                targetVtxInfo.position[2] *= -1

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdatePosition()

        CyUtility.EndProgress()

# -------------------------------------------------------------------------------------------
#   頂点情報クラス
# -------------------------------------------------------------------------------------------


class VertexInfo(object):

    # ===========================================
    # __init__
    # ===========================================
    def __init__(self, name="", manager=None):

        self.manager = manager

        self.name = name
        self.shortName = ""

        self.meshName = ""
        self.shortMeshName = ""

        self.index = 0

        self.position = [0, 0, 0]

        if self.name == "":
            return

        self.CreateInfo()

    # ===========================================
    # Clone
    # ===========================================
    def Clone(self):

        cloneVertexInfo = VertexInfo()

        cloneVertexInfo.manager = self.manager

        cloneVertexInfo.name = self.name
        cloneVertexInfo.shortName = self.shortName

        cloneVertexInfo.meshName = self.meshName
        cloneVertexInfo.shortMeshName = self.shortMeshName

        cloneVertexInfo.index = self.index

        cloneVertexInfo.position = CyUtility.CopyList(self.position)

        return cloneVertexInfo

    # ===========================================
    # CreateInfo
    # ===========================================
    def CreateInfo(self):

        self.name = CyUtility.GetLongName(self.name)

        if cmds.objExists(self.name) is False:
            self.name = ""
            return

        self.index = CyUtility.GetVertexIndex(self.name)

        self.shortName = CyUtility.GetShortName(self.name)

        self.meshName = CyUtility.GetMeshNameFromVertex(self.name)
        self.shortMeshName = CyUtility.GetShortName(self.meshName)

        self.position = cmds.pointPosition(self.name, w=True)

    # ===========================================
    # RewriteData
    # ===========================================
    def RewriteData(self, targetVtxInfo):

        self.position = CyUtility.CopyList(targetVtxInfo.position)

    # ===========================================
    # UpdatePosition
    # ===========================================
    def UpdatePosition(self):

        cmds.xform(self.name, ws=True, t=self.position)
