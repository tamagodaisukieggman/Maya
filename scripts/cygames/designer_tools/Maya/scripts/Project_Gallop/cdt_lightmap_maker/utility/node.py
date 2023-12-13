# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from . import name as utility_name
from . import list as utility_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ===============================================
    @staticmethod
    def exist_node(target_node, type=''):
        """ノードが存在するかどうか

        :param target_node: 対象となるノード
        :param type: タイプ
        """

        type_list = []

        if type != '':
            type_list = type.split(',')

        long_target_name = utility_name.Method.get_long_name(target_node)

        if long_target_name is None:
            return False

        if not cmds.objExists(long_target_name):
            return False

        if len(type_list) == 0:
            return True

        this_type = cmds.objectType(long_target_name)

        exist = False
        for temp_type in type_list:

            if temp_type == this_type:
                exist = True
                break

        if not exist:
            return False

        return True

    # ===============================================
    @staticmethod
    def search_node(
        target_node_name,
        filter='',
        type='transform'
    ):
        """ノード検索

        :param target_node_name: 対象となるノード名
        :param filter: フィルター
        :param type: タイプ
        """

        filter_list = []
        type_list = []

        if filter != '':
            filter_list = filter.split(',')

        if type != '':
            type_list = type.split(',')

        hit_name_list = cmds.ls(
            '*' + target_node_name, typ=type_list, l=True, r=True)

        if not utility_list.Method.exist_list(hit_name_list):
            return

        target_hit_name_list = []

        for hit_name in hit_name_list:

            exist = True
            for filter in filter_list:
                if hit_name.find(filter) < 0:
                    exist = False
                    break

            if not exist:
                continue

            target_hit_name_list.append(hit_name)

        if not utility_list.Method.exist_list(target_hit_name_list):
            return

        if len(target_hit_name_list) > 1:
            return

        return cmds.ls(target_hit_name_list[0], l=True, typ=type_list)[0]

    # ==================================================
    @staticmethod
    def exist_transform(target_transform):
        """トランスフォームが存在するかどうか

        :param target_transform: 対象となるトランスフォーム
        """

        return Method.exist_node(target_transform, 'transform')

    # ==================================================
    @staticmethod
    def get_mesh_shape(target_transform):
        """シェープノードを取得

        :param target_transform: 対象となるトランスフォーム
        """

        if not Method.exist_transform(target_transform):
            return

        long_target_name = utility_name.Method.get_long_name(target_transform)

        if long_target_name is None:
            return

        shapes = cmds.listRelatives(long_target_name, shapes=True, f=True)

        if not utility_list.Method.exist_list(shapes):
            return

        long_shape_name = utility_name.Method.get_long_name(shapes[0])

        if long_shape_name is None:
            return

        if cmds.objectType(long_shape_name) != 'mesh':
            return

        return long_shape_name

    # ==================================================
    @staticmethod
    def duplicate_node(target_node, duplicate_name=None):
        """
        ノード複製
        """

        if not Method.exist_node(target_node):
            return

        target_node_name = utility_name.Method.get_short_name(target_node)

        if duplicate_name is None:
            duplicate_name = target_node_name + "_copy"

        if Method.exist_node(duplicate_name):
            return

        target_shape_node = Method.get_mesh_shape(target_node)

        if target_shape_node is not None:

            target_shape_node_name = \
                utility_name.Method.get_short_name(target_shape_node)

            if target_node_name.lower() == target_shape_node_name.lower():
                cmds.rename(target_shape_node,
                            target_shape_node_name + 'Shape')

        duplicated_node = cmds.ls(cmds.duplicate(
            target_node, rr=True, name=duplicate_name), l=True)[0]

        return duplicated_node

    # ==================================================
    @staticmethod
    def get_target_list_from_set(target_set, target_node):

        if not NodeMethod.exist_node(target_set):
            return []

        if not NodeMethod.exist_node(target_node):
            return []

        member_list = cmds.sets(target_set, q=True)

        cmds.select(member_list, r=True)

        member_full_list = cmds.ls(member_list, l=True, fl=True)

        target_list = []

        for member in member_full_list:

            if member.find(target_node) < 0:
                continue

            target_list.append(member)

        return target_list

    # ==================================================
    @staticmethod
    def set_lock_transform(target_transform, lock):

        if not cmds.objExists(target_transform):
            return

        cmds.setAttr(target_transform + '.translateX', l=lock)
        cmds.setAttr(target_transform + '.translateY', l=lock)
        cmds.setAttr(target_transform + '.translateZ', l=lock)

        cmds.setAttr(target_transform + '.rotateX', l=lock)
        cmds.setAttr(target_transform + '.rotateY', l=lock)
        cmds.setAttr(target_transform + '.rotateZ', l=lock)

        cmds.setAttr(target_transform + '.scaleX', l=lock)
        cmds.setAttr(target_transform + '.scaleY', l=lock)
        cmds.setAttr(target_transform + '.scaleZ', l=lock)

    # ==================================================
    @staticmethod
    def get_vertex_index_list(target_transform):
        """頂点番号リストを取得

        :param target_transform: 対象となるトランスフォーム
        :return: 頂点番号の配列
        """

        if not Method.exist_transform(target_transform):
            return

        vertex_num = cmds.polyEvaluate(target_transform, v=True)

        vertex_index_list = []

        for p in range(vertex_num):

            vertex_index_list.append(p)

        return vertex_index_list

    # ==================================================
    @staticmethod
    def get_vertex_face_index_list(target_transform):
        """頂点フェース番号リストを取得

        :param target_transform: 対象となるトランスフォーム
        :return: [頂点番号,フェース番号]の配列
        """

        if not Method.exist_transform(target_transform):
            return

        vtxface_list = cmds.ls(
            (cmds.polyListComponentConversion(target_transform, tvf=True)),
            l=True,
            fl=True
        )

        vertex_face_index_list = []
        for p in range(len(vtxface_list)):

            this_vtxface = vtxface_list[p]

            vtx_and_face_index = \
                utility_name.Method.get_vertex_and_face_index(this_vtxface)

            vertex_face_index_list.append(
                [vtx_and_face_index[0], vtx_and_face_index[1]])

        vertex_face_index_list.sort()

        return vertex_face_index_list

    # ==================================================
    @staticmethod
    def get_uv_index_list(target_transform):
        """UV番号リストを取得

        :param target_transform: 対象となるトランスフォーム
        :return: UV番号の配列
        """

        if not Method.exist_transform(target_transform):
            return

        uv_list = cmds.ls(
            (cmds.polyListComponentConversion(target_transform, tuv=True)),
            l=True,
            fl=True
        )

        uv_index_list = []
        for p in range(len(uv_list)):

            this_uv = uv_list[p]

            uv_index = \
                utility_name.Method.get_uv_index(this_uv)

            uv_index_list.append(uv_index)

        uv_index_list.sort()

        return uv_index_list

    # ==================================================
    @staticmethod
    def get_uv_index_from_vertex_face(
            target_transform, vertex_index, face_index):

        this_vertex_face = \
            "{0}.vtxFace[{1}][{2}]".format(
                target_transform, vertex_index, face_index)

        uv_list = cmds.ls(
            (cmds.polyListComponentConversion(this_vertex_face, tuv=True)),
            l=True,
            fl=True
        )

        if not utility_list.Method.exist_list(uv_list):
            return -1

        this_uv = uv_list[0]

        uv_index = utility_name.Method.get_uv_index(this_uv)

        return uv_index

    # ==================================================
    @staticmethod
    def get_material_list(target_transform):
        """マテリアルリストを取得

        :param target_transform: 対象トランスフォーム
        """

        shape = Method.get_mesh_shape(target_transform)

        if shape is None:
            return

        shading_engine_list = cmds.listConnections(shape, type="shadingEngine")

        if not utility_list.Method.exist_list(shading_engine_list):
            return

        fix_shading_engine_list = []

        for shading_engine in shading_engine_list:

            exist = False
            for fix_shading_engine in fix_shading_engine_list:

                if shading_engine == fix_shading_engine:
                    exist = True

            if exist:
                continue

            fix_shading_engine_list.append(shading_engine)

        material_list = []

        for shading_engine in fix_shading_engine_list:

            this_material_list = cmds.listConnections(
                shading_engine + ".surfaceShader")

            if not utility_list.Method.exist_list(this_material_list):
                return

            material_list.extend(this_material_list)

        return material_list
