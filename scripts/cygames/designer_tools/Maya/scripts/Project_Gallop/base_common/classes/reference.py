# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import codecs
import os
import random
import re
import shutil
import string

import maya.cmds as cmds


class ReferenceController(object):

    def __init__(self):

        self.initialize()

    def initialize(self):
        self.loaded = False
        self.is_error = False

        self.file_path = None
        self.namespace = None
        self.added_node_list = []
        self.reason = None

        self.is_temp_file = False

    def load(self, target_path, target_namespace, block_multi_level_reference=False):
        """
        file pathとnamespaceを指定してリファレンスでロードする。

        Args:
            target_path (str): リファレンスを行うパス
            target_namespace (str): リファレンスに命名するネームスペース
            block_multi_level_reference (bool, optional): リファレンスファイルの中にさらにリファレンスが含まれる場合取り込みをブロックするか. Defaults to False.
        """

        self.initialize()

        if target_path is None or target_namespace is None:
            self.__register_error('pathやnamespaceにNoneの指定はできない')
            return

        if not os.path.exists(target_path):
            self.__register_error('指定されたパスが存在しないため')
            return

        if self.__namespace_exists(target_namespace):
            self.__register_error('ネームスペースが衝突している')
            return
        else:
            self.file_path = target_path
            self.namespace = target_namespace

        if not self.loaded:
            if block_multi_level_reference:
                self.added_node_list = cmds.file(self.file_path, ignoreVersion=True, ns=self.namespace, r=True,
                                                mergeNamespacesOnClash=False, rnn=True, lrd='topOnly')
            else:
                self.added_node_list = cmds.file(self.file_path, ignoreVersion=True, ns=self.namespace, r=True,
                                                mergeNamespacesOnClash=False, rnn=True)
            self.loaded = True

            if not self.__namespace_exists(self.namespace):
                self.__register_error('読み込み中に不明なエラーが発生した')

    def load_using_no_plugin_tmp(self, target_path, target_namespace, block_multi_level_reference=False):
        """プラグイン情報を削除した一時ファイルを作成してロード
        一時ファイルはunloadで削除されます。一時ファイルは.maを直接書き換えているので一時的なジオメトリ参照限定で使用してください。

        Args:
            target_path (str): リファレンスを行うパス
            target_namespace (str): リファレンスに命名するネームスペース
            block_multi_level_reference (bool, optional): リファレンスファイルの中にさらにリファレンスが含まれる場合取り込みをブロックするか. Defaults to False.
        """

        # tmpファイルを作成
        tmp_path = target_path.replace('.ma', '__no_plugin_tmp_{0}__.ma'.format(self.__generate_random_string(5)))
        shutil.copyfile(target_path, tmp_path)

        # プラグイン情報を削除
        # requires行からmaya以外を削除
        ma_str = ''
        with codecs.open(tmp_path, 'r', 'shift_jis') as f:
            ma_str = f.read()

        ma_str = re.sub('requires (?!.*maya).+;\n', '', ma_str)
        with codecs.open(tmp_path, 'w', 'shift_jis') as f:
            f.write(ma_str)

        self.load(tmp_path, target_namespace, block_multi_level_reference)

        if self.loaded:
            self.is_temp_file = True

    def unload(self, unload_hard=False):
        """
        Unload HardがTrueの際は、TurtleノードやBaseAnimationなどがリファレンスしたシーンに残らないようにする。
        """

        if self.loaded:
            ref_node = None

            for node in self.added_node_list:
                if cmds.referenceQuery(node, inr=True):
                    # _UNKNOWN_REF_NODE_が存在している時にエラーになるのでtry/exceptする
                    try:
                        ref_node = cmds.referenceQuery(node, rfn=True, tr=True)
                        break
                    except Exception:
                        continue

            if ref_node:
                cmds.file(rfn=ref_node, rr=True)

            # 'TEMPORARY_REFERENCE_NAMESPACE_'が頭につくゴミが残ってしまうことがあるため残っていれば削除する
            # この対応はMaya2019でファイルリファレンス実行時にバグがあるための対応(2022では発生しない)
            temp_name = 'TEMPORARY_REFERENCE_NAMESPACE_' + ref_node[:-2]
            if cmds.namespace(ex=temp_name):
                cmds.namespace(rm=temp_name)

            if unload_hard:
                self.__clean_up_nodes(self.added_node_list)
                self.__clean_up_anim_layer()

            if not self.__namespace_exists(self.namespace):
                self.loaded = False
            else:
                self.__register_error('リファレンス解除時に不明なエラーが発生した')

            if self.is_temp_file:
                os.remove(self.file_path)

    def __clean_up_nodes(self, node_list):
        """
        与えられたノードのリストのうちシーンに残っているものの削除します。
        """

        if not node_list:
            return

        for target_node in node_list:
            if cmds.objExists(target_node):
                cmds.lockNode(target_node, l=False)
                cmds.delete(target_node)

    def __clean_up_anim_layer(self):
        """
        残っているAnimation Layerが1つでかつBaseAnimationの場合、BaseAnimationを削除する
        """

        current_anim_layer_list = cmds.ls(type='animLayer')
        if len(current_anim_layer_list) == 1 and current_anim_layer_list[0] == 'BaseAnimation':
            cmds.delete('BaseAnimation')

    def __register_error(self, reason):
        self.is_error = True
        self.reason = reason

    def __namespace_exists(self, target_namespace):
        return target_namespace in self.__get_all_namespace()

    def __get_all_namespace(self):

        reference_namespace_list = []
        reference_file_list = cmds.file(q=True, r=True)

        if reference_file_list:
            for ref_file in reference_file_list:
                reference_namespace = cmds.file(ref_file, q=True, ns=True)
                reference_namespace_list.append(reference_namespace)

        return reference_namespace_list

    def __generate_random_string(self, length):
        """ランダムな文字列を生成する

        Args:
            length (int): ランダム文字列の長さ

        Returns:
            str: ランダム文字列
        """
        random_str_list = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
        random_str = ''.join(random_str_list)
        return random_str
