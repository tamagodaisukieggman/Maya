# -*- coding: utf-8 -*-
from collections import OrderedDict
import codecs
import json
import re

import maya.cmds as cmds
import maya.api.OpenMaya as om2

import tkgRigBuild.libs.modifyJoints as tkgMJ

COMPOUND_ATTRS = ['translate',
                  'rotate',
                  'scale',
                  'rotateAxis',
                  'preferredAngle',
                  'jointOrient',
                  'wireColorRGB',
                  'outlinerColor']

SINGLE_ATTRS = ['rotateOrder',
                'inheritsTransform',
                'segmentScaleCompensate',
                'side',
                'type',
                'otherType',
                'radius',
                'useObjectColor',
                'objectColor',
                'useOutlinerColor']

def order_dags(dags=None):
    parent_dag = cmds.ls(dags[0], l=1, type='transform')[0].split('|')[1]

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

def get_transform(node):
    if node:
        if cmds.nodeType(node) == "transform":
            transform = node
        else:
            transform = cmds.listRelatives(node, type="transform", parent=True)[0]

        return transform

    else:
        return None

def get_bounding_box(nodes):
    x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(nodes, ce=True)
    return x1, y1, z1, x2, y2, z2

def set_rgb_color(ctrl=None, color=[1,1,1]):
    rgb = ("R","G","B")
    shape = cmds.listRelatives(ctrl, s=True, f=True)[0]
    cmds.setAttr(shape + ".overrideEnabled",1)
    cmds.setAttr(shape + ".overrideRGBColors",1)
    for channel, color in zip(rgb, color):
        cmds.setAttr(shape + ".overrideColor{}".format(channel), color)

def set_obj_color(obj=None, color=[0.5, 0.5, 0.5], outliner=None):
    cmds.setAttr(obj+'.useObjectColor', 2)
    cmds.setAttr(obj+'.wireColorRGB', *color)

    if outliner:
        cmds.setAttr(obj+'.useOutlinerColor', 1)
        cmds.setAttr(obj+'.outlinerColor', *color)

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

def create_curve_on_nodes(nodes=None, name=None):
    pts = [cmds.xform(j,q=True,ws=True,t=True) for j in nodes]
    crv = cmds.curve(ep=pts, d=3, n=name)
    fix_shapes(crv)
    return crv

def create_loft(nodes=None, name='loft_suf', axis='x'):
    if not nodes:
        nodes = cmds.ls(os=True)

    move_axis = {
        'x':[[1, 0, 0], [-1, 0, 0]],
        'y':[[0, 1, 0], [0, -1, 0]],
        'z':[[0, 0, 1], [0, 0, -1]]
    }

    moves = move_axis[axis]

    cuC = create_curve_on_nodes(nodes=nodes, name='{0}_center_crv'.format(nodes[0]))
    cuR = create_curve_on_nodes(nodes=nodes, name='{0}_right_crv'.format(nodes[0]))
    cmds.move(moves[0][0],moves[0][1],moves[0][2],cuR,ls=True) #+z axis
    cuL = cmds.duplicate(cuR)
    cmds.move(moves[1][0],moves[1][1],moves[1][2],cuL,ls=True) #-z axis
    lofted=cmds.loft(cuR, cuL, ch=False, rn=True, n='{}'.format(name))[0]
    cmds.delete(cuR,cuL)
    cmds.rebuildSurface(lofted, rt=0, kc=0, fr=0, ch=1, end=1, sv=0, su=0, kr=0, dir=2, kcp=0, tol=0.01, dv=0, du=0, rpo=1)
    return lofted, cuC

def get_loft_axis(start=None, end=None):
    loft_axis = None
    start_loc = cmds.spaceLocator()[0]
    cmds.xform(start_loc, t=cmds.xform(start, q=1, t=1, ws=1), ws=1, a=1)
    end_loc = cmds.spaceLocator()[0]
    cmds.xform(start_loc, t=cmds.xform(end, q=1, t=1, ws=1), ws=1, a=1)
    cmds.parent(end_loc, start_loc)
    end_loc_wt = cmds.xform(end_loc, q=1, t=1, os=1)
    if abs(end_loc_wt[1]) > abs(end_loc_wt[0]) or abs(end_loc_wt[2]) > abs(end_loc_wt[0]):
        loft_axis = 'x'
    elif abs(end_loc_wt[0]) > abs(end_loc_wt[1]) or abs(end_loc_wt[2]) > abs(end_loc_wt[1]):
        loft_axis = 'y'
    elif abs(end_loc_wt[0]) > abs(end_loc_wt[2]) or abs(end_loc_wt[1]) > abs(end_loc_wt[2]):
        loft_axis = 'z'
    cmds.delete(start_loc)

    return loft_axis

def create_follicles(mesh=None, points=None):
    fols_renames = OrderedDict()
    for obj in points:
        if 'joint' == cmds.objectType(obj):
            fol_shape = obj
        else:
            fol_shape = cmds.listRelatives(obj, s=1)[0] or None

        if not 'follicle' == cmds.objectType(fol_shape):
            fol_shape = cmds.createNode('follicle', ss=1)
            fol = cmds.listRelatives(fol_shape, p=1)[0]
            cmds.matchTransform(fol, obj, pos=1, rot=1)

        if 'follicle' == cmds.objectType(fol_shape):
            fol = cmds.listRelatives(fol_shape, p=1)[0]
            closest_shape = cmds.listRelatives(mesh, s=1)[0] or None
            if 'mesh' == cmds.objectType(closest_shape):
                cpt = cmds.createNode('closestPointOnMesh', ss=1)
                cmds.connectAttr(closest_shape+'.outMesh', cpt+'.inMesh', f=1)
                cmds.connectAttr(closest_shape+'.outMesh', fol_shape+'.inputMesh', f=1)
                cmds.connectAttr(closest_shape+'.worldMatrix[0]', fol_shape+'.inputWorldMatrix', f=1)

            elif 'nurbsSurface' == cmds.objectType(closest_shape):
                cpt = cmds.createNode('closestPointOnSurface', ss=1)
                cmds.connectAttr(closest_shape+'.worldSpace[0]', cpt+'.inputSurface', f=1)
                cmds.connectAttr(closest_shape+'.worldSpace[0]', fol_shape+'.inputSurface', f=1)

            dcmx = cmds.createNode('decomposeMatrix', ss=1)
            cmds.connectAttr(fol+'.worldMatrix[0]', dcmx+'.inputMatrix', f=1)
            cmds.connectAttr(dcmx+'.outputTranslate', cpt+'.inPosition', f=1)

            cmds.setAttr(fol_shape+'.parameterU', cmds.getAttr(cpt+'.parameterU'))
            cmds.setAttr(fol_shape+'.parameterV', cmds.getAttr(cpt+'.parameterV'))

            cmds.connectAttr(fol_shape+'.outTranslate', fol+'.translate', f=1)
            cmds.connectAttr(fol_shape+'.outRotate', fol+'.rotate', f=1)

            cmds.delete(cpt, dcmx)

        fols_renames[fol] = obj+'_fol'

    [cmds.rename(fol_k, fol_v) for fol_k, fol_v in fols_renames.items()]
    fols = [f for f in fols_renames.values()]

    return fols

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

def duplicate_spl_joints(joints=None, prefix='spl_', suffix=None, replace=None):
    joints = cmds.ls(joints, type='joint')
    spls = []
    for jnt in joints:
        new_name = prefix+jnt
        spls.append(new_name)
        dup = cmds.duplicate(jnt, po=True, n=new_name)
        pa = cmds.listRelatives(jnt, p=True) or None
        if pa:
            parent_name = prefix+pa[0]
            if cmds.objExists(parent_name):
                try:
                    cmds.parent(new_name, w=True)
                except:
                    print(traceback.format_exc())

    tkgMJ.merge_joints(spls)

    return spls

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point

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

def json_transfer(file_name=None, operation=None, export_values=None):
    encodings = ["utf-8", "shift_jis", "iso-2022-jp", "euc-jp"]
    if operation == 'export':
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)
        except:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        for encoding in encodings:
            try:
                with codecs.open(file_name, 'r', encoding=encoding) as f:
                    return json.load(f, encoding, object_pairs_hook=OrderedDict)
            except:
                with open(file_name, 'r', encoding=encoding) as f:
                    return json.load(f, object_pairs_hook=OrderedDict)

def get_node_values(nodes=None):
    u"""
    joints_attrs = get_joint_values()
    file_name = 'C:/Users/'+os.environ['USER']+'/Documents/maya/scripts/tkgTools/tkgRig/scripts/build/types/biped/wizard2_base_00_000/000_data/chr0006_proxy_joints.ma.json'
    json_transfer(file_name, 'export', joints_attrs)
    """
    node_values = {}

    ordered_nodes = order_dags(nodes)

    node_values['hierarchy'] = ordered_nodes

    for node in ordered_nodes:
        node_values[node] = {}
        for gcat in COMPOUND_ATTRS:
            if cmds.objExists(node+'.'+gcat):
                node_values[node][gcat] = cmds.getAttr(node+'.'+gcat)[0]
                if gcat == 'translate':
                    node_values[node]['worldTranslate'] = cmds.xform(node, q=True, t=True, ws=True)
                elif gcat == 'rotate':
                    node_values[node]['worldRotate'] = cmds.xform(node, q=True, ro=True, ws=True)
        for gsat in SINGLE_ATTRS:
            if cmds.objExists(node+'.'+gsat):
                node_values[node][gsat] = cmds.getAttr(node+'.'+gsat)
        pa = cmds.listRelatives(node, p=True) or list()
        if pa:
            node_values[node]['parent'] = pa[0]
        else:
            node_values[node]['parent'] = None

    return node_values

def find_centerline(verticies=None, axis='y', local_world='world'):
    """
    Find an approximate centerline of a cylindrical mesh.
    :param mesh: Name of the mesh object.
    :return: A list of points representing the centerline.
    """

    pos_settings = {}
    if local_world == 'local':
        pos_settings['local'] = True
        pos_settings['world'] = False
    if local_world == 'world':
        pos_settings['local'] = False
        pos_settings['world'] = True

    # 頂点の位置を取得
    vertex_positions = [cmds.pointPosition(v, **pos_settings)
                        for v in verticies]

    # 各頂点のXとZ座標の合計を計算
    sum_x, sum_y, sum_z = 0, 0, 0
    for pos in vertex_positions:
        sum_x += pos[0]
        sum_y += pos[1]
        sum_z += pos[2]

    # 平均座標を計算
    n = len(vertex_positions)
    if axis == 'x':
        yz_avg = (sum_y / n, sum_z / n)
        x_coords = [pos[0] for pos in vertex_positions]
        return [(x, yz_avg[0], yz_avg[1]) for x in x_coords]

    elif axis == 'y':
        xz_avg = (sum_x / n, sum_z / n)
        y_coords = [pos[1] for pos in vertex_positions]
        return [(xz_avg[0], y, xz_avg[1]) for y in y_coords]

    elif axis == 'z':
        xy_avg = (sum_x / n, sum_y / n)
        z_coords = [pos[2] for pos in vertex_positions]
        return [(xy_avg[0], xy_avg[1], z) for z in z_coords]


def get_highest_lowest_vertex(verticies=None,
                              axis=['x', 'y', 'z', '-x', '-y', '-z'],
                              than_axis=['x', 'y', 'z'],
                              local_world='world'):
    """
    verticies = cmds.ls(os=True, long=True, fl=True)
    try:
        vertex_values = get_highest_lowest_vertex(verticies, local_world='world')
        highest_pos = vertex_values[0]
        lowest_pos = vertex_values[1]
        higher_than_pos = vertex_values[2]
        lower_than_pos = vertex_values[3]
    except:
        print(traceback.format_exc())
    """
    pos_settings = {}
    if local_world == 'local':
        pos_settings['local'] = True
        pos_settings['world'] = False
    if local_world == 'world':
        pos_settings['local'] = False
        pos_settings['world'] = True

    highest_pos = {}
    lowest_pos = {}
    higher_than_pos = {}
    lower_than_pos = {}
    if 'x' in axis:
        highest_x = float('-inf')
    if 'y' in axis:
        highest_y = float('-inf')
    if 'z' in axis:
        highest_z = float('-inf')
    if '-x' in axis:
        lowest_x = float('inf')
    if '-y' in axis:
        lowest_y = float('inf')
    if '-z' in axis:
        lowest_z = float('inf')

    center_x_points = None
    center_y_points = None
    center_z_points = None
    if 'x' in than_axis:
        center_y_points = find_centerline(verticies, 'y')
        center_z_points = find_centerline(verticies, 'z')

    if 'y' in than_axis:
        center_x_points = find_centerline(verticies, 'x')
        center_z_points = find_centerline(verticies, 'z')

    if 'z' in than_axis:
        center_x_points = find_centerline(verticies, 'x')
        center_y_points = find_centerline(verticies, 'y')

    for i, vertex in enumerate(verticies):
        position = cmds.pointPosition(vertex, **pos_settings)
        # center X
        if 'y' in than_axis or 'z' in than_axis:
            for th_ax in than_axis:
                if 'x' == th_ax:
                    continue
                ul_key = 'centerXthan{}'.format(th_ax.upper())
                if not ul_key in higher_than_pos.keys():
                    higher_than_pos[ul_key] = []
                if not ul_key in lower_than_pos.keys():
                    lower_than_pos[ul_key] = []

                if th_ax == 'y':
                    if position[1] >= center_x_points[i][1]:
                        higher_than_pos[ul_key].append(vertex)
                    elif position[1] <= center_x_points[i][1]:
                        lower_than_pos[ul_key].append(vertex)

                elif th_ax == 'z':
                    if position[2] >= center_x_points[i][2]:
                        higher_than_pos[ul_key].append(vertex)
                    elif position[2] <= center_x_points[i][2]:
                        lower_than_pos[ul_key].append(vertex)

        # center Y
        if 'x' in than_axis or 'z' in than_axis:
            for th_ax in than_axis:
                if 'y' == th_ax:
                    continue
                ul_key = 'centerYthan{}'.format(th_ax.upper())
                if not ul_key in higher_than_pos.keys():
                    higher_than_pos[ul_key] = []
                if not ul_key in lower_than_pos.keys():
                    lower_than_pos[ul_key] = []

                if th_ax == 'x':
                    if position[0] >= center_y_points[i][0]:
                        higher_than_pos[ul_key].append(vertex)
                    elif position[0] <= center_y_points[i][0]:
                        lower_than_pos[ul_key].append(vertex)

                elif th_ax == 'z':
                    if position[2] >= center_y_points[i][2]:
                        higher_than_pos[ul_key].append(vertex)
                    elif position[2] <= center_y_points[i][2]:
                        lower_than_pos[ul_key].append(vertex)

        # center Z
        if 'x' in than_axis or 'y' in than_axis:
            for th_ax in than_axis:
                if 'z' == th_ax:
                    continue
                ul_key = 'centerZthan{}'.format(th_ax.upper())
                if not ul_key in higher_than_pos.keys():
                    higher_than_pos[ul_key] = []
                if not ul_key in lower_than_pos.keys():
                    lower_than_pos[ul_key] = []

                if th_ax == 'x':
                    if position[0] >= center_z_points[i][0]:
                        higher_than_pos[ul_key].append(vertex)
                    elif position[0] <= center_z_points[i][0]:
                        lower_than_pos[ul_key].append(vertex)

                elif th_ax == 'y':
                    if position[1] >= center_z_points[i][1]:
                        higher_than_pos[ul_key].append(vertex)
                    elif position[1] <= center_z_points[i][1]:
                        lower_than_pos[ul_key].append(vertex)


    for i, vertex in enumerate(verticies):
        position = cmds.pointPosition(vertex, **pos_settings)

        if 'x' in axis:
            if position[0] > highest_x:
                highest_x = position[0]
                highest_pos['x'] = vertex
        if 'y' in axis:
            if position[1] > highest_y:
                highest_y = position[1]
                highest_pos['y'] = vertex
        if 'z' in axis:
            if position[2] > highest_z:
                highest_z = position[2]
                highest_pos['z'] = vertex

        if '-x' in axis:
            if position[0] < lowest_x:
                lowest_x = position[0]
                lowest_pos['-x'] = vertex
        if '-y' in axis:
            if position[1] < lowest_y:
                lowest_y = position[1]
                lowest_pos['-y'] = vertex
        if '-z' in axis:
            if position[2] < lowest_z:
                lowest_z = position[2]
                lowest_pos['-z'] = vertex

    return highest_pos, lowest_pos, higher_than_pos, lower_than_pos

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
