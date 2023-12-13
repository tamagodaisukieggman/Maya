# -*- coding: utf-8 -*-

"""
子ノードを選択

"""

toolName = "CySelectChildNode"
__author__ = "Cygames, Inc. Yuta Kimura"

import os

import pymel.core as pm



#maya設定フォルダのパス
userAppDirPath = pm.internalVar(userAppDir=1)

#ツール設定のパス
configFolderPath = userAppDirPath + "Cygames/" + toolName
configFilePath = configFolderPath + "/" + toolName + ".ini"

FILTER_CATEGORIES = ["model","light","skeleton","etc"]

CATEGORY_FILTERS_DICT = {}
CATEGORY_FILTERS_DICT["model"] = ["mesh","nurbsSurface","nurbsCurve"]
CATEGORY_FILTERS_DICT["light"] = ["ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight"]
CATEGORY_FILTERS_DICT["skeleton"] = ["joint","ikEffector","ikHandle"]
CATEGORY_FILTERS_DICT["etc"] = ["camera","locator"]
CATEGORY_FILTERS_DICT["etc"].append("group")

ALL_FILTERS = []
for currentCategory in FILTER_CATEGORIES:
    ALL_FILTERS.extend(CATEGORY_FILTERS_DICT[currentCategory])


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
        loadedConfigInfo = loadConfig()

        #既にウィンドウが開いている場合は閉じる
        if pm.window(toolName, q=1, exists=1):
            pm.deleteUI(toolName)

        #UIの定義
        self.window = pm.window(toolName, title=u"子選択", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            self.columnLayout_top = pm.columnLayout("columnLayout_top", columnOffset=("left", 5))
            with self.columnLayout_top:
                self.separator_topSpace = pm.separator("separator_topSpace", w=1, h=5, style="none")

                with pm.columnLayout(rowSpacing=10):
                    self.rowLayout_topButton = pm.rowLayout("rowLayout_topButton", numberOfColumns=2)
                    with self.rowLayout_topButton:
                        self.button_onAll = pm.button("button_onAll", width=53, label=u"全チェック", command=pm.Callback(self.EditAllCheckButton_click, 1))
                        self.button_offAll = pm.button("button_offAll", width=53, label=u"全解除", command=pm.Callback(self.EditAllCheckButton_click, 0))

                    for currentCategory in FILTER_CATEGORIES:
                        self.__dict__["frameLayout_" + currentCategory] = pm.frameLayout("frameLayout_" + currentCategory, w=110, label=currentCategory.capitalize(), borderStyle="etchedIn", font="plainLabelFont", marginWidth=7, marginHeight=5)
                        with self.__dict__["frameLayout_" + currentCategory]:
                            for currentFilter in CATEGORY_FILTERS_DICT[currentCategory]:
                                #チェックボックス
                                self.__dict__["checkBox_" + currentFilter] = pm.checkBox("checkBox_" + currentFilter,
                                                                                         label=currentFilter,
                                                                                         cc=pm.Callback(self.CheckBox_changeCommand))

                                #右クリックメニュー
                                self.__dict__["popupMenu_" + currentFilter] = pm.popupMenu("popupMenu_" + currentFilter,
                                                                                           parent="checkBox_" + currentFilter,
                                                                                           button=3)
                                self.__dict__["menuItem_" + currentFilter + "Only"] = pm.menuItem("menuItem_" + currentFilter + "Only",
                                                                                                  label=(u"「 " + currentFilter + u" 」 だけをチェック"),
                                                                                                  command=pm.Callback(self.CheckBox_rclick, currentFilter, "only"))
                                self.__dict__["menuItem_" + currentFilter + "Other"] = pm.menuItem("menuItem_" + currentFilter + "Other",
                                                                                                   label=(u"「 " + currentFilter + u" 」 以外をチェック"),
                                                                                                   command=pm.Callback(self.CheckBox_rclick, currentFilter, "other"))

                    self.columnLayout_option = pm.columnLayout("columnLayout_option")
                    with self.columnLayout_option:
                        self.checkBox_selShapeFlg = pm.checkBox("checkBox_selShapeFlg", label=u"Shapeも選択する", cc=pm.Callback(self.CheckBox_changeCommand))
                        self.checkBox_selSrcFlg = pm.checkBox("checkBox_selSrcFlg", label=u"選択元も対象", cc=pm.Callback(self.CheckBox_changeCommand))

                    self.columnLayout_bottomButton = pm.columnLayout("columnLayout_bottomButton", rowSpacing=5)
                    with self.columnLayout_bottomButton:
                        self.button_select = pm.button("button_select", width=108, label=u"子ノードを選択", command=pm.Callback(self.SelectButton_click, "select"))
                        self.button_filter = pm.button("button_filter", width=108, label=u"選択を絞り込む", command=pm.Callback(self.SelectButton_click, "filter"))

        #前回の設定を復帰
        self.restoreParam(loadedConfigInfo)

        #ウィンドウのサイズ変更
        winWidthValue = 124
        winHeightValue = 593
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue += 24
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    #-------------------------
    #選択ボタンをクリックした時の処理
    def SelectButton_click(self, mode):
        #チェックされている項目
        filters = []
        for currentFilter in ALL_FILTERS:
            if self.__dict__["checkBox_" + currentFilter].getValue():
                filters.append(currentFilter)

        if len(filters) == 0:
            messageStr = u"ノードタイプを選択して下さい。"
            pm.confirmDialog(title=toolName, message=u"● " + messageStr)
            return

        selShapeFlgValue = self.checkBox_selShapeFlg.getValue()
        selSrcFlgValue = self.checkBox_selSrcFlg.getValue()

        if mode == "select":
            #子ノードを選択
            select(filters, 1, selShapeFlgValue, selSrcFlgValue, 1)

        elif mode == "filter":
            #選択を絞り込む
            filter(filters, 1, selShapeFlgValue, 1)

        return

    #-------------------------
    #全チェック/解除ボタンをクリックした時の処理
    def EditAllCheckButton_click(self, value):
        for currentFilter in ALL_FILTERS:
            self.__dict__["checkBox_" + currentFilter].setValue(value)

        self.saveConfig()

        return

    #-------------------------
    #チェックボックスを右クリックした時の処理
    def CheckBox_rclick(self, targetFilter, mode):
        for currentFilter in ALL_FILTERS:
            value = 0
            if mode == "only":
                if currentFilter == targetFilter:
                    value = 1
                else:
                    value = 0
            elif mode == "other":
                if currentFilter == targetFilter:
                    value = 0
                else:
                    value = 1
            self.__dict__["checkBox_" + currentFilter].setValue(value)

        self.saveConfig()

        return

    #-------------------------
    #チェックボックスの状態が変更された時の処理
    def CheckBox_changeCommand(self):
        self.saveConfig()

        return

    #-------------------------
    #前回の設定を復帰
    def restoreParam(self, loadedConfigInfo):
        #フィルター
        for currentCategory in FILTER_CATEGORIES:
            for currentFilter in CATEGORY_FILTERS_DICT[currentCategory]:
                if currentFilter in loadedConfigInfo:
                    currentControlName = "checkBox_" + currentFilter
                    if currentControlName in self.__dict__:
                        try:
                            self.__dict__[currentControlName].setValue(loadedConfigInfo[currentFilter])
                        except:
                            pass

        #オプション
        for currentParamName in ["selShapeFlg", "selSrcFlg"]:
            if currentParamName in loadedConfigInfo:
                currentControlName = "checkBox_" + currentParamName
                if currentControlName in self.__dict__:
                    try:
                        self.__dict__[currentControlName].setValue(loadedConfigInfo[currentParamName])
                    except:
                        pass

        self.saveConfig()

        return

    #-------------------------
    #設定を保存
    def saveConfig(self):
        configInfo = {}

        #{パラメーター名:値}
        for currentFilter in ALL_FILTERS:
            currentControlName = "checkBox_" + currentFilter
            if currentControlName in self.__dict__:
                configInfo[currentFilter] = str(int(self.__dict__[currentControlName].getValue()))

        configInfo["selShapeFlg"] = str(int(self.checkBox_selShapeFlg.getValue()))
        configInfo["selSrcFlg"] = str(int(self.checkBox_selSrcFlg.getValue()))

        allParamNames = configInfo.keys()
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
#設定を元に子ノードを選択
def selectWithSettings(mainFlg=0):
    if mainFlg == 1:
        print("")
        print("#-----")
        print("#[Python Command]")
        print("#import CySelectChildNode;reload(CySelectChildNode);CySelectChildNode.selectWithSettings()")
        print("#-----")
        print("")

    #設定を読み込み
    loadedConfigInfo = loadConfig()

    filters = []
    for currentFilter in ALL_FILTERS:
        if currentFilter in loadedConfigInfo:
            if loadedConfigInfo[currentFilter] == 1:
                filters.append(currentFilter)

    selShapeFlgValue = 0
    if "selShapeFlg" in loadedConfigInfo:
        selShapeFlgValue = loadedConfigInfo["selShapeFlg"]

    selSrcFlgValue = 0
    if "selSrcFlg" in loadedConfigInfo:
        selSrcFlgValue = loadedConfigInfo["selSrcFlg"]

    #子ノードを選択
    select(filters, 1, selShapeFlgValue, selSrcFlgValue, 0)

    return


#-------------------------------------------------
#子ノードを選択
def select(filters, selTransformFlg, selShapeFlg, selSrcFlg, mainFlg=0):
    if mainFlg == 1:
        print("")
        print("#-----")
        print("#[Python Command]")
        print("#import CySelectChildNode;reload(CySelectChildNode);CySelectChildNode.select(filters=" + str(filters).replace(" ", "") + ", selTransformFlg=" + str(selTransformFlg) + ", selShapeFlg=" + str(selShapeFlg) + ", selSrcFlg=" + str(selSrcFlg) + ")")
        print("#-----")
        print("")

    #選択中のノード
    selNodes = pm.ls(sl=1)

    #特定の種類の子ノードを取得
    resultNodes = getSpecificTypeChildNodes(selNodes, filters, selTransformFlg, selShapeFlg, selSrcFlg)

    #ノードを選択
    pm.select(resultNodes)

    return resultNodes


#-------------------------------------------------
#選択を絞り込む
def filter(filters, selTransformFlg, selShapeFlg, mainFlg=0):
    if mainFlg == 1:
        print("")
        print("#-----")
        print("#[Python Command]")
        print("#import CySelectChildNode;reload(CySelectChildNode);CySelectChildNode.filter(filters=" + str(filters).replace(" ", "") + ", selTransformFlg=" + str(selTransformFlg) + ", selShapeFlg=" + str(selShapeFlg) + ")")
        print("#-----")
        print("")

    #選択中のノード
    selNodes = pm.ls(sl=1)

    #特定の種類のノードを取得
    resultNodes = getSpecificTypeNodes(selNodes, filters, selTransformFlg, selShapeFlg)

    #ノードを選択
    pm.select(resultNodes)

    return resultNodes


#-------------------------------------------------
#子ノードを取得(再帰)
def getChildNodes(currentNode, allChildNodes=[]):
    childNodes = currentNode.getChildren()

    if len(childNodes) > 0:
        for currentChildNode in childNodes:
            allChildNodes.append(currentChildNode)
            allChildNodes = getChildNodes(currentChildNode, allChildNodes)

    return allChildNodes


#-------------------------------------------------
#特定の種類の子ノードを取得
def getSpecificTypeChildNodes(srcNodes, filters, selTransformFlg, selShapeFlg, selSrcFlg):
    #子ノードを取得
    allChildNodes = []
    for currentSelNode in srcNodes:
        allChildNodes = getChildNodes(currentSelNode, allChildNodes)

    #初期選択ノードを含める場合
    if selSrcFlg == 1:
        allChildNodes.extend(srcNodes)

    #特定の種類のノードを取得
    resultNodes = getSpecificTypeNodes(allChildNodes, filters, selTransformFlg, selShapeFlg)

    return resultNodes


#-------------------------------------------------
#特定の種類のノードを取得
def getSpecificTypeNodes(srcNodes, filters, selTransformFlg, selShapeFlg):
    resultNodes = []

    if len(filters) == 0:
        return resultNodes

    if "all" in filters:
        filters = ALL_FILTERS

    for currentNode in srcNodes:
        transformNode = None
        shapeNode = None
        if currentNode.type() == "transform":
            if selTransformFlg == 1:
                transformNode = currentNode
                shapeNode = currentNode.getShape()
        #トランスフォーム以外の場合
        else:
            if currentNode.type() in CATEGORY_FILTERS_DICT["skeleton"]:
                transformNode = currentNode
            else:
                if selShapeFlg == 1:
                    transformNode = currentNode.getParent()
            shapeNode = currentNode

        if transformNode is None:
            continue

        if shapeNode is None:
            nodeType = "group"
        else:
            nodeType = shapeNode.type()

        if nodeType in filters:
            if selTransformFlg == 1:
                if transformNode not in resultNodes:
                    resultNodes.append(transformNode)
            if selShapeFlg == 1:
                resultNodes.append(shapeNode)

    return resultNodes


#-------------------------------------------------
#設定を読み込み
def loadConfig():
    loadedConfigInfo = {}

    #テキストファイルの読み込み
    if os.path.isfile(configFilePath):
        f = open(configFilePath)
        allLines = f.readlines()
        f.close()

        for currentLineString in allLines:
            paramParts = currentLineString.replace("\n", "").split("@")
            if len(paramParts) == 2:
                loadedConfigInfo[paramParts[0]] = int(paramParts[1])

    return loadedConfigInfo


#-------------------------------------------------
if __name__ == '__main__':
    main()
