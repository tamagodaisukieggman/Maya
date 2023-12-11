# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from . import turtle_utility
from . import bake_setting
from . import tool_utility
from . import tool_define

reload(turtle_utility)
reload(bake_setting)
reload(tool_utility)
reload(tool_define)


def show_preview(bake_layer):
    """ベイク結果をプレビューする

    Args:
        bake_layer (str): 表示するベイクレイヤー
    """

    if not cmds.objExists(bake_layer):
        return

    bake_type = cmds.getAttr('{}.renderType'.format(bake_layer))

    if bake_type == 1:  # BakeToTexture
        __preview_texture(bake_layer)
    elif bake_type == 2:  # BakeToVertices
        __preview_vtx_colors(bake_layer)


def show_default(bake_layer):
    """表示状態を元に戻す

    Args:
        bake_layer (str): 戻すベイクレイヤー
    """

    if not cmds.objExists(bake_layer):
        return

    bake_type = cmds.getAttr('{}.renderType'.format(bake_layer))

    if bake_type == 1:  # BakeToTexture
        __back_to_default_texture(bake_layer)
    elif bake_type == 2:  # BakeToVertices
        __turn_off_vtx_colors(bake_layer)


def __preview_texture(bake_layer):
    """テクスチャベイクの結果を表示する

    Args:
        bake_layer (str): 表示するベイクレイヤー
    """

    shape_list = cmds.ls(cmds.sets(bake_layer, q=True), s=True)

    if not shape_list:
        return

    # 頂点カラーはオフ
    __turn_off_vtx_colors(bake_layer)

    # UVセットとカラーセットを変更
    uv_set = bake_setting.get_texture_bake_uv(bake_layer)
    for shape in shape_list:

        if uv_set in cmds.polyUVSet(shape, q=True, auv=True):
            cmds.polyUVSet(shape, currentUVSet=True, uvSet=uv_set)

        tool_utility.change_colorset(shape, tool_utility.generate_bake_colorset_name(bake_layer))

    # マテリアルの取得
    material_list = tool_utility.get_material_list(shape_list)

    # ベイクマテリアルの割り当て
    for material in material_list:

        # プレビュー用のマテリアルの名前を定義
        bake_material = tool_utility.generate_bake_material_name(bake_layer, material)

        if not cmds.objExists(bake_material):
            cmds.warning(u'ベイクマテリアルが存在しません: {}'.format(bake_material))
            continue

        if material == bake_material:  # 既に割り当たってる
            continue

        # オリジナルのメンバーかつshape_listに含まれるものをプレビュー用のメンバーとする
        shading_group = tool_utility.get_shading_group(material)
        all_material_member_list = cmds.sets(shading_group, q=True)

        this_member_list = []

        for member in all_material_member_list:
            for shape in shape_list:
                if member.find(shape) >= 0:
                    this_member_list.append(member)

        # ベイクマテリアルの割り当て
        bake_shading_group = tool_utility.get_shading_group(bake_material)
        cmds.sets(this_member_list, e=True, fe=bake_shading_group)


def __back_to_default_texture(bake_layer):
    """テクスチャベイクの表示を元に戻す

    Args:
        bake_layer (str): 元に戻すベイクレイヤー
    """

    shape_list = cmds.ls(cmds.sets(bake_layer, q=True), s=True)

    if not shape_list:
        return

    # UVセットをmap1に
    for shape in shape_list:
        cmds.polyUVSet(shape, currentUVSet=True, uvSet='map1')

    # マテリアルの取得
    material_list = tool_utility.get_material_list(shape_list)

    # 確認用マテリアルの割り当て
    for material in material_list:

        if material.find(tool_define.PREVIEW_MATERIAL_SUFFIX) < 0:  # 既に割り当たってる
            continue

        org_material = None

        # 元マテリアルを取得(ベイク時にこの接続が作成されているはず)
        mul_div_node = cmds.listConnections('{}.color'.format(material), type='multiplyDivide')
        org_materials = cmds.listConnections(mul_div_node[0] + '.input2', type='lambert')

        if org_materials:
            org_material = org_materials[0]
        else:
            # 接続がない場合は一応名前でも検索
            org_material = tool_utility.slice_base_material_name(material)

            if not cmds.objExists(org_material):
                cmds.warning(u'オリジナルのマテリアルが存在しません：{}'.format(org_material))
                continue

        shading_group = tool_utility.get_shading_group(material)
        material_member_list = cmds.sets(shading_group, q=True)

        default_shading_group = tool_utility.get_shading_group(org_material)
        cmds.sets(material_member_list, e=True, fe=default_shading_group)


def __preview_vtx_colors(bake_layer):
    """頂点カラーベイクを表示する

    Args:
        bake_layer (str): 表示するベイクレイヤー
    """

    shape_list = cmds.ls(cmds.sets(bake_layer, q=True), s=True)

    if not shape_list:
        return

    for shape in shape_list:

        # カラーセットの設定
        set_result = tool_utility.change_colorset(shape, tool_utility.generate_bake_colorset_name(bake_layer))
        if not set_result:
            continue  # ベイクされていない
        cmds.setAttr('{}.displayColors'.format(shape), 1)  # 頂点カラー表示
        # シェイプのカラーブレンド設定
        cmds.setAttr('{}.materialBlend'.format(shape), 6)  # modulate2x


def __turn_off_vtx_colors(bake_layer):
    """頂点カラーベイクの表示を元に戻す

    Args:
        bake_layer (str): 元に戻すベイクレイヤー
    """

    shape_list = cmds.ls(cmds.sets(bake_layer, q=True), s=True)

    if not shape_list:
        return

    for shape in shape_list:
        cmds.setAttr('{}.displayColors'.format(shape), 0)  # 頂点カラー非表示
        cmds.setAttr('{}.materialBlend'.format(shape), 0)  # overwrite


def is_on_preview(bake_layer):
    """ベイク結果をプレビューしているかどうか

    Args:
        bake_layer (str): チェックするベイクレイヤー

    Returns:
        bool: プレビューしているかどうか
    """

    if not cmds.objExists(bake_layer):
        return False

    shape_list = cmds.ls(cmds.sets(bake_layer, q=True), s=True)

    if not shape_list:
        return False

    for shape in shape_list:

        # テクスチャベイクならマテリアルが刺さっているかどうか
        if bake_setting.get_bake_type(bake_layer) == 1:

            material_list = tool_utility.get_material_list(shape_list)

            if not material_list:
                continue

            for material in material_list:

                if material.find(tool_utility.generate_material_suffix(bake_layer)) >= 0:
                    return True

        # 頂点カラーベイクならカラーセットがカレントになっているかどうか
        elif bake_setting.get_bake_type(bake_layer) == 2:

            if cmds.getAttr('{}.displayColors'.format(shape)) != 1:
                continue

            col_sets = cmds.polyColorSet(shape, q=True, currentColorSet=True)

            if not col_sets:
                continue

            if col_sets[0] == tool_utility.generate_bake_colorset_name(bake_layer):
                return True

    return False
