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

import os
import shutil

import maya.cmds as cmds
import maya.mel as mel

from . import list as utility_list
from . import node as utility_node


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ==================================================
    @staticmethod
    def exist_set(target_set):
        """セットが存在するかどうか
        """

        set_list = cmds.ls(type='objectSet')

        if not utility_list.Method.exist_list(set_list):
            return False

        for set in set_list:

            if set == target_set:
                return True

        return False

    # ==================================================
    @staticmethod
    def create_new_set(set_name):
        """新しいセットを作成
        """

        if Method.exist_set(set_name):
            return

        cmds.select(cl=True)

        cmds.sets(name=set_name)

    # ==================================================
    @staticmethod
    def delete_set(target_set):
        """セットを削除
        """

        if not Method.exist_set(target_set):
            return

        cmds.delete(target_set)

    # ==================================================
    @staticmethod
    def add_member_to_set(target_set, target_member_list):
        """セットにノードを登録
        """

        if not Method.exist_set(target_set):
            return

        if not utility_list.Method.exist_list(target_member_list):
            return

        fix_member_list = []
        for node in target_member_list:

            if not utility_node.Method.exist_node(node):
                continue

            fix_member_list.append(node)

        cmds.sets(fix_member_list, add=target_set)

    # ==================================================
    @staticmethod
    def remove_member_from_set(target_set, target_member_list):
        """セットからノードを除去
        """

        if not Method.exist_set(target_set):
            return

        if not utility_list.Method.exist_list(target_member_list):
            return

        fix_member_list = []
        for node in target_member_list:

            if not utility_node.Method.exist_node(node):
                continue

            fix_member_list.append(node)

        cmds.sets(fix_member_list, remove=target_set)

    # ==================================================
    @staticmethod
    def get_member_list_from_set(target_set):
        """セットからメンバーリストを取得
        """

        if not Method.exist_set(target_set):
            return

        member_list = cmds.sets(target_set, q=True)

        if not utility_list.Method.exist_list(member_list):
            return

        return member_list

    # ==================================================
    @staticmethod
    def clear_member_from_set(target_set):
        """セットからメンバーをクリア
        """

        member_list = Method.get_member_list_from_set(target_set)

        if not utility_list.Method.exist_list(member_list):
            return

        Method.remove_member_from_set(target_set, member_list)
