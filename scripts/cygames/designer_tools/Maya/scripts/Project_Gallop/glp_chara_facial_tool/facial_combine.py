# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import os
import csv

import maya.cmds as cmds

from . import target_info


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialCombine(object):

    # ===============================================
    def __init__(self):

        self.facial_info = None

        # face_type_data.csvの情報
        # {'label': face_tyep_name, 'parts': {'eyebrow_l': {label: value, label: value},,,}, 'group': set_face_group}
        self.face_type_info_dict_list = None

        # 個々のパーツのtrsを記録
        self.eyebrow_l_trs_list_dict = None
        self.eyebrow_r_trs_list_dict = None
        self.eye_l_trs_list_dict = None
        self.eye_r_trs_list_dict = None
        self.mouth_trs_list_dict = None

        # スクリプターが指定する表情になるように組み合わせたitemのリスト
        # face_type_info_dict_listを元に作成
        self.face_type_item_list = None

        # ------------------------------
        # 定数

        # face_type_data.csvの定数
        self.face_type_csv_header_index = 0
        self.face_type_csv_data_starts_from = 2
        self.face_type_csv_label_header = 'label'
        self.face_type_csv_eyebrow_l_header = 'eyebrow_l'
        self.face_type_csv_eyebrow_r_header = 'eyebrow_r'
        self.face_type_csv_eye_l_header = 'eye_l'
        self.face_type_csv_eye_r_header = 'eye_r'
        self.face_type_csv_mouth_header = 'mouth'
        self.face_type_csv_set_face_group_header = 'set_face_group'

        # target_infoの対象part名
        self.eyebrow_l_part = 'Eyebrow_L'
        self.eyebrow_r_part = 'Eyebrow_R'
        self.eye_l_part = 'Eye_L'
        self.eye_r_part = 'Eye_R'
        self.mouth_part = 'Mouth'

    # ===============================================
    def initialize_from_csv(self, csv_file_name, controller_csv_file_name, face_type_csv_file_name):
        """
        csvからディクショナリを作る。
        csv_file_name: 例: facial_target_info
        controller_csv_file_name: 例: facial_controller_info
        face_type_csv_file_name: 例: face_type_data
        """
        self.facial_info = target_info.TargetInfo()
        self.facial_info.create_info_from_csv(csv_file_name, controller_csv_file_name)
        self.__set_face_type_info_dict_list(face_type_csv_file_name)
        self.__set_parts_trs_list_dict()
        self.__set_face_type_item_list()

    # ===============================================
    def initialize_only_parts_trs(self, csv_file_name, controller_csv_file_name):

        self.facial_info = target_info.TargetInfo()
        self.facial_info.create_info_from_csv(csv_file_name, controller_csv_file_name)
        self.__set_parts_trs_list_dict()

    # ===============================================
    def apply_blend_face(self, face_type_info_dict_list):

        self.face_type_info_dict_list = face_type_info_dict_list
        self.__set_face_type_item_list()
        self.face_type_item_list[0].apply_facial()

    # ===============================================
    def __set_face_type_info_dict_list(self, face_type_data_csv_name):
        """
        face_type_data.csv から self.face_type_info_dict_list に
        label, group, parts のディクショナリを格納する
        face_type_data_csv_name: face_type_data (face_type_data.csv のこと)
        """
        self.face_type_info_dict_list = []

        # 80_3D/01_character/01_model/head/このキャラのID/scenes の中に
        # face_type_data.csv があればそちらを優先
        target_csv_file_path = \
            self.facial_info.target_dir_path + '/' + face_type_data_csv_name + '.csv'
        # なければツールの glp_chara_facial_tool/resource/face_type_data.csv を読み込み
        if not os.path.isfile(target_csv_file_path):
            target_csv_file_path = \
                self.facial_info.script_dir_path + '/resource/' + \
                face_type_data_csv_name + '.csv'

        if not os.path.isfile(target_csv_file_path):
            cmds.warning("face_type_data.csv が見つかりませんでした")
            return

        # face_type_info_dictの作成
        with open(target_csv_file_path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            # 項目のIndexを確認
            label_col = None
            eyebrow_l_col = None
            eyebrow_r_col = None
            eye_l_col = None
            eye_r_col = None
            mouth_col = None
            set_face_group_col = None
            row = 0
            for column_list in csv_reader:
                # 最初の行
                if row == self.face_type_csv_header_index:
                    for col, label in enumerate(column_list):
                        if label == self.face_type_csv_label_header:
                            label_col = col
                        elif label == self.face_type_csv_eyebrow_l_header:
                            eyebrow_l_col = col
                        elif label == self.face_type_csv_eyebrow_r_header:
                            eyebrow_r_col = col
                        elif label == self.face_type_csv_eye_l_header:
                            eye_l_col = col
                        elif label == self.face_type_csv_eye_r_header:
                            eye_r_col = col
                        elif label == self.face_type_csv_mouth_header:
                            mouth_col = col
                        elif label == self.face_type_csv_set_face_group_header:
                            set_face_group_col = col
                    if label_col is None or not(eyebrow_l_col and
                       eyebrow_r_col and eyebrow_r_col and eye_l_col and
                       eye_r_col and mouth_col and set_face_group_col):
                        cmds.warning("列番号の取得に失敗しました")
                        return
                elif row < self.face_type_csv_data_starts_from:
                    # ２行目(row 1) はデータタイプの行だったりしている(使われていないっぽいけれど)
                    pass
                else:
                    this_face_type_info_dict = {}
                    this_face_type_info_dict['label'] = column_list[label_col]
                    this_face_type_info_dict['group'] = column_list[set_face_group_col]

                    parts_dict = {}
                    parts_dict[self.face_type_csv_eyebrow_l_header] = self.__get_parts_data(column_list[eyebrow_l_col])
                    parts_dict[self.face_type_csv_eyebrow_r_header] = self.__get_parts_data(column_list[eyebrow_r_col])
                    parts_dict[self.face_type_csv_eye_l_header] = self.__get_parts_data(column_list[eye_l_col])
                    parts_dict[self.face_type_csv_eye_r_header] = self.__get_parts_data(column_list[eye_r_col])
                    parts_dict[self.face_type_csv_mouth_header] = self.__get_parts_data(column_list[mouth_col])

                    this_face_type_info_dict['parts'] = parts_dict

                    self.face_type_info_dict_list.append(this_face_type_info_dict)
                row += 1

    # ===============================================
    def __get_parts_data(self, csv_face_type_parts_str):
        """
        csvのカラムをlabelとブレンド値のdictに変換
        csvは (ラベル)__(ブレンド値％)|(ラベル)__(ブレンド値％) の形式
        """

        result_dict = {}
        blend_list = csv_face_type_parts_str.split('|')

        for blend_elm in blend_list:
            if(len(blend_elm.split('__')) > 1):
                this_label = blend_elm.split('__')[0]
                this_blend_ratio = blend_elm.split('__')[1]
                result_dict[this_label] = float(this_blend_ratio) / 100
            else:
                # ブレンド値の記載がない場合は100％
                this_label = blend_elm
                result_dict[this_label] = 1.0

        return result_dict

    # ===============================================
    def __set_parts_trs_list_dict(self):
        """
        各パーツごとの表情を記録したdictを作成
        key:表情ラベル、value:コントローラーのtrsリスト
        """

        self.eyebrow_l_trs_list_dict = {}
        self.eyebrow_r_trs_list_dict = {}
        self.eye_l_trs_list_dict = {}
        self.eye_r_trs_list_dict = {}
        self.mouth_trs_list_dict = {}

        for info_item in self.facial_info.info_item_list:

            # アニメーションレイヤーの判定
            is_anim_layer = False
            if info_item.animation_layer_name:
                if cmds.animLayer(info_item.animation_layer_name, q=True, exists=True):
                    is_anim_layer = True

            # 各コントローラーのラベルとtrsを記録
            for controller_item in self.facial_info.target_controller_info.info_item_list:

                if not controller_item.part == info_item.part:
                    continue

                if not cmds.objExists(controller_item.controller_name):
                    continue

                target_dict = None

                if info_item.part == self.eyebrow_l_part:
                    target_dict = self.eyebrow_l_trs_list_dict
                elif info_item.part == self.eyebrow_r_part:
                    target_dict = self.eyebrow_r_trs_list_dict
                elif info_item.part == self.eye_l_part:
                    target_dict = self.eye_l_trs_list_dict
                elif info_item.part == self.eye_r_part:
                    target_dict = self.eye_r_trs_list_dict
                elif info_item.part == self.mouth_part:
                    target_dict = self.mouth_trs_list_dict

                this_trs = TRSInfo()

                # アニメーションレイヤー適用してtrsを取得
                if is_anim_layer:
                    this_trs.label = info_item.animation_layer_name
                    self.__active_anim_layer(info_item.animation_layer_name)
                else:
                    this_trs.label = info_item.label
                this_trs.create_info_from_target(controller_item.controller_name, info_item.frame)

                # アニメーションレイヤーを切ってからbase初期位置を取得
                if is_anim_layer:
                    self.__reset_anim_layer()
                this_trs.set_base_trs()

                if this_trs.label not in target_dict:
                    target_dict[this_trs.label] = [this_trs]
                else:
                    target_dict[this_trs.label].append(this_trs)

    # ===============================================
    def __set_face_type_item_list(self):

        if not self.face_type_info_dict_list:
            return

        self.face_type_item_list = []

        face_type_index = 0
        group_index_dict = {}

        # スクリプターが指定する表情ごとにFaceTypeItemを作成
        for face_type_info_dict in self.face_type_info_dict_list:

            this_info = FaceTypeItem()

            this_info.label = face_type_info_dict['label']
            this_info.set_face_group_index = int(face_type_info_dict['group'])

            this_info.face_type_index = face_type_index
            face_type_index += 1

            if str(face_type_info_dict['group']) not in group_index_dict:
                group_index_dict[str(face_type_info_dict['group'])] = 0

            this_info.group_index = group_index_dict[str(face_type_info_dict['group'])]
            group_index_dict[str(face_type_info_dict['group'])] += 1

            this_parts_dict = face_type_info_dict['parts']

            # 各パーツごとにtrsをブレント
            for part in this_parts_dict:

                # 検索するパーツ、ラベル、ブレンド値を定義
                this_part = part
                label_list = []
                ratio_list = []

                blend_dict = this_parts_dict[part]

                for blend_label in blend_dict:
                    label_list.append(blend_label)
                    ratio_list.append(blend_dict[blend_label])

                # 検索するdictと追加するlistをパーツから特定
                this_tsr_list_dict = None
                target_trs_list = None

                if this_part == self.face_type_csv_eyebrow_l_header:
                    this_tsr_list_dict = self.eyebrow_l_trs_list_dict
                    target_trs_list = this_info.eyebrow_l_trs_list

                elif this_part == self.face_type_csv_eyebrow_r_header:
                    this_tsr_list_dict = self.eyebrow_r_trs_list_dict
                    target_trs_list = this_info.eyebrow_r_trs_list

                elif this_part == self.face_type_csv_eye_l_header:
                    this_tsr_list_dict = self.eye_l_trs_list_dict
                    target_trs_list = this_info.eye_l_trs_list

                elif this_part == self.face_type_csv_eye_r_header:
                    this_tsr_list_dict = self.eye_r_trs_list_dict
                    target_trs_list = this_info.eye_r_trs_list

                elif this_part == self.face_type_csv_mouth_header:
                    this_tsr_list_dict = self.mouth_trs_list_dict
                    target_trs_list = this_info.mouth_trs_list

                else:
                    continue

                # どのlabelでもリストに格納しているTsrInfoの数=コントローラーの数は同じはず
                controller_len = len(this_tsr_list_dict[label_list[0]])

                for tsr_list_index in range(controller_len):

                    blend_tsr_list = []

                    for label in label_list:
                        blend_tsr_list.append(this_tsr_list_dict[label][tsr_list_index])

                    blended_tsr = TRSInfo.blend_trs(blend_tsr_list, ratio_list)
                    target_trs_list.append(blended_tsr)

            self.face_type_item_list.append(this_info)

    # ===============================================
    def __active_anim_layer(self, anim_layer_name):

        if not self.facial_info or not self.facial_info.info_item_list:
            return

        anim_info_list = []

        for info_item in self.facial_info.info_item_list:
            if info_item.animation_layer_name:
                anim_info_list.append(info_item)

        for anim_info in anim_info_list:

            this_anim_layer_name = anim_info.animation_layer_name

            if not cmds.animLayer(this_anim_layer_name, q=True, exists=True):
                continue

            if this_anim_layer_name == anim_layer_name:
                cmds.animLayer(this_anim_layer_name, edit=True, weight=1.0, mute=False)

    # ===============================================
    def __reset_anim_layer(self):

        if not self.facial_info or not self.facial_info.info_item_list:
            return

        anim_info_list = []

        for info_item in self.facial_info.info_item_list:
            if info_item.animation_layer_name:
                anim_info_list.append(info_item)

        for anim_info in anim_info_list:

            this_anim_layer_name = anim_info.animation_layer_name

            if not cmds.animLayer(this_anim_layer_name, q=True, exists=True):
                continue

            cmds.animLayer(this_anim_layer_name, edit=True, weight=0.0, mute=False)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FaceTypeItem(object):

    # ===============================================
    def __init__(self):

        # スクリプター側の区分
        # 0=全体、1=目のみ、2=口のみ
        self.set_face_group_index = -1

        # スクリプター側の表情ラベル
        self.label = ''

        self.face_type_index = 0
        self.group_index = 0

        self.eyebrow_l_trs_list = []
        self.eyebrow_r_trs_list = []
        self.eye_l_trs_list = []
        self.eye_r_trs_list = []
        self.mouth_trs_list = []

    # ===============================================
    def apply_facial(self):

        apply_trs_list = self.__get_apply_trs_list('all')

        for trs in apply_trs_list:
            trs.apply_trs()

    # ===============================================
    def apply_facial_by_set_face_group(self):

        apply_trs_list = self.__get_apply_trs_list('by_set_face_group')

        for tsr in apply_trs_list:
            tsr.apply_trs()

    # ===============================================
    def __get_apply_trs_list(self, apply_type):

        result_list = []

        if apply_type == 'all':
            result_list = \
                self.eyebrow_l_trs_list +\
                self.eyebrow_r_trs_list +\
                self.eye_l_trs_list +\
                self.eye_r_trs_list +\
                self.mouth_trs_list

        elif apply_type == 'by_set_face_group':

            if self.set_face_group_index == 0:
                result_list = self.__get_apply_trs_list('all')

            elif self.set_face_group_index == 1:
                result_list = self.eye_l_trs_list + self.eye_r_trs_list

            elif self.set_face_group_index == 2:
                result_list = self.mouth_trs_list

        return result_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TRSInfo(object):

    # ===============================================
    def __init__(self):

        self.label = ''
        self.target_name = None

        self.__base_frame = 0
        self.base_t = [0, 0, 0]
        self.base_r = [0, 0, 0]
        self.base_s = [1, 1, 1]

        self.local_t = [0, 0, 0]
        self.local_r = [0, 0, 0]
        self.local_s = [1, 1, 1]

    # ===============================================
    def create_info_from_target(self, target_transform, frame=None):

        if not cmds.objExists(target_transform):
            return

        self.target_name = target_transform

        if frame is None:
            self.local_t = cmds.xform(self.target_name, q=True, t=True)
            self.local_r = cmds.xform(self.target_name, q=True, ro=True)
            self.local_s = cmds.xform(self.target_name, q=True, r=True, s=True)
        else:
            self.local_t = cmds.getAttr(self.target_name + '.t', t=frame)[0]
            self.local_r = cmds.getAttr(self.target_name + '.r', t=frame)[0]
            self.local_s = cmds.getAttr(self.target_name + '.s', t=frame)[0]

    # ===============================================
    def set_base_trs(self):

        if not cmds.objExists(self.target_name):
            return

        self.base_t = cmds.getAttr(self.target_name + '.t', t=self.__base_frame)[0]
        self.base_r = cmds.getAttr(self.target_name + '.r', t=self.__base_frame)[0]
        self.base_s = cmds.getAttr(self.target_name + '.s', t=self.__base_frame)[0]

    # ===============================================
    def apply_trs(self):

        if not cmds.objExists(self.target_name):
            return

        cmds.xform(self.target_name, t=self.local_t)
        cmds.xform(self.target_name, ro=self.local_r)
        cmds.xform(self.target_name, s=self.local_s)

    # ===============================================
    def apply_trs_relative(self):

        if not cmds.objExists(self.target_name):
            return

        cmds.xform(self.target_name, r=True, t=self.local_t)
        cmds.xform(self.target_name, r=True, ro=self.local_r)
        cmds.xform(self.target_name, s=self.local_s)

    # ===============================================
    @staticmethod
    def blend_trs(trs_list, ratio_list):

        new_trs = TRSInfo()

        new_label_list = []
        new_target_name = trs_list[0].target_name

        # baseを新しいtrsの初期値に
        new_local_t = list(trs_list[0].base_t)
        new_local_r = list(trs_list[0].base_r)
        new_local_s = list(trs_list[0].base_s)

        # ブレンド値をbaseとの差分で計算
        local_t_diff = [0, 0, 0]
        local_r_diff = [0, 0, 0]
        local_s_diff = [0, 0, 0]

        rotate_count = 0

        for trs, ratio in zip(trs_list, ratio_list):

            if not trs.target_name == new_target_name:
                continue

            # label
            new_label_list.append('{}__{}'.format(trs.label, str(int(ratio * 100)).zfill(3)))

            # t
            local_t_diff[0] += (trs.local_t[0] - trs.base_t[0]) * ratio
            local_t_diff[1] += (trs.local_t[1] - trs.base_t[1]) * ratio
            local_t_diff[2] += (trs.local_t[2] - trs.base_t[2]) * ratio

            # r
            rotate_x_diff = trs.local_r[0] - trs.base_r[0]
            rotate_y_diff = trs.local_r[1] - trs.base_r[1]
            rotate_z_diff = trs.local_r[2] - trs.base_r[2]

            if rotate_x_diff > 360:
                rotate_x_diff = rotate_x_diff % 360
            if rotate_y_diff > 360:
                rotate_y_diff = rotate_y_diff % 360
            if rotate_z_diff > 360:
                rotate_z_diff = rotate_z_diff % 360

            local_r_diff[0] += rotate_x_diff * ratio
            local_r_diff[1] += rotate_y_diff * ratio
            local_r_diff[2] += rotate_z_diff * ratio

            # s
            local_s_diff[0] += (trs.local_s[0] - trs.base_s[0]) * ratio
            local_s_diff[1] += (trs.local_s[1] - trs.base_s[1]) * ratio
            local_s_diff[2] += (trs.local_s[2] - trs.base_s[2]) * ratio

        new_trs.label = '|'.join(new_label_list)
        new_trs.target_name = new_target_name

        # ブレンド差分と初期値を合成
        new_trs.local_t[0] = new_local_t[0] + local_t_diff[0]
        new_trs.local_t[1] = new_local_t[1] + local_t_diff[1]
        new_trs.local_t[2] = new_local_t[2] + local_t_diff[2]

        new_trs.local_r[0] = new_local_r[0] + local_r_diff[0]
        new_trs.local_r[1] = new_local_r[1] + local_r_diff[1]
        new_trs.local_r[2] = new_local_r[2] + local_r_diff[2]

        new_trs.local_s[0] = new_local_s[0] + local_s_diff[0]
        new_trs.local_s[1] = new_local_s[1] + local_s_diff[1]
        new_trs.local_s[2] = new_local_s[2] + local_s_diff[2]

        return new_trs
