# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from . import cloth_collision_checker_command

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(cloth_collision_checker_command)


class ClothCollisionCheckerItemList(object):
    """
    チェッカーの要素の中身を構成するリスト
    """

    def __init__(self, root):
        """
        """

        cloth_collision_check_command_cls = cloth_collision_checker_command.ClothCollisionCheckerCommand(root)
        self.check_item_list = [
            # {
            #     'label': 'デバッグボタン',
            #     'description': 'デバッグボタン',
            #     'func': cloth_collision_check_command_cls.check_debug,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False
            # },
            {
                'label': 'シーン内の骨名とクロスデータ内の骨名が合致しているか',
                'description': 'シーン内の骨名とクロスデータ内の骨名が合致しているかチェックします。',
                'func': cloth_collision_check_command_cls.check_match_bone_name_for_cloth,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'cloth.Prefab内でboneNameが設定されていない項目はないか',
                'description': 'cloth.Prefab内でboneNameが設定されていない項目はないかチェックします。',
                'func': cloth_collision_check_command_cls.cheke_empty_bone_names,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'シーン内のSp骨がcloth.Prefab内で設定されているか',
                'description': 'シーン内のSp骨がcloth.Prefab内で設定されているかチェックします。\n※末端の骨・Sp_Ch_Bustは除きます',
                'func': cloth_collision_check_command_cls.check_cloth_data_in_name,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'ChildElementsのsizeが10以下か',
                'description': 'ChildElementsのsizeが10以下かチェックします。',
                'func': cloth_collision_check_command_cls.check_childElements_size,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'CollisionNameListのsizeが5以下か',
                'description': 'CollisionNameListのsizeが5以下かチェックします。',
                'func': cloth_collision_check_command_cls.check_collision_name_list_size,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'CollisionNameListの内でコリジョン名が重複していないか',
                'description': 'Collision Name Listの内でコリジョン名が\n重複していないかチェックします。',
                'func': cloth_collision_check_command_cls.check_duplicate_collision_name_list_value,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'クロス名が重複していないか',
                'description': 'クロス名が重複していないかチェックします。',
                'func': cloth_collision_check_command_cls.check_duplicate_bone_name,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'クロス名の接頭語が「Sp_」かどうか',
                'description': 'クロス名が全て「Sp_」からスタートしているかチェックします。',
                'func': cloth_collision_check_command_cls.check_bone_name_prefix,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'コリジョン名の接頭語が「Col」かどうか',
                'description': 'コリジョン名の接頭語が「Col」かどうかチェックします。',
                'func': cloth_collision_check_command_cls.check_collision_name_prefix,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            {
                'label': 'コリジョンのsize（全体の個数）が100以内か',
                'description': 'コリジョンのsize（全体の個数）が100以内かチェックします。',
                'func': cloth_collision_check_command_cls.check_all_collision_size,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
            # {
            #     'label': 'TargetObjectNameが「md_bdy/Position/」からか',
            #     'description': 'コリジョン内のTargetObjectNameが「md_body/Position/」から始まっているかチェックします。',
            #     'func': cloth_collision_check_command_cls.check_target_object_name_prefix,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False
            # },
            {
                'label': 'collisionNameListのサイズが1以上でなおかつ空でないか',
                'description': 'collisionNameListのサイズが1以上でなおかつ空でないかチェックします。',
                'func': cloth_collision_check_command_cls.check_collision_name_list_size_over_one,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False,
                'ui_button_for_error_bcg': [1, 1, 0]
            },
            # {
            #     'label': 'Offset2のxyzの値が全て0か',
            #     'description': 'Offset2のxyzの数値が全て0であるかチェックします。',
            #     'func': cloth_collision_check_command_cls.check_offset2_xyz_value_is_zero,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False,
            #     'ui_button_for_error_bcg': [1, 1, 0]
            # },
            # {
            #     'label': 'stiffnessの値が0.001～2の範囲内か',
            #     'description': 'stiffnessが0.001～2の範囲内かチェックします。',
            #     'func': cloth_collision_check_command_cls.check_stiffness_value,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False,
            #     'ui_button_for_error_bcg': [1, 1, 0]
            # },
            # {
            #     'label': 'dragforceの値が0.1～1.0の範囲内か',
            #     'description': 'drag forceが0.1～1.0の範囲内かチェックします。',
            #     'func': cloth_collision_check_command_cls.check_dragforce_value,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False,
            #     'ui_button_for_error_bcg': [1, 1, 0]
            # },
            {
                'label': 'CollisionNameListのコリジョンが存在しているか',
                'description': 'CollisionNameListのコリジョンがcollision.asset以下に存在しているかチェックします',
                'func': cloth_collision_check_command_cls.check_cloth_clild_collision_exists,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False,
                'ui_button_for_error_bcg': [1, 1, 0]
            },
            {
                'label': '未使用のコリジョンが存在しているか',
                'description': 'CollisionNameListで指定されていないコリジョンが存在しているかチェックします',
                'func': cloth_collision_check_command_cls.check_unassigned_collision,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False,
                'ui_button_for_error_bcg': [1, 1, 0]
            },
            {
                'label': 'gravityの値が0以外か',
                'description': 'gravityが0以外かどうかチェックします。',
                'func': cloth_collision_check_command_cls.detection_gravity_value,
                'args': [['_Ear', '_Bust'], True, 0, True],
                'is_select_button_view': False,
                'is_correction_button_view': False,
                'ui_button_for_error_bcg': [1, 1, 0]
            },
            {
                'label': 'Earのgravityの値が0になっているか',
                'description': 'Earのgravityの値が0になっているかどうかチェックします。',
                'func': cloth_collision_check_command_cls.detection_gravity_value,
                'args': [['_Ear'], False, 0, False],
                'is_select_button_view': False,
                'is_correction_button_view': False,
                'ui_button_for_error_bcg': [1, 1, 0]
            },
            # {
            #     'label': 'SpringForceの値が0か',
            #     'description': 'SpringForceが0かどうかチェックします。',
            #     'func': cloth_collision_check_command_cls.detection_Spring_force_value,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False,
            #     'ui_button_for_error_bcg': [1, 1, 0]
            # },
            # {
            #     'label': '1つの骨のコリジョン指定が全てCapsuleになってしまっていないか',
            #     'description': 'CollisionNameListのコリジョンが全てCapsuleタイプかチェックします。',
            #     'func': cloth_collision_check_command_cls.detection_cloth_collision_type,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False,
            #     'ui_button_for_error_bcg': [1, 1, 0]
            # },
            # {
            #     'label': 'Capabilityの値がNoneか',
            #     'description': 'CapabilityがNoneかチェックします。',
            #     'func': cloth_collision_check_command_cls.detection_capability_not_none,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False,
            #     'ui_button_for_error_bcg': [1, 1, 0]
            # },
            # {
            #     'label': 'CapsGroupIndexの値が0か',
            #     'description': 'CapsGroupIndexが0かチェックします。',
            #     'func': cloth_collision_check_command_cls.detection_caps_group_index_is_zero,
            #     'args': [],
            #     'is_select_button_view': False,
            #     'is_correction_button_view': False,
            #     'ui_button_for_error_bcg': [1, 1, 0]
            # },
            {
                'label': 'CollisionTargetNameにSp骨が指定されていないか',
                'description': 'CollisionTargetNameにSp骨が指定されていないかチェックします。',
                'func': cloth_collision_check_command_cls.check_target_object_name_into_sp,
                'args': [],
                'is_select_button_view': False,
                'is_correction_button_view': False
            },
        ]
