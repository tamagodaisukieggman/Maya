#-*- encoding: utf-8
# SameEdgeLength
# エッジの長さを同じにする
# 2023/9/13更新
# 高舘俊之

import maya.cmds as cmds


class SameEdgeLength(object):
    def __init__(self):
        pass

    #=============================================================================================
    # エッジの長さを取得 複数選択は平均
    #=============================================================================================
    def GetLength(self):
        selEdge = cmds.filterExpand(sm=32) #エッジのセレクションマスク　sm=32

        if selEdge is not None:

            Edgelength_list = []

            for sel_edge in selEdge:
                Edgelength_list.append(cmds.arclen(sel_edge))   #選択したエッジのリストへの追加
                Avelength = sum(Edgelength_list) / len(Edgelength_list)    # 長さの平均値
                cmds.floatField('edge_length', v=Avelength, e=True)

                print(u"長さ =  " + str(cmds.arclen(sel_edge)))

        else:
            cmds.error(u"エッジを選択してください")


    #=============================================================================================
    # ロックする頂点の追加ボタン
    #=============================================================================================
    def AddVertex(self):
        allItems = self.GetAllItems()

        #頂点の選択
        sel = cmds.ls(os=True, fl=True)
        selVertices = cmds.ls(cmds.polyListComponentConversion(sel, tv=True), fl=True)
        cmds.select(selVertices)

        if selVertices is not None:
            if allItems is not None:
                for sel_vertex in selVertices:
                    if sel_vertex not in allItems:
                        cmds.textScrollList('lock_VertexList', e=True, a=sel_vertex)
            else:
                cmds.textScrollList('lock_VertexList', e=True, a=selVertices)
        else:
            cmds.error("頂点を選択してください")

    #=============================================================================================
    # リスト上のアイテムを全て取得
    #=============================================================================================
    def GetAllItems(self):
        allItems = cmds.textScrollList('lock_VertexList', q=True, allItems=True)
        return allItems

    #=============================================================================================
    # クリア
    #=============================================================================================
    def ClearList(self):
        cmds.textScrollList('lock_VertexList', edit=True, removeAll=True)


    #=============================================================================================
    # 選択アイテムをリストから削除
    #=============================================================================================
    def RemoveItemList(self):
        selItem = cmds.textScrollList('lock_VertexList', q=True, selectItem=True)
        if selItem is not None:
            cmds.textScrollList('lock_VertexList', edit=True, removeItem=selItem)

    #=============================================================================================
    # 選択アイテムの実体を選択
    #=============================================================================================
    def SelectItem(self):
        selItem = cmds.textScrollList('lock_VertexList', q=True, selectItem=True)
        cmds.select(cl=True)
        cmds.select(selItem)

    #=============================================================================================
    # ロックされた頂点との一致を確認
    #=============================================================================================
    def LockedVertex(self, inc_vertices, allLockVertices):
        match_vertices = []
        for inc_vertex in inc_vertices:
            if inc_vertex not in allLockVertices:
                continue
            else:
                match_vertices.append(inc_vertex)
        return match_vertices

    #=============================================================================================
    # エッジの長さを変更する
    #=============================================================================================
    def SetLength(self, holdUvScale):
        allLockVertices = self.GetAllItems()
        uvsValue = cmds.checkBox(holdUvScale, q=True, v=True)    #チェックボックス

        selEdge = cmds.filterExpand(sm=32) #エッジのセレクションマスク　sm=32
        sourceLength = cmds.floatField('edge_length', q=True, v=True)

        #エッジ選択されてないならエラー
        if not selEdge : 
            cmds.error(u"エッジが何も選択されていません")
            return

        symmetryValue = cmds.symmetricModelling(q=True, s=True)    # シンメトリがONだとおかしくなるので
        Error_edges = []    

        #エッジの長さ変更
        for sel_edge in selEdge:
            cmds.symmetricModelling(e=True, s=False)    # いったんシンメトリOFF
            targetLength = cmds.arclen(sel_edge)
            scaleVal = sourceLength / targetLength
            cmds.select(cl=True)
            cmds.select(sel_edge)

            #ロックする頂点があったらピボット変更
            if allLockVertices is not None:    
                inc_vertices = cmds.ls(cmds.polyListComponentConversion(sel_edge, tv=True), fl=True)
                lockedVertex = self.LockedVertex(inc_vertices, allLockVertices)

                if len(lockedVertex) == 1:    # ロックする頂点の一致が一つだけならピボットに設定
                    pivot_pos = cmds.pointPosition(lockedVertex)
                    cmds.scale(1, scaleVal, 1, cs=True, a=True, p=pivot_pos, puv=uvsValue)
                elif len(lockedVertex) >= 2:    # 両側がロックされた頂点ならエラー
                    Error_edges.append(sel_edge)    #エラーエッジ格納
                else:
                    cmds.scale(1, scaleVal, 1, cs=True, a=True, puv=uvsValue)
            else:
                cmds.scale(1, scaleVal, 1, cs=True, a=True, puv=uvsValue)


        #エラーエッジがあればワーニング
        if len(Error_edges) >= 1:    
            cmds.select(cl=True)
            cmds.select(Error_edges)
            cmds.symmetricModelling(e=True, s=symmetryValue)    # シンメトリ戻す
            cmds.warning(u"エッジの両側の頂点がロックされています")
            return
        else:
            cmds.select(cl=True)
            cmds.select(selEdge)
            cmds.symmetricModelling(e=True, s=symmetryValue)    # シンメトリ戻す


        print(u"エッジの長さを変更しました")


    #=============================================================================================
    # GUIの作成
    #=============================================================================================
    def createGui(self):
        # 「エッジの長さ」項目初期値
        edge_length = 1.0
        
        cmds.window(t = 'SameEdgeLength' )

        cmds.columnLayout()


        #----------------------------------------------------
        # エッジの長さを揃える
        #----------------------------------------------------
        cmds.frameLayout( label=u" エッジの長さを取得する" , bv =True)

        #エッジの長さ
        cmds.rowLayout( nc = 2)
        cmds.text( label=u"エッジの長さ        " , w = 120)
        cmds.floatField('edge_length', v = edge_length , w = 60)
        cmds.setParent('..')

        #エッジの長さを取得
        cmds.button( l='GetLength', command=lambda gl:self.GetLength() , w = 200, bgc=(0.7968, 0.5, 0.5))

        #----------------------------------------------------
        # 頂点を固定
        #----------------------------------------------------
        cmds.frameLayout( label=u" 頂点を固定するリスト" , bv =True)

        #ロックする頂点リスト
        cmds.lockVertexList = cmds.textScrollList(
            'lock_VertexList',
            numberOfRows=6,
            allowMultiSelection=True
        )

        #スクロール
        cmds.textScrollList(
            cmds.lockVertexList,
            edit=True,
            deleteKeyCommand = self.RemoveItemList,
            selectCommand = self.SelectItem
        )

        cmds.rowLayout(numberOfColumns=2, cw2 = (100, 100) ,columnAttach2=('both', 'both'))

        #Add Vertex
        cmds.button( l=u'Add Vertex', command=lambda av:self.AddVertex() , bgc=(0.7968, 0.5, 0.5))

        #Clear
        cmds.button( l=u'Clear', command=lambda cl:self.ClearList() , bgc=(0.7968, 0.5, 0.5))

        cmds.setParent('..')

        # スケーリングの際UVを保持
        holdUvScale = cmds.checkBox(label=u'スケーリングの際UVを保持', v = False)

        #----------------------------------------------------
        # 長さを設定する
        #----------------------------------------------------
        cmds.frameLayout( label=u" 長さを設定する" , bv =True)

        cmds.button( l='SetLength', command=lambda sl:self.SetLength(holdUvScale) , w = 200, bgc=(0.7968, 0.5, 0.5))

        cmds.showWindow()

def main():
    ins = SameEdgeLength()
    ins.createGui()