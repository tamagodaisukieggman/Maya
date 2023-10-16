# -*- coding: utf-8 -*-
import maya.cmds as cmds

def order_dags(dags=None, type='transform'):
    parent_dag = cmds.ls(dags[0], l=1, type=type)[0].split('|')[1]

    all_hir = cmds.listRelatives(parent_dag, ad=True, f=True)
    hir_split_counter = {}
    for fp_node in all_hir:
        hir_split_counter[fp_node] = len(fp_node.split('|'))

    hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

    sorted_joint_list = [dag_count[0] for dag_count in hir_split_counter_sorted]

    all_ordered_dags = cmds.ls(sorted_joint_list)
    return [dag for dag in all_ordered_dags if dag in dags]

def create_sets(name=None, add=None):
    if not cmds.objExists(name):
        cmds.sets(em=True, n=name)
    if add:
        cmds.sets(add, add=name)
