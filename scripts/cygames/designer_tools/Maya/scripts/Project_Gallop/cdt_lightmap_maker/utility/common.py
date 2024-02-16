# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

import maya.OpenMaya as om_old
import maya.OpenMayaAnim as omanim_old

import maya.api.OpenMaya as om

import math
from math import modf
import os
import re

import subprocess

from . import attribute


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StringMethod(object):

    # ===============================================
    @staticmethod
    def get_string_by_regex(target_string, pattern):
        """
        正規表現で文字列取得
        """

        match_obj = \
            re.search(pattern, target_string)

        if match_obj is None:
            return ''

        return match_obj.group()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NameMethod(object):

    # ===============================================
    @staticmethod
    def get_short_name(name):
        """
        ショート名を取得
        """

        if name.find('|') < 0:
            return name

        return name.split('|')[-1]

    # ===============================================
    @staticmethod
    def get_long_name(name):
        """
        ロング名を取得
        """

        long_name_list = cmds.ls(name, l=True)

        if long_name_list is None:
            return

        if len(long_name_list) == 0:
            return

        if len(long_name_list) != 1:
            return

        return long_name_list[0]

    # ===============================================
    @staticmethod
    def get_vertex_and_face_index(vertex_face):
        """
        頂点フェース番号を取得
        """

        vtx_face_string = vertex_face.split('.')[-1]

        vtx_face_string = vtx_face_string.replace('vtxFace[', '')
        vtx_face_string = vtx_face_string.replace(']', '')

        split_string = vtx_face_string.split('[')

        vertex_index = split_string[0]
        face_index = split_string[1]

        return [int(vertex_index), int(face_index)]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ListMethod(object):

    # ===============================================
    @staticmethod
    def exist_list(target_list):
        """
        リストが存在するかどうか
        """

        if target_list is None:
            return False

        if type(target_list) != list:
            return False

        if len(target_list) == 0:
            return False

        return True


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NodeMethod(object):

    # ===============================================
    @staticmethod
    def exist_node(target_node, type_list=[]):
        """
        ノードが存在するかどうか
        """

        long_target_name = NameMethod.get_long_name(target_node)

        if long_target_name is None:
            return

        if not cmds.objExists(long_target_name):
            return False

        if len(type_list) > 0:

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
    def exist_transform(target_transform):
        """
        トランスフォームが存在するかどうか
        """

        long_target_name = NameMethod.get_long_name(target_transform)

        if long_target_name is None:
            return

        if not cmds.objExists(long_target_name):
            return False

        this_type = cmds.objectType(long_target_name)

        if this_type != 'transform':
            return False

        return True

    # ===============================================
    @staticmethod
    def get_mesh_shape(target_transform):
        """
        シェープノード取得
        """

        if not NodeMethod.exist_transform(target_transform):
            return

        long_target_name = NameMethod.get_long_name(target_transform)

        if long_target_name is None:
            return

        shapes = cmds.listRelatives(long_target_name, shapes=True, f=True)

        if not ListMethod.exist_list(shapes):
            return

        long_shape_name = NameMethod.get_long_name(shapes[0])

        if long_shape_name is None:
            return

        if cmds.objectType(long_shape_name) != 'mesh':
            return

        return long_shape_name

    # ===============================================
    @staticmethod
    def create_group(name, parent):

        if NodeMethod.exist_node(name):
            return

        new_group = cmds.group(name=name, em=True)

        if new_group is None:
            return

        if parent is None:
            return

        NodeMethod.parent_object(new_group, parent)

    # ===============================================
    @staticmethod
    def parent_object(target, parent):

        if not cmds.objExists(target):
            return

        if not cmds.objExists(parent):
            return

        cmds.parent(target, parent)

    # ===============================================
    @staticmethod
    def get_selected_shape_transform_list():

        cmds.select(hi=True)

        select_list = cmds.ls(sl=True, type="transform", l=True)

        if select_list is None:
            return []

        if len(select_list) == 0:
            return []

        result_list = []

        for select in select_list:

            if NodeMethod.get_mesh_shape(select) is None:
                continue

            result_list.append(select)

        return result_list

    # ===========================================
    @staticmethod
    def get_material_list(target):

        shape = NodeMethod.get_mesh_shape(target)

        if shape is None:
            return

        shading_engine_list = cmds.listConnections(shape, type="shadingEngine")

        if shading_engine_list is None:
            return

        if len(shading_engine_list) == 0:
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

            this_material_list =\
                cmds.listConnections(shading_engine + ".surfaceShader")

            if this_material_list is None:
                continue

            if len(this_material_list) == 0:
                continue

            material_list.extend(this_material_list)

        return material_list

    # ===========================================
    @staticmethod
    def turn_off_hardware_texture(target_material):

        if not cmds.objExists(target_material):
            return

        if not cmds.objectType(target_material, isa="lambert"):
            return

        if not attribute.Method.exist_attr(target_material, "materialInfo"):
            return

        material_info_list = cmds.listConnections(
            target_material, t="materialInfo")

        if material_info_list is None:
            return

        for mat_info in material_info_list:

            if not attribute.Method.exist_attr(mat_info, "texture"):
                continue

            this_connect_list = cmds.listConnections(
                mat_info + ".texture", p=True)

            if this_connect_list is None:
                continue

            if len(this_connect_list) == 0:
                continue

            if not cmds.isConnected(
                    this_connect_list[0], mat_info + ".texture[0]"):
                continue

            cmds.disconnectAttr(this_connect_list[0], mat_info + ".texture[0]")

    # ===========================================
    @staticmethod
    def connect_place2d_to_file(place2d_node, file_node):

        if not cmds.objExists(place2d_node):
            return

        if not cmds.objExists(file_node):
            return

        place2d_attr_list = ["outUV",
                             "outUvFilterSize",
                             "coverage",
                             "translateFrame",
                             "rotateFrame",
                             "mirrorU",
                             "mirrorV",
                             "stagger",
                             "wrapU",
                             "wrapV",
                             "repeatUV",
                             "vertexUvOne",
                             "vertexUvTwo",
                             "vertexUvThree",
                             "vertexCameraOne",
                             "noiseUV",
                             "offset",
                             "rotateUV"]

        file_attr_list = ["uvCoord",
                          "uvFilterSize",
                          "coverage",
                          "translateFrame",
                          "rotateFrame",
                          "mirrorU",
                          "mirrorV",
                          "stagger",
                          "wrapU",
                          "wrapV",
                          "repeatUV",
                          "vertexUvOne",
                          "vertexUvTwo",
                          "vertexUvThree",
                          "vertexCameraOne",
                          "noiseUV",
                          "offset",
                          "rotateUV"]

        if len(file_attr_list) != len(place2d_attr_list):
            return

        for cnt in range(0, len(place2d_attr_list)):

            attribute.Method.connect_attr(
                place2d_node,
                place2d_attr_list[cnt],
                file_node,
                file_attr_list[cnt])

    # ===========================================
    @staticmethod
    def connect_chooser_to_place2d(chooser_node, place2d_node):

        if not cmds.objExists(chooser_node):
            return

        if not cmds.objExists(place2d_node):
            return

        chooser_attr_list = ["outVertexCameraOne",
                             "outVertexUvThree",
                             "outVertexUvTwo",
                             "outVertexUvOne",
                             "outUv"]

        place2d_attr_list = ["vertexCameraOne",
                             "vertexUvThree",
                             "vertexUvTwo",
                             "vertexUvOne",
                             "uvCoord"]

        if len(chooser_attr_list) != len(place2d_attr_list):
            return

        for cnt in range(0, len(chooser_attr_list)):

            attribute.Method.connect_attr(
                chooser_node,
                chooser_attr_list[cnt],
                place2d_node,
                place2d_attr_list[cnt])


class OmMethod(object):

    # ===============================================
    @staticmethod
    def get_om_dag_path(target_node):

        if not NodeMethod.exist_node(target_node):
            return

        om_select_list = om.MSelectionList()
        om_select_list.add(target_node)

        om_dag_path = om_select_list.getDagPath(0)

        return om_dag_path

    # ===============================================
    @staticmethod
    def get_om_object(target_node):

        if not NodeMethod.exist_node(target_node):
            return

        om_select_list = om.MSelectionList()
        om_select_list.add(target_node)

        om_object = om_select_list.getDependNode(0)

        return om_object

    # ===============================================
    @staticmethod
    def get_om_mesh(target_transform):

        om_dag_path = OmMethod.get_om_dag_path(target_transform)

        if om_dag_path is None:
            return

        om_mesh = om.MFnMesh(om_dag_path)

        return om_mesh

    # ===============================================
    @staticmethod
    def get_om_color(color):

        om_color = om.MColor()

        om_color.r = color[0]
        om_color.g = color[1]
        om_color.b = color[2]
        om_color.a = color[3]

        return om_color

    # ===============================================
    @staticmethod
    def get_color(om_color):

        return [om_color.r, om_color.g, om_color.b, om_color.a]

    # ===============================================
    @staticmethod
    def set_om_color_to_color_list(om_color, dst_color):

        dst_color[0] = om_color.r
        dst_color[1] = om_color.g
        dst_color[2] = om_color.b
        dst_color[3] = om_color.a

    # ===============================================
    @staticmethod
    def get_om_vector(vector):

        om_vector = om.MVector()

        om_vector.x = vector[0]
        om_vector.y = vector[1]
        om_vector.z = vector[2]

        return om_vector

    # ===============================================
    @staticmethod
    def get_vector(om_vector):

        vector = [0] * 3

        vector[0] = om_vector.x
        vector[1] = om_vector.y
        vector[2] = om_vector.z

        return vector


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IOMethod(object):

    # ===============================================
    @staticmethod
    def open_directory(target_path):
        """
        ディレクトリを開く
        """

        if target_path is None:
            return

        target_dir_path = None

        target_path == target_path.replace('\\', '/')

        if os.path.isfile(target_path):
            target_dir_path = os.path.dirname(target_path)

        elif os.path.isdir(target_path):
            target_dir_path = target_path

        if target_dir_path is None:
            return

        target_dir_path = target_dir_path.replace('/', '\\')
        subprocess.Popen('explorer "' + target_dir_path + '"')

    # ===============================================
    @staticmethod
    def open_notepad(target_file_path):
        """
        ノートパッドでファイルを開く
        """
        if not os.path.isfile(target_file_path):
            return

        subprocess.Popen('notepad "' + target_file_path + '"')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OtherMethod(object):

    # ===============================================
    @staticmethod
    def execute_mel(command):

        try:
            mel.eval(command)

        except Exception:
            print("cannot execute mel : " + command)

    # ===============================================
    @staticmethod
    def reset_display_mode_for_lightmap(target):

        this_shape = NodeMethod.get_mesh_shape(target)

        if this_shape is None:
            return

        cmds.setAttr(this_shape + ".displayColors", 1)
        cmds.setAttr(this_shape + ".displayColorChannel",
                     "Ambient+Diffuse", type="string")
        cmds.setAttr(this_shape + ".materialBlend", 6)

    # ===============================================
    @staticmethod
    def reset_display_mode(target):

        this_shape = NodeMethod.get_mesh_shape(target)

        if this_shape is None:
            return

        cmds.setAttr(this_shape + ".displayColors", 1)
        cmds.setAttr(this_shape + ".displayColorChannel",
                     "Ambient+Diffuse", type="string")
        cmds.setAttr(this_shape + ".materialBlend", 3)

    # ===============================================
    @staticmethod
    def reset_vtxcolor_for_lightmap(target):

        this_shape = NodeMethod.get_mesh_shape(target)

        if this_shape is None:
            return

        cmds.polyColorPerVertex(target, r=0.5, g=0.5, b=0.5)
