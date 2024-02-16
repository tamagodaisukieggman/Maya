# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

# region import

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
except Exception:
    pass

import os
import re
import math
from decimal import Decimal, ROUND_HALF_UP

import maya.cmds as cmds
import maya.api.OpenMaya as om

from . import define

from ..base_common import utility as base_utility
from ..base_common import classes as base_class

from ..glp_common import classes as glp_class

# endregion

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
    必須メッシュの存在確認
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

        if base_utility.node.exists(mesh):
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_name(param_item, arg):
    """
    メッシュ名がレギュレーションから逸脱していないか確認
    """
    # ------------------------------
    # 設定

    target_mesh_list = []

    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

        # 体型差分アリの場合はsuffix有りバージョンも追加
        if param_item.main.chara_info.is_common_body:
            base_grp_name, base_mesh_name = mesh_param['name'].rsplit('|', 1)
            for suffix in define.BODY_DEFFERENCE_TARGET_SUFFIX_LIST:
                target_mesh_list.append(base_grp_name + suffix + '|' + base_mesh_name + suffix)

    for outline_mesh_param in param_item.main.chara_info.part_info.outline_mesh_param_list:
        target_mesh_list.append(outline_mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)
    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    mesh_shape_list = cmds.ls(type='mesh', noIntermediate=True)

    mesh_transform_list = []
    for mesh_shape in mesh_shape_list:
        mesh_transform = cmds.ls(cmds.listRelatives(mesh_shape, p=True), l=True)
        if not mesh_transform:
            continue

        mesh_transform_list.append(mesh_transform[0])

    for mesh in mesh_transform_list:

        if mesh in target_mesh_list:
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_poly_count(param_item, arg):
    """
    メッシュのポリゴン数をチェック
    """

    target_poly_count = param_item.main.chara_info.part_info.polygon_limit

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

    param_item.add_require_value_to_label('{0}以内'.format(target_poly_count))

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
    # 適当なIDでinfoを作り、各パートの上限数を取得して合算する
    target_sum_poly_min_count = 0

    if param_item.main.chara_info.part_info.is_mini:
        sample_info = glp_class.info.chara_info.CharaInfo()
        sample_info.create_info('mdl_mbdy1001_00', is_create_all_info=True)
        target_sum_poly_min_count += sample_info.head_part_info.polygon_limit
        target_sum_poly_min_count += sample_info.body_part_info.polygon_limit
        target_sum_poly_min_count += sample_info.tail_part_info.polygon_limit

        sample_info = glp_class.info.chara_info.CharaInfo()
        sample_info.create_info('mdl_mchr0001_00_face0', is_create_all_info=True)
        target_sum_poly_min_count += sample_info.part_info.polygon_limit

    else:
        sample_info = glp_class.info.chara_info.CharaInfo()
        sample_info.create_info('mdl_bdy1001_00', is_create_all_info=True)
        target_sum_poly_min_count += sample_info.head_part_info.polygon_limit
        target_sum_poly_min_count += sample_info.body_part_info.polygon_limit
        target_sum_poly_min_count += sample_info.tail_part_info.polygon_limit

    param_item.add_require_value_to_label('{0}以内'.format(target_sum_poly_min_count))

    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        check_mesh_poly_sum_count_base(param_item, target_sum_poly_min_count, True, arg)

    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        check_mesh_poly_sum_count_base(param_item, target_sum_poly_min_count, False, arg)


# ==================================================
def check_mesh_poly_sum_count_base(param_item, target_sum_poly_min_count, from_head, arg):
    """
    ユニーク頭部と勝負服の合算ポリ数をチェック
    """

    # ------------------------------
    # 設定

    is_mini = param_item.main.chara_info.is_mini

    # 対応しうる身体or頭部を検索
    opposit_part = 'body' if from_head else 'head'
    opposit_finder = glp_class.path_finder.path_finder.PathFinder(opposit_part, param_item.main.chara_info.data_main_id, is_mini)
    opposit_files = [x for x in opposit_finder.model_ma_list if os.path.exists(x)]

    if not opposit_files:
        return

    check_dict_list = []
    for opposit_file in opposit_files:

        check_dict = {
            'head_part_info': None,
            'head_path': '',
            'body_part_info': None,
            'body_path': '',
            'tail_part_info': None,
            'tail_path': '',
            'mini_face_part_info': None,
            'mini_face_path': '',
            'info_str': ''
        }

        # chara_info系の取得
        tmp_opposit_info = glp_class.info.chara_info.CharaInfo()
        tmp_opposit_info.create_info(opposit_file, '', True)

        if not tmp_opposit_info.part_info or not tmp_opposit_info.tail_part_info:
            continue

        if from_head:
            check_dict['head_part_info'] = param_item.main.chara_info.part_info
            check_dict['body_part_info'] = tmp_opposit_info.part_info
            check_dict['tail_part_info'] = tmp_opposit_info.tail_part_info
        else:
            check_dict['head_part_info'] = tmp_opposit_info.part_info
            check_dict['body_part_info'] = param_item.main.chara_info.part_info
            check_dict['tail_part_info'] = param_item.main.chara_info.tail_part_info

        if is_mini:
            m_face_info = glp_class.info.chara_info.CharaInfo()
            m_face_info.create_info(define.MINI_FACE_PATH, '', True)
            check_dict['mini_face_part_info'] = m_face_info.part_info

        # path系の取得
        opposit_info = check_dict['body_part_info']
        if not from_head:
            opposit_info = check_dict['head_part_info']

        opposit_finder = glp_class.path_finder.path_finder.PathFinder(
            opposit_part, '{}_{}'.format(opposit_info.main_id, opposit_info.sub_id), is_mini)
        tail_finder = glp_class.path_finder.path_finder.PathFinder(
            'tail', '{}_{}'.format(check_dict['tail_part_info'].main_id, check_dict['tail_part_info'].sub_id), is_mini)

        if not opposit_finder.model_ma_list or not tail_finder.model_ma_list:
            continue

        if from_head:
            check_dict['head_path'] = cmds.file(q=True, sn=True)
            check_dict['body_path'] = opposit_finder.model_ma_list[0]
        else:
            check_dict['head_path'] = opposit_finder.model_ma_list[0]
            check_dict['body_path'] = cmds.file(q=True, sn=True)
        check_dict['tail_path'] = tail_finder.model_ma_list[0]

        if is_mini:
            check_dict['mini_face_path'] = define.MINI_FACE_PATH

        if is_mini and not os.path.exists(check_dict['mini_face_path']) or\
                not os.path.exists(check_dict['head_path']) or\
                not os.path.exists(check_dict['body_path']) or\
                not os.path.exists(check_dict['tail_path']):
            continue

        head_file_name = os.path.basename(check_dict['head_path'])
        body_file_name = os.path.basename(check_dict['body_path'])
        tail_file_name = os.path.basename(check_dict['tail_path'])

        if not is_mini:
            check_dict['info_str'] = '{}, {}, {}'.format(head_file_name, body_file_name, tail_file_name)
        else:
            m_face_file_name = os.path.basename(check_dict['mini_face_path'])
            check_dict['info_str'] = '{}, {}, {}, {}'.format(head_file_name, body_file_name, tail_file_name, m_face_file_name)

        check_dict_list.append(check_dict)

    opposit_ref_name_space = '__BODY_MODEL_REF__' if from_head else '__HEAD_MODEL_REF__'
    tail_ref_name_space = '__TAIL_MODEL_REF__'
    m_face_ref_name_space = '__M_FACE_MODEL_REF__'

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

        ref_ctrl_list = []

        head_mesh_list = check_dict['head_part_info'].mesh_list[:]
        body_mesh_list = check_dict['body_part_info'].mesh_list[:]
        tail_mesh_list = check_dict['tail_part_info'].mesh_list[:]
        if is_mini:
            face_mesh_list = check_dict['mini_face_part_info'].mesh_list[:]

        # 最終的に集計するメッシュ名のリスト
        final_mesh_list = []

        if from_head:
            final_mesh_list = head_mesh_list[:]
            for body_mesh in body_mesh_list:
                final_mesh_list.append(body_mesh.replace('|', '|{}:'.format(opposit_ref_name_space)))

        else:
            final_mesh_list = body_mesh_list[:]
            for head_mesh in head_mesh_list:
                final_mesh_list.append(head_mesh.replace('|', '|{}:'.format(opposit_ref_name_space)))

        for tail_mesh in tail_mesh_list:
            final_mesh_list.append(tail_mesh.replace('|', '|{}:'.format(tail_ref_name_space)))

        if is_mini:
            for face_mesh in face_mesh_list:
                final_mesh_list.append(face_mesh.replace('|', '|{}:'.format(m_face_ref_name_space)))

        final_mesh_list = __get_poly_check_mesh_list(final_mesh_list)

        # ロード/失敗したらエラーで返す
        target_path_list = ['', '']
        if from_head:
            target_path_list = [check_dict['body_path'], check_dict['tail_path']]
        else:
            target_path_list = [check_dict['head_path'], check_dict['tail_path']]
        target_namespace_list = [opposit_ref_name_space, tail_ref_name_space]
        error_ref_list = []

        if is_mini:
            target_path_list.append(check_dict['mini_face_path'])
            target_namespace_list.append(m_face_ref_name_space)

        for target_path, target_namespace in zip(target_path_list, target_namespace_list):

            temp_ref_ctrl = base_class.reference.ReferenceController()
            temp_ref_ctrl.load_using_no_plugin_tmp(target_path, target_namespace, True)

            if temp_ref_ctrl.is_error:
                error_ref_list.append(temp_ref_ctrl)

            ref_ctrl_list.append(temp_ref_ctrl)

        if error_ref_list:
            for error_ref in error_ref_list:
                param_item.error_target_list.append('{0}が{1}ため'.format(error_ref.original_file_path, error_ref.reason))

            for ref_ctrl in ref_ctrl_list:
                ref_ctrl.unload(unload_hard=True)
            continue

        # チェック
        is_in_limit, all_tri_count, this_tri_limit = __check_mesh_poly_count_base(final_mesh_list, target_sum_poly_min_count)
        param_item.check_target_list.append(check_dict['info_str'])

        # アンロード
        for ref_ctrl in ref_ctrl_list:
            ref_ctrl.unload(unload_hard=True)

        # チェック結果の記載
        over_count = 'NO_DATA'
        if all_tri_count:
            over_count = all_tri_count - this_tri_limit

        if not is_in_limit:
            param_item.error_target_list.append('{} ({}/{} tris: {} tris over)'.format(check_dict['info_str'], all_tri_count, this_tri_limit,
                                                                                       over_count))
        else:
            param_item.unerror_target_list.append('{} ({}/{} tris)'.format(check_dict['info_str'], all_tri_count, this_tri_limit))


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

        if not base_utility.transform.exists(mesh):
            continue

        # 作業途中でグループ名などで名前が衝突するとpolyEvaluateがエラーになるためメッシュか確認
        if not __is_mesh(mesh):
            continue

        this_count = cmds.polyEvaluate(mesh, triangle=True)

        all_tri_count += this_count

    if all_tri_count <= target_poly_min_count:
        is_in_limit = True

    return is_in_limit, all_tri_count, count_limit


# ==================================================
def __is_mesh(transform):
    """与えられたトランスフォーム名のシェイプがメッシュか確認する

    Args:
        transform (str): 確認対象の(存在している)トランスフォーム名

    Returns:
        bool: メッシュか
    """
    has_mesh = False
    shape_list = cmds.listRelatives(transform, shapes=True) or []
    for shape in shape_list:
        # メッシュか確認する
        if cmds.objectType(shape) == 'mesh':
            has_mesh = True
            break

    return has_mesh


# ==================================================
def check_mesh_transform(param_item, arg):
    """
    メッシュのトランスフォーム情報をチェック
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    param_item.add_require_value_to_label('translate, rotateはそれぞれ0、scaleは1')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
            continue

        param_item.check_target_list.append(mesh)

        translate = base_utility.attribute.get_value(
            mesh, 'translate'
        )

        rotate = base_utility.attribute.get_value(
            mesh, 'rotate'
        )

        scale = base_utility.attribute.get_value(
            mesh, 'scale'
        )

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

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    param_item.add_require_value_to_label('タイプがlambert')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
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
def check_body_diff_target_mesh(param_item, arg):

    # ------------------------------
    # 設定

    target_mesh_list = []

    m_body_list = cmds.ls('M_Body*', l=True, typ='transform')
    root_node_start_str = param_item.main.chara_info.part_info.root_node
    body_diff_mesh_list = param_item.main.chara_info.part_info.mesh_list

    if not m_body_list:
        return

    for m_body in m_body_list:

        if m_body.find('_Outline') >= 0:
            continue

        if m_body in body_diff_mesh_list:
            continue

        if not m_body.startswith(root_node_start_str):
            continue

        target_mesh_list.append(m_body)

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

        hierarchy_list = mesh.split('|')

        if not len(hierarchy_list) == 3:
            # M_Bodyはルート直下、第二階層のはず
            param_item.error_target_list.append(mesh)
            continue

        this_root = hierarchy_list[1]
        this_m_body = hierarchy_list[2]

        # this_root, this_m_bodyともにdefine.BODY_DEFFERENCE_TARGET_SUFFIX_LISTのどれかに末尾一致のはず
        is_hit = False
        for target_suffix in define.BODY_DEFFERENCE_TARGET_SUFFIX_LIST:

            if this_root.endswith(target_suffix) and this_m_body.endswith(target_suffix):
                is_hit = True
                break

        if not is_hit:
            param_item.error_target_list.append(mesh)
        else:
            param_item.unerror_target_list.append(mesh)


# ==================================================
def check_prop_mesh_pivot(param_item, arg):
    """
    「PropのPivotの位置」チェック
    UIの更新の時とチェック実行時に呼ばれる
    M_PropメッシュのPivotのrotationとscaleがlocal, worldともに0ならOK
    Args:
        param_item (CheckerParamItem): チェック項目のobject
        arg (None): Unused
    """

    # ------------------------------
    # 設定

    # ±PROP_TRANSLATION_ALLOWANCE_LIMIT分、移動値に微小値が入ることを許容する
    PROP_TRANSLATION_ALLOWANCE_LIMIT = 0.001

    target_mesh_list = []

    prop_mesh_list = cmds.ls(['M_Prop*', 'M_ToonProp*'], l=True, typ='transform')
    root_node_start_str = param_item.main.chara_info.part_info.root_node

    if not prop_mesh_list:
        return

    for prop_mesh in prop_mesh_list:

        if prop_mesh.find('_Outline') >= 0:
            continue

        if not prop_mesh.startswith(root_node_start_str):
            continue

        target_mesh_list.append(prop_mesh)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    # UIの更新時はここまで
    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(target_mesh_list)

    for mesh in target_mesh_list:
        pivot_local_list = cmds.xform(mesh, q=True, pivots=True, worldSpace=False)
        pivot_world_list = cmds.xform(mesh, q=True, pivots=True, worldSpace=True)

        if not pivot_local_list or not pivot_world_list:
            param_item.error_target_list.append(mesh)
            continue

        is_under_allowance = True
        for pivot_local in pivot_local_list:
            if not abs(pivot_local) < PROP_TRANSLATION_ALLOWANCE_LIMIT:
                is_under_allowance = False
                break

        if is_under_allowance:
            for pivot_world in pivot_world_list:
                if not abs(pivot_world) < PROP_TRANSLATION_ALLOWANCE_LIMIT:
                    is_under_allowance = False
                    break

        if is_under_allowance:
            param_item.unerror_target_list.append(mesh)
        else:
            param_item.error_target_list.append(mesh)


# endregion

# region NeckEdgeSet系


# ==================================================
def check_neck_edge_set_exists(param_item, arg):
    """
    NeckEdgeSetが存在するかどうか
    """

    # ------------------------------
    # 情報

    param_item.info_target_list.append(define.NECK_EDGE_SET_NAME)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    param_item.check_target_list.append(define.NECK_EDGE_SET_NAME)
    result = check_exists_neck_edge_set()
    if not result:
        param_item.unerror_target_list.append(define.NECK_EDGE_SET_NAME)
    else:
        param_item.error_target_list.append(result.get('error_target_list'))
        param_item.error_info = result.get('error_info')


# ==================================================
def check_neck_edge_normals(param_item, arg):
    """
    NeckEdgeSetの法線方向をチェック
    """

    neck_normal_info = glp_class.neck_normal.NeckNormalInfo()

    # ------------------------------
    # 情報

    target_list = [define.NECK_EDGE_SET_NAME]

    neck_edge_list = get_neck_edge_list()
    vertices = []
    if neck_edge_list:
        vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)
        target_list = vertices

    param_item.info_target_list.extend(target_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    result = check_exists_neck_edge_set()
    if result:
        param_item.error_target_list.extend(result.get('error_target_list'))
        param_item.error_info = result.get('error_info')
        return

    param_item.check_target_list.extend(neck_edge_list)

    select_list = cmds.ls(sl=True, l=True, fl=True)
    cmds.select(cmds.sets(define.NECK_EDGE_SET_NAME, q=True))
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

            this_info_vtx = this_info['vtx']
            neck_normals = this_info['normal']

            if this_info_vtx != vtx:
                continue

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
    # 情報

    target_list = [define.NECK_EDGE_SET_NAME]

    neck_edge_list = get_neck_edge_list()
    vertices = []
    if neck_edge_list:
        vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)
        target_list = vertices

    param_item.info_target_list.extend(target_list)
    param_item.add_require_value_to_label('RGBが[1.0, 1.0, 1.0]')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    result = check_exists_neck_edge_set()
    if result:
        param_item.check_target_list.extend(result.get('error_target_list'))
        param_item.error_target_list.extend(result.get('error_target_list'))
        param_item.error_info = result.get('error_info')
        return

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
    # 情報

    target_list = [define.NECK_EDGE_SET_NAME]

    neck_edge_list = get_neck_edge_list()
    vertices = []
    if neck_edge_list:
        vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)
        target_list = vertices

    param_item.info_target_list.extend(target_list)

    param_item.add_require_value_to_label('Head:0.7, Neck:0.3')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    result = check_exists_neck_edge_set()
    if result:
        param_item.check_target_list.extend(result.get('error_target_list'))
        param_item.error_target_list.extend(result.get('error_target_list'))
        param_item.error_info = result.get('error_info')
        return

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


# ==================================================
def check_neck_edge_vtx_pos(param_item, arg):
    """
    NeckEdgeSetの頂点位置をチェック
    """

    # ------------------------------
    # 設定

    suffix_list = [
        '_Height_SS',
        '_Height_L',
        '_Shape_1',
        '_Shape_2',
        '_Bust_SS',
        '_Bust_S',
        '_Bust_L',
        '_Bust_LL'
    ]

    # 以下運用モデルから計測したHeadから各頂点への方向ベクトル
    default_pos_from_head_list = [
        [0.0, -1.5779866655318244, 3.9121787834167865],
        [1.6488499641418457, -1.129424043461512, 3.2342957544327167],
        [-1.6488499641418457, -1.129424043461512, 3.2342957544327167],
        [2.8118231296539307, -0.6455068071333869, 1.4194979953766254],
        [-2.8118231296539307, -0.6455068071333869, 1.4194979953766254],
        [3.0871293544769287, -0.15591330127401193, -1.082383365631065],
        [-3.0871293544769287, -0.15591330127401193, -1.082383365631065],
        [2.000286102294922, 0.05314736767130057, -2.6636268806457135],
        [-2.000286102294922, 0.05314736767130057, -2.6636268806457135],
        [0.0, -0.02551168994588693, -3.580390663146934],
    ]

    height_ss_pos_from_head_list = [
        [0.0, -1.5779866655318244, 4.019833831787148],
        [1.6941499710083008, -1.129424043461512, 3.32332661628727],
        [-1.6941499710083008, -1.129424043461512, 3.32332661628727],
        [2.88907527923584, -0.6455068071333869, 1.458669929504433],
        [-2.88907527923584, -0.6455068071333869, 1.458669929504433],
        [3.171945333480835, -0.15591330127401193, -1.1119472694396588],
        [-3.171945333480835, -0.15591330127401193, -1.1119472694396588],
        [2.0552420616149902, 0.05314736767130057, -2.7366339874267194],
        [-2.0552420616149902, 0.05314736767130057, -2.7366339874267194],
        [0.0, -0.02551168994588693, -3.6785847854613873],
    ]

    height_l_pos_from_head_list = [
        [0.0, -1.5779866655318244, 3.8493517923355487],
        [1.6211999654769897, -1.129424043461512, 3.1828367996216205],
        [-1.6211999654769897, -1.129424043461512, 3.1828367996216205],
        [2.7646713256835938, -0.6455068071333869, 1.3984718608856586],
        [-2.7646713256835938, -0.6455068071333869, 1.3984718608856586],
        [3.0353612899780273, -0.15591330127401193, -1.0614545059203717],
        [-3.0353612899780273, -0.15591330127401193, -1.0614545059203717],
        [1.966742992401123, 0.05314736767130057, -2.6161815834045026],
        [-1.966742992401123, 0.05314736767130057, -2.6161815834045026],
        [0.0, -0.02551168994588693, -3.5175721359252545],
    ]

    torelance = 0.001

    # ------------------------------
    # 情報

    target_list = [define.NECK_EDGE_SET_NAME]

    neck_edge_list = get_neck_edge_list()
    vertices = []
    if neck_edge_list:
        vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)

    fix_vertices = []

    for vtx in vertices:

        data_type = param_item.main.chara_info.part_info.data_type

        if not data_type.endswith('head') and\
                not param_item.main.chara_info.part_info.data_type.endswith('body'):
            return

        # headならネックエッジ頂点をそのまま追加
        if param_item.main.chara_info.part_info.data_type.endswith('head'):
            fix_vertices.append(vtx)
            continue

        # bodyは体型差分のネックエッジも考慮する
        for suffix in suffix_list:

            if vtx.find(suffix) >= 0:
                # 体型差分の頂点もNeckEdgeSetに含まれている場合の処理
                fix_vertices.append(vtx)

            else:

                # M_Bodyの頂点の場合、体型差分の頂点も追加対象にする
                fix_vertices.append(vtx)

                diff_vtx = vtx.replace('|M_Body', '{0}|M_Body{0}'.format(suffix))

                if cmds.objExists(diff_vtx) and diff_vtx not in fix_vertices:
                    fix_vertices.append(diff_vtx)

    fix_vertices.sort()
    if fix_vertices:
        target_list = fix_vertices
    param_item.info_target_list.extend(target_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    result = check_exists_neck_edge_set()
    if result:
        param_item.check_target_list.extend(result.get('error_target_list'))
        param_item.error_target_list.extend(result.get('error_target_list'))
        param_item.error_info = result.get('error_info')
        return

    param_item.check_target_list.extend(fix_vertices)

    for vtx in fix_vertices:

        base_pos = [0.0, 0.0, 0.0]

        # Headが見つかった場合はHeadからの相対位置をとる
        short_name = vtx.split('|')[-1]
        root_node = vtx.replace('|' + short_name, '')

        descendent_joint_list = []
        if cmds.objExists(root_node):
            descendent_joint_list = cmds.listRelatives(root_node, ad=True, type='joint', f=True)

        if descendent_joint_list is None:
            param_item.error_target_list.append("{0}{1}ジョイントの状態が異常です。".format(vtx, param_item.root.info_window.detail_separator))

            continue

        for descendent_joint in descendent_joint_list:
            if descendent_joint.endswith('Head'):
                base_pos = cmds.xform(descendent_joint, q=True, ws=True, t=True)

        vtx_pos = cmds.xform(vtx, q=True, ws=True, t=True)

        vtx_pos_from_base = [
            vtx_pos[0] - base_pos[0],
            vtx_pos[1] - base_pos[1],
            vtx_pos[2] - base_pos[2],
        ]

        ref_pos_list = default_pos_from_head_list

        if not param_item.main.chara_info.data_info.exists or param_item.main.chara_info.data_info.height_id is None:
            # 身長idが取れない汎用衣装などは接尾語からref_pos_listを判定
            if vtx.find(define.HEIGHT_SS_SUFFIX) >= 0:
                ref_pos_list = height_ss_pos_from_head_list
            elif vtx.find(define.HEIGHT_L_SUFFIX) >= 0:
                ref_pos_list = height_l_pos_from_head_list
            else:
                ref_pos_list = default_pos_from_head_list

        else:
            # 身長idが取れる場合はそこからref_pos_listを判定
            height_id = int(param_item.main.chara_info.data_info.height_id)

            if height_id < 1:
                ref_pos_list = height_ss_pos_from_head_list
            elif height_id > 1:
                ref_pos_list = height_l_pos_from_head_list

        is_error = True
        nearest_ref_distance = 10000
        nearest_ref_pos = [0, 0, 0]

        for ref_pos in ref_pos_list:

            # 結果表示のため距離計算を行う
            x_diff = vtx_pos_from_base[0] - ref_pos[0]
            y_diff = vtx_pos_from_base[1] - ref_pos[1]
            z_diff = vtx_pos_from_base[2] - ref_pos[2]

            x_square = math.pow(x_diff, 2)
            y_square = math.pow(y_diff, 2)
            z_square = math.pow(z_diff, 2)

            this_distance = math.sqrt(x_square + y_square + z_square)

            if this_distance < nearest_ref_distance:
                nearest_ref_distance = this_distance
                nearest_ref_pos = ref_pos

            # 判定
            if abs(x_diff) < torelance and abs(y_diff) < torelance and abs(z_diff) < torelance:
                is_error = False
                break

        if is_error:
            error_str = '{}{}headからの相対位置:{} / 規定値:{} / 許容誤差:{}'.format(
                vtx,
                param_item.root.info_window.detail_separator,
                str(vtx_pos_from_base),
                str(nearest_ref_pos),
                torelance
            )
            param_item.error_target_list.append(error_str)
        else:
            param_item.unerror_target_list.append(vtx)


def get_neck_edge_list():
    """NeckEdgeSet内のedgeの一覧を取得する
    """

    neck_edge_list = []

    if cmds.objExists(define.NECK_EDGE_SET_NAME):
        neck_edge_list = cmds.ls(cmds.sets(define.NECK_EDGE_SET_NAME, q=True), fl=True)

    return neck_edge_list


def check_exists_neck_edge_set():
    """NeckEdgeSetオブジェクト自体と、NeckEdgeSetオブジェクト

    Returns:
        dict: error_target_listとerror_infoの辞書型
    """

    result = {}

    if not cmds.objExists(define.NECK_EDGE_SET_NAME):
        result['error_target_list'] = [define.NECK_EDGE_SET_NAME]
        result['error_info'] = 'NeckEdgeSetが見つかりませんでした'

    elif not cmds.ls(cmds.sets(define.NECK_EDGE_SET_NAME, q=True), fl=True):
        result['error_target_list'] = [define.NECK_EDGE_SET_NAME]
        result['error_info'] = 'NeckEdgeSet内にエッジが設定されていません'

    return result

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

    target_mesh_list = []
    tmp_target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_name in param_item.main.chara_info.part_info.mesh_list:
        if cmds.objExists(mesh_name):
            tmp_target_mesh_list.append(mesh_name)

    for outline_mesh_name in param_item.main.chara_info.part_info.outline_mesh_list:
        if cmds.objExists(outline_mesh_name):
            tmp_target_mesh_list.append(outline_mesh_name)

    for mesh in tmp_target_mesh_list:

        # 非多様体フェース検出問題の暫定処置
        if cleanup_type == 'nonmanifold':
            if mesh.find('M_Face') >= 0:
                continue

        target_mesh_list.append(mesh)

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
            target_list = [mesh]
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

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
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

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        if not mesh_param['name'].find('M_Face') >= 0:
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

    # 対象の確定
    for mesh in target_mesh_list:

        target_list = base_utility.mesh.get_vertex_list(mesh)

        if not target_list:
            continue

        param_item.check_target_list.extend(target_list)

    # エラーチェック
    vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
    vtxcolor_info.create_info(param_item.check_target_list)

    this_vertex_list = \
        base_utility.mesh.vertex_color.get_vertex_list_with_unshared_color(vtxcolor_info)

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
def check_mesh_vertex_color_alpha(param_item, arg):
    """
    頂点カラーのアルファ値チェック
    アルファに1以外が入っている場合はエラー
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    param_item.add_require_value_to_label('Alpha: 1.0')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

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

            param_item.error_target_list.append(
                '{0}.vtx[{1}]'.format(mesh, str(this_index)))

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

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
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

    noise = 0.05

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
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
    カラーセット数が2以上でエラー。M_Faceのみ3以上でエラー
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    param_item.add_require_value_to_label('2以下(Faceは3以下)')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
            continue

        param_item.check_target_list.append(mesh)

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            mesh)

        color_set_limit = 1

        # M_Faceのみ口腔内用にカラーセット2を持つ
        if mesh.endswith('M_Face') or mesh.find('M_Face_Prop') > -1:
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

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
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

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
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
def check_all_joints_in_influence(param_item, arg):
    """
    全ジョイントがインフルエンスに含まれているか
    """

    # ------------------------------
    # 設定

    # 対象はルート以下の全ジョイント
    root_node = param_item.main.chara_info.part_info.root_node
    target_all_joints = __get_filtered_joint_list([root_node], None, None)

    if not target_all_joints:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_all_joints)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    # スキニングされている各メッシュでスキンクラスターからインフルエンスをチェック
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:

        this_mesh = mesh_param['name']
        if not cmds.objExists(this_mesh):
            continue

        this_skincluster = base_utility.mesh.skin.get_skin_cluster(this_mesh)
        if not this_skincluster:
            continue

        influence_names = cmds.listConnections(this_skincluster, type='joint')
        influences = cmds.ls(influence_names, l=True)

        for joint in target_all_joints:
            separator = param_item.root.info_window.detail_separator
            if joint in influences:
                param_item.unerror_target_list.append('{0}{1}{2}'.format(joint, separator, this_mesh))
            else:
                param_item.error_target_list.append('{0}{1}{2}'.format(joint, separator, this_mesh))


# ==================================================
def check_mesh_skin_round(param_item, arg):
    """
    ウェイト精度小数点以下2桁以内かの確認
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
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

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
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
    # 設定

    target_joint_list = [
        'Hand_Attach_L',
        'Hand_Attach_R',
        'Sp_Ch_Bust0_L_00',
        'Sp_Ch_Bust0_R_00',
        'Ankle_L',
        'Ankle_R',
        'Toe_L',
        'Toe_R'
    ]

    head_target_joint = [
        'Sp_He_Ear0_R_00',
        'Sp_He_Ear0_R_01',
        'Sp_He_Ear0_R_02',
        'Sp_He_Ear0_L_00',
        'Sp_He_Ear0_L_01',
        'Sp_He_Ear0_L_02'
    ]

    if param_item.main.chara_info.part_info.data_type.endswith('head'):
        target_joint_list = head_target_joint

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

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

        if not base_utility.transform.exists(mesh):
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

                if joint_waight_info[0].split('|')[-1] in target_joint_list:

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

    mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        mesh_list.append(mesh_param['name'])

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

        if not base_utility.transform.exists(mesh):
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

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    param_item.add_require_value_to_label('1(Faceは3(但し、emissive除く))')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
            continue

        param_item.check_target_list.append(mesh)

        uvset_count = 1

        if not param_item.main.chara_info.is_mini:
            if mesh.find('Face') >= 0 and not mesh.endswith('_Emissive'):
                uvset_count = 3

        uvset_list = base_utility.mesh.uvset.get_uvset_list(mesh)

        if uvset_list is None:
            param_item.error_target_list.append(mesh)
            continue

        if len(uvset_list) == uvset_count:
            param_item.unerror_target_list.append(mesh)
            continue

        param_item.error_target_list.append(mesh)


# ==================================================
def check_mesh_uv_coordinate(param_item, arg):
    """
    UV座標の確認
    0~1.0の範囲になければエラー
    """

    # ------------------------------
    # 設定

    target_mesh_list = []

    # Alphaメッシュを含めるためcheckフラグでの判定は行わない
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:
        target_mesh_list.append(mesh_param['name'])

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    param_item.add_require_value_to_label('U, Vともに0.0~1.0に収まっている')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in target_mesh_list:

        if not base_utility.transform.exists(mesh):
            continue

        if mesh.find('Tear') >= 0:
            continue

        all_uv_info_list = base_utility.mesh.uv.get_all_uv_info_list(
            mesh)

        if all_uv_info_list is None:
            param_item.error_target_list.append(mesh)
            continue

        for uv_info in all_uv_info_list:

            uv_name = mesh + '.map[%s]' % str(uv_info[0])

            param_item.check_target_list.append(uv_name)

            if 0 <= uv_info[1][0] <= 1.0 and 0 <= uv_info[1][1] <= 1.0:

                param_item.unerror_target_list.append(uv_name)
                continue

            param_item.error_target_list.append(uv_name)


# ==================================================
def check_eye_uv_map(param_item, args):
    """
    EyeのUVMapに含まれるシェルが、Eyeマテリアルかどうか
    """
    # ------------------------------
    # 設定

    target_mesh_list = []

    for mesh_name in param_item.main.chara_info.part_info.mesh_list:
        if cmds.objExists(mesh_name):
            target_mesh_list.append(mesh_name)

    for outline_mesh_name in param_item.main.chara_info.part_info.outline_mesh_list:
        if cmds.objExists(outline_mesh_name):
            target_mesh_list.append(outline_mesh_name)

    if not target_mesh_list:
        return

    target_uv_list = []

    uv_list = cmds.polyUVSet(target_mesh_list, q=True, auv=True)
    for uv_set in uv_list:
        if uv_set.find('eye') >= 0:
            target_uv_list.append(uv_set)

    target_uv_list = list(set(target_uv_list))

    if not target_uv_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_uv_list)

    param_item.add_require_value_to_label('Eye用のマテリアルが割り振られている')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    target_SG_list = []
    for material_name in param_item.main.chara_info.part_info.material_list:

        if material_name.find('eye') >= 0:
            _material_connected_item_list = cmds.listConnections(material_name, source=False, destination=True)
            if not _material_connected_item_list:
                continue

            sg_list = cmds.ls(_material_connected_item_list, type='shadingEngine')
            if not sg_list:
                continue

            target_SG_list.append(sg_list[0])

    # UVセットの保全
    saved_uv_set_list = {}
    for mesh_name in target_mesh_list:
        _current_mesh_uv_set = cmds.polyUVSet(mesh_name, query=True, currentUVSet=True)
        if not _current_mesh_uv_set:
            continue

        saved_uv_set_list[mesh_name] = _current_mesh_uv_set[0]

    # UV setからmapのリスト作成
    for uv_set in target_uv_list:

        cmds.polyUVSet(target_mesh_list, uvSet=uv_set, cuv=True)

        for mesh_name in target_mesh_list:

            target_map_list = []

            mesh = om.MGlobal.getSelectionListByName(mesh_name)
            shape = mesh.getDagPath(0).extendToShape()
            mfn_mesh = om.MFnMesh(shape)

            try:
                uv_shell_count, uv_shell_ids = mfn_mesh.getUvShellsIds(uv_set)
            except Exception:
                continue

            for map_index, _ in enumerate(uv_shell_ids):
                target_map_list.append(mesh_name + '.map[' + str(map_index) + ']')

            # メッシュが適切か判定
            for map_index in target_map_list:

                if map_index not in param_item.check_target_list:
                    param_item.check_target_list.append(map_index)

                _face = cmds.polyListComponentConversion(map_index, toFace=True)

                _is_included = False
                for shading_engine in target_SG_list:
                    if cmds.sets(_face, isMember=shading_engine):
                        _is_included = True
                        break

                if _is_included:
                    param_item.unerror_target_list.append(map_index)
                    continue

                if map_index not in param_item.error_target_list:
                    param_item.error_target_list.append(map_index)

    # UVセットの復元
    for mesh_name in target_mesh_list:

        if mesh_name not in list(saved_uv_set_list.keys()):
            continue

        cmds.polyUVSet(mesh_name, uvSet=saved_uv_set_list[mesh_name], currentUVSet=True)

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

    # Alphaメッシュなどに紐づくオプショナルなマテリアルを追加
    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:

        if not base_utility.transform.exists(mesh_param['name']):
            continue

        this_material_ids = mesh_param['material_list']

        for material_param in param_item.main.chara_info.part_info.material_param_list:

            if str(material_param['id']) in this_material_ids:
                if not material_param['name'] in target_material_list:
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

        if base_utility.node.exists(material, ['lambert']):
            param_item.unerror_target_list.append(material)
            continue

        param_item.error_target_list.append(material)


# ==================================================
def check_wrong_material_exist(param_item, args):
    """
    不要マテリアルが存在するかのチェック
    """

    ignore_materials = ['lambert1', 'particleCloud1', 'standardSurface1']

    # ------------------------------
    # 設定

    tmp_material_list = cmds.ls(mat=True)
    target_material_list = []

    for material in tmp_material_list:
        if material not in ignore_materials:
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

    for material in target_material_list:

        if material in param_item.main.chara_info.part_info.material_list:
            param_item.unerror_target_list.append(material)
        else:
            param_item.error_target_list.append(material)


# ==================================================
def check_material_link(param_item, args):
    """
    メッシュに正しいマテリアルが紐づいているかのチェック
    """

    # ------------------------------
    # 設定

    target_mesh_list = []
    target_materials_list = []

    for mesh_param in param_item.main.chara_info.part_info.mesh_param_list:

        if not base_utility.transform.exists(mesh_param['name']):
            continue

        target_mesh_list.append(mesh_param['name'])

        this_material_ids = mesh_param['material_list']

        this_mesh_materials = []

        for material_param in param_item.main.chara_info.part_info.material_param_list:

            if str(material_param['id']) in this_material_ids:
                if not material_param['name'] in this_mesh_materials:
                    this_mesh_materials.append(material_param['name'])

        target_materials_list.append(this_mesh_materials)

    if not target_mesh_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_mesh_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh, materials in zip(target_mesh_list, target_materials_list):

        actual_material_list = base_utility.material.get_material_list(mesh)

        if not actual_material_list:
            param_item.error_target_list.append(mesh)
            continue

        has_true_materials = True
        for actual_material in actual_material_list:
            if actual_material not in materials:
                param_item.error_target_list.append(mesh)
                has_true_materials = False
                break

        if has_true_materials:
            param_item.unerror_target_list.append(mesh)


# ==================================================
def check_material_texture_path(param_item, arg):
    """
    マテリアルのテクスチャパスがSVN上のものになっているかチェック
    """

    # ------------------------------
    # 情報

    part_type = ''

    if param_item.main.chara_info.part_info.data_type.endswith('body'):
        part_type = 'body'
    elif param_item.main.chara_info.part_info.data_type.endswith('head'):
        part_type = 'head'
    elif param_item.main.chara_info.part_info.data_type.endswith('tail'):
        part_type = 'tail'
    elif param_item.main.chara_info.part_info.data_type.endswith('toon_prop'):
        part_type = 'toon_prop'
    elif param_item.main.chara_info.part_info.data_type.endswith('prop'):
        part_type = 'prop'
    else:
        return

    is_mini = param_item.main.chara_info.is_mini

    path_finder = glp_class.path_finder.path_finder.PathFinder(part_type, param_item.main.chara_info.data_main_id, is_mini)

    # 外注先等SVNパスが無いところではチェックしない
    if not os.path.exists(path_finder.SVN_CHARA_MODEL_DIR_PATH):
        return

    texture_path_list = path_finder.texture_list

    if not texture_path_list:
        return

    fix_str_path_list = []

    for texture_path in texture_path_list:
        fix_str_path_list.append(texture_path.replace('\\', '/'))

    param_item.info_target_list.extend(
        param_item.main.chara_info.part_info.material_list
    )

    param_item.add_require_value_to_label('SVNパス上である')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(param_item.main.chara_info.part_info.material_list)

    # ミニ顔にある以下の名前のついたマテリアルはテクスチャが不定なのでスキップ
    mini_skip_flag_list = ['_mayu', '_mouth', '_eye']

    for p in range(len(param_item.main.chara_info.part_info.material_param_list)):

        should_skip = False
        material = param_item.main.chara_info.part_info.material_param_list[p]['name']

        # 特殊対応でスキップするものの判定
        if is_mini:
            for skip_flag in mini_skip_flag_list:
                if material.find(skip_flag) >= 0:
                    should_skip = True

        if should_skip:
            continue

        # テクスチャパス取得
        input_attr_list = \
            base_utility.attribute.get_input_attr_list(
                material, 'color'
            )

        if not input_attr_list:
            continue

        this_input_attr = input_attr_list[0]

        this_input_node = this_input_attr.split('.')[0]

        if not cmds.objectType(this_input_node) == 'file':
            continue

        this_file_path = base_utility.attribute.get_value(
            this_input_node, 'fileTextureName'
        )

        if this_file_path is None:
            continue

        fix_file_path = this_file_path.replace('\\', '/')

        # path_list内にあればセーフ
        if fix_file_path in fix_str_path_list:
            param_item.unerror_target_list.append(fix_file_path)
        else:
            param_item.error_target_list.append(this_file_path)

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
    target_texture_info_list = None

    if texture_type == 'texture':
        target_texture_list = param_item.main.chara_info.part_info.all_texture_list
        target_texture_info_list = param_item.main.chara_info.part_info.all_texture_param_list

    elif texture_type == 'psd':
        target_texture_list = param_item.main.chara_info.part_info.psd_list
        target_texture_info_list = param_item.main.chara_info.part_info.psd_param_list

    if not target_texture_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_texture_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    count = -1

    for texture_param in target_texture_info_list:

        count += 1

        if not texture_param['check']:
            continue

        texture_path = param_item.main.chara_info.part_info.maya_sourceimages_dir_path + \
            '/' + texture_param['name']

        if os.path.isfile(texture_path):
            param_item.unerror_target_list.append(texture_path)
            continue

        if not texture_param['check']:
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
    target_texture_info_list = None

    if texture_type == 'texture':
        target_texture_list = param_item.main.chara_info.part_info.all_texture_list
        target_texture_info_list = param_item.main.chara_info.part_info.all_texture_param_list

    elif texture_type == 'psd':
        target_texture_list = param_item.main.chara_info.part_info.psd_list
        target_texture_info_list = param_item.main.chara_info.part_info.psd_param_list

    if not target_texture_list or not target_texture_info_list:
        return

    if len(target_texture_list) != len(target_texture_info_list):
        return

    # ------------------------------
    # 情報

    param_item.info_target_list = target_texture_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    temp_file_node = cmds.shadingNode(
        'file', asTexture=True, name='temp_file_node')

    count = -1

    exists_emissive_mesh = False
    if param_item.main.chara_info.data_type.endswith('body'):
        mesh_list = param_item.main.chara_info.part_info.mesh_list
        emissive_mesh_list = [mesh for mesh in mesh_list if mesh.endswith('M_Body_Emissive')]
        if emissive_mesh_list:
            exists_emissive_mesh = cmds.objExists(emissive_mesh_list[0])

    for texture_param in target_texture_info_list:
        count += 1

        texture_path = param_item.main.chara_info.part_info.maya_sourceimages_dir_path + \
            '/' + texture_param['name']

        param_item.check_target_list.append(texture_path)

        if not os.path.isfile(texture_path):

            if texture_param['check']:
                param_item.error_target_list.append('{0}'.format(texture_path))
                continue

            continue

        this_ref_size = [int(texture_param['width'][0]), int(texture_param['height'][0])]
        # emissive_meshがある場合は2番目の数値を参照する
        if texture_param['name'].find('_ctrl') > -1 and exists_emissive_mesh and len(texture_param['width']) > 1 and len(texture_param['height']) > 1:
            this_ref_size = [int(texture_param['width'][1]), int(texture_param['height'][1])]

        base_utility.attribute.set_value(temp_file_node, 'fileTextureName', texture_path)

        this_tex_size = base_utility.attribute.get_value(
            temp_file_node, 'outSize', [0, 0]
        )

        if base_utility.vector.is_same(this_ref_size, this_tex_size):
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

        if base_utility.node.exists(locator):
            param_item.unerror_target_list.append(locator)
            continue

        param_item.error_target_list.append(locator)


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

        if not base_utility.node.exists(locator):
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

        translate = base_utility.attribute.get_value(
            locator, 'translate'
        )

        rotate = base_utility.attribute.get_value(
            locator, 'rotate'
        )

        scale = base_utility.attribute.get_value(
            locator, 'scale'
        )

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

        if not base_utility.node.exists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not base_utility.node.exists(this_set[1]):
            param_item.error_target_list.extend(this_set)
            continue

        base_name = base_utility.name.get_long_name(
            this_set[0], param_item.main.chara_info.data_id + r'\|')

        locator_name = base_utility.name.get_long_name(
            this_set[1], param_item.main.chara_info.data_id + r'\|')

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

        if not base_utility.node.exists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not base_utility.node.exists(this_set[1]):
            param_item.error_target_list.extend(this_set)
            continue

        base_name = base_utility.name.get_long_name(
            this_set[0], param_item.main.chara_info.data_id + r'\|')

        locator_name = base_utility.name.get_long_name(
            this_set[1], param_item.main.chara_info.data_id + r'\|')

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

        if not base_utility.node.exists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not base_utility.node.exists(this_set[1]):
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

    target_locator_list = []

    for locator_param in param_item.main.chara_info.part_info.locator_param_list:

        # 必須ではなく、存在しないロケーターはスルー
        if not locator_param['check'] and not cmds.objExists(locator_param['name']):
            continue

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

    attr_list = ['translate', 'rotate', 'scale']
    direction_list = ['X', 'Y', 'Z']

    for locator_node in target_locator_list:

        is_lock = False

        if not cmds.objExists(locator_node):
            param_item.error_target_list.append('{0} が存在しません。'.format(locator_node))
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


# ==================================================
def check_spec_info_scale_value(param_item, args):
    """
    spec_infoのscale値が正しいかどうかのチェック
    """
    # ------------------------------
    # 設定

    min_scale_value = 0.0
    max_scale_value = 1.0

    locator_nodes = param_item.main.chara_info.part_info.locator_list
    if not locator_nodes:
        return

    target_locator_nodes = [locator_node for locator_node in locator_nodes if locator_node.find('spec_info') >= 0]
    if not target_locator_nodes:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_locator_nodes)

    if not param_item.is_check_data:
        return

    param_item.check_target_list = target_locator_nodes

    attr_list = ['scaleX', 'scaleY', 'scaleZ']

    for target_locator_node in target_locator_nodes:

        if not cmds.objExists(target_locator_node):
            param_item.error_target_list.append('{} が存在しない'.format(target_locator_node))
            continue

        for attr in attr_list:

            target_locator_attr = '{}.{}'.format(target_locator_node, attr)
            if cmds.attributeQuery(attr, node=target_locator_node, exists=True) is False:

                param_item.error_target_list.append('{} アトリビュートが見つからない'.format(target_locator_attr))
                continue

            target_locator_attr_value = cmds.getAttr(target_locator_attr)
            if not (min_scale_value <= target_locator_attr_value <= max_scale_value):

                param_item.error_target_list.append(
                    '{} (現在のスケール値 {} 基準値 {}～{})'.format(
                        target_locator_attr,
                        target_locator_attr_value,
                        min_scale_value,
                        max_scale_value
                    ))
                continue

            param_item.unerror_target_list.append(target_locator_attr)


# ==================================================
def check_locator_local_position_value(param_item, arg):
    """
    head_heightロケーターのLocalPositionの値チェック
    """
    # ------------------------------
    # 設定

    target_locator_list = []

    locator_list = param_item.main.chara_info.part_info.locator_list
    for locator in locator_list:
        if cmds.objExists(locator):
            target_locator_list.append(locator)

    if not target_locator_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_locator_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for locator in target_locator_list:

        locator_child_list = cmds.listRelatives(locator, type='locator')
        if not locator_child_list:
            param_item.error_target_list(locator)
            continue
        locator_shape = locator_child_list[0]

        local_pos_list = cmds.getAttr('{}.localPosition'.format(locator_shape))[0]
        for local_pos in local_pos_list:
            # -0.0や浮動小数点で0が入っている可能性があるため丸める
            if round(local_pos, 5) != 0.0:
                param_item.error_target_list.append(locator)
                break
        else:
            param_item.unerror_target_list.append(locator)


# ==================================================
def check_specific_locater_pivot_value_is_zero(param_item, arg):
    """
    特定のロケーターのpivot位置が0かどうかチェックする

    head(face_head)の場合は以下のロケーター
    Eye_base_info_L
    Eye_base_info_R
    Eye_big_info_L
    Eye_big_info_R
    Eye_small_info_L
    Eye_small_info_R
    Eye_kira_info
    """
    # ------------------------------
    # 設定

    target_locator_list = []

    locator_list = []
    if param_item.main.chara_info.data_type.endswith('head'):
        locator_list = define.SPECIFIC_EYE_LOCATOR

    for locator in locator_list:
        if cmds.objExists(locator):
            target_locator_list.append(locator)

    if not target_locator_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_locator_list)

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

# region ジョイント系


# ==================================================
def check_joint_exist(param_item, arg):
    """
    ジョイントの存在チェック
    """

    # ------------------------------
    # 設定

    target_joint_list = []
    either_target_joint_list_dict = {}

    for joint_param in param_item.main.chara_info.part_info.joint_param_list:

        if joint_param['check']:
            target_joint_list.append(joint_param['name'])

            if 'check_either_target' in joint_param:

                if len(joint_param['check_either_target']) == 1 and joint_param['check_either_target'][0] == '':
                    continue

                tmp_check_either_target_joint_list = []
                for tmp_joint_param in param_item.main.chara_info.part_info.joint_param_list:
                    _id = tmp_joint_param['id']
                    if str(_id) in joint_param['check_either_target']:
                        tmp_check_either_target_joint_list.append(tmp_joint_param['name'])

                if tmp_check_either_target_joint_list:
                    either_target_joint_list_dict[joint_param['name']] = tmp_check_either_target_joint_list

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

        if base_utility.node.exists(joint):
            param_item.unerror_target_list.append(joint)
            continue

        # もし存在しなかったときにcheck_either_targetに値があって尚且つ対象が存在していたら無視
        if joint in either_target_joint_list_dict:
            either_target_joint_list = either_target_joint_list_dict[joint]
            for either_target_joint in either_target_joint_list:
                if not cmds.objExists(either_target_joint):
                    break
            else:
                continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_all_joint_count(param_item, arg):
    """
    すべてのジョイントの数をチェック
    """

    # ------------------------------
    # 設定

    target_min_count = param_item.main.chara_info.part_info.normal_bone_limit
    target_min_count += param_item.main.chara_info.part_info.sp_bone_limit

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    param_item.add_require_value_to_label('{0}以下'.format(target_min_count))

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

    target_min_count = param_item.main.chara_info.part_info.normal_bone_limit

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    param_item.add_require_value_to_label('{0}以下'.format(target_min_count))

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    joint_list = __get_filtered_joint_list([root_node], None, define.CLOTH_JOINT_LIST)

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

    target_min_count = param_item.main.chara_info.part_info.sp_bone_limit

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    param_item.add_require_value_to_label('{0}以下'.format(target_min_count))

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    joint_list = __get_filtered_joint_list([root_node], define.CLOTH_JOINT_LIST, None)

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

    # 頭、身体の合算上限
    # 適当なIDでinfoを作り、各パートの上限数を取得して合算する
    head_target_min_count = 0
    body_target_min_count = 0

    if param_item.main.chara_info.part_info.is_mini:
        sample_info = glp_class.info.chara_info.CharaInfo()
        sample_info.create_info('mdl_mbdy1001_00', is_create_all_info=True)
        head_target_min_count += sample_info.head_part_info.sp_bone_limit
        body_target_min_count += sample_info.body_part_info.sp_bone_limit

    else:
        sample_info = glp_class.info.chara_info.CharaInfo()
        sample_info.create_info('mdl_bdy1001_00', is_create_all_info=True)
        head_target_min_count += sample_info.head_part_info.sp_bone_limit
        body_target_min_count += sample_info.body_part_info.sp_bone_limit

    target_min_count = head_target_min_count + body_target_min_count

    param_item.add_require_value_to_label('head:{0}以下、body:{1}以下'.format(head_target_min_count, body_target_min_count))

    if param_item.main.chara_info.part_info.data_type.find('head') >= 0:
        check_cloth_joint_sum_count_base(param_item, target_min_count, True, arg)

    elif param_item.main.chara_info.part_info.data_type.find('body') >= 0:
        check_cloth_joint_sum_count_base(param_item, target_min_count, False, arg)


# ==================================================
def check_cloth_joint_sum_count_base(param_item, target_min_count, from_head, arg):
    """
    ユニーク頭部と勝負服のクロスジョイント合算数をチェック
    """

    # 対応しうる身体or頭部を検索
    opposit_part = 'body' if from_head else 'head'
    opposit_finder = glp_class.path_finder.path_finder.PathFinder(opposit_part, param_item.main.chara_info.data_main_id, param_item.main.chara_info.part_info.is_mini)
    opposit_files = [x for x in opposit_finder.model_ma_list if os.path.exists(x)]

    check_dict_list = []

    for opposit_file in opposit_files:

        check_dict = {'head_path': '', 'body_path': '', 'info_str': ''}

        if from_head:
            check_dict['head_path'] = cmds.file(q=True, sn=True)
            check_dict['body_path'] = opposit_file
        else:
            check_dict['head_path'] = opposit_file
            check_dict['body_path'] = cmds.file(q=True, sn=True)

        head_file_name = os.path.basename(check_dict['head_path'])
        body_file_name = os.path.basename(check_dict['body_path'])

        check_dict['info_str'] = '{}, {}'.format(head_file_name, body_file_name)

        check_dict_list.append(check_dict)

    # ------------------------------
    # 設定

    if not check_dict_list:
        return

    opposit_ref_name_space = '__BODY_MODEL_REF__' if from_head else '__HEAD_MODEL_REF__'

    # ------------------------------
    # 情報

    for check_dict in check_dict_list:
        param_item.info_target_list.append(check_dict['info_str'])

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    ref_ctrl = base_class.reference.ReferenceController()

    for check_dict in check_dict_list:

        tmp_info = glp_class.info.chara_info.CharaInfo()

        if from_head:
            tmp_info.create_info(check_dict['body_path'])
        else:
            tmp_info.create_info(check_dict['head_path'])

        if not tmp_info.part_info:
            continue

        body_root = ''
        head_root = ''

        if from_head:
            body_root = tmp_info.part_info.root_node
            body_root = body_root.replace('|', '|{}:'.format(opposit_ref_name_space))
            head_root = param_item.main.chara_info.part_info.root_node
        else:
            body_root = param_item.main.chara_info.part_info.root_node
            head_root = tmp_info.part_info.root_node
            head_root = head_root.replace('|', '|{}:'.format(opposit_ref_name_space))

        target_path = check_dict['body_path'] if from_head else check_dict['head_path']

        # ロード/失敗したらエラーで返す
        ref_ctrl.load_using_no_plugin_tmp(target_path, opposit_ref_name_space, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{}が{}ため'.format(ref_ctrl.original_file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            continue

        # 対象ジョイントの取得
        joint_list = __get_filtered_joint_list([head_root, body_root], define.CLOTH_JOINT_PREFIX_LIST, None)

        # アンロード
        ref_ctrl.unload(unload_hard=True)

        # チェック結果の記載
        all_count = len(joint_list)
        error_count = all_count - target_min_count

        param_item.check_target_list.append(check_dict['info_str'])
        if error_count > 0:
            param_item.error_target_list.append('{} ({}/{} joints: {} joints over)'.format(check_dict['info_str'], all_count, target_min_count,
                                                                                           error_count))
        else:
            param_item.unerror_target_list.append('{} ({}/{} joints)'.format(check_dict['info_str'], all_count, target_min_count))


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

    # define.CLOTH_JOINT_LISTの要素順に応じて並び替え
    sort_target_len = len(define.CLOTH_JOINT_LIST)
    sort_target_joints_list = [[] for i in range(sort_target_len)]

    for joint in all_joint_list:

        joint_name = joint.split('|')[-1]

        for i in range(sort_target_len):

            sort_target = define.CLOTH_JOINT_LIST[i]
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

            if joint_prefix not in define.CLOTH_JOINT_PREFIX_LIST:
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

            # 親骨がdefine.CLOTH_JOINT_PARENT_DICT通りになっているかチェック
            joint_parent_str = joint_elm_list[1]
            parent_joint_base_name = ''

            if joint_parent_str not in define.CLOTH_JOINT_PARENT_DICT:
                param_item.error_target_list.append(joint)
                continue
            else:
                parent_joint_base_name = define.CLOTH_JOINT_PARENT_DICT[joint_parent_str]

            parent_short_name = ''

            if param_item.main.chara_info.part_info.data_type.find('tail') >= 0:
                # tailはHip確定
                parent_short_name = 'Hip'

            else:
                # 最初に特殊骨の接頭辞の付く一つ上の骨をチェック対象にする
                joint_hierarchy_list = joint.split('|')
                parent_short_name = joint_hierarchy_list[0]

                for this_short_name in joint_hierarchy_list:

                    is_special_joint = False

                    for prefix in define.CLOTH_JOINT_PREFIX_LIST:
                        if this_short_name.startswith(prefix):
                            is_special_joint = True
                            break

                    if is_special_joint:
                        break
                    else:
                        parent_short_name = this_short_name

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
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    param_item.add_require_value_to_label('特殊なジョイントを除きrotate, translateともに0')

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

        translate = base_utility.attribute.get_value(
            joint, 'translate'
        )

        rotate = base_utility.attribute.get_value(
            joint, 'rotate'
        )

        scale = base_utility.attribute.get_value(
            joint, 'scale'
        )

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

            if joint_name in list(tail_rotate_dict.keys()) and not param_item.main.chara_info.is_mini:

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

            if not base_utility.vector.is_same(
                scale, [1, 1, 1]
            ):
                is_hit = True

        if not is_hit:
            param_item.unerror_target_list.append(joint)
            continue

        param_item.error_target_list.append(joint)


# ==================================================
def check_world_joint_orient(param_item, arg):
    """
    ワールド方向に設定するジョイントの軸方向をチェック
    """

    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.append(root_node)

    param_item.add_require_value_to_label('原則、joint orientがそれぞれ0.0')

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

        if any([joint_name.startswith(x) for x in define.CLOTH_JOINT_PREFIX_LIST]):

            is_check_joint = False

            for check_orient_sp_target in check_orient_sp_target_list:

                if joint_name.find(check_orient_sp_target) >= 0:
                    is_check_joint = True
                    break

        if not is_check_joint:
            continue

        orient = base_utility.attribute.get_value(
            joint, 'jointOrient'
        )

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
                error_attr_list.append('jointOrientX({})'.format(str(orient[0])))
            if not orient[1] == 0.0:
                is_hit = True
                error_attr_list.append('jointOrientY({})'.format(str(orient[1])))
            if not orient[2] == 0.0:
                is_hit = True
                error_attr_list.append('jointOrientZ({})'.format(str(orient[2])))

        error_attr_str = ' / '.join(error_attr_list)

        if not is_hit:
            param_item.unerror_target_list.append(joint)
            continue

        separator = param_item.root.info_window.detail_separator
        param_item.error_target_list.append('{0}{1}{2}'.format(joint, separator, error_attr_str))


# ==================================================
def check_local_joint_orient(param_item, arg):
    """
    ローカル方向に設定するジョイントの軸方向をチェック
    """

    # ------------------------------
    # 設定

    # ±JOINT_TRANSLATION_ALLOWANCE_LIMIT分、移動値に微小値が入ることを許容する
    JOINT_TRANSLATION_ALLOWANCE_LIMIT = 0.001

    # 検出除外条件(ジョイント名/ショートネームに対して正規表現で検索する)
    EXCLUDE_REGEX_LIST = [
        '_00$',
        r'_Bust\d+'
    ]

    # すべてのジョイントを検索する対象とするタイプ
    EXAMINE_ALL_BONE_TYPE_LIST = ['prop', 'toon_prop']

    # すべてのジョイントを検索するバージョン側で検出除外条件(ジョイント名/ショートネームに対して正規表現で検索する)
    EXAMINE_ALL_BONE_EXCLUDE_REGEX_LIST = [
        '_00$',
        'Root$',
    ]

    target_joint = []

    original_root_node = param_item.main.chara_info.part_info.root_node
    if not original_root_node:
        return

    root_node_list = [original_root_node]

    if param_item.main.chara_info.is_common_body:

        for diff_suffix in define.BODY_DEFFERENCE_TARGET_SUFFIX_LIST:
            diff_root = original_root_node + diff_suffix

            if cmds.objExists(diff_root):
                root_node_list.append(diff_root)

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(root_node_list)

    param_item.add_require_value_to_label('対象の子のジョイントのX, Yのtranslateが-{0}~{0}'.format(JOINT_TRANSLATION_ALLOWANCE_LIMIT))

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    if not cmds.objExists(original_root_node):
        param_item.error_target_list.append('ルートノードが存在していません')
        return

    for root_node in root_node_list:

        all_joint_list = cmds.listRelatives(
            root_node, ad=True, f=True, typ='joint')

        if not all_joint_list:
            return

        # 除外ジョイント以外をリストアップ
        for joint in all_joint_list:

            joint_short_name = joint.rsplit('|')[-1]
            is_match_exclude = False
            current_exclude_regex_list = None

            # すべてのジョイントを検索する対象の場合
            if param_item.main.chara_info.data_type in EXAMINE_ALL_BONE_TYPE_LIST:
                current_exclude_regex_list = EXAMINE_ALL_BONE_EXCLUDE_REGEX_LIST

            # 揺れ骨のみを検索する対象の場合
            else:
                if not any([joint_short_name.startswith(x) for x in define.CLOTH_JOINT_PREFIX_LIST]):
                    continue
                current_exclude_regex_list = EXCLUDE_REGEX_LIST

            for exclude_regex in current_exclude_regex_list:
                if re.search(exclude_regex, joint_short_name) is not None:
                    is_match_exclude = True
                    break

            if is_match_exclude:
                continue

            target_joint.append(joint)

        for joint in target_joint:

            joint_pos = cmds.getAttr('{0}.translate'.format(joint))[0]

            joint_parent = cmds.listRelatives(joint, parent=True, fullPath=True)
            if not joint_parent:
                continue

            if joint not in param_item.check_target_list:
                param_item.check_target_list.append(joint)

            target_pos_list = [joint_pos[0], joint_pos[1]]
            is_error = False

            # 耳のみ揺れ骨の基軸が異なるため特殊処理
            # propなどでjoint名がEarを含んでしまった時のための保険
            if joint.find('Ear') >= 0 and param_item.main.chara_info.data_type.find('head') >= 0:
                target_pos_list = [joint_pos[0], joint_pos[2]]

            for target_pos in target_pos_list:

                if Decimal(str(-JOINT_TRANSLATION_ALLOWANCE_LIMIT)) <\
                    Decimal(str(target_pos)).quantize(Decimal(str(JOINT_TRANSLATION_ALLOWANCE_LIMIT)), rounding=ROUND_HALF_UP) <\
                        Decimal(str(JOINT_TRANSLATION_ALLOWANCE_LIMIT)):
                    continue

                is_error = True
                break

            if is_error:
                if joint not in param_item.error_target_list:
                    param_item.error_target_list.append(joint)
            else:
                if joint not in param_item.unerror_target_list:
                    param_item.unerror_target_list.append(joint)


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

    param_item.add_require_value_to_label('耳の通常ジョイントと揺れジョイントの位置が一致している')

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

        if not base_utility.node.exists(this_set[0]):
            param_item.error_target_list.extend(this_set)
            continue

        if not base_utility.node.exists(this_set[1]):
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

    bust_id = None
    if data_id.find('bdy0') >= 0:
        bust_id = 2
    elif param_item.main.chara_info.data_info.exists and param_item.main.chara_info.data_info.bust_id is not None:
        bust_id = param_item.main.chara_info.data_info.bust_id

    if not root_node:
        return

    bust_type = ''
    if bust_id is not None:
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

    if not bust_type:
        param_item.error_target_list.append('chara_data.csvからバストの種類が取得できなかったため、チェックできませんでした')
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

        if not cmds.objExists(joint):
            continue

        target_bust_joint_translate = cmds.xform(joint, q=True, ws=True, translation=True)

        if round(original_bust_joint_translate[0], 2) == round(target_bust_joint_translate[0], 2):
            if round(original_bust_joint_translate[1], 2) == round(target_bust_joint_translate[1], 2):
                if round(original_bust_joint_translate[2], 2) == round(target_bust_joint_translate[2], 2):
                    param_item.unerror_target_list.append(joint)
                    continue

        param_item.error_target_list.append(
            '{0} (規定値: x:{1}, y:{2}, z:{3})'.format(joint, target_bust_joint_translate[0], target_bust_joint_translate[1], target_bust_joint_translate[2])
        )


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

    bust_id = None
    if data_id.find('bdy0') >= 0:
        bust_id = 2
    elif param_item.main.chara_info.data_info.exists and param_item.main.chara_info.data_info.bust_id is not None:
        bust_id = param_item.main.chara_info.data_info.bust_id

    if not root_node:
        return

    bust_type = ''
    if bust_id is not None:
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

    if not bust_type:
        param_item.error_target_list.append('chara_data.csvからバストの種類が取得できなかったため、チェックできませんでした')
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

        orient = base_utility.attribute.get_value(
            joint, 'jointOrient'
        )

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
            continue

        hip_translate = base_utility.attribute.get_value(node, 'translate')

        if hip_translate is None:
            continue

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

    param_item.add_require_value_to_label('OFF')

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


def check_tooth_joint_segment_scale(param_item, args):
    """
    歯のジョイントのセグメントスケールがOFFになっているか
    """
    # ------------------------------
    # 設定

    target_joint_list = []

    for joint_name in param_item.main.chara_info.part_info.joint_list:

        # toothを名前に含み、かつ末端のジョイントのみを抽出
        if joint_name.find('Tooth') >= 0:
            if cmds.objExists(joint_name):
                if cmds.listRelatives(joint_name) is None:
                    target_joint_list.append(joint_name)

    if not target_joint_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_joint_list)

    param_item.add_require_value_to_label('OFF')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_joint_list

    for joint in target_joint_list:

        if not cmds.getAttr(joint + '.segmentScaleCompensate'):
            param_item.unerror_target_list.append(joint)
            continue

        param_item.error_target_list.append(joint)


def check_all_joint_segment_scale(param_item, args):
    """
    全ジョイントのセグメントスケールがOFFになっているか

    prop, toon_propの仕様決定により追加されたチェック
    """
    # ------------------------------
    # 設定

    target_joint_list = []

    root_node = param_item.main.chara_info.part_info.root_node

    if not cmds.objExists(root_node):
        return

    target_joint_list = cmds.listRelatives(root_node, ad=True, f=True, typ='joint')

    if not target_joint_list:
        return

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(target_joint_list)

    param_item.add_require_value_to_label('OFF')

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_joint_list

    for joint in target_joint_list:

        if not cmds.getAttr(joint + '.segmentScaleCompensate'):
            param_item.unerror_target_list.append(joint)
            continue

        param_item.error_target_list.append(joint)


def check_top_node_pivot(param_item, args):
    """一番上のノードのpivotが原点であるか確認

    Args:
        param_item (CheckerParamItem): Checker Paramの情報を格納したクラス
    """
    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node

    if not cmds.objExists(root_node):
        return

    # ------------------------------
    # 情報
    param_item.info_target_list.append(root_node)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = [root_node]

    # pivotが0か確認
    pivots = cmds.xform(root_node, q=True, pivots=True, ws=True)

    is_accepted = __is_under_torelance(pivots)

    if is_accepted:
        param_item.unerror_target_list.append(root_node)
    else:
        param_item.error_target_list.append(root_node)


def check_root_translate(param_item, args):
    """Root骨のTranslateが原点に存在しているか

    Args:
        param_item (CheckerParamItem): Checker Paramの情報を格納したクラス
    """
    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node

    if not cmds.objExists(root_node):
        return

    root_joint = root_node + '|Root'

    if not cmds.objExists(root_joint) or cmds.objectType(root_joint) != 'joint':
        return

    # ------------------------------
    # 情報
    param_item.info_target_list.append(root_joint)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = [root_joint]

    # root jointが原点か
    root_joint_translate = cmds.xform(root_joint, q=True, t=True, ws=True)

    # 厳密には0でないものもあるため一定の誤差は許容
    is_accepted = __is_under_torelance(root_joint_translate)

    if is_accepted:
        param_item.unerror_target_list.append(root_joint)
    else:
        param_item.error_target_list.append(root_joint)


def check_root_jointorient(param_item, args):
    """Root骨のjoint Orientがすべて0か確認する

    Args:
        param_item (CheckerParamItem): Checker Paramの情報を格納したクラス
    """
    # ------------------------------
    # 設定

    root_node = param_item.main.chara_info.part_info.root_node

    if not cmds.objExists(root_node):
        return

    root_joint = root_node + '|Root'

    if not cmds.objExists(root_joint) or cmds.objectType(root_joint) != 'joint':
        return

    # ------------------------------
    # 情報
    param_item.info_target_list.append(root_joint)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    param_item.check_target_list = [root_joint]

    root_joint_orient = cmds.getAttr("{0}.jointOrient".format(root_joint))[0]

    # 厳密には0でないものもあるため一定の誤差は許容
    is_accepted = __is_under_torelance(root_joint_orient)

    if is_accepted:
        param_item.unerror_target_list.append(root_joint)
    else:
        param_item.error_target_list.append(root_joint)


def __is_under_torelance(examine_target, offset=0.0):
    """許容値以内に収まっているか検証します

    Args:
        examine_target (int, float, list, tupple): 確認対象のデータです。
        offset (float, optional): 値をオフセットする必要がある場合指定します. Defaults to 0.0.
    """

    SINGLE_ITEM_TYPE_LIST = [float, int]
    MULTI_ITEM_TYPE_LIST = [tuple, list]

    # 対応型以外が来た場合にはFalseでreturnする
    if type(examine_target) not in SINGLE_ITEM_TYPE_LIST + MULTI_ITEM_TYPE_LIST:
        return False

    is_accepted = True

    # 要素数が1つであるtype
    if type(examine_target) in SINGLE_ITEM_TYPE_LIST:
        if abs(examine_target) > define.TORELANCE + offset:
            is_accepted = False

    # 複数要素を含むタイプの場合はこの関数を再帰的に呼ぶ
    else:
        for item in examine_target:
            if not __is_under_torelance(item, offset):
                is_accepted = False
                break

    return is_accepted


def check_single_bindpose(param_item, arg):
    """
    バインドポーズが複数設定されていないか確認
    """

    # ------------------------------
    # 情報

    root_node = param_item.main.chara_info.part_info.root_node

    if not root_node or not cmds.objExists(root_node):
        return

    all_joints = cmds.listRelatives(root_node, ad=True, type='joint', f=True)

    if not all_joints:
        return

    param_item.info_target_list = all_joints

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = param_item.info_target_list

    dag_poses = cmds.dagPose(param_item.check_target_list, q=True, bp=True)

    if dag_poses and len(dag_poses) > 1:
        param_item.error_target_list.extend(param_item.check_target_list)
    else:
        param_item.unerror_target_list.extend(param_item.check_target_list)


# endregion

# region アウトライン系


# ==================================================
def check_outline_exist(param_item, arg):
    """
    _Outlineノードが存在するかチェック
    """

    # ------------------------------
    # 情報

    outline_list = []

    for outline_mesh_param in param_item.main.chara_info.part_info.outline_mesh_param_list:

        if not outline_mesh_param['check']:
            continue

        outline_list.append(outline_mesh_param['name'])

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in outline_list:

        param_item.check_target_list.append(mesh)

        if not base_utility.transform.exists(mesh):
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

    outline_list = []

    for outline_mesh_param in param_item.main.chara_info.part_info.outline_mesh_param_list:

        if not outline_mesh_param['check']:
            continue

        outline_list.append(outline_mesh_param['name'])

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in outline_list:

        if not base_utility.transform.exists(mesh):
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        # 元ノードを取得
        org_mesh = mesh.replace('_Outline', '')

        if not base_utility.transform.exists(org_mesh):
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
                if not base_utility.value.is_same(org_vtx_pos, vtx_pos, 0.001):
                    param_item.error_target_list.append(
                        mesh + '.vtx[%s]' % str(index))
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

    outline_list = []

    for outline_mesh_param in param_item.main.chara_info.part_info.outline_mesh_param_list:

        if not outline_mesh_param['check']:
            continue

        outline_list.append(outline_mesh_param['name'])

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in outline_list:

        if not base_utility.transform.exists(mesh):
            continue

        vertex_list = base_utility.mesh.get_vertex_list(mesh)

        if not vertex_list:
            continue

        param_item.check_target_list.extend(vertex_list)

        # 元ノードを取得
        org_mesh = mesh.replace('_Outline', '')

        if not base_utility.transform.exists(org_mesh):
            continue

        org_vtx_color_info_list = base_utility.mesh.vertex_color.get_all_vertex_color_info_list(
            org_mesh)
        vtx_color_list = base_utility.mesh.vertex_color.get_all_vertex_color_info_list(
            mesh)

        if not org_vtx_color_info_list or not vtx_color_list:
            param_item.error_target_list.extend(vertex_list)
            continue

        if len(org_vtx_color_info_list) != len(vtx_color_list):
            param_item.error_target_list.extend(vertex_list)
            continue

        for (org_vtxs, vtxs) in zip(org_vtx_color_info_list, vtx_color_list):
            index = org_vtxs[0]
            for (org_vtx_color, vtx_color) in zip(org_vtxs[2], vtxs[2]):
                if org_vtx_color != vtx_color:
                    param_item.error_target_list.append(
                        mesh + '.vtx[%s]' % str(index))
                    break

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

    outline_list = []

    for outline_mesh_param in param_item.main.chara_info.part_info.outline_mesh_param_list:

        if not outline_mesh_param['check']:
            continue

        # 非多様体フェース検出問題の暫定処置
        if outline_mesh_param['name'].find('M_Face') >= 0:
            continue

        outline_list.append(outline_mesh_param['name'])

    param_item.info_target_list = outline_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    for mesh in outline_list:

        if not base_utility.transform.exists(mesh):
            continue

        edge_list = cmds.ls('{}.e[*]'.format(mesh), l=True, fl=True)
        info_list = cmds.polyInfo(edge_list, ev=True)

        if not edge_list:
            continue

        param_item.check_target_list.extend(edge_list)

        this_error_target_list = \
            base_utility.mesh.cleanup.check_nonmanifold(
                mesh, False
            )

        if this_error_target_list:
            param_item.error_target_list.append('{0}{1}当該のメッシュには非多様体フェースがあるためチェックできません'.format(mesh, param_item.root.info_window.detail_separator))
            continue

        # 全エッジ番号で境界エッジを検索する
        edge_border_index_list = cmds.polySelect(mesh, q=True, eb=list(range(len(edge_list))))
        edge_reg = r'e\[([0-9]*)\]'

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
        cmds.ls(param_item.info_target_list, dag=True, l=True, typ='transform')

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

    all_locator_param_list = param_item.main.chara_info.part_info.locator_param_list
    root_node = param_item.main.chara_info.part_info.root_node
    target_locator_list = []

    if not all_locator_param_list or not root_node:
        return

    for locator_param in all_locator_param_list:

        # 必須ではなく、存在しないロケーターはスルー
        if not locator_param['check'] and not cmds.objExists(locator_param['name']):
            continue

        # root_node直下のロケーターのみが対象
        if len(locator_param['name'].replace('{}|'.format(root_node), '').split('|')) == 1:

            # かつ、positionは除く
            if locator_param['name'] != '{0}|Position'.format(root_node):
                target_locator_list.append(locator_param['name'])

    if not target_locator_list:
        return

    param_item.info_target_list = target_locator_list

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_locator_list

    for locator in param_item.check_target_list:

        if not cmds.objExists(locator):
            param_item.error_target_list.append('{0} が存在しません。'.format(locator))
            continue

        if cmds.listConnections(locator, t='dagPose'):
            param_item.error_target_list.append(locator)
            continue

        param_item.unerror_target_list.append(locator)


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
def check_turtle_node(param_item, arg):
    """
    Turtleノードが含まれていないか確認
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

    name_starts_with_turtle_node = cmds.ls('Turtle*', showType=True)

    for i in range(len(name_starts_with_turtle_node) // 2):

        node_name = name_starts_with_turtle_node[i * 2]
        node_type = name_starts_with_turtle_node[i * 2 + 1]

        if node_type.startswith('ilr') or node_type == 'unknown':
            param_item.error_target_list.append(node_name)

    if len(param_item.error_target_list) == 0:
        param_item.unerror_target_list.append(this_scene)


def check_display_layer(param_item, arg):
    """
    不要なディスプレイレイヤーのチェック
    """

    DISPLAY_LAYER_LIST_GENERAL_BODY = [
        'joint_layer',
        'original_layer',
        'height_layer',
        'shape_layer',
        'bust_layer'
    ]

    DISPLAY_LAYER_LIST_MINI_GENERAL_BODY = [
        'joint_layer_Mini',
        'original_layer_Mini',
        'height_layer_Mini',
        'shape_layer_Mini',
        'bust_layer_Mini'
    ]

    # ------------------------------
    # 情報

    this_scene = cmds.file(q=True, sn=True, exn=True)

    param_item.info_target_list = [this_scene]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = [this_scene]

    display_layer_list = cmds.ls(typ='displayLayer')

    if len(display_layer_list) != 1:

        accepted_display_layer_list = []

        if param_item.main.chara_info.is_common_body:
            if param_item.main.chara_info.is_mini:
                accepted_display_layer_list = DISPLAY_LAYER_LIST_MINI_GENERAL_BODY
            else:
                accepted_display_layer_list = DISPLAY_LAYER_LIST_GENERAL_BODY

        for display_layer in display_layer_list:
            if display_layer != 'defaultLayer':

                if display_layer not in accepted_display_layer_list:
                    param_item.error_target_list.append(display_layer)

    if len(param_item.error_target_list) == 0:
        param_item.unerror_target_list.append(this_scene)


# ==================================================
def check_particular_node_position(param_item, args):
    """
    「mdl_(bdy|chr)xxxx_xx」「Position」「M_Body」「M_Hair」「M_Face」ノードの位置が0かどうかのチェック
    """
    # ------------------------------
    # 情報

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    param_item.info_target_list = [
        root_node,
        '{0}|Position'.format(root_node),
        '{0}|M_Body'.format(root_node),
        '{0}|M_Face'.format(root_node),
        '{0}|M_Hair'.format(root_node),
    ]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    param_item.check_target_list = param_item.info_target_list

    for node in param_item.check_target_list:

        if not cmds.objExists(node):
            continue

        translate = base_utility.attribute.get_value(
            node, 'translate'
        )

        if translate == [0.0, 0.0, 0.0]:
            param_item.unerror_target_list.append(node)
        else:
            param_item.error_target_list.append(node)


# ==================================================
def check_particular_node_pivot_position(param_item, args):
    """
    「mdl_(bdy|chr)xxxx_xx」「Position」「M_Body」「M_Hair」「M_Face」ノードのピボット位置が原点かどうかのチェック
    """
    # ------------------------------
    # 情報

    root_node = param_item.main.chara_info.part_info.root_node
    if not root_node:
        return

    param_item.info_target_list = [
        root_node,
        '{0}|Position'.format(root_node),
        '{0}|M_Body'.format(root_node),
        '{0}|M_Face'.format(root_node),
        '{0}|M_Hair'.format(root_node),
    ]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック
    param_item.check_target_list = param_item.info_target_list

    for node in param_item.check_target_list:

        if not cmds.objExists(node):
            continue

        pivots = cmds.xform(node, q=True, pivots=True)

        if pivots == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]:
            param_item.unerror_target_list.append(node)
        else:
            param_item.error_target_list.append(node)


def check_unknown_node(param_item, arg):
    """
    unknownノードが含まれていないか確認
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

    # unknownノードの取得
    unknown_nodes = cmds.ls(type='unknown')
    if unknown_nodes:
        param_item.error_target_list.extend(unknown_nodes)
    else:
        param_item.unerror_target_list.append(this_scene)


def check_unknown_plugin(param_item, arg):
    """
    unknownプラグインが含まれていないか確認
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

    # unknownプラグインの取得
    initial_unknown_plugins = cmds.unknownPlugin(q=True, list=True)
    unknown_plugins = []
    if initial_unknown_plugins:

        for plugin in initial_unknown_plugins:

            # ロードできているのにUnknownPluginとしてリストされるものがあるのでダブルチェック
            if cmds.pluginInfo(plugin, q=True, loaded=True):
                continue
            else:
                unknown_plugins.append(plugin)

    if unknown_plugins:
        param_item.error_target_list.extend(unknown_plugins)
    else:
        param_item.unerror_target_list.append(this_scene)

# endregion
