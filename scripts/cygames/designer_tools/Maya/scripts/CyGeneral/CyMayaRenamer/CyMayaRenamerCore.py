# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-
try:
    # Maya 2015-2016
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    # Maya 2017-
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

import os
import re
import sys
import tempfile
import csv

g_supportedTextureTypes = [".png", ".jpg", ".jpeg", ".tga", ".psd", ".tif", ".tiff"]
g_invalidChars = ['\\', '/', ':', '*', '"', '<', '>', '|']
g_doWriteLog = True
g_logFile = None # ログファイル書き出し用。

def writeLog(msg):
    u"""
    ログファイルに文字列を書き込みます。　UTF-8対応。 g_logFileがあることが前提です。
    :param msg:　string. ファイルに書き込む文字列。
    """
    if g_doWriteLog == False:
        return
    if g_logFile:
        if sys.version_info.major == 2:
            g_logFile.write(msg.encode("utf-8_sig") + "\n")
        else:
            # Python3より上とみなす
            g_logFile.write(msg + "\n")
    else:
        print("Warning: In writeLog. g_logFile is not defined. Message was not written to a file.")


def getScenesToProcess(rootPath, isTopdown=False, mayaAscii=True, mayaBinary=True, ignore=""):
    u"""
    rootPath配下のMayaシーンを取得。
    :param rootPath: string. Mayaシーンを検索するルートフォルダ。
    :param isTopdown: bool. 検索方向
    :param mayaAscii: bool. Trueなら「.ma」ファイルを検索する。
    :param mayaBinary: bool. Trueなら「.mb」ファイルを検索する。
    :param ignore: 対象から外すキーワード (例：old)
    :return: string[]. Mayaシーンファイルのフルパスの配列。
    """
    scenesToProcess = []
    try:
        for root, dirs, files in os.walk(rootPath, topdown=isTopdown):
            dirs[:] = [d for d in dirs if d not in ignore]
            rootFolder = os.path.basename(root)
            if rootFolder == ignore:
                print(u"無視しました: " + root)
                continue
            else:
                for fileName in files:
                    if fileName.endswith(".ma"):
                        if mayaAscii == False:
                            print(u"無視しました: " + os.path.join(root, fileName))
                        else:
                            scenesToProcess.append(os.path.join(root, fileName))
                    elif fileName.endswith(".mb"):
                        if mayaBinary == False:
                            print(u"無視しました: " + os.path.join(root, fileName))
                        else:
                            scenesToProcess.append(os.path.join(root, fileName))
    except Exception as e:
        cmds.error(str(e))
    return scenesToProcess


def getCurrentProjectDir():
    u"""
    現在Mayaで開いているシーンのプロジェクトフォルダへのパスを返します。
    :return: string. Path to the current Maya scene project.
    """
    import maya.cmds as cmds
    projPath = ""
    try:
        scenePath = cmds.file(q=True, sn=True)
        scenePath = os.path.join(scenePath, os.pardir)
        if not scenePath:
            print(u"シーンパスの取得に失敗しました")
        else:
            if os.path.basename(scenePath) != "scenes":
                projPath = os.path.abspath(os.path.join(scenePath, os.pardir))
            else:
                print(u"Error: 現在のシーンはscenesフォルダに入っていません。")
    except Exception as e:
        print(str(e))
    return projPath

def replaceDirPath(fullPathBefore, fromTxt, toTxt, bRegex):
    u"""
    検索文字列がない場合、変更なしのfullPathBeforeを返します。
    マテリアルのパスをじかに変更する場合に使います。
    :param fullPathBefore: リネームの対象となるパス
    :param rootDir: このディレクトリ配下のフォルダ名だけ変更します。
    :param fromTxt: 検索する文字列
    :param toTxt: 置き換える文字列
    :return: string. リネーム後のフルパスを返します。
    """
    fullPathBefore = os.path.normpath(fullPathBefore)
    if fullPathBefore.startswith(os.path.sep):
        fullPathBefore = fullPathBefore[1:]

    folders = fullPathBefore.split(os.path.sep) # フォルダ単位でリネーム
    fullPathAfter = ""
    for folder in folders[:-1]: # ファイル名以外の所をリネーム
        if bRegex:
            newFolderName = re.sub(fromTxt, toTxt, folder)
        else:
            newFolderName = folder.replace(fromTxt, toTxt)
        if not newFolderName: # もしリネームで空になってしまったら元に戻す
            newFolderName = folder
            print(u"Error: パス中のフォルダ名を空にはできません：" + folder)
            writeLog(u"Error: パス中のフォルダ名を空にはできません：" + folder)
        if fullPathAfter:
            fullPathAfter = os.path.join(fullPathAfter, newFolderName)
        else:
            # 重要：os.path.join("C:", "a") が C:\a にならずC:a になってしまうので敢えて\を追加
            fullPathAfter = newFolderName + os.path.sep
    fileName = folders[-1] # ファイル名
    fullPathAfter = os.path.join(fullPathAfter, fileName)
    return fullPathAfter

def replaceFileName(fullPathBefore, fromTxt, toTxt, bRegex):
    u"""
    パスのファイル名の部分を置き換えます
    :param fullPathBefore: ファイル名を含むフルパス（リネームの対象）
    :param fromTxt: ファイル名の部分で検索する文字列
    :param toTxt: ファイル名の部分で置き換える文字列
    :return: string. ファイル名の部分を置き換えたフルパスを返します。
    """
    fullPathBefore = os.path.normpath(fullPathBefore)
    dirPath = os.path.dirname(fullPathBefore)
    fileName = os.path.basename(fullPathBefore)
    fileNameOnly, fileExtension = os.path.splitext(fileName)
    if bRegex:
        newFileName = re.sub(fromTxt, toTxt, fileNameOnly)
    else:
        newFileName = fileNameOnly.replace(fromTxt, toTxt)
    if not newFileName:
        newFileName = fileNameOnly
    fullPathAfter = os.path.join(dirPath, newFileName) + fileExtension
    return fullPathAfter

def renameMaterials(fromTxt, toTxt, bRegex, bDryRun=False):
    u"""
    シーン内のマテリアルをリネームします。
    :param fromTxt: string. 検索文字列。
    :param toTxt: string. リネーム文字列。
    """
    import maya.cmds as cmds
    materials = cmds.ls(mat=True)
    for mat in materials:
        if mat == "lambert1" or mat == "particleCloud1":
            continue
        if bRegex:
            matNameAfter = re.sub(fromTxt, toTxt, mat)
        else:
            matNameAfter = mat.replace(fromTxt, toTxt)

        if not matNameAfter:
            matNameAfter = mat
        try:
            if mat != matNameAfter:
                if cmds.objExists(mat):
                    writeLog(u"マテリアル名," + mat + "," + matNameAfter + "," + cmds.file(query=True, sn=True))
                    if not bDryRun:
                        cmds.rename(mat, matNameAfter)
        except:
            writeLog("Could not rename " + mat)

def readBeforeAfterCSV(csvpath):
    u"""
    リネームの変更前、変更後のcsvを読み込み、ディクショナリとして返します。
    :param csvpath: string. csvファイルのパス。
    :return: {}. 変換前と変換後のテキストのディクショナリ
    """
    beforeAfterDict = {}
    with open(csvpath, 'r') as f:
        reader = csv.reader(f)
        for beforeAfter in reader:
            if len(beforeAfter) != 2:
                return
            fromText = beforeAfter[0].strip()
            toText = beforeAfter[1].strip()
            beforeAfterDict[fromText] = toText
        f.close()
    return beforeAfterDict

def renameFoldersInDir(rootDirPath, fromTxt, toTxt, bRegex, ignore="", bDryRun=False):
    u"""
    指定したルートフォルダ（rootDirPath）配下のフォルダをリネームします。
    :param rootDirPath: このフォルダ配下のフォルダをリネームします。
    :param fromTxt: string. 検索文字列。
    :param toTxt: string. リネーム文字列。
    :param bRegex: Trueならリネームを正規表現で行う。
    :param isDryRun: Trueだと実際にリネームをせずwriteLog関数でglobalのログファイルに変更内容を書きこむ。テスト用。
    :return rootDirPath. リネームされていたらリネーム後のrootDirPath.
    """
    rootDirPath = os.path.normpath(rootDirPath)
    try:
        if bRegex:
            rootDirAfter = re.sub(fromTxt, toTxt, rootDirPath)
        else:
            rootDirAfter = rootDirPath.replace(fromTxt, toTxt)
    except Exception as e:
        print(u"Error: フォルダのリネームに失敗しました。　"
              u"「検索する文字列」や「リネーム後の文字列」に問題があるかもしれません。")
        raise e

    if rootDirPath != rootDirAfter:
        try:
            rootFolder = os.path.basename(rootDirPath)
            if rootFolder == ignore:
                print(u"無視しました: " + rootDirPath)
                return
            if rootDirPath != rootDirAfter:
                if not bDryRun:
                    os.rename(rootDirPath, rootDirAfter)
                writeLog(u"フォルダ名," + rootDirPath + "," + rootDirAfter)

            rootDirPath = rootDirAfter
        except Exception as e:
            print("Error @ renameFoldersInDir: " + str(e))

    # ルートフォルダ配下のフォルダ
    for root, dirs, files in os.walk(rootDirPath, topdown=False):
        rootFolder = os.path.basename(root)
        if rootFolder == ignore:
            print(u"無視しました: " + root)
            continue
        for dirName in dirs:
            fullPathBefore = os.path.join(root, dirName)
            if bRegex:
                newDirName = re.sub(fromTxt, toTxt, dirName)
            else:
                newDirName = dirName.replace(fromTxt, toTxt) # Memo: Do not change above root!!! That's not what user intended.
            if not newDirName:
                newDirName = dirName
                writeLog(u"空の名前にはリネームできません：" + dirName)
            fullPathAfter = os.path.join(root, newDirName)
            # /と￥を揃える
            fullPathBefore = os.path.normpath(fullPathBefore)
            fullPathAfter = os.path.normpath(fullPathAfter)
            if fullPathBefore != fullPathAfter:
                if os.path.exists(fullPathBefore):
                    if not os.path.exists(fullPathAfter):
                        try:
                            if not bDryRun:
                                os.rename(fullPathBefore, fullPathAfter)
                            writeLog(u"フォルダ名," + fullPathBefore + "," + fullPathAfter)
                        except Exception as e:
                            writeLog(u"フォルダリネーム失敗: " + fullPathBefore + ". " + str(e))
                    else:
                        writeLog(fullPathAfter + u" は既に存在しています。　フォルダはリネームしませんでした。")
                else:
                    writeLog(fullPathBefore + u" は存在しません。")
    return rootDirAfter

def renameFilesInDirByExtension(rootDirPath, fromTxt, toTxt, bRegex, extensions, ignore="", isDryRun=False):
    u"""
    指定したrootディレクトリ配下の指定の拡張子を持ったファイルをリネームする。
    :param rootDirPath: rootディレクトリ
    :param fromTxt: 検索する文字列
    :param toTxt: 置き換える文字列
    :param extensions: ファイル拡張子の配列 (小文字! Must be all lower case!) Ex. .png
    :param isDryRun: Trueだと実際にリネームをせずwriteLog関数でglobalのログファイルに変更内容を書きこむ。テスト用。
    """
    for root, dirs, files in os.walk(rootDirPath, topdown=False):
        rootFolder = os.path.basename(root)
        if rootFolder == ignore:
            print(u"無視しました: " + root)
            continue
        for fileName in files:
            fileNameOnly, fileExtension = os.path.splitext(fileName)
            fileExtensionLower = fileExtension.lower() # 比較の時だけ拡張子を全部小文字にする
            if fileExtensionLower in [x.lower() for x in extensions]:
                fullPathBefore = os.path.join(root, fileName)
                if bRegex:
                    newFileName = re.sub(fromTxt, toTxt, fileNameOnly)
                else:
                    newFileName = fileNameOnly.replace(fromTxt, toTxt)
                if not newFileName:
                    newFileName = fileNameOnly
                    writeLog(u"空の名前にはリネームできません：" + fileNameOnly)
                fullPathAfter = os.path.join(root, newFileName) + fileExtension
                # /と￥を揃える
                fullPathBefore = os.path.normpath(fullPathBefore)
                fullPathAfter = os.path.normpath(fullPathAfter)
                if fullPathBefore != fullPathAfter:
                    if os.path.exists(fullPathBefore):
                        if os.path.exists(fullPathAfter) == False:
                            if not isDryRun:
                                os.rename(fullPathBefore, fullPathAfter)
                            writeLog(u"ファイル名," + fullPathBefore + "," + fullPathAfter)
                        else:
                            writeLog(u"Warning: " + fullPathAfter + u" は既に存在しています。既存のファイルには上書きしませんでした。")
                    else:
                        writeLog(u"Error: " + fullPathBefore + u" は存在しません。")

def renameFolderNamesInMaterials(fromTxt, toTxt, bRegex, bDryRun=False):
    u"""
    シーン内のマテリアルのテクスチャーパス内のフォルダ名をリネームします。
    :param fromTxt: string. 検索文字列。
    :param toTxt: string. リネーム文字列。
    """
    import maya.cmds as cmds
    materials = cmds.ls(mat=True)
    for mat in materials:
        matInfo = cmds.listConnections(mat, type='materialInfo')
        if matInfo:
            fileNodes = cmds.listConnections(matInfo, type='file')
            if fileNodes:
                for fileNode in fileNodes:
                    fullPathBefore = os.path.normpath(cmds.getAttr(fileNode + ".ftn", asString=True))
                    fullPathAfter = os.path.normpath(replaceDirPath(fullPathBefore, fromTxt, toTxt, bRegex))
                    if fullPathBefore != fullPathAfter:
                        writeLog(u"マテリアルのテクスチャーパス内のフォルダ名," + fullPathBefore + "," + fullPathAfter +
                                     "," + cmds.file(query=True, sn=True))
                        if not bDryRun:
                            cmds.setAttr(fileNode + ".ftn", fullPathAfter, type="string")


def renameTextureNamesInMaterials(fromTxt, toTxt, bRegex, isDryRun=False):
    u"""
    シーン内のマテリアルのテクスチャーパス内のテクスチャーファイル名をリネームします。
    :param fromTxt: string. 検索文字列。
    :param toTxt: string. リネーム文字列。
    """
    import maya.cmds as cmds
    materials = cmds.ls(mat=True)
    for mat in materials:
        matInfo = cmds.listConnections(mat, type='materialInfo')
        if matInfo:
            fileNodes = cmds.listConnections(matInfo, type='file')
            if fileNodes:
                for fileNode in fileNodes:
                    fullPathBefore = os.path.normpath(cmds.getAttr(fileNode + ".ftn", asString=True))
                    fullPathAfter = replaceFileName(fullPathBefore, fromTxt, toTxt, bRegex)
                    if fullPathBefore != fullPathAfter:
                        writeLog(u"マテリアルのテクスチャーパス内のファイル名," + fullPathBefore + "," + fullPathAfter +
                                     "," + cmds.file(query=True, sn=True))
                        if not isDryRun:
                            cmds.setAttr(fileNode + ".ftn", fullPathAfter, type="string")


def renameWithTransform(node, fromTxt, toTxt, bRegex, bDryRun=False):
    u"""
    NodeとtransformがセットになっているMayaオブジェクトのリネーム。
    :param node: mesh, locatorなどのMaya node.
    :param fromTxt: string. 検索する文字列
    :param toTxt: string. リネームする文字列
    :param bRegex: bool. Trueならリネームを正規表現でする
    :param isDryRun: bool. Trueだと実際にリネームをせずwriteLog関数でglobalのログファイルに変更内容を書きこむ。テスト用。
    """
    import maya.cmds as cmds
    try:
        if str(cmds.objectType(node)) != "objectSet":
            transforms = cmds.listRelatives(node, type='transform', p=True, fullPath=True)
            if transforms:
                for trans in transforms:
                    renameNode(trans, fromTxt, toTxt, bRegex, bDryRun)
    except Exception as e:
        writeLog(u"リネームできませんでした： " + node + ": type: " + str(cmds.objectType(node)) + ", " + str(e))

def renameNode(node, fromTxt, toTxt, bRegex, bDryRun=False):
    import maya.cmds as cmds
    try:
        if node.rfind("|") != -1:
            dirPath = node[0:node.rfind("|")]
            shortName = node.split("|")[-1] # fullPath対応
        else:
            dirPath = ""
            shortName = node
        if bRegex:
            newName = re.sub(fromTxt, toTxt, shortName)
        else:
            newName = shortName.replace(fromTxt, toTxt)
        if shortName != newName:
            nodeType = cmds.objectType(node)
            writeLog(nodeType + "," + node + "," + (dirPath + "|" + newName) + "," + cmds.file(query=True, sn=True))
            if not bDryRun:
                cmds.rename(node, newName)  # nodeのtransformのリネームをするとnodeのShapeもリネームされる
    except Exception as e:
        writeLog(u"リネームできませんでした： " + node + ": type: " + str(cmds.objectType(node)) + ". " + str(e))

def renameReferencePathFolderPath(fromText, toText, bRegex, bDryRun=False):
    import maya.cmds as cmds
    scenePath = cmds.file(q=True, sn=True)
    refs = cmds.file(q=True, reference=True)
    for pth in refs:
        fullPathBefore = os.path.normpath(pth)
        fullPathAfter = replaceDirPath(fullPathBefore, fromText, toText, bRegex)
        refName = cmds.referenceQuery(fullPathBefore, rfn=True)
        if fullPathBefore != fullPathAfter:
            if cmds.file(fullPathAfter, q=True, ex=True):  # ファイルがないとリファレンスパスの置き換えができない。
                writeLog(u"リファレンスパスのフォルダ名部分," + fullPathBefore + "," + fullPathAfter + "," + scenePath + u" の " + pth)
                if not bDryRun:
                    # リファレンス ノードが存在しない場合、lrコマンドは失敗します
                    cmds.file(fullPathAfter, lr=refName)
            else:
                writeLog(u"ファイルがないのでリファレンスパスの置き換えができませんでした," + fullPathBefore + "," +
                         fullPathAfter + "," + scenePath + u" の " + pth)

def renameReferencePathFileName(fromText, toText, bRegex, bDryRun=False):
    import maya.cmds as cmds
    scenePath = cmds.file(q=True, sn=True)
    refs = cmds.file(q=True, reference=True)
    for pth in refs:
        fullPathBefore = os.path.normpath(pth)
        fullPathAfter = replaceFileName(fullPathBefore, fromText, toText, bRegex)
        refName = cmds.referenceQuery(fullPathBefore, rfn=True)
        if fullPathBefore != fullPathAfter:
            if cmds.file(fullPathAfter, q=True, ex=True):  # ファイルがないとリファレンスパスの置き換えができない。
                writeLog(u"リファレンスパスのファイル名部分," + fullPathBefore + "," + fullPathAfter + "," +
                             scenePath + u" の " + pth)
                if not bDryRun:
                    cmds.file(fullPathAfter, lr=refName)
            else:
                writeLog(u"ファイルがないのでリファレンスパスの置き換えができませんでした," + fullPathBefore + "," +
                         fullPathAfter + "," + scenePath + u" の " + pth)

def isGroup(node):
    u"""
    nodeがグループかどうか判定します。
    transformノードで、Shapeがなくて、childrenがあるものをグループとみなしています。
    :param node: Maya node.
    :return: boolean. True if node is a group object.
    """
    import maya.cmds as cmds
    itemType = cmds.objectType(node)
    if itemType == "transform":
        shapes = cmds.listRelatives(node, shapes=True)
        if shapes is None:
            children = cmds.listRelatives(node, children=True)
            if children and len(children) > 0:
                return True
    return False


# このツールの利用上の注意点のダイアログ。
# ユーザーがリスクなどに対して了解したらTrueを返す。
def didUserAcceptDisclaimer():
    # このツールを使う注意点のダイアログを表示
    msgBox = QMessageBox()
    msgBox.setWindowTitle(u"重要")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(u"このツールはファイルやフォルダ、Mayaのシーン内のオブジェクトのリネームをするツールです。")
    msgBox.setInformativeText(u"Undoできませんので、複製を作ってから実行してください。")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Cancel)
    ret = msgBox.exec_()
    if ret == QMessageBox.Cancel:
        return False
    else:
        return True

def checkFoldersAndFilesReadOnly(rootPath):
    u"""
    rootPath配下のフォルダとファイルが「読み取り専用」になっていないか確認（保存できないので）
    :param rootPath:
    :return: 読み取り専用でなければTrue
    """
    bResult = True
    readOnlyList = []
    for root, dirs, files in os.walk(rootPath, topdown=False):
        for dir in dirs:
            if os.access(os.path.join(root, dir), os.W_OK) == False:
                bResult = False
                readOnlyList.append(os.path.join(root, dir))
                print(u"フォルダが読み取り専用です: " + os.path.join(root, dir))
        for afile in files:
            if os.access(os.path.join(root, afile), os.W_OK) == False:
                bResult = False
                readOnlyList.append(os.path.join(root, afile))
                print(u"ファイルが読み取り専用です: " + os.path.join(root, afile))
    return bResult

def renameFilesAndFolders(folderPath, doFolder, doTexture, doMayaAscii, doMayaBinary, fromText, toText, isRegex, ignore="", isDryRun=False):
    u"""
    ファイルとフォルダをリネームします。
    ファイルの中身まではリネームしないのでOuterFileと言っています。
    :param folderPath:
    :param doFolder:
    :param doTexture:
    :param doMayaAscii:
    :param doMayaBinary:
    :param fromText:
    :param toText:
    :param isRegex:
    :param isDryRun: Trueだと実際にリネームをせずwriteLog関数でglobalのログファイルに変更内容を書きこむ。テスト用。
    :return:
    """
    # フォルダをリネーム
    if doFolder:
        folderPath = renameFoldersInDir(folderPath, fromText, toText, isRegex, ignore, isDryRun)
    # 対象ファイル
    fileExtensions = []
    if doTexture:
        fileExtensions = g_supportedTextureTypes
    if doMayaAscii:
        fileExtensions.append(".ma")
    if doMayaBinary:
        fileExtensions.append(".mb")
    # ファイルをリネーム
    renameFilesInDirByExtension(folderPath, fromText, toText, isRegex, fileExtensions, ignore, isDryRun)
    return folderPath


def renameCurrentScene(fromText, toText, bRegex, bMatFolderPath, bMatTextureName,
                       bMatName, bLocator, bMesh, bJoint, bGroup, bRefPathFolder, bRefPathFile, bDryRun=False):
    u"""
    現在開いているシーン内のリネームをする。
    :param fromText: string. 検索文字列。
    :param toText: string. リネームする文字列。
    :param bRegex: boolean. 検索する文字列が正規表現かどうか。
    :param bMatFolderPath: boolean. マテリアルのテクスチャーパスのフォルダ名をリネームするかどうか。
    :param bMatTextureName: boolean. マテリアルのテクスチャーパスのテクスチャーファイル名をリネームするかどうか。
    :param bMatName: boolean. マテリアル名をリネームするかどうか。
    :param bLocator: boolean. ジョイントをリネームするかどうか。
    :param bMesh: boolean. メッシュをリネームするかどうか。
    :param bJoint: boolean. ジョイントをリネームするかどうか。
    :param bGroup: boolean. グループをリネームするかどうか。
    :param bRefPathFolder. リファレンスパスのフォルダ名部分をリネームするかどうか。 リネーム後のパスが存在していないと変えられない。
    :param bRefPathFile. リファレンスパスのファイル名部分をリネームするかどうか。 リネーム後のパスが存在していないと変えられない。
    :param bDryRun. Trueだと実際にリネームをせずwriteLog関数でglobalのログファイルに変更内容を書きこむ。テスト用。
    """
    import maya.cmds as cmds

    # マテリアルのテクスチャーのフォルダパス部分リネーム
    if bMatFolderPath:
        renameFolderNamesInMaterials(fromText, toText, bRegex, bDryRun)
    # マテリアルのテクスチャーのファイル名部分リネーム
    if bMatTextureName:
        renameTextureNamesInMaterials(fromText, toText, bRegex, bDryRun)

    # マテリアルをリネーム
    if bMatName:
        renameMaterials(fromText, toText, bRegex, bDryRun)

    # その他のノードのリネーム
    cmds.select(all=True) # シーン内のオブジェクトすべてリスト
    allObjInScene = cmds.ls(sl=True, long=True)
    if allObjInScene != None:
        allRels = cmds.listRelatives(allObjInScene, ad=True, fullPath=True)
        if allRels != None:
            allObjInScene = allRels + allObjInScene

    # シーン内のオブジェクトがチェックボックスのタイプとマッチしたらリネーム
    for item in allObjInScene:
        try:
            cmds.select(item, replace=True)
        except Exception as e:
            # mesh等、transformと一緒にリネームしてしまうと見つからないtransformがあるけどスルー
            continue
        itemObj = cmds.ls(sl=True)
        if itemObj:
            itemObj = itemObj[0]
            itemType = cmds.objectType(itemObj)
        else:
            continue
        # ロケーターをリネーム
        if itemType == "locator" and bLocator:
            renameWithTransform(item, fromText, toText, bRegex, bDryRun)

        # メッシュをリネーム
        elif itemType == "mesh" and bMesh:
            renameWithTransform(item, fromText, toText, bRegex, bDryRun)

        # ジョイントをリネーム
        elif itemType == "joint" and bJoint:
            renameNode(item, fromText, toText, bRegex, bDryRun)

        # グループをリネーム
        elif bGroup:
            if isGroup(itemObj):
                renameNode(item, fromText, toText, bRegex, bDryRun)

    # リファレンスをリネーム(フォルダ名の部分)
    if bRefPathFolder:
        renameReferencePathFolderPath(fromText, toText, bRegex, bDryRun)

    # リファレンスをリネーム(ファイル名の部分)
    if bRefPathFile:
        renameReferencePathFileName(fromText, toText, bRegex, bDryRun)
