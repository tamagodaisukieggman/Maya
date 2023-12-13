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

import os

import maya.cmds as cmds
import maya.mel as mel

from . import bake_setting
from . import tool_utility
from . import tool_define
from ..glp_bg_exporter import export_model
from ..glp_bg_exporter import commands
from ..glp_bg_exporter import constants

reload(bake_setting)
reload(tool_utility)
reload(tool_define)
reload(export_model)
reload(commands)
reload(constants)


# 出力時の処理用フラグ関連定数
EDIT_FLAG_SEPARATOR = '__'
COMBINE_FLAGS = ['combine', 'cmb']
FREEZE_FLAGS = ['freeze', 'frz']
BBOX_CENTER_FLAGS = ['boundingbox', 'bbox']
MERGE_FLAG = ['merge', 'mrg']
RESULT_COLORSET = '____result_colorset'


def export_fbx(target_transform, export_path, active_bake_layers=[]):
    """FBXの出力
    現在の表示状態をそのまま出力する

    Args:
        target_transform (str): 出力親のトランスフォームノード
        export_path (str): 出力するfbxのパス
    """

    if not cmds.objExists(target_transform):
        return ''

    target_transform_name = target_transform.split('|')[-1]

    org_prefix = '__org__'
    org_transform_name = org_prefix + target_transform_name

    if cmds.objExists(org_transform_name):
        cmds.delete(org_transform_name)

    # オリジナルを一旦リネームし、オリジナルの名前で編集用のコピーを作成
    org_obj = cmds.rename(target_transform, org_transform_name)
    dup_obj_for_edit = cmds.duplicate(org_obj, n=target_transform_name)[0]
    dup_obj_for_edit = cmds.ls(dup_obj_for_edit, l=True)[0]

    output_list = [dup_obj_for_edit]

    all_child_list = cmds.listRelatives(dup_obj_for_edit, ad=True, f=True)
    if all_child_list:
        output_list.extend(all_child_list)

    tmp_node_list = []

    for output_obj in output_list:

        # UVセットの調整
        trim_uv_set(output_obj, active_bake_layers)
        # カラーセットの調整
        trim_colorset(output_obj, active_bake_layers)
        # マテリアルの調整
        tmp_node_list.extend(setup_output_material(output_obj))

    # 編集用のコピーから更に最終出力用のモデルを生成
    # 出力モデルのトランスフォーム編集はglp_bg_exporterのメソッドを使用
    dup_obj_for_edit = cmds.rename(dup_obj_for_edit, dup_obj_for_edit.split('|')[-1] + constants.TEMP_NODE_SUFFIX)
    output_model_info = export_model.create_one(dup_obj_for_edit, 'export')

    # fbx出力
    if not os.path.exists(os.path.dirname(export_path)):
        os.makedirs(os.path.dirname(export_path))
    if os.path.exists(export_path):
        os.remove(export_path)

    cmds.select(output_model_info['topNode'], r=True)
    cmds.select(hi=True)
    result = commands.fbx_export_selection(export_path)

    # 編集用モデル、出力用モデル、一時ノードの削除
    cmds.delete([dup_obj_for_edit, output_model_info['topNode']])
    cmds.delete(tmp_node_list)

    if cmds.objExists(target_transform):
        cmds.delete(target_transform)

    # オリジナルの名前を戻す
    org_obj = cmds.rename(org_obj, target_transform_name)

    return result


def trim_uv_set(obj, active_bake_layers=[]):
    """必要なUVセット以外を削除

    Args:
        obj (str): 対象オブジェクト
    """

    # ライトマップのUVセットはUVセットの2番目に出力する仕様なので、あれば取得しておく
    export_uv_set = ''

    obj_long_name = cmds.ls(obj, l=True)[0]

    for bake_layer in active_bake_layers:
        if bake_setting.get_bake_type(bake_layer) == 2:  # 頂点カラーベイク
            continue
        if not cmds.sets(obj_long_name, im=bake_layer):
            continue
        export_uv_set = bake_setting.get_texture_bake_uv(bake_layer)
        break

    # ここからUVセットの編集
    all_uv_sets = cmds.polyUVSet(obj, q=True, auv=True)

    if not all_uv_sets or len(all_uv_sets) < 2:
        return

    # ライトマップのUVセットを2番目と入れ替え
    if export_uv_set and export_uv_set in all_uv_sets:

        replace_uv_set = all_uv_sets[1]
        if replace_uv_set != export_uv_set:
            cmds.polyUVSet(obj, reorder=True, nuv=export_uv_set, uvSet=replace_uv_set)

    # 背景モデルでUVセット4以降を使うことはないので削除
    all_uv_sets = cmds.polyUVSet(obj, q=True, auv=True)
    for i, uv_set in enumerate(all_uv_sets):
        if i > 2:
            cmds.polyUVSet(obj, d=True, uvs=uv_set)


def trim_colorset(obj, active_bake_layers=[]):
    """必要なカラーセット以外を削除

    Args:
        obj (str): 対象オブジェクト
    """

    # ライトマップのカラーセットがあれば取得しておく
    export_color_set = ''

    obj_long_name = cmds.ls(obj, l=True)[0]

    for bake_layer in active_bake_layers:
        if not cmds.sets(obj_long_name, im=bake_layer):
            continue
        export_color_set = tool_utility.generate_bake_colorset_name(bake_layer)
        break

    # ここからカラーセットの編集
    all_colorsets = cmds.polyColorSet(obj, q=True, acs=True)

    if not all_colorsets:
        return

    # ベイクカラーセットがあればそれをカレントに
    if export_color_set and export_color_set in all_colorsets:
        cmds.polyColorSet(obj, ccs=True, cs=export_color_set)

    # カレント以外消去
    current_colorset = cmds.polyColorSet(obj, q=True, ccs=True)[0]
    for colorset in all_colorsets:
        if colorset != current_colorset:
            cmds.polyColorSet(obj, colorSet=colorset, delete=True)

    # カラーセット名を出力用にリネーム
    current_colorset = cmds.polyColorSet(obj, q=True, ccs=True)[0]

    if current_colorset != RESULT_COLORSET:
        cmds.polyColorSet(obj, rn=True, cs=current_colorset, nc=RESULT_COLORSET)
        cmds.polyColorSet(obj, ccs=True, cs=RESULT_COLORSET)


def setup_output_material(obj):
    """出力用マテリアルのセットアップ
    ツール文字列を除いた名前でカラーテクスチャが刺さったマテリアルを用意する

    Args:
        obj (str): 対象オブジェクト

    Returns:
        list: 出力用に作成されたノードリスト
    """

    # ここで作成されたノードは後で削除するので返す
    new_created_material_list = []

    shape = cmds.listRelatives(obj, s=True, f=True)[0] if cmds.listRelatives(obj, s=True) else None

    if shape is None:
        return new_created_material_list

    current_material_list = tool_utility.get_material_list([shape])

    # マテリアルごとにセットアップ
    for material in current_material_list:

        if material.find(tool_define.PREVIEW_MATERIAL_SUFFIX) < 0:
            continue

        material_members = tool_utility.get_material_member(material, obj)

        if not material_members:
            continue

        final_material_name = material.replace(tool_define.PREVIEW_MATERIAL_SUFFIX, '_')

        if not cmds.objExists(final_material_name):

            # 元マテリアルを取得(ベイク時にこの接続が作成されているはず)
            mul_div_node = cmds.listConnections('{}.color'.format(material), type='multiplyDivide')
            org_materials = cmds.listConnections(mul_div_node[0] + '.input2', type='lambert')
            new_final_material = None

            if org_materials:
                # 元マテリアルがあれば出力用に複製
                # lambert1のような特殊なノードは複製できないので、新規作成に流す
                try:
                    dup_material_nodes = cmds.duplicate(org_materials[0], n=final_material_name, un=True)
                    new_final_material = dup_material_nodes[0]
                    new_created_material_list.extend(dup_material_nodes)

                    final_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=new_final_material + 'SG')
                    cmds.connectAttr('{}.{}'.format(new_final_material, 'outColor'), '{}.{}'.format(final_sg, 'surfaceShader'))
                    new_created_material_list.append(final_sg)
                except Exception:
                    pass

            if not new_final_material:
                # なければ新規でランバートを作る
                new_final_material = tool_utility.create_material(final_material_name)
                new_created_material_list.append(new_final_material)

                shading_group = tool_utility.get_shading_group(new_final_material)
                new_created_material_list.append(shading_group)

        # マテリアルをセット
        shading_group = tool_utility.get_shading_group(final_material_name)
        cmds.sets(material_members, e=True, fe=shading_group)

    return new_created_material_list
