# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from . import reorder_dicts
from .condition_methods import glp as glp_method
from .... import glp_common
from ....glp_common.classes.info import chara_info

reload(reorder_dicts)
reload(glp_method)
reload(glp_common)


class ReorderNodes(object):

    def __init__(self):

        self.__chara_info = chara_info.CharaInfo()

    def reorder_nodes(self):
        """アウトライナーの整列を実行
        """

        self.__chara_info.create_info()

        if not self.__chara_info.exists:
            return

        chara_info_root_node = self.__chara_info.part_info.root_node
        root_nodes = cmds.ls(chara_info_root_node + '*', l=True, type='transform')

        if not root_nodes:
            return

        # head
        if self.__chara_info.part_info.data_type.endswith('head'):
            for root_node in root_nodes:
                self.reorder_head_model_nodes(root_node)

        # body(attach)
        elif self.__chara_info.part_info.data_type.endswith('body') or self.__chara_info.part_info.data_type.endswith('attach'):
            for root_node in root_nodes:
                self.reorder_body_model_nodes(root_node)

        # default
        else:
            for root_node in root_nodes:
                self.reorder_base_model_nodes(root_node)

    def reorder_base_model_nodes(self, root_node):
        """デフォルトのモデルのアウトライナー整列

        Args:
            root_node (str): _description_
        """

        self.__reorder_nodes_default(root_node)
        self.__reorder_root_nodes(root_node)

    def reorder_head_model_nodes(self, root_node):
        """ヘッドモデルのアウトライナー整列

        Args:
            root_node (str): _description_
        """

        self.__reorder_head_root_nodes(root_node)
        self.__reorder_head_joint_nodes(root_node)

    def reorder_body_model_nodes(self, root_node):
        """ボディーモデルのアウトライナー整列

        Args:
            root_node (str): 整列をするボディーのルートノード
        """

        self.__reorder_nodes_default(root_node)
        self.__reorder_root_nodes(root_node)
        self.__reorder_hip_nodes(root_node)
        self.__reorder_wrist_nodes(root_node)

    def __reorder_nodes_default(self, root_node):
        """ノード内をデフォルトの並び順で整列

        Args:
            root_node (str): 整列をするルートノード
        """

        targets = [root_node]
        all_children = cmds.listRelatives(root_node, ad=True, f=True)

        if all_children:
            targets.extend(all_children)

        for node in targets:
            self.__reorder_children(node, reorder_dicts.default_order_dicts)

    def __reorder_root_nodes(self, root_node):
        """ルートノード内を整列

        Args:
            root_node (str): 整列をするルートノード
        """

        if cmds.objExists(root_node):
            self.__reorder_children(root_node, reorder_dicts.root_order_dicts)

    def __reorder_head_root_nodes(self, root_node):
        """ヘッドのルートノード内を整列

        Args:
            root_node (str): 整列をするヘッドのルートノード
        """

        if cmds.objExists(root_node):
            self.__reorder_children(root_node, reorder_dicts.head_model_root_order_dicts)

    def __reorder_head_joint_nodes(self, root_node):
        """Headジョイントノード内を整列

        Args:
            root_node (str): 整列をするヘッドのルートノード
        """

        all_children = cmds.listRelatives(root_node, ad=True, f=True)

        for node in all_children:

            if node.split('|')[-1].endswith('Head'):
                self.__reorder_children(node, reorder_dicts.head_order_dicts)
                break

    def __reorder_hip_nodes(self, root_node):
        """Hip内を整列

        Args:
            root_node (str): 整列をするボディーのルートノード
        """

        all_children = cmds.listRelatives(root_node, ad=True, f=True)

        for node in all_children:

            if node.split('|')[-1].startswith('Hip'):
                self.__reorder_children(node, reorder_dicts.hip_order_dicts)
                break

    def __reorder_wrist_nodes(self, root_node):
        """Wrist_L, Wrist_R内を整列

        Args:
            root_node (str): 整列をするボディーのルートノード
        """

        all_children = cmds.listRelatives(root_node, ad=True, f=True)

        for node in all_children:

            if node.split('|')[-1] == 'Wrist_L' or node.split('|')[-1] == 'Wrist_R':
                self.__reorder_children(node, reorder_dicts.wrist_order_dicts)

    def __reorder_children(self, parent, order_dicts):
        """子階層をreorder_dictsにしたがって整列

        Args:
            parent (str): 整列させるノード群の親ノード
            reorder_dicts (order_dicts): 並び替えを指定するディクトのリスト
        """

        targets = cmds.listRelatives(parent, c=True, f=True, typ='transform')

        if not targets:
            return

        dicts = reorder_dicts.get_sorted_order_dicts(targets, order_dicts)
        new_list = reorder_dicts.get_list_from_order_dicts(dicts)
        self.__reorder_outliner(new_list)

    def __reorder_outliner(self, order_list):
        """アウトライナーの並び替え

        Args:
            order_list (list): 並び替える順のリスト
        """

        for obj in reversed(order_list):
            if cmds.objExists(obj):
                cmds.reorder(obj, f=True)

    def apply_outliner_color(self):
        """アウトライナーカラーの適用
        """

        self.__chara_info.create_info()

        if not self.__chara_info.exists:
            return

        chara_info_root_node = self.__chara_info.part_info.root_node
        root_nodes = cmds.ls(chara_info_root_node + '*', l=True, type='transform')

        if not root_nodes:
            return

        targets = cmds.listRelatives(root_nodes, ad=True, f=True)

        for target in targets:

            if glp_method.is_ear_joint(target):
                self.__apply_ear_joint_color(target)

            elif glp_method.get_special_joint_prefix(target):
                prefix = glp_method.get_special_joint_prefix(target)

                if prefix == 'Sp':
                    self.__apply_sp_joint_color(target)
                else:
                    self.__apply_special_joint_color(target)

    def __apply_ear_joint_color(self, target):
        """耳ジョイント用のカラー適用

        Args:
            target (str): 適用するノード
        """

        cmds.setAttr(target + '.useOutlinerColor', True)
        cmds.setAttr(target + '.outlinerColorR', 1)
        cmds.setAttr(target + '.outlinerColorG', 0.4)
        cmds.setAttr(target + '.outlinerColorB', 0.8)

    def __apply_sp_joint_color(self, target):
        """揺れもの用ジョイントのカラー適用

        Args:
            target (str): 適用するノード
        """

        cmds.setAttr(target + '.useOutlinerColor', True)
        cmds.setAttr(target + '.outlinerColorR', 1)
        cmds.setAttr(target + '.outlinerColorG', 1)
        cmds.setAttr(target + '.outlinerColorB', 0)

    def __apply_special_joint_color(self, target):
        """揺れもの以外の特殊ジョイントのカラー適用

        Args:
            target (str): 適用するノード
        """

        cmds.setAttr(target + '.useOutlinerColor', True)
        cmds.setAttr(target + '.outlinerColorR', 1)
        cmds.setAttr(target + '.outlinerColorG', 0.5)
        cmds.setAttr(target + '.outlinerColorB', 0)
