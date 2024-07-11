# -*- coding: utf-8 -*-

"""
選択ポイント(Vertex・ControlVertex(CV)・EditPoint(EP))の名前リストを取得

"""

toolName = "getSelPointNames"
__author__ = "TKG,  Yuta Kimura"

import maya.cmds as mc
import pymel.core as pm


#-------------------------------------------------
#メイン
#    convFlg : ポイント以外のコンポーネントの場合にポイントに変換して取得するかどうか
def get(convFlg=0):
    selPointNames = []

    selItems = mc.ls(sl=1)

    #選択コンポーネント(CV・EP)を取得
    selNurbsComponentNames = mc.filterExpand(expand=1, selectionMask=(28,30), fullPath=1)
    if selNurbsComponentNames != None and len(selNurbsComponentNames) > 0:
        selPointNames.extend(selNurbsComponentNames)

    #選択コンポーネント(Vertex)を取得
    if convFlg == 0:
        selVertexNames = mc.filterExpand(expand=1, selectionMask=(31), fullPath=1)
        if selVertexNames != None and len(selVertexNames) > 0:
            selPointNames.extend(selVertexNames)
    elif convFlg == 1:
        selPolyComponentNames = mc.filterExpand(expand=1, selectionMask=(31,32,34,35,70), fullPath=1)
        if selPolyComponentNames != None and len(selPolyComponentNames) > 0:
            #選択コンポーネントを頂点に変換
            pm.runtime.ConvertSelectionToVertices()
            selVertexNames = mc.filterExpand(expand=1, selectionMask=(31), fullPath=1)
            if selVertexNames != None and len(selVertexNames) > 0:
                selPointNames.extend(selVertexNames)

            #選択状態を元に戻す
            mc.select(selItems)

    if len(selPointNames) > 0:
        selPointNames.sort()

    return selPointNames


#-------------------------------------------------
if __name__ == "__main__":
    pass
