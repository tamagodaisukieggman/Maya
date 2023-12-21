# -*- coding: utf-8 -*-
import codecs
from collections import OrderedDict
import fnmatch
from imp import reload
import json
import re
import traceback

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

def order_dags(dags=None):
    parent_dag = cmds.ls(dags[0], l=1)[0].split('|')[1]

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

def mid_point(objA=None, objB=None, percentage=0.5):
    pos1 = cmds.xform(objA, q=True, t=True, ws=True)
    pos2 = cmds.xform(objB, q=True, t=True, ws=True)
    return get_mid_point(pos1, pos2, percentage)

def set_mid_point(objA=None, objB=None, objC=None, percentage=0.5):
    mid_pos = mid_point(objA, objB, percentage)
    cmds.xform(objC, t=mid_pos, ws=True, a=True)

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

def get_virtual_transform(obj=None, relative_move=[0,0,0]):
    wt = cmds.xform(obj, q=True, t=True, ws=True)
    wr = cmds.xform(obj, q=True, ro=True, ws=True)

    virtual_loc = cmds.spaceLocator()[0]

    cmds.xform(virtual_loc, t=wt, ws=True, a=True)
    cmds.xform(virtual_loc, ro=wr, ws=True, a=True)

    cmds.xform(virtual_loc, t=relative_move, os=True, r=True)

    virtual_pos = cmds.xform(virtual_loc, q=True, t=True, ws=True)
    virtual_rot = cmds.xform(virtual_loc, q=True, ro=True, ws=True)

    cmds.delete(virtual_loc)

    return [virtual_pos, virtual_rot]

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

def set_rgb(node, color):
    rgb = ("R","G","B")
    for channel, color in zip(rgb, color):
        cmds.setAttr(node + ".overrideColor{}".format(channel), color)

def set_rgb_color(ctrl=None, color=[1,1,1]):
    # shape = cmds.listRelatives(ctrl, s=True, f=True)[0]
    shapes = cmds.listRelatives(ctrl, s=True, f=True)
    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled",1)
        cmds.setAttr(shape + ".overrideRGBColors",1)
        set_rgb(shape, color)

def set_obj_color(obj=None, color=[0.5, 0.5, 0.5], outliner=None):
    cmds.setAttr(obj+'.useObjectColor', 2)
    cmds.setAttr(obj+'.wireColorRGB', *color)

    if outliner:
        cmds.setAttr(obj+'.useOutlinerColor', 1)
        cmds.setAttr(obj+'.outlinerColor', *color)

def create_spaces(base_ctrl=None,
                  base_ctrl_space=None,
                  space_ctrls=None,
                  spaces=None,
                  const_type='parent',
                  space_type='enum'):

    if not cmds.objExists(base_ctrl):
        return

    # print('{}...{}'.format(spaces, space_ctrls))

    for i, (sp, cl) in enumerate(zip(spaces, space_ctrls)):
        space_node = '{}_{}_spc'.format(base_ctrl, sp)

        cmds.createNode('transform', n=space_node)
        cmds.matchTransform(space_node, base_ctrl)

        if cmds.objExists(cl):
            cmds.parent(space_node, cl)

        if const_type == 'parent':
            cnst = cmds.parentConstraint(space_node, base_ctrl_space, w=1, mo=True)

        if const_type == 'pos':
            cnst = cmds.pointConstraint(space_node, base_ctrl_space, w=1, mo=True)

        if const_type == 'rot':
            cnst = cmds.orientConstraint(space_node, base_ctrl_space, w=1, mo=True)
            cmds.setAttr('{}.interpType'.format(cnst[0]), 2)

        if space_type == 'double':
            cmds.addAttr(base_ctrl, ln='{}Space'.format(sp), at='double', max=1, min=0, dv=0, k=1)
            cmds.connectAttr('{}.{}Space'.format(base_ctrl, sp), cnst[0]+'.w{}'.format(i), f=1)

        if space_type == 'enum':
            #
            spcdn = base_ctrl + '_' + sp + '_cdn'
            if not cmds.objExists(spcdn):
                cmds.createNode('condition', n=spcdn)

            if cmds.objExists(base_ctrl + '.space'):
                get_en_attrs = cmds.addAttr(base_ctrl + '.space', q=True, en=True)
                get_en_attrs = get_en_attrs + ':' + sp
                cmds.addAttr(base_ctrl + '.space', e=True, en=get_en_attrs)
            else:
                cmds.addAttr(base_ctrl, ln='space', at='enum', en=sp, k=1)

            cmds.setAttr(spcdn + '.secondTerm'.format(spcdn), i)
            cmds.setAttr(spcdn + '.colorIfTrueR'.format(spcdn), 1)
            cmds.setAttr(spcdn + '.colorIfFalseR'.format(spcdn), 0)

            cmds.connectAttr(base_ctrl + '.space', '{0}.firstTerm'.format(spcdn), f=1)
            cmds.connectAttr('{0}.outColorR'.format(spcdn), cnst[0]+'.w{}'.format(i), f=1)

def closest_hit_point_on_mesh(point=None, mesh=None, axis='z'):
    axis_dict = {
        'x':[1,0,0],
        'y':[0,1,0],
        'z':[0,0,1],
        '-x':[-1,0,0],
        '-y':[0,-1,0],
        '-z':[0,0,-1]
    }

    direction = om2.MVector(*axis_dict[axis])  # Z軸方向
    startPoint = om2.MPoint(*point)


    # メッシュのダグパスを取得
    selectionList = om2.MSelectionList()
    selectionList.add(mesh)
    dagPath = selectionList.getDagPath(0)

    # メッシュの形状ノードを取得
    meshFn = om2.MFnMesh(dagPath)

    try:
        # レイの作成と交点の取得
        hitPoint = meshFn.closestIntersection(
            om2.MFloatPoint(startPoint),  # レイの開始点
            om2.MFloatVector(direction),  # レイの方向
            om2.MSpace.kWorld,            # ワールド座標系
            10000,                       # 最大距離
            False                        # 任意の交点ではなく最も近い点
        )[0]
    except:
        return point

    return [hitPoint.x, hitPoint.y, hitPoint.z]

def get_finger_tip(mesh=None):
    sel = cmds.ls(os=True)
    # 選択されたメッシュの頂点を取得
    vertices = cmds.polyListComponentConversion(mesh, toVertex=True)
    vertices = cmds.filterExpand(vertices, selectionMask=31)

    # 条件に合う頂点を探索
    max_x = float('-inf')
    min_y = float('inf')
    target_vertex = None

    for vertex in vertices:
        # 頂点の座標を取得
        position = cmds.pointPosition(vertex, world=True)

        # Xが最大でYが最小の頂点を探す
        if position[0] > max_x or (position[0] == max_x and position[1] < min_y):
            max_x = position[0]
            min_y = position[1]
            target_vertex = vertex

    persp_wt = cmds.xform('persp', q=True, t=True, ws=True)
    persp_wr = cmds.xform('persp', q=True, ro=True, ws=True)

    cmds.xform('persp', t=[0,0,0], ro=[0,0,0], a=True)
    cmds.viewFit()

    cmds.select(target_vertex, r=True)

    pw_count = 30
    for i in range(pw_count):
        cmds.pickWalk(d='down')

    finger_tip = cmds.ls(os=True)[0]

    cmds.xform('persp', t=persp_wt, ws=True)
    cmds.xform('persp', ro=persp_wr, ws=True)

    if sel:
        cmds.select(sel, r=True)

    cmds.FrameSelectedWithoutChildren()

    return finger_tip

def get_perpendicular_point(pos1, pos2, obj_pos):
    # 2点間の座標を取得
    # pos1 = cmds.xform(line_point1, q=True, ws=True, t=True)
    # pos2 = cmds.xform(line_point2, q=True, ws=True, t=True)

    # 2点間のベクトル（直線の方向）を計算
    line_vector = [pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2]]

    # 別のオブジェクトの位置を取得
    # obj_pos = cmds.xform(other_object, q=True, ws=True, t=True)

    # オブジェクトから直線への最短距離ベクトルを計算
    obj_vector = [obj_pos[0] - pos1[0], obj_pos[1] - pos1[1], obj_pos[2] - pos1[2]]
    dot_product = sum(p*q for p, q in zip(obj_vector, line_vector))
    line_length_squared = sum(p*p for p in line_vector)
    t = dot_product / line_length_squared

    # 最も近い点を計算
    closest_point = [pos1[0] + t * line_vector[0], pos1[1] + t * line_vector[1], pos1[2] + t * line_vector[2]]

    return closest_point

def merge_curves(sel=None):
    if not sel:
        sel = cmds.ls(os=True)
    # cmds.select(sel[0], r=True)
    # cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
    if not sel:
        return
    shape = cmds.listRelatives(sel[0], s=True, f=True) or list()
    # cmds.select(sel[0], r=True)
    # mel.eval('channelBoxCommand -freezeAll;')
    if shape:
        for sh in shape:
            cmds.parent(sh, sel[1], s=True, r=True)

    cmds.delete(sel[0])

    cmds.select(sel[1], r=True)

def get_sublists(lst, n):
    """ 
    リストからn個ずつの要素を持つサブリストを生成する関数。
    ここではn=3としています。
    """
    return [lst[i:i + n] for i in range(len(lst) - n + 1)]

def filter_items(source_items=None, search_txt_list=None, remover=None):
    """
    source_items = cmds.ls(os=True, type='joint', dag=True)

    search_txt_list = [
        '*cloth_test*',
        '*proxy_*',
        '*ik_*'
    ]

    filtered_items = filter_items(source_items=source_items, search_txt_list=search_txt_list, remover=False)
    """

    filtered_items = list()
    filters = list()
    for search_txt in search_txt_list:
        filtered = list(set(fnmatch.filter(source_items, search_txt)))
        [filters.append(fil) for fil in filtered]

    if remover:
        [filtered_items.append(item) for item in source_items if not item in filters]
    else:
        [filtered_items.append(item) for item in source_items if item in filters]

    return filtered_items

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
