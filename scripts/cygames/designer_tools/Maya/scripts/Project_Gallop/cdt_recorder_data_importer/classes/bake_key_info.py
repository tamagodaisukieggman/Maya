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

import math

import maya.cmds as cmds


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeKeyInfo(object):

    # ==================================================
    def __init__(self, parent):

        self.exists = False

        self.parent = parent

        self.translate = [0] * 3
        self.rotate = [0] * 3
        self.scale = [1] * 3

        self.world_position = [0] * 3

        self.forward_vector = [0] * 3
        self.up_vector = [0] * 3

        self.fov = 0
        self.focalLength = 0

        self.fix_translate = [0] * 3

        self.fix_rotate_position = [0] * 3
        self.fix_forward_vector = [0] * 3
        self.fix_up_vector = [0] * 3

        self.fix_focalLength = 0

    # ==================================================
    def read_xml(self, parent_element):

        self.exists = False

        self.translate = self.__get_float_list_from_attribute(
            parent_element, 'Translate')

        self.rotate = self.__get_float_list_from_attribute(
            parent_element, 'Rotate')

        self.scale = self.__get_float_list_from_attribute(
            parent_element, 'Scale')

        self.world_position = self.__get_float_list_from_attribute(
            parent_element, 'WorldPosition')

        self.forward_vector = self.__get_float_list_from_attribute(
            parent_element, 'ForwardVector')

        self.up_vector = self.__get_float_list_from_attribute(
            parent_element, 'UpVector')

        self.fov = float(parent_element.attrib['Fov'])

        self.focalLength = float(parent_element.attrib['FocalLength'])

        self.exists = True

    # ==================================================
    def __get_float_list_from_attribute(self, target_element, attr_name):

        valueX = float(target_element.attrib[attr_name + 'X'])
        valueY = float(target_element.attrib[attr_name + 'Y'])
        valueZ = float(target_element.attrib[attr_name + 'Z'])

        return [valueX, valueY, valueZ]

    # ==================================================
    def initialize_for_bake(self):

        self.fix_translate[0] = \
            -self.translate[0] * self.parent.parent.scale_factor
        self.fix_translate[1] = \
            self.translate[1] * self.parent.parent.scale_factor
        self.fix_translate[2] = \
            self.translate[2] * self.parent.parent.scale_factor

        self.fix_rotate_position[0] = \
            -self.world_position[0] * self.parent.parent.scale_factor
        self.fix_rotate_position[1] = \
            self.world_position[1] * self.parent.parent.scale_factor
        self.fix_rotate_position[2] = \
            self.world_position[2] * self.parent.parent.scale_factor

        for cnt in range(3):

            if self.fix_rotate_position[cnt] < self.parent.parent.rotate_min_position[cnt]:
                self.parent.parent.rotate_min_position[cnt] = self.fix_rotate_position[cnt]

            if self.fix_rotate_position[cnt] > self.parent.parent.rotate_max_position[cnt]:
                self.parent.parent.rotate_max_position[cnt] = self.fix_rotate_position[cnt]

        if cmds.objExists(self.parent.camera_transform):
            self.fix_focalLength = self.__get_maya_focal_length(self.fov)

    # ==================================================
    def __get_maya_focal_length(self, unity_fov):

        this_vert_aperture = cmds.camera(self.parent.camera_transform, q=True, vfa=True)

        # Mayaの規定値
        maya_focal_length_min = 2.5

        if unity_fov == 0:
            return maya_focal_length_min

        # Unityのfovの計算式をMayaのfocalLengthについて解いたもの。以下のサイトを参考にしている。
        # https://www.slideshare.net/nyaakobayashi/mayaunity
        maya_focal_length = this_vert_aperture / (2 * 0.03937 * math.tan(unity_fov / (2 * 57.29578)))

        if maya_focal_length < maya_focal_length_min:
            return maya_focal_length_min
        else:
            return maya_focal_length

    # ==================================================
    def initialize_for_bake_later(self):

        self.fix_rotate_position[0] -= self.parent.parent.rotate_position_offset[0]
        self.fix_rotate_position[1] -= self.parent.parent.rotate_position_offset[1]
        self.fix_rotate_position[2] -= self.parent.parent.rotate_position_offset[2]

        self.fix_forward_vector[0] = \
            -self.forward_vector[0] + self.fix_rotate_position[0]

        self.fix_forward_vector[1] = \
            self.forward_vector[1] + self.fix_rotate_position[1]

        self.fix_forward_vector[2] = \
            self.forward_vector[2] + self.fix_rotate_position[2]

        self.fix_up_vector[0] = \
            -self.up_vector[0] + self.fix_rotate_position[0]

        self.fix_up_vector[1] = \
            self.up_vector[1] + self.fix_rotate_position[1]

        self.fix_up_vector[2] = \
            self.up_vector[2] + self.fix_rotate_position[2]

    # ==================================================
    def bake_to_temp_transform(self, target_frame):

        cmds.setAttr(
            self.parent.trans_scale_transform + '.translate', self.fix_translate[0], self.fix_translate[1], self.fix_translate[2])

        cmds.setAttr(
            self.parent.trans_scale_transform + '.scale', self.scale[0], self.scale[1], self.scale[2])

        cmds.setAttr(
            self.parent.rotate_transform + '.translate', self.fix_rotate_position[0], self.fix_rotate_position[1], self.fix_rotate_position[2])

        cmds.setAttr(
            self.parent.forward_transform + '.translate', self.fix_forward_vector[0], self.fix_forward_vector[1], self.fix_forward_vector[2])

        cmds.setAttr(
            self.parent.up_transform + '.translate', self.fix_up_vector[0], self.fix_up_vector[1], self.fix_up_vector[2])

        if cmds.objExists(self.parent.camera_transform):
            cmds.setAttr(
                self.parent.camera_transform + '.focalLength', self.fix_focalLength)

        cmds.setKeyframe(
            self.parent.trans_scale_transform, attribute='translate', time=target_frame)

        cmds.setKeyframe(
            self.parent.trans_scale_transform, attribute='scale', time=target_frame)

        cmds.setKeyframe(
            self.parent.rotate_transform, attribute='translate', time=target_frame)

        cmds.setKeyframe(
            self.parent.forward_transform, attribute='translate', time=target_frame)

        cmds.setKeyframe(
            self.parent.up_transform, attribute='translate', time=target_frame)

        if cmds.objExists(self.parent.camera_transform):
            cmds.setKeyframe(
                self.parent.camera_transform, attribute='rotate', time=target_frame)

            cmds.setKeyframe(
                self.parent.camera_transform, attribute='focalLength', time=target_frame)
