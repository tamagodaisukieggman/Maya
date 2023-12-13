# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re
import os

import maya.cmds as cmds

from . import cloth_collision_info as cci
from .. import check_answer_info as cai

try:
    from builtins import zip
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(cci)
reload(cai)


class ClothCollisionCheckerCommand(object):
    """
    チェッカー本体のコマンド
    """

    def __init__(self, root):
        """
        """

        self.root = root
        self.chara_info = root.chara_info

        self.COL_TYPE_CAPSULE = 2

        self.CAPABILITY_NONE = 0

    # ------------------------------------------------------------
    def get_cloth_prefab_path_list(self, target_part=''):
        """
        """

        self.chara_info = self.root.chara_info
        if not self.chara_info.exists:
            return []

        cloth_prefab_path_list = []

        target_part_info = None

        if target_part == 'head':
            target_part_info = self.chara_info.head_part_info
        elif target_part == 'body':
            target_part_info = self.chara_info.body_part_info
        elif target_part == 'tail':
            target_part_info = self.chara_info.tail_part_info
        elif target_part == 'attach':
            target_part_info = self.chara_info.attach_part_info
        else:
            target_part_info = self.chara_info.part_info

        if not target_part_info:
            return []

        cloth_dir = target_part_info.maya_clothes_dir_path
        cloth_data_name_list = target_part_info.cloth_list
        for cloth_data_name in cloth_data_name_list:

            # skirt.asset等prefabでないクロスデータは除く
            if not cloth_data_name.endswith('.prefab'):
                continue

            cloth_prefab_path_list.append(
                '{}/{}'.format(cloth_dir, cloth_data_name)
            )

        return cloth_prefab_path_list

    # ------------------------------------------------------------
    def get_bone_list(self):
        """
        positionノード以下のjointをすべて取得する
        """

        bone_list = []

        root_node = self.chara_info.part_info.root_node
        data_type = self.chara_info.part_info.data_type
        bone_root_node = None
        if data_type.endswith('head'):
            bone_root_node = '{}|Neck'.format(root_node)
        elif data_type.endswith('body'):
            bone_root_node = '{}|Position'.format(root_node)
        elif data_type.endswith('prop'):
            bone_root_node = '{}|Root'.format(root_node)
        elif data_type.endswith('tail'):
            bone_root_node = '{}|Hip'.format(root_node)

        if bone_root_node and cmds.objExists(bone_root_node):
            bone_list = cmds.listRelatives(bone_root_node, ad=True, pa=True, type='joint')

        return bone_list

    # ------------------------------------------------------------
    def get_cloth_collision_info_list(self, cloth_prefab_path_list, initialize_type):
        """
        positionノード以下のjointをすべて取得する
            :cloth_prefab_path_list: cloth_prefabファイルのパスリスト
            :initialize_type: 'cloth' or 'collision' or 'both'
        """

        if not cloth_prefab_path_list:
            return []

        info_initialize_paths_list = []

        if not self.chara_info.part_info.data_type.endswith('body'):

            for cloth_prefab_path in cloth_prefab_path_list:
                info_initialize_paths_list.append([cloth_prefab_path])

        # bodyはバストとセットで考える
        elif self.chara_info.part_info.data_type.find('general') >= 0:
            info_initialize_paths_list = self.__get_general_body_paths_list(cloth_prefab_path_list)

        else:
            info_initialize_paths_list = self.__get_unique_body_paths_list(cloth_prefab_path_list)

        cloth_col_info_list = []

        for info_initialize_paths in info_initialize_paths_list:

            cloth_col_info = cci.ClothCollisionInfo(info_initialize_paths)

            if initialize_type == 'cloth':
                cloth_col_info.create_cloth_info()
            elif initialize_type == 'collision':
                cloth_col_info.create_collision_info()
            elif initialize_type == 'both':
                cloth_col_info.create_cloth_info()
                cloth_col_info.create_collision_info()

            cloth_col_info_list.append(cloth_col_info)

        return cloth_col_info_list

    # ------------------------------------------------------------
    def __get_general_body_paths_list(self, cloth_prefab_path_list):
        """
        """

        bust_size_count = 4
        bust_flag = '_bust'

        info_initialize_paths_list = []

        for cloth_prefab_path in cloth_prefab_path_list:

            # ここではバストはスキップ
            if cloth_prefab_path.find(bust_flag) >= 0:
                continue

            # ここからバスト分組み合わせを作る
            for i in range(bust_size_count):
                this_bust_cloth = cloth_prefab_path.replace('_cloth', '{}{}_cloth'.format(bust_flag, str(i)))

                if this_bust_cloth in cloth_prefab_path_list:
                    info_initialize_paths_list.append([cloth_prefab_path, this_bust_cloth])
                else:
                    if [cloth_prefab_path] not in info_initialize_paths_list:
                        info_initialize_paths_list.append([cloth_prefab_path])

        return info_initialize_paths_list

    # ------------------------------------------------------------
    def __get_unique_body_paths_list(self, cloth_prefab_path_list):
        """
        """

        bust_flag = '_bust'

        info_initialize_paths_list = []

        for cloth_prefab_path in cloth_prefab_path_list:

            # ここではバストはスキップ
            if cloth_prefab_path.find(bust_flag) >= 0:
                continue

            # ここからバスト分組み合わせを作る
            this_bust_cloth = cloth_prefab_path.replace('_cloth', '{}_cloth'.format(bust_flag))

            if this_bust_cloth in cloth_prefab_path_list:
                info_initialize_paths_list.append([cloth_prefab_path, this_bust_cloth])
            else:
                info_initialize_paths_list.append([cloth_prefab_path])

        return info_initialize_paths_list

    # ------------------------------------------------------------

    def check_debug(self, is_query=False, args=[]):
        """
        デバッグボタン
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = self.get_bone_list()

        if not is_query:

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()

            invalid_object_name_list = []

            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'both')

            for cloth_col_info in cloth_col_info_list:

                for item_set in cloth_col_info.cloth_info:
                    print(item_set)
                    print(item_set['_boneName'])
                for item_set in cloth_col_info.collision_info:
                    print(item_set)
                    print(item_set['_collisionName'])

            if invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        ''
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_match_bone_name_for_cloth(self, is_query=False, args=[]):
        """
        シーン内の骨名とクロスデータ内の骨名が合致しているか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = self.get_bone_list()

        exclude_sp_joint_prefix_name_list = []

        if not self.chara_info.data_type.endswith('body'):
            # 対象外のSp骨
            exclude_sp_joint_prefix_name_list = ['Sp_Ch_Bust']

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                cloth_bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                bone_short_name_list = [bone_name.split('|')[-1] for bone_name in check_answer_info.check_target_item_list]

                for i in range(len(cloth_bone_name_lists)):

                    cloth_bone_name_list = cloth_bone_name_lists[i]
                    root_bone_name = cloth_bone_name_list[0]
                    for bone_name in cloth_bone_name_list:

                        is_hit_exclude = False
                        for exclude_sp_joint_prefix_name in exclude_sp_joint_prefix_name_list:
                            if bone_name.startswith(exclude_sp_joint_prefix_name):
                                is_hit_exclude = True
                                break

                        if is_hit_exclude:
                            continue

                        if bone_name not in bone_short_name_list:
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name

                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:

                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内で設定されている骨名がシーン内に存在しません'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def cheke_empty_bone_names(self, is_query=False, args=[]):
        """
        boneNameが空ではないかチェック
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        check_answer_info = cai.CheckAnswerInfo()

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                cloth_bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                for cloth_bone_name_list in cloth_bone_name_lists:
                    for bone_name in cloth_bone_name_list:
                        if not bone_name:
                            invalid_object_name_list.append(cloth_prefab_short_name)
                            break

                    if invalid_object_name_list:
                        break

            if invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内でboneNameが設定されていない項目があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_cloth_data_in_name(self, is_query=False, args=[]):
        """
        シーン内のSp_骨がcloth設定されているか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        # 対象外のSp骨
        exclude_sp_joint_prefix_name_list = ['Sp_Ch_Bust']

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = self.get_bone_list()

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                cloth_bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)

                all_cloth_bone_list = []
                for cloth_bone_name_list in cloth_bone_name_lists:
                    all_cloth_bone_list += cloth_bone_name_list

                for bone_name in check_answer_info.check_target_item_list:

                    bone_short_name = bone_name.split('|')[-1]

                    if not bone_short_name.startswith('Sp_'):
                        continue

                    is_hit_exclude = False
                    for exclude_sp_joint_prefix_name in exclude_sp_joint_prefix_name_list:
                        if bone_short_name.startswith(exclude_sp_joint_prefix_name):
                            is_hit_exclude = True
                            break

                    if is_hit_exclude:
                        continue

                    # 末端骨は検索から除外する
                    bone_child_list = cmds.listRelatives(bone_name, ad=True, type='transform')
                    if not bone_child_list:
                        continue
                    if bone_short_name not in all_cloth_bone_list:
                        invalid_object_name_list.append('{} -> {}'.format(cloth_prefab_short_name, bone_short_name))

            if not check_answer_info.result:

                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'シーン内のSp_でcloth設定されていないものがあります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_stiffness_value(self, is_query=False, args=[]):
        """
        stiffnessが0.001～2の範囲内か
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                cloth_stiffness_value_lists = cloth_collision_info.get_target_value_list('_stiffnessForce', 'cloth', True)
                for i in range(len(cloth_stiffness_value_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    cloth_stiffness_value_list = cloth_stiffness_value_lists[i]
                    for j in range(len(cloth_stiffness_value_list)):
                        cloth_stiffness_value = cloth_stiffness_value_list[j]
                        bone_name = bone_name_list[j]
                        if not (0.001 <= cloth_stiffness_value <= 2.0):
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:

                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内でstiffnessの数値が0.001～2.0の間に収まっていない箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_dragforce_value(self, is_query=False, args=[]):
        """
        drag forceが0.1～1.0の範囲内か
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                cloth_dragforce_value_lists = cloth_collision_info.get_target_value_list('_dragForce', 'cloth', True)
                for i in range(len(cloth_dragforce_value_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    cloth_dragforce_value_list = cloth_dragforce_value_lists[i]
                    for j in range(len(cloth_dragforce_value_list)):
                        cloth_dragforce_value = cloth_dragforce_value_list[j]
                        bone_name = bone_name_list[j]
                        if not (0.1 <= cloth_dragforce_value <= 1.0):
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:

                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内でdrag forceが0.1～1.0の範囲内に収まっていない箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_childElements_size(self, is_query=False, args=[]):
        """
        ChildElementsのsizeが10以下か
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_list = cloth_collision_info.get_target_value_list('_boneName', 'cloth')
                cloth_childElements_value_list = cloth_collision_info.get_target_value_list('_childElements', 'cloth')
                if bone_name_list and cloth_childElements_value_list and (len(bone_name_list) == len(cloth_childElements_value_list)):
                    for i in range(len(cloth_childElements_value_list)):
                        bone_name = bone_name_list[i]
                        cloth_childElements_value = cloth_childElements_value_list[i]
                        if len(cloth_childElements_value) > 10:
                            invalid_object_name_list.append('{} -> {}'.format(cloth_prefab_short_name, bone_name))

            if not check_answer_info.result:

                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内でChildElementsのsizeが10以下に収まっていない箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_collision_name_list_size(self, is_query=False, args=[]):
        """
        Collision Name Listのsizeが5以下か
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                cloth_col_name_set_lists = cloth_collision_info.get_target_value_list('_collisionNameList', 'cloth', True)
                for i in range(len(cloth_col_name_set_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    cloth_col_name_set_list = cloth_col_name_set_lists[i]
                    for j in range(len(cloth_col_name_set_list)):
                        cloth_col_name_set = cloth_col_name_set_list[j]
                        bone_name = bone_name_list[j]
                        if len(cloth_col_name_set) > 5:
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:

                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )
                return check_answer_info

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内でCollision Name Listのsizeが5以下に収まっていない箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_duplicate_collision_name_list_value(self, is_query=False, args=[]):
        """
        Collision Name Listの内でコリジョン名が重複していないか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                cloth_col_name_set_lists = cloth_collision_info.get_target_value_list('_collisionNameList', 'cloth', True)

                for i in range(len(cloth_col_name_set_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    cloth_col_name_set_list = cloth_col_name_set_lists[i]
                    for j in range(len(cloth_col_name_set_list)):
                        cloth_col_name_set = cloth_col_name_set_list[j]
                        bone_name = bone_name_list[j]
                        cloth_col_name_set_len = len(cloth_col_name_set)
                        without_duplicate_cloth_col_name_set_len = len(list(set(cloth_col_name_set)))
                        if cloth_col_name_set_len != without_duplicate_cloth_col_name_set_len:
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内のCollision Name Listでコリジョン名が重複している箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_duplicate_bone_name(self, is_query=False, args=[]):
        """
        クロスの骨名が全て 'Sp_ 'からスタートしているか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                checked_name_list = []

                for bone_name_list in bone_name_lists:
                    root_bone_name = bone_name_list[0]
                    for bone_name in bone_name_list:

                        if bone_name in checked_name_list:
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

                        checked_name_list.append(bone_name)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:
                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内で骨名が重複している箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_bone_name_prefix(self, is_query=False, args=[]):
        """
        クロスの骨名が全て 'Sp_ 'からスタートしているか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                for bone_name_list in bone_name_lists:
                    root_bone_name = bone_name_list[0]
                    for bone_name in bone_name_list:
                        if not bone_name.startswith('Sp_'):
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:
                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内で骨名がSp_からスタートしていない箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_collision_name_prefix(self, is_query=False, args=[]):
        """
        MEMO: コリジョン側
        コリジョン名の接頭語が「Col_」かどうか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'collision')

            for cloth_col_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                file_exists = False
                for file_path in cloth_col_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_col_info.collision_info:
                    continue

                if not cloth_col_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                collision_name_list = cloth_col_info.get_target_value_list('_collisionName', 'col')
                for collision_name in collision_name_list:
                    if not collision_name.startswith('Col'):
                        invalid_object_name_list.append('{} -> {}'.format(cloth_prefab_short_name, collision_name))

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '_collision.assetが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '_collision.asset内のコリジョン名の接頭語が「Col」ではない箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_all_collision_size(self, is_query=False, args=[]):
        """
        MEMO: コリジョン側
        コリジョンのsize（全体の個数）が100以内か
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'collision')

            for cloth_col_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                file_exists = False
                for file_path in cloth_col_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_col_info.collision_info:
                    continue

                if not cloth_col_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                collision_name_list = cloth_col_info.get_target_value_list('_collisionName', 'col')
                if len(collision_name_list) > 100:
                    invalid_object_name_list.append(cloth_prefab_short_name)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '_collision.assetが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '_collision.asset内のコリジョンのsize（全体の個数）が100以内ではありません'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_target_object_name_prefix(self, is_query=False, args=[]):
        """
        コリジョン内のTargetObjectNameが「md_body/Position/」からスタートしているか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'collision')

            for cloth_col_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                file_exists = False
                for file_path in cloth_col_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_col_info.collision_info:
                    continue

                if not cloth_col_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                collision_name_list = cloth_col_info.get_target_value_list('_collisionName', 'col')
                target_object_name_list = cloth_col_info.get_target_value_list('_targetObjectName', 'col')

                for i in range(len(target_object_name_list)):

                    collision_name = collision_name_list[i]
                    target_object_name = target_object_name_list[i]
                    if target_object_name.startswith('md_bdy/Position/'):
                        continue

                    # NeckとHeadは検出対象外なので除外
                    for ignore_target_suffix in ['Neck', 'Head']:
                        if target_object_name.endswith(ignore_target_suffix):
                            break
                    else:
                        invalid_object_name_list.append('{} -> {}'.format(cloth_prefab_short_name, collision_name))

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '_collision.assetが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '_collision.asset内のTargetObjectNameが「md_body/Position/」から始まっていません'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_collision_name_list_size_over_one(self, is_query=False, args=[]):
        """
        collisionNameListのサイズが1以上でなおかつ空でないか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                cloth_col_name_set_lists = cloth_collision_info.get_target_value_list('_collisionNameList', 'cloth', True)

                for i in range(len(bone_name_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    cloth_col_name_set_list = cloth_col_name_set_lists[i]

                    tmp_cloth_col_name_set_list = []
                    for cloth_col_name_set in cloth_col_name_set_list:
                        tmp_cloth_col_name_set = cloth_col_name_set[:]
                        tmp_cloth_col_name_set_list.extend(tmp_cloth_col_name_set)

                    for j in range(len(cloth_col_name_set_list)):
                        bone_name = bone_name_list[j]
                        cloth_col_name_set = cloth_col_name_set_list[j]

                        if len(cloth_col_name_set) == 0:
                            continue

                        for cloth_col_name in cloth_col_name_set:
                            if cloth_col_name:
                                break
                        else:
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if root_bone_name != bone_name:
                                error_obj_str = '{0} >> {1}'.format(error_obj_str, bone_name)
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:
                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'サイズが0か、中身が空のcollisionNameListが存在します'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_offset2_xyz_value_is_zero(self, is_query=False, args=[]):
        """
        MEMO: コリジョン側
        Offset 2のxyzの数値が全て0であるか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'collision')

            for cloth_col_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                file_exists = False
                for file_path in cloth_col_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_col_info.collision_info:
                    continue

                if not cloth_col_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                collision_name_list = cloth_col_info.get_target_value_list('_collisionName', 'col')
                type_value_list = cloth_col_info.get_target_value_list('_type', 'col')
                offset2_item_list = cloth_col_info.get_target_value_list('_offset2', 'col')

                if collision_name_list and type_value_list and offset2_item_list:

                    for i in range(len(type_value_list)):
                        type_value = type_value_list[i]
                        offset2_item = offset2_item_list[i]
                        collision_name = collision_name_list[i]

                        if type_value == 2:
                            continue

                        for offset2_value in list(offset2_item.values()):
                            if offset2_value != 0:
                                invalid_object_name_list.append('{} -> {}'.append(cloth_prefab_short_name, collision_name))
                                break

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内のOffset 2のxyzの数値に0以外の数値が入っています'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_cloth_clild_collision_exists(self, is_query=False, args=[]):
        """
        CollisionNameListのコリジョンが存在しているか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'both')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                file_exists = False
                for file_path in cloth_collision_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_collision_info.collision_info:
                    continue

                if not cloth_collision_info.cloth_info or not cloth_collision_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                cloth_col_name_set_lists = cloth_collision_info.get_target_value_list('_collisionNameList', 'cloth', True)
                col_name_list = cloth_collision_info.get_target_value_list('_collisionName', 'col')

                for i in range(len(bone_name_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    cloth_col_name_set_list = cloth_col_name_set_lists[i]
                    for j in range(len(cloth_col_name_set_list)):
                        bone_name = bone_name_list[j]
                        cloth_col_name_set = cloth_col_name_set_list[j]
                        if not cloth_col_name_set:
                            continue
                        for cloth_col_name in cloth_col_name_set:
                            for col_name in col_name_list:
                                if cloth_col_name == col_name:
                                    break
                            else:
                                error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                                if bone_name != root_bone_name:
                                    error_obj_str += ' >> ' + bone_name
                                invalid_object_name_list.append(error_obj_str)
                                break

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内のCollisionNameListのコリジョンに、\n存在していないcollisionが設定されている項目があります。\n以下は検出されたコリジョンの親骨のリストです'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def detection_gravity_value(self, is_query=False, args=[[], True, 0, True]):
        """
        gravityが0の場合は検出
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: [0]:boneフィルタstrリスト, [1]:フィルタされたboneをスキップするか, [2]:チェック値, [3]:チェック値をエラーにするか
        """

        target_bone_filter_list = args[0]
        uses_filter_for_skip = args[1]
        check_value = args[2]
        is_error_at_check_value = args[3]

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                gravity_dict_list = self.__get_gravity_dict_list(cloth_collision_info)

                for gravity_dict in gravity_dict_list:

                    # boneのフィルタリング
                    should_skip = False

                    if uses_filter_for_skip:

                        for skip_bone_filter_str in target_bone_filter_list:
                            if gravity_dict['bone'].find(skip_bone_filter_str) >= 0:
                                should_skip = True
                                break

                    else:

                        should_skip = True
                        for skip_bone_filter_str in target_bone_filter_list:
                            if gravity_dict['bone'].find(skip_bone_filter_str) >= 0:
                                should_skip = False
                                break

                    if should_skip:
                        continue

                    # エラー判定
                    is_error = False

                    if is_error_at_check_value and gravity_dict['gravity'] == check_value:
                        is_error = True
                    elif not is_error_at_check_value and not gravity_dict['gravity'] == check_value:
                        is_error = True

                    if is_error:
                        error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, gravity_dict['root_bone'])
                        if gravity_dict['bone'] != gravity_dict['root_bone']:
                            error_obj_str += ' >> ' + gravity_dict['bone']
                        invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内でgravityが0で設定されている項目があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def __get_gravity_dict_list(self, cloth_collision_info):
        """
            :return {'gravity': value, 'bone': bone_name, 'root_bone': root_bone_name}のリスト
        """

        if not cloth_collision_info:
            return []

        result_dict_list = []

        bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
        gravity_value_lists = cloth_collision_info.get_target_value_list('_gravity', 'cloth', True)

        for bone_name_list, gravity_value_list in zip(bone_name_lists, gravity_value_lists):

            root_bone_name = bone_name_list[0]

            for bone_name, gravity_value in zip(bone_name_list, gravity_value_list):

                result_dict_list.append(
                    {'gravity': gravity_value, 'bone': bone_name, 'root_bone': root_bone_name}
                )

        return result_dict_list

    # ------------------------------------------------------------

    def detection_Spring_force_value(self, is_query=False, args=[]):
        """
        SpringForceが0以外の場合は検出
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                spring_force_value_lists = cloth_collision_info.get_target_value_list('_springForce', 'cloth', True)

                for i in range(len(spring_force_value_lists)):

                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    spring_force_value_list = spring_force_value_lists[i]
                    for j in range(len(spring_force_value_list)):

                        spring_force_value = spring_force_value_list[j]
                        bone_name = bone_name_list[j]
                        for key, value in list(spring_force_value.items()):
                            if value != 0:
                                error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                                if bone_name != root_bone_name:
                                    error_obj_str += ' >> ' + bone_name
                                invalid_object_name_list.append(error_obj_str)
                                break

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefab内でSpringForceが0以外で設定されている項目があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def detection_cloth_collision_type(self, is_query=False, args=[]):
        """
        CollisionNameListのコリジョンが全てCapsuleタイプなら検出
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            setting_collision_obj = True
            unsetting_collision_obj_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'both')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                file_exists = False
                for file_path in cloth_collision_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_collision_info.collision_info:
                    continue

                if not cloth_collision_info.cloth_info or not cloth_collision_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                cloth_col_name_set_lists = cloth_collision_info.get_target_value_list('_collisionNameList', 'cloth', True)
                col_name_list = cloth_collision_info.get_target_value_list('_collisionName', 'col')
                col_type_list = cloth_collision_info.get_target_value_list('_type', 'col')

                if len(col_name_list) != len(col_type_list):

                    setting_collision_obj = False
                    unsetting_collision_obj_list.append(cloth_prefab_short_name)
                    continue

                else:

                    for i in range(len(bone_name_lists)):

                        bone_name_list = bone_name_lists[i]
                        root_bone_name = bone_name_list[0]
                        cloth_col_name_set_list = cloth_col_name_set_lists[i]
                        for j in range(len(cloth_col_name_set_list)):

                            cloth_col_name_set = cloth_col_name_set_list[j]
                            bone_name = bone_name_list[j]

                            # _collisionNameListの項目数が3つ以下の時はチェックしない
                            if len(cloth_col_name_set) <= 3:
                                continue

                            for cloth_col_name in cloth_col_name_set:

                                for j in range(len(col_name_list)):
                                    col_name = col_name_list[j]
                                    col_type = col_type_list[j]

                                    if cloth_col_name != col_name:
                                        continue
                                    if col_type == self.COL_TYPE_CAPSULE:
                                        # breakすることでelseを踏まなくなる(=カプセルタイプだという証明)
                                        break
                                else:
                                    # 何も一致しないか、カプセルタイプではなかった場合
                                    # breakすることによって次のelseが合致しなくなる
                                    break
                            else:
                                # 全てカプセルタイプだった場合(breakに引っかからなかった場合)
                                # 便宜的にclothの_boneNameを入れる
                                error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                                if bone_name != root_bone_name:
                                    error_obj_str += ' >> ' + bone_name
                                invalid_object_name_list.append(error_obj_str)
                                break

            if not check_answer_info.result:

                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif not setting_collision_obj:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = unsetting_collision_obj_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'CollisionTypeが未設定のコリジョンオブジェクトが存在します'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'CollisionNameListのコリジョンが全てCapsuleタイプな項目があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def detection_capability_not_none(self, is_query=False, args=[]):
        """
        CapabilityがNone以外の場合は検出
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                capability_value_lists = cloth_collision_info.get_target_value_list('_capability', 'cloth', True)

                for i in range(len(capability_value_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    capability_value_list = capability_value_lists[i]
                    for j in range(len(capability_value_list)):
                        capability_value = capability_value_list[j]
                        bone_name = bone_name_list[j]
                        if capability_value != self.CAPABILITY_NONE:
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:
                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'CapabilityがNone以外の項目があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def detection_caps_group_index_is_zero(self, is_query=False, args=[]):
        """
        Caps Group Indexが0以外の場合は検出
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'cloth')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                bone_name_lists = cloth_collision_info.get_target_value_list('_boneName', 'cloth', True)
                caps_group_index_lists = cloth_collision_info.get_target_value_list('_capsGroupIndex', 'cloth', True)

                for i in range(len(caps_group_index_lists)):
                    bone_name_list = bone_name_lists[i]
                    root_bone_name = bone_name_list[0]
                    caps_group_index_list = caps_group_index_lists[i]
                    for j in range(len(caps_group_index_list)):
                        bone_name = bone_name_list[j]
                        caps_group_index = caps_group_index_list[j]
                        if caps_group_index != 0:
                            error_obj_str = '{} -> {}'.format(cloth_prefab_short_name, root_bone_name)
                            if bone_name != root_bone_name:
                                error_obj_str += ' >> ' + bone_name
                            invalid_object_name_list.append(error_obj_str)

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:
                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の検出項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'Caps Group Indexが0以外の項目があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_target_object_name_into_sp(self, is_query=False, args=[]):
        """
        MEMO: コリジョン側
        _targetObjectNameにSp骨が指定されていないか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        self.chara_info = self.root.chara_info

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'collision')

            for cloth_col_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                file_exists = False
                for file_path in cloth_col_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_col_info.collision_info:
                    continue

                if not cloth_col_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                collision_name_list = cloth_col_info.get_target_value_list('_collisionName', 'col')
                collision_target_name_list = cloth_col_info.get_target_value_list('_targetObjectName', 'col')
                pattern = re.compile(r'Sp_')
                for i in range(len(collision_target_name_list)):
                    collision_name = collision_name_list[i]
                    collision_target_name = collision_target_name_list[i]
                    if pattern.search(collision_target_name):
                        invalid_object_name_list.append('{} -> {}'.format(cloth_prefab_short_name, collision_name))

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:

                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '_targetObjectNameにSp骨が指定されている箇所があります'
                    )

        return check_answer_info

    # ------------------------------------------------------------

    def check_unassigned_collision(self, is_query=False, args=[]):
        """
        未使用コリジョンが存在しているか
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        # チェック対象
        check_answer_info.check_target_item_list.append('=' * 20 + '以下のファイルのコリジョンがチェック対象')
        tmp_cloth_prefab_path_list = self.get_cloth_prefab_path_list()

        cloth_prefab_path_list = []
        for cloth_prefab_path in tmp_cloth_prefab_path_list:
            if os.path.exists(cloth_prefab_path):
                cloth_prefab_path_list.append(cloth_prefab_path)
        check_answer_info.check_target_item_list.extend(cloth_prefab_path_list)

        # 全パーツのprefabが検索対象
        tmp_all_parts_cloth_prefab_path_list = []
        tmp_all_parts_cloth_prefab_path_list.extend(self.get_cloth_prefab_path_list('head'))
        tmp_all_parts_cloth_prefab_path_list.extend(self.get_cloth_prefab_path_list('body'))
        tmp_all_parts_cloth_prefab_path_list.extend(self.get_cloth_prefab_path_list('tail'))
        tmp_all_parts_cloth_prefab_path_list.extend(self.get_cloth_prefab_path_list('attach'))

        all_parts_cloth_prefab_path_list = []
        for part_cloth_prefab_path in tmp_all_parts_cloth_prefab_path_list:
            if os.path.exists(part_cloth_prefab_path):
                all_parts_cloth_prefab_path_list.append(part_cloth_prefab_path)

        check_answer_info.check_target_item_list.append('=' * 20 + '以下のファイルで使用されているか検索')
        check_answer_info.check_target_item_list.extend(all_parts_cloth_prefab_path_list)

        if not is_query:

            invalid_object_name_list = []

            cloth_collision_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'collision')

            for cloth_collision_info in cloth_collision_info_list:

                file_name_list = []
                for file_path in cloth_collision_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)
                cloth_prefab_scene_type_match = re.search(r'_cloth[0-9]{2}.prefab$', cloth_prefab_short_name)

                file_exists = False
                for file_path in cloth_collision_info.file_path_list:
                    if os.path.exists(file_path):
                        file_exists = True
                        break

                # Clothファイルは存在するがCollisionが存在しなかったとき
                if file_exists and not cloth_collision_info.collision_info:
                    continue

                if not cloth_collision_info.collision_info or not cloth_prefab_scene_type_match:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

                cloth_prefab_scene_type = cloth_prefab_scene_type_match.group(0)

                # clothにアサインされているコリジョンを全パーツの同じシーン用のclothからリスト
                assigned_collision_list = []

                all_parts_cloth_col_info_list = self.get_cloth_collision_info_list(all_parts_cloth_prefab_path_list, 'cloth')

                for this_cloth_collision_info in all_parts_cloth_col_info_list:

                    if not this_cloth_collision_info.cloth_info:
                        continue

                    if not this_cloth_collision_info.file_path_list[0].endswith(cloth_prefab_scene_type):
                        continue

                    this_cloth_col_name_set_lists = this_cloth_collision_info.get_target_value_list('_collisionNameList', 'cloth', True)

                    for cloth_col_name_set_list in this_cloth_col_name_set_lists:

                        col_list_in_this_list = []

                        for cloth_col_name_set in cloth_col_name_set_list:
                            col_list_in_this_list.extend(cloth_col_name_set)

                        assigned_collision_list.extend(col_list_in_this_list)

                assigned_collision_list = list(set(assigned_collision_list))

                # 今開いているシーンのコリジョンのリスト
                collision_list = cloth_collision_info.get_target_value_list('_collisionName', 'col')

                # リスト同士をつき合わせる
                for collision_name in collision_list:
                    if collision_name not in assigned_collision_list:
                        invalid_object_name_list.append('{} -> {}'.format(cloth_prefab_short_name, collision_name))

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:
                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '使用されていないコリジョンがあります'
                    )

        return check_answer_info

    # ------------------------------------------------------------
    # 追加用テンプレート
    # ------------------------------------------------------------

    def checker_command_template(self, is_query=False, args=[]):
        """
        チェッカーコマンドのテンプレート
            :param is_query=False: チェック項目を参照するかどうか
            :param args=[]: 引数
        """

        check_answer_info = cai.CheckAnswerInfo()
        check_answer_info.check_target_item_list = []

        if not is_query:

            invalid_object_name_list = []

            cloth_prefab_path_list = self.get_cloth_prefab_path_list()
            cloth_col_info_list = self.get_cloth_collision_info_list(cloth_prefab_path_list, 'both')

            for cloth_collision_info in cloth_col_info_list:

                file_name_list = []
                for file_path in cloth_col_info.file_path_list:
                    file_name_list.append(file_path.split('/')[-1])
                cloth_prefab_short_name = ','.join(file_name_list)

                if not cloth_collision_info.cloth_info or not cloth_collision_info.collision_info:

                    check_answer_info.result = False
                    check_answer_info.invalid_item_list.append(cloth_prefab_short_name)

                if not check_answer_info.result:
                    continue

            if not check_answer_info.result:
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        'cloth.prefabが見つかりません'
                    )

            elif invalid_object_name_list:
                check_answer_info.result = False
                check_answer_info.invalid_item_list = invalid_object_name_list
                check_answer_info.error_message = \
                    '{0}個の不正な項目があります。\n{1}'.format(
                        str(len(check_answer_info.invalid_item_list)),
                        '何が不正かどうかの文言を書きます'
                    )

        return check_answer_info
