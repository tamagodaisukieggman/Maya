# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

# from functools import partial
import os
import sys
from itertools import zip_longest
from collections import OrderedDict
import webbrowser

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import maya.mel


TURTLE = "Turtle"
RENDER_GLOBAL = "defaultRenderGlobals"
RENDER_OPTIONS = "TurtleRenderOptions"
TUTTLE_LAYER_MANAGER = "TurtleBakeLayerManager"
MTK_BAKE_LAYER = "ilrBakeLayer_mtk"

BILLBOAD_PREF = "MapBaker"
BILLBOAD_NAME = "{}_billBord".format(BILLBOAD_PREF)
SHADING_NODE_NAME = "initialShadingGroup"

SUFFIX_DICT = {
    "normal_map": "nrm",
    "ws_normal_map": "wnrm",
    "full_shading_map": "fsd",
    "albedo_map": "alb",
    "diffuse_map": "dif",
    "illumination_map": "ilm",
    "depth_map": "dps",
    "alpha_map": "alp",
    "occlusion_map": "occ",
    "thickness_map": "tkn",
    "root_map": "rot"

}


def open_help_site():
    _web_site = "https://wisdom.cygames.jp/pages/viewpage.action?pageId=142529087"
    webbrowser.open(_web_site)


def vertex_color_off(mesh):
    if not cmds.objExists(mesh):
        return
    cmds.setAttr("{}.displayColors".format(mesh), 0)


def change_uv_link(mesh):
    if not cmds.objExists(mesh):
        return
    for _link in cmds.uvLink(q=True, uvSet="{}.uvSet[0].uvSetName".format(mesh)):
        if _link:
            cmds.uvLink(make=True, uvSet="{}.uvSet[1].uvSetName".format(
                mesh), texture=_link)
            cmds.uvLink(uvSet="{}.uvSet[1].uvSetName".format(
                mesh), texture=_link)


def get_parents(node):
    """ルートノード取得

    Args:
        node (str)): Maya ノードの文字列

    Yields:
        [type]: [description]
    """
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in get_parents(parent):
            yield p


def set_world_parent(mesh_node, visible_flag=False):
    _num = 0
    new_transform_node = ""
    node_transform = cmds.listRelatives(mesh_node, p=True, f=True)
    node_transform = node_transform[0]
    if visible_flag:
        cmds.setAttr("{}.v".format(node_transform), 1)
    parent_node = cmds.listRelatives(node_transform, p=True, f=True)
    if parent_node:
        source_parent_children = cmds.listRelatives(
            parent_node, c=True, f=True)
        _num = source_parent_children.index(node_transform)
        new_transform_node = cmds.parent(node_transform, w=True)
    return _num, new_transform_node, parent_node


def reset_parent(num, node, node_parent):
    new_node = cmds.parent(node, node_parent)
    new_node = cmds.ls(new_node, l=True)[0]
    source_parent_children = cmds.listRelatives(node_parent, c=True, f=True)
    new_num = source_parent_children.index(new_node)
    if new_num:
        cmds.reorder(new_node, r=new_num - num)


def create_plane(source_name="", num=0, bb=om2.MBoundingBox()):

    bb_center = bb.center
    bb_width = bb.width
    bb_heigit = bb.height
    bb_depth = bb.depth

    if bb.width > bb.depth:
        _p1 = om2.MPoint(bb_center.x-bb_width/2, bb.min.y, bb_center.z)
        _p2 = om2.MPoint(bb_center.x+bb_width/2, bb.min.y, bb_center.z)
        _p3 = om2.MPoint(bb_center.x-bb_width/2, bb.max.y, bb_center.z)
        _p4 = om2.MPoint(bb_center.x+bb_width/2, bb.max.y, bb_center.z)
    else:
        _p1 = om2.MPoint(bb_center.x-bb_depth/2, bb.min.y, bb_center.z)
        _p2 = om2.MPoint(bb_center.x+bb_depth/2, bb.min.y, bb_center.z)
        _p3 = om2.MPoint(bb_center.x-bb_depth/2, bb.max.y, bb_center.z)
        _p4 = om2.MPoint(bb_center.x+bb_depth/2, bb.max.y, bb_center.z)

    points = [_p1, _p2, _p3, _p4]

    vtxs = [0, 1, 3, 2]
    u_values = om2.MFloatArray([0.0, 1.0, 0.0, 1.0])
    v_values = om2.MFloatArray([0.0, 0.0, 1.0, 1.0])

    vertexArray = om2.MPointArray(points)
    polygonCounts = om2.MIntArray([4])

    polygonConnects = om2.MIntArray(vtxs)

    if not source_name:
        node_name = "{}_{}".format(BILLBOAD_NAME, num)
    else:
        node_name = "{}_{}_{}".format(BILLBOAD_PREF, source_name, num)

    dagModifier = om2.MDagModifier()
    meshTransformObj = dagModifier.createNode('transform')
    meshFn = om2.MFnMesh()

    meshShapeObj = meshFn.create(vertexArray,
                                 polygonCounts,
                                 polygonConnects,
                                 parent=meshTransformObj)

    meshFn.setUVs(u_values, v_values)
    meshFn.assignUVs(polygonCounts, polygonConnects)

    meshFn.setName('{}Shape'.format(node_name))

    dagshapeNodeFn = om2.MFnDagNode(meshShapeObj)
    meshShapeDagPath = dagshapeNodeFn.getPath()

    transformFn = om2.MFnTransform(meshTransformObj)
    dagtransformNodeFn = om2.MFnDagNode(meshTransformObj)
    meshTransformDagPath = dagtransformNodeFn.getPath()

    transformFn.setRotatePivot(bb.center, om2.MSpace.kTransform, False)
    transformFn.setScalePivot(bb.center, om2.MSpace.kTransform, False)
    # transformFn.setTranslation(om2.MVector(0, 2, 0), om2.MSpace.kTransform)

    transformFn.setName(node_name)

    # これがないと処理が行われないので注意
    dagModifier.doIt()

    return meshTransformDagPath.fullPathName(), meshShapeDagPath.fullPathName()


def _create_plane(dagModifier="", source_name="", num=0, bb=om2.MBoundingBox()):
    # より多くのことを API2.0 でやっている版
    # 同名問題未解決のため不使用

    _mul = 1.2

    bb_center = bb.center
    bb_width = bb.width
    bb_heigit = bb.height
    bb_depth = bb.depth

    if bb.width > bb.depth:
        _p1 = om2.MPoint(bb_center.x-bb_width/2, bb.min.y, bb_center.z)
        _p2 = om2.MPoint(bb_center.x+bb_width/2, bb.min.y, bb_center.z)
        _p3 = om2.MPoint(bb_center.x-bb_width/2, bb.max.y, bb_center.z)
        _p4 = om2.MPoint(bb_center.x+bb_width/2, bb.max.y, bb_center.z)
    else:
        _p1 = om2.MPoint(bb_center.x-bb_depth/2, bb.min.y, bb_center.z)
        _p2 = om2.MPoint(bb_center.x+bb_depth/2, bb.min.y, bb_center.z)
        _p3 = om2.MPoint(bb_center.x-bb_depth/2, bb.max.y, bb_center.z)
        _p4 = om2.MPoint(bb_center.x+bb_depth/2, bb.max.y, bb_center.z)

    points = [_p1, _p2, _p3, _p4]

    vtxs = [0, 1, 3, 2]
    u_values = om2.MFloatArray([0.0, 1.0, 0.0, 1.0])
    v_values = om2.MFloatArray([0.0, 0.0, 1.0, 1.0])

    vertexArray = om2.MPointArray(points)
    polygonCounts = om2.MIntArray([4])

    polygonConnects = om2.MIntArray(vtxs)

    if not source_name:
        node_name = "{}_{}".format(BILLBOAD_NAME, num)
    else:
        node_name = "{}_{}_{}".format(BILLBOAD_PREF, source_name, num)

    # dagModifier = om2.MDagModifier()
    meshTransformObj = dagModifier.createNode('transform')
    meshFn = om2.MFnMesh()

    meshShapeObj = meshFn.create(vertexArray,
                                 polygonCounts,
                                 polygonConnects,
                                 parent=meshTransformObj)

    meshFn.setUVs(u_values, v_values)
    meshFn.assignUVs(polygonCounts, polygonConnects)

    meshFn.setName('{}Shape'.format(node_name))

    dagshapeNodeFn = om2.MFnDagNode(meshShapeObj)
    meshShapeDagPath = dagshapeNodeFn.getPath()

    transformFn = om2.MFnTransform(meshTransformObj)
    dagtransformNodeFn = om2.MFnDagNode(meshTransformObj)
    deptransformNodeFn = om2.MFnDependencyNode(meshTransformObj)

    meshTransformDagPath = dagtransformNodeFn.getPath()
    depmeshNodeFn = om2.MFnDependencyNode(meshShapeObj)

    receiveShadows = dagshapeNodeFn.findPlug('receiveShadows', False)
    castsShadows = dagshapeNodeFn.findPlug('castsShadows', False)

    receiveShadows.setBool(False)
    castsShadows.setBool(False)

    transformFn.setRotatePivot(bb.center, om2.MSpace.kTransform, False)
    transformFn.setScalePivot(bb.center, om2.MSpace.kTransform, False)

    transformFn.setScale((_mul, _mul, _mul))

    _rot = om2.MEulerRotation(0, 0, 0)
    if num == 1:
        _rot = om2.MQuaternion([0.0, 0.707106781187, 0.0, 0.707106781187])
    elif num == 2:
        _rot = om2.MQuaternion([0.0, 0.382683432365, 0.0, 0.923879532511])
    elif num == 3:
        _rot = om2.MQuaternion([0.0, -0.382683432365, 0.0, 0.923879532511])

    transformFn.setRotation(_rot, om2.MSpace.kTransform)
    transformFn.setName(node_name)

    # API だと勝手にリネームされないから既に同名がある場合はアサイン失敗する
    dagModifier.commandToExecute('sets -e -forceElement {} {}'.format(
        SHADING_NODE_NAME, meshShapeDagPath.fullPathName().split("|")[-1]))

    return meshTransformDagPath, meshShapeDagPath


def ground_plane(node_name="", bb_size=[]):
    if not node_name or not bb_size:
        return

    point1 = om2.MPoint(bb_size[0][0], bb_size[1][0], bb_size[2][0])
    point2 = om2.MPoint(bb_size[0][1], bb_size[1][1], bb_size[2][1])

    bb = om2.MBoundingBox()
    bb.expand(point1)
    bb.expand(point2)

    _p1 = om2.MPoint(bb.min.x, bb.center.y, bb.min.z)
    _p2 = om2.MPoint(bb.min.x, bb.center.y, bb.max.z)
    _p3 = om2.MPoint(bb.max.x, bb.center.y, bb.min.z)
    _p4 = om2.MPoint(bb.max.x, bb.center.y, bb.max.z)

    points = [_p1, _p2, _p3, _p4]
    vtxs = [0, 1, 3, 2]

    vertexArray = om2.MPointArray(points)
    polygonCounts = om2.MIntArray([4])
    polygonConnects = om2.MIntArray(vtxs)

    dagModifier = om2.MDagModifier()
    meshTransformObj = dagModifier.createNode('transform')
    meshFn = om2.MFnMesh()

    meshShapeObj = meshFn.create(vertexArray,
                                 polygonCounts,
                                 polygonConnects,
                                 parent=meshTransformObj)

    meshFn.setName('{}Shape'.format(node_name))

    dagshapeNodeFn = om2.MFnDagNode(meshShapeObj)
    meshShapeDagPath = dagshapeNodeFn.getPath()

    transformFn = om2.MFnTransform(meshTransformObj)
    dagtransformNodeFn = om2.MFnDagNode(meshTransformObj)
    meshTransformDagPath = dagtransformNodeFn.getPath()

    transformFn.setRotatePivot(bb.center, om2.MSpace.kTransform, False)
    transformFn.setScalePivot(bb.center, om2.MSpace.kTransform, False)
    # transformFn.setTranslation(om2.MVector(0, 2, 0), om2.MSpace.kTransform)

    transformFn.setName(node_name)

    # これがないと処理が行われないので注意
    dagModifier.doIt()

    _plane = meshTransformDagPath.fullPathName()
    _plane_shape = meshShapeDagPath.fullPathName()
    cmds.sets(_plane_shape, e=True, forceElement=SHADING_NODE_NAME)

    _mul = 100
    cmds.setAttr("{}.receiveShadows".format(_plane_shape), 0)
    cmds.setAttr("{}.castsShadows".format(_plane_shape), 0)
    cmds.setAttr("{}.s".format(_plane), _mul, _mul, _mul)
    cmds.setAttr("{}.ty".format(_plane), -(bb.height / 2))

    return _plane


def create_plane_meshes(source_name, bb_size, _count):

    _exists_flag = False
    _exists_nodes = []

    for i in range(_count):
        _bill_bord_name = "{}_{}_{}".format(BILLBOAD_PREF, source_name, i)
        if cmds.objExists(_bill_bord_name):
            _exists_flag = True
            _exists_nodes.append(_bill_bord_name)

    if _exists_flag:
        # cmds.select(_exists_nodes, r=True)
        cmds.warning(u"[ {}_{} ] ノードはすでにシーンに存在してます　削除してから再度実行してください".format(
            BILLBOAD_PREF, source_name))
        return False

    point1 = om2.MPoint(bb_size[0][0], bb_size[1][0], bb_size[2][0])
    point2 = om2.MPoint(bb_size[0][1], bb_size[1][1], bb_size[2][1])

    bb = om2.MBoundingBox()
    bb.expand(point1)
    bb.expand(point2)

    _mul = 1.2
    _planes = []
    _plane_transform = []

    # dagModifier = om2.MDagModifier()

    # グループノードを作る処理、途中　プレーン作成時のペアレントを指定すればできるはず
    # # groupTransformObj = dagModifier.createNode('transform')
    # # transformFn = om2.MFnTransform(groupTransformObj)
    # # dagtransformNodeFn = om2.MFnDagNode(groupTransformObj)
    # # groupTransformDagPath = dagtransformNodeFn.getPath()
    # # transformFn.setName("{}_group".format(BILLBOAD_NAME))

    # より多くの事を API2.0 でやってる版
    # for i in range(_count):
    #     _plane, _plane_shape = create_plane(dagModifier, source_name, i, bb)
    #     _planes.append(_plane_shape.fullPathName())
    #     _plane_transform.append(_plane.fullPathName())

    # dagModifier.doIt()
    # return _planes

    for i in range(_count):

        _plane, _plane_shape = create_plane(source_name, i, bb)

        cmds.sets(_plane_shape, e=True, forceElement=SHADING_NODE_NAME)

        cmds.setAttr("{}.receiveShadows".format(_plane_shape), 0)
        cmds.setAttr("{}.castsShadows".format(_plane_shape), 0)
        cmds.setAttr("{}.s".format(_plane), _mul, _mul, _mul)
        cmds.setAttr("{}.ty".format(_plane), -(bb.height / 2))

        if i == 1:
            cmds.setAttr("{}.r".format(_plane), 0, 90, 0)
        elif i == 2:
            cmds.setAttr("{}.r".format(_plane), 0, 45, 0)
        elif i == 3:
            cmds.setAttr("{}.r".format(_plane), 0, -45, 0)

        _planes.append(_plane_shape)
        _plane_transform.append(_plane)

    # _group = cmds.createNode('transform',name="{}_group".format(BILLBOAD_NAME), skipSelect=True)

    # [cmds.parent(x, _group) for x in _plane_transform]
    return _planes


def create_plane_mesh(bb_size, _count):
    #
    # cmds 版
    #

    _plane_name = BILLBOAD_NAME

    point1 = om2.MPoint(bb_size[0][0], bb_size[1][0], bb_size[2][0])
    point2 = om2.MPoint(bb_size[0][1], bb_size[1][1], bb_size[2][1])

    bb = om2.MBoundingBox()
    bb.expand(point1)
    bb.expand(point2)

    cmds.select(cl=True)

    # (maya.api.OpenMaya.MIntArray([4]), maya.api.OpenMaya.MIntArray([0, 1, 3, 2]))

    _mul = 1.2
    _planes = []
    for i in range(_count):
        if i == 0:
            _plane = cmds.polyPlane(name="{}_{}".format(_plane_name, i),
                                    axis=[0, 0, 1], sh=1, sw=1, sx=1, sy=1, h=bb.height*_mul, w=bb.width*_mul)
            _planes.append(_plane)
        elif i == 1:
            _plane = cmds.polyPlane(name="{}_{}".format(_plane_name, i),
                                    axis=[1, 0, 0], sh=1, sw=1, sx=1, sy=1, h=bb.height*_mul, w=bb.width*_mul)
            _planes.append(_plane)
        elif i == 2:
            _plane = cmds.polyPlane(name="{}_{}".format(_plane_name, i),
                                    axis=[1, 0, 1], sh=1, sw=1, sx=1, sy=1, h=bb.height*_mul, w=bb.width*_mul*_mul)
            _planes.append(_plane)
        else:
            _plane = cmds.polyPlane(name="{}_{}".format(_plane_name, i),
                                    axis=[1, 0, -1], sh=1, sw=1, sx=1, sy=1, h=bb.height*_mul, w=bb.width*_mul*_mul)
            _planes.append(_plane)
        cmds.move(bb.center[0], bb.center[1],
                  bb.center[2], _plane, absolute=True)

    return _planes


def get_poly_meshes():
    """現在の選択の精査と必要ノードの抽出
    :return: ソースメッシュのルートノードとターゲットメッシュのリスト
    :rtype: list
    """
    _current_selections = cmds.ls(
        orderedSelection=True, long=True, type="transform")
    if len(_current_selections) != 2:
        cmds.confirmDialog(message=u"ベイクソース、ベイクターゲットの順番で2つのノードを選択してください",
                           title=u'選択を確認してください',
                           button=['OK'],
                           defaultButton='OK',
                           cancelButton="OK",
                           dismissString="OK")
        return [], []

    _source_meshes = cmds.listRelatives(
        _current_selections[0], allDescendents=True, fullPath=True, type="mesh")
    _target_meshes = cmds.listRelatives(
        _current_selections[1], allDescendents=True, fullPath=True, type="mesh")

    if not _source_meshes:
        cmds.confirmDialog(message=u"選択されたベイクソースにメッシュジオメトリがありませんでした",
                           title=u'選択を確認してください',
                           button=['OK'],
                           defaultButton='OK',
                           cancelButton="OK",
                           dismissString="OK")
        return [], []

    if not _target_meshes:
        cmds.confirmDialog(message=u"選択されたベイクターゲットにメッシュジオメトリがありませんでした",
                           title=u'選択を確認してください',
                           button=['OK'],
                           defaultButton='OK',
                           cancelButton="OK",
                           dismissString="OK")
        return [], []

    # elif len(_target_meshes) != 1:
    #     cmds.confirmDialog(message=u"ベイクターゲットのメッシュジオメトリは一つにしてください",
    #                     title=u'選択を確認してください',
    #                     button=['OK'],
    #                     defaultButton='OK',
    #                     cancelButton="OK",
    #                     dismissString="OK")
    #     return [], []

    return _current_selections[0], _target_meshes


def view_return(_show_hide_flags):
    for _transform, _value in _show_hide_flags.items():
        if not cmds.objExists(_transform):
            continue
        cmds.setAttr("{}.visibility".format(_transform), _value)


def set_view(targets, sources):
    _all_transform = cmds.ls(type="transform", long=True)
    _show_hide_flags = OrderedDict()
    for _transform in _all_transform:
        _show_hide_flags[_transform] = cmds.getAttr(
            "{}.visibility".format(_transform))
        cmds.setAttr("{}.visibility".format(_transform), 0)

    for target in targets:
        if not cmds.objExists(target):
            continue
        transform = cmds.listRelatives(
            target, p=True, f=True, type="transform")
        for _parent in get_parents(target):
            cmds.setAttr("{}.visibility".format(_parent), 1)

    for source in sources:
        if not cmds.objExists(source):
            continue
        transform = cmds.listRelatives(
            source, p=True, f=True, type="transform")
        for _parent in get_parents(transform):
            cmds.setAttr("{}.visibility".format(_parent), 1)

    return _show_hide_flags


def visible_all_mesh():
    meshes = cmds.ls(type="mesh")
    for mesh in meshes:
        for _parent in get_parents(mesh):
            cmds.setAttr("{}.v".format(_parent), 1)


def setting_turtle(texture_bake_flag=True):
    """Turtle の設定
    :return: 設定ができたか、できなかったか
    :rtype: bool
    """
    _render = cmds.ls(RENDER_GLOBAL)
    _flag = True

    if not _render:
        cmds.warning(u"{} がありません!!".format(RENDER_GLOBAL))
        return False

    _render = _render[0]
    # レンダラーを変更
    try:
        cmds.setAttr("{}.currentRenderer".format(
            _render), TURTLE.lower(), type="string")
    except:
        _flag = False
        pass

    # ベイクレイヤー
    _bake_layer = cmds.ls(MTK_BAKE_LAYER)
    if not _bake_layer:
        _bake_layer = cmds.createNode(
            "ilrBakeLayer", name=MTK_BAKE_LAYER, skipSelect=True)
    else:
        _bake_layer = _bake_layer[0]

    cmds.setAttr("{}.orthoRefl".format(MTK_BAKE_LAYER), 1)
    cmds.setAttr("{}.envelopeMode".format(MTK_BAKE_LAYER), 4)
    cmds.setAttr("{}.normalDirection".format(MTK_BAKE_LAYER), 0)

    if not texture_bake_flag:
        cmds.setAttr("{}.renderType".format(_bake_layer), 2)
    else:
        cmds.setAttr("{}.renderType".format(_bake_layer), 1)
        cmds.setAttr("{}.vbClamp".format(_bake_layer), 1)

    # レイヤーマネージャ
    _layer_manager = cmds.ls(TUTTLE_LAYER_MANAGER)

    if not _layer_manager:
        _layer_manager = cmds.createNode(
            "ilrBakeLayerManager", name=TUTTLE_LAYER_MANAGER, skipSelect=True)
        cmds.connectAttr(_bake_layer + ".index",
                         _layer_manager + ".bakeLayerId[0]")
    else:
        _layer_manager = _layer_manager[0]

    # Turtle レンダーオプション
    _turtle_render_option = cmds.ls(RENDER_OPTIONS)
    if not _turtle_render_option:
        _turtle_render_option = cmds.createNode(
            "ilrOptionsNode", name=RENDER_OPTIONS, skipSelect=True)
        cmds.connectAttr(_turtle_render_option + ".message",
                         _bake_layer + ".renderOptions")
    else:
        _turtle_render_option = _turtle_render_option[0]

    # レンダータイプをベイクに変更
    cmds.setAttr("{}.renderer".format(_turtle_render_option), 1)

    if not _flag:
        cmds.warning(u"{} のレンダラーを変更できませんでした　処理を中止します".format(_render))
        return False
    return True


def create_position_map_shader():
    _position_map_shader = cmds.shadingNode(
        'surfaceShader', asShader=True, skipSelect=True)
    _samlper_info = cmds.shadingNode(
        "samplerInfo", asUtility=True, skipSelect=True)
    cmds.connectAttr("{}.pointWorld".format(_samlper_info),
                     "{}.outColor".format(_position_map_shader), force=True)
    return _position_map_shader, _samlper_info


def create_white_shader():
    _white_shader = cmds.shadingNode(
        'surfaceShader', asShader=True, skipSelect=True)
    cmds.setAttr("{}.outColor".format(_white_shader), 1, 1, 1, type="double3")
    return _white_shader


def create_ramp_shader():
    _ramp_shader = cmds.shadingNode(
        'surfaceShader', asShader=True, skipSelect=True)
    # _ramp_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="{}SG".format(_ramp_shader))
    _ramp = cmds.shadingNode("ramp", asTexture=True, skipSelect=True)
    _place2d = cmds.shadingNode(
        "place2dTexture", asUtility=True, skipSelect=True)

    cmds.connectAttr("{}.outUV".format(_place2d),
                     "{}.uv".format(_ramp), force=True)
    cmds.connectAttr("{}.outUvFilterSize".format(_place2d),
                     "{}.uvFilterSize".format(_ramp), force=True)

    cmds.connectAttr("{}.outColor".format(_ramp),
                     "{}.outColor".format(_ramp_shader), force=True)
    # cmds.connectAttr("{}.outColor".format(_ramp_shader), "{}.surfaceShader".format(_ramp_sg), force=True)

    #
    # cmds.connectAttr("{}.outColor".format(_ramp_shader), "{}.customShader".format(MTK_BAKE_LAYER), force=True)

    return _ramp, _place2d, _ramp_shader


def create_occ_sampler():
    _occ = cmds.shadingNode("ilrOccSampler", asShader=True, skipSelect=True)
    _sets = cmds.sets(renderable=True, noSurfaceShader=True,
                      empty=True, name="ilrOccSampler2SG")
    cmds.connectAttr("{}.outColor".format(
        _occ), "{}.surfaceShader".format(_sets), force=True)
    # cmds.connectAttr("{}.outColor".format(_occ), "{}.customShader".format(MTK_BAKE_LAYER), force=True)
    return _occ, _sets


def create_thickness_shader():
    _thick_shader = cmds.shadingNode(
        'surfaceShader', asShader=True, skipSelect=True)
    # _thickness_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="{}SG".format(_thick_shader))
    # cmds.connectAttr("{}.outColor".format(_thick_shader), "{}.surfaceShader".format(_thickness_sg), force=True)
    _thick = cmds.shadingNode('ilrSurfaceThickness',
                              asUtility=True, skipSelect=True)
    cmds.connectAttr("{}.outThickness".format(_thick),
                     "{}.outColor".format(_thick_shader), force=True)
    #cmds.connectAttr("{}.outColor".format(_thick_shader), "{}.customShader".format(MTK_BAKE_LAYER), force=True)
    # cmds.listConnections("{}.outColor".format(_thick_shader), source=True, destination=False)
    # cmds.setAttr("{}.fullShading".format(MTK_BAKE_LAYER), 0)
    return _thick_shader, _thick


def bake_vertex_command(
    target="",
    source="",
    custom_shader_use_flag="",
    custom_shader="",
    use_shadow=0,
    scale_value=1.0,
    filterNormalDev=6,
):

    _cmds_eval = 'ilrVertexBakeCmd '
    _cmds_eval += '-target "{}" '.format(target)
    _cmds_eval += '-source "{}" '.format(source)
    _cmds_eval += '-frontRange 10 '
    _cmds_eval += '-backRange 0 '
    _cmds_eval += '-frontBias 10 '
    _cmds_eval += '-backBias 0 '
    _cmds_eval += '-transferSpace 1 '
    _cmds_eval += '-selectionMode 0 '
    _cmds_eval += '-mismatchMode 0 '
    _cmds_eval += '-envelopeMode 0 '
    _cmds_eval += '-ignoreInconsistentNormals 1 '
    _cmds_eval += '-considerTransparency 1 '
    _cmds_eval += '-transparencyThreshold 0.001000000047 '
    _cmds_eval += '-camera "persp" '
    _cmds_eval += '-normalDirection 0 '
    _cmds_eval += '-shadows {} '.format(use_shadow)
    _cmds_eval += '-alpha 1 '
    _cmds_eval += '-viewDependent 0 '
    _cmds_eval += '-orthoRefl 1 '
    _cmds_eval += '-backgroundColor 0 0 0 '
    _cmds_eval += '-frame 0 '
    _cmds_eval += '-bakeLayer {} '.format(MTK_BAKE_LAYER)
    _cmds_eval += '-samplingMode 1 '
    _cmds_eval += '-minSamples 8 '
    _cmds_eval += '-maxSamples 16 '
    _cmds_eval += '-vertexBias 0.001000000047 '
    _cmds_eval += '-camera "persp" '
    _cmds_eval += '-frame 0 '
    _cmds_eval += '-shadows {} '.format(use_shadow)
    _cmds_eval += '-orthoRefl 1 '
    _cmds_eval += '-alpha 1 '
    _cmds_eval += '-normalDirection 0 '
    _cmds_eval += '-viewDependent 1 '
    _cmds_eval += '-useBlending 1 '
    _cmds_eval += '-rgbBlend 0 '
    _cmds_eval += '-alphaBlend 0 '
    _cmds_eval += '-rgbScale {} '.format(scale_value)
    _cmds_eval += '-alphaScale 1 '
    _cmds_eval += '-saveToColorSet 1 '
    _cmds_eval += '-colorSet "baked_$p" '
    _cmds_eval += '-overwriteColorSet 1 '
    _cmds_eval += '-saveToFile 0 '
    _cmds_eval += '-clamp 1 '
    _cmds_eval += '-rgbMin 0 0 0 '
    _cmds_eval += '-rgbMax 1 1 1 '
    _cmds_eval += '-alphaMin 0 '
    _cmds_eval += '-alphaMax 1 '
    _cmds_eval += '-filter 1 '
    _cmds_eval += '-filterSize 0.05 '
    _cmds_eval += '-filterShape 1.1 '
    _cmds_eval += '-filterNormalDev {} '.format(filterNormalDev)
    if custom_shader_use_flag:
        _cmds_eval += '{} '.format(custom_shader_use_flag)
    else:
        _cmds_eval += '-custom 0 '
    if custom_shader:
        _cmds_eval += '{} '.format(custom_shader)
    else:
        _cmds_eval += ''
    _cmds_eval += '-layer defaultRenderLayer;'

    return _cmds_eval


def bake_command(exprot_path="",
                 file_name="",
                 map_type="normal_map",
                 targets="",
                 sources="",
                 apply_gi=0,
                 resolusion=1024,
                 image_format="tga",
                 full_shading_flag="",
                 normal_map_flag="",
                 normal_space="",
                 albedo_map_flag="",
                 depth_map_flag="",
                 diffuse_map_flag="",
                 alpha_map_flag=0,
                 illumination_map_flag="",
                 custom_shader_use_flag="",
                 custom_shader="",
                 use_shadow=0,
                 edge_dilation=5,
                 bilinear_filter=0,
                 anti_aliasing=1,
                 background_color="0 0 0 ",
                 save_flag=1,
                 normal_flip=0,
                 uv_set="",
                 mismatch_mode_flag="",
                 opacity_threshold=0.8,
                 suffix="",
                 bake_vtx_color_flag=False,
                 ):

    # if extention:
    #     save_flag = 0
    #     file_name = ""
    #     exprot_path = ""
    # else:
    exprot_path = exprot_path.replace(os.sep, '/')
    file_name = "{}_{}.{}".format(file_name, map_type, image_format)

    file_type_dict = {"tga": 0,
                      "tiff": 4,
                      "png": 9}

    image_format_int = file_type_dict[image_format]

    # -transparencyThreshold 0.001000000047
    if suffix and map_type == "albedo_map":
        map_type = suffix

    _cmds_eval = '''
                ilrTextureBakeCmd
                {0:}
                {1:}
                {15:}
                {16:}
                {17:}
                -displacementRemap 1
                -displacementScale 1
                -displacementOffset 0
                -frontRange 10
                -backRange 0
                -frontBias 10
                -backBias 0
                -transferSpace 1
                -selectionMode 0
                {24:}
                -envelopeMode 0
                -ignoreInconsistentNormals 0
                -considerTransparency 1
                -transparencyThreshold {25:}
                -camera "persp"
                -normalDirection 0
                -shadows {11:}
                -alpha {2:}
                -viewDependent 0
                -orthoRefl 1
                -backgroundColor {18:}
                -frame 1
                -bakeLayer {3:}
                -width {4:}
                -height {4:}
                -saveToRenderView 0
                -saveToFile {20:}
                -directory "{5:}"
                -fileName "{6:}"
                -fileFormat {12:}
                -visualize 0
                -uvRange 0
                -uMin 0
                -uMax 1
                -vMin 0
                -vMax 1
                -uvSet "{22:}"
                {23:}
                -tangentUvSet ""
                -edgeDilation {13:}
                -bilinearFilter {14:}
                -merge 1
                -conservative 0
                -windingOrder 1
                {7:}
                {8:}
                {19:}
                -normalsFlipChannel {21:}
                -normalsFaceTangents 0
                -normalsUseBump 1
                -useRenderView 0
                -layer defaultRenderLayer
                {9:}
                {10:};
                '''.format(targets,
                           sources,
                           alpha_map_flag,
                           MTK_BAKE_LAYER,
                           resolusion,
                           exprot_path.replace(os.sep, '/'),
                           file_name,
                           full_shading_flag,
                           normal_map_flag,
                           custom_shader_use_flag,
                           custom_shader,
                           use_shadow,
                           image_format_int,
                           edge_dilation,
                           bilinear_filter,

                           albedo_map_flag,
                           depth_map_flag,
                           illumination_map_flag,
                           background_color,
                           normal_space,
                           save_flag,
                           normal_flip,
                           uv_set,
                           diffuse_map_flag,
                           mismatch_mode_flag,
                           opacity_threshold
                           )
    return _cmds_eval


def turtle_bake_setup(
    exprot_path="",
    file_name="",
    map_type="normal_map",
    targets=[],
    sources=[],
    apply_gi=0,
    resolusion=1024,
    image_format="tga",
    full_shading_flag="",
    normal_map_flag="",
    normal_space="",
    albedo_map_flag="",
    diffuse_map_flag="",
    depth_map_flag="",
    alpha_map_flag=0,
    illumination_map_flag="",
    custom_shader_use_flag="",
    custom_shader="",
    use_shadow=0,
    edge_dilation=5,
    bilinear_filter=0,
    anti_aliasing=1,
    uv_set="",
    opacity_threshold=0.8,
    suffix=""
):

    # bilinear_filter = 0
    if custom_shader_use_flag:
        custom_shader_use_flag = "-custom 1"
        custom_shader = '-customShader "{}"'.format(custom_shader)

    # map_type = map_type + "_$p"

    normal_flip = 0
    if normal_map_flag:
        # cmds.setAttr("{}.normalsFlipChannel".format(MTK_BAKE_LAYER), 2)
        normal_map_flag = "-normals 1 "
        background_color = "0.5 0.5 1 "
        if map_type.split("_")[0] == "ws":
            # normal_map_flag = normal_map_flag + "-normalsFlipChannel 0 "
            normal_space = "-normalsCoordSys 2 "
        else:
            # normal_map_flag = normal_map_flag + "-normalsFlipChannel 2 "
            normal_flip = 2
            normal_space = "-normalsCoordSys 0 "
            # if alpha_map_flag:

            # normal_space += "-stencilBake 1 "
            # alpha_map_flag = 1
    else:
        background_color = "0 0 0 "

    # cmds.setAttr("{}.enableGI".format(RENDER_OPTIONS), 0)
    if albedo_map_flag:
        albedo_map_flag = "-albedo 1 "

    if diffuse_map_flag:
        diffuse_map_flag = "-diffuse 1 "

    if illumination_map_flag:
        illumination_map_flag = "-illumination 1 "

    if depth_map_flag:
        depth_map_flag = "-displacement 1 "

    if full_shading_flag:
        full_shading_flag = "-fullShading 1 "

    if map_type == "occlusion_map":
        mismatch_mode_flag = "-mismatchMode 1 "
    else:
        mismatch_mode_flag = "-mismatchMode 0 "

    if map_type == "alpha_map":
        # edge_dilation = 0
        normal_space = "-normalsCoordSys 0 "
        normal_space += "-stencilBake 1 "
        alpha_map_flag = 1

    if suffix:
        map_type = suffix

    # if full_shading_flag or illumination_map_flag:
    # GI 使うとき
    if apply_gi:
        cmds.setAttr("{}.enableGI".format(RENDER_OPTIONS), 1)
        cmds.setAttr("{}.rtEnvironment".format(RENDER_OPTIONS), 2)
        cmds.setAttr("{}.secondaryIntegrator".format(RENDER_OPTIONS), 1)
    if not apply_gi:
        cmds.setAttr("{}.enableGI".format(RENDER_OPTIONS), 0)
        cmds.setAttr("{}.rtEnvironment".format(RENDER_OPTIONS), 0)
        cmds.setAttr("{}.secondaryIntegrator".format(RENDER_OPTIONS), 0)

    # アンチエイリアシング
    max_anti_aliasing = anti_aliasing + 1 if anti_aliasing < 4 else anti_aliasing
    if anti_aliasing == 0:
        max_anti_aliasing = 0
    cmds.setAttr("{}.aaMinSampleRate".format(RENDER_OPTIONS), anti_aliasing)
    cmds.setAttr("{}.aaMaxSampleRate".format(
        RENDER_OPTIONS), max_anti_aliasing)

    cmds.setAttr("{}.aaFilterSizeX".format(RENDER_OPTIONS), 1)
    cmds.setAttr("{}.aaFilterSizeY".format(RENDER_OPTIONS), 1)
    # cmds.setAttr("{}.aaFilter".format(RENDER_OPTIONS), 0)
    cmds.setAttr("{}.aaFilter".format(RENDER_OPTIONS), 3)

    # ターゲットとソースのみを表示させる
    # 後で表示を元に戻す
    # _all_meshes = cmds.ls(targets + sources, long=True)
    # _all_transform = cmds.ls(type="transform", long=True)
    # _show_hide_flags = {}
    # for _transform in _all_transform:
    #     _cld = cmds.listRelatives(_transform, allDescendents=True, fullPath=True, noIntermediate=True)
    #     if _cld:
    #         _show_hide_flags[_transform] = cmds.getAttr("{}.visibility".format(_transform))
    #         if [x for x in _all_meshes if x in _cld]:
    #             cmds.setAttr("{}.visibility".format(_transform), 1)
    #         else:
    #             cmds.setAttr("{}.visibility".format(_transform), 0)

    billboads = []
    # _show_hide_flags = set_view(targets, sources)

    for target in targets:
        if len(target.split(BILLBOAD_PREF)) != 1:
            billboads.append(target)

    if billboads:
        # targets = ''.join(['-target "{}" '.format(x) for x in billboads])
        if file_name:
            file_name = "{}_".format(file_name)

        # source = '-source "{}" '.format(sources[0])
        sources = ''.join(['-source "{}" '.format(x) for x in sources])

        for target in billboads:
            bill_boad_file_name = "{}{}".format(file_name,
                                                target.split(BILLBOAD_NAME + "_")[-1].split("Shape")[0])
            target = '-target "{}" '.format(target)

            if map_type == "root_map":
                _cmds_eval = bake_command(exprot_path=exprot_path,
                                          file_name=bill_boad_file_name,
                                          map_type=map_type,
                                          targets=target,
                                          sources=sources,
                                          apply_gi=0,
                                          resolusion=2,
                                          image_format=image_format,
                                          custom_shader_use_flag=custom_shader_use_flag,
                                          custom_shader=custom_shader,
                                          edge_dilation=0,
                                          bilinear_filter=0,
                                          anti_aliasing=0,
                                          save_flag=0,
                                          mismatch_mode_flag=mismatch_mode_flag,
                                          opacity_threshold=opacity_threshold,
                                          suffix=suffix)
                try:
                    # print("TrurtleComm----")
                    maya.mel.eval(_cmds_eval)
                except Exception as e:
                    print("Error ", e)

            _cmds_eval = bake_command(exprot_path=exprot_path,
                                      file_name=bill_boad_file_name,
                                      map_type=map_type,
                                      targets=target,
                                      sources=sources,
                                      apply_gi=apply_gi,
                                      image_format=image_format,
                                      resolusion=resolusion,
                                      full_shading_flag=full_shading_flag,
                                      normal_map_flag=normal_map_flag,
                                      normal_space=normal_space,
                                      albedo_map_flag=albedo_map_flag,
                                      diffuse_map_flag=diffuse_map_flag,
                                      depth_map_flag=depth_map_flag,
                                      alpha_map_flag=alpha_map_flag,
                                      illumination_map_flag=illumination_map_flag,
                                      custom_shader_use_flag=custom_shader_use_flag,
                                      custom_shader=custom_shader,
                                      use_shadow=use_shadow,
                                      edge_dilation=edge_dilation,
                                      bilinear_filter=bilinear_filter,
                                      anti_aliasing=anti_aliasing,
                                      background_color=background_color,
                                      normal_flip=normal_flip,
                                      uv_set=uv_set,
                                      mismatch_mode_flag=mismatch_mode_flag,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            try:
                # print("TrurtleComm----")
                maya.mel.eval(_cmds_eval)
            except Exception as e:
                print("Error ", e)

    else:
        targets = ''.join(['-target "{}" '.format(x) for x in targets])
        sources = ''.join(['-source "{}" '.format(x) for x in sources])

        if map_type == "root_map":
            _cmds_eval = bake_command(exprot_path=exprot_path,
                                      file_name=file_name,
                                      map_type=map_type,
                                      targets=targets,
                                      sources=sources,
                                      apply_gi=0,
                                      resolusion=2,
                                      image_format=image_format,
                                      custom_shader_use_flag=custom_shader_use_flag,
                                      custom_shader=custom_shader,
                                      edge_dilation=0,
                                      bilinear_filter=0,
                                      anti_aliasing=0,
                                      save_flag=0,
                                      mismatch_mode_flag=mismatch_mode_flag,
                                      opacity_threshold=opacity_threshold,
                                      suffix=suffix)
            try:
                # print("TrurtleComm----")
                maya.mel.eval(_cmds_eval)
            except Exception as e:
                print("Error ", e)

        _cmds_eval = bake_command(exprot_path=exprot_path,
                                  file_name=file_name,
                                  map_type=map_type,
                                  targets=targets,
                                  sources=sources,
                                  apply_gi=apply_gi,
                                  image_format=image_format,
                                  resolusion=resolusion,
                                  full_shading_flag=full_shading_flag,
                                  normal_map_flag=normal_map_flag,
                                  normal_space=normal_space,
                                  albedo_map_flag=albedo_map_flag,
                                  diffuse_map_flag=diffuse_map_flag,
                                  depth_map_flag=depth_map_flag,
                                  alpha_map_flag=alpha_map_flag,
                                  illumination_map_flag=illumination_map_flag,
                                  custom_shader_use_flag=custom_shader_use_flag,
                                  custom_shader=custom_shader,
                                  use_shadow=use_shadow,
                                  edge_dilation=edge_dilation,
                                  bilinear_filter=bilinear_filter,
                                  anti_aliasing=anti_aliasing,
                                  background_color=background_color,
                                  normal_flip=normal_flip,
                                  uv_set=uv_set,
                                  mismatch_mode_flag=mismatch_mode_flag,
                                  opacity_threshold=opacity_threshold,
                                  suffix=suffix)

        try:
            maya.mel.eval(_cmds_eval)
            print("bake command -- ", _cmds_eval)
        except Exception as e:
            print("Error ", e)
    # if _show_hide_flags:
    #     view_return(_show_hide_flags)
    # # 表示を切り替えたものを元に戻す
    # for _transform, _value in _show_hide_flags.items():
    #     cmds.setAttr("{}.visibility".format(_transform), _value)


def turtle_vertex_bake_setup(
    targets=[],
    sources=[],
    apply_gi=0,
    custom_shader_use_flag="",
    custom_shader="",
    use_shadow=0,
    scale_value=1.0,
    ground_plane="",
    filterNormalDev=6,
):

    if custom_shader_use_flag:
        custom_shader_use_flag = "-custom 1"
        custom_shader = '-customShader "{}"'.format(custom_shader)

    if apply_gi:
        cmds.setAttr("{}.enableGI".format(RENDER_OPTIONS), 1)
        cmds.setAttr("{}.rtEnvironment".format(RENDER_OPTIONS), 2)
        cmds.setAttr("{}.secondaryIntegrator".format(RENDER_OPTIONS), 1)
    if not apply_gi:
        cmds.setAttr("{}.enableGI".format(RENDER_OPTIONS), 0)
        cmds.setAttr("{}.rtEnvironment".format(RENDER_OPTIONS), 0)
        cmds.setAttr("{}.secondaryIntegrator".format(RENDER_OPTIONS), 0)

    # cmds.setAttr("{}.vbClamp".format(RENDER_OPTIONS), 1)
    # 後で表示を元に戻す
    # _all_meshes = cmds.ls(targets + sources, long=True)
    # print(_all_meshes," _all_meshes")

    # _all_transform = cmds.ls(type="transform", long=True)
    # _show_hide_flags = OrderedDict()
    # for _transform in _all_transform:
    #     _show_hide_flags[_transform] = cmds.getAttr("{}.visibility".format(_transform))
    #     cmds.setAttr("{}.visibility".format(_transform), 0)

    for target, source in zip_longest(targets, sources):
        if not source or not target:
            continue
        if ground_plane:
            sources = '-source "{}" -source "{}" '.format(source, ground_plane)
        # source_num, source_transform, sorce_parent = set_world_parent(source, True)
        # target_transform = ""
        # if source != target:
        #     target_num, target_transform, target_parent = set_world_parent(target, True)

        _cmds_eval = bake_vertex_command(
            target=target,
            source=source,
            custom_shader_use_flag=custom_shader_use_flag,
            custom_shader=custom_shader,
            use_shadow=use_shadow,
            scale_value=scale_value,
            filterNormalDev=filterNormalDev,
        )
        try:
            # print("TrurtleComm----[ {} ]".format("vertex baker"))
            maya.mel.eval(_cmds_eval)
        except Exception as e:
            print("Error ", e)

        # if sorce_parent:
        #     reset_parent(source_num, source_transform, sorce_parent)
        #     if target_transform:
        #         reset_parent(target_num, target_transform, target_parent)

    # 表示を切り替えたものを元に戻す
    # for _transform, _value in _show_hide_flags.items():
    #     cmds.setAttr("{}.visibility".format(_transform), _value)

    for target in targets:
        if cmds.objExists(target):
            cmds.setAttr("{}.displayColors".format(target), 1)
            cmds.setAttr("{}.displayColorChannel".format(
                target), "None", type="string")
