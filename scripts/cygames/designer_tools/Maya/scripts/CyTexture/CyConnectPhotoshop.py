# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

"""
Photoshopとの通信用にポートを開く

"""

toolName = "CyConnectPhotoshop"
__author__ = "Cygames, Inc. Yuta Kimura"

import maya.cmds as mc


#-------------------------------------------------
#メイン
def open():
    #MayaコマンドポートをPhotoshop用に開く
    mc.commandPort(n=':30000',stp='python')

    return


#-------------------------------------------------
if __name__ == '__main__':
    open()
