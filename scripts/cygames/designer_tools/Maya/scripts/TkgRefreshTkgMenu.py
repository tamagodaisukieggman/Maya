# -*- coding: utf-8 -*-

u"""
designer_tools(Maya)を最新の状態にしてからTKG Toolsメニューを更新する

"""
from __future__ import print_function
from __future__ import absolute_import
try:
    # Maya 2022-
    from importlib import reload
except:
    pass

toolName = "TkgRefreshTkgMenu"
__author__ = "TKG,  Yuta Kimura"

import os
import maya.cmds as cmds


#-------------------------------------------------
#メイン
def refresh(batPauseFlg=0):
    dialogResult = cmds.confirmDialog(title=toolName, message=u"● TKG Toolsメニューの更新を実行しますか？", button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
    if dialogResult == "No":
        return False
    #designer_tools(Maya)を最新の状態にする
    batFilePath = "C:/tkgpublic/designer_tools/WindowsScriptHost/TkgSync/TkgSync_Maya.bat"
    command = batFilePath + " " + str(batPauseFlg)
    os.system(command)

    #このファイルのパス
    thisFilePath = __file__.replace("\\", "/")
    print(u"● " + thisFilePath)

    #Mayaスクリプトパスを追加
    try:
        import TkgAddMayaScriptPath
        reload(TkgAddMayaScriptPath)
    except:
        pass
    try:
        TkgAddMayaScriptPath.add(os.path.dirname(thisFilePath))
    except Exception as e:
        print(u"   Mayaスクリプトパスを追加 : 失敗！")
        print(str(e))

    #TKG Toolsメニューを更新
    try:
        import TkgMenu
        reload(TkgMenu)
    except:
        pass
    TkgMenu.UI()

    cmds.confirmDialog(title=toolName, message=u"● TKG Toolsメニューの更新が完了しました！")

    return True


#-------------------------------------------------
if __name__ == "__main__":
    refresh(0)
