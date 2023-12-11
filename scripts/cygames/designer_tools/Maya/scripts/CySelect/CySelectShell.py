# -*- coding: utf-8 -*-

"""
コンポーネントのアイランド選択
※頂点・エッジ・ポリゴン・UV・頂点フェースに対応

"""

toolName = "CySelectShell"
__author__ = "Cygames, Inc. Yuta Kimura"

import pymel.core as pm


#-------------------------------------------------
#メイン
def select(mainFlg=0):
    if mainFlg == 1:
        print("")
        print("#-----")
        print("#[Python Command]")
        print("#import CySelectShell;reload(CySelectShell);CySelectShell.select()")
        print("#-----")
        print("")

    #頂点・エッジ・ポリゴン
    if pm.selectType(q=1, vertex=1) or pm.selectType(q=1, edge=1) or pm.selectType(q=1, facet=1):
        pm.runtime.ConvertSelectionToShell()
    else:
        #UV
        if pm.selectType(q=1, polymeshUV=1):
            pm.runtime.ConvertSelectionToUVShell()

        #頂点フェース
        elif pm.selectType(q=1, polymeshVtxFace=1):
            pm.runtime.ConvertSelectionToVertices()
            pm.runtime.ConvertSelectionToShell()
            pm.runtime.ConvertSelectionToVertexFaces()
            pm.runtime.SelectVertexFaceMask();

    return


#-------------------------------------------------
if __name__ == '__main__':
    select()
