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

import re

import maya.cmds as cmds


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PolyInfo(object):

    # ==================================================
    def __init__(self, target_list=None):

        self.exists = False

        self.transform_list = None

        self.face_list = None
        self.vertex_list = None
        self.vertex_face_list = None

        self.face_with_vertex_dict = None
        self.face_with_vertex_face_dict = None

        self.vertex_with_vertex_face_dict = None
        self.vertex_with_face_dict = None

        self.vertex_face_with_vertex_dict = None
        self.vertex_face_with_face_dict = None

        self.create(target_list)

    # ==================================================
    def create(self, target_list):

        self.exists = False

        if not target_list:
            return

        vertex_face_list = \
            cmds.polyListComponentConversion(target_list, tvf=True)

        if not vertex_face_list:
            return

        vertex_face_list = \
            cmds.ls(vertex_face_list, fl=True, l=True)

        if not vertex_face_list:
            return

        # ------------------------------

        self.transform_list = []

        self.face_list = []
        self.vertex_list = []
        self.vertex_face_list = []

        self.face_with_vertex_dict = {}
        self.face_with_vertex_face_dict = {}

        self.vertex_with_vertex_face_dict = {}
        self.vertex_with_face_dict = {}

        self.vertex_face_with_vertex_dict = {}
        self.vertex_face_with_face_dict = {}

        # ------------------------------

        for vertex_face in vertex_face_list:

            this_split = vertex_face.split('.')

            this_transform = this_split[0]
            this_info = this_split[1]

            this_info_split = re.findall('\[\d+\]', this_info)

            this_vertex_index = this_info_split[0][1:-1]
            this_face_index = this_info_split[1][1:-1]

            this_face = '{0}.f[{1}]'.format(
                this_transform, this_face_index)

            this_vertex = '{0}.vtx[{1}]'.format(
                this_transform, this_vertex_index)

            # ------------------------------

            if this_transform not in self.transform_list:
                self.transform_list.append(this_transform)

            if this_face not in self.face_list:
                self.face_list.append(this_face)

            if this_vertex not in self.vertex_list:
                self.vertex_list.append(this_vertex)

            if vertex_face not in self.vertex_face_list:
                self.vertex_face_list.append(vertex_face)

            # ------------------------------

            if this_face not in self.face_with_vertex_dict:
                self.face_with_vertex_dict[this_face] = []

            if this_vertex not in self.face_with_vertex_dict[this_face]:
                self.face_with_vertex_dict[this_face].append(this_vertex)

            # ------------------------------

            if this_face not in self.face_with_vertex_face_dict:
                self.face_with_vertex_face_dict[this_face] = []

            if vertex_face not in self.face_with_vertex_face_dict[this_face]:
                self.face_with_vertex_face_dict[this_face].append(vertex_face)

            # ------------------------------

            if this_vertex not in self.vertex_with_face_dict:
                self.vertex_with_face_dict[this_vertex] = []

            if this_face not in self.vertex_with_face_dict[this_vertex]:
                self.vertex_with_face_dict[this_vertex].append(this_face)

            # ------------------------------

            if this_vertex not in self.vertex_with_vertex_face_dict:
                self.vertex_with_vertex_face_dict[this_vertex] = []

            if vertex_face not in self.vertex_with_vertex_face_dict[this_vertex]:
                self.vertex_with_vertex_face_dict[this_vertex].append(
                    vertex_face)

            # ------------------------------

            if vertex_face not in self.vertex_face_with_face_dict:
                self.vertex_face_with_face_dict[vertex_face] = []

            if this_face not in self.vertex_face_with_face_dict[vertex_face]:
                self.vertex_face_with_face_dict[vertex_face].append(this_face)

            # ------------------------------

            if vertex_face not in self.vertex_face_with_vertex_dict:
                self.vertex_face_with_vertex_dict[vertex_face] = []

            if this_vertex not in self.vertex_face_with_vertex_dict[vertex_face]:
                self.vertex_face_with_vertex_dict[vertex_face].append(
                    this_vertex)

        self.exists = True

    # ==================================================
    def get_face_list_from_vertex_list(self, vertex_list):

        if not vertex_list:
            return

        result_list = []

        for vertex in vertex_list:

            this_list = self.vertex_with_face_dict[vertex]

            if not this_list:
                continue

            result_list.extend(this_list)

        result_list = list(set(result_list))

        return result_list

    # ==================================================
    def get_vertex_list_from_face_list(self, face_list):

        if not face_list:
            return

        result_list = []

        for face in face_list:

            this_list = self.face_with_vertex_dict[face]

            if not this_list:
                continue

            result_list.extend(this_list)

        result_list = list(set(result_list))

        return result_list
