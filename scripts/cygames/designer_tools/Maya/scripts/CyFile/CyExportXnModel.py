# -*- coding: utf-8 -*-

"""
xNormal用のモデルをエクスポート

"""

toolName = "CyExportXnModel"
__author__ = "Cygames, Inc. Yuta Kimura"

import maya.cmds as mc
import pymel.core as pm


#-------------------------------------------------
#メイン
def export():
    #選択中のノード
    selTransNodes = pm.ls(sl=1, transforms=1, flatten=1)
    if len(selTransNodes) != 1:
        return

    #上流ノードも含めて複製
    copiedTopNode = selTransNodes[0].duplicate(upstreamNodes=1)[0]

    #コンバイン ※親ノードが自動的に削除されてしまう可能性があるため、あえてヒストリーを残す
    combinedNodes = pm.polyUnite(copiedTopNode, constructionHistory=0, mergeUVSets=1)
    combinedNode = combinedNodes[0]
    combinedNode.rename("xnModel")

    #三角化
    pm.polyTriangulate(combinedNode, constructionHistory=0)

    #コンバイン後に残ったノードを削除
    if pm.objExists(copiedTopNode):
        pm.delete(copiedTopNode)

    pm.select(combinedNode)

    #FBXエクスポート
#   exportFilePath = pm.Workspace.getPath() + "/data/xnModel.fbx"
#   mc.file(exportFilePath, force=1, exportSelected=1, type="FBX export", options="v=0;", preserveReferences=1)

    #OBJエクスポート
    exportFilePath = pm.Workspace.getPath() + "/data/xnModel.obj"
    mc.file(exportFilePath, force=1, exportSelected=1, type="OBJexport", options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1", preserveReferences=1)

    pm.select(combinedNode)

    return


#-------------------------------------------------
if __name__ == '__main__':
    export()
