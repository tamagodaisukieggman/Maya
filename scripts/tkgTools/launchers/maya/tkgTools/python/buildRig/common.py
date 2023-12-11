# -*- coding: utf-8 -*-
import codecs
from collections import OrderedDict
from imp import reload
import json
import re

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

def rename(obj=None, prefix=None, suffix=None, replace=None):
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

    return renamed

def get_shapes(node):
    shape_list = cmds.listRelatives(node, s=True, ni=True)

    if not shape_list:
        shape_list = cmds.ls(node, s=True)

    if shape_list:
        return shape_list
    else:
        return None

def fix_shapes(node):
    curve_shapes = get_shapes(node)
    for i, shp in enumerate(curve_shapes):
        cmds.setAttr('{}.lineWidth'.format(shp), 2)

        if i == 0:
            cmds.rename(shp, node + "Shape")
        else:
            cmds.rename(shp, "{}Shape_{}".format(node, i))

def create_curve_on_nodes(nodes=None, name=None):
    pts = [cmds.xform(j,q=True,ws=True,t=True) for j in nodes]
    crv = cmds.curve(ep=pts, d=3, n=name)
    fix_shapes(crv)
    return crv

def get_transform(node):
    if node:
        if cmds.nodeType(node) == "transform":
            transform = node
        else:
            transform = cmds.listRelatives(node, type="transform", parent=True)[0]

        return transform

    else:
        return None

def order_dags(dags=None, type='transform'):
    parent_dag = cmds.ls(dags[0], l=1, type=type)[0].split('|')[1]

    all_hir = cmds.listRelatives(parent_dag, ad=True, f=True)
    hir_split_counter = {}
    parent_node = '|' + parent_dag
    hir_split_counter[parent_node] = len(parent_node.split('|'))
    for fp_node in all_hir:
        hir_split_counter[fp_node] = len(fp_node.split('|'))

    hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

    sorted_joint_list = [dag_count[0] for dag_count in hir_split_counter_sorted]

    all_ordered_dags = cmds.ls(sorted_joint_list)
    return [dag for dag in all_ordered_dags if dag in dags]

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point

def vector_from_two_points(point_a=None, point_b=None):
    pos_a = get_world_pose(point_a)
    pos_b = get_world_pose(point_b)

    return [b-a for a, b in zip(pos_a, pos_b)]


def get_world_pose(pos):
    if isinstance(pos, list) or isinstance(pos, tuple) and len(pos) == 3:
        pass
    elif isinstance(pos, str) or isinstance(pos, unicode):
        pos = cmds.xform(pos,
                         query=True,
                         worldSpace=True,
                         translation=True)
    else:
        cmds.error('Must provide cartesian position or transform node for pos.')

    return pos


def vector_length(vector=[]):
    return pow(sum([pow(n, 2) for n in vector]), 0.5)


def distance_between(point_a=None, point_b=None):
    vector_ab = vector_from_two_points(point_a, point_b)
    distance = vector_length(vector_ab)
    return distance

def chain_length(chain_list=None):
    chain_length = []
    for i, obj in enumerate(chain_list):
        if i == 0:
            pass
        else:
            length = distance_between(obj, chain_list[i-1])
            chain_length.append(length)
    return chain_length

def split_list(lst):
    # リストの長さを取得
    length = len(lst)

    # リストの長さが偶数の場合
    if length % 2 == 0:
        # 中間のインデックスを見つける
        middle_index = length // 2
        # リストを中間で分割する
        return lst[:middle_index], lst[middle_index:]
    # リストの長さが奇数の場合
    else:
        # 中間のインデックスを見つける
        middle_index = length // 2
        # 中間の値を含む分割されたリストを返す
        return lst[middle_index], lst[:middle_index], lst[middle_index+1:]

def m_obj(obj):
    selection_list = om2.MSelectionList()
    selection_list.add(obj)
    return selection_list.getDependNode(0)

def fn_addNumAttr(obj=None, longName=None, shortName=None, minValue=None, maxValue=None, defaultValue=None, numericData=om2.MFnNumericData.kFloat):
    m_object = m_obj(obj)
    m_dependency_node = om2.MFnDependencyNode(m_object)

    num_att_fn = om2.MFnNumericAttribute(m_object)
    attr = num_att_fn.create(longName, shortName, numericData, defaultValue) # float
    num_att_fn.keyable=True

    if maxValue != None:
        num_att_fn.setMax(maxValue)
    if minValue != None:
        num_att_fn.setMin(minValue)

    m_dependency_node.addAttribute(attr)

def json_transfer(file_name=None, operation=None, export_values=None):
    if operation == 'export':
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)
        except:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)
        except:
            with open(file_name, 'r', encoding="utf-8") as f:
                return json.load(f, object_pairs_hook=OrderedDict)
