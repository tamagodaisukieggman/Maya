# -*- coding: utf-8 -*-
u"""ヘアーポリゴンのウェイトコピー
..
    BEGIN__CYGAMES_MENU
    label=CyCopyHairWeight : ヘアーポリゴンのウェイトコピー
    command=main()
    order=3000
    END__CYGAMES_MENU

..
    BEGIN__CYGAMES_MANUAL
    ========================================
    CyCopyHairWeight : ヘアーポリゴンのウェイトコピー
    ========================================
    END__CYGAMES_MANUAL

"""
import maya.cmds as cmds
import maya.mel as mel

import mtku.maya.utils.edgesort as edgesort
from mtku.maya.utils.decoration import undo_redo
from mtku.maya.utils.decoration import hide_uv_editor
from mtku.maya.utils.decoration import hide_script_editor
from mtku.maya.mtklog import MtkLog


logger = MtkLog(__name__)


def sort_edge_ring(sels):
    u"""エッジリングの順番を正す

    :param sels: ソートしたいエッジリング
    :return: ソートされたエッジリング
    """
    edges = edgesort.sort_ring_order(sels)
    return edges


def get_edge_ring(edge):
    u"""エッジリングを選択してソートする

    :param edge: エッジ
    :return: ソートされたエッジリング
    """
    cmds.select(cl=True)
    cmds.select(edge)
    mel.eval('SelectEdgeRingSp')
    edge_ring = cmds.ls(sl=True)
    sorted_edge_ring = sort_edge_ring(edge_ring)

    if sorted_edge_ring[len(sorted_edge_ring) - 1] == edge:
        sorted_edge_ring.reverse()

    return sorted_edge_ring


def convert_edge_to_vertex(edge):
    u"""エッジを頂点に分解してリストをセパレートする

    :param edge: エッジ
    :return: ソートされたエッジリング
    """
    cmds.select(cl=True)
    cmds.select(edge)
    mel.eval("ConvertSelectionToVertices;")
    vtx_list = cmds.ls(sl=True)
    separated_vtx_list = cmds.filterExpand(vtx_list, sm=31)

    return separated_vtx_list


def select_next_vertex(this_vertex, next_edge):
    u"""頂点とそれに隣接したエッジを指定して、隣接頂点を取得する

    :param this_vertex: 選択頂点
    :param next_edge: 隣接エッジ
    :return: 隣接頂点
    """
    next_vtx_list = convert_edge_to_vertex(next_edge)
    cmds.select(cl=True)
    cmds.select(this_vertex)
    mel.eval("ConvertSelectionToEdges;")
    mel.eval("ConvertSelectionToVertices;")
    this_vtx_list = cmds.ls(sl=True)
    this_separated_vtx_list = convert_edge_to_vertex(this_vtx_list)
    next_vtx = None

    for i in range(len(this_separated_vtx_list)):
        if this_separated_vtx_list[i] in next_vtx_list:
            next_vtx = this_separated_vtx_list[i]

    return next_vtx


def get_vertex_list_for_pasting(this_vtx, edge_list):
    u"""ペースト対象の頂点リストを作成する

    :param this_vertex: 選択頂点
    :param next_edge: 隣接エッジ
    :return: 隣接頂点
    """
    list_length = len(edge_list) - 1
    paste_vtx_list = []
    paste_vtx_list.append(select_next_vertex(this_vtx, edge_list[1]))
    for i in range(list_length - 1):
        paste_vtx_list.append(select_next_vertex(paste_vtx_list[i], edge_list[i + 2]))

    return paste_vtx_list


def copy_weight(this_edge):
    u"""髪単体のウェイトコピー

    :param this_edge: エッジ
    """
    edge_ring = get_edge_ring(this_edge)
    vertexs = convert_edge_to_vertex(this_edge)

    if this_edge != edge_ring[0] and this_edge != edge_ring[len(edge_ring) - 1]:
        return

    for i in range(2):
        this_vtx = vertexs[i]

        paste_vtx_list = get_vertex_list_for_pasting(this_vtx, edge_ring)

        cmds.select(this_vtx)
        mel.eval("artAttrSkinWeightCopy;")
        cmds.select(paste_vtx_list)
        mel.eval("artAttrSkinWeightPaste;")


@undo_redo(True)
@hide_uv_editor
@hide_script_editor
def main():
    u"""ウェイトコピー実行

    """
    logger.usage()
    select_list = cmds.ls(sl=True)
    for i in range(len(select_list)):
        copy_weight(select_list[i])
