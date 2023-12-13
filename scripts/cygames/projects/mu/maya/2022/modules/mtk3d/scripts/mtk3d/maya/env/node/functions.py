# -*- coding: cp932 -*-
#===============================================
#
# ノード関連
#
# Fujita Yukihiro
#
#===============================================

import maya.cmds as cmds

#===============================================
#
# 最上位ノードを取得
#
# @param      nodeName : ノード名
# @return     最上位ノード名
#
#===============================================
def getRootNodeName(nodeName):
    """ 最上位のノード名を取得 """

    # ノードネームが空なら終了
    if nodeName == "":
        return ""

    # ノードが存在しなければ終了
    if cmds.objExists(nodeName) == False:
        print ("// " + nodeName + u" が見つかりません。")
        return ""

    # ノードがトランスフォームノードじゃなければ終了
    if cmds.objectType( nodeName, isType='transform' ) == False:
        print ("// " + nodeName + u" はトランスフォームノードではありません。")
        return ""
    
    # ノードのフルパス名を取得
    fullPathName = cmds.ls( nodeName, long=True)
    
    # フルパス名を分割
    tokens = fullPathName[0].split("|")
    
    # ワールドの子の場合
    if nodeName == tokens[1]:
        return nodeName
    else:
        # リストの２番目を返す。一番目は空白が入るので。
        return tokens[1]


#===============================================
#
# 指定したノード階層の中から、指定した文字列を含むノードを取得
#
# @param      targetNode : 対象ノード階層
# @param      searchStrs : 検索文字列リスト
# @return     マッチしたノードリスト
#
#===============================================
def searchNodesContains(targetNode, searchStrs):
    """ 指定したノード階層の中から、指定した文字列を全て含むノードを取得 """
    
    # ノードが存在しなければ終了
    if cmds.objExists(targetNode) == False:
        print ("// " + targetNode + u" が見つかりません。")
        return []
    
    if len(searchStrs) == 0:
        print (u"// 検索文字列が指定されていません。")
        return []

    # 全ての子ノードと孫ノードを取得
    allDescendents = cmds.listRelatives(targetNode, allDescendents=True, path=True, type="transform", noIntermediate=True)

    if allDescendents is None:
        return []

    # マッチしたノードリスト
    matchedNodes = []

    for elm in allDescendents:
        
        # ノード名を分割
        tokens = elm.split("|")
        
        counts = 0
        
        for str in searchStrs:
            
            # 検索文字列がノード名に含まれているか
            if str in tokens[-1]:
                counts += 1
                
        # 検索文字列が全てノード名に含まれていたら
        if len(searchStrs) == counts:
            matchedNodes.append(elm)

    return matchedNodes



