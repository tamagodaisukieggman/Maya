# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from . import view
from . import snap_importer_command as command
from . import unity_snap_data
from . import obj_mapping_data
from . import const

reload(view)
reload(command)
reload(unity_snap_data)
reload(obj_mapping_data)
reload(const)


class SnapImporter(object):

    def __init__(self):
        """コンストラクタ
        """

        self.unity_snap_data = None
        self.scene_org_snap_data = None
        self.current_mapping_data = None
        self.frame_index = 0
        self.root_orient_key = const.ROOT_ORIENT_WORLD

        self.is_initialized = False
        self.is_connecting = False

    def __undo_ignore_decorator(func):
        """Undo対象にしないためのデコレーター
        デコレートする関数内で破壊的な操作をおこなうとUndo結果が不安定になる恐れがあるので注意
        """
        def wrapper(self, *args, **kwargs):

            # Undoへの記録をオフにする
            cmds.undoInfo(swf=False)

            try:
                func(self, *args, **kwargs)
            except Exception as e:
                raise e
            finally:
                # Undoへの記録をオンに戻す
                cmds.undoInfo(swf=True)

        return wrapper

    def initialize(self, json_path, valid_version_range=None):
        """初期化
        """

        self.is_initialized = False

        # jsonの読み取り
        self.unity_snap_data = self.create_unity_snap_data(json_path)

        # 古いバージョンのjsonははじく
        if valid_version_range:
            snap_ver = self.unity_snap_data.snap_ver
            if snap_ver < valid_version_range[0] or valid_version_range[1] < snap_ver:
                cmds.warning('INVALID VERSION: {}(valid version={})'.format(str(snap_ver), str(valid_version_range)))
                return

        if not self.unity_snap_data.exists:
            return

        # マッピングデータの作成
        grp_info_dicts = self.unity_snap_data.get_grp_info_dicts()
        if not grp_info_dicts:
            return

        self.current_mapping_data = self.create_new_mapping_data(
            grp_info_dicts,
            self.unity_snap_data.get_axis_obj_name()
        )

        self.is_initialized = True

    def set_root_orient(self, key):
        """ルート軸の設定
        """

        self.root_orient_key = key
        self.apply_snap(self.root_orient_key)

    def set_frame_index(self, index):
        """再現するフレームインデックスの指定
        """

        self.frame_index = index
        self.apply_snap(self.root_orient_key)

    def set_connection_state(self, connection_state):
        """再現するかどうかを指定
        """

        if self.is_connecting == connection_state:
            return
        else:
            self.is_connecting = connection_state

        if self.is_connecting:
            # 開始
            self.scene_org_snap_data = self.create_current_snap()
            self.apply_snap(self.root_orient_key)
        else:
            # 終了
            if self.scene_org_snap_data:
                self.apply_org_scene_snap()

    def create_new_mapping_data(self, grp_info_dicts, axis_obj):
        """新規マッピングデータの作成

        Args:
            grp_info_dicts ([{'GrpId':int, 'RootName':str, 'Type':str},,,]): マッピング情報を持ったdictのリスト
            axis_obj (str): 基準軸オブジェクトのUnity名

        Returns:
            obj_mapping_data.ObjMappingData: マッピングデータ
        """

        if not grp_info_dicts:
            return
        else:
            return obj_mapping_data.ObjMappingData(grp_info_dicts, axis_obj)

    def update_mapping(self, root_mappting_infos, axis_mapping_obj=None):
        """_summary_

        Args:
            root_mappting_infos (['ObjType': str, 'UnityRoot': str, 'MayaRoot': str, 'Opts': list, 'GrpId': int]): 更新用ルート情報リスト
            axis_mapping_obj (_type_, optional): 基準軸オブジェクトのMayaパス. Defaults to None.
        """

        if not self.current_mapping_data:
            return

        # マッピングを更新すると元を復元できなくなるので、更新前に戻しておく
        if self.is_connecting and self.scene_org_snap_data:
            self.apply_org_scene_snap()

        for root_mappting_info in root_mappting_infos:

            maya_root = root_mappting_info['MayaRoot']
            opts = root_mappting_info['Opts']
            grp_id = root_mappting_info['GrpId']

            self.current_mapping_data.init_obj_mapping_for_each_root(grp_id, maya_root, opts)

        self.current_mapping_data.init_axis_obj_mapping(axis_mapping_obj)

        # 更新されたマッピングで再度オリジナルを記録してからスナップを実行
        if self.is_connecting:
            self.scene_org_snap_data = self.create_current_snap()
            self.apply_snap(self.root_orient_key)

    def create_unity_snap_data(self, json_path):
        """jsonファイルのロード
        """

        data = unity_snap_data.UnitySnapData()
        data.init(json_path)
        return data

    def create_current_snap(self):
        """現在のシーン情報から１フレームのスナップデータを作成
        スナップデータとマッピングデータから元スナップと同じアトリビュートのスナップを作成

        Returns:
            unity_snap_data.UnitySnapData: 現在のシーンのスナップデータ
        """

        if not self.unity_snap_data or not self.unity_snap_data.exists:
            return

        if not self.current_mapping_data:
            return

        current_snap = command.save_current_scene_to_snap(self.unity_snap_data, self.current_mapping_data)

        return current_snap

    @__undo_ignore_decorator
    def apply_snap(self, root_orient):
        """再現実行

        Args:
            root_orient (str): ルート軸のキー
        """

        if not self.is_connecting:
            return
        if not self.unity_snap_data.exists:
            return

        current_index = 0
        if self.unity_snap_data.get_frame_count() != 1:
            current_index = self.frame_index
            current_index = max([current_index, 0])
            current_index = min([current_index, self.unity_snap_data.get_frame_count() - 1])

        # ローカルパラメータの適用
        command.import_local_snap_data(self.unity_snap_data, self.current_mapping_data, current_index)

        # ルートの座標変換
        if root_orient == const.ROOT_ORIENT_WORLD:
            command.import_world_transform_to_root(self.unity_snap_data, self.current_mapping_data, current_index)
        elif root_orient == const.ROOT_ORIENT_AXIS_OBJ:
            command.import_axis_transform_to_root(self.unity_snap_data, self.current_mapping_data, current_index)

    @__undo_ignore_decorator
    def apply_org_scene_snap(self):
        """self.scene_org_snap_dataに記録されているスナップを復元
        """

        if not self.scene_org_snap_data.exists:
            return

        command.import_local_snap_data(self.scene_org_snap_data, self.current_mapping_data, 0, True)
