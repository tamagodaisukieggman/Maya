# -*- coding: cp932 -*-
#===============================================
#
# OS / システム 関連
#
# Fujita Yukihiro
#
#===============================================

import os
import subprocess

#===============================================
#
# バッチコマンドをウィンドウなしで実行
#
# @param      commandStr : コマンド
# @return
#
#===============================================
def execBatchCmd(commandStr):
    """ バッチコマンドをウィンドウ無しで実行 """

    # 引数が文字列じゃなければ終了
    if not isinstance(commandStr, str):
        return False

    # 一時ファイル
    tempBatFileName = os.path.join(os.getenv("TMP"), "fy_temp.bat")
    tempVbsFileName = os.path.join(os.getenv("TMP"), "fy_temp.vbs")

    # バッチファイル作成
    tempBatFile = open(tempBatFileName, "w")
    tempBatFile.write(commandStr)
    tempBatFile.close()

    # vbs ファイル作成（バッチ実行時にウィンドウを表示させない用に）
    tempVbsFile = open(tempVbsFileName, "w")
    tempVbsFile.write('CreateObject("WScript.Shell").Run "' + tempBatFileName + '",0')
    tempVbsFile.close()

    # vbs ファイル実行
    subprocess.call(tempVbsFileName, shell=True)

    return True
