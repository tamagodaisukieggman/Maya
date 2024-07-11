# -*- coding: utf-8 -*-

"""
移動・回転・スケール値のマッチング

"""
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

import pymel.core as pm

toolName = "TkgMatchTransform"
__author__ = "TKG,  Yuta Kimura"


#-------------------------------------------------
#メイン
def match(mode, mainFlg=0):
    if mainFlg == 1:
        print("")
        print("#-----")
        print("#[Python Command]")
        print("#import TkgMatchTransform;reload(TkgMatchTransform);TkgMatchTransform.match('" + mode + "')")
        print("#-----")
        print("")

    #選択中のノード
    selNodes = pm.ls(sl=1)

    if len(selNodes) < 2:
        pm.confirmDialog(title=toolName, message=u"● 2つ以上のノードを選択してから実行して下さい。")

    for currentCnt in range(len(selNodes)):
        if currentCnt > 0:
            if mode == "all":
                pm.delete(pm.parentConstraint(selNodes[0], selNodes[currentCnt]))
                pm.delete(pm.scaleConstraint(selNodes[0], selNodes[currentCnt]))
            elif mode == "translate":
                pm.delete(pm.pointConstraint(selNodes[0], selNodes[currentCnt]))
            elif mode == "rotate":
                pm.delete(pm.orientConstraint(selNodes[0], selNodes[currentCnt]))
            elif mode == "scale":
                pm.delete(pm.scaleConstraint(selNodes[0], selNodes[currentCnt]))

    return


#-------------------------------------------------
if __name__ == '__main__':
    match("all")
