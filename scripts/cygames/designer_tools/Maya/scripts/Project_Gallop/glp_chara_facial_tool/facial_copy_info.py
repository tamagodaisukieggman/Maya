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

import os

import maya.cmds as cmds

from . import target_info


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialCopyInfo(object):

    # ==================================================
    def __init__(self):

        self.script_file_path = None
        self.script_dir_path = None

        self.target_file_path = None
        self.target_dir_path = None

        self.copy_info_item_list = None

        self.is_init = False

        self.is_copied = False

        self.facial_target_info = None

    # ==================================================
    def __initialize(self):

        self.is_init = False
        self.is_copied = False

        current_path = cmds.file(q=True, sn=True)

        if not current_path:
            cmds.warning("mdl_chrxxxx_xx_facial_targetシーンを開いて実行してください")
            return

        if not os.path.isfile(current_path):
            return

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.target_file_path = current_path
        self.target_dir_path = os.path.dirname(self.target_file_path)

        self.copy_info_item_list = []

        self.is_init = True

    # ==================================================
    def create_info_from_frame(self, target_frame):

        self.__initialize()

        if not self.is_init:
            return

        new_info = FacialCopyInfoItem(self)

        new_info.label = 'Temp'

        new_info.eyebrow_l_frame = target_frame
        new_info.eyebrow_r_frame = target_frame

        new_info.eye_l_frame = target_frame
        new_info.eye_r_frame = target_frame

        new_info.mouth_frame = target_frame

        self.copy_info_item_list.append(new_info)

        self.facial_target_info = target_info.TargetInfo()

        self.facial_target_info.target_controller_info.controller_root_name = 'Rig_head|Rig_eye_high'
        self.facial_target_info.target_controller_info.target_root_name = 'Neck'

        self.facial_target_info.create_info_from_csv(
            'facial_target_info', 'facial_controller_info')

        self.is_copied = True

    # ==================================================
    def update_info(self, update_controller, update_target):

        if not self.is_copied:
            return

        self.facial_target_info.update_info(update_controller, update_target)

        for copy_info_item in self.copy_info_item_list:
            copy_info_item.update_info(update_controller, update_target)

    # ==================================================
    def set_transform(self,
                      frame,
                      is_controller,
                      is_eyebrow_r, is_eyebrow_l,
                      is_eye_r, is_eye_l,
                      is_mouth
                      ):

        if not self.is_copied:
            return

        for copy_info_item in self.copy_info_item_list:

            copy_info_item.set_transform(
                frame,
                is_controller,
                is_eyebrow_r, is_eyebrow_l, is_eye_r, is_eye_l, is_mouth)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialCopyInfoItem(object):

    # ==================================================
    def __init__(self, parent):

        self.parent = parent

        self.label = None

        self.eyebrow_l_frame = 0
        self.eyebrow_r_frame = 0

        self.eye_l_frame = 0
        self.eye_r_frame = 0

        self.mouth_frame = 0

        self.eyebrow_l_controller_info_item_list = None
        self.eyebrow_r_controller_info_item_list = None

        self.eye_l_controller_info_item_list = None
        self.eye_r_controller_info_item_list = None

        self.mouth_controller_info_item_list = None

    # ==================================================
    def update_info(self, update_controller, update_target):

        self.parent.facial_target_info.target_controller_info.update_info(
            self.eyebrow_l_frame, update_controller, update_target)

        self.eyebrow_l_controller_info_item_list = \
            self.parent.facial_target_info.target_controller_info.get_clone_info_item_list()

        self.parent.facial_target_info.target_controller_info.update_info(
            self.eyebrow_r_frame, update_controller, update_target)

        self.eyebrow_r_controller_info_item_list = \
            self.parent.facial_target_info.target_controller_info.get_clone_info_item_list()

        self.parent.facial_target_info.target_controller_info.update_info(
            self.eye_l_frame, update_controller, update_target)

        self.eye_l_controller_info_item_list = \
            self.parent.facial_target_info.target_controller_info.get_clone_info_item_list()

        self.parent.facial_target_info.target_controller_info.update_info(
            self.eye_r_frame, update_controller, update_target)

        self.eye_r_controller_info_item_list = \
            self.parent.facial_target_info.target_controller_info.get_clone_info_item_list()

        self.parent.facial_target_info.target_controller_info.update_info(
            self.mouth_frame, update_controller, update_target)

        self.mouth_controller_info_item_list = \
            self.parent.facial_target_info.target_controller_info.get_clone_info_item_list()

    # ==================================================
    def set_transform(
        self,
        frame,
        is_controller,
        is_eyebrow_l, is_eyebrow_r,
        is_eye_l, is_eye_r,
        is_mouth
    ):

        if self.eyebrow_l_controller_info_item_list and is_eyebrow_l:

            for controller_info in self.eyebrow_l_controller_info_item_list:

                if controller_info.part != 'Eyebrow_L':
                    continue

                controller_info.set_transform(
                    is_controller, frame, False, 1)

        if self.eyebrow_r_controller_info_item_list and is_eyebrow_r:

            for controller_info in self.eyebrow_r_controller_info_item_list:

                if controller_info.part != 'Eyebrow_R':
                    continue

                controller_info.set_transform(
                    is_controller, frame, False, 1)

        if self.eye_l_controller_info_item_list and is_eye_l:

            for controller_info in self.eye_l_controller_info_item_list:

                if controller_info.part != 'Eye_L':
                    continue

                controller_info.set_transform(
                    is_controller, frame, False, 1)

        if self.eye_r_controller_info_item_list and is_eye_r:

            for controller_info in self.eye_r_controller_info_item_list:

                if controller_info.part != 'Eye_R':
                    continue

                controller_info.set_transform(
                    is_controller, frame, False, 1)

        if self.mouth_controller_info_item_list and is_mouth:

            for controller_info in self.mouth_controller_info_item_list:

                if controller_info.part != 'Mouth':
                    continue

                controller_info.set_transform(
                    is_controller, frame, False, 1)
