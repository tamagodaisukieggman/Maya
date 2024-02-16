# -*- coding: utf-8 -*-

"""
ピボット操作ツール

"""
from __future__ import division
from __future__ import unicode_literals

try:
    # Maya 2022-
    from past.utils import old_div
    from builtins import object
    from importlib import reload
except Exception:
    pass

import sys

import maya.cmds as mc
import pymel.core as pm

import CyNode
from CyComponent import getSelPointNames, getPointPosInfo
import CySelectChildNode
reload(CySelectChildNode)

toolName = "CyPivotTool"
__author__ = "Cygames, Inc. Yuta Kimura"

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
        #既にウィンドウが開いている場合は閉じる
        if pm.window(toolName, q=1, exists=1):
            pm.deleteUI(toolName)

        #UIの定義
        self.window = pm.window(toolName, title=u"ピボット操作ツール", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            with pm.columnLayout(rowSpacing=3):
                self.button_moveCenterPivotToComponent  = pm.button("button_moveCenterPivotToComponent", width=200, label=u"センター＆ピボット → 選択コンポーネント", command=pm.Callback(moveCenterPivotToComponent, 1))
                self.button_moveCenterToPivot           = pm.button("button_moveCenterToPivot", width=200, label=u"センター → ピボット", command=pm.Callback(moveCenterToPivot, 1))
                self.button_movePivotToCenter           = pm.button("button_movePivotToCenter", width=200, label=u"ピボット → センター", command=pm.Callback(movePivotToCenter, 1))

        #ウィンドウのサイズ変更
        winWidthValue = 200
        winHeightValue = 154
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue += 6
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return


#-------------------------------------------------
#センター＆ピボット → 選択コンポーネント
def moveCenterPivotToComponent():
    #選択コンポーネントの中心座標を取得
    model_selCenterPos = getSelCenterPos()
    if len(model_selCenterPos) == 0:
        mc.confirmDialog(title=toolName, message=u"● コンポーネントが1つも選択されていません。")
        return

    for currentShapeNodeName in model_selCenterPos:
        currentWorldPos = model_selCenterPos[currentShapeNodeName]
        if len(currentWorldPos) == 3:
            #センターを移動
            moveCenter(currentShapeNodeName, currentWorldPos)

    return


#-------------------------------------------------
#センター → ピボット
def moveCenterToPivot():
    selNodes = pm.ls(sl=1, transforms=1)
    for currentNode in selNodes:
        #回転ピボットのワールド座標
        worldRotatePivot = currentNode.getRotatePivot(space="world")
        pivotWorldPos = [worldRotatePivot.x, worldRotatePivot.y, worldRotatePivot.z]

        #センターを移動
        moveCenter(currentNode, pivotWorldPos)

    pm.select(selNodes)

    return


#-------------------------------------------------
#ピボット → センター
def movePivotToCenter():
    selNodes = pm.ls(sl=1, transforms=1)
    for currentNode in selNodes:
        #ピボット位置をリセットする
        currentNode.zeroTransformPivots()

    pm.select(selNodes)

    return


#-------------------------------------------------
#センターを移動
def moveCenter(targetNode, targetWorldPos):
    targetCyNode = CyNode.CyNode(targetNode)

    transformNode = targetCyNode.transformNode
    shapeNode = targetCyNode.shapeNode
    nodeType = targetCyNode.nodeType

    #子ノードを取得
    childNodes = CySelectChildNode.getSpecificTypeChildNodes([transformNode], ["all"], 1, 0, 0)
    for childNode in childNodes:
        childNode.parentNode = childNode.getParent()
        childNode.setParent(None)

    #ノードのワールド座標(移動前)
    nodeBeforeWorldPos = transformNode.getTranslation(space="world")

    #ノードをピボット位置に移動する
    transformNode.setTranslation(targetWorldPos, "world")

    #ノードのワールド座標(移動後)
    nodeAfterWorldPos = transformNode.getTranslation(space="world")

    #移動値
    moveValues = []
    moveValues.append(-(nodeAfterWorldPos[0] - nodeBeforeWorldPos[0]))
    moveValues.append(-(nodeAfterWorldPos[1] - nodeBeforeWorldPos[1]))
    moveValues.append(-(nodeAfterWorldPos[2] - nodeBeforeWorldPos[2]))

    if nodeType == "mesh" or nodeType == "nurbsSurface" or nodeType == "nurbsCurve":
        #全頂点
        allVertsStr = ""
        if nodeType == "mesh":
            allVertsStr = shapeNode.name() + ".vtx[*]"
        elif nodeType == "nurbsSurface":
            allVertsStr = shapeNode.name() + ".cv[*][*]"
        elif nodeType == "nurbsCurve":
            allVertsStr = shapeNode.name() + ".cv[*]"

        #ノードの移動とは逆の方向に全頂点を戻す
        pm.move(allVertsStr, moveValues, relative=1, worldSpace=1)

    elif nodeType == "locator":
        #ロケーターの見た目とセンターを一致させる(ズレを解消する)
        shapeNode.setAttr("localPositionX", 0)
        shapeNode.setAttr("localPositionY", 0)
        shapeNode.setAttr("localPositionZ", 0)

    else:
        pass

    #ピボットを元の位置に戻す
    transformNode.setPivots(targetWorldPos, worldSpace=1)

    #親子付を復帰
    for childNode in childNodes:
        childNode.setParent(childNode.parentNode)

    return


#-------------------------------------------------
#選択コンポーネントの中心座標を取得
def getSelCenterPos():
    model_selCenterPos = {}

    #選択ポイント(Vertex・CV・EP)の名前リストを取得
    selPointNames = getSelPointNames.get(convFlg=1)
    if len(selPointNames) == 0:
        return model_selCenterPos

    #ポイントの位置情報を取得
    pointPosInfo = getPointPosInfo.get(selPointNames, space="world", flatFlg=1)
    model_pointPosList = pointPosInfo["model_pointPosList"]

    for currentShapeName in model_pointPosList:
        currentWorldPosXList = model_pointPosList[currentShapeName]["pointPosXList"]
        currentWorldPosYList = model_pointPosList[currentShapeName]["pointPosYList"]
        currentWorldPosZList = model_pointPosList[currentShapeName]["pointPosZList"]

        if len(currentWorldPosXList) > 0 and len(currentWorldPosYList) > 0 and len(currentWorldPosZList) > 0:
            #バウンディングボックスの中心
            bBoxXMin = min(currentWorldPosXList)
            bBoxXMax = max(currentWorldPosXList)

            bBoxYMin = min(currentWorldPosYList)
            bBoxYMax = max(currentWorldPosYList)

            bBoxZMin = min(currentWorldPosZList)
            bBoxZMax = max(currentWorldPosZList)

            if sys.version_info.major == 2:
                bBoxCenX = (bBoxXMin + bBoxXMax) / 2
                bBoxCenY = (bBoxYMin + bBoxYMax) / 2
                bBoxCenZ = (bBoxZMin + bBoxZMax) / 2
            else:
                # for Maya 2022-
                bBoxCenX = old_div((bBoxXMin + bBoxXMax), 2)
                bBoxCenY = old_div((bBoxYMin + bBoxYMax), 2)
                bBoxCenZ = old_div((bBoxZMin + bBoxZMax), 2)

            selCenterPos = [bBoxCenX, bBoxCenY, bBoxCenZ]

            model_selCenterPos[currentShapeName] = selCenterPos

    return model_selCenterPos


#-------------------------------------------------
if __name__ == "__main__":
    main()
