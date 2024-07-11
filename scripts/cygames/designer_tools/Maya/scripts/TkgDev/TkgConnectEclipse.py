# -*- coding: utf-8 -*-

"""
Mayaのスクリプト開発にEclipseを使用するための接続設定

"""

toolName = "TkgConnectEclipse"
__author__ = "TKG,  Yuta Kimura"

import maya.cmds as mc

#-------------------------------------------------
#メイン
def main():
    #このファイルのパス
    thisFilePath = ""
    try:
        thisFilePath = __file__
    except NameError, e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        thisFilePath = tb[0][0]
    thisFilePath = thisFilePath.replace("\\", "/")
    print("・" + thisFilePath)

    #MayaコマンドポートをEclipse用に開く
    if mc.commandPort(':7720', q=True) !=1:
        try:
            mc.commandPort(n=':7720', eo = False, nr = True)
            print("  Eclipseに接続成功！")
        except:
            print("  Eclipseに接続失敗！")

    return


#-------------------------------------------------
if __name__ == '__main__':
    main()
