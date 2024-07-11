# -*- coding: utf-8 -*-

"""
エクストラアトリビュートを整理

"""
try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from past.builtins import basestring
except Exception:
    pass

toolName = "cleanupExtraAttr"
__author__ = "TKG,  Yuta Kimura"

import pymel.core as pm


#-------------------------------------------------
#メイン
#   node : 対象のノード(PyNode)
#   attrNamePrefix : アトリビュート名のプレフィックスによるフィルター
#   attrType : アトリビュートのタイプによるフィルター
def cleanup(node, attrNamePrefix, attrType):
    #ノード名が渡された場合はPyNodeに変換する
    if isinstance(node, basestring):
        node = pm.PyNode(node)

    #エクストラアトリビュート一覧を取得
    extraAttrs = node.listAttr(userDefined=1)

    #値を取得後にエクストラアトリビュートを削除
    attrValues = []
    for currentAttr in extraAttrs:
        currentAttrName = currentAttr.attrName(longName=1)
        if currentAttrName.startswith(attrNamePrefix) and currentAttr.type() == attrType:
            attrValues.append(currentAttr.get())
            pm.deleteAttr(currentAttr)

    #ノードにエクストラアトリビュートを追加
    for currentAttrIndex in range(len(attrValues)):
        newAttrShortName = attrNamePrefix + str(currentAttrIndex)

        node.addAttr(newAttrShortName, niceName=newAttrShortName, dataType=attrType)
        node.setAttr(newAttrShortName, attrValues[currentAttrIndex])

    return


#-------------------------------------------------
if __name__ == "__main__":
    pass
