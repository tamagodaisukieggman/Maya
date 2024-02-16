# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import json

from . import const

reload(const)


class UnitySnapData(object):

    def __init__(self):

        self.json_data = None
        self.exists = False
        self.snap_list = []
        self.grp_ids = []
        self.root_labels = []
        self.types = []
        self.snap_ver = 0

    def init(self, json_path):
        """初期化
        """

        self.exists = False

        self.load(json_path)
        if not self.json_data:
            return

        self.snap_list = self.json_data.get(const.SNAP_LIST_KEY)
        self.grp_ids = self.json_data.get(const.GRP_ID_LIST_KEY)
        self.root_labels = self.json_data.get(const.ROOT_LABEL_LIST_KEY)
        self.types = self.json_data.get(const.ROOT_TYPE_LIST_KEY)
        self.snap_ver = self.json_data.get(const.SNAP_VER_KEY)

        self.id_dict = {}

        if not all([self.grp_ids, self.root_labels, self.types]):
            return

        for grp_id, root_label, type in zip(self.grp_ids, self.root_labels, self.types):
            self.id_dict[grp_id] = {'Type': type, 'RootName': root_label}

        self.exists = True

    def load(self, json_path):
        """jsonファイルのロード
        """

        try:
            with open(json_path) as f:
                self.json_data = json.load(f)
        except Exception:
            pass

    def init_from_snap_data(self, snap_data):
        """別のスナップデータを使って初期化

        Args:
            snap_data (UnitySnapData): スナップデータ
        """

        self.exists = False

        if not snap_data or not snap_data.exists:
            return

        self.snap_list = snap_data.snap_list
        self.grp_ids = snap_data.grp_ids
        self.root_labels = snap_data.root_labels
        self.types = snap_data.types
        self.snap_ver = snap_data.snap_ver

        self.id_dict = {}
        for grp_id, root_label, type in zip(self.grp_ids, self.root_labels, self.types):
            self.id_dict[grp_id] = {'Type': type, 'RootName': root_label}

        self.exists = True

    def generate_obj_info_iterator(self, frame_index):
        """オブジェクト情報イテレーターを作成

        Args:
            frame_index (int): 取得したいフレームのインデックス
            obj_types ([str]): 取得したいオブジェクトタイプのリスト
            attr_type_keys ([str]): 取得したいアトリビュートの型のキーリスト
            attr_keys ([str]): 取得したいアトリビュートのキーリスト

        Yields:
            str, str, str, any: rootオブジェクト名, オブジェクト名, オブジェクトタイプ, アトリビュート値
        """

        if not self.exists:
            print('no json data')
            return

        if frame_index > len(self.snap_list) - 1:
            print('frame out of range')
            return

        this_snap = self.snap_list[frame_index]
        obj_datas = this_snap[const.OBJ_DATA_LIST_KEY]

        for obj_data in obj_datas:

            obj_name = obj_data[const.OBJ_NAME_KEY]
            grp_id = obj_data[const.OBJ_GRP_ID_KEY]
            is_root = obj_data[const.OBJ_IS_ROOT_KEY]
            obj_type = self.id_dict[grp_id]['Type']

            for data_type in const.ALL_DATA_LIST_KEYS:
                for type_data in obj_data[data_type]:
                    yield obj_name, obj_type, grp_id, is_root, type_data[const.ATTR_LABEL], type_data[const.DATA_LABEL]

    def get_axis_obj_name(self):

        if not self.exists:
            print('no json data')
            return

        if not self.snap_list:
            return

        this_snap = self.snap_list[0]
        axis_obj_data = this_snap[const.AXIS_OBJ_DATA_KEY]
        return axis_obj_data.get(const.OBJ_NAME_KEY)

    def get_axis_obj_attr(self, frame_index, attr_type_key, attr_key):
        """基準軸オブジェクト情報を取得

        Args:
            frame_index (int): 取得したいフレームのインデックス
            attr_type_key (str): 取得したいアトリビュートの型のキー
            attr_key (str): 取得したいアトリビュートのキー

        Returns:
            any: アトリビュート値
        """

        if not self.exists:
            print('no json data')
            return

        if frame_index > len(self.snap_list) - 1:
            print('frame out of range')
            return

        this_snap = self.snap_list[frame_index]
        axis_obj_data = this_snap[const.AXIS_OBJ_DATA_KEY]
        if not axis_obj_data:
            return

        type_datas = axis_obj_data.get(attr_type_key)
        if not type_datas:
            return

        for type_data in type_datas:
            if type_data[const.ATTR_LABEL] == attr_key:
                return type_data[const.DATA_LABEL]

    def get_grp_info_dicts(self):
        """グループ情報リストを取得

        Returns:
            list: [{'GrpId':int, 'RootName':str, 'Type':str},,,]
        """

        if not self.exists:
            return []

        result_dicts = []

        for grp_id, root_label, type in zip(self.grp_ids, self.root_labels, self.types):
            result_dicts.append(
                {
                    'GrpId': grp_id,
                    'RootName': root_label,
                    'Type': type,
                }
            )

        result_dicts.sort(key=lambda x: x['GrpId'])
        return result_dicts

    def get_frame_count(self):
        """総フレーム数を取得
        """
        return len(self.snap_list)

    def get_frame_time(self, frame_index):
        """フレームの時間を取得

        Args:
            frame_index (int): 取得したいフレームのインデックス

        Returns:
            float: フレームの時間
        """

        if not self.exists:
            print('no json data')
            return

        if frame_index > len(self.snap_list) - 1:
            print('frame out of range')
            return

        return self.snap_list[frame_index].get(const.SANP_TIME_KEY)
