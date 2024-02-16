# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2


def get_m_selection_list(name):
    """ノード名から選択リストを取得する

    Args:
        name (str): ノード名

    Returns:
        OpenMaya.MSelectionList: 選択リスト
    """

    sel_list = None

    # OpenMayaにオブジェクトの存在チェックがないので例外処理
    try:
        sel_list = om2.MGlobal.getSelectionListByName(name)
    except Exception:
        pass

    return sel_list


def get_m_dag_path(name):
    """ノード名からDAGパスを取得する

    Args:
        name (str): ノード名

    Returns:
        OpenMaya.MDagPath: DAGパス
    """

    sel_list = get_m_selection_list(name)

    return sel_list.getDagPath(0) if sel_list else None


def get_mfn_mesh(name):
    """ノード名からメッシュデータを取得する

    Args:
        name (str): ノード名

    Returns:
        OpenMaya.MFnMesh: メッシュデータ
    """

    dag_path = get_m_dag_path(name)

    if dag_path is None:
        return None

    if not dag_path.hasFn(om2.MFn.kMesh):
        return None

    return om2.MFnMesh(dag_path)


def get_iter(it):
    """OpenMaya.MIt~クラスのイテレータを返すジェネレータ

    Args:
        it (object): OpenMaya.MIt~クラスのイテレータ
    """

    if int(om2.MGlobal.mayaVersion()) <= 2019 and type(it) is om2.MItMeshPolygon:
        while not it.isDone():
            yield it
            # Maya2019以前では、MItMeshPolygonのnextに引数が必要
            it.next(1)
    else:
        while not it.isDone():
            yield it
            it.next()


def convert_to_vertex(sel_list):
    """選択リストをすべて頂点に変換する

    Args:
        sel_list (OpenMaya.MSelectionList): 選択リスト

    Returns:
        OpenMaya.MSelectionList: 選択頂点リスト
    """

    vert_sel_list = om2.MSelectionList()

    if not sel_list:
        return vert_sel_list

    dag_path_to_vertex_set = {}

    for sel_iter in get_iter(om2.MItSelectionList(sel_list)):
        dag_path, comp = sel_iter.getComponent()

        if comp.isNull() and not dag_path.hasFn(om2.MFn.kMesh):
            continue

        vertex_set = set()

        # オブジェクト選択
        if comp.isNull():
            mesh_fn = om2.MFnMesh(dag_path)
            vertex_set = set(range(mesh_fn.numVertices))

        # 頂点選択
        elif comp.hasFn(om2.MFn.kMeshVertComponent):
            vertex_set = set(om2.MFnSingleIndexedComponent(comp).getElements())

        # エッジ選択
        elif comp.hasFn(om2.MFn.kMeshEdgeComponent):
            vertex_set = set(it.vertexId(i) for it in get_iter(om2.MItMeshEdge(dag_path, comp)) for i in range(2))

        # UV選択
        elif comp.hasFn(om2.MFn.kMeshMapComponent):
            map_ids = set(om2.MFnSingleIndexedComponent(comp).getElements())
            vertex_set = set(it.index() for it in get_iter(om2.MItMeshVertex(dag_path)) if any(uv in map_ids for uv in it.getUVIndices()))

        # フェース選択
        elif comp.hasFn(om2.MFn.kMeshPolygonComponent):
            vertex_set = set(v for it in get_iter(om2.MItMeshPolygon(dag_path, comp)) for v in it.getVertices())

        # 頂点フェース選択
        elif comp.hasFn(om2.MFn.kMeshVtxFaceComponent):
            vertex_set = set(it.vertexId() for it in get_iter(om2.MItMeshFaceVertex(dag_path, comp)))

        dag_path_name = dag_path.fullPathName()

        if dag_path_name not in dag_path_to_vertex_set:
            dag_path_to_vertex_set[dag_path_name] = set()

        # 設定済みの頂点との重複を除外
        vertex_set -= dag_path_to_vertex_set[dag_path_name]
        # オブジェクトごとに設定済みの頂点を保存
        dag_path_to_vertex_set[dag_path_name] |= vertex_set

        vert_comp = om2.MFnSingleIndexedComponent()
        vert_comp.create(om2.MFn.kMeshVertComponent)
        vert_comp.addElements(list(vertex_set))

        # 選択順を保持するため、mergeWithExistingにFalseを指定
        vert_sel_list.add((dag_path, vert_comp.object()), mergeWithExisting=False)

    return vert_sel_list


def get_mfn_skin_cluster(name):
    """ノード名からスキンクラスタを取得する

    Args:
        name (str): ノード名

    Returns:
        OpenMaya.MFnSkinCluster: スキンクラスタ
    """

    sel_list = get_m_selection_list(name)

    if sel_list is None:
        return None

    dag_path = sel_list.getDagPath(0)

    if not dag_path.hasFn(om2.MFn.kMesh):
        return None

    mesh_fn = om2.MFnMesh(dag_path)
    depend_iter = om2.MItDependencyGraph(mesh_fn.object(), om2.MFn.kSkinClusterFilter, om2.MItDependencyGraph.kUpstream)

    return oma2.MFnSkinCluster(depend_iter.currentNode()) if not depend_iter.isDone() else None
