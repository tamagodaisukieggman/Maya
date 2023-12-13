# -*- coding: cp932 -*-
#===============================================
#
# MASH関連
#
# Fujita Yukihiro
#
#===============================================

import maya.cmds as cmds
import MASH.api as mapi

#===============================================
#
# コライダーを追加
#
# @param      mashNetworkName : MASH ネットワーク名
# @param      colliderName : コライダーノード名
#
#===============================================
def addCollider(mashNetworkName, colliderName):
    """ コライダーを追加 """

    # ノードが存在しなければ終了
    if cmds.objExists(mashNetworkName) == False:
        print ("// " + mashNetworkName + u" が見つかりません。")
        return ""

    if cmds.objExists(colliderName) == False:
        print ("// " + colliderName + u" が見つかりません。")
        return ""

    # MASH ネットワークを取得
    mashNetwork = mapi.Network(mashNetworkName)

    # コライダーを追加
    mashNetwork.addCollider(colliderName)
