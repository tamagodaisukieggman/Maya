# -*- coding: utf-8 -*-

"""
複数エクスポーターのUI部分

以下のメソッドをオーバーライドすれば様々な複数エクスポーターのUIとして使用することが出来ます。
MainWindow.exportFunc()
MainWindow.helpFunc()
※参考：CyExportModel.py

"""
from __future__ import unicode_literals
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import os
import pymel.core as pm

import CyOpenWinExplorer
import CyOpenWebPage
reload(CyOpenWinExplorer)
reload(CyOpenWebPage)

toolName = "CyMultiExporterUI"
__author__ = "Cygames, Inc. Yuta Kimura"
attrShortName_folderPath = "exportInfo_folderPath"


#-------------------------------------------------
#メイン(デバッグ用)
def debug_main(mainFileType="fbx"):
    #ツール情報
    toolInfo = {}
    toolInfo["toolName"] = toolName             #ツール名
    toolInfo["mainFileType"] = mainFileType     #メインのファイルタイプ
    toolInfo["fileTypes"] = []                  #ファイルタイプオプションメニューの項目
    toolInfo["fileTypes"].append("obj")
    toolInfo["fileTypes"].append("fbx")

    #メインウィンドウオブジェクトの生成
    mainWindow = MainWindow(toolInfo)

    return


##################################################
#メインウィンドウクラス
class MainWindow(object):
    def __init__(self, toolInfo):
        self.type = "window"

        #ツール情報
        self.toolInfo = toolInfo
        self.toolName = toolInfo["toolName"]
        self.fileType = toolInfo["mainFileType"]
        self.fileTypes = toolInfo["fileTypes"]

        #maya設定フォルダのパス
        userAppDirPath = pm.internalVar(userAppDir=1)

        #ツール設定のパス
        self.configFolderPath = userAppDirPath + "Cygames/" + self.toolName
        self.configFilePath = self.configFolderPath + "/" + self.toolName + ".ini"

        #既にウィンドウが開いている場合は閉じる
        if pm.window(self.toolName, q=1, exists=1):
            pm.deleteUI(self.toolName)

        self.nodeLines = []

        #UIの定義
        self.window = pm.window(self.toolName, title=self.toolName, minimizeButton=0, maximizeButton=0, sizeable=1, resizeToFitChildren=1)
        with self.window:
            #フォームレイアウト
            self.formLayout_main = pm.formLayout(numberOfDivisions=100)
            with self.formLayout_main:
                #フレームレイアウト(上部)
                self.frameLayout_header = pm.frameLayout(borderVisible=0, marginWidth=5, marginHeight=5, labelVisible=0, width=300, label=u"")
                with self.frameLayout_header:
                    with pm.rowLayout(numberOfColumns=5, adjustableColumn=4):
                        #ファイルタイプオプションメニュー
                        self.optionMenu_fileType = pm.optionMenu(w=125, cc=pm.Callback(self.fileTypeOptionMenu_change))
                        for currentFileType in self.fileTypes:
                            pm.menuItem(parent=self.optionMenu_fileType, label=" File Type : " + currentFileType.upper())

                        pm.separator(width=10, style="none")

                        #「フォルダ作成」チェックボックス
                        self.checkBox_option_makedirsFlg = pm.checkBox(label=u"保存先フォルダが存在しない場合は自動作成する", cc=pm.Callback(self.optionCheckBox_changeCommand, "checkBox_option_makedirsFlg"))

                        pm.separator(style="none")

                        #「ヘルプ」ボタン
                        self.button_help = pm.button(width=40, height=20, label=u"ヘルプ", align="right", command=pm.Callback(self.helpButton_onClick))

                #フレームレイアウト(ノードリスト)
                self.frameLayout_nodeList = pm.frameLayout(bgc=[0.2,0.4,0.3], borderVisible=1, borderStyle="etchedIn", marginWidth=5, marginHeight=5, labelVisible=0, label="")
                with self.frameLayout_nodeList:
                    with pm.rowLayout(numberOfColumns=3, adjustableColumn=2):
                        #リストを更新ボタン
                        self.button_refreshNodeList = pm.button(bgc=[0.6,0.6,0.6], width=120, height=20, label=u"↓ノードリストを更新", command=pm.Callback(self.refreshNodeListButton_onClick))

                        pm.separator(style="none")

                        #「全ノード選択」ボタン
                        self.button_selectAllNode = pm.button(bgc=[0.6,0.6,0.6], width=120, height=20, label=u"↓ノードを全て選択", command=pm.Callback(selectNodeButton_onClick, self, "all"))

                    #スクロールレイアウト
                    self.scrollLayout_list = pm.scrollLayout(childResizable=1, bgc=[0.35,0.35,0.35])
                    with self.scrollLayout_list:
                        #エクスポート情報一覧をリフレッシュ
                        self.refreshNodeList()

                #フレームレイアウト(同一保存先)
                self.frameLayout_oneDst = pm.frameLayout(bgc=[0.2,0.3,0.4], collapse=0, collapsable=0, borderVisible=1, borderStyle="etchedIn", marginWidth=5, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"A : 全てのノードを同一の保存先にエクスポートする場合")
                with self.frameLayout_oneDst:
                    with pm.rowLayout(numberOfColumns=6, adjustableColumn=2):
                        pm.text(label=u"メインの保存先", font="boldLabelFont", width=80)

                        #エクスポート先フォルダパス
                        try:
                            self.textField_folderPath = pm.textField(text="", changeCommand=pm.Callback(textField_onChange, self), enterCommand=pm.Callback(textField_onChange, self), placeholderText=u"保存先フォルダパス")
                        except:
                            self.textField_folderPath = pm.textField(text="", changeCommand=pm.Callback(textField_onChange, self), enterCommand=pm.Callback(textField_onChange, self))

                        pm.separator(width=1, style="none")

                        #フォルダ選択ボタン
                        self.button_selectDst = pm.button(width=35, height=20, label=u"参照", command=pm.Callback(selectFolderButton_onClick, self))

                        #Explorerボタン
                        self.button_explorer = pm.button(width=60, height=20, label=u"Explorer", command=pm.Callback(explorerButton_onClick, self))

                    #ローレイアウト
                    with pm.rowLayout(numberOfColumns=2, adjustableColumn=1):
                        pm.separator(width=1, style="none")

                        #エクスポートボタン
                        self.button_exportOneDst = pm.button(width=95, label=u"A : Exportを実行", bgc=[0.5,0.6,0.7], command=pm.Callback(self.exportButton_onClick, "oneDst"))

                #フレームレイアウト(複数保存先)
                self.frameLayout_multiDst = pm.frameLayout(bgc=[0.2,0.4,0.3], collapse=0, collapsable=0, borderVisible=1, borderStyle="etchedIn", marginWidth=5, marginHeight=5, labelVisible=1, font="plainLabelFont", label=u"B : ノードごとに保存先が異なる場合")
                with self.frameLayout_multiDst:
                    with pm.rowLayout(numberOfColumns=4, adjustableColumn=3):
                        pm.text(label=u"個別の保存先が未指定の場合 ：")

                        #複数保存先オプションメニュー
                        self.optionMenu_option_multiDstMode = pm.optionMenu(w=170, cc=pm.Callback(self.multiDstOptionMenu_change))
                        pm.menuItem(parent=self.optionMenu_option_multiDstMode, label=u"何もしない")
                        pm.menuItem(parent=self.optionMenu_option_multiDstMode, label=u"「 A : メインの保存先 」 に保存")

                        pm.separator(width=1, style="none")

                        #エクスポートボタン
                        self.button_exportMultiDst = pm.button(width=95, label=u"B : Exportを実行", bgc=[0.5,0.7,0.6], command=pm.Callback(self.exportButton_onClick, "multiDst"))

            #フォームレイアウトの編集
            afValue = []
            afValue.append((self.frameLayout_header, "top", 2))
            afValue.append((self.frameLayout_header, "right", 10))
            afValue.append((self.frameLayout_header, "left", 10))

            afValue.append((self.frameLayout_nodeList, "right", 10))
            afValue.append((self.frameLayout_nodeList, "left", 10))

            afValue.append((self.frameLayout_oneDst, "right", 10))
            afValue.append((self.frameLayout_oneDst, "left", 10))

            afValue.append((self.frameLayout_multiDst, "right", 10))
            afValue.append((self.frameLayout_multiDst, "left", 10))
            afValue.append((self.frameLayout_multiDst, "bottom", 10))

            acValue = []
            acValue.append((self.frameLayout_nodeList, "top", 0, self.frameLayout_header))

            acValue.append((self.frameLayout_nodeList, "bottom", 10, self.frameLayout_oneDst))
            acValue.append((self.frameLayout_oneDst, "bottom", 15, self.frameLayout_multiDst))

            anValue = []

            pm.formLayout(self.formLayout_main, e=1, attachForm=afValue, attachControl=acValue, attachNone=anValue)

        #オプション設定オブジェクト
        self.optionSetting = OptionSetting(self)

        #シーン設定を読み込み
        sceneSettingInfo = self.loadSceneSetting()
        self.extraAttr_folderPath = sceneSettingInfo["extraAttr_folderPath"]

        #UI設定を初期化
        self.initUISetting(sceneSettingInfo)

        #ウィンドウのサイズ変更
        if not pm.windowPref(self.toolName, exists=1):
            self.window.setWidthHeight([600, 500])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    ##########################
    #「エクスポート」ボタン
    def exportButton_onClick(self, mode):
        #UIからエクスポート情報を取得
        uiExportInfo = self.getExportInfoFromUI(mode)
        fileType = uiExportInfo["fileType"]
        exportNodes = uiExportInfo["exportNodes"]
        exportNodeName_dstFolderPath = uiExportInfo["exportNodeName_dstFolderPath"]

        #ノードリストの内容と現在の選択ノードを比較する
        confirmMessageStr = self.compareNodeListWithSelection(uiExportInfo)
        if confirmMessageStr:
            dialogResult = pm.confirmDialog(title=self.toolName, message=confirmMessageStr, button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
            if dialogResult == "No":
                return

        #エクスポート時のエラーチェック
        errorMessageStr = self.checkExportError(uiExportInfo, mode)
        if errorMessageStr:
            pm.confirmDialog(title=self.toolName, message=errorMessageStr)
            return

        #{保存先フォルダ:保存ファイル名のリスト}
        dstFolderPath_fileNames = {}
        for currentNode in exportNodes:
            currentNodeName = currentNode.longName()
            currentFileName = currentNodeName.split("|")[-1].split("__")[0] + "." + fileType
            currentDstFolderPath = exportNodeName_dstFolderPath[currentNodeName]

            if currentDstFolderPath not in dstFolderPath_fileNames:
                dstFolderPath_fileNames[currentDstFolderPath] = []
            dstFolderPath_fileNames[currentDstFolderPath].append(currentFileName)
        dstFolderPaths = list(dstFolderPath_fileNames.keys())
        dstFolderPaths.sort()

        #確認メッセージ
        messageStr = u"以下の内容でエクスポートします。"
        messageStr += "\n" + u"実行しますか？"
        for currentDstFolderPath in dstFolderPaths:
            messageStr += "\n"
            if not os.path.isdir(currentDstFolderPath):
                messageStr += "\n" + u"[フォルダ自動作成]"
            messageStr += "\n" + currentDstFolderPath

            fileNames = dstFolderPath_fileNames[currentDstFolderPath]
            fileNames.sort()
            for currentFileName in fileNames:
                messageStr += "\n" + u"   → " + currentFileName
        messageStr += "\n"

        dialogResult = pm.confirmDialog(title=self.toolName, message=messageStr, button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
        if dialogResult == "No":
            return

        #エクスポート
        self.exportFunc(uiExportInfo)

        #エラー表示をリフレッシュ
        self.refreshError()

        return

    ##########################
    #エクスポート
    def exportFunc(self, exportInfo):
        print("export!!")

        return

    ##########################
    #「ヘルプ」ボタン
    def helpButton_onClick(self):
        #ヘルプを開く
        self.helpFunc()

        return

    ##########################
    #ヘルプを開く
    def helpFunc(self):
        CyOpenWebPage.open("https://wisdom.cygames.jp/pages/viewpage.action?pageId=25927354")

        return

    ##########################
    #「ノードリストを更新」ボタン
    def refreshNodeListButton_onClick(self):
        #エクスポート情報一覧をリフレッシュ
        self.refreshNodeList()

        #エラー表示をリフレッシュ
        self.refreshError()

        return

    ##########################
    #オプション用チェックボックスの状態が変更された時の処理
    def optionCheckBox_changeCommand(self, uiName):
        #オプション設定を保存
        self.optionSetting.save()

        if uiName == "checkBox_option_makedirsFlg":
            #エラー表示をリフレッシュ
            self.refreshError()

        return

    ##########################
    #「リストから除外」ボタン
    def removeListItemButton_onClick(self, nodeLine):
        nodeName = nodeLine.node.longName()
        if pm.objExists(nodeName):
            pm.select(nodeName, deselect=1)
        pm.deleteUI(nodeLine.columnLayout_node)
        self.nodeLines.remove(nodeLine)
        del nodeLine

        return

    ##########################
    #ファイルタイプオプションメニュー
    def fileTypeOptionMenu_change(self):
        self.fileType = self.getOptionMenuValue("optionMenu_fileType")
        for currentNodeLine in self.nodeLines:
            currentNodeLine.text_fileName_ext.setLabel(self.fileType)

        return

    ##########################
    #複数保存先オプションメニュー
    def multiDstOptionMenu_change(self):
        #オプション設定を保存
        self.optionSetting.save()

        return

    ##########################
    #エクスポート情報一覧をリフレッシュ
    def refreshNodeList(self):
        selTransNodes = pm.ls(sl=1, transforms=1, flatten=1)
        selTransNodes = sorted(selTransNodes, key=lambda x: x.longName())

        with self.scrollLayout_list:
            #既にカラムレイアウトが存在する場合は削除
            if pm.columnLayout("columnLayout_list", q=1, exists=1):
                pm.deleteUI("columnLayout_list")

            #カラムレイアウト
            self.columnLayout_list = pm.columnLayout("columnLayout_list", adjustableColumn=1)
            with self.columnLayout_list:
                self.nodeLines = []
                for currentNodeIndex in range(len(selTransNodes)):
                    currentNode = selTransNodes[currentNodeIndex]

                    #ノード行を追加
                    currentNodeLine = NodeLine(currentNode, currentNodeIndex, self)
                    self.nodeLines.append(currentNodeLine)

        #全ノード行のエラーチェック
        self.checkAllNodeLinesError()

        return

    ##########################
    #エラー表示をリフレッシュ
    def refreshError(self):
        #テキストフィールドの背景色を変更
        textField_changeBgColor(self)

        for currentNodeLine in self.nodeLines:
            #エラー表示を変更
            currentNodeLine.nodeErrorText_change()

            if len(currentNodeLine.folderLines) == 1:
                #テキストフィールドの背景色を変更
                textField_changeBgColor(currentNodeLine.folderLines[0])

        return

    ##########################
    #UIからエクスポート情報を取得
    def getExportInfoFromUI(self, mode):
        uiExportInfo = {}
        uiExportInfo["mainFolderPath"] = mainFolderPath = self.textField_folderPath.getText()
        uiExportInfo["fileType"] = self.fileType
        uiExportInfo["allNodes"] = []
        uiExportInfo["exportNodes"] = []
        uiExportInfo["exportNodeName_dstFolderPath"] = {}
        uiExportInfo["useMainNodeLines"] = []

        #全てのオプション設定の値を取得
        self.optionSetting.getAll()
        for currentUiName in self.optionSetting.uiName_value:
            currentParamName = currentUiName.split("_option_")[-1]
            currentParamValue = self.optionSetting.uiName_value[currentUiName]
            uiExportInfo[currentParamName] = currentParamValue

        for currentNodeLine in self.nodeLines:
            currentNode = currentNodeLine.node
            uiExportInfo["allNodes"].append(currentNode)

            #エクスポート先フォルダパスを取得
            dstFolderPath = ""
            if mode == "oneDst":
                dstFolderPath = mainFolderPath
                uiExportInfo["useMainNodeLines"].append(currentNodeLine)
            elif mode == "multiDst":
                #個別フォルダが設定されていない場合
                if len(currentNodeLine.folderLines) == 0:
                    #メインフォルダにエクスポートする場合
                    if uiExportInfo["multiDstMode"] == "mainFolder":
                        dstFolderPath = mainFolderPath
                        uiExportInfo["useMainNodeLines"].append(currentNodeLine)

                #個別フォルダが設定されている場合
                elif len(currentNodeLine.folderLines) == 1:
                    dstFolderPath = currentNodeLine.folderLines[0].textField_folderPath.getText()

            if dstFolderPath != "":
                uiExportInfo["exportNodes"].append(currentNode)
                uiExportInfo["exportNodeName_dstFolderPath"][currentNodeLine.nodeName] = dstFolderPath

        return uiExportInfo

    ##########################
    #ノードリストの内容と現在の選択ノードを比較する
    def compareNodeListWithSelection(self, uiExportInfo):
        confirmMessageStr = ""

        #ノードリストに表示されているノード
        exportNodes = uiExportInfo["allNodes"]
        exportNodesSet = set(exportNodes)

        #現在の選択ノード
        selTransNodes = pm.ls(sl=1, transforms=1, flatten=1)
        selTransNodesSet = set(selTransNodes)

        #共通のノード
        matchedNodes = list(exportNodesSet & selTransNodesSet)

        if len(exportNodes) == len(selTransNodes) == len(matchedNodes):
            pass
        else:
            confirmMessageStr = u"ノードリストの内容と選択ノードが一致しません。"
            confirmMessageStr += "\n"
            confirmMessageStr += "\n" + u" [Yes] " + u"現在のノードリストの内容でエクスポートを実行します。"
            confirmMessageStr += "\n" + u" [No] " + u"エクスポートをキャンセルします。"
            confirmMessageStr += "\n" + u"          → " + u"ノードリストを更新してから再び実行して下さい。"

        return confirmMessageStr

    ##########################
    #エクスポート時のエラーチェック
    def checkExportError(self, uiExportInfo, mode):
        errorMessageStr = ""

        #メインフォルダのチェック
        mainFolderErrorFlg = 0
        mainFolderStatus = checkFolder(uiExportInfo["mainFolderPath"], uiExportInfo["makedirsFlg"])
        if mainFolderStatus == "" or mainFolderStatus == "none" or mainFolderStatus == "ng":
            if mode == "oneDst":
                mainFolderErrorFlg = 1
            elif mode == "multiDst":
                if len(uiExportInfo["useMainNodeLines"]) > 0:
                    mainFolderErrorFlg = 1

        if mainFolderErrorFlg == 1:
            errorMessageStr += "\n\n" + u" ・ " + u"「 A : メインの保存先 」 が無効です。"

        #エクスポート可能なノードがあるかどうかのチェック
        if len(uiExportInfo["exportNodes"]) == 0:
            errorMessageStr += "\n\n" + u" ・ " + u"エクスポート可能なノードが1つもありません。"

        #全ノード行のエラーチェック
        allNodeLinesErrorInfo = self.checkAllNodeLinesError()
        if mode == "multiDst":
            errorMessageStr += self.getMessageStr(allNodeLinesErrorInfo["folderErrorNodes"], u"保存先フォルダパスが無効です。")
        errorMessageStr += self.getMessageStr(allNodeLinesErrorInfo["familyMemberNodes"], u"親子関係のあるノードを同時にエクスポートすることは出来ません。")

        if errorMessageStr != "":
            errorMessageStr = u"エラー！" + errorMessageStr

        return errorMessageStr

    ##########################
    #エラーメッセージ:エラーノードのリストを文字列で取得
    def getMessageStr(self, errorNodes, errorMessageStr):
        messageStr = ""

        if len(errorNodes) > 0:
            messageStr += "\n\n" + u" ・ " + errorMessageStr
            for currentNode in errorNodes:
                messageStr += "\n" + u"    " + currentNode.longName()

        return messageStr

    ##########################
    #全ノード行のエラーチェック
    def checkAllNodeLinesError(self):
        allNodeLinesErrorInfo = {}

        folderErrorNodes = []
        familyMemberNodes = []

        for nodeLineA in self.nodeLines:
            nodeA = nodeLineA.node
            nodeAName = nodeA.longName()

            #ノード行のエラーチェック
            nodeLineErrorFlg = nodeLineA.checkNodeLineError()
            if nodeLineErrorFlg:
                folderErrorNodes.append(nodeA)

            for nodeLineB in self.nodeLines:
                nodeB = nodeLineB.node
                nodeBName = nodeB.longName()

                if nodeAName != nodeBName:
                    #親子関係チェック
                    if nodeAName.startswith(nodeBName + "|"):
                        nodeLineA.errorInfo["b_familyError"] = 1
                        nodeLineB.errorInfo["b_familyError"] = 1

                        if nodeA not in familyMemberNodes:
                            familyMemberNodes.append(nodeA)

                        if nodeB not in familyMemberNodes:
                            familyMemberNodes.append(nodeB)

        allNodeLinesErrorInfo["folderErrorNodes"] = sorted(folderErrorNodes, key=lambda x: x.longName())
        allNodeLinesErrorInfo["familyMemberNodes"] = sorted(familyMemberNodes, key=lambda x: x.longName())

        return allNodeLinesErrorInfo

    ##########################
    #オプションメニューの選択値を取得
    def getOptionMenuValue(self, optionMenuName):
        optionMenuValue = ""

        if optionMenuName in self.__dict__:
            selMenuItemLabel = self.__dict__[optionMenuName].getValue()
            optionMenuValue = self.getMenuItemStr(optionMenuName, selMenuItemLabel, "label_value")

        return optionMenuValue

    ##########################
    #オプションメニューのメニュー項目(文字列)を取得
    def getMenuItemStr(self, optionMenuName, value_or_label, mode):
        menuItemStr = ""

        #{コントロール名:値:ラベル}
        optionMenuName_value_label = {}

        optionMenuName_value_label["optionMenu_fileType"] = {}
        for currentFileType in self.fileTypes:
            optionMenuName_value_label["optionMenu_fileType"][currentFileType] = " File Type : " + currentFileType.upper()

        optionMenuName_value_label["optionMenu_option_multiDstMode"] = {}
        optionMenuName_value_label["optionMenu_option_multiDstMode"]["none"] = u"何もしない"
        optionMenuName_value_label["optionMenu_option_multiDstMode"]["mainFolder"] = u"「 A : メインの保存先 」 に保存"

        #{コントロール名:ラベル:値}
        optionMenuName_label_value = {}
        for currentOptionMenuName in optionMenuName_value_label:
            optionMenuName_label_value[currentOptionMenuName] = {}
            for currentValue in optionMenuName_value_label[currentOptionMenuName]:
                currentLabel = optionMenuName_value_label[currentOptionMenuName][currentValue]
                optionMenuName_label_value[currentOptionMenuName][currentLabel] = currentValue

        #値からラベルを取得
        if mode == "value_label":
            targetValue = value_or_label
            if optionMenuName in optionMenuName_value_label:
                if targetValue in optionMenuName_value_label[optionMenuName]:
                    menuItemStr = optionMenuName_value_label[optionMenuName][targetValue]

        #ラベルから値を取得
        elif mode == "label_value":
            targetLabel = value_or_label
            if optionMenuName in optionMenuName_label_value:
                if targetLabel in optionMenuName_label_value[optionMenuName]:
                    menuItemStr = optionMenuName_label_value[optionMenuName][targetLabel]

        return menuItemStr

    ##########################
    #UI設定を初期化
    def initUISetting(self, sceneSettingInfo):
        #ファイルタイプオプションメニュー
        optionMenuValue = self.getMenuItemStr("optionMenu_fileType", self.fileType, "value_label")
        self.optionMenu_fileType.setValue(optionMenuValue)

        self.textField_folderPath.setText(sceneSettingInfo["folderPath"])

        #テキストフィールドの背景色を変更
        textField_changeBgColor(self)

        #エラー表示をリフレッシュ
        self.refreshError()

        return

    ##########################
    #シーン設定を読み込み
    def loadSceneSetting(self):
        sceneSettingInfo = {}
        sceneSettingInfo["extraAttr_folderPath"] = None
        sceneSettingInfo["folderPath"] = ""

        selNodes = pm.ls(sl=1)

        #ツール設定用ロケーター
        topLocator = None
        topLocatorName = "CygamesTools"
        if pm.objExists(topLocatorName):
            topLocator = pm.PyNode(topLocatorName)
        else:
            topLocator = pm.spaceLocator(position=(0,0,0), name=topLocatorName)

        configLocator = None
        configLocatorName = self.toolName
        if pm.objExists(configLocatorName):
            configLocator = pm.PyNode(configLocatorName)
        else:
            configLocator = pm.spaceLocator(position=(0,0,0), name=configLocatorName)

        if configLocator.getParent() != topLocator:
            configLocator.setParent(topLocator)

        #エクストラアトリビュート
        if configLocator.hasAttr(attrShortName_folderPath):
            sceneSettingInfo["folderPath"] = configLocator.getAttr(attrShortName_folderPath)
        else:
            #エクストラアトリビュートを追加
            configLocator.addAttr(attrShortName_folderPath, niceName=attrShortName_folderPath, dataType="string")
            configLocator.setAttr(attrShortName_folderPath, "")

        sceneSettingInfo["extraAttr_folderPath"] = configLocator.attr(attrShortName_folderPath)

        pm.select(selNodes)

        return sceneSettingInfo


##################################################
#オプション設定クラス
class OptionSetting(object):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        #ツール設定のパス
        self.configFolderPath = self.mainWindow.configFolderPath
        self.configFilePath = self.mainWindow.configFilePath

        self.uiNames = []
        self.uiNames.append("checkBox_option_makedirsFlg")
        self.uiNames.append("optionMenu_option_multiDstMode")

        #オプション設定を読み込み
        self.uiName_value = self.load()

        #オプション設定の値を適用
        for currentUiName in self.uiNames:
            if currentUiName in self.uiName_value:
                currentUiValue = self.uiName_value[currentUiName]
                self.set(currentUiName, currentUiValue, mainWindow)

        return

    ##########################
    #オプション設定を読み込み
    def load(self):
        uiName_value = {}

        #テキストファイルの読み込み
        loadedConfigInfo = {}
        if os.path.isfile(self.configFilePath):
            f = open(self.configFilePath)
            allLines = f.readlines()
            f.close()

            for currentLineString in allLines:
                paramParts = currentLineString.replace("\n", "").split("@")
                if len(paramParts) == 2:
                    currentParamName = paramParts[0]
                    currentValue = paramParts[1]
                    loadedConfigInfo[currentParamName] = currentValue

        #{UI名:値}
        for currentUiName in self.uiNames:
            uiName_value[currentUiName] = None
            if currentUiName in loadedConfigInfo:
                currentUiValue = loadedConfigInfo[currentUiName]
                uiName_value[currentUiName] = currentUiValue

        return uiName_value

    ##########################
    #オプション設定を保存
    def save(self):
        #全てのオプション設定の値を取得
        configString = self.getAll()

        #テキストファイルの書き込み
        if not os.path.isdir(self.configFolderPath):
            os.makedirs(self.configFolderPath)
        f = open(self.configFilePath, "w")
        f.write(configString)
        f.close()

        return

    ##########################
    #全てのオプション設定の値を取得
    def getAll(self):
        configString = ""

        for currentUiName in self.uiNames:
            #オプション設定の値を取得
            currentUiValue = self.get(currentUiName, self.mainWindow)

            self.uiName_value[currentUiName] = currentUiValue

            if configString != "":
                configString += "\n"
            configString += currentUiName + "@" + str(currentUiValue)

        return configString

    ##########################
    #オプション設定の値を取得
    @staticmethod
    def get(targetUiName, mainWindow):
        targetUiValue = None
        if targetUiName in mainWindow.__dict__:
            targetUiControl = mainWindow.__dict__[targetUiName]

            #チェックボックスの場合
            if isinstance(targetUiControl, pm.uitypes.CheckBox):
                targetUiValue = int(targetUiControl.getValue())

            #オプションメニューの場合
            elif isinstance(targetUiControl, pm.uitypes.OptionMenu):
                targetUiValue = mainWindow.getOptionMenuValue(targetUiName)

        return targetUiValue

    ##########################
    #オプション設定の値を適用
    @staticmethod
    def set(targetUiName, targetUiValue, mainWindow):
        if targetUiValue == None:
            return

        if targetUiName in mainWindow.__dict__:
            targetUiControl = mainWindow.__dict__[targetUiName]

            #チェックボックスの場合
            if isinstance(targetUiControl, pm.uitypes.CheckBox):
                targetUiValue = int(targetUiValue)
                targetUiControl.setValue(targetUiValue)

            #オプションメニューの場合
            elif isinstance(targetUiControl, pm.uitypes.OptionMenu):
                targetUiValue = mainWindow.getMenuItemStr(targetUiName, targetUiValue, "value_label")
                if targetUiValue != "":
                    targetUiControl.setValue(targetUiValue)

        return


##################################################
#ノード行
class NodeLine(object):
    def __init__(self, node, nodeIndex, mainWindow):
        self.type = "node"

        self.mainWindow = mainWindow

        self.node = node

        self.nodeName = node.longName()
        self.nodeLineId = str(nodeIndex)

        self.fileName = self.nodeName.split("|")[-1].split("__")[0]

        self.errorInfo = {}
        self.errorInfo["a_folderError"] = 0
        self.errorInfo["b_familyError"] = 0

        self.errorCommentInfo = {}
        self.errorCommentInfo["a_folderError"] = u" ・ " + u"保存先フォルダパスが無効です。"
        self.errorCommentInfo["b_familyError"] = u" ・ " + u"親子関係のあるノードがリスト内に存在します。"

        self.annotation = ""

        #カラムレイアウト
        self.columnLayout_node = pm.columnLayout(adjustableColumn=1)
        with self.columnLayout_node:
            pm.separator(height=3, style="none")

            #ローレイアウト(ノード行)
            with pm.rowLayout(numberOfColumns=13, adjustableColumn=10):
                pm.separator(width=3, style="none")

                #「リストから除外」ボタン
                self.button_removeListItem = pm.button(width=13, height=12, label=u"×", bgc=[0.25,0.25,0.25], command=pm.Callback(mainWindow.removeListItemButton_onClick, self))

                pm.separator(width=3, style="none")

                #ノード名
                self.text_nodeName = pm.text(label=self.nodeName, font="boldLabelFont", align="left")

                pm.separator(width=7, style="none")

                #ファイル名
                self.text_fileName_left = pm.text(label=u"( ファイル名 : ", align="left")
                self.text_fileName_name = pm.text(label=self.fileName, align="left")
                self.text_fileName_dot = pm.text(label=".", align="left")
                self.text_fileName_ext = pm.text(label=mainWindow.fileType, align="left")
                self.text_fileName_right = pm.text(label=" )", align="left")

                #エラー表示
                self.text_nodeError = pm.text(label=" error ! ", font="boldLabelFont", width=41, align="left", bgc=[0.8, 0.3, 0.3], annotation="", visible=0)

                #「ノード選択」ボタン
                self.button_selectNode = pm.button(width=60, height=20, label=u"ノード選択", command=pm.Callback(selectNodeButton_onClick, self, "one"))

                pm.separator(width=2, style="none")

            #ローレイアウト(フォルダ行)
            self.rowLayout_folder = pm.rowLayout(height=25, numberOfColumns=3, adjustableColumn=3)
            with self.rowLayout_folder:
                pm.separator(width=25, style="none")

                #「保存先追加・削除」ボタン
                self.button_folderLine = pm.button(width=16, height=16, label="", command=pm.Callback(self.folderLineButton_onClick))

                #フォルダ一覧をリフレッシュ
                self.folderLines = []
                self.folderLines = self.refreshFolderList()

                #保存先追加・削除ボタンの表示を変更
                self.folderLineButton_changeDisplay()

            #罫線を追加
            self.addSeparatorLine()

        return

    ##########################
    #罫線を追加
    def addSeparatorLine(self):
        with self.columnLayout_node:
            self.separator_line1 = pm.separator(height=3, style="none")
            self.separator_line2 = pm.separator(height=1, style="none", bgc=[0.6,0.6,0.6])

        return

    ##########################
    #「保存先追加・削除」ボタン
    def folderLineButton_onClick(self):
        #保存先追加の場合
        if len(self.folderLines) == 0:
            pm.deleteUI(self.separator_line1)
            pm.deleteUI(self.separator_line2)

            #フォルダ行を追加
            newFolderLine = FolderLine(self)
            self.folderLines.append(newFolderLine)

            #罫線を追加
            self.addSeparatorLine()

        #保存先削除の場合
        else:
            for folderLine in self.folderLines:
                pm.deleteUI(folderLine.rowLayout_folderLine)
                pm.deleteAttr(folderLine.extraAttr_folderPath)
                self.folderLines.remove(folderLine)
                del folderLine

        #保存先追加・削除ボタンの表示を変更
        self.folderLineButton_changeDisplay()

        #エラー表示を変更
        self.nodeErrorText_change()

        return

    ##########################
    #保存先追加・削除ボタンの表示を変更
    def folderLineButton_changeDisplay(self):
        bgColorValue = [0,0,0]
        if len(self.folderLines) == 0:
            self.button_folderLine.setLabel(u"+")
            bgColorValue = [1,1,1]
        else:
            self.button_folderLine.setLabel(u"-")
            bgColorValue = [1,0.7,0.3]

        self.button_folderLine.setBackgroundColor(bgColorValue)

        return

    ##########################
    #フォルダ一覧をリフレッシュ
    def refreshFolderList(self):
        #全てのフォルダ行を削除
        for oldFolderLine in self.folderLines:
            pm.deleteUI(oldFolderLine.rowLayout_folderLine)
            del oldFolderLine

        #フォルダ行を追加
        self.folderLines = []
        if self.node.hasAttr(attrShortName_folderPath):
            newFolderLine = FolderLine(self, self.node.attr(attrShortName_folderPath))
            self.folderLines.append(newFolderLine)

        return self.folderLines

    ##########################
    #ノード行のエラーチェック
    def checkNodeLineError(self):
        errorFlg = 0

        if self.node.hasAttr(attrShortName_folderPath):
            folderPath = self.node.getAttr(attrShortName_folderPath)

            if folderPath == "":
                errorFlg = 1
            else:
                #フォルダのチェック
                folderStatus = checkFolder(folderPath, OptionSetting.get("checkBox_option_makedirsFlg", self.mainWindow))
                if folderStatus == "" or folderStatus == "none" or folderStatus == "ng":
                    errorFlg = 1

        self.errorInfo["a_folderError"] = errorFlg

        return errorFlg

    ##########################
    #エラー表示を変更
    def nodeErrorText_change(self):
        #ノード行のエラーチェック
        self.checkNodeLineError()

        errorkeys = list(self.errorInfo.keys())
        errorkeys.sort()

        errorMessageStr = ""
        for currentErrorKey in errorkeys:
            if self.errorInfo[currentErrorKey]:
                if errorMessageStr != "":
                    errorMessageStr += "\n"
                errorMessageStr += self.errorCommentInfo[currentErrorKey]
        self.text_nodeError.setAnnotation(errorMessageStr)

        visibleValue = 0
        if errorMessageStr != "":
            visibleValue = 1
        self.text_nodeError.setVisible(visibleValue)

        return


##################################################
#フォルダ行
class FolderLine(object):
    def __init__(self, nodeLine, extraAttr=None):
        self.type = "folder"

        self.mainWindow = nodeLine.mainWindow

        self.parentNodeLine = nodeLine
        parentNodeLineId = nodeLine.nodeLineId

        self.extraAttr_folderPath = extraAttr
        if self.extraAttr_folderPath == None:
            #ノードにエクストラアトリビュートを追加
            nodeLine.node.addAttr(attrShortName_folderPath, niceName=attrShortName_folderPath, dataType="string")
            nodeLine.node.setAttr(attrShortName_folderPath, "")

            #追加されたエクストラアトリビュート
            newAttrLongName = nodeLine.node.longName() + "." + attrShortName_folderPath
            self.extraAttr_folderPath = pm.Attribute(newAttrLongName)

        self.folderPath = self.extraAttr_folderPath.get()
        if self.folderPath == None:
            self.folderPath = ""

        with nodeLine.rowLayout_folder:
            #ローレイアウト(フォルダ行)
            self.rowLayout_folderLine = pm.rowLayout(numberOfColumns=6, adjustableColumn=2)
            with self.rowLayout_folderLine:
                pm.separator(width=1, style="none")

                #エクスポート先フォルダパス
                try:
                    self.textField_folderPath = pm.textField(text=self.folderPath, changeCommand=pm.Callback(textField_onChange, self), enterCommand=pm.Callback(textField_onChange, self), placeholderText=u"保存先フォルダパス")
                except:
                    self.textField_folderPath = pm.textField(text=self.folderPath, changeCommand=pm.Callback(textField_onChange, self), enterCommand=pm.Callback(textField_onChange, self))

                pm.separator(width=1, style="none")

                #「参照」ボタン
                self.button_selectDst = pm.button(width=41, height=20, label=u"参照", command=pm.Callback(selectFolderButton_onClick, self))

                #「Explorer」ボタン
                self.button_explorer = pm.button(width=60, height=20, label=u"Explorer", command=pm.Callback(explorerButton_onClick, self))

                pm.separator(width=1, style="none")

        #テキストフィールドの背景色を変更
        textField_changeBgColor(self)

        return


#-------------------------------------------------
#テキストフィールドの値が変更された時に発生
def textField_onChange(self):
    inputtedFolderPath = self.textField_folderPath.getText()

    #テキストフィールドの背景色を変更
    textField_changeBgColor(self, inputtedFolderPath)

    #エクストラアトリビュートの値を更新
    self.extraAttr_folderPath.set(inputtedFolderPath)

    if self.type == "folder":
        #エラー表示を変更
        self.parentNodeLine.nodeErrorText_change()

    return


#-------------------------------------------------
#テキストフィールドの背景色を変更
def textField_changeBgColor(self, folderPath=""):
    if folderPath == "":
        folderPath = self.textField_folderPath.getText()

    bgColorValue = [0.165, 0.165, 0.165]
    errorMessageStr = ""

    makedirsFlg = 0
    if self.type == "window":
        makedirsFlg = OptionSetting.get("checkBox_option_makedirsFlg", self)
    elif self.type == "folder":
        makedirsFlg = OptionSetting.get("checkBox_option_makedirsFlg", self.mainWindow)

    #フォルダのチェック
    folderStatus = checkFolder(folderPath, makedirsFlg)

    #フォルダパスが入力されていない場合
    if folderStatus == "none":
        bgColorValue = [0.2,0.12,0.12]
        errorMessageStr = u"フォルダパスが入力されていません。"

    #フォルダが無効な場合
    elif folderStatus == "ng":
        bgColorValue = [0.2,0.12,0.12]
        errorMessageStr = u"保存先フォルダパスが無効です。"

    #フォルダを作成する場合
    elif folderStatus == "make":
        bgColorValue = [0.6,0.6,0]
        errorMessageStr = u"保存先フォルダが存在しないため自動作成します。"

    self.textField_folderPath.setBackgroundColor(bgColorValue)
    self.textField_folderPath.setAnnotation(errorMessageStr)

    return


#-------------------------------------------------
#「参照」ボタン
def selectFolderButton_onClick(self):
    inputtedFolderPath = self.textField_folderPath.getText()

    #ダイアログの開始フォルダ
    targetFolderPath = ""
    if os.path.isdir(inputtedFolderPath):
        targetFolderPath = inputtedFolderPath
    else:
        targetFolderPath = pm.system.sceneName()

    try:
        selectedFolderPaths = pm.fileDialog2(fileMode=3, caption=u"エクスポート先フォルダを選択して下さい。", startingDirectory=targetFolderPath)
        if len(selectedFolderPaths) == 1:
            self.textField_folderPath.setText(selectedFolderPaths[0])

            #テキストフィールドの背景色を変更
            textField_changeBgColor(self, selectedFolderPaths[0])

            #エクストラアトリビュートの値を更新
            self.extraAttr_folderPath.set(selectedFolderPaths[0])

            if self.type == "folder":
                #エラー表示を変更
                self.parentNodeLine.nodeErrorText_change()
    except:
        pass

    return


#-------------------------------------------------
#「ノード選択」ボタン
def selectNodeButton_onClick(self, mode):
    if mode == "one":
        pm.select(self.node)

    elif mode == "all":
        allNodes = []
        for currentNodeLine in self.nodeLines:
            allNodes.append(currentNodeLine.node)
        pm.select(allNodes)

    return


#-------------------------------------------------
#「Explorer」ボタン
def explorerButton_onClick(self):
    inputtedFilePath = self.textField_folderPath.getText()
    CyOpenWinExplorer.open("", inputtedFilePath)

    return


#-------------------------------------------------
#フォルダのチェック
def checkFolder(folderPath, makedirsFlg):
    folderStatus = ""

    #フォルダパスが入力されている場合
    if folderPath != "":
        #トップフォルダが存在する場合
        if os.path.isdir(folderPath.replace("\\", "/").split("/")[0]):
            #フォルダが存在する場合
            if os.path.isdir(folderPath):
                folderStatus = "ok"

            #フォルダが存在しない場合
            else:
                #フォルダを作成する場合
                if makedirsFlg == 1:
                    folderStatus = "make"

                #フォルダを作成しない場合
                else:
                    folderStatus = "ng"

        #トップフォルダが存在しない場合
        else:
            folderStatus = "ng"

    #フォルダパスが入力されていない場合
    else:
        folderStatus = "none"

    return folderStatus


#-------------------------------------------------
if __name__ == "__main__":
    debug_main("fbx")
