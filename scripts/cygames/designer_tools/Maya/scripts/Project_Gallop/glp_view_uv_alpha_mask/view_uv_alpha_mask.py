# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import maya.cmds as cmds


# 確認シェーダー名
SHADER_FILE = 'GlpUVAlphaMask.fx'


def create_uv_alpha_mask_material(mat_name):
    """UVAlphaMask確認用マテリアルの作成

    Args:
        mat_name (str): 作成したいマテリアル名

    Returns:
        str: 生成されたマテリアル名
    """

    # シェーダーにインプットするUVセット名
    # 背景班からの指定があったので決め打ち
    RGB_UV_SET = 'uv:map1'
    ALPHA_UV_SET = 'uv:uvSet1'

    if not cmds.pluginInfo('dx11Shader', query=True, loaded=True):
        cmds.loadPlugin('dx11Shader.mll')

    new_material = None
    if cmds.objExists(mat_name):
        return

    new_material = cmds.shadingNode('dx11Shader', name=mat_name, asShader=True)
    shader = os.path.join(os.path.dirname(__file__), SHADER_FILE).replace('\\', '/')

    if not os.path.exists(shader):
        cmds.error('シェーダーが見つかりません')
        return None

    cmds.setAttr(new_material + '.shader', shader, typ='string')

    try:
        cmds.setAttr('{}.{}'.format(new_material, 'TexCoord0_Source'), RGB_UV_SET, type='string')
        cmds.setAttr('{}.{}'.format(new_material, 'TexCoord1_Source'), ALPHA_UV_SET, type='string')
    except Exception:
        cmds.error('シェーダーのセットアップに失敗しました.preferences > Display > Viewport2.0でRenderingEngineがDirectX11になっていることを確認してください.')
        cmds.delete(new_material)
        return None

    return new_material


def create_lambert_material(mat_name):
    """lambertマテリアルの作成
    UVAlphaMaskから戻す際に使用を想定している

    Args:
        mat_name (str): 作成したいマテリアル名

    Returns:
        str: 生成されたマテリアル名
    """

    if cmds.objExists(mat_name):
        return

    new_material = cmds.shadingNode('lambert', name=mat_name, asShader=True)

    return new_material


def replace_to_uv_alpha_mask_material(material):
    """指定したマテリアルをUVAlphaMask確認用に変換

    Args:
        material (str): 変換するマテリアル名

    Returns:
        bool: 変換したか
    """

    if not cmds.objExists(material) or cmds.objectType(material) != 'lambert':
        return False

    org_mat = cmds.rename(material, material + '__org')
    view_mat = create_uv_alpha_mask_material(material)

    if not view_mat:
        org_mat = cmds.rename(org_mat, material)
        return False

    sgs = cmds.listConnections(org_mat, type='shadingEngine')
    if sgs:
        cmds.connectAttr('{}.{}'.format(view_mat, 'outColor'), '{}.{}'.format(sgs[0], 'surfaceShader'), f=True)

    files = cmds.listConnections(org_mat + '.color', type='file')
    if files:
        cmds.connectAttr(files[0] + '.outColor', view_mat + '.MainTexture', f=True)

    cmds.delete(org_mat)
    return True


def replace_to_lambert_material(material):
    """指定したマテリアルをlambertに変換
    表示をもとに戻す際に使用を想定していて、テクスチャにアルファがあるはずなので不当明度にも接続する

    Args:
        material (str): 変換するマテリアル名

    Returns:
        bool: 変換したか
    """

    if not cmds.objExists(material):
        return False

    shader = os.path.join(os.path.dirname(__file__), SHADER_FILE).replace('\\', '/')
    if cmds.objectType(material) != 'dx11Shader' or cmds.getAttr(material + '.shader') != shader:
        return False

    view_mat = cmds.rename(material, material + '__view')
    lam_mat = create_lambert_material(material)

    sgs = cmds.listConnections(view_mat, type='shadingEngine')
    if sgs:
        cmds.connectAttr('{}.{}'.format(lam_mat, 'outColor'), '{}.{}'.format(sgs[0], 'surfaceShader'), f=True)

    files = cmds.listConnections(view_mat + '.MainTexture', type='file')
    if files:
        cmds.connectAttr(files[0] + '.outColor', lam_mat + '.color', f=True)
        cmds.connectAttr(files[0] + '.outTransparency', lam_mat + '.transparency', f=True)

    cmds.delete(view_mat)
    return True
