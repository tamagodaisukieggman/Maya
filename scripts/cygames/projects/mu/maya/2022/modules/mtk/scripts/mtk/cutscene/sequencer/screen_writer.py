"""モジュールの説明
Screen writerのヘルパー関数
"""
from __future__ import annotations

import copy
import re
import typing as tp
from enum import Enum

from maya import cmds
from mtk.cutscene.sequencer.config.data import BindingData


class ScreenWriterManager(object):
    _instance = None

    def create_node(self):
        screen_writer = cmds.createNode("ScreenWriter", skipSelect=True)
        # self._screen_writer_list.append({"node": screen_writer})
        return screen_writer

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ScreenWriterManager()
        return cls._instance

    @classmethod
    def check_plugin(cls):
        if not cmds.pluginInfo("MtkSequencer", query=True, loaded=True):
            cmds.loadPlugin("z:/mtk/tools/maya/2022/modules/mtk/plug-ins/MtkSequencer.mll")

    @classmethod
    def delete_node(cls, name):
        if cmds.nodeType(name) == "ScreenWriter":
            cmds.delete(name)
        else:
            raise ValueError(f"mismatch node type. [{name}]")


class ConnectType(Enum):
    Input = 0
    Output = 1


class ObjectType(Enum):
    Matrix = 0
    Extra = 1
    Position = 2
    Rotation = 3


class ScreenWriterConnector(object):
    def __init__(self, screen_writer) -> None:
        self.screen_writer = screen_writer
        self.organizer = _ScreenWriterConnectOrganizer(self.screen_writer)

    # =============================================================================
    # 入力接続
    # =============================================================================
    def connect_input(self, object_type: ObjectType, **kwargs):
        """入力を接続する

        Args:
            object_type (ObjectType): 接続タイプ
        """
        if ObjectType.Matrix == object_type:
            self._connect_input_matrix(self.screen_writer, kwargs["play_data_index"], kwargs["index"], kwargs["target"])
        elif ObjectType.Extra == object_type:
            self._connect_input_extra(self.screen_writer, kwargs["play_data_index"], kwargs["index"], kwargs["target"], kwargs["name"])
        else:
            raise ValueError("Input error.")

        self.organize_input_connect()

    # =============================================================================
    # 出力接続
    # =============================================================================

    def connect_output(self, object_type: ObjectType, **kwargs):
        if ObjectType.Position == object_type:
            self._connect_output_position(self.screen_writer, kwargs["index"], kwargs["target"])
        elif ObjectType.Rotation == object_type:
            self._connect_output_rotation(self.screen_writer, kwargs["index"], kwargs["target"])
        elif ObjectType.Extra == object_type:
            self._connect_output_extra(self.screen_writer, kwargs["index"], kwargs["target"], kwargs["name"])
        else:
            raise ValueError("Output Error.")

    def _connect_input_matrix(self, screen_writer, play_data_index, index, connect_node):
        matrix_attr = f"{connect_node}.matrix"
        if not cmds.getAttr(matrix_attr, lock=True):
            cmds.connectAttr(matrix_attr, f"{screen_writer}.screen_play_data[{play_data_index}].input_matrix[{index}]", force=True)

    def _connect_input_extra(self, screen_writer, play_data_index, index, connect_node, attr_name):
        attr = f"{connect_node}.{attr_name}"
        input_attr = f"{screen_writer}.screen_play_data[{play_data_index}].input_extra[{index}]"
        cmds.connectAttr(attr, input_attr, force=True)

    def _connect_output_position(self, screen_writer, index, connect_node):
        transform_attr = f"{connect_node}.translate"
        if not cmds.getAttr(transform_attr, lock=True):
            output_attr = f"{screen_writer}.output_position[{index}]"
            cmds.connectAttr(output_attr, transform_attr, force=True)

    def _connect_output_rotation(self, screen_writer, index, connect_node):
        rotation_attr = f"{connect_node}.rotate"
        if not cmds.getAttr(rotation_attr, lock=True):
            output_attr = f"{screen_writer}.output_rotate[{index}]"
            cmds.connectAttr(output_attr, rotation_attr, force=True)

    def _connect_output_extra(self, screen_writer, index, connect_node, connect_attr_name):
        attr = f"{connect_node}.{connect_attr_name}"
        output_attr = f"{screen_writer}.output_extra[{index}]"
        cmds.connectAttr(output_attr, attr, force=True)

    def create_binding_list(self, namespace, binding_data: BindingData):
        search_condition = binding_data.binding_condition.format(namespace=namespace)
        node_list = cmds.ls(search_condition)

        if binding_data.is_binding_solo:
            binding_data = node_list
        else:
            binding_data = cmds.listRelatives(node_list[0], allDescendents=True, type=binding_data.node_type, shapes=False)
            binding_data = [cmds.listRelatives(_, parent=True, path=True, type="transform")[0] for _ in binding_data]
        binding_data.sort()
        return binding_data

    def organize_input_connect(self):
        """コネクトを整理する
        Clipを削除したり、Trackを追加した時にコネクト順番を整理する関数
        """
        self.organizer.organize()

    def get_can_input_index(self):
        """接続可能なinput_indexを取得する

        Returns:
            int: 接続可能なindex
        """
        return self.organizer.get_missing_number()


class _ScreenWriterConnectOrganizer(object):
    """ScreeWriterの接続整理機能
    """
    SEARCH_WORD = "(?<={}\[)[0-9]"
    SEARCH_REGEX = re.compile("(?<={}\[)[0-9]")

    def __init__(self, screen_writer) -> None:
        super().__init__()
        self.screen_writer = screen_writer

    def organize(self):
        connect_filter_list = self._collect_screen_writer_connect()
        if not connect_filter_list:
            return

        number_list = self._extract_number_list(connect_filter_list)
        missing_value = self._get_missing_value(number_list)

        connect_filter_pair_list = self._create_connect_pair_list(connect_filter_list)

        if missing_value is None:
            return

        organized_connect_filter_pair_list = self._crate_organized_pair_list(connect_filter_pair_list, missing_value)

        self._reconnect(connect_filter_pair_list, organized_connect_filter_pair_list)

    def get_missing_number(self):
        connect_filter_list = self._collect_screen_writer_connect()
        if not connect_filter_list:
            return 0

        number_list = self._extract_number_list(connect_filter_list)
        missing_value = self._get_missing_value(number_list, offset=1)

        if missing_value is None:
            return 0

        return missing_value

    def _collect_screen_writer_connect(self):
        """接続を収集する
        Args:
            screen_writer (str): screen_writerノード名
        Returns:
            list[str]: 接のノードリスト
        """
        connect_list = cmds.listConnections(self.screen_writer, connections=True, destination=False)
        if not connect_list:
            return None

        connect_list = self._extract_word(connect_list)
        return connect_list

    def _extract_word(self, filter_list: tp.List[str], search_word="screen_play_data"):
        """文字列を元に抽出する

        Args:
            filter_list (list[str]): フィルターする元リスト

        Returns:
            list[str]: 抽出後のword
        """
        filter_list = [_ for _ in filter_list if f"{search_word}" in _]
        filter_list.sort()
        return filter_list

    def _extract_number_list(self, connect_list):
        number_list = list()
        for connect_node in connect_list:
            number_list.append(self._extract_number(connect_node))

        number_list = list(set(number_list))
        number_list.sort()
        return number_list

    def _extract_number(self, connect_node):
        search_format_regex = re.compile(self.SEARCH_WORD.format("screen_play_data"))
        result = search_format_regex.search(connect_node)
        if result:
            return int(result.group())

    def _get_missing_value(self, number_list, offset=0):
        max_value = max(number_list) + offset
        for index in range(0, max_value + 1):
            if index not in number_list:
                return index

        return None

    def _create_connect_pair_list(self, original_list):
        """接続の対応リストを作成する
        """
        connect_filter_pair_list = list()
        for attr_name in original_list:
            connect_filter_pair_list.append([cmds.connectionInfo(attr_name, sourceFromDestination=True),
                                            attr_name])
        return connect_filter_pair_list

    def _crate_organized_pair_list(self, base_pair_list, missing_value):
        """整理済みのペアリストを作成する

        Args:
            base_pair_list (list[str])): 既存の接続ペアリスト
            missing_value (int): 欠損している番号
        """
        organized_connect_filter_pair_list = copy.deepcopy(base_pair_list)
        for i, connet_node in enumerate(organized_connect_filter_pair_list):
            number = self._extract_number(connet_node[1])

            if missing_value < number:
                search_format_regex = re.compile(self.SEARCH_WORD.format("screen_play_data"))
                replace_string = search_format_regex.sub(str(number - 1), connet_node[1])
                organized_connect_filter_pair_list[i][1] = replace_string
        return organized_connect_filter_pair_list

    def _reconnect(self, des_connect_pair_list, src_connect_pair_list):
        """再接続する

        Args:
            des_connect_pair_list (list[str])): 接続リスト
            src_connect_pair_list (list[str]): 整理後の接続リスト
        """
        for des_node, src_node in des_connect_pair_list:
            cmds.disconnectAttr(des_node, src_node)

        for des_node, src_node in src_connect_pair_list:
            cmds.connectAttr(des_node, src_node, force=True)
