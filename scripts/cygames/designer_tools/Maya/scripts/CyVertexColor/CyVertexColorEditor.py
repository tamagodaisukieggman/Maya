# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

# -------------------------------------------------------------------------------------------
#   CyVertexColorEditor
# -------------------------------------------------------------------------------------------

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import math

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

g_version = '0.1.0'
g_toolName = 'CyVertexColorEditor'
g_scriptPrefix = g_toolName + '.'
g_uiPrefix = g_toolName + 'UI_'
g_setting = None

g_vtxColorManager = None

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
    global g_vtxColorManager
    global g_setting

    cmds.selectPref(tso=True)

    if g_vtxColorManager is None:
        g_vtxColorManager = VertexColorManager()

    if g_setting is None:
        g_setting = CySetting(g_toolName)

    width = 250
    height = 1
    formWidth = width - 5

    windowTitle = g_scriptPrefix.replace('.', '')
    windowName = windowTitle + 'Win'

    CyUtility.CheckWindow(windowName)

    cmds.window(windowName, title=windowTitle, widthHeight=(width, height), s=1, mnb=True, mxb=False, rtf=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.frameLayout(l='Copy And Paste Vertex Color', cll=1, cl=0, bv=1, mw=10, mh=10)
    cmds.columnLayout(adjustableColumn=True, rs=5)

    cmds.button(label='Copy Vertex Color', bgc=[0.8, 0.5, 0.5], command=g_scriptPrefix + 'CopyVertexColor()')
    cmds.separator(style='none', h=5, w=formWidth)
    cmds.button(label='Paste Vertex Color By SelectOrder', bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + 'PasteVertexColorBySelectOrder()')
    cmds.button(label='Paste Vertex Color By Index', bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + 'PasteVertexColorByIndex()')
    cmds.button(label='Paste Vertex Color By Position', bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + 'PasteVertexColorByPosition()')

    cmds.separator(style='none', h=5, w=formWidth)

    cmds.button(label='Paste Vertex Color By Mirror X', bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + 'PasteVertexColorByMirror(0)')
    cmds.button(label='Paste Vertex Color By Mirror Y', bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + 'PasteVertexColorByMirror(1)')
    cmds.button(label='Paste Vertex Color By Mirror Z', bgc=[0.8, 0.8, 0.5], command=g_scriptPrefix + 'PasteVertexColorByMirror(2)')

    cmds.separator(style='none', h=5, w=formWidth)

    cmds.floatSliderGrp(g_uiPrefix + 'PasteDistance', label='Paste Distance', field=True,
                        minValue=0.0, maxValue=1000, fmn=0.0, fmx=1000, value=5, cw3=[80, 50, 0],
                        cl3=['left', 'center', 'center'], cc=g_scriptPrefix + 'SaveSetting()')

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(l='Round Vertex Color', cll=1, cl=0,
                     bv=1, mw=10, mh=10)
    cmds.columnLayout(adjustableColumn=True, rs=5)

    cmds.intSliderGrp(g_uiPrefix + 'RoundNum', label='Precision', field=True, minValue=1, maxValue=10, fmn=1,
                      fmx=10, value=2, cw3=[80, 30, 0], cl3=['left', 'center', 'center'], cc=g_scriptPrefix + 'SaveSetting()')
    cmds.button(label='Round Vertex Color', bgc=[
                0.8, 0.5, 0.5], command=g_scriptPrefix + 'RoundVertexColor()')
    cmds.button(label='Check Round Vertex Color', bgc=[
                0.5, 0.5, 0.8], command=g_scriptPrefix + 'CheckRoundVertexColor()')

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.separator(style='in', h=15, w=formWidth)
    cmds.button(label='About', w=formWidth, command=g_scriptPrefix + 'ShowAbout()')

    cmds.showWindow(windowName)

    LoadSetting()

# -------------------------------------------------------------------------------------------
#   CopyVertexColor
# -------------------------------------------------------------------------------------------


def CopyVertexColor():

    global g_vtxColorManager

    g_vtxColorManager.CreateInfo(True)

# -------------------------------------------------------------------------------------------
#   PasteVertexColorBySelectOrder
# -------------------------------------------------------------------------------------------


def PasteVertexColorByIndex():

    global g_vtxColorManager

    if cmds.confirmDialog(t='Confirm', m='Paste Vertex Color By Index ?', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel', ma='center') == 'Cancel':
        return

    g_vtxColorManager.CreateInfo()
    g_vtxColorManager.PasteVertexColorByIndex()

# -------------------------------------------------------------------------------------------
#   PasteVertexColorBySelectOrder
# -------------------------------------------------------------------------------------------


def PasteVertexColorBySelectOrder():

    global g_vtxColorManager

    if cmds.confirmDialog(t='Confirm', m='Paste Vertex Color By SelectOrder ?', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel', ma='center') == 'Cancel':
        return

    g_vtxColorManager.CreateInfo()
    g_vtxColorManager.PasteVertexColorBySelectOrder()

# -------------------------------------------------------------------------------------------
#   PasteVertexColorByPosition
# -------------------------------------------------------------------------------------------


def PasteVertexColorByPosition():

    global g_vtxColorManager

    if cmds.confirmDialog(t='Confirm', m='Paste Vertex Color By Position ?', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel', ma='center') == 'Cancel':
        return

    g_vtxColorManager.CreateInfo()
    g_vtxColorManager.PasteVertexColorByPosition()

# -------------------------------------------------------------------------------------------
#   PasteVertexColorByMirror
# -------------------------------------------------------------------------------------------


def PasteVertexColorByMirror(typ=0):

    global g_vtxColorManager

    if cmds.confirmDialog(t='Confirm', m='Paste Vertex Color By Mirror ?', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel', ma='center') == 'Cancel':
        return

    g_vtxColorManager.CreateInfo()

    if typ == 0:
        g_vtxColorManager.PasteVertexColorByMirror(True, False, False)
    elif typ == 1:
        g_vtxColorManager.PasteVertexColorByMirror(False, True, False)
    elif typ == 2:
        g_vtxColorManager.PasteVertexColorByMirror(False, False, True)


# -------------------------------------------------------------------------------------------
#   RoundVertexColor
# -------------------------------------------------------------------------------------------


def RoundVertexColor():

    global g_uiPrefix
    global g_vtxColorManager

    if cmds.confirmDialog(t='Confirm', m='Round vertex color ?', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel', ma='center') == 'Cancel':
        return

    roundNum = cmds.intSliderGrp(g_uiPrefix + 'RoundNum', q=True, v=True)

    g_vtxColorManager.CreateInfo()
    g_vtxColorManager.RoundVertexColor(roundNum)


# -------------------------------------------------------------------------------------------
#   CheckRoundVertexColor
# -------------------------------------------------------------------------------------------


def CheckRoundVertexColor():

    global g_uiPrefix
    global g_vtxColorManager

    if cmds.confirmDialog(t='Confirm', m='Check round vertex color ?', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel', ma='center') == 'Cancel':
        return

    roundNum = cmds.intSliderGrp(g_uiPrefix + 'RoundNum', q=True, v=True)

    g_vtxColorManager.CreateInfo()
    g_vtxColorManager.ExistRoundVertexColor(roundNum)


# -------------------------------------------------------------------------------------------
#   情報
# -------------------------------------------------------------------------------------------


def ShowAbout():

    global g_toolName
    global g_version

    CyUtility.ShowAbout(g_toolName, g_version, '')

# **************************************************************************************************************************
#   セーブロード関連
# **************************************************************************************************************************

# -------------------------------------------------------------------------------------------
#   ロード
# -------------------------------------------------------------------------------------------


def LoadSetting():

    global g_setting
    global g_uiPrefix

    pasteDistance = g_setting.Load('PasteDistance', 'float')

    roundNum = g_setting.Load('RoundNum', 'int')

    if pasteDistance != 0:
        cmds.floatSliderGrp(g_uiPrefix + 'PasteDistance', e=True, v=pasteDistance)

    if roundNum != 0:
        cmds.intSliderGrp(g_uiPrefix + 'RoundNum', e=True, v=roundNum)

# -------------------------------------------------------------------------------------------
#   セーブ
# -------------------------------------------------------------------------------------------


def SaveSetting():

    global g_setting
    global g_uiPrefix

    pasteDistance = cmds.floatSliderGrp(g_uiPrefix + 'PasteDistance', q=True, v=True)

    roundNum = cmds.intSliderGrp(g_uiPrefix + 'RoundNum', q=True, v=True)

    g_setting.Save('PasteDistance', str(pasteDistance))

    g_setting.Save('RoundNum', roundNum)

# **************************************************************************************************************************
#   クラス群
# **************************************************************************************************************************

# -------------------------------------------------------------------------------------------
#   VertexColorManager
# -------------------------------------------------------------------------------------------


class VertexColorManager(object):

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

            mel.eval('PolySelectConvert 3')

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
            mel.eval('warning \'Cannot get target vertices!\'')
            return

        info = 'Create Vertex Color Info'
        if useCopyList is True:
            info = 'Copy Vertex Color'
            self.copyVtxInfoList = []
        else:
            self.targetVtxInfoList = []

        CyUtility.StartProgress(info)

        for p in range(len(vtxList)):

            if CyUtility.UpdateProgress(float(p) / float(len(vtxList)), info + '...') is False:
                CyUtility.EndProgress()
                break

            thisVertex = vtxList[p]

            thisVtxInfo = VertexInfo(thisVertex, self)

            if thisVtxInfo.shortName == '':
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

        self.pasteDistance = cmds.floatSliderGrp(g_uiPrefix + 'PasteDistance', q=True, v=True)

    # ===========================================
    # PasteVertexColorByIndex
    # ===========================================
    def PasteVertexColorByIndex(self):

        if len(self.copyVtxInfoList) == 0:
            mel.eval('warning \'Cannot get copy vertex info!\'')
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval('warning \'Cannot get paste vertex info!\'')
            return

        CyUtility.StartProgress('Paste Vertex Color By Index')

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), 'Pasting...') is False:
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

            thisVtxInfo.UpdateVertexColor()

        CyUtility.EndProgress()

    # ===========================================
    # PasteVertexColorBySelectOrder
    # ===========================================
    def PasteVertexColorBySelectOrder(self):

        if len(self.copyVtxInfoList) == 0:
            mel.eval('warning \'Cannot get copy vertex info!\'')
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval('warning \'Cannot get paste vertex info!\'')
            return

        CyUtility.StartProgress('Paste Vertex Color By SelectOrder')

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), 'Pasting...') is False:
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

            thisVtxInfo.UpdateVertexColor()

        CyUtility.EndProgress()

    # ===========================================
    # PasteVertexColorByPosition
    # ===========================================
    def PasteVertexColorByPosition(self):

        if len(self.copyVtxInfoList) == 0:
            mel.eval('warning \'Cannot get copy vertex info!\'')
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval('warning \'Cannot get paste vertex info!\'')
            return

        CyUtility.StartProgress('Pasete Vertex Color By Position')

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), 'Pasting...') is False:
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

            thisVtxInfo.UpdateVertexColor()

        CyUtility.EndProgress()

    # ===========================================
    # PasteVertexColorByMirror
    # ===========================================
    def PasteVertexColorByMirror(self, isX, isY, isZ):

        if len(self.copyVtxInfoList) == 0:
            mel.eval('warning \'Cannot get copy vertex info!\'')
            return

        if len(self.targetVtxInfoList) == 0:
            mel.eval('warning \'Cannot get paste vertex info!\'')
            return

        CyUtility.StartProgress('Paste Vertex Color By Mirror')

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), 'Pasting...') is False:
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

            thisVtxInfo.RewriteData(targetVtxInfo)

            thisVtxInfo.UpdateVertexColor()

        CyUtility.EndProgress()

    # ===========================================
    # RoundVertexColor
    # ===========================================
    def RoundVertexColor(self, n):

        if len(self.targetVtxInfoList) == 0:
            return

        CyUtility.StartProgress('Round Vertex Color')

        for p in range(len(self.targetVtxInfoList)):

            if CyUtility.UpdateProgress(float(p) / float(len(self.targetVtxInfoList)), 'Rounding...') is False:
                CyUtility.EndProgress()
                break

            this_info = self.targetVtxInfoList[p]

            this_info.RoundVertexColor(n)

        CyUtility.EndProgress()

    # ===========================================
    # ExistRoundVertexColor
    # ===========================================
    def ExistRoundVertexColor(self, n):

        result = []

        for p in range(len(self.targetVtxInfoList)):

            info = self.targetVtxInfoList[p]

            if info.ExistRoundVertexColor(n):
                result.append(info.name)

        if len(result) == 0:
            cmds.select(cl=True)
            return

        cmds.select(result, r=True)

        cmds.warning('Some vertices have round vertex color !!!!!!')

# -------------------------------------------------------------------------------------------
#   頂点情報クラス
# -------------------------------------------------------------------------------------------


class VertexInfo(object):

    # ===========================================
    # __init__
    # ===========================================
    def __init__(self, name='', manager=None):

        self.manager = manager

        self.name = name
        self.shortName = ''

        self.meshName = ''
        self.shortMeshName = ''

        self.index = 0

        self.position = [0, 0, 0]

        self.baseColor = [0, 0, 0, 1]
        self.sameColor = True

        self.existColor = True

        self.vtxFaceInfoList = []

        if self.name == '':
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

        cloneVertexInfo.baseColor = CyUtility.CopyList(self.baseColor)
        cloneVertexInfo.sameColor = self.sameColor

        cloneVertexInfo.existColor = self.existColor

        cloneVertexInfo.vtxFaceInfoList = []
        for p in range(len(self.vtxFaceInfoList)):

            cloneVertexInfo.vtxFaceInfoList.append(self.vtxFaceInfoList[p].Clone(cloneVertexInfo))

        return cloneVertexInfo

    # ===========================================
    # CreateInfo
    # ===========================================
    def CreateInfo(self):

        self.name = CyUtility.GetLongName(self.name)

        if cmds.objExists(self.name) is False:
            self.name = ''
            return

        self.index = CyUtility.GetVertexIndex(self.name)

        self.shortName = CyUtility.GetShortName(self.name)

        self.meshName = CyUtility.GetMeshNameFromVertex(self.name)
        self.shortMeshName = CyUtility.GetShortName(self.meshName)

        self.position = cmds.pointPosition(self.name, w=True)

        self.existColor = True
        try:
            cmds.polyColorPerVertex(self.name, q=True, r=True, g=True, b=True, a=True)
        except Exception:
            self.existColor = False

        # VertexFace
        tempStr = self.name.replace('vtx[', 'vtxFace[')
        tempStr += '[*]'

        vtxFaceList = cmds.ls(tempStr, fl=True, l=True)

        self.vtxFaceList = []
        for p in range(len(vtxFaceList)):

            vtxFaceInfo = VertexFaceInfo(vtxFaceList[p], self)

            if vtxFaceInfo.shortName == '':
                continue

            self.vtxFaceInfoList.append(vtxFaceInfo)

        if len(self.vtxFaceInfoList) == 0:
            return

        self.baseColor = self.vtxFaceInfoList[0].color
        self.sameColor = True

        for p in range(0, len(self.vtxFaceInfoList)):

            thisVtxInfo = self.vtxFaceInfoList[p]

            if CyUtility.SameValueList(self.baseColor, thisVtxInfo.color) is False:
                self.sameColor = False
                break

    # ===========================================
    # RewriteData
    # ===========================================
    def RewriteData(self, targetVtxInfo):

        self.baseColor = CyUtility.CopyList(targetVtxInfo.baseColor)
        self.sameColor = targetVtxInfo.sameColor

        for p in range(len(self.vtxFaceInfoList)):

            thisIndex = p
            if p >= len(targetVtxInfo.vtxFaceInfoList):
                thisIndex = len(targetVtxInfo.vtxFaceInfoList) - 1

            self.vtxFaceInfoList[p].color = CyUtility.CopyList(targetVtxInfo.vtxFaceInfoList[thisIndex].color)

    # ===========================================
    # UpdateVertexColor
    # ===========================================
    def UpdateVertexColor(self):

        if self.sameColor is False:
            for p in range(len(self.vtxFaceInfoList)):
                self.vtxFaceInfoList[p].UpdateVertexColor()
        else:
            cmds.polyColorPerVertex(self.name, e=True, r=self.baseColor[0], g=self.baseColor[1], b=self.baseColor[2], a=self.baseColor[3])

    # ===========================================
    # RoundVertexColor
    # ===========================================
    def RoundVertexColor(self, n):

        if not self.vtxFaceInfoList:
            return

        for p in range(len(self.vtxFaceInfoList)):

            info = self.vtxFaceInfoList[p]

            info.RoundVertexColor(n)

    # ===========================================
    # ExistRoundVertexColor
    # ===========================================
    def ExistRoundVertexColor(self, n):

        if not self.vtxFaceInfoList:
            return False

        for info in self.vtxFaceInfoList:

            if info.ExistRoundVertexColor(n):
                return True

        return False


# -------------------------------------------------------------------------------------------
#   頂点フェース情報クラス
# -------------------------------------------------------------------------------------------
class VertexFaceInfo(object):

    # ===========================================
    # __init__
    # ===========================================
    def __init__(self, name='', vertexInfo=None):

        self.vertexInfo = vertexInfo

        self.name = name
        self.shortName = ''

        self.index = 0

        self.color = [0, 0, 0, 1]

        if self.name == '':
            return

        self.CreateInfo()

    # ===========================================
    # Clone
    # ===========================================
    def Clone(self, newVertexInfo):

        cloneVertexFaceInfo = VertexFaceInfo()

        cloneVertexFaceInfo.vertexInfo = newVertexInfo

        cloneVertexFaceInfo.name = self.name
        cloneVertexFaceInfo.shortName = self.shortName

        cloneVertexFaceInfo.index = self.index

        cloneVertexFaceInfo.color = CyUtility.CopyList(self.color)

        return cloneVertexFaceInfo

    # ===========================================
    # CreateInfo
    # ===========================================
    def CreateInfo(self):

        self.name = CyUtility.GetLongName(self.name)

        if cmds.objExists(self.name) is False:
            self.name = ''
            return

        self.index = CyUtility.GetVertexFaceIndex(self.name)

        self.shortName = CyUtility.GetShortName(self.name)

        self.color = [0, 0, 0, 1]
        if self.vertexInfo.existColor is False:
            return

        self.color = cmds.polyColorPerVertex(self.name, q=True, r=True, g=True, b=True, a=True)

    # ===========================================
    # UpdateVertexColor
    # ===========================================
    def UpdateVertexColor(self):

        cmds.polyColorPerVertex(self.name, e=True, r=self.color[0], g=self.color[1], b=self.color[2], a=self.color[3])

    # ===========================================
    # RoundVertexColor
    # ===========================================
    def RoundVertexColor(self, n):

        is_round = False

        for p in range(0, len(self.color)):

            this_color = self.color[p]

            if not self.__ExistRoundColor(this_color, n):
                continue

            fix_color = round(this_color, n)

            self.color[p] = fix_color

            is_round = True

        if not is_round:
            return

        self.UpdateVertexColor()

    # ===========================================
    # ExistRoundVertexColor
    # ===========================================
    def ExistRoundVertexColor(self, n):

        for p in range(0, len(self.color)):

            this_color = self.color[p]

            if self.__ExistRoundColor(this_color, n):
                return True

        return False

    # ===========================================
    # ExistRoundColor
    # ===========================================
    def __ExistRoundColor(self, color_value, n):

        tempFullValue = color_value * pow(10, n)
        tempValue = math.modf(tempFullValue)

        if tempValue[0] < 0.01 or tempValue[0] > 0.99:
            return False

        return True
