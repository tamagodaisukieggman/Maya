# -*- coding: utf-8 -*-

"""
スキニングモデルをウェイトを保ったままスケーリングする

"""
from __future__ import division

try:
    # Maya 2022-
    from builtins import str
    from builtins import zip
    from builtins import object
    from past.utils import old_div
except Exception:
    pass

toolName = "TkgScaleSkinModel"
__author__ = "TKG,  Yuta Kimura"

import os
import sys

import maya.mel as mm
import maya.cmds as mc
import pymel.core as pm

import TkgSelectChildNode
import TkgPivotTool
from TkgDagNode import getFilteredDagNodeInfo

#maya設定フォルダのパス
userAppDirPath = pm.internalVar(userAppDir=1)

#ツール設定のパス
configFolderPath = userAppDirPath + "TKG/" + toolName
configFilePath = configFolderPath + "/" + toolName + ".ini"


#-------------------------------------------------
#メイン
def main():
    #メインウィンドウオブジェクトの生成
    toolWindow = MainWindow()
    return


#-------------------------------------------------
#メインウィンドウクラス
class MainWindow(object):
    def __init__(self):
        #設定を読み込み
        loadedConfigInfo = self.loadConfig()

        #既にウィンドウが開いている場合は閉じる
        if pm.window(toolName, q=1, exists=1):
            pm.deleteUI(toolName)

        #UIの定義
        self.window = pm.window(toolName, title="ScaleSkinModel", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            self.columnLayout_top = pm.columnLayout("columnLayout_top", columnOffset=("left", 5))
            with self.columnLayout_top:
                self.separator_topSpace = pm.separator("separator_topSpace", w=1, h=5, style="none")

                #スケール
                self.rowLayout_scaleTitle = pm.rowLayout("rowLayout_scaleTitle", numberOfColumns=3)
                with self.rowLayout_scaleTitle:
                    self.text_scaleTitle = pm.text("text_scaleTitle", align="left", label=u" Scale ", bgc=[1,1,1], font="boldLabelFont")
                    self.separator_scaleTitleSpace = pm.separator("separator_scaleTitleSpace", w=1, style="none")
                    self.separator_scaleTitle = pm.separator("separator_scaleTitle", w=100, style="double")

                self.columnLayout_scale = pm.columnLayout("columnLayout_scale", rowSpacing=3, columnOffset=("left", 7))
                with self.columnLayout_scale:
                    self.separator_scaleSpace = pm.separator("separator_scaleSpace", w=1, h=1, style="none")

                    #スケールALL
                    self.rowLayout_scaleALL = pm.rowLayout("rowLayout_scaleALL", numberOfColumns=3)
                    with self.rowLayout_scaleALL:
                        self.button_scaleALLMinus = pm.button("button_scaleALLMinus", w=25, h=20, label=u"All-", bgc=[0.8,0.8,0.8], command=pm.Callback(self.scale, "all", "minus"))
                        self.floatField_scaleALLValue = pm.floatField("floatField_scaleALLValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleALLPlus = pm.button("button_scaleALLPlus", w=25, h=20, label=u"All+", bgc=[0.8,0.8,0.8], command=pm.Callback(self.scale, "all", "plus"))

                    #スケールX
                    self.rowLayout_scaleX = pm.rowLayout("rowLayout_scaleX", numberOfColumns=3)
                    with self.rowLayout_scaleX:
                        self.button_scaleXMinus = pm.button("button_scaleXMinus", w=25, h=20, label=u"X-", bgc=[0.8,0.6,0.6], command=pm.Callback(self.scale, "x", "minus"))
                        self.floatField_scaleXValue = pm.floatField("floatField_scaleXValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleXPlus = pm.button("button_scaleXPlus", w=25, h=20, label=u"X+", bgc=[0.8,0.6,0.6], command=pm.Callback(self.scale, "x", "plus"))

                    #スケールY
                    self.rowLayout_scaleY = pm.rowLayout("rowLayout_scaleY", numberOfColumns=3)
                    with self.rowLayout_scaleY:
                        self.button_scaleYMinus = pm.button("button_scaleYMinus", w=25, h=20, label=u"Y-", bgc=[0.6,0.8,0.6], command=pm.Callback(self.scale, "y", "minus"))
                        self.floatField_scaleYValue = pm.floatField("floatField_scaleYValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleYPlus = pm.button("button_scaleYPlus", w=25, h=20, label=u"Y+", bgc=[0.6,0.8,0.6], command=pm.Callback(self.scale, "y", "plus"))

                    #スケールZ
                    self.rowLayout_scaleZ = pm.rowLayout("rowLayout_scaleZ", numberOfColumns=3)
                    with self.rowLayout_scaleZ:
                        self.button_scaleZMinus = pm.button("button_scaleZMinus", w=25, h=20, label=u"Z-", bgc=[0.6,0.8,0.9], command=pm.Callback(self.scale, "z", "minus"))
                        self.floatField_scaleZValue = pm.floatField("floatField_scaleZValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleZPlus = pm.button("button_scaleZPlus", w=25, h=20, label=u"Z+", bgc=[0.6,0.8,0.9], command=pm.Callback(self.scale, "z", "plus"))

                self.separator_scalePivotSpace = pm.separator("separator_scalePivotSpace", w=1, h=15, style="none")

        #前回の設定を復帰
        self.restoreParam(loadedConfigInfo)

        #ウィンドウのサイズ変更
        winWidthValue = 159
        winHeightValue = 144
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue += 1
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    #-------------------------
    #スケール
    def scale(self, direction, plus_or_minus):
        selNodes = pm.ls(sl=1, flatten=1)
        if len(selNodes) == 0:
            messageStr = u"操作対象が1つも選択されていません。"
            pm.confirmDialog(title=toolName, message=u"● " + messageStr)
            return

        #編集値を取得
        scaleValues = self.getEditValue(direction, plus_or_minus)

        for currentNode in selNodes:
            pm.select(currentNode)

            #子ノードを取得
            firstHierarchyChildNodes = currentNode.getChildren()
            allChildNodes = TkgSelectChildNode.getChildNodes(currentNode, [])

            #フィルタリングされた(タイプごとの)DAGノードリストを取得
            filteredDagNodeInfo = getFilteredDagNodeInfo.get(allChildNodes, ["mesh","joint","locator"])
            nodetype_nodeList = filteredDagNodeInfo["nodetype_nodeList"]

            meshNodes = nodetype_nodeList["mesh"]
            jointNodes = nodetype_nodeList["joint"]
            locatorNodes = nodetype_nodeList["locator"]

            if len(meshNodes) == 0 or len(jointNodes) == 0:
                continue

            #ウェイト情報をエクスポート
            pm.select(meshNodes)
            weightInfo = exportWeight(meshNodes)

            #バインドポーズに戻す
            pm.runtime.GoToBindPose()

            #スキンのデタッチ
            pm.runtime.DetachSkin()

            #スケーリング用にジョイントの設定を変更
            for currentJointNode in jointNodes:
                currentJointNode.setScaleCompensate(0)

            #ピボット→センター
            pm.select(meshNodes)
            TkgPivotTool.movePivotToCenter()

            #スケーリング
            pm.select(firstHierarchyChildNodes)
            pm.scale(scaleValues, relative=1)

            #スケールのフリーズ(変更したジョイント設定はリセットされる)
            pm.makeIdentity(apply=1, translate=0, rotate=0, scale=1, normal=0)

            #ロケーター
            if len(locatorNodes) > 0:
                #センター→ピボット
                pm.select(locatorNodes)
                TkgPivotTool.moveCenterToPivot()

            #ヒストリーを削除
            pm.select(allChildNodes)
            pm.delete(constructionHistory=1)

            #各メッシュ
            for currentMeshNode in meshNodes:
                currentMeshNodeName = currentMeshNode.longName()

                if currentMeshNodeName in weightInfo:
                    connectedJointNames = weightInfo[currentMeshNodeName]["jointNames"]

                    #メッシュとジョイントを選択
                    pm.select(currentMeshNode, replace=1)
                    pm.select(connectedJointNames, add=1)

                    #スムースバインド
                    pm.skinCluster(bindMethod=0,
                                   skinMethod=0,
                                   normalizeWeights=2,
                                   maximumInfluences=5,
                                   obeyMaxInfluences=1,
                                   dropoffRate=4.0,
                                   removeUnusedInfluence=0)

            #ウェイト情報をインポート
            importWeight(meshNodes, weightInfo)

        #選択を復帰
        pm.select(selNodes)

        return

    #-------------------------
    #編集値を取得
    def getEditValue(self, direction, plus_or_minus):
        editValues = [1, 1, 1]

        if direction == "all":
            scaleALLValue = self.__dict__["floatField_scaleALLValue"].getValue()
            if plus_or_minus == "minus":
                if sys.version_info.major == 2:
                    scaleALLValue = 1 / scaleALLValue
                else:
                    # for Maya 2022-
                    scaleALLValue = old_div(1, scaleALLValue)
            editValues = [scaleALLValue, scaleALLValue, scaleALLValue]
        else:
            direction_index = {"x":0, "y":1, "z":2}
            for currentDirection in ["x", "y", "z"]:
                if currentDirection == direction:
                    currentControlName = "floatField_scale" + currentDirection.upper() + "Value"
                    if currentControlName in self.__dict__:
                        currentEditValue = self.__dict__[currentControlName].getValue()
                        if plus_or_minus == "minus":
                            if sys.version_info.major == 2:
                                currentEditValue = 1 / currentEditValue
                            else:
                                # for Maya 2022-
                                currentEditValue = old_div(1, currentEditValue)
                    editValues[direction_index[currentDirection]] = currentEditValue

        return editValues

    #-------------------------
    #前回の設定を復帰
    def restoreParam(self, loadedConfigInfo):
        for currentParamName in loadedConfigInfo:
            currentControlName = "floatField_" + currentParamName + "Value"
            if currentControlName in self.__dict__:
                try:
                    self.__dict__[currentControlName].setValue(loadedConfigInfo[currentParamName])
                except:
                    pass

        self.saveConfig()

        return

    #-------------------------
    #設定を読み込み
    def loadConfig(self):
        loadedConfigInfo = {}

        #テキストファイルの読み込み
        if os.path.isfile(configFilePath):
            f = open(configFilePath)
            allLines = f.readlines()
            f.close()

            for currentLineString in allLines:
                paramParts = currentLineString.replace("\n", "").split("@")
                if len(paramParts) == 2:
                    currentParamName = paramParts[0]
                    currentValue = float(paramParts[1])
                    loadedConfigInfo[currentParamName] = currentValue

        return loadedConfigInfo

    #-------------------------
    #設定を保存
    def saveConfig(self):
        configInfo = {}

        #{パラメーター名:値}
        for currentDirection in ("all", "x", "y", "z"):
            currentParamName = "scale" + currentDirection.upper()
            currentControlName = "floatField_" + currentParamName + "Value"
            if currentControlName in self.__dict__:
                currentEditValue = self.__dict__[currentControlName].getValue()
                configInfo[currentParamName] = str(currentEditValue)

        allParamNames = list(configInfo.keys())
        allParamNames.sort()

        #設定情報を文字列にまとめる
        configString = ""
        for currentParamName in allParamNames:
            if configString != "":
                configString += "\n"
            configString += currentParamName + "@" + configInfo[currentParamName]

        #テキストファイルの書き込み
        if not os.path.isdir(configFolderPath):
            os.makedirs(configFolderPath)
        f = open(configFilePath, "w")
        f.write(configString)
        f.close()

        return


#-------------------------------------------------
#ウェイト情報をエクスポート
def exportWeight(meshTransNodes):
    weightInfo = {}

    gMainProgressBar = mm.eval("$tmp = $gMainProgressBar")

    for transNode in meshTransNodes:
        transNodeName = transNode.longName()

        weightInfo[transNodeName] = {}
        weightInfo[transNodeName]["jointNames"] = []
        weightInfo[transNodeName]["weightValuesList"] = []

        #ヒストリーからスキンクラスターを取得
        shapeNode = transNode.getShape()
        hisNodes = shapeNode.listHistory()
        skinClusters = pm.ls(hisNodes, type="skinCluster")
        if len(skinClusters) == 0:
            return
        skinClusterName = skinClusters[0].name()

        #ジョイントのリスト
        connectedJointNames = mc.skinCluster(skinClusterName, q=1, influence=1)
        weightInfo[transNodeName]["jointNames"] = connectedJointNames

        allVertNames = mc.ls(transNodeName + ".vtx[*]", flatten=1)

        mc.progressBar(gMainProgressBar,
                        e=1,
                        beginProgress=1,
                        status=u"ウェイト情報をエクスポート中...",
                        maxValue=len(allVertNames))

        #各頂点
        for currentVertName in allVertNames:
            #現在の頂点のウェイト値を取得
            currentVertWeightValues = mc.skinPercent(skinClusterName, currentVertName, q=1, v=1)
            weightInfo[transNodeName]["weightValuesList"].append(currentVertWeightValues)

            mc.progressBar(gMainProgressBar, edit=1, step=1)

        mc.progressBar(gMainProgressBar, edit=1, endProgress=1)

    return weightInfo


#-------------------------------------------------
#ウェイト情報をインポート
def importWeight(meshTransNodes, weightInfo):
    gMainProgressBar = mm.eval("$tmp = $gMainProgressBar")

    for transNode in meshTransNodes:
        transNodeName = transNode.longName()

        #ヒストリーからスキンクラスターを取得
        shapeNode = transNode.getShape()
        hisNodes = shapeNode.listHistory()
        skinClusters = pm.ls(hisNodes, type="skinCluster")
        if len(skinClusters) == 0:
            continue
        skinClusterName = skinClusters[0].name()

        if transNodeName in weightInfo:
            #一時保存されたウェイト情報
            savedJointNames = weightInfo[transNodeName]["jointNames"]
            savedWeightValuesList = weightInfo[transNodeName]["weightValuesList"]

            #頂点リスト
            allVertNames = mc.ls(transNodeName + ".vtx[*]", flatten=1)

            if len(allVertNames) == len(savedWeightValuesList):
                mc.progressBar(gMainProgressBar,
                                e=1,
                                beginProgress=1,
                                status=u"ウェイト情報をインポート中...",
                                maxValue=len(allVertNames))

                #各頂点
                for i, currentVertWeightValues in enumerate(savedWeightValuesList):
                    #ウェイト値を編集
                    mc.skinPercent(skinClusterName, allVertNames[i], normalize=0, zeroRemainingInfluences=1, transformValue=(list(zip(savedJointNames, currentVertWeightValues))))

                    mc.progressBar(gMainProgressBar, edit=1, step=1)

                mc.progressBar(gMainProgressBar, edit=1, endProgress=1)

    return


#-------------------------------------------------
if __name__ == '__main__':
    main()
