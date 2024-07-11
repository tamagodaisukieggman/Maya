# -*- coding: utf-8 -*-

"""
選択項目の変換

"""

toolName = "TkgConvertSelection"
__author__ = "TKG,  Yuta Kimura"

import pymel.core as pm


#-------------------------------------------------
#メイン
def convert(targetType):
    if targetType == "vertex":
        pm.runtime.ConvertSelectionToVertices()
        pm.runtime.SelectVertexMask()

    elif targetType == "edge":
        pm.runtime.ConvertSelectionToEdges()
        pm.runtime.SelectEdgeMask()

    elif targetType == "polygon":
        pm.runtime.ConvertSelectionToFaces()
        pm.runtime.SelectFacetMask()

    elif targetType == "uv":
        pm.runtime.ConvertSelectionToUVs()
        pm.runtime.SelectUVMask()

    elif targetType == "vertexFace":
        pm.runtime.ConvertSelectionToVertexFaces()
        pm.runtime.SelectVertexFaceMask()

    return


#-------------------------------------------------
if __name__ == '__main__':
    pass
