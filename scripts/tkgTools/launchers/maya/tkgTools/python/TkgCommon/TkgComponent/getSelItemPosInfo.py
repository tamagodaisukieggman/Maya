# -*- coding: utf-8 -*-

"""
選択アイテムの位置情報を取得

"""
from __future__ import division

try:
    # Maya 2022-
    from past.utils import old_div
    from importlib import reload
except Exception:
    pass

import sys

import pymel.core as pm

import TkgComponent.getSelPointNames as getSelPointNames
import TkgComponent.getPointPosInfo as getPointPosInfo

reload(getSelPointNames)
reload(getPointPosInfo)

toolName = "getSelItemPosInfo"
__author__ = "TKG,  Yuta Kimura"

#-------------------------------------------------
#選択アイテム全体の座標を取得
def get(spaceValue="world"):
    selItemPosInfo = {}
    selItemPosInfo["cenPos"] = [0, 0, 0]
    selItemPosInfo["maxPos"] = [0, 0, 0]
    selItemPosInfo["minPos"] = [0, 0, 0]

    posXList = []
    posYList = []
    posZList = []

    #選択ポイント(Vertex・CV・EP)の名前リストを取得
    selPointNames = getSelPointNames.get(convFlg=1)
    if len(selPointNames) > 0:
        #ポイントの位置情報を取得
        pointPosInfo = getPointPosInfo.get(selPointNames, space=spaceValue, flatFlg=0)
        model_pointPosList = pointPosInfo["model_pointPosList"]

        posXList = model_pointPosList["all"]["pointPosXList"]
        posYList = model_pointPosList["all"]["pointPosYList"]
        posZList = model_pointPosList["all"]["pointPosZList"]
    else:
        if spaceValue == "local":
            spaceValue = "object"

        selTransforms = pm.ls(sl=1, transforms=1, flatten=1)
        if len(selTransforms) > 0:
            for currentTransform in selTransforms:
                #選択トランスフォームの位置を取得
                currentTransformPos = currentTransform.getTranslation(space=spaceValue)
                posXList.append(currentTransformPos[0])
                posYList.append(currentTransformPos[1])
                posZList.append(currentTransformPos[2])

    if len(posXList) > 0 and len(posYList) > 0 and len(posZList) > 0:
        bBoxXMax = max(posXList)
        bBoxYMax = max(posYList)
        bBoxZMax = max(posZList)

        bBoxXMin = min(posXList)
        bBoxYMin = min(posYList)
        bBoxZMin = min(posZList)

        if sys.version_info.major == 2:
            bBoxXCen = (bBoxXMin + bBoxXMax) / 2
            bBoxYCen = (bBoxYMin + bBoxYMax) / 2
            bBoxZCen = (bBoxZMin + bBoxZMax) / 2
        else:
            bBoxXCen = old_div((bBoxXMin + bBoxXMax), 2)
            bBoxYCen = old_div((bBoxYMin + bBoxYMax), 2)
            bBoxZCen = old_div((bBoxZMin + bBoxZMax), 2)

        selItemPosInfo["cenPos"] = [bBoxXCen, bBoxYCen, bBoxZCen]
        selItemPosInfo["maxPos"] = [bBoxXMax, bBoxYMax, bBoxZMax]
        selItemPosInfo["minPos"] = [bBoxXMin, bBoxYMin, bBoxZMin]

    return selItemPosInfo


#-------------------------------------------------
if __name__ == "__main__":
    pass
