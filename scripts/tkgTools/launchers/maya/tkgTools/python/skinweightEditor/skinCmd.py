# -*- coding: utf-8 -*-
from imp import reload
import traceback

import maya.cmds as cmds

import skinweightEditor.edge as edge
reload(edge)

def list_related_skinClusters(nodes):
    """
    List SkinClusters
    """
    if not nodes:
        return []

    shapes = cmds.listRelatives(nodes, s=True, ni=True, pa=True, type='controlPoint')
    if not shapes:
        shapes = cmds.ls(nodes, ni=True, type='controlPoint')
        if not shapes:
            return []

    history = cmds.listHistory(shapes, pdo=True)
    if not history:
        return []

    return cmds.ls(history, typ='skinCluster') or []

def get_skinweights_from_vertices(vertices=None):
    vert_skin_weights = {}
    for vtx in vertices:
        skin_cluster = cmds.ls(cmds.listHistory(vtx), type='skinCluster')
        skin_cluster = skin_cluster[0]
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
        weights = cmds.skinPercent(skin_cluster, vtx, query=True, value=True)
        vert_skin_weights[vtx] = {}
        vert_skin_weights[vtx]['vertices'] = list(zip(influences, weights))
        vert_skin_weights[vtx]['skinCluster'] = skin_cluster
    return vert_skin_weights

def copy_hair_skinweights(base_obj=None, hair_obj=None):
    """
    :usage:
    from imp import reload

    import maya.cmds as cmds

    import skinweightEditor.edge as edge
    import skinweightEditor.skinCmd as skin
    reload(edge)
    reload(skin)

    skin.copy_hair_skinweights()
    """
    closest_edges = edge.get_closest_edges_from_selection(base_obj, hair_obj)

    for close_edge, loop_edges in closest_edges.items():
        # 根元の頂点の取得
        base_vertices_from_edges = cmds.polyListComponentConversion(close_edge, toVertex=True)
        base_vertices_from_edges_flatted = cmds.ls(base_vertices_from_edges, fl=True)

        # 根元の頂点のウェイトの取得
        base_vertices_skin_weights = get_skinweights_from_vertices(vertices=base_vertices_from_edges_flatted)

        # 他の頂点の取得
        other_vertices_from_edges = cmds.polyListComponentConversion(loop_edges, toVertex=True)
        other_vertices_from_edges_flatted = cmds.ls(other_vertices_from_edges, fl=True)

        set_weights = [bvsw for bvsw in base_vertices_skin_weights.values()][0]['vertices']
        skin_cluster = [bvsw for bvsw in base_vertices_skin_weights.values()][0]['skinCluster']

        for other_vert in other_vertices_from_edges_flatted:
            cmds.skinPercent(skin_cluster, other_vert, transformValue=set_weights)
