# -*- coding: utf-8 -*-

"""
フィルタリングされた(タイプ別の)DAGノードリストを取得

"""

toolName = "getFilteredNodeInfo"
__author__ = "TKG,  Yuta Kimura"


import TkgDagNode


#-------------------------------------------------
#メイン
#   srcNodes : フィルタリング前のDAGノードリスト
def get(srcNodes, nodeTypes=[]):
    filteredDagNodeInfo = {}

    nodetype_nodeList = {}
    nodetype_nodeNameList = {}

    for currentNodeType in nodeTypes:
        nodetype_nodeList[currentNodeType] = []
        nodetype_nodeNameList[currentNodeType] = []

    for currentNode in srcNodes:
        currentTkgDagNode = TkgDagNode.TkgDagNode(currentNode)
        currentNodeType = currentTkgDagNode.nodeType

        if currentNodeType not in nodetype_nodeList:
            nodetype_nodeList[currentNodeType] = []
            nodetype_nodeNameList[currentNodeType] = []

        if currentTkgDagNode.mainLongName not in nodetype_nodeNameList[currentNodeType]:
            nodetype_nodeList[currentNodeType].append(currentTkgDagNode.mainNode)
            nodetype_nodeNameList[currentNodeType].append(currentTkgDagNode.mainLongName)

    filteredDagNodeInfo["nodetype_nodeList"] = nodetype_nodeList
    filteredDagNodeInfo["nodetype_nodeNameList"] = nodetype_nodeNameList

    return filteredDagNodeInfo


#-------------------------------------------------
if __name__ == "__main__":
    pass
