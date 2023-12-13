# -*- coding: utf-8 -*-

"""
相対変形(移動・回転・スケール)ツール

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
    from past.utils import old_div
except Exception:
    pass

toolName = "CyRelativeTransformTool"
__author__ = "Cygames, Inc. Yuta Kimura"

import os
import re
import sys

import maya.cmds as mc
import pymel.core as pm

from CyComponent import getSelItemPosInfo
reload(getSelItemPosInfo)

#maya設定フォルダのパス
userAppDirPath = pm.internalVar(userAppDir=1)

#ツール設定のパス
configFolderPath = userAppDirPath + "Cygames/" + toolName
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
        self.window = pm.window(toolName, title=u"相対変形ツール", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            self.columnLayout_top = pm.columnLayout("columnLayout_top", columnOffset=("left", 5))
            with self.columnLayout_top:
                self.separator_topSpace = pm.separator("separator_topSpace", w=1, h=5, style="none")

                #移動
                self.rowLayout_moveTitle = pm.rowLayout("rowLayout_moveTitle", numberOfColumns=3)
                with self.rowLayout_moveTitle:
                    self.text_moveTitle = pm.text("text_moveTitle", align="left", label=u" Move ", bgc=[1,1,1], font="boldLabelFont")
                    self.separator_moveTitleSpace = pm.separator("separator_moveTitleSpace", w=1, style="none")
                    self.separator_moveTitle = pm.separator("separator_moveTitle", w=99, style="double")

                self.columnLayout_move = pm.columnLayout("columnLayout_move", rowSpacing=3, columnOffset=("left", 7))
                with self.columnLayout_move:
                    self.separator_moveSpace = pm.separator("separator_moveSpace", w=1, h=1, style="none")

                    #移動オプションメニュー
                    self.rowLayout_moveSpace = pm.rowLayout("rowLayout_moveSpace", numberOfColumns=2)
                    with self.rowLayout_moveSpace:
                        self.text_moveSpace = pm.text("text_moveSpace", align="left", label=u" 空間 : ")

                        self.optionMenu_moveSpace = pm.optionMenu("optionMenu_moveSpace", w=89, h=20, cc=pm.Callback(self.saveConfig))
                        self.menuItem_moveWorld = pm.menuItem("menuItem_moveWorld", parent=self.optionMenu_moveSpace, label=u"ワールド")
                        self.menuItem_moveLocal = pm.menuItem("menuItem_moveLocal", parent=self.optionMenu_moveSpace, label=u"ローカル")
                        self.menuItem_moveObject = pm.menuItem("menuItem_moveObject", parent=self.optionMenu_moveSpace, label=u"オブジェクト")

                    #移動X
                    self.rowLayout_moveX = pm.rowLayout("rowLayout_moveX", numberOfColumns=3)
                    with self.rowLayout_moveX:
                        self.button_moveXMinus = pm.button("button_moveXMinus", w=25, h=20, label=u"X-", bgc=[0.8,0.6,0.6], command=pm.Callback(self.transform, "move", "x", "minus"))
                        self.floatField_moveXValue = pm.floatField("floatField_moveXValue", w=75, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_moveXPlus = pm.button("button_moveXPlus", w=25, h=20, label=u"X+", bgc=[0.8,0.6,0.6], command=pm.Callback(self.transform, "move", "x", "plus"))

                    #移動Y
                    self.rowLayout_moveY = pm.rowLayout("rowLayout_moveY", numberOfColumns=3)
                    with self.rowLayout_moveY:
                        self.button_moveYMinus = pm.button("button_moveYMinus", w=25, h=20, label=u"Y-", bgc=[0.6,0.8,0.6], command=pm.Callback(self.transform, "move", "y", "minus"))
                        self.floatField_moveYValue = pm.floatField("floatField_moveYValue", w=75, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_moveYPlus = pm.button("button_moveYPlus", w=25, h=20, label=u"Y+", bgc=[0.6,0.8,0.6], command=pm.Callback(self.transform, "move", "y", "plus"))

                    #移動Z
                    self.rowLayout_moveZ = pm.rowLayout("rowLayout_moveZ", numberOfColumns=3)
                    with self.rowLayout_moveZ:
                        self.button_moveZMinus = pm.button("button_moveZMinus", w=25, h=20, label=u"Z-", bgc=[0.6,0.8,0.9], command=pm.Callback(self.transform, "move", "z", "minus"))
                        self.floatField_moveZValue = pm.floatField("floatField_moveZValue", w=75, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_moveZPlus = pm.button("button_moveZPlus", w=25, h=20, label=u"Z+", bgc=[0.6,0.8,0.9], command=pm.Callback(self.transform, "move", "z", "plus"))

                    #自動入力ボタン
                    self.button_input2PointDistance = pm.button("button_input2PointDistance", w=131, h=20,
                                                        label=u"2点差分取得(ワールド)",
                                                        annotation=u"「2頂点」か「2ノード(Transform)」の位置の差分(World座標)を測って自動入力します。",
                                                        bgc=[0.7,0.7,0.7],
                                                        command=pm.Callback(self.input2PointDistance))

                self.separator_moveRotateSpace = pm.separator("separator_moveRotateSpace", w=1, h=12, style="none")

                #回転
                self.rowLayout_rotateTitle = pm.rowLayout("rowLayout_rotateTitle", numberOfColumns=3)
                with self.rowLayout_rotateTitle:
                    self.text_rotateTitle = pm.text("text_rotateTitle", align="left", label=u" Rotate ", bgc=[1,1,1], font="boldLabelFont")
                    self.separator_rotateTitleSpace = pm.separator("separator_rotateTitleSpace", w=1, style="none")
                    self.separator_rotateTitle = pm.separator("separator_rotateTitle", w=91, style="double")

                self.columnLayout_rotate = pm.columnLayout("columnLayout_rotate", rowSpacing=3, columnOffset=("left", 7))
                with self.columnLayout_rotate:
                    self.separator_rotateSpace = pm.separator("separator_rotateSpace", w=1, h=1, style="none")

                    #回転オプションメニュー
                    self.rowLayout_rotateSpace = pm.rowLayout("rowLayout_rotateSpace", numberOfColumns=2)
                    with self.rowLayout_rotateSpace:
                        self.text_rotateSpace = pm.text("text_rotateSpace", align="left", label=u" 空間 : ")

                        self.optionMenu_rotateSpace = pm.optionMenu("optionMenu_rotateSpace", w=89, h=20, cc=pm.Callback(self.saveConfig))
                        self.menuItem_rotateWorld = pm.menuItem("menuItem_rotateWorld", parent=self.optionMenu_rotateSpace, label=u"ワールド")
                        self.menuItem_rotateObject = pm.menuItem("menuItem_rotateObject", parent=self.optionMenu_rotateSpace, label=u"オブジェクト")

                    #回転X
                    self.rowLayout_rotateX = pm.rowLayout("rowLayout_rotateX", numberOfColumns=3)
                    with self.rowLayout_rotateX:
                        self.button_rotateXMinus = pm.button("button_rotateXMinus", w=25, h=20, label=u"X-", bgc=[0.8,0.6,0.6], command=pm.Callback(self.transform, "rotate", "x", "minus"))
                        self.floatField_rotateXValue = pm.floatField("floatField_rotateXValue", w=75, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_rotateXPlus = pm.button("button_rotateXPlus", w=25, h=20, label=u"X+", bgc=[0.8,0.6,0.6], command=pm.Callback(self.transform, "rotate", "x", "plus"))

                    #回転Y
                    self.rowLayout_rotateY = pm.rowLayout("rowLayout_rotateY", numberOfColumns=3)
                    with self.rowLayout_rotateY:
                        self.button_rotateYMinus = pm.button("button_rotateYMinus", w=25, h=20, label=u"Y-", bgc=[0.6,0.8,0.6], command=pm.Callback(self.transform, "rotate", "y", "minus"))
                        self.floatField_rotateYValue = pm.floatField("floatField_rotateYValue", w=75, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_rotateYPlus = pm.button("button_rotateYPlus", w=25, h=20, label=u"Y+", bgc=[0.6,0.8,0.6], command=pm.Callback(self.transform, "rotate", "y", "plus"))

                    #回転Z
                    self.rowLayout_rotateZ = pm.rowLayout("rowLayout_rotateZ", numberOfColumns=3)
                    with self.rowLayout_rotateZ:
                        self.button_rotateZMinus = pm.button("button_rotateZMinus", w=25, h=20, label=u"Z-", bgc=[0.6,0.8,0.9], command=pm.Callback(self.transform, "rotate", "z", "minus"))
                        self.floatField_rotateZValue = pm.floatField("floatField_rotateZValue", w=75, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_rotateZPlus = pm.button("button_rotateZPlus", w=25, h=20, label=u"Z+", bgc=[0.6,0.8,0.9], command=pm.Callback(self.transform, "rotate", "z", "plus"))

                self.separator_rotateScaleSpace = pm.separator("separator_rotateScaleSpace", w=1, h=12, style="none")

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
                        self.button_scaleALLMinus = pm.button("button_scaleALLMinus", w=25, h=20, label=u"All-", bgc=[0.8,0.8,0.8], command=pm.Callback(self.transform, "scale", "all", "minus"))
                        self.floatField_scaleALLValue = pm.floatField("floatField_scaleALLValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleALLPlus = pm.button("button_scaleALLPlus", w=25, h=20, label=u"All+", bgc=[0.8,0.8,0.8], command=pm.Callback(self.transform, "scale", "all", "plus"))

                    #スケールX
                    self.rowLayout_scaleX = pm.rowLayout("rowLayout_scaleX", numberOfColumns=3)
                    with self.rowLayout_scaleX:
                        self.button_scaleXMinus = pm.button("button_scaleXMinus", w=25, h=20, label=u"X-", bgc=[0.8,0.6,0.6], command=pm.Callback(self.transform, "scale", "x", "minus"))
                        self.floatField_scaleXValue = pm.floatField("floatField_scaleXValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleXPlus = pm.button("button_scaleXPlus", w=25, h=20, label=u"X+", bgc=[0.8,0.6,0.6], command=pm.Callback(self.transform, "scale", "x", "plus"))

                    #スケールY
                    self.rowLayout_scaleY = pm.rowLayout("rowLayout_scaleY", numberOfColumns=3)
                    with self.rowLayout_scaleY:
                        self.button_scaleYMinus = pm.button("button_scaleYMinus", w=25, h=20, label=u"Y-", bgc=[0.6,0.8,0.6], command=pm.Callback(self.transform, "scale", "y", "minus"))
                        self.floatField_scaleYValue = pm.floatField("floatField_scaleYValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleYPlus = pm.button("button_scaleYPlus", w=25, h=20, label=u"Y+", bgc=[0.6,0.8,0.6], command=pm.Callback(self.transform, "scale", "y", "plus"))

                    #スケールZ
                    self.rowLayout_scaleZ = pm.rowLayout("rowLayout_scaleZ", numberOfColumns=3)
                    with self.rowLayout_scaleZ:
                        self.button_scaleZMinus = pm.button("button_scaleZMinus", w=25, h=20, label=u"Z-", bgc=[0.6,0.8,0.9], command=pm.Callback(self.transform, "scale", "z", "minus"))
                        self.floatField_scaleZValue = pm.floatField("floatField_scaleZValue", w=75, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_scaleZPlus = pm.button("button_scaleZPlus", w=25, h=20, label=u"Z+", bgc=[0.6,0.8,0.9], command=pm.Callback(self.transform, "scale", "z", "plus"))

                self.separator_scalePivotSpace = pm.separator("separator_scalePivotSpace", w=1, h=15, style="none")

                #ピボット
                self.frameLayout_pivot = pm.frameLayout(w=148, label=u"RotateとScale用のPivot", borderStyle="etchedIn", font="plainLabelFont", marginWidth=7, marginHeight=5)
                with self.frameLayout_pivot:

                    self.columnLayout_pivot = pm.columnLayout("columnLayout_pivot")
                    with self.columnLayout_pivot:
                        #ピボットオプションメニュー
                        self.text_usePivotLabel = pm.text("text_usePivotLabel", align="left", label=u"※ コンポーネント限定機能")
                        self.rowLayout_pivotOption = pm.rowLayout("rowLayout_pivotOption", numberOfColumns=2)
                        with self.rowLayout_pivotOption:
                            self.optionMenu_pivotSelect = pm.optionMenu("optionMenu_pivotSelect", w=128, h=20, cc=pm.Callback(self.OptionMenu_change))
                            self.menuItem_pivotSelection = pm.menuItem("menuItem_pivotSelection", parent=self.optionMenu_pivotSelect, label=u"選択の中心")
                            self.menuItem_pivotObject = pm.menuItem("menuItem_pivotObject", parent=self.optionMenu_pivotSelect, label=u"オブジェクトの中心")
                            self.menuItem_pivotPosision = pm.menuItem("menuItem_pivotPosision", parent=self.optionMenu_pivotSelect, label=u"座標を指定")

                        self.separator_pivotTopSpace = pm.separator("separator_pivotTopSpace", w=1, h=2, style="none")

                        #ピボットX
                        self.rowLayout_pivotX = pm.rowLayout("rowLayout_pivotX", numberOfColumns=2)
                        with self.rowLayout_pivotX:
                            self.text_pivotXLabel = pm.text("text_pivotXLabel", align="left", label=u"pivX : ")
                            self.floatField_pivotXValue = pm.floatField("floatField_pivotXValue", w=91, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))

                        self.separator_pivotXYSpace = pm.separator("separator_pivotXYSpace", w=1, h=2, style="none")

                        #ピボットY
                        self.rowLayout_pivotY = pm.rowLayout("rowLayout_pivotY", numberOfColumns=2)
                        with self.rowLayout_pivotY:
                            self.text_pivotYLabel = pm.text("text_pivotYLabel", align="left", label=u"pivY : ")
                            self.floatField_pivotYValue = pm.floatField("floatField_pivotYValue", w=91, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))

                        self.separator_pivotYZSpace = pm.separator("separator_pivotYZSpace", w=1, h=2, style="none")

                        #ピボットZ
                        self.rowLayout_pivotZ = pm.rowLayout("rowLayout_pivotZ", numberOfColumns=2)
                        with self.rowLayout_pivotZ:
                            self.text_pivotZLabel = pm.text("text_pivotZLabel", align="left", label=u"pivZ : ")
                            self.floatField_pivotZValue = pm.floatField("floatField_pivotZValue", w=91, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))

                        self.separator_pivotBottomSpace = pm.separator("separator_pivotBottomSpace", w=1, h=3, style="none")

                        #自動入力ボタン
                        self.button_inputPivotPos = pm.button("button_inputPivotPos", w=125, h=20,
                                                            label=u"選択位置自動入力",
                                                            annotation=u"選択中の 「 頂点 」 か 「 ノード (Transform) 」 のワールド座標を自動入力します。",
                                                            bgc=[0.7,0.7,0.7],
                                                            command=pm.Callback(self.inputPivotPos))

        #前回の設定を復帰
        self.restoreParam(loadedConfigInfo)

        #ウィンドウのサイズ変更
        winWidthValue = 160
        winHeightValue = 618
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue += 6
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    #-------------------------
    #トランスフォーム(移動・回転・スケール)
    def transform(self, mode, direction, plus_or_minus):
        selItems = pm.ls(sl=1, flatten=1)
        if len(selItems) == 0:
            self.showMessage(u"操作対象が1つも選択されていません。")

        if mode == "move":
            self.move(direction, plus_or_minus)
        elif mode == "rotate":
            self.rotate(direction, plus_or_minus)
        elif mode == "scale":
            self.scale(direction, plus_or_minus)

        return

    #-------------------------
    #移動
    def move(self, direction, plus_or_minus):
        moveValues = self.getEditValue("move", direction, plus_or_minus)
        moveSpaceValue = self.getOptionMenuValue("optionMenu_moveSpace")

        wsValue = 0
        lsValue = 0
        osValue = 0
        if moveSpaceValue == "world":
            wsValue = 1
        elif moveSpaceValue == "local":
            lsValue = 1
        elif moveSpaceValue == "object":
            osValue = 1

        pm.move(moveValues, relative=1, worldSpace=wsValue, localSpace=lsValue, objectSpace=osValue)

        return

    #-------------------------
    #回転
    def rotate(self, direction, plus_or_minus):
        rotateValues = self.getEditValue("rotate", direction, plus_or_minus)
        rotateSpaceValue = self.getOptionMenuValue("optionMenu_rotateSpace")

        #ピボット情報を取得
        pivotPos = self.getPivotInfo()

        wsValue = 0
        osValue = 0
        if rotateSpaceValue == "world":
            wsValue = 1
        elif rotateSpaceValue == "object":
            osValue = 1

        if len(pivotPos) == 3:
            pm.rotate(rotateValues, relative=1, worldSpace=wsValue, objectSpace=osValue, pivot=pivotPos)
        else:
            pm.rotate(rotateValues, relative=1, worldSpace=wsValue, objectSpace=osValue)

        return

    #-------------------------
    #スケール
    def scale(self, direction, plus_or_minus):
        scaleValues = self.getEditValue("scale", direction, plus_or_minus)

        #ピボット情報を取得
        pivotPos = self.getPivotInfo()

        if len(pivotPos) == 3:
            pm.scale(scaleValues, relative=1, pivot=pivotPos)
        else:
            pm.scale(scaleValues, relative=1)

        return

    #-------------------------
    #編集値を取得
    def getEditValue(self, mode, direction, plus_or_minus):
        editValues = []
        if mode == "move":
            editValues = [0, 0, 0]
        elif mode == "rotate":
            editValues = [0, 0, 0]
        elif mode == "scale":
            editValues = [1, 1, 1]

        if mode == "scale" and direction == "all":
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
                    currentControlName = "floatField_" + mode + currentDirection.upper() + "Value"
                    if currentControlName in self.__dict__:
                        currentEditValue = self.__dict__[currentControlName].getValue()
                        if plus_or_minus == "minus":
                            if mode == "scale":
                                if sys.version_info.major == 2:
                                    currentEditValue = 1 / currentEditValue
                                else:
                                    # for Maya 2022-
                                    currentEditValue = old_div(1, currentEditValue)
                            else:
                                currentEditValue = -(currentEditValue)

                    editValues[direction_index[currentDirection]] = currentEditValue

        return editValues

    #-------------------------
    #ピボット情報を取得
    def getPivotInfo(self):
        pivotPos = []

        selItems = mc.ls(sl=1)

        componentFlag = 0
        for currentItem in selItems:
            if re.search("\.", currentItem):
                componentFlag = 1
            else:
                if componentFlag == 1:
                    componentFlag = 0

        #コンポーネント選択モードの場合
        if componentFlag:
            pivotSelectValue = self.getOptionMenuValue("optionMenu_pivotSelect")

            if pivotSelectValue == "selCenter":
                #選択アイテムの位置情報を取得
                selItemPosInfo = getSelItemPosInfo.get("world")

                #選択アイテムの中心座標
                pivotPos = selItemPosInfo["cenPos"]

            elif pivotSelectValue == "objCenter":
                pass

            elif pivotSelectValue == "usePosValue":
                pivotPos.append(self.floatField_pivotXValue.getValue())
                pivotPos.append(self.floatField_pivotYValue.getValue())
                pivotPos.append(self.floatField_pivotZValue.getValue())

        return pivotPos

    #-------------------------
    #2点間の距離を取得して自動入力
    def input2PointDistance(self):
        selItems = pm.ls(sl=1, flatten=1)

        #選択アイテムの座標を取得
        posList = []
        for currentItem in selItems:
            #Transformノードの場合
            if type(currentItem) == pm.nodetypes.Transform:
                #ワールド座標
                currentWorldPos = currentItem.getTranslation(space="world")
                posList.append(currentWorldPos)

            #頂点の場合
            elif type(currentItem) == pm.general.MeshVertex or type(currentItem) == pm.general.NurbsSurfaceCV or type(currentItem) == pm.general.NurbsCurveCV:
                #ワールド座標
                currentWorldPos = pm.pointPosition(currentItem, world=1)
                posList.append(currentWorldPos)

        if len(posList) != 2:
            self.showMessage(u"「2頂点」か「2ノード(Transform)」を選択してから実行して下さい。")
            return

        #2点間の距離
        distanceValues = []
        for i in range(3):
            currentDistanceValue = posList[0][i] - posList[1][i]
            if currentDistanceValue < 0:
                currentDistanceValue *= -1
            distanceValues.append(currentDistanceValue)

        #UIに入力
        self.floatField_moveXValue.setValue(distanceValues[0])
        self.floatField_moveYValue.setValue(distanceValues[1])
        self.floatField_moveZValue.setValue(distanceValues[2])

        self.saveConfig()

        return

    #-------------------------
    #ピボット座標を自動入力
    def inputPivotPos(self):
        #選択アイテムの位置情報を取得
        selItemPosInfo = getSelItemPosInfo.get("world")

        #選択アイテムの中心座標
        selCenterPos = selItemPosInfo["cenPos"]

        #UIに入力
        self.floatField_pivotXValue.setValue(selCenterPos[0])
        self.floatField_pivotYValue.setValue(selCenterPos[1])
        self.floatField_pivotZValue.setValue(selCenterPos[2])

        self.saveConfig()

        return

    #-------------------------
    #メッセージを表示
    def showMessage(self, messageStr):
        print(u"#    " + messageStr)
        pm.confirmDialog(title=toolName, message=u"● " + messageStr)
        return

    #-------------------------
    #オプションメニューの状態が変更された時の処理
    def OptionMenu_change(self):
        self.editControlStatus()
        self.saveConfig()

        return

    #-------------------------
    #コントロールの状態を変更する
    def editControlStatus(self):
        #Pivot用チェックボックスの状態によってコントロールの状態を変更する
        pivotSelectValue = self.getOptionMenuValue("optionMenu_pivotSelect")

        usePivotValue = 0
        if pivotSelectValue == "selCenter" or pivotSelectValue == "objCenter":
            pass
        elif pivotSelectValue == "usePosValue":
            usePivotValue = 1

        self.floatField_pivotXValue.setEnable(usePivotValue)
        self.floatField_pivotYValue.setEnable(usePivotValue)
        self.floatField_pivotZValue.setEnable(usePivotValue)
        self.button_inputPivotPos.setEnable(usePivotValue)

        return

    #-------------------------
    #オプションメニューの選択値を取得
    def getOptionMenuValue(self, optionMenuName):
        optionMenuValue = ""

        if optionMenuName in self.__dict__:
            selMenuItemLabel = self.__dict__[optionMenuName].getValue()
            optionMenuValue = self.getMenuItemStr(optionMenuName, selMenuItemLabel, "label_value")

        return optionMenuValue

    #-------------------------
    #オプションメニューのメニュー項目(文字列)を取得
    def getMenuItemStr(self, optionMenuName, source, mode):
        menuItemStr = ""

        #{コントロール名:ラベル:値}
        optionMenuName_label_value = {}

        optionMenuName_label_value["optionMenu_moveSpace"] = {}
        optionMenuName_label_value["optionMenu_moveSpace"][u"ワールド"] = "world"
        optionMenuName_label_value["optionMenu_moveSpace"][u"ローカル"] = "local"
        optionMenuName_label_value["optionMenu_moveSpace"][u"オブジェクト"] = "object"

        optionMenuName_label_value["optionMenu_rotateSpace"] = {}
        optionMenuName_label_value["optionMenu_rotateSpace"][u"ワールド"] = "world"
        optionMenuName_label_value["optionMenu_rotateSpace"][u"オブジェクト"] = "object"

        optionMenuName_label_value["optionMenu_pivotSelect"] = {}
        optionMenuName_label_value["optionMenu_pivotSelect"][u"選択の中心"] = "selCenter"
        optionMenuName_label_value["optionMenu_pivotSelect"][u"オブジェクトの中心"] = "objCenter"
        optionMenuName_label_value["optionMenu_pivotSelect"][u"座標を指定"] = "usePosValue"

        #ラベルから値を取得
        if mode == "label_value":
            if optionMenuName in optionMenuName_label_value:
                if source in optionMenuName_label_value[optionMenuName]:
                    menuItemStr = optionMenuName_label_value[optionMenuName][source]

        #値からラベルを取得
        elif mode == "value_label":
            #{コントロール名:値:ラベル}
            optionMenuName_value_label = {}
            for currentOptionMenuName in optionMenuName_label_value:
                optionMenuName_value_label[currentOptionMenuName] = {}
                for currentLabel in optionMenuName_label_value[currentOptionMenuName]:
                    currentValue = optionMenuName_label_value[currentOptionMenuName][currentLabel]
                    optionMenuName_value_label[currentOptionMenuName][currentValue] = currentLabel

            if optionMenuName in optionMenuName_value_label:
                if source in optionMenuName_value_label[optionMenuName]:
                    menuItemStr = optionMenuName_value_label[optionMenuName][source]

        return menuItemStr

    #-------------------------
    #前回の設定を復帰
    def restoreParam(self, loadedConfigInfo):
        for currentParamName in loadedConfigInfo:
            currentControlName = ""
            if currentParamName in ("moveSpace", "rotateSpace", "pivotSelect"):
                currentControlName = "optionMenu_" + currentParamName
            else:
                currentControlName = "floatField_" + currentParamName + "Value"

            if currentControlName in self.__dict__:
                try:
                    self.__dict__[currentControlName].setValue(loadedConfigInfo[currentParamName])
                except:
                    pass

        self.editControlStatus()
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
                    currentValue = paramParts[1]

                    if currentParamName in ("moveSpace", "rotateSpace", "pivotSelect"):
                        currentValue = self.getMenuItemStr("optionMenu_" + currentParamName, currentValue, "value_label")
                    else:
                        currentValue = float(currentValue)

                    loadedConfigInfo[currentParamName] = currentValue

        return loadedConfigInfo

    #-------------------------
    #設定を保存
    def saveConfig(self):
        configInfo = {}

        #{パラメーター名:値}
        for currentMode in ("move", "rotate", "scale", "pivot"):
            for currentDirection in ("all", "x", "y", "z"):
                currentParamName = currentMode + currentDirection.upper()
                currentControlName = "floatField_" + currentParamName + "Value"

                if currentControlName in self.__dict__:
                    currentEditValue = self.__dict__[currentControlName].getValue()
                    configInfo[currentParamName] = str(currentEditValue)

        configInfo["moveSpace"] = self.getOptionMenuValue("optionMenu_moveSpace")
        configInfo["rotateSpace"] = self.getOptionMenuValue("optionMenu_rotateSpace")
        configInfo["pivotSelect"] = self.getOptionMenuValue("optionMenu_pivotSelect")

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
if __name__ == "__main__":
    main()
