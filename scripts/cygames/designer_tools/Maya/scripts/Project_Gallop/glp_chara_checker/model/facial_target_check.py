# -*- coding: utf-8 -*-
"""facialtarget系のチェック関数
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re
import csv

import maya.cmds as cmds

from ...base_common import classes as base_class
from . import util
from .. import define

try:
    from importlib import reload
except Exception:
    pass

reload(define)


def check_kiba_bone(param_item, arg):
    """
    キバ骨対応の骨回りが適切か確認
    """

    # 今回のキバ骨対応で追加されているべき骨
    should_exists_bone_list = [
        '|Neck|Head|Mouth_Root|Mouth_L|Mouth_sub_01_L',
        '|Neck|Head|Mouth_Root|Mouth_R|Mouth_sub_01_R'
    ]

    # 今回のキバ骨対応で削除されているべき骨
    should_delete_bone_list = [
        '|Neck|Head|Mouth_Root|Mouth_L|Mouth_sub_01'
    ]

    jnt_namespace = ''

    # ------------------------------
    # 情報

    param_item.info_target_list.extend(should_exists_bone_list)
    param_item.info_target_list.extend(should_delete_bone_list)

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    chara_full_id = param_item.main.chara_info.data_main_id + '_' + param_item.main.chara_info.data_sub_id

    param_item.check_target_list.extend(should_delete_bone_list)
    param_item.check_target_list.extend(should_exists_bone_list)

    if param_item.main.chara_info.is_facial_target:
        jnt_namespace = 'mdl_chr{0}'.format(chara_full_id)

    for should_delete_bone in should_delete_bone_list:

        # long_nameの頭にchara idを追加
        should_delete_bone = 'mdl_chr{0}{1}'.format(chara_full_id, should_delete_bone)

        renamed_should_delete_bone = util.add_namespace_to_ln(should_delete_bone, jnt_namespace)

        if cmds.objExists(renamed_should_delete_bone):
            param_item.error_target_list.append('{0}{1}除去されているべきジョイントが残っています。'.format(should_delete_bone, param_item.root.info_window.detail_separator))
        else:
            param_item.unerror_target_list.append(should_delete_bone)

    for should_exists_bone in should_exists_bone_list:

        # long_nameの頭にchara idを追加
        should_exists_bone = 'mdl_chr{0}{1}'.format(chara_full_id, should_exists_bone)

        # facial targetファイルの場合はnamespaceを付与する必要あり
        renamed_should_exists_bone = util.add_namespace_to_ln(should_exists_bone, jnt_namespace)

        param_item.check_target_list.append(renamed_should_exists_bone)

        if not cmds.objExists(renamed_should_exists_bone):
            param_item.error_target_list.append('{0}{1}追加されているべきジョイントがありません。'.format(should_exists_bone, param_item.root.info_window.detail_separator))
        else:
            param_item.unerror_target_list.append(should_exists_bone)


def check_kiba_bone_ctrl(param_item, arg):
    """
    キバ骨対応のコントローラが適切か確認
    """

    # 今回のキバ骨対応で追加されているべきコントローラー
    should_exists_ctrl_list = [
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_L_g|Mouth_L_Ctrl|Mouth_sub_01_L_g',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_L_g|Mouth_L_Ctrl|Mouth_sub_01_L_g|Mouth_sub_01_L_Ctrl',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_L_g|Mouth_L_Ctrl|Mouth_sub_01_L_g|Mouth_sub_01_L_Ctrl|Mouth_sub_01_L_c',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_R_g|Mouth_R_Ctrl|Mouth_sub_01_R_g',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_R_g|Mouth_R_Ctrl|Mouth_sub_01_R_g|Mouth_sub_01_R_Ctrl',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_R_g|Mouth_R_Ctrl|Mouth_sub_01_R_g|Mouth_sub_01_R_Ctrl|Mouth_sub_01_R_c',
    ]

    # 今回のキバ骨対応で削除されているべきコントローラー
    should_delete_ctrl_list = [
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_L_g|Mouth_L_Ctrl|Mouth_sub_01_g',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_L_g|Mouth_L_Ctrl|Mouth_sub_01_g|Mouth_sub_01_Ctrl',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_L_g|Mouth_L_Ctrl|Mouth_sub_01_g|Mouth_sub_01_Ctrl|Mouth_sub_01_c'
    ]

    rig_namespace = 'chara_checker_temp_import'

    is_face_target_file = param_item.main.chara_info.is_facial_target

    # ------------------------------
    # 情報

    target_path = param_item.main.chara_info.facial_target_path
    param_item.info_target_list = [target_path]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.extend(should_delete_ctrl_list)
    param_item.check_target_list.extend(should_exists_ctrl_list)
    ref_ctrl = base_class.reference.ReferenceController()

    if not os.path.exists(target_path):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_path))
        return

    if is_face_target_file:
        rig_namespace = ''
    else:
        ref_ctrl.load_using_no_plugin_tmp(target_path, rig_namespace, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{0}が{1}ため'.format(ref_ctrl.file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            return

    for should_delete_ctrl in should_delete_ctrl_list:

        target_ctrl_long_name = util.add_namespace_to_ln(should_delete_ctrl, rig_namespace)

        if cmds.objExists(target_ctrl_long_name):
            param_item.error_target_list.append('{0}{1}除去されているべきコントローラが残っています。'.format(should_delete_ctrl, param_item.root.info_window.detail_separator))
        else:
            param_item.unerror_target_list.append(should_delete_ctrl)

    for should_exists_ctrl in should_exists_ctrl_list:

        param_item.check_target_list.append(should_exists_ctrl)

        target_ctrl_long_name = util.add_namespace_to_ln(should_exists_ctrl, rig_namespace)

        if not cmds.objExists(target_ctrl_long_name):
            param_item.error_target_list.append('{0}{1}追加されているべきコントローラが存在しません。'.format(should_exists_ctrl, param_item.root.info_window.detail_separator))
        else:
            param_item.unerror_target_list.append(should_exists_ctrl)

    if not is_face_target_file:
        ref_ctrl.unload(unload_hard=True)


def check_kiba_bone_base_key(param_item, arg):
    """
    キバ骨対応のベースキーがちゃんと打たれているか確認
    """

    # ベースキーを打つ対象のctrl
    target_ctrl_ln = 'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_R_g|Mouth_R_Ctrl|Mouth_sub_01_R_g|Mouth_sub_01_R_Ctrl'

    rig_namespace = 'chara_checker_temp_import'

    is_face_target_file = param_item.main.chara_info.is_facial_target

    # ------------------------------
    # 情報

    target_path = param_item.main.chara_info.facial_target_path
    param_item.info_target_list = [target_path]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list.append(target_ctrl_ln)
    ref_ctrl = base_class.reference.ReferenceController()

    if not os.path.exists(target_path):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_path))
        return

    if is_face_target_file:
        rig_namespace = ''
    else:
        ref_ctrl.load_using_no_plugin_tmp(target_path, rig_namespace, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{0}が{1}ため'.format(ref_ctrl.file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            return

    renamed_target_ctrl = util.add_namespace_to_ln(target_ctrl_ln, rig_namespace)

    if not cmds.objExists(renamed_target_ctrl):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_ctrl_ln))
        if not is_face_target_file:
            ref_ctrl.unload(unload_hard=True)
        return

    anim_layer_list = cmds.ls(type='animLayer')

    if len(anim_layer_list) > 0:
        cmds.animLayer('BaseAnimation', selected=True, preferred=True, e=True)

    if not len(cmds.keyframe(renamed_target_ctrl, t=(0, 1000), q=True)) > 0:
        param_item.error_target_list.append(target_ctrl_ln)
    else:
        param_item.unerror_target_list.append(target_ctrl_ln)

    if not is_face_target_file:
        ref_ctrl.unload(unload_hard=True)


def check_kiba_bone_anim_layer(param_item, arg):
    """
    Mouth_sub_01_R_Ctrlをアニメーションレイヤに追加しているか確認
    """

    # Mouth_sub_01_R_Ctrlをアニメーションレイヤに追加されているべきアニメーションレイヤー
    should_exists_anim_layer_list = [
        'Mo_LowAngle',
        'Mo_Offset_D',
        'Mo_Offset_L',
        'Mo_Offset_R',
        'Mo_Offset_U',
        'Mo_Scale_D',
        'Mo_Scale_U'
    ]

    rig_namespace = 'chara_checker_temp_import'
    target_ctrl = 'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Mouth_R_g|Mouth_R_Ctrl|Mouth_sub_01_R_g|Mouth_sub_01_R_Ctrl'

    is_face_target_file = param_item.main.chara_info.is_facial_target

    # ------------------------------
    # 情報

    target_path = param_item.main.chara_info.facial_target_path
    param_item.info_target_list = [target_path]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = should_exists_anim_layer_list
    ref_ctrl = base_class.reference.ReferenceController()

    if not os.path.exists(target_path):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_path))
        return

    if is_face_target_file:
        rig_namespace = ''

    else:
        ref_ctrl.load_using_no_plugin_tmp(target_path, rig_namespace, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{0}が{1}ため'.format(ref_ctrl.file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            return

    renamed_target = util.add_namespace_to_ln(target_ctrl, rig_namespace)

    if not cmds.objExists(renamed_target):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_ctrl))
        if not is_face_target_file:
            ref_ctrl.unload(unload_hard=True)
        return

    current_selected_item = cmds.ls(selection=True)
    cmds.select(renamed_target)
    anim_layer_list = cmds.animLayer(afl=True, q=True)

    if anim_layer_list is None:
        param_item.error_target_list.append('{0}{1}{0}にアニメーションレイヤー接続されていません。'.format(target_ctrl, param_item.root.info_window.detail_separator))
        if not is_face_target_file:
            ref_ctrl.unload(unload_hard=True)
        return

    for should_exists_anim_layer in should_exists_anim_layer_list:

        if not rig_namespace == '':
            renamed_anim_layer = rig_namespace + ':' + should_exists_anim_layer
        else:
            renamed_anim_layer = should_exists_anim_layer

        if renamed_anim_layer not in anim_layer_list:
            param_item.error_target_list.append('{0}が存在しません。'.format(should_exists_anim_layer))

        else:
            param_item.unerror_target_list.append(should_exists_anim_layer)

    if not is_face_target_file:
        ref_ctrl.unload(unload_hard=True)

    cmds.select(current_selected_item)


def check_tooth_scale_offset(param_item, arg):
    """
    Tooth_bottom_Ctrl, tooth_up_ctrlのスケール値がBaseAnimationで1000Fに1.0でセットされているか
    """
    # キーが入っているはずのAnimation layer
    target_anmlayer = [
        'BaseAnimation',
        'Mo_Offset_R',
        'Mo_Offset_L',
        'Mo_Offset_D',
        'Mo_Offset_U',
        'Mo_Scale_D',
        'Mo_Scale_U',
        'Mo_LowAngle',
    ]

    # 検索対象のCtrl
    target_ctrl_list = [
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Tooth_up_g|Tooth_up_Ctrl',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Mouth_Root_g|Mouth_Root_Ctrl|Tooth_bottom_g|Tooth_bottom_Ctrl',
    ]

    # 検索対象のattr
    target_attr_list = [
        '.scaleX',
        '.scaleY',
        '.scaleZ',
    ]

    rig_namespace = 'chara_checker_temp_import'

    is_face_target_file = param_item.main.chara_info.is_facial_target

    # ------------------------------
    # 情報

    target_path = param_item.main.chara_info.facial_target_path
    param_item.info_target_list = [target_path]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_ctrl_list
    ref_ctrl = base_class.reference.ReferenceController()

    if not os.path.exists(target_path):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_path))
        return

    if is_face_target_file:
        rig_namespace = ''
    else:
        ref_ctrl.load_using_no_plugin_tmp(target_path, rig_namespace, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{0}が{1}ため'.format(ref_ctrl.file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            return

    anim_layer_list = cmds.ls(type='animLayer')
    if len(anim_layer_list) == 0:
        # 空のリストではエラーになるため、識別用データ
        anim_layer_list = ['ANIMATION_LAYER_NOT_FOUND_GLP_CHECKER']

    # animation layerの状態を保存
    is_anmlayer_selected = {}
    is_anmlayer_preferred = {}
    for animation_layer in anim_layer_list:
        if animation_layer != 'ANIMATION_LAYER_NOT_FOUND_GLP_CHECKER':
            is_anmlayer_selected[animation_layer] = cmds.animLayer(animation_layer, selected=True, q=True)
            is_anmlayer_preferred[animation_layer] = cmds.animLayer(animation_layer, preferred=True, q=True)
            cmds.animLayer(animation_layer, preferred=False, e=True)

    for animation_layer in anim_layer_list:

        if animation_layer != 'ANIMATION_LAYER_NOT_FOUND_GLP_CHECKER':
            cmds.animLayer(animation_layer, selected=True, preferred=True, e=True)

        for target_ctrl in target_ctrl_list:
            renamed_target_ctrl = util.add_namespace_to_ln(target_ctrl, rig_namespace)

            if not cmds.objExists(renamed_target_ctrl):
                param_item.error_target_list.append('{0}が存在しません。'.format(target_ctrl))
                continue

            for target_attr in target_attr_list:

                # キーフレーム自体は打たれていて、かつ1.0にセットされていないもののみ検出
                if cmds.keyframe(renamed_target_ctrl + target_attr, time=(1000, 1000), eval=True, q=True) == [1.0]:
                    param_item.unerror_target_list.append('{0}{1}{2}の{3}にエラーが存在します'.format(target_ctrl, param_item.root.info_window.detail_separator, animation_layer, target_attr[1:]))
                elif cmds.keyframe(renamed_target_ctrl + target_attr, t=(1000, 1000), q=True) \
                        and animation_layer in target_anmlayer:
                    param_item.error_target_list.append('{0}{1}{2}の{3}にエラーが存在します'.format(target_ctrl, param_item.root.info_window.detail_separator, animation_layer, target_attr[1:]))

        if animation_layer != 'ANIMATION_LAYER_NOT_FOUND_GLP_CHECKER':
            cmds.animLayer(animation_layer, selected=False, preferred=False, e=True)

    # animation layerの状態を復元
    for animation_layer in anim_layer_list:
        if animation_layer != 'ANIMATION_LAYER_NOT_FOUND_GLP_CHECKER':
            cmds.animLayer(animation_layer, selected=is_anmlayer_selected[animation_layer], preferred=is_anmlayer_preferred[animation_layer], e=True)

    if not is_face_target_file:
        ref_ctrl.unload(unload_hard=True)


def check_eyes_within_range(param_item, arg):
    """
    全表情で目の動きがX, Yrangeの範囲内に収まっているか
    """

    # X, Yrangeのフレーム
    x_range_frame = 420
    y_range_frame = 422

    # チェック除外フレーム
    # 表情のニュアンスのため意図して範囲外に出ているフレームもあるための対応
    skip_x_range_frame_list = [192]
    skip_y_range_frame_list = []

    # 調査する最終フレーム
    facial_end_frame = 1000

    # 検索対象のCtrl
    target_ctrl_list = [
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Eye_L_g|Eye_L_Ctrl',
        'Rig_head|Neck_g|Neck_Ctrl|Head_g|Head_Ctrl|Eye_R_g|Eye_R_Ctrl',
    ]

    # キーが入っているAnimation layer
    target_anim_layer = 'BaseAnimation'

    rig_namespace = 'chara_checker_temp_import'

    is_face_target_file = param_item.main.chara_info.is_facial_target

    # ------------------------------
    # 情報

    target_path = param_item.main.chara_info.facial_target_path
    param_item.info_target_list = [target_path]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    param_item.check_target_list = target_ctrl_list
    ref_ctrl = base_class.reference.ReferenceController()

    if not os.path.exists(target_path):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_path))
        return

    if is_face_target_file:
        rig_namespace = ''
    else:
        ref_ctrl.load_using_no_plugin_tmp(target_path, rig_namespace, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{0}が{1}ため'.format(ref_ctrl.file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            return

    # animLayer情報の取得
    anim_layer_list = cmds.ls(type='animLayer')
    org_anmlayer_selection_dict = {}
    org_anmlayer_preferred_dict = {}

    for anim_layer in anim_layer_list:
        org_anmlayer_selection_dict[anim_layer] = cmds.animLayer(anim_layer, selected=True, q=True)
        org_anmlayer_preferred_dict[anim_layer] = cmds.animLayer(anim_layer, preferred=True, q=True)
        # 情報を取得したら選択を解除しておく
        cmds.animLayer(anim_layer, selected=False, preferred=False, e=True)

    # 目のキーが打たれているanimLayerを選択
    if target_anim_layer in anim_layer_list:
        cmds.animLayer(target_anim_layer, selected=True, preferred=True, e=True)

    # X, Yrangeを取得
    x_range_min_max = __get_eye_range(
        util.add_namespace_to_ln(target_ctrl_list[0], rig_namespace),
        util.add_namespace_to_ln(target_ctrl_list[1], rig_namespace),
        x_range_frame,
        '.translateX'
    )
    y_range_min_max = __get_eye_range(
        util.add_namespace_to_ln(target_ctrl_list[0], rig_namespace),
        util.add_namespace_to_ln(target_ctrl_list[1], rig_namespace),
        y_range_frame,
        '.translateY'
    )
    if not x_range_min_max or not y_range_min_max:
        param_item.error_target_list.append('X, Yrangeが取得できません')

    # チェック用のattrリスト
    check_x_attr_list = [
        util.add_namespace_to_ln('{}{}'.format(target_ctrl_list[0], '.translateX'), rig_namespace),
        util.add_namespace_to_ln('{}{}'.format(target_ctrl_list[1], '.translateX'), rig_namespace),
    ]
    check_y_attr_list = [
        util.add_namespace_to_ln('{}{}'.format(target_ctrl_list[0], '.translateY'), rig_namespace),
        util.add_namespace_to_ln('{}{}'.format(target_ctrl_list[1], '.translateY'), rig_namespace),
    ]
    error_attr_list = []

    # キーが打たれているフレームのリスト
    tmp_frame_list = []
    for attr in (check_x_attr_list + check_y_attr_list):
        tmp_frame_list.extend(cmds.keyframe(attr, time=(0, facial_end_frame), query=True))
    all_key_frame_list = list(set(tmp_frame_list))
    all_key_frame_list.sort()

    # どのフレームでもrangeを超えていないかをチェックする
    for frame in all_key_frame_list:

        if frame not in skip_x_range_frame_list:
            for x_attr in check_x_attr_list:
                if not x_range_min_max[0] <= cmds.getAttr(x_attr, t=frame) <= x_range_min_max[1]:
                    param_item.error_target_list.append('{} は {} フレームでXrange({},{})を超えています'.format(x_attr.split('|')[-1], frame, x_range_min_max[0], x_range_min_max[1]))
                    if x_attr not in error_attr_list:
                        error_attr_list.append(x_attr)

        if frame not in skip_y_range_frame_list:
            for y_attr in check_y_attr_list:
                if not y_range_min_max[0] <= cmds.getAttr(y_attr, t=frame) <= y_range_min_max[1]:
                    param_item.error_target_list.append('{} は {} フレームでYrange({},{})を超えています'.format(y_attr.split('|')[-1], frame, y_range_min_max[0], y_range_min_max[1]))
                    if y_attr not in error_attr_list:
                        error_attr_list.append(y_attr)

    # エラー外のチェック
    for attr in (check_x_attr_list + check_y_attr_list):
        if attr not in error_attr_list:
            param_item.unerror_target_list.append(attr)

    # animation layerの状態を復元
    for anim_layer in anim_layer_list:
        cmds.animLayer(anim_layer, selected=org_anmlayer_selection_dict[anim_layer], preferred=org_anmlayer_preferred_dict[anim_layer], e=True)

    if not is_face_target_file:
        ref_ctrl.unload(unload_hard=True)


def __get_eye_range(eye_controller_L, eye_controller_R, range_frame, range_attr):
    """
    eye_rangeの(min, max)を返す
    """

    # 目のコントローラーが揃っていない場合
    if not cmds.objExists(eye_controller_L) or not cmds.objExists(eye_controller_R):
        return None

    l_value = cmds.getAttr(eye_controller_L + range_attr, t=range_frame)
    r_value = cmds.getAttr(eye_controller_R + range_attr, t=range_frame)

    if l_value < r_value:
        return (l_value, r_value)
    else:
        return (r_value, l_value)


def check_facial_keyframes(param_item, arg):
    """baseから表情が切り替わっているかを検証する
    """

    rig_namespace = 'chara_checker_temp_import'
    is_face_target_file = param_item.main.chara_info.is_facial_target

    # ブラックリスト方式で検出除外する対象を設定する
    # keyがコントローラーのマッチ条件でvalueが除外フレーム。*で全フレーム指定
    IGNORE_OBJ_DICT = {
        '.*sub.*': ['*'],
        '(|.*:)Eyebrow_04_(L|R)_Ctrl': ['!454', '!456'],
    }

    IGNORE_PART_DICT = {
        'Eye_(L|R)': ['444']
    }

    # ------------------------------
    # 情報

    target_path = param_item.main.chara_info.facial_target_path
    param_item.info_target_list = [target_path]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    ctrl_part_dict = __generate_facial_ctrl_part_dict()
    param_item.check_target_list = ctrl_part_dict
    if not ctrl_part_dict:
        param_item.unerror_target_list.append('対象となるCtrlの設定が発見できませんでした')
        return

    inspection_key_dict = __generate_facial_timing_dict()
    if not inspection_key_dict:
        param_item.unerror_target_list.append('対象となるキーの設定が発見できませんでした')
        return

    ref_ctrl = base_class.reference.ReferenceController()

    # facial targetファイルの存在確認
    if not os.path.exists(target_path):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_path))
        return

    if is_face_target_file:
        rig_namespace = ''
    else:
        ref_ctrl.load_using_no_plugin_tmp(target_path, rig_namespace, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{0}が{1}ため'.format(ref_ctrl.file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            return

    # 監査対象アトリビュートの選定
    ctrl_part_attr_dict = dict()
    for current_part, obj_names in ctrl_part_dict.items():

        obj_attr_dict = dict()

        for obj_name in obj_names:

            # フェイシャルターゲットをロードしてある場合はネームスペースを付与する
            if not is_face_target_file:
                obj_name = '{0}:{1}'.format(rig_namespace, obj_name)

            target_attrs = []

            # キバ骨対応などでctrlに差異があることがあるためチェック
            current_ls = cmds.ls(obj_name)
            if len(current_ls) == 0:
                # バッチ実行時に出力される可能性のあるメッセージで日本語を使うと文字コードエラーを吐く
                print('[Info] Ctrl {0} is not found.'.format(obj_name))
                continue
            # 複数ヒットしてしまう場合はエラーに追加
            elif len(current_ls) > 1:
                # バッチ実行時に出力される可能性のあるメッセージで日本語を使うと文字コードエラーを吐く
                print('[Error] Ctrl {0} cannot be identified.'.format(obj_name))
                param_item.error_target_list.append('{0}を同定できません。同じ名前のオブジェクトが複数存在していませんか?'.format(obj_name))
                continue

            # animation系のノードがつながっていれば、監査対象に追加
            for attr in cmds.listAttr(obj_name, keyable=True):

                currnt_target = obj_name + '.' + attr
                connections = cmds.listConnections(currnt_target, s=True)

                if connections:

                    contain_anim = False
                    for item in connections:

                        current_type = cmds.objectType(item)
                        if current_type.startswith('anim'):
                            contain_anim = True
                            break

                    if contain_anim:
                        target_attrs.append(currnt_target)

            obj_attr_dict[obj_name] = target_attrs

        if obj_attr_dict:
            ctrl_part_attr_dict[current_part] = obj_attr_dict.copy()

    # 初期値のリストを作成
    base_value_dict = dict()
    for obj_attr_dict in ctrl_part_attr_dict.values():
        for obj_name in obj_attr_dict.keys():
            for current_attr in obj_attr_dict[obj_name]:
                base_value_dict[current_attr] = cmds.getAttr(current_attr, t=0)

    for current_frame, parts in sorted(inspection_key_dict.items()):

        # 0, 1000は初期値が入っているはずなので除外
        if current_frame == 1000 or current_frame == 0:
            continue

        error_items = []
        for current_part in parts:

            is_change = False

            # パーツのブラックリストをマッチ
            if __is_ignore_pattern(current_part, current_frame, IGNORE_PART_DICT):
                continue

            for current_obj in ctrl_part_attr_dict[current_part]:

                # objのブラックリストをマッチ
                if __is_ignore_pattern(current_obj, current_frame, IGNORE_OBJ_DICT):
                    continue

                for current_attr in ctrl_part_attr_dict[current_part][current_obj]:
                    current_value = cmds.getAttr(current_attr, t=current_frame)

                    # 同値でないならフラグ立てて抜ける
                    if current_value != base_value_dict[current_attr]:
                        is_change = True
                        break

                # 検出の単位はパーツごとのため、すでに変更が入っているならあとのオブジェクトの処理は飛ばす
                if is_change:
                    break

            if not is_change:
                error_items.append(current_part)

        if not error_items:
            param_item.unerror_target_list.append(current_frame)
        else:
            param_item.error_target_list.append('{0}frameで{1}がBase表情のままになっています'.format(current_frame, ','.join(error_items)))

    if not is_face_target_file:
        ref_ctrl.unload(unload_hard=True)


def __generate_facial_ctrl_part_dict():
    """CSVからパーツが含むCtrl情報のdictを作成

    Returns:
        dict: keyがパーツ名、valueがメンバーのdict
        {
            'Eyebrow_L': [
                'Eyebrow_offset_L_Ctrl',
                'Eyebrow_01_L_Ctrl',
                'Eyebrow_02_L_Ctrl',
                ...
            ],
            'Eye_R': [
                'Eye_R_Ctrl',
                'Eye_middle_01_R_Ctrl'.
                'Eye_up_01_R_Ctrl',
                ...
            ],
            ...
        }
    """

    if not os.path.exists(define.FACIAL_CNT_CSV):
        return

    driver_dict = dict()
    with open(define.FACIAL_CNT_CSV) as f:
        csv_dict = csv.DictReader(f)

        for current_line in csv_dict:
            part_name = current_line['Part']
            ctrl_name = current_line['ControllerName']

            if part_name not in driver_dict:
                driver_dict[part_name] = []

            driver_dict[part_name].append(ctrl_name)

    return driver_dict


def __generate_facial_timing_dict():
    """CSVからキーフレームのタイミングと対象パーツのdictを作成する

    Returns:
        dict: keyがキーフレーム、valueが対象パーツのdict
        {
            0 : [
                'Eyebrow_L',
                'Eyebrow_R',
                'Eye_L',
                ...
            ],
            4: [
                'Eye_L',
                'Eye_R'
            ],
            ...
        }
    """

    if not os.path.exists(define.FACIAL_TARGET_CSV):
        return

    key_dict = dict()
    with open(define.FACIAL_TARGET_CSV) as f:
        csv_dict = csv.DictReader(f)

        for current_line in csv_dict:
            part_name = current_line['Part']
            frame = int(current_line['Frame'])

            if frame not in key_dict:
                key_dict[frame] = []

            key_dict[frame].append(part_name)

    return key_dict


def __is_ignore_pattern(inspection_target, target_frame, pattern_dict):
    """与えられた条件で無効なパターンとマッチするかチェックする

    Args:
        inspection_target (str): 調査対象の文字列
        target_frame (int): 調査対象のフレーム
        pattern_dict (dict): ブラックリスト情報

    Returns:
        bool: ブラックリストにマッチしたか
    """

    target_frame_str = str(target_frame)

    for ignore_obj_pattern in pattern_dict:
        if re.match(ignore_obj_pattern, inspection_target):
            allow_only_match = False
            for ignore_frame in pattern_dict[ignore_obj_pattern]:

                # 全フレーム除外
                if ignore_frame == '*':
                    return True

                # 一部フレームのみ許可
                if ignore_frame.startswith('!'):
                    allow_only_match = True
                    if ignore_frame[1:] == target_frame_str:
                        return False

                # 一部フレームを除外
                elif ignore_frame == target_frame_str:
                    return True

            if allow_only_match:
                return True

    return False


def check_facial_symmetry(param_item, arg):
    """左右非対称なフェイシャルをチェックする

    左右対称をチェックするフレームとコントローラーはdefine内に記載されている
    """

    rig_namespace = 'chara_checker_temp_import'
    is_face_target_file = param_item.main.chara_info.is_facial_target

    # ------------------------------
    # 情報

    target_path = param_item.main.chara_info.facial_target_path
    param_item.info_target_list = [target_path]

    if not param_item.is_check_data:
        return

    # ------------------------------
    # チェック

    ref_ctrl = base_class.reference.ReferenceController()

    # facial targetファイルの存在確認
    if not os.path.exists(target_path):
        param_item.error_target_list.append('{0}が存在しません。'.format(target_path))
        return

    if is_face_target_file:
        rig_namespace = ''
    else:
        ref_ctrl.load_using_no_plugin_tmp(target_path, rig_namespace, True)
        if ref_ctrl.is_error:
            param_item.error_target_list.append('{0}が{1}ため'.format(ref_ctrl.file_path, ref_ctrl.reason))
            ref_ctrl.unload(unload_hard=True)
            return

    for key, value in define.FACIAL_SYMMETRY_CHECK_DATA.items():

        target_part = key
        left_controllers = value.get('controllers')
        frames = value.get('frames')

        exists_left_controllers = []
        exists_right_controllers = []
        for left_controller in left_controllers:
            if not is_face_target_file:
                left_controller = '{0}:{1}'.format(rig_namespace, left_controller)
            right_controller = left_controller.replace('_L', '_R')
            if not cmds.objExists(left_controller):
                param_item.error_target_list.append('コントローラー {} が見つかりませんでした'.format(left_controller))
            elif not cmds.objExists(right_controller):
                param_item.error_target_list.append('コントローラー {} が見つかりませんでした'.format(right_controller))
            else:
                exists_left_controllers.append(left_controller)
                exists_right_controllers.append(right_controller)

        for frame in frames:
            error_controller_pairs = []
            for left_controller, right_controller in zip(exists_left_controllers, exists_right_controllers):
                for attr_name in ['translate', 'rotate', 'scale']:

                    left_controller_attr_values = list(cmds.getAttr('{}.{}'.format(left_controller, attr_name), t=frame)[0])
                    right_controller_attr_values = list(cmds.getAttr('{}.{}'.format(right_controller, attr_name), t=frame)[0])

                    if not compare_attr_values(left_controller_attr_values, right_controller_attr_values):
                        error_controller_pairs.append([left_controller, right_controller])
                        break

            if not error_controller_pairs:
                param_item.unerror_target_list.append('部位: {} フレーム: {}'.format(target_part, frame))
            else:
                param_item.error_target_list.append(
                    '部位が {0} の {1} frameでコントローラー [{2}] がアシンメトリーな状態になっています'.format(
                        target_part, frame, ', '.join('{} ⇔ {}'.format(*pair) for pair in error_controller_pairs)
                    ))

    if not is_face_target_file:
        ref_ctrl.unload(unload_hard=True)


def compare_attr_values(values1, values2):
    """アトリビュートの数値同士の比較を行う

    Args:
        values1 (list): 比較するアトリビュートの数値リスト
        values2 (list): 比較するアトリビュートの数値リスト
    """

    if len(values1) != len(values2):
        return False

    for value1, value2 in zip(values1, values2):
        if abs(round(value1, 3) - round(value2, 3)) > 0.001:
            return False

    return True
