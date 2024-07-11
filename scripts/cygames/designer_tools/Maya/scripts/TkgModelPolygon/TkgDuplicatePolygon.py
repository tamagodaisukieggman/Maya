# -*- coding: utf-8 -*-

"""
選択ポリゴンの切り離し

"""

toolName = "TkgDuplicatePolygon"
__author__ = "TKG,  Yuta Kimura"

import maya.cmds as mc


#-------------------------------------------------
#メイン
def Duplicate(mainFlg=0):
    if mainFlg == 1:
        print("")
        print("#-----")
        print("#[Python Command]")
        print("#import TkgDuplicatePolygon")
        print("#-----")
        print("")

    #選択中のノード
    selNodes = mc.ls(sl=1, transforms=1)

    #選択ポリゴンを取得
    allSelPolyNames = mc.filterExpand(expand=1, selectionMask=34)

    if allSelPolyNames == None or len(allSelPolyNames) == 0:
        mc.confirmDialog(title=toolName, message=u"● ポリゴンが1つも選択されていません。")
        return

    newTransformNames = []

    #メッシュ・ポリゴン情報
    meshPolyInfo = {}
    for currentPolyName in allSelPolyNames:
        currentNodeName, polyIndex = currentPolyName.split(".")

        oldTransformName = ""
        if mc.nodeType(currentNodeName) == "transform":
            oldTransformName = currentNodeName
        else:
            oldTransformName = mc.listRelatives(currentNodeName, parent=1, fullPath=1, type="transform")[0]

        if not oldTransformName in meshPolyInfo:
            #メッシュを複製
            newTransformName = mc.duplicate(oldTransformName, name=(oldTransformName.split("|")[-1] + ""))[0]

            #子ノードがある場合は削除
            childNodes = mc.listRelatives(newTransformName, allDescendents=1, fullPath=1, type="transform")
            if childNodes != None and len(childNodes):
                mc.delete(childNodes)

            newTransformNames.append(newTransformName)
            newAllPolyNames = mc.ls(newTransformName + ".f[*]", flatten=1)

            meshPolyInfo[oldTransformName] = {}
            meshPolyInfo[oldTransformName]["newTransformName"] = newTransformName
            meshPolyInfo[oldTransformName]["newAllPolyNames"] = newAllPolyNames
            meshPolyInfo[oldTransformName]["newSelPolyNames"] = []

        meshPolyInfo[oldTransformName]["newSelPolyNames"].append(newTransformName + "." + polyIndex)

    #新メッシュの削除予定ポリゴン
    newDelPolyNames = []
    for oldTransformName in meshPolyInfo:
        newAllPolyNames = meshPolyInfo[oldTransformName]["newAllPolyNames"]
        newSelPolyNames = meshPolyInfo[oldTransformName]["newSelPolyNames"]
        newDelPolyNames.extend(list(set(newAllPolyNames) - set(newSelPolyNames)))

    #ポリゴンを削除
    #mc.delete(allSelPolyNames)
    mc.delete(newDelPolyNames)

    #新メッシュを全て選択
    mc.select(newTransformNames)

    #オブジェクト選択モードに変更
    mc.selectMode(object=1)

    return


#-------------------------------------------------
if __name__ == '__main__':
    Duplicate()
