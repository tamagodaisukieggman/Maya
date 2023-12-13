# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

from maya import cmds

from . import constants

reload(constants)


def delete_extra_attributes(node, filter_prefix='', filter_type=''):
    """エクストラアトリビュートを削除する

    Args:
        node (str): 対象ノード名
        filter_prefix (str): 対象プリフィックス
        filter_type (str): 対象ノード名
    """

    attrs = cmds.listAttr(node, userDefined=True) or []

    for attr in attrs:

        long_name = '{}.{}'.format(node, attr)

        if filter_prefix and not attr.startswith(filter_prefix):
            continue

        if filter_type and cmds.getAttr(long_name, type=True) != filter_type:
            continue

        cmds.setAttr(long_name, l=False)
        cmds.deleteAttr(long_name)


def get_transform_and_shape_node(node):
    """指定されたノードから、関連するトランスフォームノード、シェイプノードを取得する

    Args:
        node (str): 対象ノード名

    Returns:
        (str, str): トランスフォームノード名、シェイプノード名
    """

    transform_node = None
    shape_node = None

    node_type = cmds.nodeType(node)

    # 対象ノードがトランスフォームの場合はシェイプを取得してshpae_nodeに設定
    # 対象ノードがスケルトンの場合は対象ノードをtransform_node、shape_nodeに設定
    # その他の場合は対象ノード自身がシェイプなのでその親をtransform_nodeに設定
    if node_type == 'transform':
        transform_node = node
        shapes = cmds.listRelatives(node, shapes=True, fullPath=True)
        shape_node = shapes[0] if shapes else None
    elif node_type in constants.NODE_TYPE_BY_CATEGORY['skeleton']:
        transform_node = node
        shape_node = node
    else:
        trasnforms = cmds.listRelatives(node, parent=True, fullPath=True)
        transform_node = trasnforms[0] if trasnforms else None
        shape_node = node

    return transform_node, shape_node


def get_child_transform_nodes(node, include_self=False, recurse=False, node_types=None):

    flags = {str('allDescendents'): True} if recurse else {str('children'): True}

    child_nodes = [node] if include_self else []
    child_nodes.extend(cmds.listRelatives(node, fullPath=True, **flags) or [])
    child_xform_and_shape_nodes = [get_transform_and_shape_node(child_node) for child_node in child_nodes]

    # ノードタイプでフィルタリング
    if not node_types:
        node_types = constants.NODE_TYPES
    child_xform_nodes = [xform for xform, shape in child_xform_and_shape_nodes if get_shape_node_type(shape) in node_types]

    # 重複削除
    child_xform_nodes = sorted(set(child_xform_nodes), key=child_xform_nodes.index)

    # shape経由で元のノードが含まれる可能性があるため除外
    if not include_self:
        child_xform_nodes = [xform for xform in child_xform_nodes if xform != node]

    return child_xform_nodes


def get_shape_node_type(shape_node):
    """シェイプノードからタイプを取得する

    Args:
        shape_node (str): 対象シェイプノード名

    Returns:
        str: ノードタイプ
    """

    # シェイプが存在しないなら'group'
    return cmds.nodeType(shape_node) or 'group'


def get_node_type(node):
    """ノードタイプを取得する

    Args:
        node (str): 対象ノード名

    Returns:
        str: ノードタイプ
    """

    _, shape_node = get_transform_and_shape_node(node)

    return get_shape_node_type(shape_node)


def move_center(node, pos):
    """センター位置を指定位置に移動する

    Args:
        node (str): 対象ノード名
        pos (list[float]): センター位置
    """

    transform_node, shape_node = get_transform_and_shape_node(node)
    node_type = get_shape_node_type(shape_node)

    # 子ノードを取得
    child_nodes = get_child_transform_nodes(transform_node)

    unparented_child_nodes = [cmds.parent(child_node, world=True) for child_node in child_nodes]

    # ノードのワールド座標(移動前)
    before_world_pos = cmds.xform(transform_node, q=True, translation=True, worldSpace=True)

    # ノードをピボット位置に移動する
    cmds.xform(transform_node, translation=pos, worldSpace=True)

    # ノードのワールド座標(移動後)
    after_world_pos = cmds.xform(transform_node, q=True, translation=True, worldSpace=True)

    # 移動値
    move_values = [before - after for before, after in zip(before_world_pos, after_world_pos)]

    if node_type in constants.NODE_TYPE_BY_CATEGORY['model']:
        # 全頂点
        all_verts = ''
        if node_type == 'mesh':
            all_verts = '{}.vtx[*]'.format(shape_node)
        elif node_type == 'nurbsSurface':
            all_verts = '{}.cv[*][*]'.format(shape_node)
        elif node_type == 'nurbsCurve':
            all_verts = '{}.cv[*]'.format(shape_node)

        # ノードの移動とは逆の方向に全頂点を戻す
        cmds.move(move_values[0], move_values[1], move_values[2], all_verts, relative=True, worldSpace=True)

    elif node_type == 'locator':
        # ロケーターの見た目とセンターを一致させる(ズレを解消する)
        cmds.setAttr('{}.localPositionX'.format(shape_node), 0)
        cmds.setAttr('{}.localPositionY'.format(shape_node), 0)
        cmds.setAttr('{}.localPositionZ'.format(shape_node), 0)

    # ピボットを元の位置に戻す
    cmds.xform(transform_node, rotatePivot=pos, worldSpace=True)

    # 親子付を復帰
    for child_node in unparented_child_nodes:
        cmds.parent(child_node, transform_node)


def move_center_to_pivot(node):
    """センター位置をピボット位置に移動する

    Args:
        node (str): 対象ノード名
    """

    # 回転ピボットのワールド座標
    pivot_world_pos = cmds.xform(node, q=True, rotatePivot=True, worldSpace=True)

    # センターを移動
    move_center(node, pivot_world_pos)
