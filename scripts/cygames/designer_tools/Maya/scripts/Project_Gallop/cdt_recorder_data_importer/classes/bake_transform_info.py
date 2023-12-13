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

import re

import maya.cmds as cmds

from .. import common

from . import bake_key_info


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeTransformInfo(object):

    # ==================================================
    def __init__(self, parent):

        self.exists = False

        self.parent = parent

        self.transform_name = None
        self.parent_transform_name = None

        self.is_camera = False

        self.key_info_list = None

        self.target_transform = None

        self.trans_scale_transform = None

        self.rotate_transform = None
        self.forward_transform = None
        self.up_transform = None
        self.camera_transform = None

        self.is_bake_translate = False
        self.is_bake_rotate = False
        self.is_bake_scale = False

    # ==================================================
    def read_xml(self, parent_element):

        self.exists = False

        self.transform_name = parent_element.attrib['Name']
        self.parent_transform_name = parent_element.attrib['Parent']

        self.__search_target_transform()

        if self.target_transform is None:
            return

        if parent_element.attrib['IsCamera'] == 'true' and\
                cmds.listRelatives(self.target_transform, type='camera'):
            self.is_camera = True

        self.__read_xml_for_key_info_list(parent_element)

        if not self.key_info_list:
            return

        self.exists = True

    # ==================================================
    def __search_target_transform(self):

        self.target_transform = None

        if self.transform_name not in self.parent.target_transform_dict:
            return

        target_transform_list = self.parent.target_transform_dict[self.transform_name]

        if not target_transform_list:
            return

        if len(target_transform_list) > 1:
            return

        self.target_transform = target_transform_list[0]

    # ==================================================
    def __read_xml_for_key_info_list(self, parent_element):

        self.key_info_list = []

        key_info_list_element = parent_element.find('KeyInfoList')

        if key_info_list_element is None:
            return

        key_info_element_list = list(key_info_list_element)

        if not key_info_element_list:
            return

        for p in range(0, len(self.parent.time_list)):

            key_info_element = key_info_element_list[self.parent.time_start_index + p]

            new_key_info = bake_key_info.BakeKeyInfo(self)
            new_key_info.read_xml(key_info_element)

            if not new_key_info.exists:
                continue

            self.key_info_list.append(new_key_info)

    # ==================================================
    def initialize_for_bake(self):

        if not self.exists:
            return

        self.__check_filter()
        self.__create_temp_transform()

        for key_info in self.key_info_list:
            key_info.initialize_for_bake()

    # ==================================================
    def __create_temp_transform(self):

        self.trans_scale_transform = self.target_transform + '_trans_scale'
        self.trans_scale_transform = \
            self.trans_scale_transform.replace('|', '_')

        self.rotate_transform = self.target_transform + '_rotate'
        self.rotate_transform = self.rotate_transform.replace('|', '_')

        self.forward_transform = self.target_transform + "_foward"
        self.forward_transform = self.forward_transform.replace('|', '_')

        self.up_transform = self.target_transform + "_up"
        self.up_transform = self.up_transform.replace('|', '_')

        self.camera_transform = self.target_transform + '_camera'
        self.camera_transform = \
            self.camera_transform.replace('|', '_')

        common.utility.maya.base.node.delete_node(
            [self.trans_scale_transform, self.rotate_transform, self.forward_transform, self.up_transform, self.camera_transform])

        self.trans_scale_transform = \
            cmds.spaceLocator(n=self.trans_scale_transform)[0]

        self.rotate_transform = cmds.spaceLocator(n=self.rotate_transform)[0]
        self.forward_transform = cmds.spaceLocator(n=self.forward_transform)[0]
        self.up_transform = cmds.spaceLocator(n=self.up_transform)[0]

        if self.is_camera:

            self.camera_transform = cmds.camera(n=self.camera_transform)[0]

            cmds.camera(self.target_transform, e=True, ff='vertical')
            vfa = cmds.camera(self.target_transform, q=True, vfa=True)
            cmds.camera(self.camera_transform, e=True, vfa=vfa, ff='vertical')

        aim_vector = [0, 0, 1]

        # 詳細は不明だがUnityのカメラを持ってくるとフォーワードが反転してしまっている
        if self.is_camera:
            aim_vector = [0, 0, -1]

        cmds.aimConstraint(self.forward_transform, self.rotate_transform,
                           aimVector=aim_vector, worldUpType="object", worldUpObject=self.up_transform)

    # ==================================================
    def __check_filter(self):

        self.is_bake_translate = True
        self.is_bake_rotate = True
        self.is_bake_scale = True

        if not self.parent.transform_filter_list:
            return

        hit_index = -1

        count = -1
        for transform_filter in self.parent.transform_filter_list:
            count += 1

            if not transform_filter:
                continue

            if re.search(transform_filter, self.transform_name):
                hit_index = count
                break

        if hit_index < 0:
            return

        attr_filter = self.parent.attr_filter_list[hit_index]

        self.is_bake_translate = False
        self.is_bake_rotate = False
        self.is_bake_scale = False

        if attr_filter != '':

            self.is_bake_translate = False
            self.is_bake_rotate = False
            self.is_bake_scale = False

            if attr_filter.find('Translate') >= 0:
                self.is_bake_translate = True

            if attr_filter.find('Rotate') >= 0:
                self.is_bake_rotate = True

            if attr_filter.find('Scale') >= 0:
                self.is_bake_scale = True

            if attr_filter.find('All') >= 0:

                self.is_bake_translate = True
                self.is_bake_rotate = True
                self.is_bake_scale = True

    # ==================================================
    def initialize_for_bake_later(self):

        for key_info in self.key_info_list:
            key_info.initialize_for_bake_later()

    # ==================================================
    def bake_to_temp_transform(self, index, target_frame):

        if self.target_transform is None:
            return

        key_info = self.key_info_list[index]
        key_info.bake_to_temp_transform(target_frame)

    # ==================================================
    def bake_to_target(self, target_frame):

        if self.target_transform is None:
            return

        if self.is_bake_translate:

            if cmds.getAttr(self.target_transform + '.translateX', lock=True) or\
                cmds.getAttr(self.target_transform + '.translateY', lock=True) or\
                    cmds.getAttr(self.target_transform + '.translateZ', lock=True):
                return

            this_translate = cmds.getAttr(
                self.trans_scale_transform + '.translate', t=target_frame)[0]

            cmds.setAttr(
                self.target_transform + '.translate', this_translate[0], this_translate[1], this_translate[2])

            cmds.setKeyframe(
                self.target_transform, attribute='translate', time=target_frame)

        if self.is_bake_rotate:

            if cmds.getAttr(self.target_transform + '.rotateX', lock=True) or\
                cmds.getAttr(self.target_transform + '.rotateY', lock=True) or\
                    cmds.getAttr(self.target_transform + '.rotateZ', lock=True):
                return

            this_rotate = cmds.getAttr(
                self.rotate_transform + '.rotate', t=target_frame)[0]

            cmds.xform(self.target_transform, rotation=this_rotate, ws=True)

            cmds.setKeyframe(
                self.target_transform, attribute='rotate', time=target_frame)

        if self.is_bake_scale:

            if cmds.getAttr(self.target_transform + '.scaleX', lock=True) or\
                cmds.getAttr(self.target_transform + '.scaleY', lock=True) or\
                    cmds.getAttr(self.target_transform + '.scaleZ', lock=True):
                return

            this_scale = cmds.getAttr(
                self.trans_scale_transform + '.scale', t=target_frame)[0]

            cmds.setAttr(
                self.target_transform + '.scale', this_scale[0], this_scale[1], this_scale[2])

            cmds.setKeyframe(
                self.target_transform, attribute='scale', time=target_frame)

        if self.is_camera and cmds.objExists(self.camera_transform):

            if cmds.getAttr(self.target_transform + '.focalLength', lock=True):
                return

            this_translate = cmds.getAttr(
                self.camera_transform + '.focalLength', t=target_frame)

            cmds.setAttr(
                self.target_transform + '.focalLength', this_translate)

            cmds.setKeyframe(
                self.target_transform, attribute='focalLength', time=target_frame)

    # ==================================================
    def finalize_for_bake(self):

        common.utility.maya.base.node.delete_node(
            [self.trans_scale_transform, self.rotate_transform, self.forward_transform, self.up_transform, self.camera_transform])
