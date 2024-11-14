# -*- coding: utf-8 -*-
from imp import reload

import skinweightEditor.calc as calc
import skinweightEditor.mesh as mesh
reload(calc)
reload(mesh)

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

def get_closest_edges_from_selection(hair_obj=None, base_obj=None):
    u"""
    :param hair_obj: ヘアーメッシュ
    :param base_obj: 体、または頭のメッシュ
    :return closest_edges: {近接エッジ:[エッジループ...]}
    :sample import skinweightEditor.edge as edge
    closest_edges = edge.get_closest_edges_from_selection(hair_obj=None, base_obj=None)
    """
    if not hair_obj or not base_obj:
        sel = cmds.ls(os=True)
        base_obj = sel[0]
        hair_obj = sel[1]

    hair_obj_edges = cmds.ls(f'{hair_obj}.e[*]', fl=True)

    edge_loops = []
    for hoe in hair_obj_edges:
        edge_loop = cmds.polySelectSp(hoe, l=True)
        edge_loop_sep = cmds.ls(edge_loop, fl=True)
        edge_loop_sep.sort()
        if len(edge_loop_sep) > 1:
            if not edge_loop_sep in edge_loops:
                edge_loops.append(edge_loop_sep)

    # 
    closest_edges = {}
    for loop_edges in edge_loops:
        edge_ranks = {}
        for edge in loop_edges:
            center_of_edge_point = mesh.get_center_of_cmps(cmps=edge)
            closest_info = mesh.closest_point(base_obj, center_of_edge_point, world=True)
            distance = calc.get_distance(
                obj_A=None,
                obj_B=None,
                gobj_A=center_of_edge_point,
                gobj_B=[closest_info[0].x, closest_info[0].y, closest_info[0].z]
            )
            edge_ranks[edge] = distance
            sorted_edge_ranks = sorted(edge_ranks.items(), key=lambda x:x[1])
            closest_edge = sorted_edge_ranks[0][0]
        if not closest_edge in closest_edges.keys():
            closest_edges[closest_edge] = loop_edges
    
    return closest_edges

