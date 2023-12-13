# -*- coding: utf-8 -*-

"""
ブラウザでWebページを開く

"""

toolName = "CyOpenWebPage"
__author__ = "Cygames, Inc. Yuta Kimura"

import webbrowser

import maya.cmds as mc


#-------------------------------------------------
#メイン
def open(url):
    #エラー対策として変換した文字を元に戻す
    url = url.replace("~percent~", "%")

    #Webページを開く
#   webbrowser.open(url)
    mc.showHelp(url, absolute=1)

    return


#-------------------------------------------------
if __name__ == "__main__":
    pass
