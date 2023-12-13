# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
from . import glp_dag_obj_info

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(glp_dag_obj_info)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GlpDagCollector(object):

    # ===============================================
    def __init__(self):

        self.root_long_name = None
        self.dag_info_list = []
        self.dag_group_list = []

    # ===============================================
    def initialize(self, root_long_name):

        if not cmds.objExists(root_long_name):
            return

        self.root_long_name = root_long_name

        all_child_ordered_list = self.get_all_child(self.root_long_name, [self.root_long_name])

        if not all_child_ordered_list:
            return True

        for child in all_child_ordered_list:

            this_info = glp_dag_obj_info.GlpDagObjInfo()
            this_info.initialize(child, self.root_long_name)
            self.dag_info_list.append(this_info)

            this_group = self.get_group(this_info)
            if this_group:
                this_group.add_info(this_info)
            else:
                this_group = GlpDagObjGroup()
                this_group.create_group(this_info)
                self.dag_group_list.append(this_group)

        return True

    # ===============================================
    def get_all_child(self, root_long_name, result_list):

        children = cmds.listRelatives(root_long_name, c=True, f=True)

        if not children:
            return result_list

        for child in children:

            result_list.append(child)
            result_list = self.get_all_child(child, result_list)

        return result_list

    # ===============================================
    def get_group(self, glp_dag_obj_info):

        base_name = glp_dag_obj_info.base_name

        for group in self.dag_group_list:
            if group.base_name == base_name:
                # 違う階層、違うグループのjointのGroupの入るのを防止する
                if glp_dag_obj_info.long_name.find(group.top_joint_info.long_name) > -1:
                    return group

        return None


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GlpDagObjGroup(object):

    # ===============================================
    def __init__(self):

        self.member_info_list = None

        self.top_joint_info = None
        self.base_name = None
        self.parent_long_name = None
        self.depth = None
        self.depth_from_root = None
        self.type = None
        self.joint_parts_name = None

    # ===============================================
    def create_group(self, glp_dag_obj_info):

        self.member_info_list = []
        self.member_info_list.append(glp_dag_obj_info)
        self.update_info_from_member()

    # ===============================================
    def add_info(self, glp_dag_obj_info):

        self.member_info_list.append(glp_dag_obj_info)
        self.update_info_from_member()

    # ===============================================
    def update_info_from_member(self):

        if not self.member_info_list:
            return

        self.member_info_list = sorted(self.member_info_list, key=self.get_suffix_num)
        self.top_joint_info = self.member_info_list[0]
        self.base_name = self.top_joint_info.base_name
        self.parent = self.top_joint_info.parent_long_name
        self.depth = self.top_joint_info.depth
        self.depth_from_root = self.top_joint_info.depth_from_root
        self.type = self.top_joint_info.type
        self.joint_parts_name = self.top_joint_info.joint_parts_name

    def get_special_joint_prefix(self):
        """このグループの特殊ジョイント接頭辞を取得

        Returns:
            str: 接頭辞
        """
        return self.top_joint_info.get_special_joint_prefix()

    def has_special_joint_in_descendents(self):

        if not self.member_info_list:
            return False

        first_member_long_name = self.member_info_list[-1].long_name

        if not cmds.objExists(first_member_long_name):
            return False

        descendent_joint_list = \
            cmds.listRelatives(first_member_long_name, ad=True, type='joint', f=True)

        if not descendent_joint_list:
            return False

        has_special_joint = False

        for joint in descendent_joint_list:
            this_info = glp_dag_obj_info.GlpDagObjInfo()
            this_info.initialize(joint, self.top_joint_info.long_name)

            if this_info.special_joint_prefix:
                has_special_joint = True
                break

        return has_special_joint

    # ===============================================
    def get_suffix_num(self, glp_dag_obj_info):

        if glp_dag_obj_info.suffix_num:
            return glp_dag_obj_info.suffix_num
        else:
            return -1
