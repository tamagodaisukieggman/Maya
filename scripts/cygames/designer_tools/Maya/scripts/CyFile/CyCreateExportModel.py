# -*- coding: utf-8 -*-

"""
エクスポート用のモデルを作成

"""
from __future__ import unicode_literals

try:
    # Maya 2022-
    from importlib import reload
    from builtins import range
except Exception:
    pass

toolName = "CyCreateExportModel"
__author__ = "Cygames, Inc. Yuta Kimura"

import maya.cmds as mc
import maya.mel as mm
import pymel.core as pm

import CyPivotTool
import CySelectChildNode
import CyDagNode
import CyDagNode.deleteExtraAttr as deleteExtraAttr

reload(CyPivotTool)
reload(CySelectChildNode)
reload(deleteExtraAttr)

#-------------------------------------------------
#メイン
def createAll(transNodes=[]):
    if len(transNodes) == 0:
        #確認メッセージ
        messageStr = u"「CyExportModel」によってエクスポートされるデータを確認用として作成します。"
        messageStr += "\n" + u"※作成されるデータはフラグによる追加処理を実行した後のものになります。"
        messageStr += "\n"
        messageStr += "\n" + u"実行しますか？"
        dialogResult = pm.confirmDialog(title=toolName, message=messageStr, button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
        if dialogResult == "No":
            return

        transNodes = pm.ls(sl=1, transforms=1, flatten=1)
        if len(transNodes) == 0:
            messageStr = u"操作対象が1つも選択されていません。"
            pm.confirmDialog(title=toolName, message=u"● " + messageStr)
            return

    resultNodes = []
    for currentNode in transNodes:
        #エクスポート用のデータを作成(1データ)
        resultInfo = createOne(currentNode, "create")

        currentTopNode = resultInfo["topNode"]
        currentExportName = resultInfo["exportName"]

        resultNodes.append(currentTopNode)

    pm.select(resultNodes)

    return


#-------------------------------------------------
#エクスポート用のモデルを作成(1データ)
def createOne(srcTopNode, mode):
    resultInfo = {}

    exportName = srcTopNode.shortName().split("TEMP_TEMP_TEMP")[0].split("__")[0]

    #移動値と回転値を取得
    worldPosValue = srcTopNode.getTranslation("world")
    worldRotValue = srcTopNode.getRotation("world")
    worldScaleValue = srcTopNode.getScale()

    #上流ノードも含めて複製
    copiedTopNode = srcTopNode.duplicate(upstreamNodes=1)[0]

    #親子付解除
    copiedTopNode.setParent(None)

    #エクスポートオプション情報を取得(再帰)
    allNodes, exportOptionInfo = getExportOptionInfo(copiedTopNode, [], {})
    initCopiedTopNodeKey = copiedTopNode.longName()

    #トップノードを初期化
    # notransresetフラグがある場合も子階層の編集時に面倒なので、一度リセットして最後に復元する
    initTopNode(copiedTopNode)

    #エクスポートオプションを適用
    allResultNodes = applyExportOption(copiedTopNode, allNodes, exportOptionInfo)
    if not pm.objExists(copiedTopNode):
        copiedTopNode = allResultNodes[0]

    # クリエートモードか元々のトップノードにnotransresetフラグが立っているときはトランスフォーム値を戻す
    if mode == "create" or exportOptionInfo[initCopiedTopNodeKey]["notransreset"]:

        copiedTopNode.setTranslation(worldPosValue, space="world")
        copiedTopNode.setRotation(worldRotValue, space="world")
        copiedTopNode.setScale(worldScaleValue)

        if mode == "create":
            #一時グループを作成
            tempGroupNode = None
            tempGroupName = "|export_temp"
            if pm.objExists(tempGroupName):
                tempGroupNode = pm.PyNode(tempGroupName)
            else:
                tempGroupNode = pm.group(name=tempGroupName, empty=1)

            #一時グループに移動
            copiedTopNode.setParent(tempGroupNode)

    #リネーム
    pm.rename(copiedTopNode, exportName)

    resultInfo["topNode"] = copiedTopNode
    resultInfo["exportName"] = exportName

    pm.select(copiedTopNode)

    return resultInfo


#-------------------------------------------------
#トップノードを初期化
def initTopNode(topNode):
    pm.select(topNode)

    #トップノードのトランスフォームをリセットする
    topNode.setTranslation([0, 0, 0], space="world")
    topNode.setRotation([0, 0, 0], space="world")
    topNode.setScale([1, 1, 1])

    #デフォーマ前のヒストリーを削除
    try:
        mm.eval('doBakeNonDefHistory(1, {"pre"})')
    except:
        pass

    return


#-------------------------------------------------
#エクスポートオプションを適用
def applyExportOption(topNode, allNodes, exportOptionInfo):
    allResultNodes = []
    allNodeExportNames = []

    for currentNode in allNodes:
        pm.select(currentNode)

        #ノード名
        currentNodeLongName = currentNode.longName()
        currentNodeExportName = currentNode.shortName().split("|")[-1].split("__")[0]
        allNodeExportNames.append(currentNodeExportName)

        #スキンメッシュの場合
        if exportOptionInfo[currentNodeLongName]["isSkinMesh"] == 1:
            #バインドポーズに戻す
            pm.runtime.GoToBindPose()

        #フラグ
        combineFlg = exportOptionInfo[currentNodeLongName]["combine"]
        keepTransFlg = exportOptionInfo[currentNodeLongName]["keeptrans"]
        mergeFlg = exportOptionInfo[currentNodeLongName]["merge"]
        freezeFlg = exportOptionInfo[currentNodeLongName]["freeze"]
        boundingboxFlg = exportOptionInfo[currentNodeLongName]["boundingbox"]
        attributeFlg = exportOptionInfo[currentNodeLongName]["attribute"]
        noPivResetFlg = exportOptionInfo[currentNodeLongName]["nopivreset"]

        currentNewNode = None

        #コンバインする場合
        if combineFlg == 1:

            # keepTransFlgが立っている場合は元のトランスフォーム情報を最後に戻す必要がある
            # コンバイン時にトランスフォーム情報が消えてしまうので、一旦保存してリセットからコンバインし後で復元する
            org_position = None
            org_rotation = None
            org_scale = None

            if keepTransFlg == 1:
                # トランスフォーム情報の取得. ピボットはコンバイン後に復元されるので不要.
                org_position = mc.xform(currentNodeLongName, q=True, t=True)
                org_rotation = mc.xform(currentNodeLongName, q=True, ro=True)
                org_scale = mc.xform(currentNodeLongName, q=True, s=True)

                mc.xform(currentNodeLongName, t=[0, 0, 0])
                mc.xform(currentNodeLongName, ro=[0, 0, 0])
                mc.xform(currentNodeLongName, s=[1, 1, 1])

            currentParentNode = currentNode.getParent()

            currentParentNodeLongName = ""
            if currentParentNode != None:
                currentParentNodeLongName = currentParentNode.longName()

            #子メッシュを取得
            childMeshNodes = CySelectChildNode.getSpecificTypeChildNodes([currentNode], ["mesh"], 1, 0, 1)

            #子メッシュが1つも存在しない場合
            if len(childMeshNodes) == 0:
                currentNewNode = currentNode
            else:
                #子メッシュが1つの場合→コンバインしない
                if len(childMeshNodes) == 1:
                    currentNewNode = childMeshNodes[0]

                    #現在のノードがメッシュの場合
                    if currentNewNode == currentNode:
                        pass

                    #現在のノードがメッシュ以外の場合
                    else:
                        if currentNewNode.getParent() != currentNode:
                            currentNewNode.setParent(currentNode)

                        #フリーズ・リセット
                        freezeReset(currentNewNode, noPivResetFlg)

                        #親子付を変更
                        if currentParentNodeLongName != "":
                            if pm.objExists(currentParentNodeLongName):
                                currentNewNode.setParent(currentParentNode)

                        #残ったノードを削除
                        if pm.objExists(currentNodeLongName):
                            pm.delete(currentNode)

                #子メッシュが2つ以上ある場合→コンバインする
                elif len(childMeshNodes) >= 2:
                    #コンバイン前のワールド座標を取得
                    currentWorldPosValue = currentNode.getTranslation(space="world")

                    #コンバイン ※親ノードが自動的に削除されてしまう可能性があるため、あえてヒストリーを残す
                    resultNodeNames = mc.polyUnite(currentNodeLongName, constructionHistory=1, mergeUVSets=1)
                    currentCombinedNode = pm.PyNode(resultNodeNames[0])

                    currentNewNode = currentCombinedNode

                    #親子付を復帰
                    if currentParentNodeLongName != "":
                        if pm.objExists(currentParentNodeLongName):
                            currentNewNode.setParent(currentParentNode)

                    #コンバイン後のヒストリー削除
                    pm.delete(currentNewNode, constructionHistory=1)

                    #残ったノードを削除
                    if pm.objExists(currentNodeLongName):
                        pm.delete(currentNode)

                    # 親にトランスフォーム値が入っていると親子付を復活させた時に値が入ってしまいトランスフォーム情報を復元できなくなるのでリセット
                    if keepTransFlg == 1:
                        freezeReset(currentNewNode, noPivResetFlg)

                    #センターをコンバイン前のワールド座標に移動
                    CyPivotTool.moveCenter(currentNewNode, currentWorldPosValue)

            # トランスフォーム情報の復元
            if keepTransFlg == 1:
                mc.xform(currentNewNode.name(), t=org_position)
                mc.xform(currentNewNode.name(), ro=org_rotation)
                mc.xform(currentNewNode.name(), s=org_scale)

        else:
            currentNewNode = currentNode

        #センターピボットを実行する場合
        if boundingboxFlg == 1:
            if freezeFlg == 0:
                currentNewNode.centerPivots()

                #センター → ピボット
                CyPivotTool.moveCenterToPivot()

        #フリーズする場合
        if freezeFlg == 1:
            #フリーズ・リセット
            freezeReset(currentNewNode, noPivResetFlg)

        #頂点マージする場合
        if mergeFlg == 1:
            #頂点マージ
            pm.polyMergeVertex(currentNewNode, distance=0.01, constructionHistory=0)

        if attributeFlg == 1:
            #不要なエクストラアトリビュートを削除
            deleteExtraAttr.delete(currentNewNode, "exportInfo_path", "string")
        else:
            #全てのエクストラアトリビュートを削除
            deleteExtraAttr.delete(currentNewNode)

        allResultNodes.append(currentNewNode)

    for currentNodeIndex in range(len(allResultNodes)):
        currentNode = allResultNodes[currentNodeIndex]

        #リネーム
        currentNodeExportName = allNodeExportNames[currentNodeIndex]
        currentNode.rename(currentNodeExportName)

    return allResultNodes


#-------------------------------------------------
#エクスポートオプション情報を取得(再帰)
def getExportOptionInfo(node, allNodes=[], exportOptionInfo={}):
    allNodes.append(node)

    #ノード名
    nodeLongName = node.longName()
    nodeShortName = node.shortName().split("|")[-1]

    exportOptionInfo[nodeLongName] = {}

    #フラグ
    exportOptionInfo[nodeLongName]["combine"] = 0
    exportOptionInfo[nodeLongName]["merge"] = 0
    exportOptionInfo[nodeLongName]["freeze"] = 0
    exportOptionInfo[nodeLongName]["boundingbox"] = 0
    exportOptionInfo[nodeLongName]["attribute"] = 0
    exportOptionInfo[nodeLongName]["notransreset"] = 0
    exportOptionInfo[nodeLongName]["nopivreset"] = 0
    exportOptionInfo[nodeLongName]["keeptrans"] = 0

    #ノードタイプ
    cyDagNode = CyDagNode.CyDagNode(node)
    exportOptionInfo[nodeLongName]["nodeType"] = cyDagNode.nodeType

    #スキンメッシュかどうか
    exportOptionInfo[nodeLongName]["isSkinMesh"] = 0

    #ヒストリーを調べる
    historyNodes = pm.listHistory(node)
    for currentHistoryNode in historyNodes:
        #スキンメッシュの場合
        if isinstance(currentHistoryNode, pm.nodetypes.SkinCluster):
            exportOptionInfo[nodeLongName]["isSkinMesh"] = 1

    #ノード名を分解してエクスポートオプションを取得
    nameParts = nodeShortName.lower().split("__")
    if len(nameParts) > 1:
        if nameParts[1] != "":
            optionFlgs = nameParts[1].split("_")
            for currentFlg in optionFlgs:
                #コンバインする場合
                if currentFlg in ["combine", "cmb"]:
                    exportOptionInfo[nodeLongName]["combine"] = 1

                #コンバイン時にトランスフォーム値を保持する
                elif currentFlg in ["keeptrans", "kts"]:
                    exportOptionInfo[nodeLongName]["keeptrans"] = 1

                #頂点マージする場合
                elif currentFlg in ["merge", "mrg"]:
                    exportOptionInfo[nodeLongName]["merge"] = 1

                #フリーズする場合
                elif currentFlg in ["freeze", "frz"]:
                    exportOptionInfo[nodeLongName]["freeze"] = 1

                #センターピボットを実行する場合
                elif currentFlg in ["boundingbox", "bbox"]:
                    exportOptionInfo[nodeLongName]["boundingbox"] = 1

                #エクストラアトリビュートを残す場合
                elif currentFlg in ["attribute", "atr"]:
                    exportOptionInfo[nodeLongName]["attribute"] = 1

                #トップノードのトランスフォームのリセットをしない場合
                elif currentFlg in ["notransreset", "ntr"]:
                    exportOptionInfo[nodeLongName]["notransreset"] = 1

                #ピボットのリセットをしない場合
                elif currentFlg in ["nopivreset", "npr"]:
                    exportOptionInfo[nodeLongName]["nopivreset"] = 1

    if exportOptionInfo[nodeLongName]["combine"] == 0:
        #子ノードが存在する場合
        childNodes = node.getChildren()
        if len(childNodes) > 0:
            for childNode in childNodes:
                if childNode.type() == "transform":
                    #エクスポートオプション情報を取得(再帰)
                    allNodes, exportOptionInfo = getExportOptionInfo(childNode, allNodes, exportOptionInfo)

    return allNodes, exportOptionInfo


#-------------------------------------------------
#フリーズ・リセット
def freezeReset(node, noPivResetFlg):
    #フリーズ
    pm.makeIdentity(node, apply=1, translate=1, rotate=1, scale=1, normal=0)

    if not noPivResetFlg:
        #ピボット位置をリセットする
        node.zeroTransformPivots()

    return


#-------------------------------------------------
if __name__ == "__main__":
    createAll()
