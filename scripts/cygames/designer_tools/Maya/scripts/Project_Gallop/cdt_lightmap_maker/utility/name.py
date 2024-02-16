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

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ==================================================
    @staticmethod
    def get_short_name(name):
        """ショート名取得

        :param name: 対象となる名前
        """

        if name.find('|') == -1:
            return name

        split_string = name.split('|')

        return split_string[-1]

    # ==================================================
    @staticmethod
    def get_long_name(name):
        """ロング名取得

        :param name: 対象となる名前
        """

        long_name_list = cmds.ls(name, l=True)

        if long_name_list is None:
            return

        if len(long_name_list) == 0:
            return

        if len(long_name_list) != 1:
            return

        return long_name_list[0]

    # ==================================================
    @staticmethod
    def get_transform_from_vertex(vertex):
        """トランスフォーム名を頂点名などから取得

        :param vertex_face: 対象となる頂点など
        """

        transform_name = vertex.split('.')[0]

        return transform_name

    # ==================================================
    @staticmethod
    def get_vertex_index(vertex):
        """頂点番号を取得

        :param vertex_face: 対象となる頂点
        """

        start_index = vertex.find('[') + 1
        end_index = vertex.find(']')

        return int(vertex[start_index:end_index])

    # ==================================================
    @staticmethod
    def get_vertex_and_face_index(vertex_face):
        """頂点フェース番号を取得

        :param vertex_face: 対象となる頂点フェース
        """

        vtx_face_string = vertex_face.split('.')[-1]

        vtx_face_string = vtx_face_string.replace('vtxFace[', '')
        vtx_face_string = vtx_face_string.replace(']', '')

        split_string = vtx_face_string.split('[')

        vertex_index = split_string[0]
        face_index = split_string[1]

        return [int(vertex_index), int(face_index)]

    # ==================================================
    @staticmethod
    def get_uv_index(uv):
        """UV番号を取得

        :param uv: 対象となるUV
        """

        start_index = uv.find('[') + 1
        end_index = uv.find(']')

        return int(uv[start_index:end_index])
