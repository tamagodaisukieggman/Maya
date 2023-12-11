# -*- coding: utf-8 -*-

"""
キー調整ツール

"""

g_toolName = "CyKeyAdjuster"
__author__ = "Cygames, Inc. Yuta Kimura"

import os
import re

import maya.cmds as mc
import pymel.core as pm

from CyComponent import getSelItemPosInfo

#maya設定フォルダのパス
g_userAppDirPath = pm.internalVar(userAppDir=1)

#ツール設定のパス
g_configFolderPath = g_userAppDirPath + "Cygames/" + g_toolName
g_configFilePath = g_configFolderPath + "/" + g_toolName + ".ini"


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
        if pm.window(g_toolName, q=1, exists=1):
            pm.deleteUI(g_toolName)

        winWidthValue = 191
        winHeightValue = 717
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winWidthValue += 6
            winHeightValue += 6

        frameLayoutWidthValue = winWidthValue - 13

        frameLayoutBorderVisibleValue = 1

        #ウィンドウ
        self.window = pm.window(g_toolName, title=u"CyKeyAdjuster", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            with pm.columnLayout(columnOffset=("left", 5)):
                pm.separator(w=1, h=5, style="none")

                #移動
                with pm.frameLayout(bgc=[0.3,0.1,0.0], w=frameLayoutWidthValue, borderVisible=frameLayoutBorderVisibleValue, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"■ 選択キーの移動"):
                    with pm.columnLayout(rowSpacing=3, columnOffset=("left", 14)):
                        #自動入力ボタン
                        pm.button(w=154, h=20, label=u"↓2つの選択キーの差分取得", annotation=u"2つの選択キーの差分を測って入力", bgc=[1,1,1], command=pm.Callback(self.input2PointDistance))

                        #移動(時)
                        with pm.rowLayout(numberOfColumns=4):
                            pm.text(align="left", label=u"時 : ")
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを時-方向に相対移動", image1="CyKeyAdjuster/CyKeyAdjuster_moveTimeMinus.bmp", w=26, h=26, command=pm.Callback(self.transform, "move", "time", "minus"))
                            self.floatField_moveTimeValue = pm.floatField("floatField_moveTimeValue", w=70, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを時+方向に相対移動", image1="CyKeyAdjuster/CyKeyAdjuster_moveTimePlus.bmp", w=26, h=26, command=pm.Callback(self.transform, "move", "time", "plus"))

                        #移動(値)
                        with pm.rowLayout(numberOfColumns=4):
                            pm.text(align="left", label=u"値 : ")
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを値-方向に相対移動", image1="CyKeyAdjuster/CyKeyAdjuster_moveValueMinus.bmp", w=26, h=26, command=pm.Callback(self.transform, "move", "value", "minus"))
                            self.floatField_moveValueValue = pm.floatField("floatField_moveValueValue", w=70, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを値+方向に相対移動", image1="CyKeyAdjuster/CyKeyAdjuster_moveValuePlus.bmp", w=26, h=26, command=pm.Callback(self.transform, "move", "value", "plus"))

                pm.separator(w=frameLayoutWidthValue, h=20, style="single")

                #スケール
                with pm.frameLayout(bgc=[0.2,0.3,0.1], w=frameLayoutWidthValue, borderVisible=frameLayoutBorderVisibleValue, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"■ 選択キーのスケール"):
                    with pm.columnLayout(rowSpacing=3, columnOffset=("left", 14)):
                        #スケール(時)
                        with pm.rowLayout(numberOfColumns=4):
                            pm.text(align="left", label=u"時 : ")
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「時」方向に縮小 ※Pivot位置を使用", image1="CyKeyAdjuster/CyKeyAdjuster_scaleTimeDiv.bmp", w=26, h=26, command=pm.Callback(self.transform, "scale", "time", "div"))
                            self.floatField_scaleTimeValue = pm.floatField("floatField_scaleTimeValue", w=70, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「時」方向に拡大 ※Pivot位置を使用", image1="CyKeyAdjuster/CyKeyAdjuster_scaleTimeMlt.bmp", w=26, h=26, command=pm.Callback(self.transform, "scale", "time", "mlt"))

                        #スケール(値)
                        with pm.rowLayout(numberOfColumns=4):
                            pm.text(align="left", label=u"値 : ")
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「値」方向に縮小 ※Pivot位置を使用", image1="CyKeyAdjuster/CyKeyAdjuster_scaleValueDiv.bmp", w=26, h=26, command=pm.Callback(self.transform, "scale", "value", "div"))
                            self.floatField_scaleValueValue = pm.floatField("floatField_scaleValueValue", w=70, h=22, value=1, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「値」方向に拡大 ※Pivot位置を使用", image1="CyKeyAdjuster/CyKeyAdjuster_scaleValueMlt.bmp", w=26, h=26, command=pm.Callback(self.transform, "scale", "value", "mlt"))

                        pm.separator(w=1, h=5, style="none")

                        #ピボット
                        with pm.frameLayout(label=u"スケール用のPivot", borderStyle="etchedIn", font="plainLabelFont", w=frameLayoutWidthValue-30, marginWidth=7, marginHeight=5):
                            with pm.columnLayout():
                                #自動入力ボタン
                                pm.button(w=135, h=20, label=u"↓選択キーの位置取得", annotation=u"選択キーの時(フレーム)・値を取得して入力", bgc=[1,1,1], command=pm.Callback(self.inputPivotPos))

                                pm.separator(w=1, h=3, style="none")

                                #ピボット(時)
                                with pm.rowLayout(numberOfColumns=2):
                                    pm.text(align="left", label=u"時 Pivot : ")
                                    self.floatField_pivotTimeValue = pm.floatField("floatField_pivotTimeValue", w=70, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))

                                pm.separator(w=1, h=2, style="none")

                                #ピボット(値)
                                with pm.rowLayout(numberOfColumns=2):
                                    pm.text(align="left", label=u"値 Pivot : ")
                                    self.floatField_pivotValueValue = pm.floatField("floatField_pivotValueValue", w=70, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))

                pm.separator(w=frameLayoutWidthValue, h=20, style="single")

                #フレームレイアウト(整列)
                with pm.frameLayout(bgc=[0.1,0.2,0.3], w=frameLayoutWidthValue, borderVisible=frameLayoutBorderVisibleValue, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"■ 選択キーの整列"):
                    with pm.columnLayout(rowSpacing=3, columnOffset=("left", 14)):
                        #整列・時
                        with pm.rowLayout(numberOfColumns=4):
                            pm.text(align="left", label=u"時 :")
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「時」の最小値に整列", image1="CyKeyAdjuster/CyKeyAdjuster_alignTimeMin.bmp", w=40, h=26, command=pm.Callback(self.transform, "align", "time", "min"))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「時」の中間値に整列", image1="CyKeyAdjuster/CyKeyAdjuster_alignTimeCen.bmp", w=40, h=26, command=pm.Callback(self.transform, "align", "time", "cen"))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「時」の最大値に整列", image1="CyKeyAdjuster/CyKeyAdjuster_alignTimeMax.bmp", w=40, h=26, command=pm.Callback(self.transform, "align", "time", "max"))

                        #整列・値
                        with pm.rowLayout(numberOfColumns=4):
                            pm.text(align="left", label=u"値 :")
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「値」の最小値に整列", image1="CyKeyAdjuster/CyKeyAdjuster_alignValueMin.bmp", w=40, h=26, command=pm.Callback(self.transform, "align", "value", "min"))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「値」の中間値に整列", image1="CyKeyAdjuster/CyKeyAdjuster_alignValueCen.bmp", w=40, h=26, command=pm.Callback(self.transform, "align", "value", "cen"))
                            pm.iconTextButton(style="iconOnly", annotation=u"選択キーを「値」の最大値に整列", image1="CyKeyAdjuster/CyKeyAdjuster_alignValueMax.bmp", w=40, h=26, command=pm.Callback(self.transform, "align", "value", "max"))

                pm.separator(w=frameLayoutWidthValue, h=20, style="single")

                #フレームレイアウト(タンジェント)
                with pm.frameLayout(bgc=[0.5,0.1,0.4], w=frameLayoutWidthValue, borderVisible=frameLayoutBorderVisibleValue, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"■ 選択接線(Tangent)の編集"):
                    with pm.columnLayout(rowSpacing=5, columnOffset=("left", 2)):
                        #自動入力ボタン
                        pm.button(w=169, h=20, label=u"↓選択キーの接線情報を取得", annotation=u"選択キーの接線情報を取得して入力", bgc=[1,1,1], command=pm.Callback(self.inputTangentInfo))

                        #接線の角度
                        with pm.frameLayout(label=u"接線の角度", borderStyle="etchedIn", font="plainLabelFont", marginWidth=3, marginHeight=5):
                            with pm.rowLayout(numberOfColumns=5):
                                with pm.columnLayout():
                                    pm.text(h=22, align="left", label=u"in ")
                                    pm.text(h=22, align="left", label=u"out ")

                                #-ボタン
                                with pm.columnLayout():
                                    pm.button(w=16, h=20, label=u"-", annotation=u"in接線の現在の角度から減算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustMinus", "inAngle"))
                                    pm.button(w=16, h=20, label=u"-", annotation=u"out接線の現在の角度から減算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustMinus", "outAngle"))

                                with pm.columnLayout():
                                    self.floatField_inAngleValue = pm.floatField(w=60, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                                    self.floatField_outAngleValue = pm.floatField(w=60, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))

                                #+ボタン
                                with pm.columnLayout():
                                    pm.button(w=16, h=20, label=u"+", annotation=u"in接線の現在の角度に加算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustPlus", "inAngle"))
                                    pm.button(w=16, h=20, label=u"+", annotation=u"out接線の現在の角度に加算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustPlus", "outAngle"))

                                #適用ボタン
                                with pm.columnLayout():
                                    pm.button(w=32, h=20, label=u"適用", annotation=u"in接線の角度として適用", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "apply", "inAngle"))
                                    pm.button(w=32, h=20, label=u"適用", annotation=u"out接線の角度として適用", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "apply", "outAngle"))

                        #接線のウェイト
                        with pm.frameLayout(label=u"接線のウェイト", borderStyle="etchedIn", font="plainLabelFont", marginWidth=3, marginHeight=5):
                            with pm.rowLayout(numberOfColumns=5):
                                with pm.columnLayout():
                                    pm.text(h=22, align="left", label=u"in ")
                                    pm.text(h=22, align="left", label=u"out ")

                                #-ボタン
                                with pm.columnLayout():
                                    pm.button(w=16, h=20, label=u"-", annotation=u"in接線の現在のウェイト値から減算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustMinus", "inWeight"))
                                    pm.button(w=16, h=20, label=u"-", annotation=u"in接線の現在のウェイト値から減算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustMinus", "outWeight"))

                                with pm.columnLayout():
                                    self.floatField_inWeightValue = pm.floatField(w=60, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                                    self.floatField_outWeightValue = pm.floatField(w=60, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))

                                #+ボタン
                                with pm.columnLayout():
                                    pm.button(w=16, h=20, label=u"+", annotation=u"in接線の現在のウェイト値に加算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustPlus", "inWeight"))
                                    pm.button(w=16, h=20, label=u"+", annotation=u"out接線の現在のウェイト値に加算", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "adjustPlus", "outWeight"))

                                #適用ボタン
                                with pm.columnLayout():
                                    pm.button(w=32, h=20, label=u"適用", annotation=u"in接線のウェイト値として適用", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "apply", "inWeight"))
                                    pm.button(w=32, h=20, label=u"適用", annotation=u"in接線のウェイト値として適用", bgc=[0.7,0.7,0.7], command=pm.Callback(self.editTangent, "apply", "outWeight"))

        #前回の設定を復帰
        self.restoreParam(loadedConfigInfo)

        print(winWidthValue)
        print(winHeightValue)


        #ウィンドウのサイズ変更
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    #-------------------------
    #トランスフォーム(移動・スケール)
    def transform(self, mode, direction, valueMode):
        #選択キーの情報を取得
        selKeyInfo = self.getSelKeyInfo()

        if len(selKeyInfo["selKeyPos"]) == 0:
            self.showMessage(u"編集したいキーを1つ以上選択して下さい。")
            return

        if mode == "move":
            self.move(direction, valueMode)
        elif mode == "scale":
            self.scale(direction, valueMode)
        elif mode == "align":
            self.align(direction, valueMode, selKeyInfo)

        return

    #-------------------------
    #移動
    def move(self, direction, valueMode):
        moveValue = self.getEditValue("move", direction, valueMode)

        if direction == "time":
            mc.keyframe(relative=1, option="over", timeChange=moveValue)
        elif direction == "value":
            mc.keyframe(relative=1, option="over", valueChange=moveValue)

        return

    #-------------------------
    #スケール
    def scale(self, direction, valueMode):
        scaleValue = self.getEditValue("scale", direction, valueMode)

        #ピボット情報を取得
        pivotPos = self.getPivotInfo()

        if direction == "time":
            mc.scaleKey(timeScale=scaleValue, timePivot=pivotPos[0])
        elif direction == "value":
            mc.scaleKey(valueScale=scaleValue, valuePivot=pivotPos[1])

        return

    #-------------------------
    #整列
    def align(self, direction, valueMode, selKeyInfo):
        alignPos = [0, 0]
        if valueMode == "max":
            alignPos = selKeyInfo["maxPos"]
        elif valueMode == "min":
            alignPos = selKeyInfo["minPos"]
        elif valueMode == "cen":
            alignPos = selKeyInfo["cenPos"]

        if direction == "time":
            try:
                mc.keyframe(absolute=1, option="over", animation="keys", timeChange=alignPos[0])
            except:
                self.showMessage(u"同一カーブ内で複数のキーが選択されている場合は無効です。")
        elif direction == "value":
            mc.keyframe(absolute=1, option="over", animation="keys", valueChange=alignPos[1])

        return

    #-------------------------
    #接線を編集
    def editTangent(self, mode, targetParamName):
        editValue = self.__dict__["floatField_" + targetParamName + "Value"].getValue()

        if mode == "apply":
            if targetParamName is "inAngle":
                mc.keyTangent(absolute=1, inAngle=editValue)
            elif targetParamName is "outAngle":
                mc.keyTangent(absolute=1, outAngle=editValue)
            elif targetParamName is "inWeight":
                mc.keyTangent(absolute=1, inWeight=editValue)
            elif targetParamName is "outWeight":
                mc.keyTangent(absolute=1, outWeight=editValue)

        elif mode == "adjustPlus" or mode == "adjustMinus":
            if mode == "adjustMinus":
                editValue *= -1

            if targetParamName is "inAngle":
                mc.keyTangent(relative=1, inAngle=editValue)
            elif targetParamName is "outAngle":
                mc.keyTangent(relative=1, outAngle=editValue)
            elif targetParamName is "inWeight":
                mc.keyTangent(relative=1, inWeight=editValue)
            elif targetParamName is "outWeight":
                mc.keyTangent(relative=1, outWeight=editValue)

        return

    #-------------------------
    #編集値を取得
    def getEditValue(self, mode, direction, valueMode):
        editValue = 0
        if mode == "move":
            pass
        elif mode == "scale":
            editValue = 1

        controlName = "floatField_" + mode + direction.capitalize() + "Value"
        if controlName in self.__dict__:
            editValue = self.__dict__[controlName].getValue()
            if valueMode == "minus":
                editValue = -(editValue)
            elif valueMode == "div":
                editValue = 1 / editValue

        return editValue

    #-------------------------
    #ピボット情報を取得
    def getPivotInfo(self):
        pivotPos = []
        pivotPos.append(self.floatField_pivotTimeValue.getValue())
        pivotPos.append(self.floatField_pivotValueValue.getValue())

        return pivotPos

    #-------------------------
    #2点間の距離を取得して自動入力
    def input2PointDistance(self):
        #選択キーの情報を取得
        selKeyInfo = self.getSelKeyInfo()

        if len(selKeyInfo["selKeyPos"]) != 2:
            self.showMessage(u"キーを2つ選択して下さい。")
            return

        #2点間の距離
        distanceValues = []
        for i in range(2):
            currentDistanceValue = selKeyInfo["selKeyPos"][0][i] - selKeyInfo["selKeyPos"][1][i]
            if currentDistanceValue < 0:
                currentDistanceValue *= -1
            distanceValues.append(currentDistanceValue)

        #UIに入力
        self.floatField_moveTimeValue.setValue(distanceValues[0])
        self.floatField_moveValueValue.setValue(distanceValues[1])

        self.saveConfig()

        return

    #-------------------------
    #ピボット座標を自動入力
    def inputPivotPos(self):
        #選択キーの情報を取得
        selKeyInfo = self.getSelKeyInfo()

        #選択キーの中心座標
        selCenterPos = selKeyInfo["cenPos"]

        #UIに入力
        self.floatField_pivotTimeValue.setValue(selCenterPos[0])
        self.floatField_pivotValueValue.setValue(selCenterPos[1])

        self.saveConfig()

        return

    #-------------------------
    #Tangent情報を自動入力
    def inputTangentInfo(self):
        #選択キーの情報を取得
        selKeyInfo = self.getSelKeyInfo()

        #UIに入力
        self.floatField_inAngleValue.setValue(selKeyInfo["cenIa"])
        self.floatField_outAngleValue.setValue(selKeyInfo["cenOa"])
        self.floatField_inWeightValue.setValue(selKeyInfo["cenIw"])
        self.floatField_outWeightValue.setValue(selKeyInfo["cenOw"])

        self.saveConfig()

        return

    #-------------------------
    #選択キーの情報を取得
    def getSelKeyInfo(self):
        selKeyInfo = {}
        selKeyInfo["maxPos"] = [0, 0]
        selKeyInfo["minPos"] = [0, 0]
        selKeyInfo["cenPos"] = [0, 0]

        selKeyTimes = mc.keyframe(q=1, sl=1, timeChange=1)
        selKeyValues = mc.keyframe(q=1, sl=1, valueChange=1)

        selKeyInfo["selKeyPos"] = [ [selKeyTimes[i],selKeyValues[i]] for i in range(len(selKeyTimes)) ]

        if len(selKeyTimes) > 0 and len(selKeyValues) > 0:
            bBoxTimeMax = max(selKeyTimes)
            bBoxValueMax = max(selKeyValues)

            bBoxTimeMin = min(selKeyTimes)
            bBoxValueMin = min(selKeyValues)

            bBoxTimeCen = (bBoxTimeMin + bBoxTimeMax) / 2
            bBoxValueCen = (bBoxValueMin + bBoxValueMax) / 2

            selKeyInfo["maxPos"] = [bBoxTimeMax, bBoxValueMax]
            selKeyInfo["minPos"] = [bBoxTimeMin, bBoxValueMin]
            selKeyInfo["cenPos"] = [bBoxTimeCen, bBoxValueCen]

        #接線情報
        selKeyIaValues = []
        selKeyOaValues = []
        selKeyIwValues = []
        selKeyOwValues = []

        #カーブ
        selCurves = mc.keyframe(sl=1, q=1, name=1)
        for currentCurve in selCurves:
            print("curve : " + currentCurve)

            #インデックス
            selKeyIndexes = mc.keyframe(currentCurve, sl=1, q=1, indexValue=1)
            for currentIndex in selKeyIndexes:
                print("    id : " + str(currentIndex))

                #in接線の角度
                iaValues = mc.keyTangent(currentCurve, index=(currentIndex,currentIndex), q=1, inAngle=1)

                #out接線の角度
                oaValues = mc.keyTangent(currentCurve, index=(currentIndex,currentIndex), q=1, outAngle=1)

                #in接線のウェイト
                iwValues = mc.keyTangent(currentCurve, index=(currentIndex,currentIndex), q=1, inWeight=1)

                #out接線のウェイト
                owValues = mc.keyTangent(currentCurve, index=(currentIndex,currentIndex), q=1, outWeight=1)

                selKeyIaValues.append(iaValues[0])
                selKeyOaValues.append(oaValues[0])
                selKeyIwValues.append(iwValues[0])
                selKeyOwValues.append(owValues[0])

        if len(selKeyIndexes) > 0:
            selKeyInfo["maxIa"] = bBoxIaMax = max(selKeyIaValues)
            selKeyInfo["maxOa"] = bBoxOaMax = max(selKeyOaValues)
            selKeyInfo["maxIw"] = bBoxIwMax = max(selKeyIwValues)
            selKeyInfo["maxOw"] = bBoxOwMax = max(selKeyOwValues)

            selKeyInfo["minIa"] = bBoxIaMin = min(selKeyIaValues)
            selKeyInfo["minOa"] = bBoxOaMin = min(selKeyOaValues)
            selKeyInfo["minIw"] = bBoxIwMin = min(selKeyIwValues)
            selKeyInfo["minOw"] = bBoxOwMin = min(selKeyOwValues)

            selKeyInfo["cenIa"] = bBoxIaCen = (bBoxIaMin + bBoxIaMax) / 2
            selKeyInfo["cenOa"] = bBoxOaCen = (bBoxOaMin + bBoxOaMax) / 2
            selKeyInfo["cenIw"] = bBoxIwCen = (bBoxIwMin + bBoxIwMax) / 2
            selKeyInfo["cenOw"] = bBoxOwCen = (bBoxOwMin + bBoxOwMax) / 2

        return selKeyInfo

    #-------------------------
    #メッセージを表示
    def showMessage(self, messageStr):
        print(u"#    " + messageStr)
        pm.confirmDialog(title=g_toolName, message=u"● " + messageStr)
        return

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
        if os.path.isfile(g_configFilePath):
            f = open(g_configFilePath)
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
        for currentMode in ("move", "scale", "pivot"):
            for currentDirection in ("time", "value"):
                currentParamName = currentMode + currentDirection.capitalize()
                currentControlName = "floatField_" + currentParamName + "Value"

                if currentControlName in self.__dict__:
                    currentEditValue = self.__dict__[currentControlName].getValue()
                    configInfo[currentParamName] = str(currentEditValue)

        for currentParamName in ["inAngle","outAngle","inWeight","outWeight"]:
            currentControlName = "floatField_" + currentParamName + "Value"

            if currentControlName in self.__dict__:
                currentEditValue = self.__dict__[currentControlName].getValue()
                configInfo[currentParamName] = str(currentEditValue)

        allParamNames = configInfo.keys()
        allParamNames.sort()

        #設定情報を文字列にまとめる
        configString = ""
        for currentParamName in allParamNames:
            if configString != "":
                configString += "\n"
            configString += currentParamName + "@" + configInfo[currentParamName]

        #テキストファイルの書き込み
        if not os.path.isdir(g_configFolderPath):
            os.makedirs(g_configFolderPath)
        f = open(g_configFilePath, "w")
        f.write(configString)
        f.close()

        return


#-------------------------------------------------
if __name__ == "__main__":
    main()
