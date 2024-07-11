#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# TkgPrintMayaEnvValue.py
# Maya環境変数の値を出力

u"""
    BEGIN__CYGAMES_MENU
    label=TkgPrintMayaEnvValue: Maya環境変数の値を出力
    command=main()
    order=3000
    author=kimura_yuta
    version=1.0.0
    END__CYGAMES_MENU
"""

import sys
import pymel.core as pm

toolName = "TkgPrintMayaEnvValue"
__author__ = "TKG,  Yuta Kimura"


# -------------------------------------------------
# メイン
def main():
    # メインウィンドウオブジェクトの生成
    toolWindow = MainWindow()
    return


# -------------------------------------------------
# メインウィンドウクラス
class MainWindow(object):
    def __init__(self):
        # 既にウィンドウが開いている場合は閉じる
        if pm.window(toolName, q=1, exists=1):
            pm.deleteUI(toolName)

        # UIの定義
        self.window = pm.window(toolName, title=u"Maya環境変数", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            self.columnLayout_top = pm.columnLayout("columnLayout_top", columnOffset=("left", 5), rowSpacing=1)
            with self.columnLayout_top:
                self.separator_topSpace = pm.separator("separator_topSpace", w=1, h=5, style="none")

                mayaEnvKeys = []
                mayaEnvKeys.append("MAYA_APP_DIR")
                mayaEnvKeys.append("MAYA_LOCATION")
                mayaEnvKeys.append("MAYA_SCRIPT_PATH")
                mayaEnvKeys.append("MAYA_PLUG_IN_PATH")
                mayaEnvKeys.append("MAYA_UI_LANGUAGE")
                mayaEnvKeys.append("PYTHONPATH")
                mayaEnvKeys.append("sys.path")

                for currentCnt in range(len(mayaEnvKeys)):
                    currentLineIndex = str(currentCnt + 1)
                    self.__dict__["button_out_" + currentLineIndex] = \
                        pm.button("button_out_" + currentLineIndex, w=150, h=20,
                                  label=mayaEnvKeys[currentCnt],
                                  command=pm.Callback(printLog, mayaEnvKeys[currentCnt]))

        # ウィンドウのサイズ変更
        winWidthValue = 162
        winHeightValue = 187
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue = winHeightValue
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        # ウィンドウを開く
        pm.showWindow(self.window)

        return


# -------------------------------------------------
# Maya環境変数の値をスクリプトエディタのヒストリーに出力
def printLog(mayaEnvKey):
    if mayaEnvKey == "sys.path":
        mayaPythonPaths = sys.path

        print(u"【 " + mayaEnvKey + u" 】" + " " + str(len(mayaPythonPaths)))
        for currentPath in mayaPythonPaths:
            print(u"  ・" + currentPath)
    else:
        mayaEnvValues = pm.util.getEnv(mayaEnvKey).split(";")
        print(u"【 " + mayaEnvKey + u" 】" + " " + str(len(mayaEnvValues)))

        for currentValue in mayaEnvValues:
            print(u'  ・{}'.format(unicode(currentValue, u'shift-jis')))

    print("")

    return


# -------------------------------------------------
if __name__ == "__main__":
    main()
