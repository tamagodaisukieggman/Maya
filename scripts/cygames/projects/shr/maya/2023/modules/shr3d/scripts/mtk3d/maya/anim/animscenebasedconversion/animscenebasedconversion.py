# -*- coding: utf-8 -*-
import maya.cmds as mc
import mtk3d.maya.rig.sceneBasedConversion.fbxExport as sbcf
import mtk3d.maya.rig.sceneBasedConversion.convert as sbcc

import os

animDirectoryBasePath = r"z:\mtk\work\resources\animations\clips"
wb = "workbench"
cnv = "convert"
ma = ".ma"
fbx = ".fbx"

#maを保存するためのフォルダ名
createFolderName = cnv

def directoryExistsCheck(workDirectory):

    worksceneDirectoryPath = workDirectory
    existsFlag = True

    #無い場合はあるところまでからフォルダを作成していく
    if not os.path.exists(worksceneDirectoryPath):
        os.makedirs(worksceneDirectoryPath)
        existsFlag = False

    return existsFlag

def execute():

    scenePath = mc.file(q=True,sn=True)
    exportDir = mc.fileDialog2(fileMode=3, dialogStyle=2, cap=u"FBXファイルの出力先を選択")[0] + "/"

    print(scenePath)
    print(exportDir)

    rigPath = repr(scenePath)
    fbxFile = os.path.basename(rigPath).split(".")[0] + fbx

    print(fbxFile)

    # export FBX path
    filePath = exportDir + fbxFile

    print(filePath)

    # workbench dir path
    wpath = os.path.dirname(scenePath) + "/" + wb + "/"

    # convert scene path
    convertScene = wpath + fbxFile.split("_")[1] + "_" + fbxFile.split("_")[2] + "_" + cnv + ma

    print(wpath)

    # name space
    nameSpace = fbxFile.split("_")[1] + "_" + fbxFile.split("_")[2] + "_000"
    print(nameSpace)

    # export path create if does not exist "createFolderName" directory.
    eDirPath = os.path.dirname(scenePath) +  "/" + wb + "/" + createFolderName + "/"
    flags = directoryExistsCheck(eDirPath)
    print(flags)

    savePath = eDirPath
    print(savePath)

    #FBX export command
    sbcf.main(scenePath,exportDir,nameSpace)

    #scene convert command
    sbcc.main(filePath, savePath, convertScene, nameSpace)

    #open current sceme
    mc.file(scenePath,open=True,force=True)
