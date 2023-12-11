# -*- coding: utf-8 -*-

u"""
Mayaスクリプトパスを追加

"""

from __future__ import unicode_literals

toolName = "CyAddMayaScriptPath"
__author__ = "Cygames, Inc. Yuta Kimura"

import maya.mel as mel

import sys
import os
import traceback

#-------------------------------------------------
#メイン
def add(targetFolderPath=""):
    #このファイルの情報を取得
    thisFilePath, thisFolderPath = getThisFileInfo()

    #ルートフォルダ
    rootFolderPath = ""
    if targetFolderPath == "":
        rootFolderPath = thisFolderPath
    else:
        rootFolderPath = targetFolderPath

    scriptRootFolderPath = rootFolderPath
    pluginRootFolderPath = rootFolderPath.replace("/scripts", "/plug-ins")

    #追加登録するフォルダのリストを取得
    addScriptFolderPaths = getAddPathList(scriptRootFolderPath, "_MAYA_SCRIPT_PATH.txt")
    addPluginFolderPaths = getAddPathList(pluginRootFolderPath, "_MAYA_PLUG_IN_PATH.txt")
    # ----- Wizard2用 -----
    wiz2_perforce = 'C:/cygames/wiz2'
    if os.path.exists(wiz2_perforce):
        wizard2ScriptFolderPaths = getAddPathList(wiz2_perforce, "_MAYA_SCRIPT_PATH.txt")
        if wizard2ScriptFolderPaths:
            addScriptFolderPaths.extend(wizard2ScriptFolderPaths)
    # ---------------------

    if len(addScriptFolderPaths) > 0:
        #現在のMayaパスリストを取得
        oldMayaScriptPaths = mel.eval('getenv MAYA_SCRIPT_PATH').split(";")
        oldMayaPythonPaths = sys.path

        #新Mayaパスリストを取得(再設定用)
        newMayaScriptPaths, newMayaScriptPathsStr = getNewPathList(oldMayaScriptPaths, addScriptFolderPaths, scriptRootFolderPath)
        newMayaPythonPaths, newMayaPythonPathsStr = getNewPathList(oldMayaPythonPaths, addScriptFolderPaths, scriptRootFolderPath)

        #Mayaパスを再設定
        mel.eval('putenv MAYA_SCRIPT_PATH "{}"'.format(newMayaScriptPathsStr))
        sys.path = newMayaPythonPaths

        print("     " + str(len(addScriptFolderPaths)))
        for currentPath in addScriptFolderPaths:
            print(u"    ・Scriptパス追加 : " + currentPath)

    if len(addPluginFolderPaths) > 0:
        #現在のMayaパス設定を取得
        oldMayaPluginPaths = mel.eval('getenv MAYA_PLUG_IN_PATH').split(";")

        #新Mayaパスリストを取得(再設定用)
        newMayaPluginPaths, newMayaPluginPathsStr = getNewPathList(oldMayaPluginPaths, addPluginFolderPaths, pluginRootFolderPath)

        #Mayaパスを再設定
        mel.eval('putenv MAYA_PLUG_IN_PATH "{}"'.format(newMayaPluginPathsStr))

        print("     " + str(len(addPluginFolderPaths)))
        for currentPath in addPluginFolderPaths:
            print(u"    ・Pluginパス追加 : " + currentPath)

    return


#-------------------------------------------------
#このファイルの情報を取得
def getThisFileInfo():
    #このファイルのパス
    thisFilePath = ""
    try:
        thisFilePath = __file__
    except NameError as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        thisFilePath = tb[0][0]
    thisFilePath = thisFilePath.replace("\\", "/")
    print("   " + thisFilePath)

    #このファイルがあるフォルダのパス
    thisFolderPath = os.path.dirname(thisFilePath)

    return thisFilePath, thisFolderPath


#-------------------------------------------------
#追加登録するフォルダのリストを取得
def getAddPathList(rootFolderPath, textFileName):
    addFolderPaths = []

    if os.path.isdir(rootFolderPath):
        addFolderPaths = [rootFolderPath]

        for root, folders, files in os.walk(rootFolderPath):
            for currentFolder in folders:
                currentFolderPath = os.path.join(root, currentFolder).replace("\\", "/")

                #フォルダ種類判別用のテキストファイルを含むフォルダのみ
                if os.path.isfile(currentFolderPath + "/" + textFileName):
                    addFolderPaths.append(currentFolderPath)

    return addFolderPaths


#-------------------------------------------------
#再設定用の新パスリストを取得
def getNewPathList(oldFolderPaths, addFolderPaths, rootFolderPath):
    newFolderPaths = []
    newFolderPathsStr = ""

    #既存パス
    for oldFolderPath in oldFolderPaths:
        if oldFolderPath not in newFolderPaths:
            #カスタムパスは除外
            if not oldFolderPath.startswith(rootFolderPath):
                newFolderPaths.append(oldFolderPath)
                if newFolderPathsStr != "":
                    newFolderPathsStr += ";"
                newFolderPathsStr += oldFolderPath

    #追加パス
    for addFolderPath in addFolderPaths:
        if addFolderPath not in newFolderPaths:
            newFolderPaths.append(addFolderPath)
            if newFolderPathsStr != "":
                newFolderPathsStr += ";"
            newFolderPathsStr += addFolderPath

    return newFolderPaths, newFolderPathsStr


#-------------------------------------------------
if __name__ == '__main__':
    add()
