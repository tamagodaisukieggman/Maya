import os
import typing as tp

import maya.cmds as cmds

from .node_data import NodeData, RootNodeData, DescendentsNodeData


class NodeDataFactoryBase:
    """NodeDataのFactoryの基底クラス"""

    @classmethod
    def create(cls, node_long_name: str) -> NodeData:
        ...

    @staticmethod
    def _get_short_name(node) -> str:
        """対象ノードのロングネームをショートネームに変換する関数
        Args:
            node (str): 対象のノード名
        Returns:
            str: ショートネーム
        """
        return node.split("|")[-1]


class DescendentsNodeDataFactory(NodeDataFactoryBase):
    @classmethod
    def create(cls, node_long_name: str) -> DescendentsNodeData:
        node_data = DescendentsNodeData(
            root_node_name=cls._get_top_parent(node_long_name),
            full_path_name=node_long_name,
            node_type=cmds.nodeType(node_long_name),
            short_name=cls._get_short_name(node_long_name),
            deep=cls._get_hierarchy_depth(node_long_name),
        )
        # extra_dataの設定
        cls._set_extra_data(node_data)
        return node_data

    @staticmethod
    def _get_hierarchy_depth(node) -> int:
        """対象ノードの階層の深さを調べる関数
        Args:
            node (str): 対象のノード名
        Returns:
            int: 階層の深さ
        """
        depth = 0
        while cmds.listRelatives(node, parent=True, pa=True):
            node = cmds.listRelatives(node, parent=True, pa=True)[0]
            depth += 1
        return depth

    @staticmethod
    def _get_top_parent(node) -> str:
        """対象ノードの階層で一番上の親となるノードを返す関数
        Args:
            node (str): 対象のノード名
        Returns:
            str: 一番上の親ノード名
        """
        while cmds.listRelatives(node, parent=True, pa=True):
            node = cmds.listRelatives(node, parent=True, pa=True)[0]
        return node

    @classmethod
    def _set_extra_data(cls, descendent_node: DescendentsNodeData):
        """与えられたextradataを設定する
        descendent_nodeのnodetypeによってユニークなデータを設定

        Args:
            descendent_node (DescendentsNodeData): 対象となるnodedata
        """
        if descendent_node.node_type == "transform":
            descendent_node.extra_data["has_shape"] = cls._check_has_shape(
                descendent_node
            )

    @classmethod
    def _check_has_shape(self, node: NodeData) -> bool:
        """shapeを所有しているかどうか

        Returns:
            bool: _description_
        """
        transform = node.full_path_name
        shapes = cmds.listRelatives(transform, children=True, shapes=True) or []
        if shapes:
            return True
        return False


class RootNodeDataFactory(NodeDataFactoryBase):
    @classmethod
    def create(cls, node_long_name: str) -> RootNodeData:
        node_data = RootNodeData(
            root_node_name=cls._get_short_name(node_long_name),
            full_path_name=node_long_name,
            node_type=cmds.nodeType(node_long_name),
            short_name=cls._get_short_name(node_long_name),
            all_descendents=cls._get_all_descendents(node_long_name),
        )
        return node_data

    @staticmethod
    def _get_all_descendents(node: str) -> tp.List[DescendentsNodeData]:
        """rootノード名からすべての子孫のmeta情報クラス(DescendentsNodeData)の作成
        配列でDescendentsNodeDataを返す

        Args:
            node (str): ルートとなるノード名

        Returns:
            tp.List[DescendentsNodeData]: nodeの子孫のメタ情報
        """
        descendent_node_datas = []
        for long_node_name in cmds.listRelatives(node, ad=True, ni=True, fullPath=True) or []:
            descendent_node_data = DescendentsNodeDataFactory.create(long_node_name)
            descendent_node_datas.append(descendent_node_data)
        return descendent_node_datas
