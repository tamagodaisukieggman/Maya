# -*- coding: utf-8 -*-

"""
Windowsエクスプローラーを開く

"""

toolName = "CyOpenWinExplorer"
__author__ = "Cygames, Inc. Yuta Kimura"

import os

import pymel.core as pm


#-------------------------------------------------
#メイン
def open(mode, path):
    #対象のパス
    targetPath = ""
    if mode == "":
        targetPath = path
    else:
        if mode == "maya_setting":
            targetPath = pm.util.getEnv("MAYA_APP_DIR")
        elif mode == "maya_project":
            targetPath = pm.Workspace.getPath()
        elif mode == "maya_scene":
            targetPath = pm.system.sceneName()
    targetPath = targetPath.replace("/", "\\")

    if os.path.isfile(targetPath) or os.path.isdir(targetPath):
        #Windowsエクスプローラーを開く
        print("path : " + targetPath)
        if os.path.isdir(targetPath):
            os.popen('explorer "%s"' % targetPath)
        elif os.path.isfile(targetPath):
            os.popen('explorer /select,"%s"' % targetPath)
    else:
        messageStr = u"● 指定のパスが存在しません。"
        messageStr += "\n"
        messageStr += "   " + u"「" + targetPath + u"」"
        pm.confirmDialog(title=toolName, message=messageStr)

    return


#-------------------------------------------------
if __name__ == "__main__":
    pass
