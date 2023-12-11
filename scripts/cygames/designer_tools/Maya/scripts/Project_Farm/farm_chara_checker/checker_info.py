# -*- coding: utf-8 -*-

# region import

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import str
except:
    pass

import os
import re

import maya.cmds as cmds
import maya.mel as mel

from ..base_common import utility as base_utility
from ..base_common import classes as base_class
from ..farm_common.utility import model_mesh_finder

from . import checker_param_item

# endregion


# region ファイル系

# ==================================================
def get_file_info(param_item, arg):
    """
    ファイル概要を取得
    """

    param_item.info_title = '【ファイル情報】'
    param_item.info_has_link_to_error_target = False

    # ------------------------------
    # ファイル名
    file_dict = _create_info_dict('ファイル名', [], [])
    file_dict['value_list'].append(param_item.main.chara_info.file_name)
    param_item.info_dict_list.append(file_dict)

    # ------------------------------
    # ディレクトリ
    dir_dict = _create_info_dict('ディレクトリ', [], ['フォルダの存在確認'])
    dir_dict['value_list'].append(param_item.main.chara_info.part_info.maya_root_dir_path)
    param_item.info_dict_list.append(dir_dict)

# endregion


# region モデル系

# ==================================================
def get_model_info(param_item, arg):
    """
    モデル概要を取得
    """

    param_item.info_title = '【モデル概要】'
    param_item.info_column_list = ['▼項目', '▼測定結果', '▼ステータス']
    param_item.info_has_link_to_error_target = False
    
    # ------------------------------
    # ポリゴン数
    poly_dict = _create_info_dict('ポリゴン総数', [], ['メッシュのポリゴン数確認'])
    poly_count = _count_poly(param_item)
    poly_dict['value_list'].append(poly_count)
    param_item.info_dict_list.append(poly_dict)

    # ------------------------------
    # ジョイント数
    joint_dict = _create_info_dict('ジョイント総数', [], ['ジョイントの総数確認'])

    cloth_joint_dict = _create_info_dict('クロスジョイント数', [], ['クロス系ジョイントの総数確認'])

    joint_count_dict = _count_joint(param_item, ['Sp_', 'Tail'])

    joint_dict['value_list'].append(joint_count_dict['all'])
    cloth_joint_dict['value_list'].append(joint_count_dict['cloth'])

    param_item.info_dict_list.append(joint_dict)
    param_item.info_dict_list.append(cloth_joint_dict)

# endregion


# region メッシュ系

# ==================================================
def get_mesh_info(param_item, arg):
    """
    メッシュ情報
    """

    param_item.info_title = '【メッシュ情報】'
    param_item.info_column_list = ['▼メッシュ名', '▼ポリゴン数', '▼ステータス']
    param_item.info_has_link_to_error_target = False
    link_check_label_list = [
        'メッシュの存在確認',
        '追加メッシュの存在確認',
        'メッシュのポリゴン数確認',
        'メッシュの移動、回転、スケール確認',
    ]

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    for mesh in target_mesh_list:
        short_name = mesh.split('|')[-1]

        this_mesh_dict = _create_info_dict(short_name, [], link_check_label_list)

        # ポリゴン数
        this_mesh_dict['value_list'].append(cmds.polyEvaluate(mesh, triangle=True))

        param_item.info_dict_list.append(this_mesh_dict)

# endregion


# region テクスチャ系

# ==================================================
def get_texture_info(param_item, arg):
    """
    テクスチャ情報
    """

    param_item.info_title = '【テクスチャ情報】'
    param_item.info_column_list = ['▼テクスチャ名', '▼解像度', '▼ステータス']
    param_item.info_has_link_to_error_target = True
    link_check_label_list = [
        'テクスチャの存在確認',
        '追加テクスチャの存在確認',
        'テクスチャのサイズ確認',
    ]

    target_texture_param_list = None

    target_texture_param_list = param_item.main.chara_info.part_info.all_texture_param_list

    if not target_texture_param_list:
        return

    temp_file_node = cmds.shadingNode(
        'file', asTexture=True, name='temp_file_node')

    for texture_param in target_texture_param_list:

        if not texture_param['check']:
            continue

        texture_name = texture_param['name']

        this_tex_dict = _create_info_dict(texture_name, [], link_check_label_list)

        texture_path = param_item.main.chara_info.part_info.maya_sourceimages_dir_path + \
            '/' + texture_name

        param_item.check_target_list.append(texture_path)

        if not os.path.isfile(texture_path):

            this_tex_dict['value_list'].append('テクスチャがありません')
            param_item.info_dict_list.append(this_tex_dict)
            continue

        cmds.setAttr(temp_file_node + '.fileTextureName', texture_path, type='string')

        this_tex_size = [0, 0]
        if cmds.objExists(temp_file_node) and cmds.attributeQuery('outSize', node=temp_file_node, exists=True):
            this_tex_size = cmds.getAttr('{}.{}'.format(temp_file_node, 'outSize'))[0]

        this_tex_dict['value_list'].append(str(this_tex_size).replace(',', '*'))

        param_item.info_dict_list.append(this_tex_dict)

    cmds.delete(temp_file_node)

# endregion


# region マテリアル系

# ==================================================
def get_material_info(param_item, arg):
    """
    マテリアル情報
    """

    param_item.info_title = '【マテリアル情報】'
    param_item.info_column_list = ['▼マテリアル名', '▼存在しているか', '▼ステータス']
    param_item.info_has_link_to_error_target = True
    link_check_label_list = ['マテリアル存在確認', '追加マテリアル存在確認']

    target_material_param_list = param_item.main.chara_info.part_info.material_param_list

    if not target_material_param_list:
        return

    for material_param in target_material_param_list:

        if not material_param['check']:
            continue

        material = material_param['name']

        this_mat_dict = _create_info_dict(material, [], link_check_label_list)

        if material and cmds.objExists(material):
            if cmds.ls(material, typ=['lambert']):
                this_mat_dict['value_list'].append('〇')
                param_item.info_dict_list.append(this_mat_dict)
                continue

        this_mat_dict['value_list'].append('×')
        param_item.info_dict_list.append(this_mat_dict)

# endregion


# region プライベートメソッド

# ==================================================
def _create_info_dict(item=None, value_list=[], link_check_label_list=[]):
    """
    各行を形成するinfo_dictのひな形を作成
    item: 1列目に来る見出し
    value_list: 2列目以降の値の配列
    link_check_label_list: エラーチェック対象のラベル名の配列
    """

    info_dict = {
        'item': item,
        'value_list': value_list,
        'link_check_label_list': link_check_label_list,
    }

    return info_dict


# ==================================================
def _count_poly(param_item):
    """
    ポリゴン数のチェック
    """

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    poly_count = 0

    for mesh in target_mesh_list:
        this_count = cmds.polyEvaluate(mesh, triangle=True)

        poly_count += this_count

    return poly_count


# ==================================================
def _count_joint(param_item, cloth_filter_list):
    """
    ジョイントの数をチェック
    """

    result_dict = {'all': 0, 'cloth': 0, 'no_cloth': 0}

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return result_dict
    
    if not cmds.objExists(root_node):
        return result_dict

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return result_dict

    for joint in all_joint_list:

        if not cmds.objExists(joint):
            continue

        joint_name = joint.split('|')[-1]

        result_dict['all'] += 1

        # クロス判定
        is_cloth = False
        if cloth_filter_list:

            for this_filter in cloth_filter_list:

                if re.search(this_filter, joint_name):
                    is_cloth = True
                    result_dict['cloth'] += 1
                    break

        if is_cloth:
            continue

        result_dict['no_cloth'] += 1

    return result_dict

# endregion
