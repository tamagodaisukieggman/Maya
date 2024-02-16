# -*- coding: utf-8 -*-
"""
キャラインフォからオブジェクトを追加
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass
import maya.cmds as cmds

from ....glp_common.classes.info import chara_info


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AddCharaInfoObj(object):

    # ==================================================
    def __init__(self):
        """
        """

        self.chara_info = None

        self.is_ready = False

    # ==================================================
    def __initialize(self):
        """
        """

        self.is_ready = False

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info()
        if not self.chara_info.exists:
            return

        self.is_ready = True

    # ==================================================
    def add_obj(self, type_name, short_name):
        """
        """

        self.__initialize()

        if not self.is_ready:
            return

        target_info_list = None

        if type_name == 'joint':
            target_info_list = self.chara_info.part_info.joint_list
        elif type_name == 'locator':
            target_info_list = self.chara_info.part_info.locator_list

        if not target_info_list:
            return

        this_obj_path = self.__get_target_obj_path(target_info_list, short_name)

        # 既にあったら作成しない
        if not this_obj_path or cmds.objExists(this_obj_path):
            return

        this_parent_path = self.__get_parent_obj_path(this_obj_path)

        if not this_parent_path == '' and not cmds.objExists(this_parent_path):
            return

        new_obj = None

        if type_name == 'joint':
            new_obj = '|' + cmds.joint(n=short_name)
        elif type_name == 'locator':
            new_obj = '|' + cmds.spaceLocator(n=short_name)[0]

        if not new_obj:
            return

        if this_parent_path:
            return cmds.parent(new_obj, this_parent_path)[0]
        else:
            return new_obj

    # ==================================================
    def __get_target_obj_path(self, target_list, short_name):
        """
        """

        target_obj_path = ''

        for obj in target_list:

            if not obj.endswith(short_name):
                continue

            target_obj_path = obj
            break

        return target_obj_path

    # ==================================================
    def __get_parent_obj_path(self, long_name):
        """
        """

        if not long_name:
            return

        short_name = long_name.split('|')[-1]
        parent_path = long_name.replace('|{}'.format(short_name), '')

        return parent_path
