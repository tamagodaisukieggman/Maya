# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds


def set_env_shadow(mat):
    """背景の落ち影をMayaで確認しやすくする
    UnityのBgRedAlphaGreenColorShadowFogシェーダーを模している
    Rを不透明度、GをRGBに指定する
    """

    # マテリアル確認
    if not cmds.objExists(mat) or cmds.objectType(mat) != 'lambert':
        return

    # ファイルノード確認
    file_nodes = cmds.listConnections(mat, t='file')

    if not file_nodes:
        return

    file_node = file_nodes[0]

    # マテリアルを初期化
    set_default_lambert(mat)

    # 不透明度変換用ノード確認
    rev_nodes = cmds.listConnections(mat, t='reverse')
    rev_node = None

    if not rev_nodes:
        rev_node = cmds.shadingNode('reverse', asUtility=True, n='alpha_reverse')
    else:
        for rev in rev_nodes:
            if rev.find('alpha_reverse') >= 0:
                rev_node = rev
                break
        if not rev_node:
            rev_node = cmds.shadingNode('reverse', asUtility=True, n='alpha_reverse')

    # アトリビュートコネクト
    cmds.connectAttr(file_node + '.outColorR', rev_node + '.inputX', f=True)
    cmds.connectAttr(rev_node + '.output', mat + '.transparency', f=True)
    cmds.disconnectAttr(file_node + '.outColor', mat + '.color')
    cmds.connectAttr(file_node + '.outColorG', mat + '.colorR', f=True)
    cmds.connectAttr(file_node + '.outColorG', mat + '.colorG', f=True)
    cmds.connectAttr(file_node + '.outColorG', mat + '.colorB', f=True)


def set_default_lambert(mat):
    """ただのランバートに戻す
    """

    # マテリアル確認
    if not cmds.objExists(mat) or cmds.objectType(mat) != 'lambert':
        return

    # ファイルノード確認
    file_nodes = cmds.listConnections(mat, t='file')

    if not file_nodes:
        return

    file_node = file_nodes[0]

    # 不透明度変換用ノード削除
    rev_nodes = cmds.listConnections(mat, t='reverse')

    if rev_nodes:
        for rev in rev_nodes:
            if rev.find('alpha_reverse') >= 0:
                cmds.delete(rev)

    # アトリビュートコネクトをoutColor - colorに直す
    g_connect_attr_list = cmds.listConnections(file_node + '.outColorG', p=True)

    if g_connect_attr_list:
        for attr in g_connect_attr_list:
            if check_connection(file_node + '.outColorG', attr):
                cmds.disconnectAttr(file_node + '.outColorG', attr)

    if not check_connection(file_node + '.outColor', mat + '.color'):
        cmds.connectAttr(file_node + '.outColor', mat + '.color', f=True)


def check_connection(src_attr, dst_attr):
    """アトリビュートコネクトのチェック
    """

    connect_attr_list = cmds.listConnections(src_attr, p=True)

    if not connect_attr_list:
        return False

    for attr in connect_attr_list:
        if attr == dst_attr:
            return True

    return False
