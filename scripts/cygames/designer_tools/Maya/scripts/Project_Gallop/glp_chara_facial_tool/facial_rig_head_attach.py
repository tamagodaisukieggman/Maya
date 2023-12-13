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

from ..base_common import utility as base_utility

from . import target_info


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialRigHeadAttach(object):

    # ==================================================
    def __init__(self):

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.base_exists = False

        self.rig_head_name = 'Rig_head'
        self.rig_head = None

        self.neck_name = 'Neck'
        self.neck = None

        self.head_name = 'Head'
        self.head = None

        self.neck_group_name = 'Neck_g'
        self.neck_group = None

        self.neck_controller_name = 'Neck_Ctrl'
        self.neck_controller = None

        self.head_group_name = 'Head_g'
        self.head_group = None

        self.head_controller_name = 'Head_Ctrl'
        self.head_controller = None

        self.target_info = None

        self.info_item_list = None

        self.eye_controller_name_list = [
            'Eye_small_info_L_Ctrl',
            'Eye_big_info_L_Ctrl',
            'Eye_base_info_L_Ctrl',
            'Eye_small_info_R_Ctrl',
            'Eye_big_info_R_Ctrl',
            'Eye_base_info_R_Ctrl',
            'Eye_kira_info_Ctrl'
        ]

    # ==================================================
    def attach_rig(self):

        self.__check_base()

        if not self.base_exists:
            return

        self.__create_target_info()

        base_utility.select.save_selection()

        cmds.currentTime(0)

        self.__create_info_item_list()

        for info_item in self.info_item_list:

            info_item.check_object()

            info_item.create_rig()

            info_item.save_controller_value()

            info_item.delete_constraint()
            info_item.disconnect_attribute()

            info_item.reset_controller()
            info_item.set_attribute()

            # info_item.parent_to_head_ctrl()

        for info_item in self.info_item_list:

            info_item.check_object()

        for info_item in self.info_item_list:

            info_item.check_object()
            info_item.maintain_group_and_offset()

        for info_item in self.info_item_list:

            info_item.check_object()

        for info_item in self.info_item_list:

            info_item.check_object()
            info_item.create_hierarchy()

        for info_item in self.info_item_list:

            info_item.check_object()
            info_item.maintain_group_and_offset()

        for info_item in self.info_item_list:

            info_item.constrain_to_target()
            info_item.load_controller_value()

        base_utility.select.load_selection()

    # ==================================================
    def detach_rig(self):

        base_utility.select.save_selection()

        cmds.currentTime(0)

        self.__create_target_info()

        self.__create_info_item_list()

        for info_item in self.info_item_list:

            info_item.check_object()

            info_item.save_controller_value()

            info_item.reset_controller()
            info_item.delete_constraint()
            info_item.disconnect_attribute()

            info_item.load_controller_value()

        base_utility.select.load_selection()

    # ==================================================
    def reset_rig(self):

        base_utility.select.save_selection()

        self.__create_target_info()

        self.__create_info_item_list()

        for info_item in self.info_item_list:

            info_item.check_object()

            info_item.reset_controller()

        base_utility.select.load_selection()

    # ===============================================
    def __check_base(self):

        self.base_exists = False

        self.neck_group = \
            base_utility.node.search(
                self.neck_group_name, self.rig_head_name)

        if not self.neck_group:
            return

        self.neck_controller = \
            base_utility.node.search(
                self.neck_controller_name, self.rig_head_name)

        if not self.neck_controller:
            return

        self.head_group = \
            base_utility.node.search(
                self.head_group_name, self.rig_head_name)

        if not self.head_group:
            return

        self.head_controller = \
            base_utility.node.search(
                self.head_controller_name, self.rig_head_name)

        if not self.head_controller:
            return

        self.neck = \
            base_utility.node.search(
                self.neck_name, self.neck_name)

        if not self.neck:
            return

        self.head = \
            base_utility.node.search(
                self.head_name, self.neck_name)

        if not self.head:
            return

        self.base_exists = True

    # ===============================================
    def __create_target_info(self):

        self.target_info = target_info.TargetInfo()
        self.target_info.create_info_from_csv('facial_target_info',
                                              'facial_controller_info')

        self.target_info.target_controller_info.controller_root_name = \
            'Rig_head|Rig_eye_high'

        self.target_info.target_controller_info.target_root_name = 'mdl_chr'

        self.target_info.target_controller_info.update_info(0, True, True)

    # ===============================================
    def __create_info_item_list(self):

        self.info_item_list = []

        if not self.target_info.target_controller_info.info_item_list:
            return

        for info_item in \
                self.target_info.target_controller_info.info_item_list:

            if info_item.controller_name in self.eye_controller_name_list:
                continue

            newItem = FacialRigHeadAttachInfoItem(self)

            newItem.info_item = info_item

            newItem.create_info()
            newItem.check_object()

            self.info_item_list.append(newItem)

        if not self.info_item_list:
            return

        self.info_item_list.sort(key=lambda x: x.controller)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialRigHeadAttachInfoItem(object):

    # ==================================================
    def __init__(self, root):

        self.root = root

        self.info_item = None

        self.group_name = None
        self.group = None

        self.controller_name = None
        self.controller = None

        self.offset_name = None
        self.offset = None

        self.target_name = None
        self.target = None

        self.controller_translate = None
        self.controller_rotate = None
        self.controller_scale = None

        self.is_face_controller = False

    # ==================================================
    def create_info(self):

        self.controller_name = self.info_item.controller_name
        self.controller = self.info_item.controller

        self.target_name = self.info_item.target_name
        self.target = self.info_item.target

        self.group_name = \
            self.controller_name.replace('_Ctrl', '') + '_g'
        self.offset_name = \
            self.controller_name.replace('_Ctrl', '') + '_c'

    # ==================================================
    def check_object(self):

        self.group = base_utility.node.search(
            self.group_name, self.root.rig_head_name)

        self.controller = base_utility.node.search(
            self.controller_name, self.root.rig_head_name)

        self.offset = base_utility.node.search(
            self.offset_name, self.root.rig_head_name)

        self.target = base_utility.node.search(
            self.target_name, self.root.neck_name)

    # ==================================================
    def create_rig(self):

        # グループ作成

        if not self.group:

            this_group = cmds.group(em=True, name=self.group_name)
            cmds.parent('|' + this_group, self.root.head_controller)

            self.group = base_utility.node.search(
                self.group_name, self.root.rig_head_name)

        if not self.group:
            return

        # コントローラ作成

        if not self.controller:

            this_group = cmds.group(em=True, name=self.controller_name)
            cmds.parent('|' + this_group, self.group)

            self.controller = base_utility.node.search(
                self.controller_name, self.root.rig_head_name)

        if not self.controller:
            return

        # オフセット作成

        if not self.offset:

            this_group = cmds.group(em=True, name=self.offset_name)
            cmds.parent('|' + this_group, self.controller)

            self.offset = base_utility.node.search(
                self.offset_name, self.root.rig_head_name)

    # ==================================================
    def parent_to_head_ctrl(self):

        if not self.group:
            return

        group_parent_list = cmds.listRelatives(
            self.group, p=True, type='transform', f=True)

        group_parent = None

        if group_parent_list:
            group_parent = group_parent_list[0]

        if group_parent != self.root.head_controller:
            cmds.parent(self.group, self.root.head_controller)

        self.check_object()

    # ==================================================
    def set_attribute(self):

        if self.controller:

            base_utility.attribute.set_value(
                self.controller, 'displayHandle', 1)

            cmds.setAttr(self.controller + '.overrideEnabled', 1)
            cmds.setAttr(self.controller + '.overrideRGBColors', 1)
            cmds.setAttr(self.controller + '.overrideColorRGB', 0.2, 0.8, 0.2)

            base_utility.attribute.set_lock(
                self.controller, 'tx', False)
            base_utility.attribute.set_lock(
                self.controller, 'ty', False)
            base_utility.attribute.set_lock(
                self.controller, 'tz', False)

            base_utility.attribute.set_lock(
                self.controller, 'rx', False)
            base_utility.attribute.set_lock(
                self.controller, 'ry', False)
            base_utility.attribute.set_lock(
                self.controller, 'rz', False)

            base_utility.attribute.set_lock(
                self.controller, 'sx', False)
            base_utility.attribute.set_lock(
                self.controller, 'sy', False)
            base_utility.attribute.set_lock(
                self.controller, 'sz', False)

    # ==================================================
    def save_controller_value(self):

        if not self.controller:
            return

        self.controller_translate = base_utility.attribute.get_value(
            self.controller, 'translate')
        self.controller_rotate = base_utility.attribute.get_value(
            self.controller, 'rotate')
        self.controller_scale = base_utility.attribute.get_value(
            self.controller, 'scale')

    # ==================================================
    def load_controller_value(self):

        if not self.controller:
            return

        base_utility.attribute.set_value(
            self.controller, 'translate', self.controller_translate
        )

        base_utility.attribute.set_value(
            self.controller, 'rotate', self.controller_rotate
        )

        base_utility.attribute.set_value(
            self.controller, 'scale', self.controller_scale
        )

    # ==================================================
    def reset_controller(self):

        if not self.controller:
            return

        base_utility.attribute.set_value(
            self.controller, 'translate', [0, 0, 0]
        )

        base_utility.attribute.set_value(
            self.controller, 'rotate', [0, 0, 0]
        )

        base_utility.attribute.set_value(
            self.controller, 'scale', [1, 1, 1]
        )

    # ===============================================
    def delete_constraint(self):

        if not self.target:
            return

        const_list = cmds.listRelatives(
            self.target,
            c=True, ad=True, typ='constraint')

        if not const_list:
            return

        cmds.delete(const_list)

    # ===============================================
    def disconnect_attribute(self):

        if not self.target:
            return

        if not self.controller:
            return

        base_utility.attribute.disconnect(
            self.controller, 'scale',
            self.target, 'scale'
        )

    # ===============================================
    def maintain_group_and_offset(self):

        if not self.target:
            return

        if not self.group:
            return

        if not self.controller:
            return

        if not self.offset:
            return

        cmds.pointConstraint(self.target, self.group)

        this_const_list = cmds.listRelatives(
            self.group,
            c=True, ad=True, typ='constraint')

        if this_const_list:
            cmds.delete(this_const_list)

        cmds.pointConstraint(self.target, self.offset)
        cmds.orientConstraint(self.target, self.offset)
        cmds.scaleConstraint(self.target, self.offset)

        this_const_list = cmds.listRelatives(
            self.offset,
            c=True, ad=True, typ='constraint')

        if this_const_list:
            cmds.delete(this_const_list)

    # ===============================================
    def constrain_to_target(self):

        if not self.target:
            return

        if not self.group:
            return

        if not self.controller:
            return

        if not self.offset:
            return

        cmds.pointConstraint(self.offset, self.target)
        cmds.orientConstraint(self.offset, self.target)

        # スケールはコネクト対応
        base_utility.attribute.connect(
            self.controller, 'scale',
            self.target, 'scale'
        )

    # ===============================================
    def create_hierarchy(self):

        if not self.target:
            return

        parent_list = cmds.listRelatives(
            self.target, p=True, type='transform', f=True)

        if not parent_list:
            return

        parent = parent_list[0]

        parent_info_item = None

        for info_item in self.root.info_item_list:

            if info_item.target != parent:
                continue

            parent_info_item = info_item

        if not parent_info_item:
            return

        parent_info_item.check_object()

        group_parent_list = cmds.listRelatives(
            self.group, p=True, type='transform', f=True)

        group_parent = None

        if group_parent_list:
            group_parent = group_parent_list[0]

        if group_parent != parent_info_item.controller:
            cmds.parent(self.group, parent_info_item.controller)

        self.check_object()
