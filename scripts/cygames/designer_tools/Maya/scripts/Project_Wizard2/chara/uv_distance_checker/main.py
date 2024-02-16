# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import math
import re
import itertools
import time

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om


# ==================================================
def main():

    this_main = glp_uv_distance_checker()
    this_main.create_ui()


# ==================================================
class glp_uv_distance_checker(object):

    def __init__(self):

        self.tool_version = '22072000'
        self.tool_name = 'UVdistanceChecker'
        self.window_name = self.tool_name + 'Win'

        self.suffixPattern = re.compile(r'\[(\d+)\]$')
        self.defaultMinDist = 0.0
        self.defaultMaxDist = 0.005

        self.window_width = 250
        self.window_height = 150

        self.minimumSizeField = None
        self.maximumSizeField = None
        self.isCheckShellCheckBox = None

        self.create_ui()

    def create_ui(self):

        if cmds.window(self.window_name, q=True, exists=True):
            cmds.deleteUI(self.window_name, window=True)

        self.window_name = cmds.window(
            self.window_name,
            title=self.tool_name + '  ' + self.tool_version,
            s=True, mnb=True, mxb=False, rtf=True)
        cmds.window(
            self.window_name, e=True,
            widthHeight=(self.window_width, self.window_height))

        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(
            l=u'UVのアイランド間隔チェック',
            cll=True, cl=False, bv=True,
            mw=10, mh=10, visible=True, height=self.window_height - 2)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        self.minimumSizeField = cmds.floatFieldGrp(
            numberOfFields=1, label='間隔チェック　最小値',
            value1=self.defaultMinDist, columnAlign=[1, 'left'], columnWidth=[1, 140], precision=3)
        self.maximumSizeField = cmds.floatFieldGrp(
            numberOfFields=1, label='間隔チェック　最大値',
            value1=self.defaultMaxDist, columnAlign=[1, 'left'], columnWidth=[1, 140], precision=3)
        self.isCheckShellCheckBox = cmds.checkBoxGrp(
            numberOfCheckBoxes=1, label='重複するshellはチェックしない',
            columnAlign=[1, 'left'], columnWidth=[1, 140])
        cmds.button(label='チェック実行', command=self.doScript)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.showWindow(self.window_name)

    def doScript(self, *args):

        tooCloseUVs = []

        # 現在の選択を取得
        selected = cmds.ls(sl=True, o=True)
        if not selected:
            return

        for sel in selected:
            result = self.checkTargetMeshUVInterval(sel)

            if result:
                tooCloseUVs.extend(result)

        cmds.select(tooCloseUVs)

    def checkTargetMeshUVInterval(self, targetNode):

        tooCloseUVs = []

        minDist = cmds.floatFieldGrp(self.minimumSizeField, q=True, v=True)[0]
        maxDist = cmds.floatFieldGrp(self.maximumSizeField, q=True, v=True)[0]
        isCheckedShell = cmds.checkBoxGrp(self.isCheckShellCheckBox, q=True, v1=True)

        # dagPathを取得
        dagPath = self._getDagPath(targetNode)
        # meshノードを取得
        targetMesh = om.MFnMesh(dagPath)
        # meshノードのuv情報を取得
        uvsetNames = targetMesh.getUVSetNames()

        start = time.time()
        for uvSet in uvsetNames:

            # face毎のuv数とアサインされているuvの一覧
            facesTargetUVs, asseinedUVs = targetMesh.getAssignedUVs(uvSet)
            # uv頂点の位置座標(idx順)
            uPositions, vPositions = targetMesh.getUVs(uvSet)
            # xxx
            uvBorderEdges = self.getUvBorderEdges(targetNode)
            # xxx
            uvShellsLength, uvShellsIds = targetMesh.getUvShellsIds(uvSet)

            uvShellsIDGroupList = []
            if isCheckedShell:
                for i in range(uvShellsLength):
                    uvShellsIDGroupList.append([targetNode + '.map[' + str(j) + ']' for j in range(len(uvShellsIds)) if uvShellsIds[j] == i])

            # xxx
            borderUVs = cmds.ls(cmds.polyListComponentConversion(uvBorderEdges, toUV=True), fl=True)
            # xxx
            borderUVsSuffixIdxs = [self._getTargetSuffixId(borderUV) for borderUV in borderUVs]
            # xxx
            asseinedTextureList, textureAsseinedFaceList = targetMesh.getConnectedShaders(0)

            borderUVsPerTextureIdxsList = []

            # アサインされているテクスチャが同uvsetに2つ以上ある時の処理
            if len(asseinedTextureList) != 1:

                for i in range(len(asseinedTextureList)):
                    borderUVsPerTextureIdxsList.append([])

                count = 0
                for i in range(len(facesTargetUVs)):
                    faceVtxCount = facesTargetUVs[i]
                    textureIdx = textureAsseinedFaceList[i]
                    cutCount = count + faceVtxCount
                    uvsIdx = asseinedUVs[count:cutCount]
                    borderUVsPerTextureIdxsList[textureIdx].extend(uvsIdx)
                    count = cutCount

                for i in range(len(asseinedTextureList)):
                    diffList = list(set(borderUVsPerTextureIdxsList[i][:]) & set(borderUVsSuffixIdxs))
                    borderUVsPerTextureIdxsList[i] = diffList

            edgeCount = 0
            edgeLength = len(uvBorderEdges)

            cmds.progressWindow(title='Progress...', progress=edgeCount,
                                status='Sleeping: 0%', isInterruptable=True,
                                maxValue=edgeLength)

            for edge in uvBorderEdges:
                if cmds.progressWindow(query=True, isCancelled=True):
                    break
                if cmds.progressWindow(query=True, progress=True) >= edgeLength:
                    break

                edgeCount += 1
                status = '現在実行中 : {0} / {1}'.format(str(edgeCount), str(edgeLength))
                cmds.progressWindow(edit=True, progress=edgeCount, status=status)

                uvs = cmds.ls(cmds.polyListComponentConversion(edge, toUV=True), fl=True)
                uvsCombiList = list(itertools.combinations(uvs, 2))

                for uvsCombi in uvsCombiList:

                    uv1 = uvsCombi[0]
                    uv2 = uvsCombi[1]

                    uv1SuffixId = self._getTargetSuffixId(uv1)
                    uv2SuffixId = self._getTargetSuffixId(uv2)
                    if not uv1SuffixId or not uv2SuffixId:
                        continue

                    uv1ShellsIdx = uvShellsIds[uv1SuffixId]
                    uv2ShellsIdx = uvShellsIds[uv2SuffixId]

                    if uv1ShellsIdx != uv2ShellsIdx:
                        continue

                    # uv頂点の隣接した頂点以外は対象としない
                    shortestLength = cmds.polySelect(q=True, shortestEdgePathUV=[uv1SuffixId, uv2SuffixId])
                    if len(shortestLength) > 1:
                        continue

                    uv1UPos = uPositions[uv1SuffixId]
                    uv2UPos = uPositions[uv2SuffixId]
                    uv1VPos = vPositions[uv1SuffixId]
                    uv2VPos = vPositions[uv2SuffixId]

                    targetBorderUVs = []

                    for perTextureIdxs in borderUVsPerTextureIdxsList:
                        if uv1SuffixId in perTextureIdxs:
                            targetBorderIdxs = perTextureIdxs
                            targetBorderUVs = [targetNode + '.map[' + str(idx) + ']' for idx in targetBorderIdxs]
                            break
                    else:
                        targetBorderUVs = borderUVs

                    for targetBorderUV in targetBorderUVs:

                        # 重くなっていた原因
                        # 再検索を防ごうと思って入れていたが、一致しているかどうかを取得するのに時間が掛かっていた
                        # if targetBorderUV in tooCloseUVs:
                        #     continue

                        uvBorderUVSuffixIdx = self._getTargetSuffixId(targetBorderUV)
                        if not uvBorderUVSuffixIdx:
                            continue

                        uvBorderUVsShellsIdx = uvShellsIds[uvBorderUVSuffixIdx]
                        if uv1ShellsIdx == uvBorderUVsShellsIdx:
                            continue

                        uv3UPos = uPositions[uvBorderUVSuffixIdx]
                        uv3VPos = vPositions[uvBorderUVSuffixIdx]

                        # uv1とuv3の距離(A)
                        uv13Distance = math.sqrt(pow((uv3UPos - uv1UPos), 2) + pow((uv3VPos - uv1VPos), 2))
                        # uv2とuv3の距離(B)
                        uv23Distance = math.sqrt(pow((uv3UPos - uv2UPos), 2) + pow((uv3VPos - uv2VPos), 2))

                        distAX, distABP, vectorLength = self.nearPosOnLine(uv1UPos, uv2UPos, uv3UPos, uv1VPos, uv2VPos, uv3VPos)

                        # uv3とベクトルuv1uv2の垂線の位置が１単位ベクトル内であればdistance3種の中で一番近い方で判断
                        nearDirtTargets = [uv13Distance, uv23Distance]
                        if 0 <= distAX < vectorLength:
                            nearDirtTargets.append(distABP)

                        nearDist = min(nearDirtTargets)
                        if minDist < nearDist <= maxDist:

                            # シェルが一部でも重なっている場合、検索から除外する
                            if isCheckedShell:
                                uv1ShellsIdxFaces = uvShellsIDGroupList[uvBorderUVsShellsIdx]
                                uvBorderUVsShellsIdxFaces = uvShellsIDGroupList[uvBorderUVsShellsIdx]
                                if cmds.polyUVOverlap(uv1ShellsIdxFaces + uvBorderUVsShellsIdxFaces, oc=True):
                                    continue

                            # edgeが重複しているか調べる
                            targetUV = [targetBorderUV, uv1, uv2]
                            toEdge = cmds.polyListComponentConversion(targetUV, toEdge=True)
                            if not cmds.polyUVOverlap(toEdge, oc=True):
                                tooCloseUVs.append(targetBorderUV)

            cmds.progressWindow(endProgress=True)
        elapsed_time = time.time() - start
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

        return tooCloseUVs

    def getUvBorderEdges(self, mesh):

        # 元の選択を取っておく
        selected = cmds.ls(sl=True, l=True)

        # UV境界エッジを取得する
        borderUVEdges = []
        cmds.select(mesh + ".map[*]", r=True)
        mel.eval("polySelectBorderShell 1;")
        borders = cmds.polyListComponentConversion(te=True)
        borders = cmds.ls(borders, fl=True)
        for border in borders:
            edge = cmds.polyListComponentConversion(border, tuv=True)
            edge = cmds.ls(edge, fl=True)
            if len(edge) > 2:
                borderUVEdges.append(border)
        cmds.select(mesh + ".e[*]", r=True)
        mel.eval("polySelectBorderShell 1;")
        borderUVEdges.extend(cmds.ls(sl=True, fl=True))

        # 選択状態を元に戻す
        cmds.select(selected)

        return borderUVEdges

    def nearPosOnLine(self, uv1UPos, uv2UPos, uv3UPos, uv1VPos, uv2VPos, uv3VPos):

        uv12UPos = uv2UPos - uv1UPos
        uv12VPos = uv2VPos - uv1VPos
        uv13Upos = uv3UPos - uv1UPos
        uv13Vpos = uv3VPos - uv1VPos

        # ABの単位ベクトルと単位ベクトルの長さ
        uv12VectorU, uv12VectorV, vectorLength = self.create_unit_vector(uv12UPos, uv12VPos)

        # ベクトルABとベクトルAPの外積の絶対値
        uv1213crossProduct = abs(self.calc_cross_product(uv12UPos, uv12VPos, uv13Upos, uv13Vpos))

        # 線上近似点
        dist_AX = self.carc_inner_product(uv12VectorU, uv12VectorV, uv13Upos, uv13Vpos)

        # AB間の距離
        dist_AB = self.carc_2point_distance(uv1UPos, uv1VPos, uv2UPos, uv2VPos)

        # uv3からベクトルABに垂線を引いた時の距離
        dist_ABP = 0
        if dist_AB != 0:
            dist_ABP = uv1213crossProduct / dist_AB

        return dist_AX, dist_ABP, vectorLength

    # 2点間の距離
    def carc_2point_distance(self, p1u, p1v, p2u, p2v):

        return math.sqrt(pow((p2u - p1u), 2) + pow((p2v - p1v), 2))

    # ベクトル外積
    def calc_cross_product(self, vlu, vlv, vru, vrv):

        return vlu * vrv - vlv * vru

    # ベクトル内積
    def carc_inner_product(self, vlu, vlv, vru, vrv):

        return vlu * vru + vlv * vrv

    # 単位ベクトル生成
    def create_unit_vector(self, vu, vv):

        vectorLength = pow((vu * vu) + (vv * vv), 0.5)
        if vectorLength == 0:
            return 0, 0, 0

        vectorRetU = vu / vectorLength
        vectorRetV = vv / vectorLength

        return vectorRetU, vectorRetV, vectorLength

    def _getTargetSuffixId(self, target):

        suffix = None
        matchObj = self.suffixPattern.search(target)
        if matchObj:
            suffix = matchObj.group(1)
            suffix = int(suffix)

        return suffix

    def _getTargetSuffixIdsList(self, targetList):

        targetSuffixList = []

        for target in targetList:
            suffix = self._getTargetSuffixId(target)
            if suffix:
                targetSuffixList.append(suffix)

        return targetSuffixList

    def _getDagPath(self, sel):

        selectionList = om.MSelectionList()
        selectionList.add(sel)

        return selectionList.getDagPath(0)
