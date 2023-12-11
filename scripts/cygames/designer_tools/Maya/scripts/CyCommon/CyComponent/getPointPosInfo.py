# -*- coding: utf-8 -*-

"""
ポイント(Vertex・ControlVertex(CV)・EditPoint(EP))の位置情報を取得

"""

toolName = "getPointPosInfo"
__author__ = "Cygames, Inc. Yuta Kimura"

import maya.cmds as mc


#-------------------------------------------------
#メイン
#    pointNames : 座標を取得するポイント名のリスト
#    space : 取得する座標の空間
#    flatFlg : 座標リストを作成する際に、モデルごとに分けるかどうか
def get(pointNames, space, flatFlg):
    pointPosInfo = {}
    model_pointPosList = {}

    wsValue = 0
    lsValue = 0
    if space == "world":
        wsValue = 1
    elif space == "local":
        lsValue = 1
    elif space == "object":
        lsValue = 1

    for currentPointName in pointNames:
        currentModelName = ""
        if flatFlg ==0:
            currentModelName = "all"
        elif flatFlg ==1:
            currentModelName = currentPointName.split(".")[0]

        if not currentModelName in model_pointPosList:
            model_pointPosList[currentModelName] = {}
            model_pointPosList[currentModelName]["pointPosXList"] = []
            model_pointPosList[currentModelName]["pointPosYList"] = []
            model_pointPosList[currentModelName]["pointPosZList"] = []

        #ワールド座標を取得
        currentWorldPos = mc.pointPosition(currentPointName, world=wsValue, local=lsValue)
        model_pointPosList[currentModelName]["pointPosXList"].append(currentWorldPos[0])
        model_pointPosList[currentModelName]["pointPosYList"].append(currentWorldPos[1])
        model_pointPosList[currentModelName]["pointPosZList"].append(currentWorldPos[2])

    pointPosInfo["model_pointPosList"] = model_pointPosList

    return pointPosInfo


#-------------------------------------------------
if __name__ == "__main__":
    pass
