# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re

import maya.cmds as cmds

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GlpDagObjInfo(object):

    # ===============================================
    def __init__(self):

        self.__target_prefixes = ['Sp_', 'Ex_', 'Tp_', 'Pc_']

        self.root_long_name = None

        self.special_joint_prefix = ''
        self.long_name = None
        self.short_name = None
        self.base_name = None

        self.type = None
        self.depth = None
        self.depth_from_root = None

        self.parent_long_name = None

        self.base_name = None
        self.suffix_num = None
        self.joint_parts_name = None

    # ===============================================
    def initialize(self, long_name, root_long_name):

        self.root_long_name = root_long_name
        self.long_name = long_name

        if not cmds.objExists(self.long_name):
            return

        # ネームスペース対応
        self.short_name = self.long_name.split('|')[-1].split(':')[-1]

        self.type = cmds.objectType(self.long_name)
        self.depth = self.get_depth(self.long_name)
        self.depth_from_root = self.get_depth(self.long_name, self.root_long_name)
        self.parent_long_name = self.get_parent(self.long_name)

        self.special_joint_prefix = self.get_special_joint_prefix()

        if self.special_joint_prefix:
            self.base_name = self.get_no_number_name(self.short_name)
            self.suffix_num = self.get_suffix_number(self.short_name)
            self.joint_parts_name = self.get_part_name(self.short_name, 2)
        else:
            self.base_name = self.short_name

    # ===============================================
    def get_parent(self, long_name):

        if cmds.listRelatives(long_name, p=True):
            return cmds.listRelatives(long_name, p=True, f=True)[0]
        else:
            return None

    # ===============================================
    def get_depth(self, target_long_name, root_long_name=None):

        replaced_name = ''

        if target_long_name == root_long_name:
            return 0

        if root_long_name:
            replaced_name = target_long_name.replace(root_long_name + '|', '')
        else:
            replaced_name = re.sub('^\|', '', target_long_name)

        return len(replaced_name.split('|'))

    # ===============================================
    def get_no_number_name(self, short_name):

        if not short_name:
            return

        suffix = short_name.split('_')[-1]

        try:
            int(suffix)
            return short_name.replace('_' + suffix, '')
        except Exception:
            return short_name

    # ===============================================
    def get_suffix_number(self, short_name):

        if not short_name:
            return

        suffix = short_name.split('_')[-1]

        try:
            return int(suffix)
        except Exception:
            return None

    # ===============================================
    def get_part_name(self, short_name, target_index, elm_separator='_'):

        elm_list = short_name.split(elm_separator)

        if len(elm_list) < target_index + 1:
            return
        else:
            return elm_list[target_index]

    def get_special_joint_prefix(self):
        """特殊骨の接頭辞を取得

        Args:
            long_name (str): ロングネーム

        Returns:
            str: 接頭辞
        """

        if not cmds.objExists(self.long_name):
            return ''

        if not cmds.objectType(self.long_name, isType='joint'):
            return ''

        for target_prefix in self.__target_prefixes:
            if self.has_prefix(self.short_name, target_prefix):
                return target_prefix

        return ''

    # ===============================================
    def has_prefix(self, target_name, prefix):

        if not target_name or not prefix:
            return False

        if target_name.startswith(prefix):
            return True
        else:
            return False
