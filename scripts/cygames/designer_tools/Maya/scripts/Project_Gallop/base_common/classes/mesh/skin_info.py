# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from ... import utility as base_utility


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SkinInfo(object):

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

            new_info_item = SkinInfoItem(self, target_transform)

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

            if base_utility.mesh.skin.get_skin_cluster(temp_transform) is None:
                continue

            if base_utility.mesh.skin.get_skin_root_joint(temp_transform) is None:
                continue

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

    # ==================================================s
    def write_info_to_xml(self, xml_file_path):

        if not self.info_item_list:
            return

        root_element = base_utility.xml.create_element('SkinInfo', None)

        vertex_root_element = base_utility.xml.add_element(
            root_element, 'TargetVertexList', None)

        base_utility.xml.add_element_from_list(
            vertex_root_element, 'Vertex', self.target_vertex_list
        )

        transform_root_element = base_utility.xml.add_element(
            root_element, 'TargetTransformList', None)

        base_utility.xml.add_element_from_list(
            transform_root_element, 'Transform', self.target_transform_list
        )

        for info_item in self.info_item_list:
            info_item._write_info_to_xml_element(root_element)

        base_utility.xml.write(xml_file_path, root_element)

    # ==================================================s
    def create_info_from_xml(self, xml_file_path):

        root_element = base_utility.xml.read(xml_file_path)

        if root_element is None:
            return

        # 対象頂点
        self.target_vertex_list = []

        vertex_root_element = base_utility.xml.search_element(
            root_element, 'TargetVertexList')

        vertex_element_list = base_utility.xml.search_element_list(
            vertex_root_element, 'Vertex')

        if vertex_element_list:

            for vertex_element in vertex_element_list:

                self.target_vertex_list.append(vertex_element.text)

        if not self.target_vertex_list:
            return

        # 対象トランスフォーム
        self.target_transform_list = []

        transform_root_element = base_utility.xml.search_element(
            root_element, 'TargetTransformList')

        transform_element_list = base_utility.xml.search_element_list(
            transform_root_element, 'Transform')

        if transform_element_list:

            for transform_element in transform_element_list:

                self.target_transform_list.append(transform_element.text)

        if not self.target_transform_list:
            return

        # SkinInfoItem読み込み
        item_element_list = base_utility.xml.search_element_list(
            root_element, 'SkinInfoItem')

        if not item_element_list:
            return

        self.info_item_list = []

        for item_element in item_element_list:

            new_info_item = SkinInfoItem(self, None)

            new_info_item._create_info_from_xml_element(item_element)

            self.info_item_list.append(new_info_item)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SkinInfoItem(object):

    # ==================================================
    def __init__(self, root_info, target_transform):

        self.root_info = root_info

        self.target_transform = target_transform
        self.target_transform_name = None

        self.world_vertex_position_info_list = None
        self.local_vertex_position_info_list = None

        self.uv_info_list = None

        self.joint_list = None
        self.joint_name_list = None
        self.joint_name_dict = None

        self.joint_weight_info_list = None

        self.target_vertex_list = None
        self.target_vertex_index_list = None

    # ==================================================
    def _update_info(self):

        self.__fix_transform_name()

        self.world_vertex_position_info_list = \
            base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
                self.target_transform, True)

        self.local_vertex_position_info_list = \
            base_utility.mesh.vertex_position.get_all_vertex_position_info_list(
                self.target_transform, False)

        self.joint_list = base_utility.mesh.skin.get_skin_joint_list(
            self.target_transform)

        self.__fix_joint_list()

        self.joint_weight_info_list = \
            base_utility.mesh.skin.get_all_joint_weight_info_list(
                self.target_transform)

        self.__fix_target_vertex_list()

    # ==================================================
    def _update_uv_info(self):

        self.uv_info_list = \
            base_utility.mesh.uv.get_all_uv_info_list_with_vertex_index(
                self.target_transform
            )

    # ==================================================
    def _write_info_to_xml_element(self, parent_element):

        if parent_element is None:
            return

        root_element = base_utility.xml.add_element(
            parent_element, 'SkinInfoItem', None)

        base_utility.xml.add_element(
            root_element, 'TargetTransform', self.target_transform)

        base_utility.mesh.vertex_position.write_info_list_to_xml_element(
            root_element, self.world_vertex_position_info_list, True
        )

        base_utility.mesh.vertex_position.write_info_list_to_xml_element(
            root_element, self.local_vertex_position_info_list, False
        )

        base_utility.mesh.skin.write_info_list_to_xml_element(
            root_element, self.joint_weight_info_list
        )

        joint_root_element = base_utility.xml.add_element(
            root_element, 'JointList', None)

        base_utility.xml.add_element_from_list(
            joint_root_element, 'Joint', self.joint_list
        )

        if self.uv_info_list:

            base_utility.mesh.uv.write_info_list_to_xml_element(
                root_element, self.uv_info_list
            )

    # ==================================================
    def _create_info_from_xml_element(self, parent_element):

        # 対象トランスフォーム
        target_transform_element = base_utility.xml.search_element(
            parent_element, 'TargetTransform')

        if target_transform_element is not None:
            self.target_transform = target_transform_element.text

        if not self.target_transform:
            return

        self.__fix_transform_name()

        # ジョイントリスト
        self.joint_list = []

        joint_root_element = base_utility.xml.search_element(
            parent_element, 'JointList')

        joint_element_list = base_utility.xml.search_element_list(
            joint_root_element, 'Joint')

        if joint_element_list:

            for joint_element in joint_element_list:

                self.joint_list.append(joint_element.text)

        if not self.joint_list:
            return

        self.__fix_joint_list()

        # 対象頂点

        self.__fix_target_vertex_list()

        # 頂点位置
        self.world_vertex_position_info_list =\
            base_utility.mesh.vertex_position.read_info_list_from_xml_element(
                parent_element, True
            )

        self.local_vertex_position_info_list =\
            base_utility.mesh.vertex_position.read_info_list_from_xml_element(
                parent_element, False
            )

        # ウェイト情報
        self.joint_weight_info_list = \
            base_utility.mesh.skin.read_info_list_from_xml_element(
                parent_element
            )

        # UV情報
        self.uv_info_list = \
            base_utility.mesh.uv.read_info_list_from_xml_element(
                parent_element
            )

    # ==================================================
    def __fix_transform_name(self):

        self.target_transform_name = \
            base_utility.name.get_short_name(self.target_transform)

        self.target_transform_name = \
            base_utility.namespace.get_nonamespace_name(
                self.target_transform_name)

    # ==================================================
    def __fix_joint_list(self):

        self.joint_name_list = []
        self.joint_name_dict = {}

        for joint in self.joint_list:

            joint_name = \
                base_utility.name.get_short_name(joint)

            joint_name = \
                base_utility.namespace.get_nonamespace_name(joint_name)

            self.joint_name_list.append(joint_name)

            if joint_name not in self.joint_name_dict:
                self.joint_name_dict[joint_name] = [joint]
                continue

            self.joint_name_dict[joint_name].append(joint)

    # ==================================================
    def __fix_target_vertex_list(self):

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
