# -*- coding: utf-8 -*-

# region import

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
    from importlib import reload
except:
    pass

import os
import re
import math
import itertools

import maya.cmds as cmds
import maya.mel as mel

from ..base_common import utility as base_utility
from ..base_common import classes as base_class

from .. import farm_common
from ..farm_common import classes as farm_class
from ..farm_common import utility as farm_utility
from ..farm_common.utility import model_define
from ..farm_common.utility import model_id_finder
from ..farm_common.utility import model_mesh_finder
from ..farm_common.classes.info import chara_info

from . import checker_param_item

reload(farm_common)
reload(checker_param_item)

# endregion

CLOTH_JOINT_PREFIX_LIST = ['Sp_', 'Ex_', 'Tp_']
CLOTH_JOINT_LIST = ['Tail'] + CLOTH_JOINT_PREFIX_LIST
CLOTH_JOINT_PARENT_DICT = {
    'Ne': 'Neck',
    'Ch': 'Chest',
    'Wa': 'Waist',
    'Hi': 'Hip',
    'Th': 'Thigh',
    'Kn': 'Knee',
    'An': 'Ankle',
    'Sh': 'Shoulder',
    'Ar': 'Arm',
    'El': 'Elbow',
    'Wr': 'Wrist',
    'Si': 'Spine',
    'So': 'ShoulderRoll',
    'Ao': 'ArmRoll',
    'He': 'Head',
}

# region パス系


# ==================================================
def check_directory_exist(param_item, arg):
    """
    ディレクトリが存在するかのチェック
    """

    # ------------------------------
    # 情報

    target_param_list = param_item.main.chara_info.part_info.maya_dir_param_list
    root_dir = param_item.main.chara_info.part_info.maya_root_dir_path

    for param in target_param_list:
        if param['check']:
            param_item.info_target_list.append(root_dir + '/' + param['name'])

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    target_param_list = param_item.main.chara_info.part_info.maya_dir_param_list

    for param in target_param_list:
        if param['check']:
            param_item.info_target_list.append(root_dir + '/' + param['name'])

    for path in param_item.check_target_list:

        if os.path.isdir(path):
            param_item.unerror_target_list.append(path)
            continue

        param_item.error_target_list.append(path)

# endregion

# region メッシュ系


# ==================================================
def check_mesh_exist(param_item, arg):
    """
    メッシュの存在確認
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        if mesh_param['check']:
            target_mesh_list.append(mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    for mesh in target_mesh_list:

        if mesh and cmds.objExists(mesh):
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_naming_rule(param_item, arg):
    """
    メッシュの命名規則の確認
    """

    # ------------------------------
    # 前提条件

    # 命名規則が取得できない場合は処理しない
    if not param_item.main.chara_info.part_info.mesh_naming_rule_list:
        return

    # ------------------------------
    # 設定

    target_mesh_list = []

    transform_list = cmds.ls(l=True, typ='transform')

    if not transform_list:
        return

    for transform in transform_list:
        mesh_list = cmds.listRelatives(transform, typ='mesh', ni=True)

        if not mesh_list:
            continue

        target_mesh_list.append(transform)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    naming_rule = param_item.main.chara_info.part_info.mesh_naming_rule_list[0]
    pattern = re.compile(naming_rule)

    for mesh in target_mesh_list:
        if pattern.match(mesh):
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_name_overlap(param_item, arg):
    """
    メッシュ名の重複確認
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    for mesh in target_mesh_list:

        mesh_short_name = mesh.split('|')[-1]

        exist = False

        for diff_mesh in target_mesh_list:

            if diff_mesh == mesh:
                continue

            diff_mesh_short_name = diff_mesh.split('|')[-1]

            if diff_mesh_short_name == mesh_short_name:
                exist = True
                break

        if not exist:
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_poly_count(param_item, arg):
    """
    メッシュのポリゴン数をチェック
    """

    target_poly_count = 10000
    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        target_poly_count = 6500
    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        # Max12000から今の尻尾の388を除いた残りを上限とする
        target_poly_count = 11612
    elif param_item.main.chara_info.part_info.data_type.find('prop') >= 0:
        target_poly_count = 3000

    target_mesh_list = []

    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        if not cmds.objExists(mesh_param['name']):
            continue
        target_mesh_list.append(mesh_param['name'])

    target_mesh_list = __get_poly_check_mesh_list(target_mesh_list)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    is_in_limit, all_tri_count, this_tri_limit = __check_mesh_poly_count_base(
        target_mesh_list, target_poly_count
    )
    param_item.check_target_list.extend(target_mesh_list)

    over_count = 'NO_DATA'
    if all_tri_count:
        over_count = all_tri_count - this_tri_limit

    # param_itemのターゲットリストの値で判定、一旦tmpに入れる
    if not is_in_limit:
        param_item.error_target_list.append(
            '{}/{} tris: {} tris over'.format(all_tri_count, this_tri_limit, over_count)
        )
    else:
        param_item.unerror_target_list.append(
            '{}/{} tris'.format(all_tri_count, this_tri_limit)
        )


# ==================================================
def check_mesh_poly_sum_count(param_item, arg):
    """
    頭、身体、尻尾の合算ポリ数チェック
    """

    # 頭、身体、尻尾の合算上限
    target_sum_poly_min_count = 18500

    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        check_mesh_poly_sum_count_from_head(param_item, target_sum_poly_min_count, arg)

    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        check_mesh_poly_sum_count_from_body(param_item, target_sum_poly_min_count, arg)


# ==================================================
def check_mesh_poly_sum_count_from_head(param_item, target_sum_poly_min_count, arg):
    """
    ユニーク頭部から各身体との合算ポリ数をチェック
    """

    # ------------------------------
    # 設定

    # 対応しうる身体を検索
    target_body_file_list = []

    body_finder = farm_class.path_finder.path_finder.PathFinder('body', param_item.main.chara_info.data_main_id)

    if not body_finder.model_ma_list:
        return

    for model_suggest in body_finder.model_ma_list:
        if os.path.exists(model_suggest):
            target_body_file_list.append(model_suggest)

    if not target_body_file_list:
        return

    # 身体ごとにチェック用の辞書を作成
    check_dict_list = []
    for target_body_file in target_body_file_list:

        check_dict = {
            'head_part_info': None,
            'head_path': '',
            'body_part_info': None,
            'body_path': '',
            'tail_part_info': None,
            'tail_path': '',
            'info_str': ''
        }

        tmp_info_body = farm_common.classes.info.chara_info.CharaInfo()
        tmp_info_body.create_info(target_body_file, '', True)

        if not tmp_info_body.part_info or not tmp_info_body.tail_part_info:
            continue

        check_dict['head_part_info'] = param_item.main.chara_info.part_info
        check_dict['body_part_info'] = tmp_info_body.part_info
        check_dict['tail_part_info'] = tmp_info_body.tail_part_info

        body_finder = farm_class.path_finder.path_finder.PathFinder('body', '{}_{}'.format(check_dict['body_part_info'].main_id, check_dict['body_part_info'].sub_id))
        tail_finder = farm_class.path_finder.path_finder.PathFinder('tail', '{}_{}'.format(check_dict['tail_part_info'].main_id, check_dict['tail_part_info'].sub_id))

        if not body_finder.model_ma_list or not tail_finder.model_ma_list:
            continue

        check_dict['head_path'] = cmds.file(q=True, sn=True)
        check_dict['body_path'] = body_finder.model_ma_list[0]
        check_dict['tail_path'] = tail_finder.model_ma_list[0]

        if not os.path.exists(check_dict['head_path']) or\
            not os.path.exists(check_dict['body_path']) or\
                not os.path.exists(check_dict['tail_path']):
            continue

        head_file_name = os.path.basename(check_dict['head_path'])
        body_file_name = os.path.basename(check_dict['body_path'])
        tail_file_name = os.path.basename(check_dict['tail_path'])

        check_dict['info_str'] = '{}, {}, {}'.format(head_file_name, body_file_name, tail_file_name)

        check_dict_list.append(check_dict)

    body_ref_name_space = '__BODY_MODEL_REF__'
    tail_ref_name_space = '__TAIL_MODEL_REF__'

    # ------------------------------
    # 情報

    if not check_dict_list:
        return

    for check_dict in check_dict_list:
        param_item.info_target_list.append(check_dict['info_str'])

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for check_dict in check_dict_list:

        head_mesh_list = check_dict['head_part_info'].mesh_list[:]
        body_mesh_list = check_dict['body_part_info'].mesh_list[:]
        tail_mesh_list = check_dict['tail_part_info'].mesh_list[:]

        final_mesh_list = head_mesh_list[:]

        for body_mesh in body_mesh_list:
            final_mesh_list.append(body_mesh.replace('|', '|{}:'.format(body_ref_name_space)))
        for tail_mesh in tail_mesh_list:
            final_mesh_list.append(tail_mesh.replace('|', '|{}:'.format(tail_ref_name_space)))

        final_mesh_list = __get_poly_check_mesh_list(final_mesh_list)

        # ロード/失敗したらエラーで返す
        base_utility.reference.load(check_dict['body_path'], body_ref_name_space)
        base_utility.reference.load(check_dict['tail_path'], tail_ref_name_space)

        if not base_utility.reference.exists(check_dict['body_path'], body_ref_name_space) or\
                not base_utility.reference.exists(check_dict['tail_path'], tail_ref_name_space):
            base_utility.reference.unload(check_dict['body_path'], body_ref_name_space)
            base_utility.reference.unload(check_dict['tail_path'], tail_ref_name_space)
            param_item.error_target_list.append('{} or {} (REFERENCE ERROR)'.format(check_dict['body_path'], check_dict['tail_path']))
            continue

        # チェック
        is_in_limit, all_tri_count, this_tri_limit = __check_mesh_poly_count_base(
            final_mesh_list, target_sum_poly_min_count
        )
        param_item.check_target_list.append(check_dict['info_str'])

        # アンロード
        base_utility.reference.unload(check_dict['body_path'], body_ref_name_space)
        base_utility.reference.unload(check_dict['tail_path'], tail_ref_name_space)

        # チェック結果の記載
        over_count = 'NO_DATA'
        if all_tri_count:
            over_count = all_tri_count - this_tri_limit

        if not is_in_limit:
            param_item.error_target_list.append(
                '{} ({}/{} tris: {} tris over)'.format(check_dict['info_str'], all_tri_count, this_tri_limit, over_count)
            )
        else:
            param_item.unerror_target_list.append(
                '{} ({}/{} tris)'.format(check_dict['info_str'], all_tri_count, this_tri_limit)
            )


# ==================================================
def check_mesh_poly_sum_count_from_body(param_item, target_sum_poly_min_count, arg):
    """
    特別衣装における頭、身体、尻尾の合算ポリ数チェック
    """

    # ------------------------------
    # 設定

    check_dict = {
        'head_part_info': None,
        'head_path': '',
        'body_part_info': None,
        'body_path': '',
        'tail_part_info': None,
        'tail_path': '',
        'info_str': ''
    }

    check_dict['body_part_info'] = param_item.main.chara_info.part_info

    if not check_dict['body_part_info'].data_type == 'body' or not check_dict['body_part_info'].is_unique_chara:
        return

    check_dict['head_part_info'] = param_item.main.chara_info.head_part_info
    check_dict['tail_part_info'] = param_item.main.chara_info.tail_part_info

    if not check_dict['head_part_info'] or not check_dict['tail_part_info']:
        return

    head_finder = farm_class.path_finder.path_finder.PathFinder('head', '{}_{}'.format(check_dict['head_part_info'].main_id, check_dict['head_part_info'].sub_id))
    tail_finder = farm_class.path_finder.path_finder.PathFinder('tail', '{}_{}'.format(check_dict['tail_part_info'].main_id, check_dict['tail_part_info'].sub_id))

    if not head_finder.model_ma_list or not tail_finder.model_ma_list:
        return

    check_dict['body_path'] = cmds.file(q=True, sn=True)
    check_dict['head_path'] = head_finder.model_ma_list[0]
    check_dict['tail_path'] = tail_finder.model_ma_list[0]

    if not os.path.exists(check_dict['head_path']) or not os.path.exists(check_dict['tail_path']):
        return

    head_file_name = os.path.basename(check_dict['head_path'])
    body_file_name = os.path.basename(check_dict['body_path'])
    tail_file_name = os.path.basename(check_dict['tail_path'])

    check_dict['info_str'] = '{}, {}, {}'.format(head_file_name, body_file_name, tail_file_name)

    head_ref_name_space = '__HEAD_MODEL_REF__'
    tail_ref_name_space = '__TAIL_MODEL_REF__'

    # ------------------------------
    # 情報

    param_item.info_target_list.append(check_dict['info_str'])

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.append(check_dict['info_str'])

    head_mesh_list = check_dict['head_part_info'].mesh_list[:]
    body_mesh_list = check_dict['body_part_info'].mesh_list[:]
    tail_mesh_list = check_dict['tail_part_info'].mesh_list[:]

    final_mesh_list = body_mesh_list[:]

    for head_mesh in head_mesh_list:
        final_mesh_list.append(head_mesh.replace('|', '|{}:'.format(head_ref_name_space)))
    for tail_mesh in tail_mesh_list:
        final_mesh_list.append(tail_mesh.replace('|', '|{}:'.format(tail_ref_name_space)))

    final_mesh_list = __get_poly_check_mesh_list(final_mesh_list)

    # ロード/失敗したらエラーで返す
    base_utility.reference.load(check_dict['head_path'], head_ref_name_space)
    base_utility.reference.load(check_dict['tail_path'], tail_ref_name_space)

    if not base_utility.reference.exists(check_dict['head_path'], head_ref_name_space) or\
            not base_utility.reference.exists(check_dict['tail_path'], tail_ref_name_space):

        base_utility.reference.unload(check_dict['head_path'], head_ref_name_space)
        base_utility.reference.unload(check_dict['tail_path'], tail_ref_name_space)
        param_item.error_target_list.append('{} or {} (REFERENCE ERROR)'.format(check_dict['head_path'], check_dict['tail_path']))
        return

    # チェック
    is_in_limit, all_tri_count, this_tri_limit = __check_mesh_poly_count_base(
        final_mesh_list, target_sum_poly_min_count
    )
    param_item.check_target_list.append(check_dict['info_str'])

    # アンロード
    base_utility.reference.unload(check_dict['head_path'], head_ref_name_space)
    base_utility.reference.unload(check_dict['tail_path'], tail_ref_name_space)

    over_count = 'NO_DATA'
    if all_tri_count:
        over_count = all_tri_count - this_tri_limit

    # チェック結果の記載
    if not is_in_limit:
        param_item.error_target_list.append(
            '{} ({}/{} tris: {} tris over)'.format(check_dict['info_str'], all_tri_count, this_tri_limit, over_count)
        )
    else:
        param_item.unerror_target_list.append(
            '{} ({}/{} tris)'.format(check_dict['info_str'], all_tri_count, this_tri_limit)
        )


# ==================================================
def __get_poly_check_mesh_list(target_mesh_list):
    """
    ポリゴン数のチェック対象のメッシュのみを返す
    """

    poly_check_mesh_list = []

    if not target_mesh_list:
        return []

    for mesh in target_mesh_list:

        if mesh.find('Outline') >= 0:
            continue

        poly_check_mesh_list.append(mesh)

    return poly_check_mesh_list


# ==================================================
def __check_mesh_poly_count_base(target_mesh_list, target_poly_min_count):
    """
    メッシュのポリゴン数をチェック
    """

    is_in_limit = False
    all_tri_count = 0
    count_limit = target_poly_min_count

    if not target_mesh_list:
        return is_in_limit, all_tri_count, count_limit

    if not target_poly_min_count:
        return is_in_limit, all_tri_count, count_limit

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        this_count = cmds.polyEvaluate(mesh, triangle=True)

        all_tri_count += this_count

    if all_tri_count <= target_poly_min_count:
        is_in_limit = True

    return is_in_limit, all_tri_count, count_limit


# ==================================================
def check_mesh_transform(param_item, arg):
    """
    メッシュのトランスフォーム情報をチェック
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        param_item.check_target_list.append(mesh)

        translate = None
        rotate = None
        scale = None
        if cmds.objExists(mesh):
            if cmds.attributeQuery('translate', node=mesh, exists=True):
                translate = cmds.getAttr('{}.{}'.format(mesh, 'translate'))[0]

            if cmds.attributeQuery('rotate', node=mesh, exists=True):
                rotate = cmds.getAttr('{}.{}'.format(mesh, 'rotate'))[0]

            if cmds.attributeQuery('scale', node=mesh, exists=True):
                scale = cmds.getAttr('{}.{}'.format(mesh, 'scale'))[0]

        is_hit = False

        if not base_utility.vector.is_same(
            translate, [0, 0, 0]
        ):
            is_hit = True

        if not base_utility.vector.is_same(
            rotate, [0, 0, 0]
        ):
            is_hit = True

        if not base_utility.vector.is_same(
            scale, [1, 1, 1]
        ):
            is_hit = True

        if not is_hit:
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_material_type(param_item, arg):
    """
    マテリアルの種類の確認
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        # メッシュからマテリアル取得
        material_list = base_utility.material.get_material_list(mesh)

        if not material_list:

            param_item.error_target_list.append(mesh)

            continue

        for material in material_list:

            # マテリアルの種類をチェック
            if not cmds.objectType(material, i='lambert'):

                param_item.error_target_list.append(mesh)

                break

        if mesh in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(mesh)


# ==================================================
def check_mesh_shape_name(param_item, arg):
    """
    shapeノードの名前がtransformノード+Shapeになっているか
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    root = param_item.main.chara_info.part_info.root_node
    transform_list = cmds.listRelatives(root, ad=True, f=True, typ='transform')

    if not transform_list:
        return

    # 子供にmeshノードを持つtransformがターゲット
    for transform in transform_list:
        shape_list = cmds.listRelatives(transform, f=True, ni=True, s=True)

        if not shape_list:
            continue

        for shape in shape_list:
            if cmds.objectType(shape) == 'mesh':
                target_mesh_list.append(transform)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    for mesh in target_mesh_list:

        if not cmds.objExists(mesh):
            continue

        short_name = mesh.split('|')[-1]
        shape_list = cmds.listRelatives(mesh, f=True, ni=True, s=True)

        if not shape_list:
            continue
        else:
            if shape_list[0].split('|')[-1] == short_name + 'Shape':
                param_item.unerror_target_list.append(mesh)
            else:
                param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_intermeditate_count(param_item, arg):
    """
    origノードが複数ないかのチェック
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    root = param_item.main.chara_info.part_info.root_node
    transform_list = cmds.listRelatives(root, ad=True, f=True, typ='transform')

    if not transform_list:
        return

    # 子供にmeshノードを持つtransformがターゲット
    for transform in transform_list:
        shape_list = cmds.listRelatives(transform, f=True, ni=True, s=True)

        if not shape_list:
            continue

        for shape in shape_list:
            if cmds.objectType(shape) == 'mesh':
                target_mesh_list.append(transform)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    for mesh in target_mesh_list:

        if not cmds.objExists(mesh):
            continue

        shape_list = cmds.listRelatives(mesh, f=True, s=True)

        if not shape_list:
            continue

        intermeditate_count = 0

        for shape in shape_list:

            short_name = shape.split('|')[-1]

            if short_name.find('Orig') >= 0:
                intermeditate_count += 1

        if intermeditate_count >= 2:
            param_item.error_target_list.append(mesh)
        else:
            param_item.unerror_target_list.append(mesh)


# ==================================================
def check_mesh_intermediate_name(param_item, arg):
    """
    中間ノードの名前チェック
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:
        shape_list = cmds.listRelatives(mesh, f=True, s=True)

        intermediate_list = []

        for shape in shape_list:
            shape_io = None
            if cmds.objExists(shape) and cmds.attributeQuery('io', node=shape, exists=True):
                shape_io = cmds.getAttr('{}.{}'.format(shape, 'io'))

            if shape_io:
                intermediate_list.append(shape)

        # 中間ノードの数は他の項目でチェックするので1つの場合のみ処理
        if not len(intermediate_list) == 1:
            continue

        param_item.check_target_list.append(mesh)

        mesh_short_name = mesh.split('|')[-1]
        target_short_name = intermediate_list[0].split('|')[-1]

        if target_short_name == mesh_short_name + 'ShapeOrig':
            param_item.unerror_target_list.append(mesh)
        else:
            param_item.error_target_list.append(mesh)


# ==================================================
def check_neck_edge_set_exists(param_item, arg):
    """
    NeckEdgeSetが存在するかどうか
    """

    # ------------------------------
    # 設定

    neck_edge_set_name = 'NeckEdgeSet'

    # ------------------------------
    # 情報

    param_item.info_target_list.append(neck_edge_set_name)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    param_item.check_target_list.append(neck_edge_set_name)

    for check_target in param_item.check_target_list:
        if cmds.objExists(check_target):
            param_item.unerror_target_list.append(check_target)
        else:
            param_item.error_target_list.append(check_target)


# ==================================================
def check_neck_edge_normals(param_item, arg):
    """
    NeckEdgeSetの法線方向をチェック
    """

    # ------------------------------
    # 設定

    neck_edge_set_name = 'NeckEdgeSet'

    neck_normal_info = farm_class.neck_normal.NeckNormalInfo()

    # ------------------------------
    # 情報

    neck_edge_list = []
    if not cmds.objExists(neck_edge_set_name):
        return

    neck_edge_list = cmds.ls(cmds.sets(neck_edge_set_name, q=True), fl=True)
    if not neck_edge_list:
        return

    vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)
    if not vertices:
        return

    param_item.info_target_list.extend(vertices)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(neck_edge_list)

    select_list = cmds.ls(sl=True, l=True, fl=True)
    cmds.select(cmds.sets(neck_edge_set_name, q=True))
    neck_normal_info.update_neck_edge_list_from_selected_edge()

    neck_normal_info.update_neck_vertex_info()
    neck_vertex_info_list = neck_normal_info.neck_vertex_info_list

    if not neck_vertex_info_list:
        param_item.error_target_list.extend(neck_edge_list)
        cmds.select(select_list, r=True)
        return

    for vtx in vertices:

        is_error = False

        for this_info in neck_vertex_info_list:

            this_info_vtx = this_info[2]
            this_info_index = this_info[4]

            if this_info_vtx != vtx:
                continue

            neck_normal_list = neck_normal_info.neck_default_normal_list
            if vtx.find('_Outline') > -1:
                neck_normal_list = neck_normal_info.neck_outline_normal_list

            neck_normals = neck_normal_list[this_info_index]
            normals = cmds.polyNormalPerVertex(vtx, q=True, xyz=True)
            is_rock = cmds.polyNormalPerVertex(vtx, q=True, allLocked=True)[0]

            if not is_rock:
                is_error = True

            if round(neck_normals[0], 5) != round(normals[0], 5) \
                or round(neck_normals[1], 5) != round(normals[1], 5) \
                    or round(neck_normals[2], 5) != round(normals[2], 5):
                is_error = True

            break

        else:

            is_error = True

        cmds.select(select_list, r=True)

        if is_error:
            param_item.error_target_list.append(vtx)
        else:
            param_item.unerror_target_list.append(vtx)


# ==================================================
def check_neck_edge_vtx_colors(param_item, arg):
    """
    NeckEdgeSetの頂点カラーをチェック
    """

    # ------------------------------
    # 設定

    neck_edge_set_name = 'NeckEdgeSet'

    # ------------------------------
    # 情報

    neck_edge_list = []
    if not cmds.objExists(neck_edge_set_name):
        return

    neck_edge_list = cmds.ls(cmds.sets(neck_edge_set_name, q=True), fl=True)
    if not neck_edge_list:
        return

    vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)
    if not vertices:
        return

    param_item.info_target_list.extend(vertices)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(vertices)

    for vtx in vertices:

        color_vtx = cmds.polyColorPerVertex(vtx, q=True, colorRGB=True)

        if [1, 1, 1] != color_vtx:
            param_item.error_target_list.append(vtx)
        else:
            param_item.unerror_target_list.append(vtx)


# ==================================================
def check_neck_edge_weight(param_item, arg):
    """
    NeckEdgeSetのweightをチェック
    """

    # ------------------------------
    # 設定

    neck_edge_set_name = 'NeckEdgeSet'

    # ------------------------------
    # 情報

    neck_edge_list = []
    if not cmds.objExists(neck_edge_set_name):
        return

    neck_edge_list = cmds.ls(cmds.sets(neck_edge_set_name, q=True), fl=True)
    if not neck_edge_list:
        return

    vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)
    if not vertices:
        return

    param_item.info_target_list.extend(vertices)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(vertices)

    dst_weight_data_list = [['Head', 0.7], ['Neck', 0.3]]

    for vtx in vertices:

        mesh_name = vtx.split('.')[0]

        skin_cluster = base_utility.mesh.skin.get_skin_cluster(mesh_name)

        is_error = False

        if skin_cluster:

            src_weight_joint_list = cmds.skinPercent(skin_cluster, vtx, ignoreBelow=0.001, q=True, transform=None)
            src_weight_weight_value_list = cmds.skinPercent(skin_cluster, vtx, ignoreBelow=0.001, q=True, value=True)

            for src_joint_full_name, src_joint_weight in zip(src_weight_joint_list, src_weight_weight_value_list):

                src_joint_name = src_joint_full_name.split('|')[-1]

                for dst_weight_data in dst_weight_data_list:

                    dst_joint_name = dst_weight_data[0]
                    if src_joint_name != dst_joint_name:
                        continue

                    dst_joint_weight = dst_weight_data[1]
                    if round(src_joint_weight, 3) != round(dst_joint_weight, 3):
                        continue

                    break

                else:

                    is_error = True
                    break

        else:

            is_error = True

        if is_error:
            param_item.error_target_list.append(vtx)
        else:
            param_item.unerror_target_list.append(vtx)

# endregion

# region クリーンアップ系


# ==================================================
def check_mesh_cleanup(param_item, arg):
    """
    メッシュのクリーンアップ状態をチェック
    """

    # ------------------------------
    # 設定

    cleanup_type = arg[0]

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    this_target_list = []
    this_error_target_list = []
    this_unerror_target_list = []

    # 対象の確定
    for mesh in target_mesh_list:

        if cleanup_type == 'nonmanifold':
            target_list = base_utility.mesh.get_vertex_list(mesh)
        elif cleanup_type == 'zero_edge':
            target_list = base_utility.mesh.get_edge_list(mesh)
        else:
            target_list = base_utility.mesh.get_face_list(mesh)

        if not target_list:
            continue

        this_target_list.extend(target_list)

    # エラーチェック
    if cleanup_type == 'more4side':

        this_error_target_list = \
            base_utility.mesh.cleanup.check_face_with_more_4side(
                this_target_list, False
            )

    elif cleanup_type == 'concave':

        this_error_target_list = \
            base_utility.mesh.cleanup.check_concave_face(
                this_target_list, False
            )

    elif cleanup_type == 'hole':

        this_error_target_list = \
            base_utility.mesh.cleanup.check_face_with_hole(
                this_target_list, False
            )

    elif cleanup_type == 'lamina':

        this_error_target_list = \
            base_utility.mesh.cleanup.check_lamina_face(
                this_target_list, False
            )

    elif cleanup_type == 'nonmanifold':

        this_error_target_list = \
            base_utility.mesh.cleanup.check_nonmanifold(
                this_target_list, False
            )

    elif cleanup_type == 'zero_edge':

        this_error_target_list = \
            base_utility.mesh.cleanup.check_zero_edge(
                this_target_list, False
            )

    # エラー外のチェック
    for target in this_target_list:

        if this_error_target_list:

            if target in this_error_target_list:
                continue

        this_unerror_target_list.append(target)

    # 割り当て
    if this_target_list:
        param_item.check_target_list = this_target_list

    if this_error_target_list:
        param_item.error_target_list = this_error_target_list

    if this_unerror_target_list:
        param_item.unerror_target_list = this_unerror_target_list

# endregion

# region 頂点カラー系


# ==================================================
def check_mesh_vertex_color_round(param_item, arg):
    """
    頂点カラーの桁数チェック
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    # 対象の確定
    for mesh in target_mesh_list:

        target_list = base_utility.mesh.get_vertex_list(mesh)

        if not target_list:
            continue

        param_item.check_target_list.extend(target_list)

    vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
    vtxcolor_info.create_info(param_item.check_target_list)

    this_vertex_list = \
        base_utility.mesh.vertex_color.get_vertex_list_with_unround_color(
            vtxcolor_info, 2)

    if this_vertex_list:

        param_item.error_target_list.extend(
            this_vertex_list
        )

    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_mesh_unshared_vertex_color(param_item, arg):
    """
    頂点カラーがUnsharedかどうかのチェック
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    separator = param_item.root.info_window.detail_separator

    # 対象の確定
    for mesh in target_mesh_list:
        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        colorsets = base_utility.mesh.colorset.get_colorset_list(mesh)

        if not colorsets:
            continue

        current_colorset = base_utility.mesh.colorset.get_current(mesh)

        for colorset in colorsets:
            base_utility.mesh.colorset.set_current(mesh, colorset)
            vtx_color_info_list = \
                base_utility.mesh.vertex_color.get_all_vertex_color_info_list(
                    mesh)

            if not vtx_color_info_list:
                continue

            sorted_list = sorted(vtx_color_info_list, key=lambda i: i[0])
            groups = itertools.groupby(sorted_list, lambda i: i[0])

            for index, group in [(i, list(g)) for i, g in groups]:
                if len(group) < 2:
                    continue

                is_same_color = True

                first_vtx_color = group[0][2]

                for vtx_color_info in group:
                    vtx_color = vtx_color_info[2]

                    color_threshold = 0.001
                    if any([float(abs(x - y)) >= color_threshold for (x, y) in zip(first_vtx_color, vtx_color)]):
                        is_same_color = False
                        break

                if is_same_color:
                    continue

                error_message = '{0}.vtx[{1}]'.format(mesh, str(index))

                param_item.error_target_list.append(
                    error_message + separator + colorset)

        base_utility.mesh.colorset.set_current(mesh, current_colorset)

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_mesh_vertex_color_alpha(param_item, arg):
    """
    頂点カラーのアルファ値チェック
    アルファに1以外が入っている場合はエラー
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    separator = param_item.root.info_window.detail_separator

    for mesh in target_mesh_list:
        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        colorsets = base_utility.mesh.colorset.get_colorset_list(mesh)

        if not colorsets:
            continue

        current_colorset = base_utility.mesh.colorset.get_current(mesh)

        for colorset in colorsets:
            base_utility.mesh.colorset.set_current(mesh, colorset)
            vtx_color_info_list = \
                base_utility.mesh.vertex_color.get_all_vertex_color_info_list(
                    mesh)

            if not vtx_color_info_list:
                continue

            for vtx_color_info in vtx_color_info_list:

                this_index = vtx_color_info[0]
                this_alpha = vtx_color_info[2][3]

                if this_alpha == 1:
                    continue

                error_message = '{0}.vtx[{1}]'.format(mesh, str(this_index))

                param_item.error_target_list.append(
                    error_message + separator + colorset)

        base_utility.mesh.colorset.set_current(mesh, current_colorset)

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_mesh_vertex_color_noisy(param_item, arg):
    """
    頂点カラーのブレチェック
    頂点カラーの各色は0か1ぴったりで入力されることが多いが
    0.04や0.96など、微妙にぶれているのはエラーとして検出する
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    noise = 0.05

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        vtx_color_info_list = base_utility.mesh.vertex_color.get_all_vertex_color_info_list(
            mesh)

        if not vtx_color_info_list:
            continue

        for vtx_color_info in vtx_color_info_list:

            colors_noisy = []

            for color in vtx_color_info[2][:3]:
                if 1 - noise > color > 0 + noise:
                    continue
                colors_noisy.append(color)

            if not colors_noisy:
                continue

            colors_error = []

            for color in colors_noisy:
                if color == 1 or color == 0:
                    continue
                colors_error.append(color)

            if not colors_error:
                continue

            param_item.error_target_list.append(
                vertex_list[vtx_color_info[0]])

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_mesh_colorset(param_item, arg):
    """
    カラーセット数の確認
    カラーセット数が2以上でエラー。faceのみ3以上でエラー
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        param_item.check_target_list.append(mesh)

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            mesh)

        color_set_limit = 1

        # faceのみカラーセットを2つ持つ
        if mesh.split('|')[-1].startswith('msh_face'):
            color_set_limit = 2

        if not colorset_list or len(colorset_list) <= color_set_limit:
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(
            mesh
        )

# endregion

# region ウェイト系


# ==================================================
def check_mesh_skin_influence(param_item, arg):
    """
    インフルエンス数が2以内かの確認
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        if not base_utility.mesh.skin.get_skin_cluster(mesh):
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        skin_info = base_class.mesh.skin_info.SkinInfo()
        skin_info.create_info([mesh])

        this_vertex_list = \
            base_utility.mesh.skin.get_vertex_list_with_over_influence(
                skin_info, 2)

        if this_vertex_list:

            param_item.error_target_list.extend(
                this_vertex_list
            )

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_mesh_skin_round(param_item, arg):
    """
    ウェイト精度少数2桁以内かの確認
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        if not base_utility.mesh.skin.get_skin_cluster(mesh):
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        skin_info = base_class.mesh.skin_info.SkinInfo()
        skin_info.create_info([mesh])

        this_vertex_list = \
            base_utility.mesh.skin.get_vertex_list_with_unround_weight(
                skin_info, 2)

        if this_vertex_list:

            param_item.error_target_list.extend(
                this_vertex_list
            )

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_joint_with_no_skin(param_item, arg):
    """
    不正なジョイントにウェイトがないかの確認
    """

    # ------------------------------
    # 前提条件

    # 命名規則が取得できない場合は処理しない
    if not param_item.main.chara_info.part_info.joint_naming_rule_list:
        return

    # ------------------------------
    # 設定

    target_joint_list = []

    naming_rule = param_item.main.chara_info.part_info.joint_naming_rule_list[0]
    pattern = re.compile(naming_rule)

    tmp_joint_list = cmds.ls(l=True, typ='joint')

    for joint in tmp_joint_list:
        if pattern.match(joint) and joint.endswith('End'):
            target_joint_list.append(joint)

    if not target_joint_list:
        return

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list = target_joint_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        if not base_utility.mesh.skin.get_skin_cluster(mesh):
            continue

        # メッシュからウェイト情報取り出し
        vertex_waight_info_list = \
            base_utility.mesh.skin.get_all_joint_weight_info_list(mesh)

        for vertex_waight_info in vertex_waight_info_list:

            # 頂点名を作成
            vertex = '{0}.vtx[{1}]'.format(mesh, str(vertex_waight_info[0]))

            # check_target_listに頂点を追加
            param_item.check_target_list.append(vertex)

            for joint_waight_info in vertex_waight_info[1]:

                if joint_waight_info[0] in target_joint_list:

                    # error_target_listに頂点を追加
                    param_item.error_target_list.append(vertex)

                    break

    # エラー外のチェック
    for vertex in param_item.check_target_list:

        if vertex in param_item.error_target_list:
            continue

        # unerror_target_listに頂点を追加
        param_item.unerror_target_list.append(vertex)


# ==================================================
def check_mesh_with_no_skin(param_item, arg):
    """
    メッシュに不要なスキンがないかの確認
    """

    # ------------------------------
    # 設定

    target_mesh_list = [
        'M_Tear_L',
        'M_Tear_R',
        'M_Line00',
    ]

    root_node = param_item.main.chara_info.part_info.root_node
    mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        if mesh.split('|')[-1] in target_mesh_list:

            param_item.check_target_list.append(mesh)

            if base_utility.mesh.skin.get_skin_cluster(mesh):

                param_item.error_target_list.append(mesh)
                continue

            param_item.unerror_target_list.append(mesh)

# endregion

# region UV系


# ==================================================
def check_mesh_uvset(param_item, arg):
    """
    UVセット数の確認
    Faceは3以外,他メッシュは1以外ならエラー
    _Emissiveメッシュは1以外ならエラー
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        param_item.check_target_list.append(mesh)

        uvset_count = 1

        if not param_item.main.chara_info.is_mini:
            if mesh.find('Face') >= 0 and not mesh.endswith('_Emissive'):
                uvset_count = 3

        uvset_list = base_utility.mesh.uvset.get_uvset_list(mesh)

        if len(uvset_list) == uvset_count:
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(
            mesh
        )


# ==================================================
def check_mesh_uv_coordinate(param_item, arg):
    """
    UV座標の確認
    0~1.0の範囲になければエラー
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    target_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        if mesh.find('Tear') >= 0:
            continue

        all_uv_info_list = base_utility.mesh.uv.get_all_uv_info_list(
            mesh)

        for uv_info in all_uv_info_list:

            uv_name = mesh + '.map[%s]' % str(uv_info[0])

            param_item.check_target_list.append(uv_name)

            if 0 <= uv_info[1][0] <= 1.0 and 0 <= uv_info[1][1] <= 1.0:

                param_item.unerror_target_list.append(uv_name)
                continue

            param_item.error_target_list.append(uv_name)

# endregion

# region マテリアル系


# ==================================================
def check_material_exist(param_item, args):
    """
    マテリアルが存在するかのチェック
    """

    # ------------------------------
    # 設定

    target_material_list = []

    for material_param in param_item.main.chara_info.part_info.material_param_list:

        if material_param['check']:
            target_material_list.append(material_param['name'])

    if not target_material_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_material_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_material_list)

    for material in target_material_list:

        if material and cmds.objExists(material):
            if cmds.ls(material, typ=['lambert']):
                param_item.unerror_target_list.append(material)
                continue

        param_item.error_target_list.append(material)


# ==================================================
def check_material_naming_rule(param_item, args):
    """
    マテリアルの命名規則の確認
    """

    # ------------------------------
    # 前提条件

    # 命名規則が取得できない場合は処理しない
    if not param_item.main.chara_info.part_info.material_naming_rule_list:
        return

    # ------------------------------
    # 設定

    tmp_material_list = cmds.ls(mat=True)
    target_material_list = []

    for material in tmp_material_list:
        if not material == 'lambert1' and not material == 'particleCloud1':
            target_material_list.append(material)

    if not target_material_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_material_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_material_list)

    naming_rule = param_item.main.chara_info.part_info.material_naming_rule_list[0]
    pattern = re.compile(naming_rule)

    for material in target_material_list:

        if pattern.match(material):
            param_item.unerror_target_list.append(material)
        else:
            param_item.error_target_list.append(material)


# ==================================================
def check_material_link(param_item, args):
    """
    メッシュに正しいマテリアルが紐づいているかのチェック
    """

    # ------------------------------
    # 前提条件

    # 命名規則が取得できない場合は処理しない
    if not param_item.main.chara_info.part_info.mesh_naming_rule_list:
        return

    if not param_item.main.chara_info.part_info.material_naming_rule_list:
        return

    # 割り当てパターンが取得できない場合は処理しない
    if not param_item.main.chara_info.part_info.material_link_rule_list:
        return

    # ------------------------------
    # 設定

    # 命名規則に沿ったメッシュの取得
    mesh_naming_rule = \
        param_item.main.chara_info.part_info.mesh_naming_rule_list[0]
    pattern = re.compile(mesh_naming_rule)

    root_node = param_item.main.chara_info.part_info.root_node
    tmp_mesh_list = model_mesh_finder.get_all_mesh_list(root_node)
    target_mesh_list = []

    for mesh in tmp_mesh_list:
        if pattern.match(mesh):
            target_mesh_list.append(mesh)

    if not target_mesh_list:
        return

    # 命名規則に沿ったマテリアルの取得
    material_naming_rule = \
        param_item.main.chara_info.part_info.material_naming_rule_list[0]
    pattern = re.compile(material_naming_rule)

    tmp_material_list = cmds.ls(mat=True)
    target_material_list = []

    for material in tmp_material_list:
        if pattern.match(material):
            target_material_list.append(material)

    if not target_material_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_material_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    separator = param_item.root.info_window.detail_separator

    param_item.check_target_list.extend(target_material_list)

    link_rule_list = \
        param_item.main.chara_info.part_info.material_link_rule_param_list

    for link_rule in link_rule_list:
        material_pattern = re.compile(link_rule['name'])

        for material in target_material_list:
            if not material_pattern.match(material):
                continue

            target = material_pattern.sub(link_rule['target_mesh'], material)
            mesh_pattern = re.compile(target)

            unassigned_error_mesh = []
            assigned_error_mesh = []

            for mesh in target_mesh_list:
                should_have = mesh_pattern.match(mesh) is not None
                material_list = base_utility.material.get_material_list(mesh)
                has_material = material in material_list

                # 割り当て対象のメッシュに割り当てられていない場合
                if should_have and not has_material:
                    unassigned_error_mesh.append(mesh)
                    continue

                # 割り当て対象外のメッシュに割り当てられている場合
                if not should_have and has_material:
                    assigned_error_mesh.append(mesh)
                    continue

            if not unassigned_error_mesh and not assigned_error_mesh:
                param_item.unerror_target_list.append(material)

            for mesh in unassigned_error_mesh:
                error_str = u'対象のメッシュに割り当てられていません: {}'.format(mesh)
                param_item.error_target_list.append(
                    '{0}{1}{2}'.format(material, separator, error_str))

            for mesh in assigned_error_mesh:
                error_str = u'対象外のメッシュに割り当てられています: {}'.format(mesh)
                param_item.error_target_list.append(
                    '{0}{1}{2}'.format(material, separator, error_str))


# ==================================================
def check_material_texture_path(param_item, arg):
    """
    マテリアルのテクスチャパスのチェック
    """

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(
        param_item.main.chara_info.part_info.material_list
    )

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for p in range(len(param_item.main.chara_info.part_info.material_param_list)):

        material = param_item.main.chara_info.part_info.material_param_list[p]['name']

        material_index = param_item.main.chara_info.part_info.material_param_list[p]['diff']

        if material_index < 0:
            continue

        texture_name = \
            param_item.main.chara_info.part_info.texture_list[material_index]

        input_attr_list = None
        if cmds.objExists(material) and cmds.attributeQuery('color', node=material, exists=True):
            input_attr_list = cmds.listConnections(material + '.color', p=True, s=True, d=False)

        if not input_attr_list:
            continue

        this_input_attr = input_attr_list[0]

        this_input_node = this_input_attr.split('.')[0]

        if not cmds.objectType(this_input_node) == 'file':
            continue

        this_file_path = None
        if cmds.objExists(this_input_node) and cmds.attributeQuery('fileTextureName', node=this_input_node, exists=True):
            this_file_path = cmds.getAttr('{}.{}'.format(this_input_node, 'fileTextureName'))

        if this_file_path is None:
            continue

        this_file_name = os.path.basename(this_file_path)

        if this_file_name == texture_name:
            continue

        param_item.error_target_list.append(material)

# endregion

# region テクスチャ系


# ==================================================
def check_texture_exist(param_item, arg):
    """
    テクスチャが存在するかのチェック
    """

    # ------------------------------
    # 設定

    texture_type = arg[0]
    target_texture_list = None
    material_list = param_item.main.chara_info.part_info.material_list

    if not material_list:
        return

    if texture_type == 'texture':
        target_texture_list = []
        for material in material_list:
            target_texture_list.extend(
                farm_utility.model_texture_finder.get_texture_list_from_material(material)
            )

    # elif texture_type == 'psd':
    #     target_texture_list = param_item.main.chara_info.part_info.psd_list
    #     target_texture_info_list = param_item.main.chara_info.part_info.psd_param_list

    target_texture_list = list(set(target_texture_list))
    target_texture_list.sort()

    if not target_texture_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_texture_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for texture in target_texture_list:

        texture_path = param_item.main.chara_info.part_info.maya_sourceimages_dir_path + \
            '/' + texture

        if os.path.isfile(texture_path):
            param_item.unerror_target_list.append(texture_path)
            continue

        param_item.error_target_list.append(texture_path)


# ==================================================
def check_texture_size(param_item, arg):
    """
    テクスチャサイズのチェック
    """

    # ------------------------------
    # 設定

    texture_type = arg[0]
    target_texture_list = None
    material_list = param_item.main.chara_info.part_info.material_list

    if not material_list:
        return

    if texture_type == 'texture':
        target_texture_list = []
        for material in material_list:
            target_texture_list.extend(
                farm_utility.model_texture_finder.get_texture_list_from_material(material)
            )

    # elif texture_type == 'psd':
    #     target_texture_list = param_item.main.chara_info.part_info.psd_list
    #     target_texture_info_list = param_item.main.chara_info.part_info.psd_param_list

    target_texture_list = list(set(target_texture_list))
    target_texture_list.sort()

    if not target_texture_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_texture_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    temp_file_node = cmds.shadingNode(
        'file', asTexture=True, name='temp_file_node')

    for texture in target_texture_list:

        texture_path = param_item.main.chara_info.part_info.maya_sourceimages_dir_path + \
            '/' + texture

        if not os.path.isfile(texture_path):
            continue

        param_item.check_target_list.append(texture_path)

        target_size = farm_utility.model_texture_finder.get_target_texture_size(texture)

        cmds.setAttr(temp_file_node + '.fileTextureName', texture_path, type='string')

        this_tex_size = [0, 0]
        if cmds.objExists(temp_file_node) and cmds.attributeQuery('outSize', node=temp_file_node, exists=True):
            this_tex_size = cmds.getAttr('{}.{}'.format(temp_file_node, 'outSize'))[0]

        if base_utility.vector.is_same(target_size, this_tex_size):
            continue

        param_item.error_target_list.append(texture_path)

    cmds.delete(temp_file_node)

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)

# endregion

# region ロケータ系


# ==================================================
def check_locator_exist(param_item, arg):
    """
    ロケータが存在するかのチェック
    """

    # ------------------------------
    # 設定

    data_info = param_item.main.chara_info.data_info

    # 武器を持っているが武器パーツ数が取得できない場合は処理しない
    if data_info.has_weapon and data_info.weapon_parts_count is None:
        return

    all_target_locator_list = []

    target_locator_list = []

    for locator_param in param_item.main.chara_info.part_info.locator_param_list:
        if locator_param['check']:
            target_locator_list.append(locator_param['name'])

    all_target_locator_list.extend(target_locator_list)

    target_locator_pattern_list = []

    for locator_param in param_item.main.chara_info.part_info.locator_pattern_param_list:
        if locator_param['check']:
            target_locator_pattern_list.append(locator_param['name'])

    all_target_locator_list.extend(target_locator_pattern_list)

    if not all_target_locator_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(all_target_locator_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = all_target_locator_list

    for locator in target_locator_list:

        if locator and cmds.objExists(locator):
            param_item.unerror_target_list.append(locator)
            continue

        param_item.error_target_list.append(locator)

    def is_locator(node): return cmds.listRelatives(node, s=True, typ='locator')

    locator_list = [n for n in cmds.ls(l=True) if is_locator(n)]

    for locator in target_locator_pattern_list:
        pattern = re.compile(locator)
        if any(pattern.match(l) for l in locator_list):
            param_item.unerror_target_list.append(locator)
            continue

        param_item.error_target_list.append(locator)


# ==================================================
def check_locator_naming_rule(param_item, arg):
    """
    ロケータの命名規則チェック
    """

    # ------------------------------
    # 設定

    def is_locator(node): return cmds.listRelatives(node, s=True, typ='locator')

    target_locator_list = [n for n in cmds.ls(l=True) if is_locator(n)]

    if not target_locator_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_locator_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_locator_list)

    names = param_item.main.chara_info.part_info.locator_list
    patterns = [re.compile(r'^' + re.escape(n) + r'$') for n in names]

    names = param_item.main.chara_info.part_info.locator_pattern_list
    patterns.extend([re.compile(n) for n in names])

    # CharaInfoで定義されているものに加えて、FX_center, FX_Tip, FX_FollowEFを許容する
    ex_names = [
        r'^.*\|FX_center$',
        r'^.*\|FX_Tip[2-9]?$',
        r'^.*\|FX_FollowEF[2-9]?$'
    ]
    patterns.extend([re.compile(n) for n in ex_names])

    for locator in target_locator_list:
        if any(p.match(locator) for p in patterns):
            param_item.unerror_target_list.append(locator)
            continue

        param_item.error_target_list.append(locator)


# ==================================================
def check_locator_rotation(param_item, arg):
    """
    ロケータの回転チェック
    """

    # ------------------------------
    # 設定

    target_list = {
        'Head_direction': [85.1, 90, 0.0],
    }

    locator_nodes = param_item.main.chara_info.part_info.locator_list

    if not locator_nodes:
        return

    is_target = lambda l: l.split('|')[-1] in target_list

    target_locator_list = [l for l in locator_nodes if is_target(l)]

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_locator_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_locator_list

    for locator in target_locator_list:

        rotate_check_value = target_list.get(locator.split('|')[-1])

        rotate = None
        if cmds.objExists(locator) and cmds.attributeQuery('rotate', node=locator, exists=True):
            rotate = cmds.getAttr('{}.{}'.format(locator, 'rotate'))[0]

        if not base_utility.vector.is_same(
            rotate, rotate_check_value
        ):
            param_item.error_target_list.append(locator)
            continue

        param_item.unerror_target_list.append(locator)


# ==================================================
def check_locator_transform(param_item, arg):
    """
    ロケータのトランスフォーム情報のチェック
    """

    # ------------------------------
    # 設定

    target_locator_list = []

    for locator_param in param_item.main.chara_info.part_info.locator_param_list:
        if locator_param['check']:
            target_locator_list.append(locator_param['name'])

    if not target_locator_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_locator_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_locator_list

    for locator in target_locator_list:

        if not locator or not cmds.objExists(locator):
            param_item.error_target_list.append(locator)
            continue

        check_translate = True
        check_rotate = True
        check_scale = True

        translate_check_value = [0, 0, 0]
        rotate_check_value = [0, 0, 0]
        scale_check_value = [1, 1, 1]

        if locator.find('_attach') >= 0:
            check_translate = False
            check_rotate = False
            check_scale = False

        elif locator.find('Eye_locator_') >= 0 or\
                locator.find('Eye_target_locator_') >= 0:
            check_translate = False
            check_rotate = False

        elif locator.find('|Eye_base') >= 0 or \
                locator.find('|Eye_big') >= 0 or \
                locator.find('|Eye_small') >= 0 or \
                locator.find('|Eye_kira') >= 0:
            check_rotate = False
            check_scale = False

        elif locator.find('spec_info') >= 0 or \
                locator.find('Head_shade_start') >= 0:
            check_translate = False
            check_rotate = False
            check_scale = False

        else:
            check_translate = False

        translate = None
        rotate = None
        scale = None
        if cmds.objExists(locator):
            if cmds.attributeQuery('translate', node=locator, exists=True):
                translate = cmds.getAttr('{}.{}'.format(locator, 'translate'))[0]

            if cmds.attributeQuery('rotate', node=locator, exists=True):
                rotate = cmds.getAttr('{}.{}'.format(locator, 'rotate'))[0]

            if cmds.attributeQuery('scale', node=locator, exists=True):
                scale = cmds.getAttr('{}.{}'.format(locator, 'scale'))[0]

        is_hit = False

        if check_translate:

            if not base_utility.vector.is_same(
                translate, translate_check_value
            ):
                is_hit = True

        if check_rotate:

            if not base_utility.vector.is_same(
                rotate, rotate_check_value
            ):
                is_hit = True

        if check_scale:

            if not base_utility.vector.is_same(
                scale, scale_check_value
            ):
                is_hit = True

        if not is_hit:
            param_item.unerror_target_list.append(locator)
            continue

        param_item.error_target_list.append(locator)


# ==================================================
def check_eye_locator_position(param_item, arg):
    """
    目ロケータのトランスフォーム情報のチェック
    """

    # ------------------------------
    # 設定

    target_list = [
        'Eye_L',
        'Eye_R',
        'Eye_locator_L',
        'Eye_locator_R',
    ]

    # ------------------------------
    # 情報

    param_item.info_target_list = target_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_list

    this_set_list = [
        [target_list[0], target_list[2]],
        [target_list[1], target_list[3]]
    ]

    for this_set in this_set_list:

        if not this_set[0] or not cmds.objExists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not this_set[0] or not cmds.objExists(this_set[1]):
            param_item.error_target_list.extend(this_set)
            continue

        re_obj = re.compile(param_item.main.chara_info.data_id + '\|')

        base_name = this_set[0]
        long_base_name_list = cmds.ls(base_name, l=True)
        if len(long_base_name_list) == 1:
            base_name = long_base_name_list[0]
        else:
            for long_base_name in long_base_name_list:
                if re_obj.search(long_base_name):
                    base_name = long_base_name
                    break

        locator_name = this_set[1]
        long_locator_name_list = cmds.ls(locator_name, l=True)
        if len(long_locator_name_list) == 1:
            locator_name = long_locator_name_list[0]
        else:
            for long_locator_name in long_locator_name_list:
                if re_obj.search(long_locator_name):
                    locator_name = long_locator_name
                    break

        base_trans = cmds.xform(
            base_name, q=True, t=True, ws=True)

        locator_trans = cmds.xform(
            locator_name, q=True, t=True, ws=True)

        if base_utility.vector.is_same(
            base_trans, locator_trans
        ):
            param_item.unerror_target_list.extend(this_set)
            continue

        param_item.error_target_list.extend(this_set)


# ==================================================
def check_tail_locator_position(param_item, arg):
    """
    尻尾ロケータのトランスフォーム情報のチェック
    """

    # ------------------------------
    # 設定

    target_list = [
        'Sp_Hi_Tail0_B_00',
        'Tail_Ctrl',
    ]

    # ------------------------------
    # 情報

    param_item.info_target_list = target_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_list

    this_set_list = [
        [target_list[0], target_list[1]]
    ]

    for this_set in this_set_list:

        if not this_set[0] or not cmds.objExists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not this_set[0] or not cmds.objExists(this_set[1]):
            param_item.error_target_list.extend(this_set)
            continue

        re_obj = re.compile(param_item.main.chara_info.data_id + '\|')

        base_name = this_set[0]
        long_base_name_list = cmds.ls(base_name, l=True)
        if len(long_base_name_list) == 1:
            base_name = long_base_name_list[0]
        else:
            for long_base_name in long_base_name_list:
                if re_obj.search(long_base_name):
                    base_name = long_base_name
                    break

        locator_name = this_set[1]
        long_locator_name_list = cmds.ls(locator_name, l=True)
        if len(long_locator_name_list) == 1:
            locator_name = long_locator_name_list[0]
        else:
            for long_locator_name in long_locator_name_list:
                if re_obj.search(long_locator_name):
                    locator_name = long_locator_name
                    break

        base_trans = cmds.xform(
            base_name, q=True, t=True, ws=True)

        locator_trans = cmds.xform(
            locator_name, q=True, t=True, ws=True)

        if base_utility.vector.is_same(
            base_trans, locator_trans
        ):
            param_item.unerror_target_list.extend(this_set)
            continue

        param_item.error_target_list.extend(this_set)


# ==================================================
def check_tail_locator_position_from_hip(param_item, arg):
    """
    Hipジョイントと尻尾ロケータの位置チェック
    """

    # ------------------------------
    # 設定

    target_name_list = [
        'Hip',
        'Tail_Ctrl',
    ]

    # ------------------------------
    # 情報

    param_item.info_target_list = target_name_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    transform_list = []

    transform_list.extend(
        param_item.main.chara_info.part_info.joint_list)

    transform_list.extend(
        param_item.main.chara_info.part_info.locator_list)

    target_list = []

    for name in transform_list:
        if name.split('|')[-1] in target_name_list:
            target_list.append(name)

    param_item.check_target_list = target_list

    this_set_list = [
        [target_list[0], target_list[1]]
    ]

    correct_trans_list = [
        [0.0, 7.628322167187548, -11.229461669921875]
    ]

    for this_set, correct_trans in zip(this_set_list, correct_trans_list):

        if not this_set[0] or not cmds.objExists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not this_set[0] or not cmds.objExists(this_set[1]):
            param_item.error_target_list.extend(this_set)
            continue

        base_trans = cmds.xform(
            this_set[0], q=True, t=True, ws=True)

        locator_trans = cmds.xform(
            this_set[1], q=True, t=True, ws=True)

        base_to_locator_trans = base_utility.vector.sub(
            locator_trans, base_trans)

        if base_utility.vector.is_same(
            base_to_locator_trans, correct_trans
        ):
            param_item.unerror_target_list.extend(this_set)
            continue

        param_item.error_target_list.extend(this_set)


# ==================================================
def check_lock_locator_node(param_item, args):
    """
    ロケータノードのアトリビュートがロックされていないかのチェック
    """
    # ------------------------------
    # 設定

    locator_nodes = param_item.main.chara_info.part_info.locator_list
    if not locator_nodes:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(locator_nodes)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = locator_nodes

    attr_list = ['translate', 'rotate', 'scale']
    direction_list = ['X', 'Y', 'Z']

    for locator_node in locator_nodes:

        is_lock = False

        if not cmds.objExists(locator_node):
            param_item.error_target_list.append(locator_node)
            continue

        for attr in attr_list:

            for direction in direction_list:

                attr_str = '{0}.{1}{2}'.format(locator_node, attr, direction)
                tmp_lock = cmds.getAttr(attr_str, lock=True)

                if tmp_lock:
                    is_lock = True
                    break

            if is_lock:
                break

        if is_lock:
            param_item.error_target_list.append(locator_node)
        else:
            param_item.unerror_target_list.append(locator_node)


# endregion

# region ジョイント系


# ==================================================
def check_joint_exist(param_item, arg):
    """
    ジョイントの存在チェック
    """

    # ------------------------------
    # 設定

    target_joint_list = []

    for joint_param in param_item.main.chara_info.part_info.joint_param_list:
        if joint_param['check']:
            target_joint_list.append(joint_param['name'])

    if not target_joint_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_joint_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_joint_list

    for joint in target_joint_list:

        if joint and cmds.objExists(joint):
            if cmds.ls(joint, typ='joint'):
                param_item.unerror_target_list.append(joint)
                continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_joint_naming_rule(param_item, arg):
    """
    ジョイントの命名規則チェック
    """

    # ------------------------------
    # 前提条件

    # 命名規則が取得できない場合は処理しない
    if not param_item.main.chara_info.part_info.joint_naming_rule_list:
        return

    # ------------------------------
    # 設定

    target_joint_list = cmds.ls(l=True, typ='joint')

    if not target_joint_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_joint_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_joint_list)

    naming_rule = param_item.main.chara_info.part_info.joint_naming_rule_list[0]
    pattern = re.compile(naming_rule)

    for joint in target_joint_list:
        if pattern.match(joint):
            param_item.unerror_target_list.append(joint)
            continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_all_joint_count(param_item, arg):
    """
    すべてのジョイントの数をチェック
    """

    # ------------------------------
    # 設定

    target_min_count = 10000
    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        target_min_count = 127
    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        target_min_count = 113
    elif param_item.main.chara_info.part_info.data_type.find('prop') >= 0:
        target_min_count = 35

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    joint_list = __get_filtered_joint_list([root_node], None, None)

    all_count = len(joint_list)
    error_count = all_count - target_min_count

    param_item.check_target_list.extend(joint_list)

    if error_count > 0:
        param_item.error_target_list.append(
            '{}/{} joints: {} joints over'.format(all_count, target_min_count, error_count)
        )
    else:
        param_item.unerror_target_list.append(
            '{}/{} joints'.format(all_count, target_min_count)
        )


# ==================================================
def check_nocloth_joint_count(param_item, arg):
    """
    クロス系ではないジョイントの数をチェック
    """

    target_min_count = 10000
    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        target_min_count = 95
    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        target_min_count = 62
    elif param_item.main.chara_info.part_info.data_type.find('prop') >= 0:
        target_min_count = 10000

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    joint_list = __get_filtered_joint_list([root_node], None, CLOTH_JOINT_LIST)

    all_count = len(joint_list)
    error_count = all_count - target_min_count

    param_item.check_target_list.extend(joint_list)

    if error_count > 0:
        param_item.error_target_list.append(
            '{}/{} joints: {} joints over'.format(all_count, target_min_count, error_count)
        )
    else:
        param_item.unerror_target_list.append(
            '{}/{} joints'.format(all_count, target_min_count)
        )


# ==================================================
def check_cloth_joint_count(param_item, arg):
    """
    クロス系ジョイントの数をチェック
    """

    target_min_count = 10000
    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        target_min_count = 36
    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        target_min_count = 51
    elif param_item.main.chara_info.part_info.data_type.find('prop') >= 0:
        target_min_count = 10000

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    joint_list = __get_filtered_joint_list([root_node], CLOTH_JOINT_LIST, None)

    all_count = len(joint_list)
    error_count = all_count - target_min_count

    param_item.check_target_list.extend(joint_list)

    if error_count > 0:
        param_item.error_target_list.append(
            '{}/{} joints: {} joints over'.format(all_count, target_min_count, error_count)
        )
    else:
        param_item.unerror_target_list.append(
            '{}/{} joints'.format(all_count, target_min_count)
        )


# ==================================================
def check_cloth_joint_sum_count(param_item, arg):
    """
    クロスジョイント合算数をチェック
    """

    head_target_min_count = 36
    body_target_min_count = 51
    target_min_count = head_target_min_count + body_target_min_count

    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        check_cloth_joint_sum_count_from_head(param_item, target_min_count, arg)

    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        check_cloth_joint_sum_count_from_body(param_item, target_min_count, arg)


# ==================================================
def check_cloth_joint_sum_count_from_head(param_item, target_min_count, arg):
    """
    ユニーク頭部から各身体とのクロスジョイント合算数をチェック
    """

    body_finder = farm_class.path_finder.path_finder.PathFinder('body', param_item.main.chara_info.data_main_id)
    target_body_file_list = body_finder.model_ma_list[:]

    check_dict_list = []

    for target_body_file in target_body_file_list:

        check_dict = {
            'head_path': '',
            'body_path': '',
            'info_str': ''
        }

        check_dict['head_path'] = cmds.file(q=True, sn=True)
        check_dict['body_path'] = target_body_file

        head_file_name = os.path.basename(check_dict['head_path'])
        body_file_name = os.path.basename(check_dict['body_path'])

        check_dict['info_str'] = '{}, {}'.format(head_file_name, body_file_name)

        check_dict_list.append(check_dict)

    # ------------------------------
    # 設定

    if not check_dict_list:
        return

    body_ref_name_space = '__BODY_MODEL_REF__'

    # ------------------------------
    # 情報

    for check_dict in check_dict_list:
        param_item.info_target_list.append(check_dict['info_str'])

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for check_dict in check_dict_list:

        tmp_info = farm_common.classes.info.chara_info.CharaInfo()
        tmp_info.create_info(check_dict['body_path'])

        if not tmp_info.part_info:
            continue

        body_root = tmp_info.part_info.root_node
        body_root = body_root.replace('|', '|{}:'.format(body_ref_name_space))
        head_root = param_item.main.chara_info.part_info.root_node

        # ロード/失敗したらエラーで返す
        base_utility.reference.load(check_dict['body_path'], body_ref_name_space)
        if not base_utility.reference.exists(check_dict['body_path'], body_ref_name_space):
            param_item.error_target_list.append('{} (REFERENCE ERROR)'.format(check_dict['body_path']))
            continue

        # 対象ジョイントの取得
        joint_list = __get_filtered_joint_list([head_root, body_root], CLOTH_JOINT_PREFIX_LIST, None)

        # アンロード
        base_utility.reference.unload(check_dict['body_path'], body_ref_name_space)

        # チェック結果の記載
        all_count = len(joint_list)
        error_count = all_count - target_min_count

        param_item.check_target_list.append(check_dict['info_str'])
        if error_count > 0:
            param_item.error_target_list.append(
                '{} ({}/{} joints: {} joints over)'.format(check_dict['info_str'], all_count, target_min_count, error_count)
            )
        else:
            param_item.unerror_target_list.append(
                '{} ({}/{} joints)'.format(check_dict['info_str'], all_count, target_min_count)
            )


# ==================================================
def check_cloth_joint_sum_count_from_body(param_item, target_min_count, arg):
    """
    特別衣装クロス系ジョイントの頭と身体の合算数をチェック
    """

    # ------------------------------
    # 設定

    head_info = param_item.main.chara_info.head_part_info

    if not head_info:
        return

    head_finder = farm_class.path_finder.path_finder.PathFinder('head', '{}_{}'.format(head_info.main_id, head_info.sub_id))

    if not head_finder.model_ma_list:
        return

    check_dict = {
        'head_path': '',
        'body_path': '',
        'info_str': ''
    }

    check_dict['head_path'] = head_finder.model_ma_list[0]
    check_dict['body_path'] = cmds.file(q=True, sn=True)

    head_file_name = os.path.basename(check_dict['head_path'])
    body_file_name = os.path.basename(check_dict['body_path'])

    check_dict['info_str'] = '{}, {}'.format(head_file_name, body_file_name)

    head_ref_name_space = '__HEAD_MODEL_REF__'

    # ------------------------------
    # 情報

    param_item.info_target_list.append(check_dict['info_str'])

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    head_root = head_info.root_node
    head_root = head_root.replace('|', '|{}:'.format(head_ref_name_space))
    body_root = param_item.main.chara_info.part_info.root_node

    # ロード/失敗したらエラーで返す
    base_utility.reference.load(check_dict['head_path'], head_ref_name_space)
    if not base_utility.reference.exists(check_dict['head_path'], head_ref_name_space):
        param_item.error_target_list.append('{} (REFERENCE ERROR)'.format(check_dict['head_path']))
        return

    # 対象ジョイントの取得
    joint_list = __get_filtered_joint_list([head_root, body_root], CLOTH_JOINT_PREFIX_LIST, None)

    # アンロード
    base_utility.reference.unload(check_dict['head_path'], head_ref_name_space)

    # チェック結果の記載
    all_count = len(joint_list)
    error_count = all_count - target_min_count

    param_item.check_target_list.append(check_dict['info_str'])
    if error_count > 0:
        param_item.error_target_list.append(
            '{} ({}/{} joints: {} joints over)'.format(check_dict['info_str'], all_count, target_min_count, error_count)
        )
    else:
        param_item.unerror_target_list.append(
            '{} ({}/{} joints)'.format(check_dict['info_str'], all_count, target_min_count)
        )


# ==================================================
def __get_filtered_joint_list(target_root_list, filter_list, no_filter_list):
    """
    target_root_list以下のフィルターされたジョイントリストを返す
    """

    fix_root_node_list = []
    for root in target_root_list:
        if cmds.objExists(root):
            fix_root_node_list.append(root)

    if not fix_root_node_list:
        return []

    all_joint_list = cmds.listRelatives(
        fix_root_node_list, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return []

    sorted_joint_list = []

    # CLOTH_JOINT_LISTの要素順に応じて並び替え
    sort_target_len = len(CLOTH_JOINT_LIST)
    sort_target_joints_list = [[] for i in range(sort_target_len)]

    for joint in all_joint_list:

        joint_name = joint.split('|')[-1]

        for i in range(sort_target_len):

            sort_target = CLOTH_JOINT_LIST[i]
            if re.search(sort_target, joint_name):
                sort_target_joints_list[i].append(joint)
                break

        else:

            sorted_joint_list.append(joint)

    for sort_target_joints in sort_target_joints_list:
        sorted_joint_list.extend(sort_target_joints)

    filtered_joint_list = []

    for joint in sorted_joint_list:

        if not cmds.objExists(joint):
            continue

        joint_name = joint.split('|')[-1]

        this_exists = True

        # 名前フィルタ (含む)
        if filter_list:

            this_exists = False

            for this_filter in filter_list:

                if re.search(this_filter, joint_name):
                    this_exists = True
                    break

        if not this_exists:
            continue

        # 名前フィルタ (含まない)
        if no_filter_list:

            this_exists = True

            for this_filter in no_filter_list:

                if re.search(this_filter, joint_name):
                    this_exists = False
                    break

        if not this_exists:
            continue

        filtered_joint_list.append(joint)

    return filtered_joint_list


# ==================================================
def check_joint_regex(param_item, arg):
    """
    ジョイントが命名規則に合致しているかをチェック
    """

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    param_item.info_target_list.append(root_node)
    if not param_item.is_check_data:
        return

    base_joint_list = param_item.main.chara_info.part_info.joint_list
    if not base_joint_list:
        return

    root_joint_node = ''
    all_joint_list = []

    if param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        root_joint_node = '{}|Position'.format(root_node)
    elif param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        root_joint_node = '{}|Neck'.format(root_node)
        all_joint_list.append(root_joint_node)
    elif param_item.main.chara_info.part_info.data_type.find('tail') >= 0:
        root_joint_node = '{}|Hip'.format(root_node)
        all_joint_list.append(root_joint_node)

    if not root_joint_node or not cmds.objExists(root_joint_node):
        return

    all_joint_list = cmds.listRelatives(root_joint_node, ad=True, f=True, type='joint') + all_joint_list
    if not all_joint_list:
        return

    all_joint_list.reverse()

    param_item.check_target_list = all_joint_list

    for joint in all_joint_list:

        if joint not in base_joint_list:

            joint_short_name = joint.split('|')[-1]
            joint_elm_list = joint_short_name.split('_')

            # 命名構成要素数チェック
            if not len(joint_elm_list) == 5:
                param_item.error_target_list.append(joint)
                continue

            # 接頭語チェック
            joint_prefix = '{}_'.format(joint_elm_list[0])

            if joint_prefix not in CLOTH_JOINT_PREFIX_LIST:
                param_item.error_target_list.append(joint)
                continue

            # 一連の骨命名チェック
            # 末尾の連番をとったベースネームでフルパスをスプリットすると、連番+2に分割されるはず
            joint_num = -1

            try:
                joint_num = int(joint_elm_list[-1])
            except ValueError:
                param_item.error_target_list.append(joint)
                continue

            joint_base_name = '_'.join(joint_elm_list[:4])

            if not len(joint.split(joint_base_name)) == joint_num + 2:
                param_item.error_target_list.append(joint)
                continue

            # 親骨チェック
            joint_parent_str = joint_elm_list[1]
            parent_joint_base_name = ''

            if joint_parent_str not in CLOTH_JOINT_PARENT_DICT:
                param_item.error_target_list.append(joint)
                continue
            else:
                parent_joint_base_name = CLOTH_JOINT_PARENT_DICT[joint_parent_str]

            joint_root = ''

            if param_item.main.chara_info.part_info.data_type.find('tail') >= 0:
                joint_root = 'Tail_Ctrl'
            else:
                joint_root_elm_list = joint_elm_list[:]
                joint_root_elm_list[-1] = '00'
                joint_root = '_'.join(joint_root_elm_list)

            joint_parent = joint.split('|{}'.format(joint_root))[0]
            parent_short_name = joint_parent.split('|')[-1]

            if parent_short_name.find(parent_joint_base_name) < 0:
                param_item.error_target_list.append(joint)
                continue

        param_item.unerror_target_list.append(joint)


# ==================================================
def check_joint_transform(param_item, arg):
    """
    ジョイントのトランスフォーム情報をチェック
    """

    # ------------------------------
    # 前提条件

    data_type = param_item.main.chara_info.data_type
    data_info = param_item.main.chara_info.data_info

    is_character = \
        data_type == model_define.AVATAR_DATA_TYPE \
        or data_type == model_define.UNIT_DATA_TYPE

    # モデルサイズが取得できない場合は処理しない
    if is_character and not data_info.model_size:
        return

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    if not cmds.objExists(root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return

    param_item.check_target_list = all_joint_list

    for joint in all_joint_list:

        joint_name = joint.split('|')[-1]

        check_translate = False
        check_rotate = True
        check_scale = True
        check_orient = False
        check_orient_sp_target_list = []

        translate = None
        rotate = None
        scale = None
        if cmds.objExists(joint):
            if cmds.attributeQuery('translate', node=joint, exists=True):
                translate = cmds.getAttr('{}.{}'.format(joint, 'translate'))[0]

            if cmds.attributeQuery('rotate', node=joint, exists=True):
                rotate = cmds.getAttr('{}.{}'.format(joint, 'rotate'))[0]

            if cmds.attributeQuery('scale', node=joint, exists=True):
                scale = cmds.getAttr('{}.{}'.format(joint, 'scale'))[0]

        is_hit = False

        if check_translate:

            if not base_utility.vector.is_same(
                translate, [0, 0, 0]
            ):
                is_hit = True

        if check_rotate:

            tail_rotate_dict = {
                'Sp_Hi_Tail0_B_00': [56.651, 0.0, 0.0],
                'Sp_Hi_Tail0_B_01': [18.349, 0.0, 0.0],
                'Sp_Hi_Tail0_B_02': [10.0, 0.0, 0.0],
                'Sp_Hi_Tail0_B_03': [10.0, 0.0, 0.0],
                'Sp_Hi_Tail0_B_04': [10.0, 0.0, 0.0],
            }

            if joint_name in list(tail_rotate_dict.keys()):

                rotate_value = tail_rotate_dict[joint_name]

                if not base_utility.vector.is_same(
                    rotate, rotate_value
                ):
                    is_hit = True

            else:
                if not base_utility.vector.is_same(
                    rotate, [0, 0, 0]
                ):
                    is_hit = True

        if check_scale:
            scale_dict = {}

            if is_character:
                scale_dict_list = [
                    {'root': 0.9, 'C_head': 1.111111},
                    {'root': 0.95, 'C_head': 1.052632},
                    {'root': 1, 'C_head': 1},
                    {'root': 1.04, 'C_head': 0.961538},
                ]

                scale_dict = scale_dict_list[data_info.model_size]

            if joint_name in list(scale_dict.keys()):
                scale_value = scale_dict[joint_name]

                if not base_utility.vector.is_same(
                    scale, [scale_value, scale_value, scale_value]
                ):
                    is_hit = True

            else:
                if not base_utility.vector.is_same(
                    scale, [1, 1, 1]
                ):
                    is_hit = True

        if not is_hit:
            param_item.unerror_target_list.append(joint)
            continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_joint_orient(param_item, arg):
    """
    ジョイントの軸方向をチェック
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    if not cmds.objExists(root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return

    param_item.check_target_list = all_joint_list

    for joint in all_joint_list:

        is_check_joint = True

        joint_name = joint.split('|')[-1]

        check_orient_sp_target_list = []

        if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
            check_orient_sp_target_list.append('Ear_')
        elif param_item.main.chara_info.part_info.data_type.find('tail') >= 0:
            check_orient_sp_target_list.append('Tail0_')

        if joint_name.startswith('Sp_'):

            is_check_joint = False

            for check_orient_sp_target in check_orient_sp_target_list:

                if joint_name.find(check_orient_sp_target) >= 0:
                    is_check_joint = True
                    break

        if not is_check_joint:
            continue

        orient = None
        if cmds.objExists(joint) and cmds.attributeQuery('jointOrient', node=joint, exists=True):
            orient = cmds.getAttr('{}.{}'.format(joint, 'jointOrient'))[0]

        is_hit = False
        error_attr_list = []

        if joint_name == 'Sp_Hi_Tail0_B_00':
            if not base_utility.vector.is_same(
                orient, [0.0, 180.0, 0.0]
            ):
                is_hit = True

        else:
            # 微小値が入ることがあるため厳密に0と同値判定でチェック
            if not orient[0] == 0.0:
                is_hit = True
                error_attr_list.append('rotateX({})'.format(str(orient[0])))
            if not orient[1] == 0.0:
                is_hit = True
                error_attr_list.append('rotateY({})'.format(str(orient[1])))
            if not orient[2] == 0.0:
                is_hit = True
                error_attr_list.append('rotateZ({})'.format(str(orient[2])))

        error_attr_str = ' / '.join(error_attr_list)

        if not is_hit:
            param_item.unerror_target_list.append(joint)
            continue

        separator = param_item.root.info_window.detail_separator
        param_item.error_target_list.append('{0}{1}{2}'.format(joint, separator, error_attr_str))


# ==================================================
def check_joint_overlap_naming(param_item, arg):
    """
    ジョイント名が重複していないかをチェック
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    if not cmds.objExists(root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return

    param_item.check_target_list = all_joint_list

    for joint in all_joint_list:

        joint_short_name = joint.split('|')[-1]

        exist = False
        for diff_joint in all_joint_list:

            if diff_joint == joint:
                continue

            diff_joint_short_name = diff_joint.split('|')[-1]

            if diff_joint_short_name != joint_short_name:
                continue

            exist = True
            break

        if not exist:
            param_item.unerror_target_list.append(joint)
            continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_ear_joint_position(param_item, arg):
    """
    耳のジョイントのトランスフォーム情報のチェック
    """

    # ------------------------------
    # 設定

    target_list = [
        'Sp_He_Ear0_R_00',
        'Ear_01_R',
        'Sp_He_Ear0_R_01',
        'Ear_02_R',
        'Sp_He_Ear0_R_02',
        'Ear_03_R',
        'Sp_He_Ear0_L_00',
        'Ear_01_L',
        'Sp_He_Ear0_L_01',
        'Ear_02_L',
        'Sp_He_Ear0_L_02',
        'Ear_03_L',
    ]

    # ------------------------------
    # 情報

    param_item.info_target_list = target_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_list

    this_set_list = [
        [target_list[0], target_list[1]],
        [target_list[2], target_list[3]],
        [target_list[4], target_list[5]],
        [target_list[6], target_list[7]],
        [target_list[8], target_list[9]],
        [target_list[10], target_list[11]],
    ]

    for this_set in this_set_list:

        if not this_set[0] or not cmds.objExists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not this_set[0] or not cmds.objExists(this_set[1]):
            param_item.error_target_list.extend(this_set)
            continue

        src_trans = cmds.xform(
            this_set[0], q=True, t=True, ws=True)

        dst_trans = cmds.xform(
            this_set[1], q=True, t=True, ws=True)

        if base_utility.vector.is_same(
            src_trans, dst_trans
        ):
            param_item.unerror_target_list.extend(this_set)
            continue

        param_item.error_target_list.extend(this_set)


# ==================================================
def check_bust_joint_position(param_item, arg):
    """
    特別衣装のバストジョイントのポジションをチェック
    """

    # ------------------------------
    # 設定

    data_id = param_item.main.chara_info.part_info.data_id

    if data_id.find('bdy') < 0:
        return

    root_node = param_item.main.chara_info.part_info.root_node

    if data_id.find('bdy0') >= 0:
        bust_id = 2
    else:
        bust_id = param_item.main.chara_info.data_info.bust_id

    if not root_node or bust_id is None:
        return

    bust_type = ''
    if int(bust_id) == 0:
        bust_type = 'SS'
    elif int(bust_id) == 1:
        bust_type = 'S'
    elif int(bust_id) == 2:
        bust_type = 'M'
    elif int(bust_id) == 3:
        bust_type = 'L'
    elif int(bust_id) == 4:
        bust_type = 'LL'

    check_target_param_list = [
        {
            'joint': 'Sp_Ch_Bust0_L_00',
            'position': {
                'all': [3.9000000000000044, 122.24237448153032, -1.3106414930759267]
            }
        },
        {
            'joint': 'Sp_Ch_Bust0_R_00',
            'position': {
                'all': [-3.9, 122.24200000000005, -1.3106400000000122]
            }
        },
        {
            'joint': 'Sp_Ch_Bust0_L_01',
            'position': {
                'SS': [4.986458040744821, 120.15639197168143, 2.6890942349823312],
                'S': [4.986458040744821, 120.15639197168143, 2.6890942349823312],
                'M': [4.986458040744821, 120.15639197168143, 2.6890942349823312],
                'L': [4.98659947668062, 119.54337124597265, 2.733490936967255],
                'LL': [4.986433245675956, 118.84560202194379, 2.7827239512113153]
            }
        },
        {
            'joint': 'Sp_Ch_Bust0_R_01',
            'position': {
                'SS': [-4.986458040744813, 120.15601749015113, 2.6890957280582333],
                'S': [-4.986458040744813, 120.15601749015113, 2.6890957280582333],
                'M': [-4.986458040744813, 120.15601749015113, 2.6890957280582333],
                'L': [-4.986599476680611, 119.54299676444235, 2.7334924300431545],
                'LL': [-4.986433245675947, 118.84522754041349, 2.782725444287213]
            }
        }
    ]

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node + '(バストサイズ{})'.format(bust_type))

    if not param_item.is_check_data:
        return
    # ------------------------------
    # チェック

    if not cmds.objExists(root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return

    check_target_joint_param_list = []

    for joint in all_joint_list:

        joint_name = joint.split('|')[-1]

        for param in check_target_param_list:

            check_target_joint = param['joint']

            if joint_name != check_target_joint:
                continue

            if 'all' in param['position']:
                check_target_joint_translate = param['position']['all']
            else:
                check_target_joint_translate = param['position'][bust_type]

            check_target_joint_param_list.append(
                [check_target_joint, check_target_joint_translate]
            )

    if not check_target_joint_param_list:
        return

    param_item.check_target_list = [param[0] for param in check_target_joint_param_list]

    all_joint_list = param_item.main.chara_info.part_info.joint_list

    for param in check_target_joint_param_list:

        tmp_joint = param[0]
        joint = ''
        for all_joint in all_joint_list:
            if all_joint.endswith(tmp_joint):
                joint = all_joint
                break

        if not joint:
            param_item.error_target_list.append(tmp_joint)
            continue

        original_bust_joint_translate = param[1]
        target_bust_joint_translate = cmds.xform(joint, q=True, ws=True, translation=True)

        if round(original_bust_joint_translate[0], 2) == round(target_bust_joint_translate[0], 2):
            if round(original_bust_joint_translate[1], 2) == round(target_bust_joint_translate[1], 2):
                if round(original_bust_joint_translate[2], 2) == round(target_bust_joint_translate[2], 2):
                    param_item.unerror_target_list.append(joint)
                    continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_bust_joint_orient(param_item, arg):
    """
    特別衣装のバストジョイントのオリエントをチェック
    """

    # ------------------------------
    # 設定

    data_id = param_item.main.chara_info.part_info.data_id

    if data_id.find('bdy') < 0:
        return

    root_node = param_item.main.chara_info.part_info.root_node

    if data_id.find('bdy0') >= 0:
        bust_id = 2
    else:
        bust_id = param_item.main.chara_info.data_info.bust_id

    if not root_node or bust_id is None:
        return

    bust_type = ''
    if int(bust_id) == 0:
        bust_type = 'SS'
    elif int(bust_id) == 1:
        bust_type = 'S'
    elif int(bust_id) == 2:
        bust_type = 'M'
    elif int(bust_id) == 3:
        bust_type = 'L'
    elif int(bust_id) == 4:
        bust_type = 'LL'

    check_orient_sp_target_list = [
        'Sp_Ch_Bust0_L_00',
        'Sp_Ch_Bust0_R_00',
    ]

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node + '(バストサイズ{})'.format(bust_type))

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    if not cmds.objExists(root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return

    target_bust_joint_list = []

    for joint in all_joint_list:

        joint_name = joint.split('|')[-1]

        if joint_name in check_orient_sp_target_list:
            target_bust_joint_list.append(joint)

    if not target_bust_joint_list:
        return

    param_item.check_target_list = target_bust_joint_list

    for joint in target_bust_joint_list:

        is_hit = False

        left_right_factor = 1

        if joint.find('_R_') >= 0:
            left_right_factor = -1

        orient_x = 30.949
        orient_y = 15.157 * left_right_factor
        orient_z = 1.109 * left_right_factor

        if bust_type == 'L':
            orient_x = 37.033
            orient_y = 15.0 * left_right_factor
            orient_z = 1.097 * left_right_factor
        elif bust_type == 'LL':
            orient_x = 42.958
            orient_y = 14.826 * left_right_factor
            orient_z = 1.083 * left_right_factor

        orient = None
        if cmds.objExists(joint) and cmds.attributeQuery('jointOrient', node=joint, exists=True):
            orient = cmds.getAttr('{}.{}'.format(joint, 'jointOrient'))[0]

        if not base_utility.vector.is_same(
            orient, [orient_x, orient_y, orient_z]
        ):
            is_hit = True

        if not is_hit:
            param_item.unerror_target_list.append(joint)
            continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_hip_joint_position(param_item, arg):
    """
    Hipジョイントの位置確認
    """
    # ------------------------------
    # 情報

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    hip_original_translate = param_item.main.chara_info.part_info.hip_original_translate
    if not hip_original_translate:
        return

    param_item.info_target_list = ['{0}|Position|Hip'.format(root_node)]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    param_item.check_target_list = param_item.info_target_list

    for node in param_item.check_target_list:

        if not cmds.objExists(node):
            param_item.error_target_list.append(node)

        hip_translate = None
        if cmds.objExists(node) and cmds.attributeQuery('translate', node=node, exists=True):
            hip_translate = cmds.getAttr('{}.{}'.format(node, 'translate'))[0]

        for i in range(3):
            if (round(hip_translate[i], 3)) != hip_original_translate[i]:
                param_item.error_target_list.append(node)
                break
        else:
            param_item.unerror_target_list.append(node)


# ==================================================
def check_lock_joint_node(param_item, args):
    """
    ジョイントノードがロックされていないかのチェック
    """
    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    if not cmds.objExists(root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return

    param_item.check_target_list = all_joint_list

    attr_list = ['translate', 'rotate', 'scale']
    direction_list = ['X', 'Y', 'Z']

    for joint in all_joint_list:

        is_lock = False

        for attr in attr_list:

            for direction in direction_list:

                attr_str = '{0}.{1}{2}'.format(joint, attr, direction)
                tmp_lock = cmds.getAttr(attr_str, lock=True)

                if tmp_lock:
                    is_lock = True
                    break

            if is_lock:
                break

        if is_lock:
            param_item.error_target_list.append(joint)
        else:
            param_item.unerror_target_list.append(joint)


def check_ex_joint_count(param_item, arg):
    """
    セカンダリジョイントの数をチェック
    """

    # ------------------------------
    # 設定

    data_info = param_item.main.chara_info.data_info
    data_type = param_item.main.chara_info.data_type

    sim_limit_count = 10000
    ex_limit_count = 10000

    if data_type == model_define.AVATAR_DATA_TYPE:
        sim_limit_count = 92
        ex_limit_count = 30

    if data_type == model_define.UNIT_DATA_TYPE:
        sim_limit_count = 50
        ex_limit_count = 50

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    if not cmds.objExists(root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    all_joint_list = cmds.listRelatives(
        root_node, ad=True, f=True, typ='joint')

    if not all_joint_list:
        return

    wpn_all_joint_list = []

    if data_info.has_weapon:
        wpn_file = model_id_finder.create_scene_name(
            model_define.WEAPON_DATA_TYPE,
            param_item.main.chara_info.data_main_id,
            param_item.main.chara_info.data_sub_id)
        wpn_path = model_id_finder.get_maya_file_path(wpn_file)

        wpn_namespace = 'temp_check_wpn'
        wpn_root = '{}:{}'.format(
            wpn_namespace, os.path.splitext(wpn_file)[0])

        if os.path.exists(wpn_path):
            base_utility.reference.load(wpn_path, wpn_namespace)

            if base_utility.reference.exists(wpn_path, wpn_namespace):
                if wpn_root and cmds.objExists(wpn_root):
                    joints = cmds.listRelatives(
                        wpn_root, ad=True, f=True, typ='joint')
                    wpn_all_joint_list = \
                        [j.replace(wpn_namespace + ':', '') for j in joints]

            base_utility.reference.unload(wpn_path, wpn_namespace)

    is_sim = lambda j: j.split('|')[-1].startswith(model_define.SIM_PREFIX)
    is_ex = lambda j: j.split('|')[-1].startswith(model_define.EXTRA_JOINT_PREFIX)
    is_prim = lambda j: re.match('.*\|root\d(\|[^\|]+)?$', j)

    sim_joint_list = [j for j in all_joint_list if is_sim(j)]
    ex_joint_list = [j for j in all_joint_list if is_ex(j)]
    wpn_ex_joint_list = [j for j in wpn_all_joint_list if not is_prim(j)]

    param_item.check_target_list.extend(sim_joint_list)
    param_item.check_target_list.extend(ex_joint_list)
    param_item.check_target_list.extend(wpn_ex_joint_list)
    
    sim_count = len(sim_joint_list)
    ch_ex_count = len(ex_joint_list)
    wpn_ex_count = len(wpn_ex_joint_list)
    ex_count = ch_ex_count + wpn_ex_count

    sim_message = 'SIM: {1} / {0} joints'.format(sim_limit_count, sim_count)
    ex_message = 'EX: {1} (Unit: {2}, Weapon: {3}) / {0} joints'.format(
        ex_limit_count, ex_count, ch_ex_count, wpn_ex_count)

    sim_error_count = sim_count - sim_limit_count
    ex_error_count = ex_count - ex_limit_count

    if sim_error_count > 0:
        sim_error_message = ' ({0} joints over)'.format(sim_error_count)
        param_item.error_target_list.append(sim_message + sim_error_message)
    else:
        param_item.unerror_target_list.append(sim_message)

    if ex_error_count > 0:
        ex_error_message = ' ({0} joints over)'.format(ex_error_count)
        param_item.error_target_list.append(ex_message + ex_error_message)
    else:
        param_item.unerror_target_list.append(ex_message)

# endregion

# region アウトライン系


# ==================================================
def check_outline_exist(param_item, arg):
    """
    _Outlineノードが存在するかチェック
    """

    # ------------------------------
    # 情報

    base_mesh_list = model_mesh_finder.get_all_base_mesh_list(
        param_item.main.chara_info.part_info.root_node)

    outline_list = []
    
    for base_mesh in base_mesh_list:
        
        if '_Alpha' in base_mesh:
            continue

        outline_list.append(model_mesh_finder.get_outline_mesh_name(base_mesh))

    if not outline_list:
        return

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in outline_list:

        param_item.check_target_list.append(mesh)

        if not mesh or not cmds.objExists(mesh):
            param_item.error_target_list.append(mesh)
            continue

        param_item.unerror_target_list.append(mesh)


# ==================================================
def check_outline_vtx_position(param_item, arg):
    """
    _Outlineノードの頂点位置が元モデルと同一かチェック
    """

    # ------------------------------
    # 情報

    outline_list = model_mesh_finder.get_all_outline_mesh_list(
        param_item.main.chara_info.part_info.root_node)

    if not outline_list:
        return

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in outline_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        # 元ノードを取得
        org_mesh = mesh.replace('_Outline', '')

        if not org_mesh or not cmds.objExists(org_mesh):
            continue

        org_vtx_pos_info_list = base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
            org_mesh, True
        )
        vtx_pos_info_list = base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
            mesh, True)

        if len(org_vtx_pos_info_list) != len(vtx_pos_info_list):
            param_item.error_target_list.extend(vertex_list)
            continue

        for (org_vtxs, vtxs) in zip(org_vtx_pos_info_list, vtx_pos_info_list):
            index = org_vtxs[0]
            for (org_vtx_pos, vtx_pos) in zip(org_vtxs[1], vtxs[1]):
                if not base_utility.value.is_same(org_vtx_pos, vtx_pos, 0.00001):
                    param_item.error_target_list.append(
                        mesh + ".vtx[%s]" % str(index))
                    break

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_outline_vtx_color(param_item, arg):
    """
    _Outlineノードの頂点カラーが元モデルと同一かチェック
    """

    # ------------------------------
    # 情報

    outline_list = model_mesh_finder.get_all_outline_mesh_list(
        param_item.main.chara_info.part_info.root_node)

    if not outline_list:
        return

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    
    separator = param_item.root.info_window.detail_separator

    for mesh in outline_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        # 元ノードを取得
        org_mesh = mesh.replace("_Outline", "")

        if not org_mesh or not cmds.objExists(org_mesh):
            error_str = u'元のモデル（{}）が存在しません。'.format(org_mesh)
            param_item.error_target_list.append(
                '{0}{1}{2}'.format(mesh, separator, error_str))
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        org_vertex_list = base_utility.mesh.get_vertex_list(org_mesh) or []

        if len(org_vertex_list) != len(vertex_list):
            error_str = u'元のモデル（{}）と頂点数が一致しません。'.format(org_mesh)
            param_item.error_target_list.append(
                '{0}{1}{2}'.format(mesh, separator, error_str))
            continue

        colorsets = base_utility.mesh.colorset.get_colorset_list(mesh)

        if not colorsets:
            continue

        org_colorsets = base_utility.mesh.colorset.get_colorset_list(org_mesh)

        if org_colorsets != colorsets:
            error_str = u'元のモデル（{}）とカラーセットが一致しません。'.format(org_mesh)
            param_item.error_target_list.append(
                '{0}{1}{2}'.format(mesh, separator, error_str))
            continue

        # 元モデルの存在と頂点数、カラーセットの一致を確認してからチェックリストに追加
        param_item.check_target_list.extend(vertex_list)

        org_current_colorset = base_utility.mesh.colorset.get_current(org_mesh)
        current_colorset = base_utility.mesh.colorset.get_current(mesh)

        for colorset in colorsets:
            base_utility.mesh.colorset.set_current(mesh, colorset)
            vtx_color_list = base_utility.mesh.vertex_color.get_all_vertex_color_info_list(mesh) or []

            base_utility.mesh.colorset.set_current(org_mesh, colorset)
            org_vtx_color_list = base_utility.mesh.vertex_color.get_all_vertex_color_info_list(
                org_mesh) or []

            for (org_vtxs, vtxs) in zip(org_vtx_color_list, vtx_color_list):
                index = org_vtxs[0]
                for (org_vtx_color, vtx_color) in zip(org_vtxs[2], vtxs[2]):
                    if org_vtx_color != vtx_color:
                        param_item.error_target_list.append(
                            mesh + ".vtx[%s]" % str(index) + separator + colorset)
                        break

        base_utility.mesh.colorset.set_current(org_mesh, org_current_colorset)
        base_utility.mesh.colorset.set_current(mesh, current_colorset)

    # エラー外のチェック
    for target in param_item.check_target_list:

        if target in param_item.error_target_list:
            continue

        param_item.unerror_target_list.append(target)


# ==================================================
def check_outline_softedge(param_item, arg):
    """
    _Outlineノードのエッジがすべてソフトエッジになっているかチェック
    境界エッジはハードエッジにしかならないので除く
    """

    # ------------------------------
    # 情報

    outline_list = model_mesh_finder.get_all_outline_mesh_list(
        param_item.main.chara_info.part_info.root_node)

    if not outline_list:
        return

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in outline_list:

        if not mesh or not cmds.objExists(mesh):
            continue

        edge_list = cmds.ls('{}.e[*]'.format(mesh), l=True, fl=True)
        info_list = cmds.polyInfo(edge_list, ev=True)

        if not edge_list:
            continue

        param_item.check_target_list.extend(edge_list)

        # 全エッジ番号で境界エッジを検索する
        edge_border_index_list = cmds.polySelect(mesh, q=True, eb=list(range(len(edge_list))))
        edge_reg = 'e\[([0-9]*)\]'

        for edge, info in zip(edge_list, info_list):

            match_obj = re.search(edge_reg, edge)
            edge_index = None

            if match_obj:
                edge_index = int(match_obj.group(1))
            else:
                continue

            # 境界エッジはセーフ
            if edge_border_index_list:
                if edge_index in edge_border_index_list:
                    param_item.unerror_target_list.append(edge)
                    continue

            if info.find('Hard') >= 0:
                param_item.error_target_list.append(edge)
            else:
                param_item.unerror_target_list.append(edge)

# endregion

# region その他


# ==================================================
def check_namespace(param_item, arg):
    """
    不要なネームスペースのチェック
    """

    # ------------------------------
    # 情報

    param_item.info_target_list = ['scene']

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = cmds.ls(l=True)

    for node in param_item.check_target_list:

        if node.find(':') < 0:
            param_item.unerror_target_list.append(node)
            continue

        param_item.error_target_list.append(node)


# ==================================================
def check_transform_with_no_key(param_item, arg):
    """
    キーが打たれていないかの確認
    """

    # ------------------------------
    # 情報

    param_item.info_target_list = \
        [param_item.main.chara_info.part_info.root_node]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = \
        cmds.ls(param_item.info_target_list, dag=True, l=True, typ="transform")

    for transform in param_item.check_target_list:

        if cmds.keyframe(transform, q=True, kc=True) == 0:
            param_item.unerror_target_list.append(transform)
            continue

        param_item.error_target_list.append(transform)


# ==================================================
def check_locator_with_no_bindpose(param_item, arg):
    """
    ロケーターに不要バインドポーズがないかの確認
    """

    # ------------------------------
    # 情報

    all_locator_list = param_item.main.chara_info.part_info.locator_list
    root_node = param_item.main.chara_info.part_info.root_node
    target_locator_list = []

    if not all_locator_list or not root_node:
        return

    for locator in all_locator_list:

        # root_node直下のロケーターのみが対象
        if len(locator.replace('{}|'.format(root_node), '').split('|')) == 1:
            target_locator_list.append(locator)

    if not target_locator_list:
        return

    param_item.info_target_list = target_locator_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_locator_list

    for locator in param_item.check_target_list:

        if cmds.listConnections(locator, t='dagPose'):
            param_item.error_target_list.append(locator)
            continue

        param_item.unerror_target_list.append(locator)


# ==================================================
def check_multiple_bindpose(param_item, arg):
    """
    バインドポーズが複数存在しないか確認
    """

    # ------------------------------
    # 設定

    target_joint_list = []

    joint_list = cmds.ls(l = True, typ = 'joint')

    pattern = re.compile(r'^.*\|grp_joint\|.*$')

    for joint in joint_list:
        if pattern.match(joint):
            target_joint_list.append(joint)

    if not target_joint_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_joint_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_joint_list)

    for joint in target_joint_list:
        
        pose_list = cmds.dagPose(joint, q=True, bp=True, sl=True)
        
        if pose_list and len(pose_list) > 1:
            param_item.error_target_list.append(joint)
        else:
            param_item.unerror_target_list.append(joint)


# ==================================================
def check_animation_layer(param_item, arg):
    """
    不要なアニメーションレイヤーのチェック
    """

    # ------------------------------
    # 情報

    this_scene = cmds.file(q=True, sn=True, exn=True)

    param_item.info_target_list = [this_scene]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = [this_scene]

    anim_layer_list = cmds.ls(typ='animLayer')

    if anim_layer_list:
        param_item.error_target_list.extend(anim_layer_list)
    else:
        param_item.unerror_target_list.append(this_scene)


# ==================================================
def check_particular_node_position(param_item, args):
    """
    「mdl_bdyXXXX_XX」「Position」「M_Body」ノードの位置が0かどうかのチェック
    """
    # ------------------------------
    # 情報

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    param_item.info_target_list = [root_node, '{0}|Position'.format(root_node), '{0}|M_Body'.format(root_node)]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    param_item.check_target_list = param_item.info_target_list

    for node in param_item.check_target_list:

        if not cmds.objExists(node):
            param_item.error_target_list.append(node)

        translate = None
        if cmds.objExists(node) and cmds.attributeQuery('translate', node=node, exists=True):
            translate = cmds.getAttr('{}.{}'.format(node, 'translate'))[0]

        if translate == [0.0, 0.0, 0.0]:
            param_item.unerror_target_list.append(node)
        else:
            param_item.error_target_list.append(node)


# ==================================================
def check_particular_node_pivot_position(param_item, args):
    """
    grp_joint, grp_meshノードのピボット位置が原点かどうかのチェック
    """
    # ------------------------------
    # 設定

    target_node_list = []

    part_info = param_item.main.chara_info.part_info

    root_node = part_info.root_node
    grp_joint_pattern = re.compile(part_info.grp_joint_pattern)
    grp_mesh_pattern = re.compile(part_info.grp_mesh_pattern)

    transform_list = cmds.ls(l = True, typ = 'transform')

    for transform in transform_list:
        if transform == root_node:
            target_node_list.append(transform)
        if grp_joint_pattern.match(transform):
            target_node_list.append(transform)
        if grp_mesh_pattern.match(transform):
            target_node_list.append(transform)

    target_node_list.extend(model_mesh_finder.get_all_mesh_list(root_node))

    if not target_node_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list = target_node_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = param_item.info_target_list

    for node in param_item.check_target_list:
        pivots = cmds.xform(node, q=True, pivots=True)

        if pivots == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]:
            param_item.unerror_target_list.append(node)
        else:
            param_item.error_target_list.append(node)

# endregion
