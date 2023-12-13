# -*- coding: utf-8 -*-

"""
コンバイン

"""
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

toolName = "CyCombine"
__author__ = "Cygames, Inc. Yuta Kimura"

import maya.cmds as mc
import pymel.core as pm

import CyPivotTool
reload(CyPivotTool)


#-------------------------------------------------
#メイン
def combine(mainFlg=0, freezeFlg=0):
    if mainFlg == 1:
        print("")
        print("#-----")
        print("#[Python Command]")
        print("#import CyCombine;reload(CyCombine);CyCombine.combine()")
        print("#-----")
        print("")

    #選択中のノード
    selTransNodes = pm.ls(sl=1, transforms=1, flatten=1)

    selTransNodeNames = []
    parentNodes = []
    for currentNode in selTransNodes:
        selTransNodeNames.append(currentNode.longName())
        currentParentNode = currentNode.getParent()
        if currentParentNode != None:
            if currentParentNode not in parentNodes:
                parentNodes.append(currentParentNode)

    #選択ノードが全て同一の親の子である場合
    parentNode = None
    if len(parentNodes) == 1:
        parentNode = parentNodes[0]

    #コンバイン
    resultNodeNames = mc.polyUnite(selTransNodeNames, constructionHistory=0, mergeUVSets=1)
    combinedNode = pm.PyNode(resultNodeNames[0])

    #コンバイン後に残ったノードを削除
    for currentNodeName in selTransNodeNames:
        if pm.objExists(currentNodeName):
            pm.delete(currentNodeName)

    #親子付を復帰
    if parentNode != None:
        combinedNode.setParent(parentNode)

    return


#-------------------------------------------------
if __name__ == '__main__':
    combine()
