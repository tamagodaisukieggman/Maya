# -*- coding: utf-8 -*-

"""
モデルのエクスポート

"""
from __future__ import unicode_literals
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

toolName = "CyExportModel"
__author__ = "Cygames, Inc. Yuta Kimura"

import os

import maya.cmds as mc
import pymel.core as pm

import CyMultiExporterUI
import CyCreateExportModel
import CyOpenWebPage

reload(CyMultiExporterUI)
reload(CyCreateExportModel)
reload(CyOpenWebPage)


#-------------------------------------------------
#メイン
def main(mainFileType="fbx"):
    #ツール情報
    toolInfo = {}
    toolInfo["toolName"] = toolName             #ツール名
    toolInfo["mainFileType"] = mainFileType     #メインのファイルタイプ
    toolInfo["fileTypes"] = []                  #ファイルタイプオプションメニューの項目
    toolInfo["fileTypes"].append("ma")
    toolInfo["fileTypes"].append("mb")
    toolInfo["fileTypes"].append("obj")
    toolInfo["fileTypes"].append("fbx")

    #必要なプラグインをチェック
    checkPlugin()

    #メインウィンドウオブジェクトの生成
    mainWindow = MainWindow(toolInfo)

    return


##################################################
#メインウィンドウクラス
class MainWindow(CyMultiExporterUI.MainWindow):
    ##########################
    #エクスポート
    def exportFunc(self, exportInfo):
        #モデルをまとめてエクスポート
        exportAll(exportInfo)

        return

    ##########################
    #ヘルプを開く
    def helpFunc(self):
        CyOpenWebPage.open("https://wisdom.cygames.jp/display/designersmanual/Maya%3A+File#CyExportModel")

        return


#-------------------------------------------------
#モデルをまとめてエクスポート
def exportAll(exportInfo):
    selNodes = pm.ls(sl=1)

    nodes = exportInfo["exportNodes"]
    nodeName_dstFolderPath = exportInfo["exportNodeName_dstFolderPath"]
    fileType = exportInfo["fileType"]
    makedirsFlg = exportInfo["makedirsFlg"]

    for currentNode in nodes:
        #モデルをエクスポート
        exportOne(currentNode, nodeName_dstFolderPath[currentNode.longName()], fileType, makedirsFlg)

    pm.select(selNodes)

    messageStr = u"エクスポート完了！"
    pm.confirmDialog(title=toolName, message=u"● " + messageStr)

    return


#-------------------------------------------------
#モデルをエクスポート
def exportOne(currentNode, dstFolderPath, fileType, makedirsFlg=0):
    #エクスポート用のノード名
    exportNodeName = currentNode.shortName().split("__")[0]

    #シーン内に既に同名のノードが存在する場合は、既存ノードを一時リネーム
    existingNode = None
    if pm.objExists(exportNodeName):
        existingNode = pm.PyNode(exportNodeName)
        existingNode.rename(exportNodeName + "TEMP_TEMP_TEMP")

    #エクスポート用のモデルを作成(1データ)
    resultInfo = CyCreateExportModel.createOne(currentNode, "export")
    exportNode = resultInfo["topNode"]

    pm.select(exportNode)

    #ファイルパス
    if makedirsFlg == 1:
        if not os.path.exists(dstFolderPath):
            os.makedirs(dstFolderPath)
    exportFilePath = dstFolderPath + "/" + exportNodeName + "." + fileType

    #エクスポート
    if fileType == "ma":
        mc.file(exportFilePath, force=1, exportSelected=1, type="mayaAscii", options="v=0;", preserveReferences=1)
    elif fileType == "mb":
        mc.file(exportFilePath, force=1, exportSelected=1, type="mayaBinary", options="v=0;", preserveReferences=1)
    elif fileType == "fbx":
        mc.file(exportFilePath, force=1, exportSelected=1, type="FBX export", options="v=0;", preserveReferences=1)
    elif fileType == "obj":
        mc.file(exportFilePath, force=1, exportSelected=1, type="OBJexport", options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", preserveReferences=1)

    #エクスポート専用ノードを削除
    if pm.objExists(exportNode):
        pm.delete(exportNode)

    #一時リネームした既存ノードの名前を元に戻す
    if existingNode != None:
        existingNode.rename(exportNodeName)

    return


#-------------------------------------------------
#必要なプラグインをチェック
def checkPlugin():
    pluginNames = ["fbxmaya", "objExport"]

    pluginFolderPaths = pm.util.getEnv("MAYA_PLUG_IN_PATH").split(";")

    #{プラグイン名:パスのリスト}
    pluginName_paths = {}
    for pluginFolderPath in pluginFolderPaths:
        if os.path.isdir(pluginFolderPath):
            files = os.listdir(pluginFolderPath)
            for pluginName in pluginNames:
                if (pluginName + ".mll") in files:
                    if pluginName not in pluginName_paths:
                        pluginName_paths[pluginName] = []
                    pluginName_paths[pluginName].append(pluginFolderPath + "/" + pluginName + ".mll")

    for pluginName in pluginNames:
        if pluginName in pluginName_paths:
            if len(pluginName_paths[pluginName]) == 1:
                pluginPath = pluginName_paths[pluginName][0]

                #ロードされていない場合はロードする
                if mc.pluginInfo(pluginName, q=1, loaded=1) == 0:
                    pm.loadPlugin(pluginPath)
                if mc.pluginInfo(pluginName, q=1, autoload=1) == 0:
                    pm.pluginInfo(pluginPath, e=1, autoload=1)

    return


#-------------------------------------------------
if __name__ == "__main__":
    print("a")
    main("fbx")
