# -*- coding: utf-8 -*-

import maya.cmds as mc
import mtk3d.maya.rig.sceneBasedConversion.fbxExport as afe
import mtk.utils.wrapper as wrapper
import os


def execute():

    scenePath = wrapper.getCurrentSceneFilePath() #scenePath = mc.file(q=True, sn=True)
    exportDir = mc.fileDialog2(fileMode=3, dialogStyle=2, cap=u"出力先を選択")[0] + "/"

    rPath = repr(scenePath)
    basePath = os.path.basename(rPath).split(".")[0]
    naming = basePath.split("_")
    second_name = basePath.split("_")[2]

    if (second_name == "m") or (second_name == "f"):
        nameSpace = "{}_{}_{}_{}".format(naming[1], naming[2], naming[3], "000")
        print("m or f")
        print(nameSpace)
    else:
        nameSpace = "{}_{}_{}".format(naming[1], naming[2], "000")
        print(nameSpace)

    print(scenePath)
    print(exportDir)
    print(nameSpace)

    afe.main(scenePath, exportDir, nameSpace)
    mc.file(scenePath, open=True, force=True)
