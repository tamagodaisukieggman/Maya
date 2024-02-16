# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NormalInfo(object):

    # ==================================================
    def __init__(self):

        self.target_vertex_list = None
        self.target_transform_list = None

        self.info_item_list = None

    # ==================================================
    def create_info(self, target_list):

        self.__create_target_vertex_list(target_list)

        if not self.target_transform_list:
            return

        if not self.target_vertex_list:
            return

        self.info_item_list = []

        for target_transform in self.target_transform_list:

            new_info_item = NormalInfoItem(self, target_transform)

            self.info_item_list.append(new_info_item)

        if not self.info_item_list:
            return

        self.update_info()

    # ==================================================
    def __create_target_vertex_list(self, target_list):

        if not target_list:
            return

        vertex_list = []
        for target in target_list:

            if target.find('.vtx[') >= 0:
                vertex_list.append(target)
            else:
                this_vertex_list = cmds.ls(
                    (cmds.polyListComponentConversion(target, tv=True)), l=True, fl=True)
                if this_vertex_list:
                    vertex_list.extend(this_vertex_list)

        if not vertex_list:
            return

        temp_transform_list = []

        for vertex in vertex_list:

            this_transform = \
                base_utility.mesh.get_transform_from_vertex(vertex)

            if this_transform is None:
                continue

            if this_transform in temp_transform_list:
                continue

            temp_transform_list.append(this_transform)

        if not temp_transform_list:
            return

        self.target_transform_list = []

        for temp_transform in temp_transform_list:

            self.target_transform_list.append(temp_transform)

        if not self.target_transform_list:
            return

        self.target_vertex_list = []

        for vertex in vertex_list:

            exist = False
            for target_transform in self.target_transform_list:

                if vertex.find(target_transform) < 0:
                    continue

                exist = True
                break

            if not exist:
                continue

            self.target_vertex_list.append(vertex)

    # ==================================================
    def update_info(self):

        if self.info_item_list is None:
            return

        for info_item in self.info_item_list:

            info_item._update_info()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NormalInfoItem:

    # ==================================================
    def __init__(self, root_info, target_transform):

        self.root_info = root_info

        self.target_transform = target_transform

        self.target_transform_name = None

        self.world_vertex_position_info_list = None
        self.local_vertex_position_info_list = None

        self.normal_info_list = None
        self.fix_normal_info_list = None

        self.target_vertex_list = None
        self.target_vertex_index_list = None

    # ==================================================
    def _update_info(self):

        self.target_transform_name = \
            base_utility.name.get_short_name(self.target_transform)

        self.world_vertex_position_info_list = \
            base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
                self.target_transform, True)

        self.local_vertex_position_info_list = \
            base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
                self.target_transform, False)

        self.normal_info_list = \
            base_utility.mesh.normal.get_all_normal_info_list(
                self.target_transform)

        vertex_count = cmds.polyEvaluate(self.target_transform, v=True)

        self.fix_normal_info_list = [None] * vertex_count

        for this_info in self.normal_info_list:

            this_vertex_index = this_info[0]

            if self.fix_normal_info_list[this_vertex_index] is None:

                self.fix_normal_info_list[this_vertex_index] = [this_info]

            else:

                self.fix_normal_info_list[this_vertex_index].append(this_info)

        self.target_vertex_list = []
        self.target_vertex_index_list = []

        for target_vertex in self.root_info.target_vertex_list:

            this_transform = \
                base_utility.mesh.get_transform_from_vertex(target_vertex)

            if this_transform != self.target_transform:
                continue

            this_vertex_index = \
                base_utility.mesh.get_vertex_index(target_vertex)

            self.target_vertex_list.append(target_vertex)
            self.target_vertex_index_list.append(this_vertex_index)
