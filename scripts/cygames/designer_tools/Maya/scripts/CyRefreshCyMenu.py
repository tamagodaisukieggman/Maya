# -*- coding: utf-8 -*-

u"""
designer_tools(Maya)を最新の状態にしてからCygames Toolsメニューを更新する

"""
from __future__ import print_function
from __future__ import absolute_import
try:
    # Maya 2022-
    from importlib import reload
except:
    pass

toolName = "CyRefreshCyMenu"
__author__ = "Cygames, Inc. Yuta Kimura"

import os
import maya.cmds as cmds


#-------------------------------------------------
#メイン
def refresh(batPauseFlg=0):
    dialogResult = cmds.confirmDialog(title=toolName, message=u"● Cygames Toolsメニューの更新を実行しますか？", button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
    if dialogResult == "No":
        return False
    #designer_tools(Maya)を最新の状態にする
    batFilePath = "C:/cygames/designer_tools/WindowsScriptHost/CySync/CySync_Maya.bat"
    command = batFilePath + " " + str(batPauseFlg)
    os.system(command)

    #このファイルのパス
    thisFilePath = __file__.replace("\\", "/")
    print(u"● " + thisFilePath)

    #Mayaスクリプトパスを追加
    try:
        import CyAddMayaScriptPath
        reload(CyAddMayaScriptPath)
    except:
        pass
    try:
        CyAddMayaScriptPath.add(os.path.dirname(thisFilePath))
    except Exception as e:
        print(u"   Mayaスクリプトパスを追加 : 失敗！")
        print(str(e))

    #Cygames Toolsメニューを更新
    try:
        import CyMenu
        reload(CyMenu)
    except:
        pass
    CyMenu.UI()

    cmds.confirmDialog(title=toolName, message=u"● Cygames Toolsメニューの更新が完了しました！")

    return True


#-------------------------------------------------
if __name__ == "__main__":
    refresh(0)
