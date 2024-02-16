# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from . import target_info, util

try:
    from importlib import reload
    from builtins import object
except Exception:
    pass

reload(target_info)
reload(util)


class FacialRigHeadAttach(object):

    def __init__(self):

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.base_exists = False

        self.rig_head_name = 'Rig_head'
        self.neck_name = 'Neck'
        self.head_name = 'Head'
        self.neck_group_name = 'Neck_g'
        self.neck_controller_name = 'Neck_Ctrl'
        self.head_group_name = 'Head_g'
        self.head_controller_name = 'Head_Ctrl'

        self.rig_head = None
        self.neck = None
        self.head = None
        self.neck_group = None
        self.neck_controller = None
        self.head_group = None
        self.head_controller = None

        self.target_info = None
        self.facial_rig_head_attach_info_item_list = None
        self.eye_controller_name_list = [
            'Eye_small_info_L_Ctrl',
            'Eye_big_info_L_Ctrl',
            'Eye_base_info_L_Ctrl',
            'Eye_small_info_R_Ctrl',
            'Eye_big_info_R_Ctrl',
            'Eye_base_info_R_Ctrl',
            'Eye_kira_info_Ctrl'
        ]

    def attach_rig(self):

        if not self.__check_base():
            return

        self.__create_target_info()

        # 選択状態の保存
        selected = cmds.ls(sl=True)

        cmds.currentTime(0)

        self.__create_facial_rig_head_attach_info_item_list()

        for facial_rig_head_attach_info_item in self.facial_rig_head_attach_info_item_list:

            facial_rig_head_attach_info_item.check_object()
            facial_rig_head_attach_info_item.create_rig()
            facial_rig_head_attach_info_item.save_controller_value()
            facial_rig_head_attach_info_item.delete_constraint()
            facial_rig_head_attach_info_item.disconnect_attribute()
            facial_rig_head_attach_info_item.reset_controller()
            facial_rig_head_attach_info_item.set_attribute()

        for facial_rig_head_attach_info_item in self.facial_rig_head_attach_info_item_list:

            facial_rig_head_attach_info_item.maintain_group_and_offset()

        for facial_rig_head_attach_info_item in self.facial_rig_head_attach_info_item_list:

            facial_rig_head_attach_info_item.create_hierarchy()

        for facial_rig_head_attach_info_item in self.facial_rig_head_attach_info_item_list:

            facial_rig_head_attach_info_item.maintain_group_and_offset()

        for facial_rig_head_attach_info_item in self.facial_rig_head_attach_info_item_list:

            facial_rig_head_attach_info_item.constrain_to_target()
            facial_rig_head_attach_info_item.load_controller_value()

        cmds.select(selected)

    def detach_rig(self):

        selected = cmds.ls(sl=True)

        cmds.currentTime(0)

        self.__create_target_info()

        self.__create_facial_rig_head_attach_info_item_list()

        for info_item in self.facial_rig_head_attach_info_item_list:

            info_item.check_object()

            info_item.save_controller_value()

            info_item.reset_controller()
            info_item.delete_constraint()
            info_item.disconnect_attribute()

            info_item.load_controller_value()

        cmds.select(selected)

    def reset_rig(self):

        selected = cmds.ls(sl=True)

        self.__create_target_info()
        self.__create_facial_rig_head_attach_info_item_list()

        for info_item in self.facial_rig_head_attach_info_item_list:

            info_item.check_object()
            info_item.reset_controller()

        cmds.select(selected)

    def __check_base(self):

        self.neck_group = util.find_node(self.neck_group_name, self.rig_head_name)
        if not self.neck_group:
            return False

        self.neck_controller = util.find_node(self.neck_controller_name, self.rig_head_name)
        if not self.neck_controller:
            return False

        self.head_group = util.find_node(self.head_group_name, self.rig_head_name)
        if not self.head_group:
            return False

        self.head_controller = util.find_node(self.head_controller_name, self.rig_head_name)
        if not self.head_controller:
            return False

        self.neck = util.find_node(self.neck_name, self.neck_name)
        if not self.neck:
            return False

        self.head = util.find_node(self.head_name, self.neck_name)
        if not self.head:
            return False

        return True

    def __create_target_info(self):

        self.target_info = target_info.TargetInfo()
        self.target_info.create_info_from_csv('facial_target_info', 'facial_controller_info')
        self.target_info.target_controller_info.controller_root_name = 'Rig_head|Rig_eye_high'
        self.target_info.target_controller_info.target_root_name = 'mdl_chr'
        self.target_info.target_controller_info.update_info(0, True, True)

    def __create_facial_rig_head_attach_info_item_list(self):

        self.facial_rig_head_attach_info_item_list = []

        if not self.target_info.target_controller_info.info_item_list:
            return

        for target_controller_info_item in self.target_info.target_controller_info.info_item_list:

            if target_controller_info_item.controller_name in self.eye_controller_name_list:
                continue

            newItem = FacialRigHeadAttachInfoItem(self)
            newItem.info_item = target_controller_info_item

            newItem.create_info()
            newItem.check_object()

            self.facial_rig_head_attach_info_item_list.append(newItem)

        if not self.facial_rig_head_attach_info_item_list:
            return

        self.facial_rig_head_attach_info_item_list.sort(key=lambda x: x.controller)


class FacialRigHeadAttachInfoItem(object):

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

    def create_info(self):

        self.controller_name = self.info_item.controller_name
        self.controller = self.info_item.controller

        self.target_name = self.info_item.target_name
        self.target = self.info_item.target

        self.group_name = self.controller_name.replace('_Ctrl', '') + '_g'
        self.offset_name = self.controller_name.replace('_Ctrl', '') + '_c'

    def check_object(self):

        self.group = util.find_node(self.group_name, self.root.rig_head_name)
        self.controller = util.find_node(self.controller_name, self.root.rig_head_name)
        self.offset = util.find_node(self.offset_name, self.root.rig_head_name)
        self.target = util.find_node(self.target_name, self.root.neck_name)

    def create_rig(self):

        # グループ作成

        if not self.group:

            this_group = cmds.group(em=True, name=self.group_name)
            cmds.parent('|' + this_group, self.root.head_controller)

            self.group = util.find_node(self.group_name, self.root.rig_head_name)

        if not self.group:
            return

        # コントローラ作成

        if not self.controller:

            this_group = cmds.group(em=True, name=self.controller_name)
            cmds.parent('|' + this_group, self.group)

            self.controller = util.find_node(self.controller_name, self.root.rig_head_name)

        if not self.controller:
            return

        # オフセット作成

        if not self.offset:

            this_group = cmds.group(em=True, name=self.offset_name)
            cmds.parent('|' + this_group, self.controller)

            self.offset = util.find_node(self.offset_name, self.root.rig_head_name)

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

    def set_attribute(self):

        if self.controller:

            cmds.setAttr('{}.displayHandle'.format(self.controller), 1)

            cmds.setAttr(self.controller + '.overrideEnabled', 1)
            cmds.setAttr(self.controller + '.overrideRGBColors', 1)
            cmds.setAttr(self.controller + '.overrideColorRGB', 0.2, 0.8, 0.2, type='double3')

            # transform, rotate, scaleの各アトリビュートのlock状態を解除
            for attr in ['t', 'r', 's']:
                for axis in ['x', 'y', 'z']:
                    cmds.lockNode('{}.{}{}'.format(self.controller, attr, axis), lock=False)

    def save_controller_value(self):

        if not self.controller:
            return

        self.controller_translate = cmds.getAttr('{}.translate'.format(self.controller))[0]
        self.controller_rotate = cmds.getAttr('{}.rotate'.format(self.controller))[0]
        self.controller_scale = cmds.getAttr('{}.scale'.format(self.controller))[0]

    def load_controller_value(self):

        if not self.controller:
            return

        cmds.setAttr('{}.translate'.format(self.controller), *self.controller_translate, type='double3')
        cmds.setAttr('{}.rotate'.format(self.controller), *self.controller_rotate, type='double3')
        cmds.setAttr('{}.scale'.format(self.controller), *self.controller_scale, type='double3')

    def reset_controller(self):

        if not self.controller:
            return

        cmds.setAttr('{}.translate'.format(self.controller), 0, 0, 0, type='double3')
        cmds.setAttr('{}.rotate'.format(self.controller), 0, 0, 0, type='double3')
        cmds.setAttr('{}.scale'.format(self.controller), 1, 1, 1, type='double3')

    def delete_constraint(self):

        if not self.target:
            return

        const_list = cmds.listRelatives(self.target, c=True, ad=True, typ='constraint')
        if not const_list:
            return

        cmds.delete(const_list)

    def disconnect_attribute(self):

        if not self.target or not self.controller:
            return

        if cmds.isConnected('{}.scale'.format(self.controller), '{}.scale'.format(self.target)):
            cmds.disconnectAttr('{}.scale'.format(self.controller), '{}.scale'.format(self.target))

    def maintain_group_and_offset(self):

        if not self.target or not self.group or not self.controller or not self.offset:
            return

        cmds.pointConstraint(self.target, self.group)

        this_const_list = cmds.listRelatives(self.group, c=True, ad=True, typ='constraint')
        if this_const_list:
            cmds.delete(this_const_list)

        cmds.pointConstraint(self.target, self.offset)
        cmds.orientConstraint(self.target, self.offset)
        cmds.scaleConstraint(self.target, self.offset)

        this_const_list = cmds.listRelatives(self.offset, c=True, ad=True, typ='constraint')
        if this_const_list:
            cmds.delete(this_const_list)

    def constrain_to_target(self):

        if not self.target or not self.group or not self.controller or not self.offset:
            return

        cmds.pointConstraint(self.offset, self.target)
        cmds.orientConstraint(self.offset, self.target)

        # スケールはコネクト対応
        cmds.connectAttr('{}.scale'.format(self.controller), '{}.scale'.format(self.target))

    def create_hierarchy(self):

        if not self.target:
            return

        parent_list = cmds.listRelatives(self.target, p=True, type='transform', f=True)
        if not parent_list:
            return

        parent = parent_list[0]

        parent_info_item = None

        for info_item in self.root.facial_rig_head_attach_info_item_list:

            if info_item.target != parent:
                continue

            parent_info_item = info_item

        if not parent_info_item:
            return

        parent_info_item.check_object()

        group_parent_list = cmds.listRelatives(self.group, p=True, type='transform', f=True)

        group_parent = None

        if group_parent_list:
            group_parent = group_parent_list[0]

        if group_parent != parent_info_item.controller:
            cmds.parent(self.group, parent_info_item.controller)

        self.check_object()
