# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import re

from ..base_common import utility as base_utility

from . import data_structs as data_structs

import maya.cmds as cmds

reload(data_structs)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SymmetricalPairManager(object):

    # ===============================================
    def __init__(self):

        self.target_transform = ''
        self.symmetrical_axis = ''
        self.symmetrical_str_list = ['_L', '_R']
        self.joint_search_type = 'pos'
        self.pos_torlerance = None
        self.weight_tolerance = 0.00099999   # base_utility.value.is_sameに合わせた
        self.vtx_data_list = None
        self.joint_data_list = None
        self.symmetrical_pair_item_list = None
        self.is_ready = None

    # ===============================================
    def initialize(
        self,
        target_transform,
        symmetrical_axis,
        joint_search_type,
        symmetrical_str_list,
        pos_torlerance,
    ):

        self.is_ready = False

        if not cmds.objExists(target_transform):
            return

        self.target_transform = target_transform
        self.symmetrical_axis = symmetrical_axis
        self.joint_search_type = joint_search_type
        self.symmetrical_str_list = symmetrical_str_list
        self.pos_torlerance = pos_torlerance
        self.vtx_data_list = []
        self.joint_data_list = []
        self.symmetrical_pair_item_list = []

        self.is_ready = True

    # ===============================================
    def create_info(self):

        if not self.is_ready:
            print('manager: initialize failure')
            return

        self.vtx_data_list = []
        self.joint_data_list = []
        self.symmetrical_pair_item_list = []

        self.vtx_data_list = self.__get_vtx_data_list(self.target_transform)
        self.joint_data_list = self.__get_joint_data_list(self.target_transform)

        self.__create_symmetrical_item_list()

    # ===============================================
    def __get_vtx_data_list(self, target_transform):

        vtx_data_list = []

        all_vtx_list = cmds.polyListComponentConversion(self.target_transform, tv=True)
        all_vtx_list = cmds.ls(all_vtx_list, l=True, fl=True)
        all_joint_weight_info_list = base_utility.mesh.skin.get_all_joint_weight_info_list(self.target_transform)

        for vtx in all_vtx_list:
            this_data = data_structs.VtxData()
            this_data.create_data(vtx, all_joint_weight_info_list)
            if this_data.is_ready:
                vtx_data_list.append(this_data)

        return vtx_data_list

    # ===============================================
    def __get_joint_data_list(self, target_transform):

        joint_data_list = []

        skin_joint_list = base_utility.mesh.skin.get_skin_joint_list(self.target_transform)

        if not skin_joint_list:
            return joint_data_list

        for joint in skin_joint_list:
            this_data = data_structs.JointData()
            this_data.create_data(joint)
            if this_data.is_ready:
                joint_data_list.append(this_data)

        return joint_data_list

    # ===============================================
    def __create_symmetrical_item_list(self):

        if not self.vtx_data_list:
            return

        used_index_list = []

        for i, vtx_data in enumerate(self.vtx_data_list):

            if i in used_index_list:
                continue
            else:
                used_index_list.append(i)

            symmetry_index, this_pair_item = self.__create_symmetrical_item(i, vtx_data)
            if symmetry_index >= 0:
                used_index_list.append(symmetry_index)

            self.symmetrical_pair_item_list.append(this_pair_item)

    # ===============================================
    def __create_symmetrical_item(self, index, vtx_data):

        symmetry_index = self.find_symmetrical_object(vtx_data, self.vtx_data_list, 'pos', True)
        symmetry_data = None

        if symmetry_index >= 0:
            symmetry_data = self.vtx_data_list[symmetry_index]

        symmetric_pos_index = 0
        if self.symmetrical_axis == 'y':
            symmetric_pos_index = 1
        elif self.symmetrical_axis == 'z':
            symmetric_pos_index = 2

        positive_data = None
        nagative_data = None

        if vtx_data.pos[symmetric_pos_index] >= 0:
            positive_data = vtx_data
            nagative_data = symmetry_data
        else:
            positive_data = symmetry_data
            nagative_data = vtx_data

        this_pair_item = SymmetricalPairItem()
        this_pair_item.create_info(
            index, positive_data, nagative_data, self, self.weight_tolerance)

        return symmetry_index, this_pair_item

    # ===============================================
    def get_filtered_item_list(self, filter_list):

        if not filter_list:
            return

        if not self.symmetrical_pair_item_list:
            return

        result_item_list = []
        for item in self.symmetrical_pair_item_list:
            if 'no_pair' in filter_list:
                if not item.has_pair:
                    result_item_list.append(item)
                    continue

            if 'normal_pair' in filter_list:
                if item.check_result and item.has_pair:
                    result_item_list.append(item)
                    continue

            if 'inf_error' in filter_list:
                if not item.is_symmetrical_inf and item.has_pair:
                    result_item_list.append(item)
                    continue

            if 'weight_error' in filter_list:
                if not item.is_symmetrical_weight and item.has_pair:
                    result_item_list.append(item)
                    continue

        return result_item_list

    # ===============================================
    def find_symmetrical_object(self, src_data, target_data_list, search_type, should_return_index):

        result = None

        if search_type == 'pos':
            result = self.__find_symmetrical_object_by_pos(src_data, target_data_list)
        elif search_type == 'name':
            result = self.__find_symmetrical_object_by_name(src_data, target_data_list)

        if not result:
            if should_return_index:
                result = -1
            return result

        if should_return_index:
            return result[0]
        else:
            return result[1]

    # ===============================================
    def __find_symmetrical_object_by_name(self, src_data, target_data_list):

        if not self.is_ready:
            return

        if not cmds.objExists(src_data.name):
            return

        hit_list = []
        replace_str = '####'
        replace_src_name = src_data.name
        for target_str in self.symmetrical_str_list:
            replace_src_name = replace_src_name.replace(target_str, replace_str)

        for i, data in enumerate(target_data_list):

            this_name = data.name

            for target_str in self.symmetrical_str_list:
                this_name = this_name.replace(target_str, replace_str)

            if this_name == replace_src_name:
                hit_list.append([i, data])

        # hitなし
        if len(hit_list) == 0:
            return

        # 1つhit = 対称がなくて、srcがhit
        elif len(hit_list) == 1:
            return hit_list[0]

        # 2つhit = srcと対称がhit。srcでない方を返す
        else:
            for this_hit in hit_list:
                if this_hit[1].name == src_data.name:
                    continue
                return this_hit

    # ===============================================
    def __find_symmetrical_object_by_pos(self, src_data, target_data_list):

        if not self.is_ready:
            return

        if not cmds.objExists(src_data.name):
            return

        src_pos = src_data.pos[:]
        symmetry_pos = src_pos

        if self.symmetrical_axis == 'y':
            symmetry_pos[1] = symmetry_pos[1] * -1
        elif self.symmetrical_axis == 'z':
            symmetry_pos[2] = symmetry_pos[2] * -1
        else:
            symmetry_pos[0] = symmetry_pos[0] * -1

        hit_list = []

        for i, data in enumerate(target_data_list):

            if not data.pos:
                continue

            if abs(data.pos[0] - symmetry_pos[0]) > self.pos_torlerance:
                continue
            if abs(data.pos[1] - symmetry_pos[1]) > self.pos_torlerance:
                continue
            if abs(data.pos[2] - symmetry_pos[2]) > self.pos_torlerance:
                continue

            hit_list.append([i, data])

        # hitなし
        if len(hit_list) == 0:
            return

        # 1つhit
        elif len(hit_list) == 1:
            return hit_list[0]

        # 2つ以上対称位置にある場合は名前の近さで判定
        else:
            result = hit_list[0]

            src_short_name = src_data.name.split('|')[-1]
            src_elm_len = len(src_data.name.split('|'))

            for this_hit in hit_list:
                this_short_name = this_hit[1].label
                this_elm_len = len(this_hit[1].name.split('|'))

                if not this_elm_len == src_elm_len:
                    continue

                if this_short_name == src_short_name:
                    continue

                if src_short_name.split('_')[0] == this_short_name.split('_')[0]:
                    result = this_hit
                    break

            return result

    # ===============================================
    def adjust_weight_all(self, adjust_side):
        self.__adjust_weight(self.symmetrical_pair_item_list, adjust_side)

    # ===============================================
    def adjust_weight_selection(self, adjust_side):
        this_pair_item_list = self.__get_symmetrical_pair_item_list_from_selection()
        self.__adjust_weight(this_pair_item_list, adjust_side, True)

    # ===============================================
    def __adjust_weight(self, symmetrical_pair_item_list, adjust_side, is_single_update=False):

        if not symmetrical_pair_item_list:
            return

        if not self.target_transform:
            return

        apply_joint_weight_info_list = []
        apply_symmetrical_pair_item_list = []

        for symmetrical_pair_item in symmetrical_pair_item_list:

            if symmetrical_pair_item.check_result and symmetrical_pair_item.is_symmetrical_weight:
                continue

            positive_info = [int(symmetrical_pair_item.positive_vtx_data.index), []]
            negative_info = [int(symmetrical_pair_item.negative_vtx_data.index), []]
            apply_positive_joint_weight_list = []
            apply_negative_joint_weight_list = []

            for influence_pair_item in symmetrical_pair_item.influence_pair_item_list:

                target_joint_data = None

                if adjust_side == 'positive':

                    if influence_pair_item.is_symmetrical_inf:
                        target_joint_data = influence_pair_item.negative_joint_data

                    elif influence_pair_item.positive_joint_data:
                        symmetrical_joint_data = self.find_symmetrical_object(
                            influence_pair_item.positive_joint_data,
                            self.joint_data_list,
                            'name',
                            False
                        )

                        if symmetrical_joint_data:
                            target_joint_data = symmetrical_joint_data
                        else:
                            target_joint_data = influence_pair_item.positive_joint_data

                    if target_joint_data:
                        negative_info[1].append([
                            target_joint_data.name,
                            influence_pair_item.positive_weight
                        ])
                        apply_negative_joint_weight_list.append([
                            target_joint_data,
                            influence_pair_item.positive_weight
                        ])

                elif adjust_side == 'negative':

                    if influence_pair_item.is_symmetrical_inf:
                        target_joint_data = influence_pair_item.positive_joint_data

                    elif influence_pair_item.negative_joint_data:
                        symmetrical_joint_data = self.find_symmetrical_object(
                            influence_pair_item.negative_joint_data,
                            self.joint_data_list,
                            'name',
                            False
                        )

                        if symmetrical_joint_data:
                            target_joint_data = symmetrical_joint_data
                        else:
                            target_joint_data = influence_pair_item.negative_joint_data

                    if target_joint_data:
                        positive_info[1].append([
                            target_joint_data.name,
                            influence_pair_item.negative_weight
                        ])
                        apply_positive_joint_weight_list.append([
                            target_joint_data,
                            influence_pair_item.negative_weight
                        ])

            if positive_info[1]:
                apply_joint_weight_info_list.append(positive_info)

            if negative_info[1]:
                apply_joint_weight_info_list.append(negative_info)

            if is_single_update:

                if apply_positive_joint_weight_list:
                    # VtxDataのjoint_weight_list更新
                    vtx_data = self.vtx_data_list[positive_info[0]]
                    vtx_data.joint_weight_list = apply_positive_joint_weight_list
                    self.vtx_data_list[positive_info[0]] = vtx_data

                if apply_negative_joint_weight_list:
                    # VtxDataのjoint_weight_list更新
                    vtx_data = self.vtx_data_list[negative_info[0]]
                    vtx_data.joint_weight_list = apply_negative_joint_weight_list
                    self.vtx_data_list[negative_info[0]] = vtx_data

            if positive_info[1] or negative_info[1]:
                apply_symmetrical_pair_item_list.append(symmetrical_pair_item)

        base_utility.mesh.skin.set_joint_weight_info_list(
            self.target_transform, apply_joint_weight_info_list)

        if is_single_update:

            # symmetrical_pair_item_listの作り直しによる時間削減処理
            for apply_symmetrical_pair_item in apply_symmetrical_pair_item_list:

                index = apply_symmetrical_pair_item.index

                for i in range(len(self.symmetrical_pair_item_list)):

                    symmetrical_pair_item = self.symmetrical_pair_item_list[i]
                    if index != symmetrical_pair_item.index:
                        continue

                    vtx_data = self.vtx_data_list[index]
                    _, this_pair_item = self.__create_symmetrical_item(index, vtx_data)
                    self.symmetrical_pair_item_list[i] = this_pair_item
                    break

    # ===============================================
    def __get_symmetrical_pair_item_list_from_selection(self):

        result_list = []

        if not self.symmetrical_pair_item_list:
            return result_list

        selection_list = cmds.ls(sl=True, l=True, fl=True)

        if not selection_list:
            return result_list

        selection_vtx_list = []

        for selection in selection_list:
            suffix_match = re.search('\.vtx\[([0-9]+)\]', selection)
            if not suffix_match:
                continue

            selection_vtx_list.append(selection)

        if not selection_vtx_list:
            return result_list

        for symmetrical_pair_item in self.symmetrical_pair_item_list:

            if not symmetrical_pair_item.has_pair:
                continue

            positive_vtx_name = symmetrical_pair_item.positive_vtx_data.name
            negative_vtx_name = symmetrical_pair_item.negative_vtx_data.name

            if positive_vtx_name in selection_vtx_list or negative_vtx_name in selection_vtx_list:
                result_list.append(symmetrical_pair_item)

        return result_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SymmetricalPairItem(object):

    # ===============================================
    def __init__(self):

        self.index = None

        self.positive_vtx_data = None
        self.negative_vtx_data = None
        self.influence_pair_item_list = None

        self.has_pair = None
        self.check_result = None
        self.is_symmetrical_inf = None
        self.is_symmetrical_weight = None
        self.weight_tolerance = 0.0

    # ===============================================
    def create_info(self, index, positive_vtx_data, negative_vtx_data, manager, weight_tolerance=0.0):

        self.index = index

        self.positive_vtx_data = positive_vtx_data
        self.negative_vtx_data = negative_vtx_data
        self.influence_pair_item_list = []

        self.has_pair = False
        self.weight_tolerance = weight_tolerance

        if self.positive_vtx_data and self.negative_vtx_data:
            if self.positive_vtx_data.name == self.negative_vtx_data.name:
                self.negative_vtx_data = None
                self.has_pair = False
            else:
                self.has_pair = True

        joint_weight_pair_list = self.__get_joint_weight_pair_list(manager)

        for joint_weight_pair in joint_weight_pair_list:
            influence_pair_item = InfluencePairItem()
            influence_pair_item.create_info(
                joint_weight_pair, self.weight_tolerance)
            self.influence_pair_item_list.append(influence_pair_item)

        self.__check_item()

    # ===============================================
    def __get_joint_weight_pair_list(self, manager):

        result_list = []

        positive_joint_weight_list = []
        negative_joint_weight_list = []

        if self.positive_vtx_data:
            positive_joint_weight_list = self.positive_vtx_data.joint_weight_list
        if self.negative_vtx_data:
            negative_joint_weight_list = self.negative_vtx_data.joint_weight_list

        base_joint_weight_list = []
        target_joint_weight_list = []
        is_positive_base = True

        if positive_joint_weight_list:
            base_joint_weight_list = positive_joint_weight_list
            target_joint_weight_list = negative_joint_weight_list
        else:
            base_joint_weight_list = negative_joint_weight_list
            target_joint_weight_list = positive_joint_weight_list
            is_positive_base = False

        matched_target_index_list = []

        # base側からチェック
        for base_joint_weight in base_joint_weight_list:

            if not self.has_pair:
                if is_positive_base:
                    result_list.append([base_joint_weight, []])
                else:
                    result_list.append([[], base_joint_weight])
                continue

            base_joint_data = base_joint_weight[0]
            symmetry_joint_data = \
                manager.find_symmetrical_object(
                    base_joint_data,
                    manager.joint_data_list,
                    manager.joint_search_type,
                    False)

            # 対称ジョイントなし
            if not symmetry_joint_data:
                if is_positive_base:
                    result_list.append([base_joint_weight, []])
                else:
                    result_list.append([[], base_joint_weight])
                continue

            # 対称ジョイントがターゲットにあるか
            is_hit = False

            for i, target_joint_weight in enumerate(target_joint_weight_list):

                target_joint_data = target_joint_weight[0]

                # ある
                if target_joint_data.name == symmetry_joint_data.name:

                    if is_positive_base:
                        result_list.append([base_joint_weight, target_joint_weight])
                    else:
                        result_list.append([target_joint_weight, base_joint_weight])
                    matched_target_index_list.append(i)
                    is_hit = True
                    break

            # ない
            if not is_hit:
                if is_positive_base:
                    result_list.append([base_joint_weight, []])
                else:
                    result_list.append([[], base_joint_weight])

        # hitしていないtargetをチェック
        for i, target_joint_weight in enumerate(target_joint_weight_list):

            if i in matched_target_index_list:
                continue

            if is_positive_base:
                result_list.append([[], target_joint_weight])
            else:
                result_list.append([target_joint_weight, []])

        return result_list

    # ===============================================
    def __check_item(self):

        self.check_result = True
        self.is_symmetrical_inf = True
        self.is_symmetrical_weight = True

        if not self.has_pair:
            return

        for influence_pair_item in self.influence_pair_item_list:

            if not influence_pair_item.is_symmetrical_inf:
                self.is_symmetrical_inf = False
                self.check_result = False
                continue

            if not influence_pair_item.is_symmetrical_weight:
                self.is_symmetrical_weight = False
                self.check_result = False

    # ===============================================
    def get_vtx_pair_label_list(self):

        this_nagative_label = ''
        this_positive_label = ''

        if self.negative_vtx_data:
            this_nagative_label = self.negative_vtx_data.label
        if self.positive_vtx_data:
            this_positive_label = self.positive_vtx_data.label

        return [this_positive_label, this_nagative_label]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class InfluencePairItem(object):

    # ===============================================
    def __init__(self):

        self.positive_joint_data = None
        self.negative_joint_data = None
        self.positive_weight = None
        self.negative_weight = None

        self.is_symmetrical_inf = None
        self.is_symmetrical_weight = None
        self.weight_tolerance = 0.0

    # ===============================================
    def create_info(self, joint_weight_pair, weight_tolerance=0.0):

        self.is_symmetrical_inf = False
        self.is_symmetrical_weight = False

        positive_joint_weight = joint_weight_pair[0]
        negative_joint_weight = joint_weight_pair[1]

        self.weight_tolerance = weight_tolerance

        if positive_joint_weight:
            self.positive_joint_data = positive_joint_weight[0]
            self.positive_weight = positive_joint_weight[1]

        if negative_joint_weight:
            self.negative_joint_data = negative_joint_weight[0]
            self.negative_weight = negative_joint_weight[1]

        if self.positive_joint_data and self.negative_joint_data:
            self.is_symmetrical_inf = True
        else:
            return

        # base_utilityからなるべく切り離す(#TDN-5331)
        # if base_utility.value.is_same(self.positive_weight, self.negative_weight):
        if abs(self.positive_weight - self.negative_weight) < self.weight_tolerance:
            self.is_symmetrical_weight = True
