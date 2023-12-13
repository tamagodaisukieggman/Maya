# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os
import sys
import re
import glob
import time

import maya.cmds as cmds
import maya.mel as mel

from .. import farm_common
from ..farm_common.utility import model_define

reload(farm_common)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialBlendShapeSwicher(object):

    # ===============================================
    def __init__(self):

        self.FACE_MESH_NAME = model_define.MESH_PREFIX + 'face'

        self.face_mesh = None
        self.blend_shape_node = None
        self.blend_shape_info = None

    # ===============================================
    def initialize(self, blend_shape_info):

        self.__init__()
        self.face_mesh = self.__get_face_mesh()
        self.blend_shape_node = self.__get_taget_blend_shape_node()

        self.blend_shape_info = blend_shape_info
        if not self.blend_shape_info.is_initialized:
            self.blend_shape_info.initialize()

    # ===============================================
    def __get_face_mesh(self):

        face_list = cmds.ls(self.FACE_MESH_NAME, typ='transform')

        if face_list:
            return face_list[0]

    # ===============================================
    def __get_taget_blend_shape_node(self):

        if not self.face_mesh or not cmds.objExists(self.face_mesh):
            return None

        blend_shape_nodes = cmds.ls(cmds.listHistory(self.face_mesh), typ='blendShape')

        # ブレンドシェイプはシーンにフェイシャル用の一つのみのはず
        if blend_shape_nodes:
            return blend_shape_nodes[0]
        else:
            return None

    # ===============================================
    def goto_default_facial(self, facial_type):

        for item in self.blend_shape_info.blend_shape_item_list:
            if item.facial_type == facial_type:
                self.apply_shape(item.target, 0)

    # ===============================================
    def apply_facial_by_label(self, facial_type, label):

        for item in self.blend_shape_info.blend_shape_item_list:
            if item.facial_type == facial_type:
                if item.label == label:
                    self.apply_shape(item.target, 1)
                else:
                    self.apply_shape(item.target, 0)

    # ===============================================
    def change_weight_by_label(self, facial_type, label, weight):

        for item in self.blend_shape_info.blend_shape_item_list:
            if item.facial_type == facial_type and item.label == label:
                self.apply_shape(item.target, weight)

    # ===============================================
    def change_weight_by_part(self, facial_type, part, weight):

        for item in self.blend_shape_info.blend_shape_item_list:
            if item.facial_type == facial_type and item.part == part:
                self.apply_shape(item.target, weight)

    # ===============================================
    def apply_shape(self, target, weight):

        if not self.blend_shape_node or not cmds.objExists(self.blend_shape_node):
            print('no blend shape node')
            return

        target_shape = '{}.{}'.format(self.blend_shape_node, target)

        if not cmds.objExists(target_shape):
            print('no target: ' + target)
            return

        cmds.setAttr(target_shape, weight)

    # ===============================================
    def create_check_anim(self, facial_type, spacing=10):

        if not self.blend_shape_node or not cmds.objExists(self.blend_shape_node):
            return

        # リセット
        self.goto_default_facial(facial_type)
        self.delete_check_anim(facial_type)

        label_list = self.__get_label_list(facial_type)
        label_list.sort()
        target_list = self.__get_target_list(facial_type)

        target_time = 0

        self.__set_key_to_shape_target(target_list, target_time)
        self.__set_key_to_shape_target(target_list, target_time + (spacing / 2))

        for label in label_list:
            target_time += spacing
            self.apply_facial_by_label(facial_type, label)
            self.__set_key_to_shape_target(target_list, target_time)
            self.__set_key_to_shape_target(target_list, target_time + (spacing / 2))

        final_time = target_time + (spacing / 2)
        cmds.playbackOptions(min=0.0, ast=0.0, max=final_time, aet=final_time)

    # ===============================================
    def delete_check_anim(self, facial_type):

        target_list = self.__get_target_list(facial_type)

        for target in target_list:

            key_attr = '{}.{}'.format(self.blend_shape_node, target)

            if not cmds.objExists(key_attr):
                continue

            cmds.cutKey(key_attr, cl=True)

    # ===============================================
    def __get_label_list(self, facial_type):

        label_list = []

        for item in self.blend_shape_info.blend_shape_item_list:

            if item.facial_type != facial_type:
                continue

            if item.label not in label_list:
                label_list.append(item.label)

        return label_list

    # ===============================================
    def __get_target_list(self, facial_type):

        target_list = []

        for item in self.blend_shape_info.blend_shape_item_list:

            if item.facial_type != facial_type:
                continue

            target_list.append(item.target)

        return target_list

    # ===============================================
    def __set_key_to_shape_target(self, target_list, time):

        for target in target_list:

            key_attr = '{}.{}'.format(self.blend_shape_node, target)

            if not cmds.objExists(key_attr):
                continue

            cmds.setKeyframe(key_attr, t=time)
