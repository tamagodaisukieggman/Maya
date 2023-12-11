# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import maya.cmds as cmds

from ... import utility as base_utility


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VertexPositionInfo(object):

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

            new_info_item = VertexPositionInfoItem(self, target_transform)

            self.info_item_list.append(new_info_item)

        if not self.info_item_list:
            return
        
        self.update_info()

    # ==================================================
    def __create_target_vertex_list(self, target_list):

        self.target_vertex_list = []
        self.target_transform_list = []

        if not target_list:
            return
        
        vertex_list = cmds.ls(
            (cmds.polyListComponentConversion(target_list, tv=True)), l=True, fl=True)

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

    # ==================================================s
    def update_uv_info(self):

        if self.info_item_list is None:
            return

        for info_item in self.info_item_list:
            info_item._update_uv_info()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VertexPositionInfoItem(object):

    # ==================================================
    def __init__(self, root_info, target_transform):

        self.root_info = root_info

        self.target_transform = target_transform
        self.target_transform_name = None

        self.world_vertex_position_info_list = None
        self.local_vertex_position_info_list = None

        self.uv_info_list = None

        self.target_vertex_list = None
        self.target_vertex_index_list = None

    # ==================================================
    def _update_info(self):

        self.target_transform_name = self.target_transform.split('|')[-1]

        self.target_transform_name = \
            base_utility.namespace.get_nonamespace_name(
                self.target_transform_name)

        self.world_vertex_position_info_list = \
            base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
                self.target_transform, True)

        self.local_vertex_position_info_list = \
            base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
                self.target_transform, False)

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

    # ==================================================
    def _update_uv_info(self):

        self.uv_info_list = \
            base_utility.mesh.uv.get_all_uv_info_list_with_vertex_index(
                self.target_transform
            )
