# -*- coding: utf-8 -*-

"""
スクリプトのテストを簡易にするツール

"""

g_toolName = "CySourceScript"
__author__ = "Cygames, Inc. Yuta Kimura"

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os
import re
import time
import imp
import types

import maya.cmds as mc
import maya.mel as mm
import pymel.core as pm

import CyOpenWinExplorer;reload(CyOpenWinExplorer)

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

        #UIの定義
        self.window = pm.window(g_toolName, title=g_toolName, minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            with pm.columnLayout(rowSpacing=3, columnOffset=("left", 5)):
                pm.separator(height=5, style="none")
                for currentCnt in range(5):
                    currentLineIndex = str(currentCnt + 1)
                    currentTextFieldName_filePath = "textField_filePath_" + currentLineIndex
                    currentTextFieldName_function = "textField_function_" + currentLineIndex

                    with pm.rowLayout(numberOfColumns=12):
                        pm.text(width=30, label="[ " + str(currentCnt + 1) + " ]")

                        try:
                            self.__dict__[currentTextFieldName_filePath] = pm.textField(width=400, changeCommand=pm.Callback(self.saveConfig), enterCommand=pm.Callback(self.saveConfig), placeholderText="MEL or Python File Path")
                            self.__dict__[currentTextFieldName_function] = pm.textField(width=150, changeCommand=pm.Callback(self.saveConfig), enterCommand=pm.Callback(self.saveConfig), annotation=u"指定しない場合はmain()が実行されます。", placeholderText="function(arg1, arg2, arg3)")
                        except:
                            self.__dict__[currentTextFieldName_filePath] = pm.textField(width=400, changeCommand=pm.Callback(self.saveConfig), enterCommand=pm.Callback(self.saveConfig))
                            self.__dict__[currentTextFieldName_function] = pm.textField(width=150, changeCommand=pm.Callback(self.saveConfig), enterCommand=pm.Callback(self.saveConfig), annotation=u"指定しない場合はmain()が実行されます。")

                        pm.separator(width=1, style="none")

                        pm.button(width=35, label=u"参照", command=pm.Callback(self.selectScript, currentLineIndex))
                        pm.button(width=35, label=u"編集", command=pm.Callback(self.editScript, currentLineIndex))
                        pm.button(width=53, label=u"Explorer", command=pm.Callback(self.explorerScript, currentLineIndex))

                        pm.separator(width=3, style="none")

                        pm.button(width=30, label="Run", bgc=[0.7,0.7,0.7], command=pm.Callback(self.sourceRunScript, currentLineIndex, "run"))
                        pm.button(width=45, label="Source", bgc=[0.7,0.7,0.7], command=pm.Callback(self.sourceRunScript, currentLineIndex, "source"))
                        pm.button(width=85, label=u"Source ＆ Run", bgc=[0.7,0.7,0.7], command=pm.Callback(self.sourceRunScript, currentLineIndex, "sourceRun"))

                    #前回の設定を復帰
                    if currentLineIndex in loadedConfigInfo:
                        if "filePath" in loadedConfigInfo[currentLineIndex] and "function" in loadedConfigInfo[currentLineIndex]:
                            self.__dict__[currentTextFieldName_filePath].setText(loadedConfigInfo[currentLineIndex]["filePath"])
                            self.__dict__[currentTextFieldName_function].setText(loadedConfigInfo[currentLineIndex]["function"])

        #ウィンドウのサイズ変更
        winWidthValue = 904
        winHeightValue = 155
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue += 5
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    #-------------------------
    #スクリプトファイルを選択
    def selectScript(self, targetLineIndex):
        self.saveConfig()
        inputtedFilePath = self.__dict__["textField_filePath_" + str(targetLineIndex)].getText()

        #ダイアログの開始フォルダ
        targetFolderPath = os.path.dirname(inputtedFilePath)
        if targetFolderPath == "":
            targetFolderPath = pm.internalVar(userAppDir=1) + "/scripts"

        try:
            selectedFilePaths = pm.fileDialog2(fileMode=1, caption=u"スクリプトファイル (Mel or Python) を選択して下さい。", fileFilter="All Files (*.*);;Mel Files (*.mel);;Python Files (*.py)", startingDirectory=targetFolderPath)
            if len(selectedFilePaths) == 1:
                self.__dict__["textField_filePath_" + str(targetLineIndex)].setText(selectedFilePaths[0])
                self.saveConfig()
        except:
            pass

        return

    #-------------------------
    #Source & Run Script
    def sourceRunScript(self, targetLineIndex, mode):
        print("\n#CySourceScript-------------------------------------------------")

        self.saveConfig()
        inputtedFilePath = self.__dict__["textField_filePath_" + str(targetLineIndex)].getText().replace("\\", "/")
        inputtedFuncStr = self.__dict__["textField_function_" + str(targetLineIndex)].getText()

        #実行予定の関数情報
        targetFuncStr = ""
        targetFuncName = ""
        if inputtedFuncStr != "":
            targetFuncStr = inputtedFuncStr
            targetFuncName = targetFuncStr.split("(")[0]

        print("#    inputted file : " + "\"" + inputtedFilePath + "\"")
        print("#    inputted function : " + "\"" + inputtedFuncStr + "\"")
        print("#    mode : " + mode)
        print("#")

        if inputtedFilePath != "":
            if os.path.isfile(inputtedFilePath):
                inputtedFileName = os.path.basename(inputtedFilePath)

                #モジュール内の関数情報を取得
                melFuncInfo = self.getModuleFuncInfo(inputtedFilePath, "mel")

                #MEL
                if inputtedFileName.endswith(".mel"):
                    inputtedFileSimpleName = inputtedFileName.replace(".mel", "")

                    #Source Script
                    if mode == "source" or mode == "sourceRun":
                        print("#    source : " + inputtedFilePath)
                        mm.eval('source "' + inputtedFilePath + '"')

                    #Run Script
                    if mode == "run" or mode == "sourceRun":
                        #関数が指定されている場合
                        if targetFuncStr != "":
                            #関数が存在する場合
                            if targetFuncName in melFuncInfo["funcNames"]:
                                #Melコマンドを実行
                                melCommandStr = targetFuncStr + ";"
                                self.executeCommand(melCommandStr, "mel")

                            #関数が存在しない場合
                            else:
                                self.showMessage(u"「 " + targetFuncName + u"() 」 という関数が見つからないため実行することが出来ませんでした。")

                        #関数が指定されていない場合
                        else:
                            if mode == "run":
                                #Melファイルを直接実行
                                print("#    runfile : " + inputtedFilePath)
                                mm.eval('source "' + inputtedFilePath + '"')

                #Python
                elif inputtedFileName.endswith(".py"):
                    inputtedFileSimpleName = inputtedFileName.replace(".py", "")

                    targetModule = None

                    #Source Script
                    if mode == "source" or mode == "sourceRun":
                        print("#    source : " + inputtedFilePath)
                        targetModule = imp.load_source(inputtedFileSimpleName, inputtedFilePath)

                    #Run Script
                    if mode == "run" or mode == "sourceRun":
                        if mode == "run":
                            targetModule = __import__(inputtedFileSimpleName, {}, {}, [])

                        #モジュール内の関数情報を取得
                        pyFuncInfo = self.getModuleFuncInfo(targetModule, "python")

                        #関数が指定されている場合
                        if targetFuncStr != "":
                            #関数が存在する場合
                            if targetFuncName in pyFuncInfo["funcNames"]:
                                #Pythonコマンドを実行
                                pyCommandStr = "import " + targetModule.__name__ + ";" + targetModule.__name__ + "." + targetFuncStr
                                self.executeCommand(pyCommandStr, "python")

                            #関数が存在しない場合
                            else:
                                self.showMessage(u"「 " + targetFuncName + u"() 」 という関数が見つからないため実行することが出来ませんでした。")

                        #関数が指定されていない場合
                        else:
                            #Pythonファイルを直接実行
                            print("#    runfile : " + inputtedFilePath)

                            #↓何故かどちらも正常に動作しない。
                            execfile(inputtedFilePath)
                            #eval("execfile('" + inputtedFilePath + "')")
                else:
                    self.showMessage(u"MELかPython以外のファイルは無効です。")
            else:
                self.showMessage(u"指定されたファイルが存在しません。")
        else:
            self.showMessage(u"MELかPythonのファイルを指定して下さい。")

        print("\n#---------------------------------------------------------------\n")

        return

    #-------------------------
    #コマンドを実行
    def executeCommand(self, commandStr, mode):
        print("#    run : " + commandStr)
        print("")
        time1 = time.clock()

        if mode == "mel":
            mm.eval(commandStr)
        elif mode == "python":
            exec(commandStr)

        time2 = time.clock()
        time3 = time2 - time1
        print("")
        print("#    processing time : " + str(time3))

        return

    #-------------------------
    #メッセージを表示
    def showMessage(self, messageStr):
        print(u"#    " + messageStr)
        pm.confirmDialog(title=g_toolName, message=u"● " + messageStr)

        return

    #-------------------------
    #モジュール内の関数情報を取得
    def getModuleFuncInfo(self, melFilePath_or_pyModule, fileType):
        moduleFuncInfo = {}

        funcNames = []

        if fileType == "mel":
            melFilePath = melFilePath_or_pyModule

            #テキストファイルの読み込み
            f = open(melFilePath)
            allLines = f.readlines()
            f.close()

            for currentLineStr in allLines:
                currentLineParts = currentLineStr.replace("\n", "").split()
                if len(currentLineParts) >= 3:
                    if currentLineParts[0] == "global" and currentLineParts[1] == "proc":
                        currentFuncName = currentLineParts[2].split("(")[0]
                        funcNames.append(currentFuncName)

        elif fileType == "python":
            pyModule = melFilePath_or_pyModule

            for currentAttrName in pyModule.__dict__:
                #関数のみ
                if isinstance(pyModule.__dict__[currentAttrName], types.FunctionType):
                    funcNames.append(currentAttrName)

        moduleFuncInfo["funcNames"] = funcNames

        return moduleFuncInfo

    #-------------------------
    #スクリプトファイルを編集
    def editScript(self, targetLineIndex):
        self.saveConfig()
        inputtedFilePath = self.__dict__["textField_filePath_" + str(targetLineIndex)].getText()
        command = "start \"\" " + inputtedFilePath.replace("/", "\\")
        os.system(command)

        return

    #-------------------------
    #スクリプトファイルをエクスプローラーで開く
    def explorerScript(self, targetLineIndex):
        self.saveConfig()
        inputtedFilePath = self.__dict__["textField_filePath_" + str(targetLineIndex)].getText()
        CyOpenWinExplorer.open("", inputtedFilePath)

        return

    #-------------------------
    #設定を保存
    def saveConfig(self):
        configString = ""
        for currentCnt in range(5):
            currentLineIndex = str(currentCnt + 1)
            currentTextFieldName_filePath = "textField_filePath_" + currentLineIndex
            currentTextFieldName_function = "textField_function_" + currentLineIndex

            currentScriptFilePath = self.__dict__[currentTextFieldName_filePath].getText()
            currentScriptFuncStr = self.__dict__[currentTextFieldName_function].getText()

            if currentScriptFilePath == "":
                currentScriptFilePath = "?"
            if currentScriptFuncStr == "":
                currentScriptFuncStr = "?"

            if configString != "":
                configString += "\n"
            configString += "index@" + currentLineIndex + " | " + "filePath@" + currentScriptFilePath + " | " + "function@" + currentScriptFuncStr

        if not os.path.isdir(g_configFolderPath):
            os.makedirs(g_configFolderPath)

        #テキストファイルの書き込み
        f = open(g_configFilePath, "w")
        f.write(configString)
        f.close()

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

            for currentLineStr in allLines:
                lineParts = currentLineStr.replace("\n", "").split(" | ")
                if len(lineParts) == 3:
                    lineInfo = {}
                    for currentPart in lineParts:
                        paramParts = currentPart.split("@")
                        if len(paramParts) == 2:
                            lineInfo[paramParts[0]] = paramParts[1]

                    if "index" in lineInfo and "filePath" in lineInfo and "function" in lineInfo:
                        if lineInfo["filePath"] == "?":
                            lineInfo["filePath"] = ""
                        if lineInfo["function"] == "?":
                            lineInfo["function"] = ""

                        loadedConfigInfo[lineInfo["index"]] = {"filePath":lineInfo["filePath"], "function":lineInfo["function"]}

        return loadedConfigInfo


#-------------------------------------------------
if __name__ == "__main__":
    main()
