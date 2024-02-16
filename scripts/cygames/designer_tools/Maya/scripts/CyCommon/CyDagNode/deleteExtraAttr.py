# -*- coding: utf-8 -*-

"""
エクストラアトリビュートを削除

"""
try:
    # Maya 2022-
    from past.builtins import basestring
except Exception:
    pass

import pymel.core as pm

toolName = "deleteExtraAttr"
__author__ = "Cygames, Inc. Yuta Kimura"


#-------------------------------------------------
#メイン
#   node : 対象のノード(PyNode)
#   attrNamePrefix : アトリビュート名のプレフィックスによるフィルター
#   attrType : アトリビュートのタイプによるフィルター
def delete(node, attrNamePrefix="", attrType=""):
    #ノード名が渡された場合はPyNodeに変換する
    if isinstance(node, basestring):
        node = pm.PyNode(node)

    #エクストラアトリビュート一覧を取得
    extraAttrs = node.listAttr(userDefined=1)

    #エクストラアトリビュートを削除
    for currentAttr in extraAttrs:
        deleteFlg = 1

        if attrNamePrefix != "":
            if not currentAttr.attrName(longName=1).startswith(attrNamePrefix):
                deleteFlg += -1
        if attrType != "":
            if currentAttr.type() != attrType:
                deleteFlg += -1

        if deleteFlg == 1:
            pm.deleteAttr(currentAttr)

    return


#-------------------------------------------------
if __name__ == "__main__":
    pass
