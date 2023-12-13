# -*- coding: cp932 -*-
#===============================================
#
# ユーティリティ
#
# Fujita Yukihiro
#
#===============================================

import os
import time
import mtk3d.maya.env.os.functions as envos

#===============================================
#
# テキスト クリップボート
#
# @param      method : set,get
# @param      txt : クリップボードに渡す文字列
# @return     クリップボードの文字列
#
#===============================================
def textClipboard(method, txt=""):
    """ テキストをクリップボードにコピー、クリップボードから取得 """

    # コピーかつtxt 引数が文字列じゃなければ終了
    if method == "set" and not isinstance(txt, (str, unicode)):
        return False

    elif method != "set" and method != "get":
        return False

    # 一時ファイル
    tempFileName = os.path.join(os.getenv("TMP"), "fy_tempClipboard.txt") 
    
    # クリップボードにコピーの場合、一時ファイルに書き込み
    if method == "set":
        tempFile = open(tempFileName, "w")
        tempFile.write(txt)
        tempFile.close()
    
        # 一時ファイルの内容をクリップボードにコピーするコマンド
        batCmd = "clip < " + tempFileName

    elif method == "get":
        # クリップボードの内容を一時ファイルに書き出すコマンド
        batCmd = 'mshta.exe "vbscript:Execute("str=window.clipboardData.getData(""text""):CreateObject(""Scripting.FileSystemObject"").GetStandardStream(1).Write(str^&""""):close")" > ' + tempFileName

    else:
        return False
        
    # バッチコマンド実行
    envos.execBatchCmd(batCmd)

    # クリップボードから取得の場合
    if method == "get":
        #ウェイト
        time.sleep(0.3)
        
        # 一時ファイルから読み込み
        tempFile = open(tempFileName, "r")
        txt = tempFile.read()
        tempFile.close()
    
        return txt
    else:
        return True
