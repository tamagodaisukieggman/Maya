# -*- coding: utf-8 -*-
"""GallopCharaBodyDifference: 体型差分作成ツール"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from builtins import range
    from importlib import reload
except Exception:
    pass

import os
import re
import csv

import maya.cmds as cmds

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from .. import glp_common
from ..glp_common.classes.info import chara_info

reload(base_common)
reload(glp_common)


class BodyDifference(object):

    # ==================================================
    def __init__(self):

        self.file_name_modifier = None

        self.body_difference_info = None

        self.src_root_name = None
        self.src_outline_mdl_name = None
        self.src_mesh_list = None

        self.skin_data = None

    # ==================================================
    def _initialize(self):
        """初期値設定
        """

        # 開いているファイルのフルパス
        file_path = cmds.file(q=True, sn=True)
        if not file_path:
            print('[Error] : ファイルパスが見つかりません : ' + file_path)
            return False

        # ファイル名の装飾語(BustL, BustM)
        self.file_name_modifier = self._get_file_name_modifier(file_path)

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            print('[Error] : charaInfoが見つかりません')
            return False

        # data_typeがbodyではないかSSR衣装であれば実行しない
        if not _chara_info.part_info.data_type.endswith('body') or _chara_info.is_unique_chara:
            print('[Error] : レギュレーションが合ってません')
            return False

        # 読み込むbody_differnce_infoのcsvのpath
        csv_path = self._get_csv_path(self.file_name_modifier)
        if not csv_path:
            print('[Error] : csvのパスが見つかりません')
            return False

        # 体型差分のパラメータ
        self.body_difference_info = self._get_body_difference_info(csv_path)
        if not self.body_difference_info:
            print('[Error] : body_difference_infoが見つかりません')
            return False

        # rootの各種パス
        src_root_path = _chara_info.part_info.root_node
        self.src_root_name = src_root_path.split('|')[-1]

        # outlineモデルのパス
        if _chara_info.part_info.outline_mesh_list:
            self.src_outline_mdl_name = _chara_info.part_info.outline_mesh_list[0]

        # メッシュリスト
        if _chara_info.part_info.mesh_list:
            self.src_mesh_list = _chara_info.part_info.mesh_list

        # SkinInfoを格納する辞書
        self.skin_data = {}
        for mesh in self.src_mesh_list:

            short_name = mesh.split('|')[-1]

            if not cmds.objExists(mesh):
                continue

            self.skin_data[short_name] = base_class.mesh.skin_info.SkinInfo()
            self.skin_data[short_name].create_info([mesh])

        return True

    # ==================================================
    def _get_file_name_modifier(self, file_path):
        """ファイル名から装飾語(_BustL, _BustM等)を取得し返す
        """

        file_name_modifier = ''

        file_name_without_suffix = file_path.split('\\')[-1].split('.')[0]
        search_modifier_obj = re.search(r'(_Bust[LM])$', file_name_without_suffix)
        if search_modifier_obj:
            file_name_modifier = search_modifier_obj.group(1)

        # mini対応 mchr0がファイル名から見つかった場合は装飾語として"Mini"を取得する
        search_modifier_obj = re.search(r'_mbdy0', file_name_without_suffix)
        if search_modifier_obj:
            file_name_modifier = '_Mini'

        return file_name_modifier

    # ==================================================
    def _get_csv_path(self, file_name_modifier):
        """body_difference_infoのcsvパスを返す
        """

        script_file_path = os.path.abspath(__file__)
        script_dir_path = os.path.dirname(script_file_path)
        csv_path = "{0}{1}{2}.csv".format(
            script_dir_path, '\\resource\\common_body_difference_info', file_name_modifier)

        if not os.path.exists(csv_path):
            return None

        return csv_path

    # ==================================================
    def _get_body_difference_info(self, csv_path):
        """csvから体型差分パラメータ一覧を取得
        """

        try:
            with open(csv_path) as f:
                csv_reader = csv.reader(f)

                key_list = next(csv_reader)

                value_list = [row for row in csv_reader if row and row[0] == '1' and len(row) == len(key_list)]

        except Exception:
            return None

        return {'key_list': key_list, 'value_list': value_list}

    # ==================================================
    def do_create_body_difference(self):
        """実行関数
        """

        if not self._initialize():
            return

        target_difference_list = self.body_difference_info['key_list'][3:]

        for i in range(len(target_difference_list)):

            target_difference = target_difference_list[i]

            dup_root_name = '{0}{1}'.format(self.src_root_name, target_difference)
            if cmds.objExists(dup_root_name):
                continue

            dup_root = cmds.duplicate(self.src_root_name, rr=True, un=True, n=dup_root_name)

            if self.src_outline_mdl_name:
                dup_outline_name = self.src_outline_mdl_name.replace(self.src_root_name, dup_root_name)
                cmds.delete(dup_outline_name)

            for mesh_short_name in list(self.skin_data.keys()):

                target_mesh_name = dup_root[0] + '|' + mesh_short_name
                if not cmds.objExists(target_mesh_name):
                    continue

                target_outline_mesh_name = '{}_Outline'.format(target_mesh_name)
                if cmds.objExists(target_outline_mesh_name):
                    cmds.delete(target_outline_mesh_name)

                renamed_short = cmds.rename(target_mesh_name, mesh_short_name + target_difference)
                renamed_long = cmds.ls(renamed_short, l=True)[0]

                dup_root_info = self._get_root_info(dup_root[0])
                if not dup_root_info:
                    continue

                dup_mesh_skin_cluster = base_utility.mesh.skin.get_skin_cluster(renamed_long)
                if not dup_mesh_skin_cluster:
                    continue

                inf_joint_list = cmds.skinCluster(dup_mesh_skin_cluster, q=True, influence=True)

                for info_value in self.body_difference_info['value_list']:

                    joint_name = self._get_joint_path_for_influence(info_value[1], inf_joint_list)
                    if not joint_name:
                        continue

                    attr_name = info_value[2]
                    attr_params = info_value[i + 3]

                    cmds.setAttr('{0}.{1}'.format(joint_name, attr_name), float(attr_params))

                self._duplicate_for_history_removal(renamed_long)

                self._set_default_scale_for_joint(inf_joint_list)

                cmds.skinCluster(dup_root_info['root_joint'], renamed_long, n=dup_mesh_skin_cluster)

                self._set_weight_based_src_root_skin_info(renamed_long, mesh_short_name)

        self.create_display_layer(self.src_root_name)

        self.move_body_difference(150, True, True)

    # ==================================================
    def do_change_skin_status(self, is_skinning):
        """体型差分の一括バインド・デタッチを行う
        """

        if not self._initialize():
            return

        self.move_body_difference(0, True, True)
        self.move_body_difference(0, False, True)

        target_difference_list = self.body_difference_info['key_list'][3:]

        for i in range(len(target_difference_list)):

            target_difference = target_difference_list[i]

            root_name = '{0}{1}'.format(self.src_root_name, target_difference)
            if not cmds.objExists(root_name):
                continue

            for mesh_short_name in list(self.skin_data.keys()):

                long_name = root_name + "|" + mesh_short_name + target_difference
                if not cmds.objExists(root_name):
                    continue

                root_info = self._get_root_info(root_name)

                if is_skinning:
                    self._duplicate_for_history_removal(long_name)
                    cmds.skinCluster(root_info['root_joint'], long_name)
                    self._set_weight_based_src_root_skin_info(long_name, mesh_short_name)
                else:
                    self._duplicate_for_history_removal(long_name)

    # ==================================================
    def move_body_difference(self, move_num, is_position, is_initialized=False):
        """複製したメッシュを並び替える

        :param is_position: position用かgroupNode用か
        :param move_num: 隣接間隔
        """

        target_list = {
            "_Height_SS": -1,
            "_Height_LL": 2,
            "_Height_L": 1,
            "_Shape_1": -1,
            "_Shape_2": 1,
            "_Bust_SS": -2,
            "_Bust_S": -1,
            "_Bust_LL": 2,
            "_Bust_L": 1
        }

        if not is_initialized:
            if not self._initialize():
                return

        target_difference_list = self.body_difference_info['key_list'][3:]

        for i in range(len(target_difference_list)):

            target_difference = target_difference_list[i]

            root_name = '{0}{1}'.format(self.src_root_name, target_difference)
            if not cmds.objExists(root_name):
                continue

            root_info = self._get_root_info(root_name)
            if not root_info:
                continue

            if is_position:
                cmds.setAttr(root_info['root_path'] + ".translateX", 0)
                cmds.setAttr(
                    root_info['root_path'] + "|Position.translateX",
                    move_num * target_list[target_difference])
            else:
                cmds.setAttr(
                    root_info['root_path'] + ".translateX",
                    move_num * target_list[target_difference])
                cmds.setAttr(root_info['root_path'] + "|Position.translateX", 0)

    # ==================================================
    def _set_weight_based_src_root_skin_info(self, target_mesh, mesh_type):
        """src_root_skin_infoを元に対象のメッシュにweight値をセットする
        """

        dst_skin_info = base_class.mesh.skin_info.SkinInfo()
        dst_skin_info.create_info([target_mesh])
        base_utility.mesh.skin.paste_weight_by_vertex_index(self.skin_data[mesh_type], dst_skin_info)

    # ==================================================
    def _duplicate_for_history_removal(self, mesh_name):
        """ヒストリー削除を目的にduplicateを行う
        """

        dup_mesh = cmds.duplicate(mesh_name, n='duplicate_mesh')
        cmds.delete(mesh_name)
        cmds.rename(dup_mesh[0], mesh_name.split('|')[-1])

    # ==================================================
    def _set_default_scale_for_joint(self, joint_list):
        """対象のジョイントを初期スケール(=1.0)に戻す
        """

        for joint in joint_list:
            cmds.setAttr('{0}.{1}'.format(joint, 'scaleX'), 1)
            cmds.setAttr('{0}.{1}'.format(joint, 'scaleY'), 1)
            cmds.setAttr('{0}.{1}'.format(joint, 'scaleZ'), 1)

    # ==================================================
    def _get_root_info(self, root_name):
        """対象のrootの各種情報(ルートフルパス、ルートジョイントフルパス)を取得する
        """

        root_path = self._get_long_name_for_short_name(root_name)
        if not root_path:
            print('[Error] root_pathがみつかりません : ' + root_name)
            return None

        root_joint_path = self._get_long_name_for_short_name(root_path + '|Position|Hip')
        if not root_joint_path:
            print('[Error] root_joint_pathがみつかりません' + root_path + '|Position|Hip')
            return None

        return {
            'root_path': root_path,
            'root_joint': root_joint_path
        }

    # ==================================================
    def _get_joint_path_for_influence(self, joint_name, child_list):
        """jointのショートネームを元に
        インフルエンスされているジョイントのリストからパスを取得する
        """

        for child_name in child_list:
            if child_name.endswith(joint_name):
                return child_name

        return None

    # ==================================================
    def _get_long_name_for_short_name(self, target_path):
        """ショートネームからロングネームを取得する
        """

        target_path_long_name_list = cmds.ls(target_path, l=True)
        if not target_path_long_name_list:
            return None

        target_path_long_name = target_path_long_name_list[0]
        if not cmds.objExists(target_path_long_name):
            return None

        return target_path_long_name

    # ==================================================
    def create_display_layer(self, root_name):
        u"""レイヤー作成、振り分け

        :param root_name: グループ名
        """

        key_list = self.body_difference_info['key_list'][3:]
        root_nodes = cmds.ls('Root')

        layer_name_dict = {
            'height_layer': [],
            'shape_layer': [],
            'bust_layer': [],
            'original_layer': root_name,
            'joint_layer': root_nodes
        }

        for key in key_list:
            target_root_name = root_name + key
            if '_Height_' in key:
                layer_name_dict['height_layer'].append(target_root_name)
            elif '_Shape_' in key:
                layer_name_dict['shape_layer'].append(target_root_name)
            elif '_Bust_' in key:
                layer_name_dict['bust_layer'].append(target_root_name)

        for key, value in list(layer_name_dict.items()):
            layer_name = key + self.file_name_modifier
            if cmds.objExists(layer_name):
                cmds.delete(layer_name)
            cmds.select(value)
            cmds.createDisplayLayer(name=layer_name)
