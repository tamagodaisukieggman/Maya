# -*- coding: utf-8 -*-

"""
UV調整ツール

"""

g_toolName = "CyUVAdjuster"
__author__ = "Cygames, Inc. Yuta Kimura"

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import os
import re
import math

import maya.cmds as mc
import maya.mel as mm
import pymel.core as pm

import CyConvertSelection
from CyComponent import getSelItemPosInfo

import CyOpenWebPage;reload(CyOpenWebPage)

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
        self.initFlg = 0

        #設定を読み込み
        self.loadedConfigInfo = self.loadConfig()

        #既にウィンドウが開いている場合は閉じる
        if pm.window(g_toolName, q=1, exists=1):
            pm.deleteUI(g_toolName)

        winWidthValue = 204
        winHeightValue = 745
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue += 6

        tabLayoutWidthValue = winWidthValue - 10
        tabLayoutHeightValue = winHeightValue - 26

        self.frameLayoutWidthValue = tabLayoutWidthValue - 18

        self.frameLayoutBorderVisibleValue = 1

        self.controlInfo = {}

        #ウィンドウ
        self.window = pm.window(g_toolName, title=g_toolName, minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            with pm.columnLayout(columnOffset=("left", 3)):
                pm.menuBarLayout()
                pm.menu(label="Help")
                pm.menuItem(label=u"ヘルプを開く", c=pm.Callback(CyOpenWebPage.open, "https://wisdom.cygames.jp/display/designersmanual/Maya%3A+UVAdjuster"))
                pm.menuItem(divider=1)
                pm.menuItem(label=u"設定をリセット", c=pm.Callback(self.resetConfig))

                #タブレイアウト
                with pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5, w=tabLayoutWidthValue, h=tabLayoutHeightValue):
                    #タブ1
                    with pm.columnLayout("Transform", columnOffset=("left", 5)):
                        pm.separator(w=1, h=5, style="none")

                        #対象パネル
                        self.pnl_target = TargetPanel(self)

                        pm.separator(w=1, h=12, style="none")

                        #移動パネル
                        self.pnl_move = MovePanel(self)

                        pm.separator(w=1, h=12, style="none")

                        #回転パネル
                        self.pnl_rotate = RotatePanel(self)

                        pm.separator(w=1, h=12, style="none")

                        #スケールパネル
                        self.pnl_scale = ScalePanel(self)

                        pm.separator(w=1, h=12, style="none")

                        #ピボットパネル
                        self.pnl_pivot = PivotPanel(self)

                    #タブ2
                    with pm.columnLayout("   Etc   ", columnOffset=("left", 5)):
                        pm.separator(w=1, h=5, style="none")

                        #マッピングパネル
                        self.pnl_mapping = MappingPanel(self)

                        pm.separator(w=1, h=12, style="none")

                        #その他パネル
                        self.pnl_etc = EtcPanel(self)

        #ウィンドウのサイズ変更
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        self.initFlg = 1

        return

    #-------------------------
    #floatフィールドの値を編集
    def FloatField_editValue(self, targetField, mode, editValue):
        currentValue = targetField.getValue()

        newValue = 0
        if mode == "+":
            newValue = currentValue + editValue

        elif mode == "-v":
            newValue = currentValue - editValue
        elif mode == "v-":
            newValue = editValue - currentValue

        elif mode == "*":
            newValue = currentValue * editValue

        elif mode == "/v":
            newValue = currentValue / editValue
        elif mode == "v/":
            newValue = editValue / currentValue

        elif mode == "invertSign":
            newValue = -(currentValue)
        elif mode == "value":
            newValue = editValue
        elif mode == "grid":
            #UVTextureEditorから情報を取得
            texWinName = pm.getPanel(scriptType="polyTexturePlacementPanel")
            texWinSpacingValue = pm.textureWindow(texWinName[0], q=1, spacing=1)
            newValue = texWinSpacingValue

        targetField.setValue(newValue)

        self.saveConfig()

        return

    #-------------------------
    #前回の設定を復帰
    def restoreParam(self, pnlObj):
        for controlName in pnlObj.controlNames:
            if controlName not in pnlObj.__dict__:
                continue

            controlNameParts = controlName.split("_")

            controlType = controlNameParts[0]
            paramName = controlName.replace(controlType + "_", "", 1)
            if paramName not in pnlObj.mWin.loadedConfigInfo:
                continue
            paramValue = pnlObj.mWin.loadedConfigInfo[paramName]

            if controlType == "ff": #floatフィールド
                pnlObj.__dict__[controlName].setValue(float(paramValue))
            elif controlType == "rc": #ラジオコレクション
                pnlObj.__dict__[controlName].setSelect(paramValue)
            elif controlType == "cb": #チェックボックス
                pnlObj.__dict__[controlName].setValue(int(paramValue))
            elif controlType == "om": #オプションメニュー
                if paramName in pnlObj.menuKey_menuId:
                    if paramValue in pnlObj.menuKey_menuId[paramName]:
                        menuId = int(pnlObj.menuKey_menuId[paramName][paramValue])
                        pnlObj.__dict__[controlName].setSelect(menuId)

        return

    #-------------------------
    #設定をリセット
    def resetConfig(self):
        for panelName in ["pnl_target", "pnl_move", "pnl_rotate", "pnl_scale", "pnl_pivot", "pnl_mapping"]:
            if panelName in self.__dict__:
                self.__dict__[panelName].resetConfig()

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
                    paramName = paramParts[0]
                    paramValue = paramParts[1]

                    loadedConfigInfo[paramName] = paramValue

        return loadedConfigInfo

    #-------------------------
    #設定を保存
    def saveConfig(self):
        if self.initFlg == 0:
            return

        #設定を取得
        paramName_value = {}
        for panelName in ["pnl_target", "pnl_move", "pnl_rotate", "pnl_scale", "pnl_pivot", "pnl_mapping"]:
            if panelName in self.__dict__:
                paramName_value.update(self.__dict__[panelName].getConfig())

        paramNames = paramName_value.keys()
        paramNames.sort()

        #設定情報を文字列にまとめる
        configStr = ""
        for paramName in paramNames:
            if configStr != "":
                configStr += "\n"
            configStr += paramName + "@" + str(paramName_value[paramName])

        #テキストファイルの書き込み
        if not os.path.isdir(g_configFolderPath):
            os.makedirs(g_configFolderPath)
        f = open(g_configFilePath, "w")
        f.write(configStr)
        f.close()

        return


#-------------------------------------------------
#対象パネル
class TargetPanel(object):
    def __init__(self, mainWindow):
        self.mWin = mainWindow

        self.controlNames = ["rc_target_mode"]

        #フレームレイアウト(対象)
        with pm.frameLayout(bgc=[0.1,0.1,0.1], w=self.mWin.frameLayoutWidthValue, borderVisible=self.mWin.frameLayoutBorderVisibleValue, marginWidth=2, marginHeight=2, labelVisible=1, font="plainLabelFont", label=u"操作対象"):
            with pm.columnLayout(rowSpacing=3):
                #ピボットモード
                with pm.rowLayout(numberOfColumns=3):
                    pm.separator(w=10, h=1, style="none")

                    self.rc_target_mode = pm.radioCollection()
                    pm.radioButton("normal", label=u"通常", cc=pm.Callback(self.RadioButton_change), w=75, select=1)
                    pm.radioButton("shell", label=u"UVシェル")
                    pm.setParent("..")

        #前回の設定を復帰
        self.mWin.restoreParam(self)

        return

    #-------------------------
    #ラジオボタンの状態が変更された時の処理
    def RadioButton_change(self):
        self.mWin.saveConfig()

        return

    #-------------------------
    #対象モードを取得
    def getTargetMode(self):
        targetMode = self.rc_target_mode.getSelect()

        return targetMode

    #-------------------------
    #設定をリセット
    def resetConfig(self):
        self.rc_target_mode.setSelect("normal")

        return

    #-------------------------
    #設定を取得
    def getConfig(self):
        paramName_value = {}

        paramName_value["target_mode"] = self.rc_target_mode.getSelect()

        return paramName_value


#-------------------------------------------------
#移動パネル
class MovePanel(object):
    def __init__(self, mainWindow):
        self.mWin = mainWindow

        self.controlNames = ["ff_move_uValue", "ff_move_vValue"]

        menuItemInfoList = []
        menuItemInfoList.append({"type":"command", "label":u"リセット", "mode":"value", "editValue":1})
        menuItemInfoList.append({"type":"divider"})
        menuItemInfoList.append({"type":"command", "label":u"現在のグリッドサイズ", "mode":"grid", "editValue":0})
        menuItemInfoList.append({"type":"divider"})
        menuItemInfoList.append({"type":"command", "label":u"値を32倍", "mode":"*", "editValue":32})
        menuItemInfoList.append({"type":"command", "label":u"値を16倍", "mode":"*", "editValue":16})
        menuItemInfoList.append({"type":"command", "label":u"値を8倍", "mode":"*", "editValue":8})
        menuItemInfoList.append({"type":"command", "label":u"値を4倍", "mode":"*", "editValue":4})
        menuItemInfoList.append({"type":"command", "label":u"値を2倍", "mode":"*", "editValue":2})
        menuItemInfoList.append({"type":"command", "label":u"値を1/2倍 (0.5倍)", "mode":"/v", "editValue":2})
        menuItemInfoList.append({"type":"command", "label":u"値を1/4倍 (0.25倍)", "mode":"/v", "editValue":4})
        menuItemInfoList.append({"type":"command", "label":u"値を1/8倍 (0.125倍)", "mode":"/v", "editValue":8})
        menuItemInfoList.append({"type":"command", "label":u"値を1/16倍 (0.0625倍)", "mode":"/v", "editValue":16})
        menuItemInfoList.append({"type":"command", "label":u"値を1/32倍 (0.03125倍)", "mode":"/v", "editValue":32})

        #フレームレイアウト(移動)
        with pm.frameLayout(bgc=[0.3,0.1,0.0], w=self.mWin.frameLayoutWidthValue, h=232, borderVisible=self.mWin.frameLayoutBorderVisibleValue, marginWidth=2, marginHeight=2, labelVisible=1, font="plainLabelFont", label=u"■ 移動"):
            with pm.columnLayout(rowSpacing=3):
                with pm.rowLayout(numberOfColumns=4):
                    pm.separator(w=9 , h=1, style="none")

                    #自動入力ボタン
                    pm.button(w=117, h=20, label=u"↓2頂点の距離を取得", annotation=u"選択した2つのUV頂点の距離を取得して自動入力", bgc=[1,1,1], c=pm.Callback(self.input2PointDistance))

                    pm.separator(w=3, h=1, style="none")

                    #FitPosition
                    pm.button(w=20, h=20, label=u"Fit", annotation=u"選択した2つのUV頂点の位置が一致するようにUVシェルを移動する", bgc=[1,0.8,0.5], c=pm.Callback(self.fitPosition))

                #移動値
                with pm.rowLayout(numberOfColumns=5):
                    #U移動値
                    pm.text(w=9, align="left", label=u"U ")
                    self.ff_move_uValue = pm.floatField(w=68, h=22, precision=6, value=1, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    for menuItemInfo in menuItemInfoList:
                        if menuItemInfo["type"] == "command":
                            pm.menuItem(label=menuItemInfo["label"], c=pm.Callback(self.mWin.FloatField_editValue, self.ff_move_uValue, menuItemInfo["mode"], menuItemInfo["editValue"]))
                        elif menuItemInfo["type"] == "divider":
                            pm.menuItem(divider=1)

                    pm.separator(w=2, h=1, style="none")

                    #V移動値
                    pm.text(w=9, align="left", label=u"V ")
                    self.ff_move_vValue = pm.floatField(w=68, h=22, precision=6, value=1, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    for menuItemInfo in menuItemInfoList:
                        if menuItemInfo["type"] == "command":
                            pm.menuItem(label=menuItemInfo["label"], c=pm.Callback(self.mWin.FloatField_editValue, self.ff_move_vValue, menuItemInfo["mode"], menuItemInfo["editValue"]))
                        elif menuItemInfo["type"] == "divider":
                            pm.menuItem(divider=1)

                #移動ボタン
                formLayout_move = pm.formLayout(h=155)
                with formLayout_move:
                    #定義
                    sp_moveButtonPos = pm.separator(w=1, h=1, style="none")

                    moveBtnA_WValue = 21
                    moveBtnB_WValue = 31
                    moveBtnC_WValue = 35

                    moveBtn_HValue = 20

                    #Up
                    btn_move_u_0 = pm.button(w=moveBtnA_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"↑",  c=pm.Callback(self.moveUV, "v", "plus", ""))
                    btn_move_u_5 = pm.button(w=moveBtnB_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"Grid",c=pm.Callback(self.moveUV, "v", "plus", "grid"))
                    btn_move_u_4 = pm.button(w=moveBtnB_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1/8", c=pm.Callback(self.moveUV, "v", "plus", "0.125"))
                    btn_move_u_3 = pm.button(w=moveBtnC_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1/4", c=pm.Callback(self.moveUV, "v", "plus", "0.25"))
                    btn_move_u_2 = pm.button(w=moveBtnC_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1/2", c=pm.Callback(self.moveUV, "v", "plus", "0.5"))
                    btn_move_u_1 = pm.button(w=moveBtnC_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1",     c=pm.Callback(self.moveUV, "v", "plus", "1"))

                    #Down
                    btn_move_d_0 = pm.button(w=moveBtnA_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"↓",  c=pm.Callback(self.moveUV, "v", "minus", ""))
                    btn_move_d_5 = pm.button(w=moveBtnB_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"Grid",c=pm.Callback(self.moveUV, "v", "minus", "grid"))
                    btn_move_d_4 = pm.button(w=moveBtnB_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1/8", c=pm.Callback(self.moveUV, "v", "minus", "0.125"))
                    btn_move_d_3 = pm.button(w=moveBtnC_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1/4", c=pm.Callback(self.moveUV, "v", "minus", "0.25"))
                    btn_move_d_2 = pm.button(w=moveBtnC_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1/2", c=pm.Callback(self.moveUV, "v", "minus", "0.5"))
                    btn_move_d_1 = pm.button(w=moveBtnC_WValue, h=moveBtn_HValue, bgc=[0.6,0.8,0.6], label=u"1",     c=pm.Callback(self.moveUV, "v", "minus", "1"))

                    #Right
                    btn_move_r_0 = pm.button(w=moveBtn_HValue, h=moveBtnA_WValue, bgc=[0.8,0.6,0.6], label=u"→",  c=pm.Callback(self.moveUV, "u", "plus", ""))
                    btn_move_r_5 = pm.button(w=moveBtn_HValue, h=moveBtnB_WValue, bgc=[0.8,0.6,0.6], label=u"G",     c=pm.Callback(self.moveUV, "u", "plus", "grid"))
                    btn_move_r_4 = pm.button(w=moveBtn_HValue, h=moveBtnB_WValue, bgc=[0.8,0.6,0.6], label=u"1/8", c=pm.Callback(self.moveUV, "u", "plus", "0.125"))
                    btn_move_r_3 = pm.button(w=moveBtn_HValue, h=moveBtnC_WValue, bgc=[0.8,0.6,0.6], label=u"1/4", c=pm.Callback(self.moveUV, "u", "plus", "0.25"))
                    btn_move_r_2 = pm.button(w=moveBtn_HValue, h=moveBtnC_WValue, bgc=[0.8,0.6,0.6], label=u"1/2", c=pm.Callback(self.moveUV, "u", "plus", "0.5"))
                    btn_move_r_1 = pm.button(w=moveBtn_HValue, h=moveBtnC_WValue, bgc=[0.8,0.6,0.6], label=u"1",     c=pm.Callback(self.moveUV, "u", "plus", "1"))

                    #Left
                    btn_move_l_0 = pm.button(w=moveBtn_HValue, h=moveBtnA_WValue, bgc=[0.8,0.6,0.6], label=u"←",  c=pm.Callback(self.moveUV, "u", "minus", ""))
                    btn_move_l_5 = pm.button(w=moveBtn_HValue, h=moveBtnB_WValue, bgc=[0.8,0.6,0.6], label=u"G",     c=pm.Callback(self.moveUV, "u", "minus", "grid"))
                    btn_move_l_4 = pm.button(w=moveBtn_HValue, h=moveBtnB_WValue, bgc=[0.8,0.6,0.6], label=u"1/8", c=pm.Callback(self.moveUV, "u", "minus", "0.125"))
                    btn_move_l_3 = pm.button(w=moveBtn_HValue, h=moveBtnC_WValue, bgc=[0.8,0.6,0.6], label=u"1/4", c=pm.Callback(self.moveUV, "u", "minus", "0.25"))
                    btn_move_l_2 = pm.button(w=moveBtn_HValue, h=moveBtnC_WValue, bgc=[0.8,0.6,0.6], label=u"1/2", c=pm.Callback(self.moveUV, "u", "minus", "0.5"))
                    btn_move_l_1 = pm.button(w=moveBtn_HValue, h=moveBtnC_WValue, bgc=[0.8,0.6,0.6], label=u"1",     c=pm.Callback(self.moveUV, "u", "minus", "1"))

                    #配置
                    pm.formLayout(formLayout_move, e=1, af=[(sp_moveButtonPos, "top", 75),  (sp_moveButtonPos, "left", 83)])

                    buttonMargin = 2

                    #Up
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_u_0, "bottom", 11,    sp_moveButtonPos),  (btn_move_u_0, "left", -11, sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_u_5, "bottom", buttonMargin, btn_move_u_0),   (btn_move_u_5, "right", 1,  sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_u_4, "bottom", buttonMargin, btn_move_u_0),   (btn_move_u_4, "left", 1,   sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_u_3, "bottom", buttonMargin, btn_move_u_4),   (btn_move_u_3, "right", buttonMargin,   btn_move_u_2)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_u_2, "bottom", buttonMargin, btn_move_u_4),   (btn_move_u_2, "right", -18,    sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_u_1, "bottom", buttonMargin, btn_move_u_4),   (btn_move_u_1, "left", buttonMargin,    btn_move_u_2)])

                    #Down
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_d_0, "top", 11,   sp_moveButtonPos),  (btn_move_d_0, "left", -11 ,    sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_d_5, "top", buttonMargin, btn_move_d_0),  (btn_move_d_5, "right", 1,      sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_d_4, "top", buttonMargin, btn_move_d_0),  (btn_move_d_4, "left", 1,       sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_d_3, "top", buttonMargin, btn_move_d_4),  (btn_move_d_3, "right", buttonMargin,       btn_move_d_2)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_d_2, "top", buttonMargin, btn_move_d_4),  (btn_move_d_2, "right", -18,    sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_d_1, "top", buttonMargin, btn_move_d_4),  (btn_move_d_1, "left", buttonMargin,        btn_move_d_2)])

                    #Right
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_r_0, "top", -11,  sp_moveButtonPos),  (btn_move_r_0, "left", 11,  sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_r_5, "top", 1,        sp_moveButtonPos),  (btn_move_r_5, "left", buttonMargin,    btn_move_r_0)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_r_4, "bottom", 1, sp_moveButtonPos),  (btn_move_r_4, "left", buttonMargin,    btn_move_r_0)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_r_3, "top", buttonMargin,     btn_move_r_2),  (btn_move_r_3, "left", buttonMargin,    btn_move_r_4)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_r_2, "top", -18,  sp_moveButtonPos),  (btn_move_r_2, "left", buttonMargin,    btn_move_r_4)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_r_1, "bottom", buttonMargin, btn_move_r_2),   (btn_move_r_1, "left", buttonMargin,    btn_move_r_4)])

                    #Left
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_l_0, "top", -11,  sp_moveButtonPos),  (btn_move_l_0, "right", 11,     sp_moveButtonPos)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_l_5, "top", 1,        sp_moveButtonPos),  (btn_move_l_5, "right", buttonMargin,   btn_move_l_0)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_l_4, "bottom", 1, sp_moveButtonPos),  (btn_move_l_4, "right", buttonMargin,   btn_move_l_0)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_l_3, "top", buttonMargin,     btn_move_l_2),  (btn_move_l_3, "right", buttonMargin,   btn_move_l_4)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_l_2, "top", -18,  sp_moveButtonPos),  (btn_move_l_2, "right", buttonMargin,   btn_move_l_4)])
                    pm.formLayout(formLayout_move, e=1, ac=[(btn_move_l_1, "bottom", buttonMargin, btn_move_l_2),   (btn_move_l_1, "right", buttonMargin,   btn_move_l_4)])

        #前回の設定を復帰
        self.mWin.restoreParam(self)

        return

    #-------------------------
    #2頂点の距離を取得
    def get2PointDistance(self):
        moveUValue = None
        moveVValue = None

        #選択UV情報を取得
        selUVInfo = getSelUVInfo()
        uvNameList = selUVInfo["uvNameList"]
        uvPosList = selUVInfo["uvPosList"]

        if len(uvNameList) != 2:
            messageStr = u"● 2つのUV頂点を順番に選択して下さい。"
            mc.confirmDialog(title=g_toolName, message=messageStr)
            return None, None, selUVInfo

        moveUValue = uvPosList[0][0] - uvPosList[1][0]
        moveVValue = uvPosList[0][1] - uvPosList[1][1]

        print(" [move U] : " + str(moveUValue) + " [get]")
        print(" [move V] : " + str(moveVValue) + " [get]")

        return moveUValue, moveVValue, selUVInfo

    #-------------------------
    #2点間の距離を取得して自動入力
    def input2PointDistance(self):
        #2頂点の距離を取得
        moveUValue, moveVValue, selUVInfo = self.get2PointDistance()
        if moveUValue is None or moveVValue is None:
            return

        moveUValue = math.fabs(moveUValue)
        moveVValue = math.fabs(moveVValue)

        print(" [move U] : " + str(moveUValue) + " [input]")
        print(" [move V] : " + str(moveVValue) + " [input]")

        #UIに入力
        self.ff_move_uValue.setValue(moveUValue)
        self.ff_move_vValue.setValue(moveVValue)

        print(" [move U] : " + str(self.ff_move_uValue.getValue()) + " [inputted]")
        print(" [move V] : " + str(self.ff_move_vValue.getValue()) + " [inputted]")

        self.mWin.saveConfig()

        return

    #-------------------------
    #移動
    def moveUV(self, direction, plus_or_minus, valueStr):
        selItems = pm.ls(sl=1, flatten=1)
        if len(selItems) == 0:
            showMessage(u"操作対象が1つも選択されていません。")
            return

        #選択UV情報を取得
        selUVInfo = getSelUVInfo()
        uvNameList = selUVInfo["uvNameList"]

        #編集値
        editValue = 0
        if valueStr == "":
            if direction == "u":
                editValue = self.ff_move_uValue.getValue()
            elif direction == "v":
                editValue = self.ff_move_vValue.getValue()
        elif valueStr == "grid":
            #UVTextureEditorから情報を取得
            texWinName = pm.getPanel(scriptType="polyTexturePlacementPanel")
            texWinSpacingValue = pm.textureWindow(texWinName[0], q=1, spacing=1)
            editValue = texWinSpacingValue
        else:
            editValue = float(valueStr)

        if plus_or_minus == "minus":
            editValue *= -1

        moveUValue = 0
        moveVValue = 0
        if direction == "u":
            moveUValue = editValue
            print(" [move U] : " + str(moveUValue))
        elif direction == "v":
            moveVValue = editValue
            print(" [move V] : " + str(moveVValue))

        #対象モードを取得
        targetMode = self.mWin.pnl_target.getTargetMode()

        if targetMode == "normal":
            mc.polyEditUV(uvNameList, relative=1, uValue=moveUValue, vValue=moveVValue)
        elif targetMode == "shell":
            mc.polyEditUVShell(relative=1, uValue=moveUValue, vValue=moveVValue)

        return

    #-------------------------
    #位置を一致させる
    def fitPosition(self):
        #2頂点の距離を取得
        moveUValue, moveVValue, selUVInfo = self.get2PointDistance()
        if moveUValue is None or moveVValue is None:
            return

        uvNameList = selUVInfo["uvNameList"]
        uvPosList = selUVInfo["uvPosList"]

        #移動
        mc.select(uvNameList[-1], r=1)
        mc.polyEditUVShell(relative=1, uValue=moveUValue, vValue=moveVValue)
        print(" [move U] : " + str(moveUValue) + " [fit]")
        print(" [move V] : " + str(moveVValue) + " [fit]")

        #選択を復帰
        mc.select(cl=1)
        for uvName in uvNameList:
            mc.select(uvName, add=1)

        return

    #-------------------------
    #設定をリセット
    def resetConfig(self):

        self.ff_move_uValue.setValue(1)
        self.ff_move_vValue.setValue(1)

        return

    #-------------------------
    #設定を取得
    def getConfig(self):
        paramName_value = {}

        paramName_value["move_uValue"] = self.ff_move_uValue.getValue()
        paramName_value["move_vValue"] = self.ff_move_vValue.getValue()

        return paramName_value


#-------------------------------------------------
#回転パネル
class RotatePanel(object):
    def __init__(self, mainWindow):
        self.mWin = mainWindow

        self.controlNames = ["ff_rotate_degValue"]

        #フレームレイアウト(回転)
        with pm.frameLayout(bgc=[0.2,0.3,0.1], w=self.mWin.frameLayoutWidthValue, borderVisible=self.mWin.frameLayoutBorderVisibleValue, marginWidth=2, marginHeight=2, labelVisible=1, font="plainLabelFont", label=u"■ 回転"):
            with pm.columnLayout(rowSpacing=3):
                with pm.rowLayout(numberOfColumns=4):
                    pm.separator(w=9 , h=1, style="none")

                    #自動入力ボタン
                    annotationValue = u"2UV頂点 : 選択したエッジ(2つのUV頂点)と水平線間の角度を自動入力"
                    annotationValue += u"\n"
                    annotationValue += u"3UV頂点 : 選択した1点を共有する2つのエッジ(3つのUV頂点)の間の角度を自動入力"
                    annotationValue += u"\n"
                    annotationValue += u"4UV頂点 : 選択した2つのエッジ(2+2=4つのUV頂点)の間の角度を自動入力"
                    pm.button(w=117, h=20, label=u"↓エッジの角度を取得", annotation=annotationValue, bgc=[1,1,1], c=pm.Callback(self.inputEdgeAngle))

                    pm.separator(w=3, h=1, style="none")

                    #FitRotate
                    annotationValue = u"2UV頂点 : 選択したエッジ(2つのUV頂点)が垂直or水平になるようにUVシェルを回転する"
                    annotationValue += u"\n"
                    annotationValue += u"4UV頂点 : 選択した2つのエッジ(2+2=4つのUV頂点)の角度が一致するようにUVシェルを回転する"
                    pm.button(w=20, h=20, label=u"Fit", annotation=annotationValue, bgc=[1,0.8,0.5], c=pm.Callback(self.fitRotate))

                with pm.rowLayout(numberOfColumns=2):
                    pm.text(align="left", label=u"      角度 ")
                    self.ff_rotate_degValue = pm.floatField(w=85, h=22, precision=3, value=0, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    pm.menuItem(label=u"リセット", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "value", 0))
                    pm.menuItem(divider=1)
                    pm.menuItem(label=u"+/- を反転", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "invertSign", 0))
                    pm.menuItem(divider=1)
                    pm.menuItem(label=u"現在の値 + 360", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "+", 360))
                    pm.menuItem(label=u"現在の値 + 180", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "+", 180))
                    pm.menuItem(label=u"現在の値 + 90", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "+", 90))
                    pm.menuItem(label=u"現在の値 - 90", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "-v", 90))
                    pm.menuItem(label=u"現在の値 - 180", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "-v", 180))
                    pm.menuItem(label=u"現在の値 - 360", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "-v", 360))
                    pm.menuItem(divider=1)
                    pm.menuItem(label=u"90 - 現在の値", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "v-", 90))
                    pm.menuItem(label=u"180 - 現在の値", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "v-", 180))
                    pm.menuItem(label=u"360 - 現在の値", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "v-", 360))
                    pm.menuItem(divider=1)
                    pm.menuItem(label=u"値を2倍", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "*", 2))
                    pm.menuItem(label=u"値を1/2倍 (0.5倍)", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "/v", 2))
                    pm.menuItem(divider=1)
                    pm.menuItem(label=u"180 (1/2)", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "value", 180))
                    pm.menuItem(label=u"90 (1/4)", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "value", 90))
                    pm.menuItem(label=u"45 (1/8)", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "value", 45))
                    pm.menuItem(label=u"22.5 (1/16)", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "value", 22.5))
                    pm.menuItem(label=u"11.25 (1/32)", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "value", 11.25))
                    pm.menuItem(label=u"5.625 (1/64)", c=pm.Callback(self.mWin.FloatField_editValue, self.ff_rotate_degValue, "value", 5.625))

                #回転X
                with pm.rowLayout(numberOfColumns=9):
                    pm.button(w=18, h=20, label=u"90", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "l", "plus", "90"))
                    pm.button(w=18, h=20, label=u"45", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "l", "plus", "45"))
                    pm.button(w=18, h=20, label=u"1", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "l", "plus", "1"))
                    pm.button(w=18, h=20, label=u"←", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "l", "plus", ""))

                    pm.separator(w=4, h=1, style="none")

                    pm.button(w=18, h=20, label=u"→", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "r", "minus", ""))
                    pm.button(w=18, h=20, label=u"1", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "r", "minus", "1"))
                    pm.button(w=18, h=20, label=u"45", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "r", "minus", "45"))
                    pm.button(w=18, h=20, label=u"90", bgc=[0.8,0.8,0.8], c=pm.Callback(self.rotateUV, "r", "minus", "90"))

        #前回の設定を復帰
        self.mWin.restoreParam(self)

        return

    #-------------------------
    #エッジの角度を取得
    def getEdgeAngle(self, mode):
        rotateDegValue = None

        #選択UV情報を取得
        selUVInfo = getSelUVInfo()
        uvNameList = selUVInfo["uvNameList"]
        uvPosList = selUVInfo["uvPosList"]

        if mode == "input":
            if len(uvNameList) not in [2, 3, 4]:
                messageStr = u"● 2 or 3 or 4つのUV頂点を順番に選択して下さい。"
                messageStr += "\n"
                messageStr += u"    2つ(1エッジ分)の場合：エッジの角度"
                messageStr += "\n"
                messageStr += u"    3つ(2エッジ分)の場合：2つのエッジの間の角度"
                messageStr += "\n"
                messageStr += u"    4つ(2エッジ分)の場合：2つのエッジの間の角度"
                mc.confirmDialog(title=g_toolName, message=messageStr)
                return None, selUVInfo

        elif mode == "fit":
            if len(uvNameList) not in [2, 4]:
                messageStr = u"● 2 or 4つのUV頂点を順番に選択して下さい。"
                messageStr += "\n"
                messageStr += u"    2つ(1エッジ分)の場合：エッジの角度"
                messageStr += "\n"
                messageStr += u"    4つ(2エッジ分)の場合：2つのエッジの間の角度"
                mc.confirmDialog(title=g_toolName, message=messageStr)
                return None, selUVInfo

        #1本目のエッジ
        vecAx = uvPosList[0][0] - uvPosList[1][0]
        vecAy = uvPosList[0][1] - uvPosList[1][1]

        #1本目のエッジの角度
        edge1DegValue = math.degrees(math.atan2(vecAy, vecAx))

        #2頂点(1エッジ)選択の場合
        if len(uvNameList) == 2:
            if mode == "input":
                vecBx = 1
                vecBy = 0

                #2つのベクトルABのなす角度を求める
                rotateDegValue = getAngleOf2Vector(vecAx, vecAy, vecBx, vecBy)

            elif mode == "fit":
                #回転値
                rotateDegValue = edge1DegValue

            print(" [rotate] : " + str(rotateDegValue) + " [get from 2 vertex (1 edge)]")

        #3頂点選択の場合
        elif len(uvNameList) == 3:
            vecBx = uvPosList[2][0] - uvPosList[1][0]
            vecBy = uvPosList[2][1] - uvPosList[1][1]

            if mode == "input":
                #2つのベクトルABのなす角度を求める
                rotateDegValue = getAngleOf2Vector(vecAx, vecAy, vecBx, vecBy)

            elif mode == "fit":
                #2本目のエッジの角度
                edge2DegValue = math.degrees(math.atan2(vecBy, vecBx))

                #回転値
                rotateDegValue = edge2DegValue - edge1DegValue

            print(" [rotate] : " + str(rotateDegValue) + " [get from 3 vertex (2 edge)]")

        #4頂点(2エッジ)選択の場合
        elif len(uvNameList) == 4:
            vecBx = uvPosList[2][0] - uvPosList[3][0]
            vecBy = uvPosList[2][1] - uvPosList[3][1]

            if mode == "input":
                #2つのベクトルABのなす角度を求める
                rotateDegValue = getAngleOf2Vector(vecAx, vecAy, vecBx, vecBy)

            elif mode == "fit":
                edge2DegValue = math.degrees(math.atan2(vecBy, vecBx))

                #回転値
                rotateDegValue = edge2DegValue - edge1DegValue

            print(" [rotate] : " + str(rotateDegValue) + " [get from 4 vertex (2 edge)]")

        return rotateDegValue, selUVInfo

    #-------------------------
    #エッジの角度を自動入力
    def inputEdgeAngle(self):
        #UVエッジの角度を取得
        rotateValue, selUVInfo = self.getEdgeAngle("input")
        if rotateValue is None:
            return

        if round(rotateValue, 3) == -0:
            rotateValue = 0

        print(" [rotate] : " + str(rotateValue) + " [input]")

        #UIに入力
        self.ff_rotate_degValue.setValue(rotateValue)

        print(" [rotate] : " + str(self.ff_rotate_degValue.getValue()) + " [inputted]")

        self.mWin.saveConfig()

        return

    #-------------------------
    #回転
    def rotateUV(self, direction, plus_or_minus, valueStr):
        selItems = pm.ls(sl=1, flatten=1)
        if len(selItems) == 0:
            showMessage(u"操作対象が1つも選択されていません。")
            return

        #選択UV情報を取得
        selUVInfo = getSelUVInfo()
        uvNameList = selUVInfo["uvNameList"]

        rotateValue = 0
        if valueStr == "":
            #編集値を取得
            rotateValue = self.ff_rotate_degValue.getValue()
        else:
            rotateValue = float(valueStr)

        if plus_or_minus == "minus":
            rotateValue *= -1

        print(" [rotate] : " + str(rotateValue))

        #ピボット座標を取得
        pivotPos = self.mWin.pnl_pivot.getPivotPos()

        #対象モードを取得
        targetMode = self.mWin.pnl_target.getTargetMode()

        #回転
        if targetMode == "normal":
            mc.polyEditUV(uvNameList, rotation=1, angle=rotateValue, pivotU=pivotPos[0], pivotV=pivotPos[1])
        elif targetMode == "shell":
            mc.polyEditUVShell(rotation=1, angle=rotateValue, pivotU=pivotPos[0], pivotV=pivotPos[1])

        return

    #-------------------------
    #回転を一致させる
    def fitRotate(self):
        #UVエッジの角度を取得
        rotateValue, selUVInfo = self.getEdgeAngle("fit")
        if rotateValue is None:
            return

        uvNameList = selUVInfo["uvNameList"]
        uvPosList = selUVInfo["uvPosList"]

        pivotUPos = 0
        pivotVPos = 0

        #2頂点(1エッジ)選択の場合
        if len(uvNameList) == 2:
            pivotUPos = uvPosList[0][0]
            pivotVPos = uvPosList[0][1]

            if math.fabs(round(rotateValue, 3)) in [0,90,180,270,360]:
                rotateValue = 90

            elif rotateValue > 0:
                if 135 > rotateValue and rotateValue > 45:
                    rotateValue -= 90
                elif 225 > rotateValue and rotateValue > 135:
                    rotateValue -= 180

            elif rotateValue < 0:
                if -135 < rotateValue and rotateValue < -45:
                    rotateValue += 90
                elif -225 < rotateValue and rotateValue < -135:
                    rotateValue += 180

        #4頂点(2エッジ)選択の場合
        elif len(uvNameList) == 4:
            pivotUPos = (uvPosList[-2][0] + uvPosList[-1][0]) / 2
            pivotVPos = (uvPosList[-2][1] + uvPosList[-1][1]) / 2

            if math.fabs(round(rotateValue, 3)) == 0:
                rotateValue = 180

        #逆回転
        rotateValue = -(rotateValue)

        #回転
        mc.select(uvNameList[-1], r=1)
        mc.polyEditUVShell(rotation=1, angle=rotateValue, pivotU=pivotUPos, pivotV=pivotVPos)
        print(" [rotate] : " + str(rotateValue) + " [fit]")

        #選択を復帰
        mc.select(cl=1)
        for uvName in uvNameList:
            mc.select(uvName, add=1)

        return

    #-------------------------
    #設定をリセット
    def resetConfig(self):
        self.ff_rotate_degValue.setValue(0)

        return

    #-------------------------
    #設定を取得
    def getConfig(self):
        paramName_value = {}

        paramName_value["rotate_degValue"] = self.ff_rotate_degValue.getValue()

        return paramName_value

#-------------------------------------------------
#スケールパネル
class ScalePanel(object):
    def __init__(self, mainWindow):
        self.mWin = mainWindow

        self.controlNames = ["ff_scale_allValue", "ff_scale_uValue", "ff_scale_vValue"]

        menuItemInfoList = []
        menuItemInfoList.append({"type":"command", "label":u"リセット", "mode":"value", "editValue":1})
        menuItemInfoList.append({"type":"divider"})
        menuItemInfoList.append({"type":"command", "label":u"値を2倍", "mode":"*", "editValue":2})
        menuItemInfoList.append({"type":"command", "label":u"値を1/2倍 (0.5倍)", "mode":"/v", "editValue":2})

        #フレームレイアウト(スケール)
        with pm.frameLayout(bgc=[0.1,0.2,0.3], w=self.mWin.frameLayoutWidthValue, borderVisible=self.mWin.frameLayoutBorderVisibleValue, marginWidth=2, marginHeight=2, labelVisible=1, font="plainLabelFont", label=u"■ スケール"):
            with pm.columnLayout(rowSpacing=3):
                with pm.rowLayout(numberOfColumns=4):
                    pm.separator(w=1, h=1, style="none")

                    #自動入力ボタン
                    pm.button(w=133, h=20, label=u"↓2エッジの拡縮率を取得", annotation=u"選択した2つのエッジ(2+2=4つのUV頂点)の拡縮率を取得して自動入力", bgc=[1,1,1], c=pm.Callback(self.input2EdgeScaleValue))

                    pm.separator(w=3, h=1, style="none")

                    #FitScale
                    pm.button(w=20, h=20, label=u"Fit", annotation=u"選択した2つのエッジ(2+2=4つのUV頂点)の長さが一致するようにUVシェルを拡縮する", bgc=[1,0.8,0.5], c=pm.Callback(self.fitScale))

                #スケールALL
                with pm.rowLayout(numberOfColumns=6):
                    pm.text(w=16, h=22, align="left", label=u"All ")
                    pm.button(w=20, h=20, label=u"1/2", bgc=[0.8,0.8,0.8], c=pm.Callback(self.scaleUV, "all", "divide", "0.5"))
                    pm.button(w=14, h=20, label=u"/", bgc=[0.8,0.8,0.8], c=pm.Callback(self.scaleUV, "all", "divide", ""))

                    self.ff_scale_allValue = pm.floatField(w=65, h=22, precision=6, value=1, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    for menuItemInfo in menuItemInfoList:
                        if menuItemInfo["type"] == "command":
                            pm.menuItem(label=menuItemInfo["label"], c=pm.Callback(self.mWin.FloatField_editValue, self.ff_scale_allValue, menuItemInfo["mode"], menuItemInfo["editValue"]))
                        elif menuItemInfo["type"] == "divider":
                            pm.menuItem(divider=1)

                    pm.button(w=14, h=20, label=u"*", bgc=[0.8,0.8,0.8], c=pm.Callback(self.scaleUV, "all", "multiply", ""))
                    pm.button(w=20, h=20, label=u"*2", bgc=[0.8,0.8,0.8], c=pm.Callback(self.scaleUV, "all", "multiply", "2"))

                pm.separator(w=self.mWin.frameLayoutWidthValue-8, h=5, style="in")

                #スケールU
                with pm.rowLayout(numberOfColumns=6):
                    pm.text(w=16, h=22, align="left", label=u"U ")
                    pm.button(w=20, h=20, label=u"1/2", bgc=[0.8,0.6,0.6], c=pm.Callback(self.scaleUV, "u", "divide", "0.5"))
                    pm.button(w=14, h=20, label=u"/", bgc=[0.8,0.6,0.6], c=pm.Callback(self.scaleUV, "u", "divide", ""))

                    self.ff_scale_uValue = pm.floatField(w=65, h=22, precision=6, value=1, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    for menuItemInfo in menuItemInfoList:
                        if menuItemInfo["type"] == "command":
                            pm.menuItem(label=menuItemInfo["label"], c=pm.Callback(self.mWin.FloatField_editValue, self.ff_scale_uValue, menuItemInfo["mode"], menuItemInfo["editValue"]))
                        elif menuItemInfo["type"] == "divider":
                            pm.menuItem(divider=1)

                    pm.button(w=14, h=20, label=u"*", bgc=[0.8,0.6,0.6], c=pm.Callback(self.scaleUV, "u", "multiply", ""))
                    pm.button(w=20, h=20, label=u"*2", bgc=[0.8,0.6,0.6], c=pm.Callback(self.scaleUV, "u", "multiply", "2"))

                #スケールV
                with pm.rowLayout(numberOfColumns=6):
                    pm.text(w=16, h=22, align="left", label=u"V ")
                    pm.button(w=20, h=20, label=u"1/2", bgc=[0.6,0.8,0.6], c=pm.Callback(self.scaleUV, "v", "divide", "0.5"))
                    pm.button(w=14, h=20, label=u"/", bgc=[0.6,0.8,0.6], c=pm.Callback(self.scaleUV, "v", "divide", ""))

                    self.ff_scale_vValue = pm.floatField(w=65, h=22, precision=6, value=1, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    for menuItemInfo in menuItemInfoList:
                        if menuItemInfo["type"] == "command":
                            pm.menuItem(label=menuItemInfo["label"], c=pm.Callback(self.mWin.FloatField_editValue, self.ff_scale_vValue, menuItemInfo["mode"], menuItemInfo["editValue"]))
                        elif menuItemInfo["type"] == "divider":
                            pm.menuItem(divider=1)

                    pm.button(w=14, h=20, label=u"*", bgc=[0.6,0.8,0.6], c=pm.Callback(self.scaleUV, "v", "multiply", ""))
                    pm.button(w=20, h=20, label=u"*2", bgc=[0.6,0.8,0.6], c=pm.Callback(self.scaleUV, "v", "multiply", "2"))

        #前回の設定を復帰
        self.mWin.restoreParam(self)

        return

    #-------------------------
    #2エッジの拡縮率を取得
    def get2EdgeScaleValue(self):
        scaleAllValue = None

        #選択UV情報を取得
        selUVInfo = getSelUVInfo()
        uvNameList = selUVInfo["uvNameList"]
        uvPosList = selUVInfo["uvPosList"]

        if len(uvNameList) != 4:
            messageStr = u"● 4つのUV頂点を順番に選択して下さい。"
            mc.confirmDialog(title=g_toolName, message=messageStr)
            return None, selUVInfo

        #エッジの距離
        edge1Length = math.sqrt(((uvPosList[1][0] - uvPosList[0][0]) * (uvPosList[1][0] - uvPosList[0][0])) + ((uvPosList[1][1] - uvPosList[0][1]) * (uvPosList[1][1] - uvPosList[0][1])))
        edge2Length = math.sqrt(((uvPosList[3][0] - uvPosList[2][0]) * (uvPosList[3][0] - uvPosList[2][0])) + ((uvPosList[3][1] - uvPosList[2][1]) * (uvPosList[3][1] - uvPosList[2][1])))

        #スケール値
        scaleAllValue = edge1Length / edge2Length

        print(" [scale All] : " + str(scaleAllValue) + " [get]")

        return scaleAllValue, selUVInfo

    #-------------------------
    #スケール値を取得して自動入力
    def input2EdgeScaleValue(self):
        #2エッジの拡縮率を取得
        scaleAllValue, selUVInfo = self.get2EdgeScaleValue()
        if scaleAllValue is None:
            return

        print(" [scale All] : " + str(scaleAllValue) + " [input]")

        #UIに入力
        self.ff_scale_allValue.setValue(scaleAllValue)

        print(" [scale All] : " + str(self.ff_scale_allValue.getValue()) + " [inputted]")

        self.mWin.saveConfig()

        return

    #-------------------------
    #スケール
    def scaleUV(self, direction, divide_or_multiply, valueStr):
        selItems = pm.ls(sl=1, flatten=1)
        if len(selItems) == 0:
            showMessage(u"操作対象が1つも選択されていません。")
            return

        #選択UV情報を取得
        selUVInfo = getSelUVInfo()
        uvNameList = selUVInfo["uvNameList"]

        #編集値
        editValue = 1
        if valueStr == "":
            if direction == "all":
                editValue = self.ff_scale_allValue.getValue()
            elif direction == "u":
                editValue = self.ff_scale_uValue.getValue()
            elif direction == "v":
                editValue = self.ff_scale_vValue.getValue()

            if divide_or_multiply == "divide":
                editValue = 1 / editValue
        else:
            editValue = float(valueStr)

        scaleAllValue = 1
        scaleUValue = 1
        scaleVValue = 1
        if direction == "all":
            scaleAllValue = editValue
            print(" [scale All] : " + str(scaleAllValue))
        elif direction == "u":
            scaleUValue = editValue
            print(" [scale U] : " + str(scaleUValue))
        elif direction == "v":
            scaleVValue = editValue
            print(" [scale V] : " + str(scaleVValue))

        #ピボット座標を取得
        pivotPos = self.mWin.pnl_pivot.getPivotPos()

        #対象モードを取得
        targetMode = self.mWin.pnl_target.getTargetMode()

        #スケール
        if targetMode == "normal":
            if direction == "all":
                mc.polyEditUV(uvNameList, scale=1, scaleU=scaleAllValue, scaleV=scaleAllValue, pivotU=pivotPos[0], pivotV=pivotPos[1])
            elif direction == "u":
                mc.polyEditUV(uvNameList, scale=1, scaleU=scaleUValue, pivotU=pivotPos[0])
            elif direction == "v":
                mc.polyEditUV(uvNameList, scale=1, scaleV=scaleVValue, pivotV=pivotPos[1])
        elif targetMode == "shell":
            if direction == "all":
                mc.polyEditUVShell(scale=1, scaleU=scaleAllValue, scaleV=scaleAllValue, pivotU=pivotPos[0], pivotV=pivotPos[1])
            elif direction == "u":
                mc.polyEditUVShell(scale=1, scaleU=scaleUValue, pivotU=pivotPos[0])
            elif direction == "v":
                mc.polyEditUVShell(scale=1, scaleV=scaleVValue, pivotV=pivotPos[1])

        return

    #-------------------------
    #スケールを一致させる
    def fitScale(self):
        #2エッジの拡縮率を取得
        scaleAllValue, selUVInfo = self.get2EdgeScaleValue()
        if scaleAllValue is None:
            return

        uvNameList = selUVInfo["uvNameList"]
        uvPosList = selUVInfo["uvPosList"]

        #ピボット座標
        pivotUPos = (uvPosList[2][0] + uvPosList[3][0]) / 2
        pivotVPos = (uvPosList[2][1] + uvPosList[3][1]) / 2

        #スケール
        mc.select([uvNameList[-2],uvNameList[-1]], r=1)
        mc.polyEditUVShell(scale=1, scaleU=scaleAllValue, scaleV=scaleAllValue, pivotU=pivotUPos, pivotV=pivotVPos)
        print(" [scale All] : " + str(scaleAllValue) + " [fit]")

        #選択を復帰
        mc.select(cl=1)
        for uvName in uvNameList:
            mc.select(uvName, add=1)

        return

    #-------------------------
    #設定をリセット
    def resetConfig(self):
        self.ff_scale_allValue.setValue(1)
        self.ff_scale_uValue.setValue(1)
        self.ff_scale_vValue.setValue(1)

        return

    #-------------------------
    #設定を取得
    def getConfig(self):
        paramName_value = {}

        paramName_value["scale_allValue"] = self.ff_scale_allValue.getValue()
        paramName_value["scale_uValue"] = self.ff_scale_uValue.getValue()
        paramName_value["scale_vValue"] = self.ff_scale_vValue.getValue()

        return paramName_value


#-------------------------------------------------
#ピボットパネル
class PivotPanel(object):
    def __init__(self, mainWindow):
        self.mWin = mainWindow

        self.controlNames = ["rc_pivot_mode", "ff_pivot_uValue", "ff_pivot_vValue"]

        menuItemInfoList = []
        menuItemInfoList.append({"type":"command", "label":u"リセット", "mode":"value", "editValue":0})
        menuItemInfoList.append({"type":"divider"})
        menuItemInfoList.append({"type":"command", "label":u"0.5", "mode":"value", "editValue":0.5})

        #フレームレイアウト(ピボット)
        with pm.frameLayout(bgc=[0.1,0.1,0.1], w=self.mWin.frameLayoutWidthValue, borderVisible=self.mWin.frameLayoutBorderVisibleValue, marginWidth=2, marginHeight=2, labelVisible=1, font="plainLabelFont", label=u"回転とスケール用のPivot"):
            with pm.columnLayout(rowSpacing=4):
                #ピボットモード
                with pm.rowLayout(numberOfColumns=3):
                    pm.separator(w=2, h=1, style="none")

                    self.rc_pivot_mode = pm.radioCollection()
                    pm.radioButton("selCenter", label=u"選択の中心", cc=pm.Callback(self.RadioButton_change), w=81, select=1)
                    pm.radioButton("inputPos", label=u"位置を指定")
                    pm.setParent("..")

                pm.separator(w=self.mWin.frameLayoutWidthValue-8, h=5, style="in")

                #自動入力ボタン
                with pm.rowLayout(numberOfColumns=2):
                    pm.separator(w=7, h=1, style="none")
                    self.btn_inputPivotPos = pm.button(bgc=[1,1,1], w=148, h=20, label=u"↓選択UV頂点の位置を取得", annotation=u"選択中の 「 頂点 」 か 「 ノード (Transform) 」 のワールド座標を自動入力します。", c=pm.Callback(self.inputPivotPos))

                #ピボット座標
                with pm.rowLayout(numberOfColumns=5):
                    #ピボットU
                    self.tx_pivot_uValue = pm.text(w=9, align="left", label=u"U ")
                    self.ff_pivot_uValue = pm.floatField(w=68, h=22, precision=6, value=0.5, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    for menuItemInfo in menuItemInfoList:
                        if menuItemInfo["type"] == "command":
                            pm.menuItem(label=menuItemInfo["label"], c=pm.Callback(self.mWin.FloatField_editValue, self.ff_pivot_uValue, menuItemInfo["mode"], menuItemInfo["editValue"]))
                        elif menuItemInfo["type"] == "divider":
                            pm.menuItem(divider=1)

                    pm.separator(w=2, h=1, style="none")

                    #ピボットV
                    self.tx_pivot_vValue = pm.text(w=9, align="left", label=u"V ")
                    self.ff_pivot_vValue = pm.floatField(w=68, h=22, precision=6, value=0.5, cc=pm.Callback(self.mWin.saveConfig), ec=pm.Callback(self.mWin.saveConfig))

                    #ポップアップメニュー
                    pm.popupMenu()
                    for menuItemInfo in menuItemInfoList:
                        if menuItemInfo["type"] == "command":
                            pm.menuItem(label=menuItemInfo["label"], c=pm.Callback(self.mWin.FloatField_editValue, self.ff_pivot_vValue, menuItemInfo["mode"], menuItemInfo["editValue"]))
                        elif menuItemInfo["type"] == "divider":
                            pm.menuItem(divider=1)

        #前回の設定を復帰
        self.mWin.restoreParam(self)

        #コントロールの状態を変更する
        self.editControlStatus()

        return

    #-------------------------
    #ラジオボタンの状態が変更された時の処理
    def RadioButton_change(self):
        self.editControlStatus()
        self.mWin.saveConfig()

        return

    #-------------------------
    #Pivotモードの状態によってコントロールの状態を変更する
    def editControlStatus(self):
        pivotMode = self.rc_pivot_mode.getSelect()

        #コントロールの状態を変更する
        if pivotMode == "selCenter":
            self.btn_inputPivotPos.setEnable(0)
            self.ff_pivot_uValue.setEnable(0)
            self.ff_pivot_vValue.setEnable(0)
            self.tx_pivot_uValue.setEnable(0)
            self.tx_pivot_vValue.setEnable(0)
        elif pivotMode == "inputPos":
            self.btn_inputPivotPos.setEnable(1)
            self.ff_pivot_uValue.setEnable(1)
            self.ff_pivot_vValue.setEnable(1)
            self.tx_pivot_uValue.setEnable(1)
            self.tx_pivot_vValue.setEnable(1)

        return

    #-------------------------
    #ピボット座標を自動入力
    def inputPivotPos(self):
        selItems = pm.ls(sl=1, flatten=1)
        if len(selItems) == 0:
            showMessage(u"操作対象が1つも選択されていません。")
            return

        #選択UV情報を取得
        selUVInfo = getSelUVInfo()

        #選択アイテムの中心座標
        pivotPos = selUVInfo["selCenter"]

        print(" [pivot U] : " + str(pivotPos[0]) + " [input]")
        print(" [pivot V] : " + str(pivotPos[1]) + " [input]")

        #UIに入力
        self.ff_pivot_uValue.setValue(pivotPos[0])
        self.ff_pivot_vValue.setValue(pivotPos[1])

        print(" [pivot U] : " + str(self.ff_pivot_uValue.getValue()) + " [inputted]")
        print(" [pivot V] : " + str(self.ff_pivot_vValue.getValue()) + " [inputted]")

        self.mWin.saveConfig()

        return

    #-------------------------
    #ピボット座標を取得
    def getPivotPos(self):
        pivotPos = []

        pivotMode = self.rc_pivot_mode.getSelect()

        if pivotMode == "selCenter":
            #選択UV情報を取得
            selUVInfo = getSelUVInfo()

            #選択アイテムの中心座標
            pivotPos = selUVInfo["selCenter"]
        elif pivotMode == "inputPos":
            pivotPos.append(self.ff_pivot_uValue.getValue())
            pivotPos.append(self.ff_pivot_vValue.getValue())

        return pivotPos

    #-------------------------
    #設定をリセット
    def resetConfig(self):
        self.ff_pivot_uValue.setValue(0)
        self.ff_pivot_vValue.setValue(0)
        self.rc_pivot_mode.setSelect("selCenter")

        return

    #-------------------------
    #設定を取得
    def getConfig(self):
        paramName_value = {}

        paramName_value["pivot_mode"] = self.rc_pivot_mode.getSelect()
        paramName_value["pivot_uValue"] = self.ff_pivot_uValue.getValue()
        paramName_value["pivot_vValue"] = self.ff_pivot_vValue.getValue()

        return paramName_value


#-------------------------------------------------
#マッピングパネル
class MappingPanel(object):
    def __init__(self, mainWindow):
        self.mWin = mainWindow

        self.controlNames = ["cb_mapping_keepImageRatio", "om_mapping_autoPlanes", "om_mapping_autoOptimize"]


        #オプションメニュー情報 {メニューキー:メニューID}
        self.menuKey_menuId = {}
        self.menuKey_menuId["mapping_autoPlanes"] = {}
        menuKeys = ["3","4","5","6","8","12"]
        for menuIndex in range(len(menuKeys)):
            menuKey = menuKeys[menuIndex]
            menuId = menuIndex + 1
            self.menuKey_menuId["mapping_autoPlanes"][menuKey] = menuId
        self.menuKey_menuId["mapping_autoOptimize"] = {}
        self.menuKey_menuId["mapping_autoOptimize"]["lessDistortion"] = 1
        self.menuKey_menuId["mapping_autoOptimize"]["fewerPieces"] = 2

        #オプションメニュー情報 {メニューID:メニューキー}
        self.menuId_menuKey = {}
        for param in self.menuKey_menuId:
            self.menuId_menuKey[param] = {}
            for menuKey in self.menuKey_menuId[param]:
                menuId = self.menuKey_menuId[param][menuKey]
                self.menuId_menuKey[param][str(menuId)] = menuKey

        #フレームレイアウト(マッピング)
        with pm.frameLayout(bgc=[0.35,0.35,0.35], w=self.mWin.frameLayoutWidthValue, borderVisible=self.mWin.frameLayoutBorderVisibleValue, marginWidth=5, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"■ マッピング"):
            with pm.columnLayout(rowSpacing=3):
                self.cb_mapping_keepImageRatio = pm.checkBox(label=u"縦横比を維持", cc=pm.Callback(self.CheckBox_change), value=1)

                #マッピング1
                with pm.rowLayout(numberOfColumns=5):
                    button1Width = 24
                    pm.button(w=button1Width, h=18, label=u"X", bgc=[0.8,0.6,0.6], c=pm.Callback(self.projectUV, "x"))
                    pm.button(w=button1Width, h=18, label=u"Y", bgc=[0.6,0.8,0.6], c=pm.Callback(self.projectUV, "y"))
                    pm.button(w=button1Width, h=18, label=u"Z", bgc=[0.6,0.7,0.8], c=pm.Callback(self.projectUV, "z"))

                    button2Width = 40
                    pm.button(w=button2Width, h=18, label=u"Best", bgc=[0.8,0.8,0.8], c=pm.Callback(self.projectUV, "best"))
                    pm.button(w=button2Width, h=18, label=u"Cam", bgc=[0.8,0.8,0.8], c=pm.Callback(self.projectUV, "camera"))

                pm.separator(w=self.mWin.frameLayoutWidthValue-8, h=5, style="in")

                #マッピング2
                with pm.rowLayout(numberOfColumns=4):
                    pm.text(w=40, h=22, align="left", label=u"プレーン")

                    self.om_mapping_autoPlanes = pm.optionMenu(w=45, h=20, cc=pm.Callback(self.OptionMenu_change))
                    pm.menuItem(parent=self.om_mapping_autoPlanes, label=u"3")
                    pm.menuItem(parent=self.om_mapping_autoPlanes, label=u"4")
                    pm.menuItem(parent=self.om_mapping_autoPlanes, label=u"5")
                    pm.menuItem(parent=self.om_mapping_autoPlanes, label=u"6")
                    pm.menuItem(parent=self.om_mapping_autoPlanes, label=u"8")
                    pm.menuItem(parent=self.om_mapping_autoPlanes, label=u"12")

                    pm.separator(w=2, h=1, style="none")

                    pm.button(w=67, h=18, label=u"Auto", bgc=[0.8,0.8,0.8], c=pm.Callback(self.projectUV, "auto"))

                #マッピング3
                with pm.rowLayout(numberOfColumns=2):
                    pm.text(w=33, h=22, align="left", label=u"最適化")

                    self.om_mapping_autoOptimize = pm.optionMenu(w=125, h=20, cc=pm.Callback(self.OptionMenu_change))
                    pm.menuItem(parent=self.om_mapping_autoOptimize, label=u"少ないゆがみ")
                    pm.menuItem(parent=self.om_mapping_autoOptimize, label=u"少ないピース (既定)")

                pm.separator(w=self.mWin.frameLayoutWidthValue-8, h=5, style="in")

                # マッピング4
                with pm.rowLayout(numberOfColumns=2):
                    pm.button(w=80, h=18, label=u"柱", bgc=[
                              0.8, 0.8, 0.8], c=pm.Callback(self.projectUV, "cylinder"))
                    pm.button(w=80, h=18, label=u"球", bgc=[
                              0.8, 0.8, 0.8], c=pm.Callback(self.projectUV, "sphere"))

        #前回の設定を復帰
        self.mWin.restoreParam(self)

        return

    #-------------------------
    #チェックボックスの状態が変更された時の処理
    def CheckBox_change(self):
        self.mWin.saveConfig()

        return

    #-------------------------
    #オプションメニューの状態が変更された時の処理
    def OptionMenu_change(self):
        self.mWin.saveConfig()

        return

    #-------------------------
    #UV投影
    def projectUV(self, mode):
        selItems = pm.ls(sl=1, flatten=1)
        if len(selItems) == 0:
            showMessage(u"操作対象が1つも選択されていません。")
            return

        #縦横比を維持するかどうか
        keepImageRatioValue = self.cb_mapping_keepImageRatio.getValue()

        CyConvertSelection.convert("polygon")

        if mode in ["x","y","z","best","camera"]:
            #投影方法
            mapDirectionValue = mode
            if mode == "best":
                mapDirectionValue = "b"
            elif mode == "camera":
                mapDirectionValue = "c"
            pm.polyProjection(type="Planar", mapDirection=mapDirectionValue, insertBeforeDeformers=1, imageCenterX=0.5, imageCenterY=0.5, rotationAngle=0, imageScaleU=1, imageScaleV=1, keepImageRatio=keepImageRatioValue, constructionHistory=1)

        elif mode == "cylinder" or mode == "sphere":
            typeValue = ""
            if mode == "cylinder":
                typeValue = "Cylindrical"
            elif mode == "sphere":
                typeValue = "Spherical"
            pm.polyProjection(type=typeValue, smartFit=1, insertBeforeDeformers=1, imageCenterX=0.5, imageCenterY=0.5, rotationAngle=0, imageScaleU=1, imageScaleV=1, constructionHistory=1)

        elif mode == "auto":
            #プレーン
            planesValue = int(self.menuId_menuKey["mapping_autoPlanes"][str(self.om_mapping_autoPlanes.getSelect())])

            #最適化
            optimizeValue = 1
            optimizeKey = self.menuId_menuKey["mapping_autoOptimize"][str(self.om_mapping_autoOptimize.getSelect())]
            if optimizeKey == "lessDistortion":
                optimizeValue = 0
            elif optimizeKey == "fewerPieces":
                optimizeValue = 1

            pm.polyAutoProjection(insertBeforeDeformers=1, planes=planesValue, optimize=optimizeValue, scaleMode=1, layout=2, percentageSpace=0.5, createNewMap=0, worldSpace=1, projectBothDirections=0)

        #選択を復帰
        pm.select(selItems)

        return

    #-------------------------
    #設定をリセット
    def resetConfig(self):
        self.cb_mapping_keepImageRatio.setValue(1)
        self.om_mapping_autoPlanes.setSelect(self.menuKey_menuId["mapping_autoPlanes"]["6"])
        self.om_mapping_autoOptimize.setSelect(self.menuKey_menuId["mapping_autoOptimize"]["fewerPieces"])

        return

    #-------------------------
    #設定を取得
    def getConfig(self):
        paramName_value = {}

        paramName_value["mapping_keepImageRatio"] = int(self.cb_mapping_keepImageRatio.getValue())
        paramName_value["mapping_autoPlanes"] = self.menuId_menuKey["mapping_autoPlanes"][str(self.om_mapping_autoPlanes.getSelect())]
        paramName_value["mapping_autoOptimize"] = self.menuId_menuKey["mapping_autoOptimize"][str(self.om_mapping_autoOptimize.getSelect())]

        return paramName_value


#-------------------------------------------------
#その他パネル
class EtcPanel(object):
    def __init__(self, mainWindow):
        self.mWin = mainWindow

        #フレームレイアウト(その他)
        with pm.frameLayout(bgc=[0.35,0.35,0.35], w=self.mWin.frameLayoutWidthValue, borderVisible=self.mWin.frameLayoutBorderVisibleValue, marginWidth=5, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"■ その他"):
            with pm.columnLayout(rowSpacing=3):
                #その他1
                with pm.rowLayout(numberOfColumns=3):
                    pm.button(w=44, h=18, label=u"Cut", c=pm.Callback(self.runCommand, "Cut"))
                    pm.button(w=44, h=18, label=u"Sew", c=pm.Callback(self.runCommand, "Sew"))
                    pm.button(w=68, h=18, label=u"MoveSew", c=pm.Callback(self.runCommand, "MoveSew"))

                pm.separator(w=self.mWin.frameLayoutWidthValue-8, h=5, style="in")

                #その他2
                with pm.rowLayout(numberOfColumns=3):
                    pm.button(w=50, h=18, label=u"Relax", c=pm.Callback(self.runCommand, "Relax"))
                    pm.button(w=56, h=18, label=u"Unfold", c=pm.Callback(self.runCommand, "Unfold"))
                    pm.button(w=50, h=18, label=u"Layout", c=pm.Callback(self.runCommand, "Layout"))

        return

    #-------------------------
    #コマンドを実行
    def runCommand(self, mode):
        if mode == "Cut":
            mc.polyMapCut()
        elif mode == "Sew":
            mc.polyMapSew()
        elif mode == "MoveSew":
            mc.polyMapSewMove()
        elif mode == "Relax":
            mm.eval("performPolyUntangleUV relax 1")
        elif mode == "Unfold":
            mm.eval("performUnfold 1")
        elif mode == "Layout":
            mm.eval("performPolyLayoutUV 1")

        return


#-------------------------------------------------
#選択UV情報を取得
def getSelUVInfo():
    selUVInfo = {}
    selUVInfo["uvNameList"] = []
    selUVInfo["uvPosList"] = []
    selUVInfo["selCenter"] = []

    selItems = pm.ls(sl=1, flatten=1)

    #選択をUVに変換
    mc.ConvertSelectionToUVs()

    #選択UV頂点を取得
    selUvNameList = mc.filterExpand(expand=1, selectionMask=35)
    if selUvNameList == None or len(selUvNameList) == 0:
        return selUVInfo

    #選択アイテムを取得(選択順)
    selItemNameList = mc.ls(orderedSelection=1, flatten=1)

    uValueList = []
    vValueList = []
    for itemName in selItemNameList:
        if itemName in selUvNameList:
            selUVInfo["uvNameList"].append(itemName)

            #UVの座標を取得
            currentUVPos = mc.polyEditUV(itemName, q=1)

            selUVInfo["uvPosList"].append(currentUVPos)
            uValueList.append(currentUVPos[0])
            vValueList.append(currentUVPos[1])

    #バウンディングボックスの中心座標
    bBoxUMax = max(uValueList)
    bBoxVMax = max(vValueList)

    bBoxUMin = min(uValueList)
    bBoxVMin = min(vValueList)

    bBoxUCen = (bBoxUMin + bBoxUMax) / 2
    bBoxVCen = (bBoxVMin + bBoxVMax) / 2

    selUVInfo["selCenter"] = [bBoxUCen, bBoxVCen]

    #選択を復帰
    pm.select(selItems, r=1)

    return selUVInfo


#-------------------------------------------------
#ベクトルの長さ
def getVectorLength(x, y):
    return math.pow((x * x) + (y * y), 0.5)


#-------------------------------------------------
#ベクトル内積
def dot_product(vecAx, vecAy, vecBx, vecBy):
    return vecAx * vecBx + vecAy * vecBy


#-------------------------------------------------
#2つのベクトルABのなす角度を求める
def getAngleOf2Vector(vecAx, vecAy, vecBx, vecBy):
    #ベクトルAとBの長さを計算する
    vecALength = getVectorLength(vecAx, vecAy)
    vecBLength = getVectorLength(vecBx, vecBy)

    #内積とベクトル長さを使ってcosθを求める
    cos_sita = dot_product(vecAx, vecAy, vecBx, vecBy) / (vecALength * vecBLength)

    #cosθからθを求める
    sita = math.acos( cos_sita )

    sita = math.degrees(sita)

    return sita


#-------------------------------------------------
#メッセージを表示
def showMessage(messageStr):
    print(u"#    " + messageStr)
    pm.confirmDialog(title=g_toolName, message=u"● " + messageStr)
    return


#-------------------------------------------------
if __name__ == "__main__":
    main()
