# -*- coding: utf-8 -*-
import maya.cmds as cmds

import re

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

def get_mirrors(self, mirrors=['_L', '_R'], src=None):
    mirrors_src_found = re.findall(mirrors[0], src)

    renamed_char = src.replace(mirrors[0], mirrors[1])

    if len(mirrors_src_found) > 1:
        splited_src = src.split('_')
        splited_mir_src = [mir for mir in mirrors[0].split('_') if not mir == '']
        splited_mir_dst = [mir for mir in mirrors[1].split('_') if not mir == '']
        src_idx = 0
        for spl_d in splited_src:
            for spl_ms in splited_mir_src:
                if spl_d == spl_ms:
                    src_idx = splited_src.index(spl_d)
                    break

        combined = []
        for i, repl_d in enumerate(splited_src):
            if i == src_idx:
                repl_d = ''.join(splited_mir_dst)

            combined.append(repl_d)

        renamed_char = '_'.join(combined)

    return renamed_char


def temp_rename(obj=None, prefix=None, suffix=None, replace=None, mirrors=None):
    """
    obj=None, prefix=None, suffix=None, replace=None
    """
    # replace
    replace_name = obj
    if replace:
        replace_name = obj.replace(*replace)

    # prefix
    if not prefix:
        prefix = ''
    prefix_name = re.sub("^", prefix, replace_name)

    # suffix
    if not suffix:
        suffix = ''
    renamed = re.sub("$", suffix, prefix_name)

    if mirrors:
        return get_mirrors(mirrors=mirrors, src=renamed)
    return renamed
