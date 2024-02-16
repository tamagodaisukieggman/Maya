# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


import maya.cmds as cmds


def save_in_extra_attrs(save_node, param_dict):
    """パラメーターをセーブノードのエクストラアトリビュートに保存

    Args:
        save_node (str): セーブするノード
        param_dict (dict): {attr_name: {'type': type, 'value': value},,,}
    """

    if not save_node or not cmds.objExists(save_node):
        return

    for key, val in param_dict.items():

        data_type = val.get('type')
        data_value = val.get('value')

        if data_type is None or data_value is None:
            continue

        # アトリビュート追加
        if data_type in ['string', 'stringArray', 'floatArray']:
            if not cmds.attributeQuery(key, n=save_node, ex=True):
                cmds.addAttr(save_node, ln=key, dt=data_type)
        else:
            if not cmds.attributeQuery(key, n=save_node, ex=True):
                cmds.addAttr(save_node, ln=key, at=data_type)

        # setAttr
        if data_type == 'string':
            cmds.setAttr('{}.{}'.format(save_node, key), data_value, typ=data_type)
        elif data_type == 'stringArray':
            cmds.setAttr('{}.{}'.format(save_node, key), len(data_value), *data_value, typ=data_type)
        elif data_type == 'floatArray':
            cmds.setAttr('{}.{}'.format(save_node, key), data_value, typ=data_type)
        else:
            cmds.setAttr('{}.{}'.format(save_node, key), data_value)


def load_from_extra_attrs(save_node, target_attr, default_val=None):
    """セーブノードのエクストラアトリビュートからパラメーターを取得

    Args:
        save_node (str): セーブノード
        target_attr (str): 取得するアトリビュート名
        default_val (any, optional): 取得に失敗した際の戻り値. Defaults to None.

    Returns:
        any: 保存されたパラメーター値
    """

    if not save_node or not cmds.objExists(save_node):
        return default_val

    if cmds.attributeQuery(target_attr, n=save_node, ex=True):
        return cmds.getAttr('{}.{}'.format(save_node, target_attr))
    else:
        return default_val


def create_rotate_order_conversion_nodes(from_order, to_order, node_base_name=''):

    rotate_orders = ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']

    base_name = node_base_name or 'ROT_ORDER_CONV'
    cmp_name = base_name + '_CMP'
    dcmp_name = base_name + '_DCMP'

    cmp_mtx = cmds.shadingNode('composeMatrix', au=True, n=cmp_name)
    dcmp_mtx = cmds.shadingNode('decomposeMatrix', au=True, n=dcmp_name)
    cmds.connectAttr(cmp_mtx + '.outputMatrix', dcmp_mtx + '.inputMatrix', f=True)

    if from_order in rotate_orders:
        cmds.setAttr(cmp_mtx + '.inputRotateOrder', rotate_orders.index(from_order))
    if to_order in rotate_orders:
        cmds.setAttr(dcmp_mtx + '.inputRotateOrder', rotate_orders.index(to_order))

    return cmp_mtx, dcmp_mtx