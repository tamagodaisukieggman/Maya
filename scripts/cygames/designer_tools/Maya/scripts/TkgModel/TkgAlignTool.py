# -*- coding: utf-8 -*-

"""
整列ツール

"""
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass


toolName = "TkgAlignTool"
__author__ = "TKG,  Yuta Kimura"

import os
import pymel.core as pm

from TkgComponent import getSelItemPosInfo
reload(getSelItemPosInfo)

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
        self.window = pm.window(toolName, title=u"整列ツール", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            self.columnLayout_top = pm.columnLayout("columnLayout_top", columnOffset=("left", 5))
            with self.columnLayout_top:
                self.separator_topSpace = pm.separator("separator_topSpace", w=1, h=5, style="none")

                #整列オプションメニュー
                self.rowLayout_alignSpace = pm.rowLayout("rowLayout_alignSpace", numberOfColumns=2)
                with self.rowLayout_alignSpace:
                    self.text_alignSpace = pm.text("text_alignSpace", align="left", label=u" 空間 : ")

                    self.optionMenu_alignSpace = pm.optionMenu("optionMenu_alignSpace", w=198, h=20, cc=pm.Callback(self.OptionMenu_change))
                    self.menuItem_alignWorld = pm.menuItem("menuItem_alignWorld", parent=self.optionMenu_alignSpace, label=u"ワールド")
                    self.menuItem_alignObject = pm.menuItem("menuItem_alignObject", parent=self.optionMenu_alignSpace, label=u"オブジェクト")

                self.separator_space1 = pm.separator("separator_space1", w=1, h=4, style="none")

                #自動入力ボタン
                self.button_input2PointDistance = pm.button("button_input2PointDistance", w=240 , h=20,
                                                            label=u"↓選択位置取得(ワールド)",
                                                            annotation=u"選択中の 「 頂点 」 か 「 ノード (Transform) 」 のワールド座標を自動入力します。",
                                                            bgc=[0.7,0.7,0.7],
                                                            command=pm.Callback(self.inputAlignPos))

                self.separator_space2 = pm.separator("separator_space2", w=1, h=3, style="none")

                self.rowLayout_align1 = pm.rowLayout("rowLayout_align1", numberOfColumns=3)
                with self.rowLayout_align1:
                    #移動X
                    self.columnLayout_alignX1 = pm.columnLayout("columnLayout_alignX1", rowSpacing=2)
                    with self.columnLayout_alignX1:
                        self.floatField_alignXValue = pm.floatField("floatField_alignXValue", w=76, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_alignX = pm.button("button_alignX", w=76, h=20, label=u"X 整列", bgc=[0.8,0.6,0.6], command=pm.Callback(self.align, "x", "value"))

                    #移動Y
                    self.columnLayout_alignY1 = pm.columnLayout("columnLayout_alignY1", rowSpacing=2)
                    with self.columnLayout_alignY1:
                        self.floatField_alignYValue = pm.floatField("floatField_alignYValue", w=76, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_alignY = pm.button("button_alignY", w=76, h=20, label=u"Y 整列", bgc=[0.6,0.8,0.6], command=pm.Callback(self.align, "y", "value"))

                    #移動Z
                    self.columnLayout_alignZ1 = pm.columnLayout("columnLayout_alignZ1", rowSpacing=2)
                    with self.columnLayout_alignZ1:
                        self.floatField_alignZValue = pm.floatField("floatField_alignZValue", w=76, h=22, cc=pm.Callback(self.saveConfig), ec=pm.Callback(self.saveConfig))
                        self.button_alignZ = pm.button("button_alignZ", w=76, h=20, label=u"Z 整列", bgc=[0.6,0.8,0.9], command=pm.Callback(self.align, "z", "value"))

                self.separator_space3 = pm.separator("separator_space3", w=240, h=10, style="in")

                self.rowLayout_align2 = pm.rowLayout("rowLayout_align2", numberOfColumns=3)
                with self.rowLayout_align2:
                    #移動X
                    self.columnLayout_alignX2 = pm.columnLayout("columnLayout_alignX2", rowSpacing=2)
                    with self.columnLayout_alignX2:
                        self.button_alignXMax = pm.button("button_alignXMax", w=76, h=20, label=u"X 最大", bgc=[0.8,0.6,0.6], command=pm.Callback(self.align, "x", "max"))
                        self.button_alignXCen = pm.button("button_alignXCen", w=76, h=20, label=u"X 中央", bgc=[0.8,0.6,0.6], command=pm.Callback(self.align, "x", "cen"))
                        self.button_alignXMin = pm.button("button_alignXMin", w=76, h=20, label=u"X 最小", bgc=[0.8,0.6,0.6], command=pm.Callback(self.align, "x", "min"))

                    #移動Y
                    self.columnLayout_alignY2 = pm.columnLayout("columnLayout_alignY2", rowSpacing=2)
                    with self.columnLayout_alignY2:
                        self.button_alignYMax = pm.button("button_alignYMax", w=76, h=20, label=u"Y 最大", bgc=[0.6,0.8,0.6], command=pm.Callback(self.align, "y", "max"))
                        self.button_alignYCen = pm.button("button_alignYCen", w=76, h=20, label=u"Y 中央", bgc=[0.6,0.8,0.6], command=pm.Callback(self.align, "y", "cen"))
                        self.button_alignYMin = pm.button("button_alignYMin", w=76, h=20, label=u"Y 最小", bgc=[0.6,0.8,0.6], command=pm.Callback(self.align, "y", "min"))

                    #移動Z
                    self.columnLayout_alignZ2 = pm.columnLayout("columnLayout_alignZ2", rowSpacing=2)
                    with self.columnLayout_alignZ2:
                        self.button_alignZMax = pm.button("button_alignZMax", w=76, h=20, label=u"Z 最大", bgc=[0.6,0.8,0.9], command=pm.Callback(self.align, "z", "max"))
                        self.button_alignZCen = pm.button("button_alignZCen", w=76, h=20, label=u"Z 中央", bgc=[0.6,0.8,0.9], command=pm.Callback(self.align, "z", "cen"))
                        self.button_alignZMin = pm.button("button_alignZMin", w=76, h=20, label=u"Z 最小", bgc=[0.6,0.8,0.9], command=pm.Callback(self.align, "z", "min"))

        #前回の設定を復帰
        self.restoreParam(loadedConfigInfo)

        #ウィンドウのサイズ変更
        winWidthValue = 252
        winHeightValue = 187
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue = winHeightValue
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    #-------------------------
    #整列
    def align(self, direction, valueMode):
        selItems = pm.ls(sl=1, flatten=1)
        if len(selItems) == 0:
            self.showMessage(u"操作対象が1つも選択されていません。")

        alignValues = self.getEditValue(valueMode)
        alignSpaceValue = self.getOptionMenuValue("optionMenu_alignSpace")

        mxValue = 0
        myValue = 0
        mzValue = 0
        alignValue = 0
        if direction == "x":
            mxValue = 1
            alignValue = alignValues[0]
        elif direction == "y":
            myValue = 1
            alignValue = alignValues[1]
        elif direction == "z":
            mzValue = 1
            alignValue = alignValues[2]

        wsValue = 0
        osValue = 0
        if alignSpaceValue == "world":
            wsValue = 1
        elif alignSpaceValue == "object":
            osValue = 1

        #絶対移動
        pm.move(alignValue, absolute=1, moveX=mxValue, moveY=myValue, moveZ=mzValue, worldSpace=wsValue, objectSpace=osValue)

        return

    #-------------------------
    #編集値を取得
    def getEditValue(self, valueMode):
        editValues = [0, 0, 0]

        if valueMode == "value":
            editValues[0] = self.floatField_alignXValue.getValue()
            editValues[1] = self.floatField_alignYValue.getValue()
            editValues[2] = self.floatField_alignZValue.getValue()
        else:
            alignSpaceValue = self.getOptionMenuValue("optionMenu_alignSpace")

            #選択アイテムの位置情報を取得
            selItemPosInfo = getSelItemPosInfo.get(alignSpaceValue)

            if valueMode == "cen":
                editValues = selItemPosInfo["cenPos"]
            elif valueMode == "max":
                editValues = selItemPosInfo["maxPos"]
            elif valueMode == "min":
                editValues = selItemPosInfo["minPos"]

        return editValues

    #-------------------------
    #選択アイテムから座標を自動入力
    def inputAlignPos(self):
        alignSpaceValue = self.getOptionMenuValue("optionMenu_alignSpace")

        #選択アイテムの位置情報を取得
        selItemPosInfo = getSelItemPosInfo.get(alignSpaceValue)

        #UIに入力
        self.floatField_alignXValue.setValue(selItemPosInfo["cenPos"][0])
        self.floatField_alignYValue.setValue(selItemPosInfo["cenPos"][1])
        self.floatField_alignZValue.setValue(selItemPosInfo["cenPos"][2])

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
        alignSpaceValue = self.getOptionMenuValue("optionMenu_alignSpace")

        #座標取得ボタンのラベルを変更する
        buttonLabel = ""
        if alignSpaceValue == "world":
            buttonLabel = u"↓選択位置取得 (ワールド)"
        elif alignSpaceValue == "object":
            buttonLabel = u"↓選択位置取得 (オブジェクト)"
        self.button_input2PointDistance.setLabel(buttonLabel)

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
        optionMenuName_label_value["optionMenu_alignSpace"] = {}
        optionMenuName_label_value["optionMenu_alignSpace"][u"ワールド"] = "world"
        optionMenuName_label_value["optionMenu_alignSpace"][u"オブジェクト"] = "object"

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
            if currentParamName == "alignSpace":
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

                    if currentParamName == "alignSpace":
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
        for currentDirection in ("x", "y", "z"):
            currentParamName = "align" + currentDirection.upper()
            currentControlName = "floatField_" + currentParamName + "Value"

            if currentControlName in self.__dict__:
                currentEditValue = self.__dict__[currentControlName].getValue()
                configInfo[currentParamName] = str(currentEditValue)

        configInfo["alignSpace"] = self.getOptionMenuValue("optionMenu_alignSpace")

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
