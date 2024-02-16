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

import os
import csv

import maya.cmds as cmds

from ..base_common import utility as base_utility


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TargetControllerInfo(object):

    # ==================================================
    def __init__(self, target_info):

        self.target_info = target_info

        self.target_csv_file_path = None

        self.csv_enable_index = -1
        self.csv_part_index = -1
        self.csv_controller_index = -1
        self.csv_target_index = -1
        self.csv_driver_index = -1
        self.csv_start_index = -1

        self.script_file_path = None
        self.script_dir_path = None

        self.target_file_path = None
        self.target_file_name = None
        self.target_file_name_noext = None
        self.target_file_ext = None
        self.target_dir_path = None

        self.controller_root_name = None
        self.target_root_name = None
        self.driver_root_name = None

        self.info_item_list = None

        self.is_init = False
        self.is_created = False

    # ===============================================
    def __initialize(self):

        current_path = cmds.file(q=True, sn=True)

        self.target_file_path = None

        if not current_path:
            return

        if not os.path.isfile(current_path):
            return

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.target_file_path = current_path.replace('\\', '/')
        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = os.path.dirname(self.target_file_path)
        self.target_file_name_noext, self.target_file_ext = \
            os.path.splitext(self.target_file_name)

        self.info_item_list = []

    # ==================================================
    def create_info_from_csv(self, csv_file_name):

        self.is_created = False

        self.__initialize()

        if not self.target_file_path:
            return

        if not csv_file_name:
            return

        self.__read_info(csv_file_name)

        if not self.info_item_list:
            return

        self.is_created = True

    # ==================================================
    def __read_info(self, csv_file_name):

        self.target_csv_file_path = \
            self.target_dir_path + '/' + csv_file_name + '.csv'

        if not os.path.isfile(self.target_csv_file_path):
            self.target_csv_file_path = \
                self.script_dir_path + \
                '/resource/' + csv_file_name + '.csv'

        if not os.path.isfile(self.target_csv_file_path):
            return

        referenced_nodes = cmds.ls(referencedNodes=True)
        dag_nodes = cmds.ls(dagObjects=True)

        current_list_index = 0
        with open(self.target_csv_file_path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            is_first_line = True
            for csv_line_arr in csv_reader:
                # 最初の行でカラムのインデックスを取得
                if is_first_line:
                    # csvから読み取る項目
                    self.csv_enable_index = -1
                    self.csv_part_index = -1
                    self.csv_controller_index = -1
                    self.csv_target_index = -1
                    self.csv_driver_index = -1
                    self.csv_start_index = -1
                    for col in range(len(csv_line_arr)):
                        this_text = csv_line_arr[col]
                        if this_text == 'Enable':
                            self.csv_enable_index = col
                        elif this_text == 'Part':
                            self.csv_part_index = col
                        elif this_text == 'ControllerName':
                            self.csv_controller_index = col
                        elif this_text == 'TargetName':
                            self.csv_target_index = col
                        elif this_text == 'DriverName':
                            self.csv_driver_index = col
                    is_first_line = False

                if not csv_line_arr:
                    continue

                if csv_line_arr[self.csv_enable_index] != '1':
                    continue

                new_info_item = TargetControllerInfoItem(self)

                # target_indexが存在し、targetが存在しない場合はcontinueで返す
                if self.csv_target_index >= 0:

                    target_name = csv_line_arr[self.csv_target_index]

                    # importされている場合とリファレンスされている場合があるので両方とも検索する
                    target_list = [target_node for target_node in dag_nodes if target_node.endswith(target_name)]
                    ref_target_list = [target_node for target_node in referenced_nodes if target_node.endswith(target_name)]

                    if not target_list and not ref_target_list:
                        continue

                    new_info_item.target_name = target_name

                new_info_item.list_index = current_list_index
                current_list_index += 1

                if self.csv_controller_index >= 0:
                    new_info_item.controller_name = \
                        csv_line_arr[self.csv_controller_index]

                if self.csv_part_index >= 0:
                    new_info_item.part = \
                        csv_line_arr[self.csv_part_index]

                if self.csv_driver_index >= 0:
                    new_info_item.driver_name = \
                        csv_line_arr[self.csv_driver_index]

                self.info_item_list.append(new_info_item)

    # ==================================================
    def update_info(self, target_frame, update_controller, update_target):

        if not self.is_created:
            return

        for info_item in self.info_item_list:

            info_item.update_info(
                target_frame, update_controller, update_target)

    # ==================================================
    def get_clone_info_item_list(self):

        if not self.is_created:
            return

        clone_info_item_list = []

        for info_item in self.info_item_list:

            this_clone = info_item.get_clone()

            clone_info_item_list.append(this_clone)

        return clone_info_item_list

    # ==================================================
    def get_target_info_index_list(self, target_part_type):

        info_index_list = []

        for p in range(len(self.info_item_list)):

            this_info = self.info_item_list[p]

            if this_info.part_type == target_part_type:
                info_index_list.append(p)

        return info_index_list


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TargetControllerInfoItem(object):

    # ==================================================
    def __init__(self, root):

        self.root = root

        self.list_index = -1

        self.base_controller_info_item = None

        self.part = None

        self.controller = None
        self.controller_name = None

        self.target = None
        self.target_name = None

        self.driver = None
        self.driver_name = None

        self.controller_translate = None
        self.controller_rotate = None
        self.controller_scale = None

        self.controller_translate_base = None
        self.controller_rotate_base = None
        self.controller_scale_base = None

        self.controller_translate_offset = None
        self.controller_rotate_offset = None
        self.controller_scale_offset = None

        self.target_translate = None
        self.target_rotate = None
        self.target_scale = None

        self.target_translate_base = None
        self.target_rotate_base = None
        self.target_scale_base = None

        self.target_translate_offset = None
        self.target_rotate_offset = None
        self.target_scale_offset = None

        self.animation_layer_name = None

        self.translate_offset_multiply = None
        self.rotate_offset_multiply = None
        self.scale_offset_multiply = None

    # ==================================================
    def update_info(self, target_frame, update_controller, update_target):

        self.__update_base_controller_info_item()

        self.__update_controller_and_target()

        self.__update_current(target_frame, update_controller, update_target)

        self.__update_base(update_controller, update_target)

        self.__update_offset(update_controller, update_target)

    # ==================================================
    def __update_base_controller_info_item(self):

        self.base_controller_info_item = None

        if not self.root.target_info:
            return

        if not self.root.target_info.base_info_item:
            return

        if not self.root.target_info.base_info_item.controller_info_item_list:
            return

        if self.list_index < 0 or \
                self.list_index >= len(self.root.target_info.base_info_item.controller_info_item_list):
            return

        self.base_controller_info_item = \
            self.root.target_info.base_info_item.controller_info_item_list[self.list_index]

    # ==================================================
    def __update_controller_and_target(self):

        if not self.base_controller_info_item:

            # コントローラ割り出し
            self.controller = base_utility.node.search(
                self.controller_name,
                self.root.controller_root_name, 'transform'
            )

            # 対象の割り出し
            self.target = base_utility.node.search(
                self.target_name,
                self.root.target_root_name, 'transform'
            )

            return

        self.controller = self.base_controller_info_item.controller
        self.controller_name = self.base_controller_info_item.controller_name

        self.target = self.base_controller_info_item.target
        self.target_name = self.base_controller_info_item.target_name

    # ==================================================
    def __update_current(self, target_frame, update_controller, update_target):

        current_frame = cmds.currentTime(q=True)

        if target_frame is not None:

            if target_frame != current_frame:
                cmds.currentTime(target_frame)

        if update_controller and self.controller:

            self.controller_translate = \
                cmds.xform(self.controller, q=True, ws=False, t=True)

            self.controller_rotate = \
                cmds.xform(self.controller, q=True, ws=False, ro=True)

            self.controller_scale = \
                cmds.xform(self.controller, q=True, ws=False, r=True, s=True)

        if update_target and self.target:

            self.target_translate = \
                cmds.xform(self.target, q=True, ws=False, t=True)

            self.target_rotate = \
                cmds.xform(self.target, q=True, ws=False, ro=True)

            self.target_scale = \
                cmds.xform(self.target, q=True, ws=False, r=True, s=True)

    # ==================================================
    def __update_base(self, update_controller, update_target):

        self.controller_translate_base = self.controller_translate
        self.controller_rotate_base = self.controller_rotate
        self.controller_scale_base = self.controller_scale

        self.target_translate_base = self.target_translate
        self.target_rotate_base = self.target_rotate
        self.target_scale_base = self.target_scale

        if self.animation_layer_name:

            if cmds.animLayer(self.animation_layer_name, q=True, exists=True):

                is_anim_layer_mute = cmds.animLayer(
                    self.animation_layer_name, q=True, mute=True)

                if not is_anim_layer_mute:
                    cmds.animLayer(
                        self.animation_layer_name, e=True, mute=True)

                if update_controller and self.controller:

                    self.controller_translate_base = \
                        cmds.xform(self.controller, q=True, ws=False, t=True)

                    self.controller_rotate_base = \
                        cmds.xform(self.controller, q=True, ws=False, ro=True)

                    self.controller_scale_base = \
                        cmds.xform(self.controller, q=True, ws=False, r=True, s=True)

                if update_target and self.target:

                    self.target_translate_base = \
                        cmds.xform(self.target, q=True, ws=False, t=True)

                    self.target_rotate_base = \
                        cmds.xform(self.target, q=True, ws=False, ro=True)

                    self.target_scale_base = \
                        cmds.xform(self.target, q=True, ws=False, r=True, s=True)

                if not is_anim_layer_mute:
                    cmds.animLayer(
                        self.animation_layer_name, e=True, mute=False)

                return

        if not self.base_controller_info_item:
            return

        if update_controller:

            self.controller_translate_base = \
                self.base_controller_info_item.controller_translate

            self.controller_rotate_base = \
                self.base_controller_info_item.controller_rotate

            self.controller_scale_base = \
                self.base_controller_info_item.controller_scale

        if update_target:

            self.target_translate_base = \
                self.base_controller_info_item.target_translate

            self.target_rotate_base = \
                self.base_controller_info_item.target_rotate

            self.target_scale_base = \
                self.base_controller_info_item.target_scale

    # ==================================================
    def __update_offset(self, update_controller, update_target):

        if update_controller:

            if self.controller_translate and self.controller_translate_base:

                self.controller_translate_offset = base_utility.vector.sub(
                    self.controller_translate, self.controller_translate_base
                )

                # if self.translate_offset_multiply:

                #     self.controller_translate_offset = base_utility.vector.multiply(
                #         self.controller_translate_offset, self.translate_offset_multiply
                #     )

                # self.controller_translate = base_utility.vector.add(
                #     self.controller_translate_base, self.controller_translate_offset
                # )

            if self.controller_rotate and self.controller_rotate_base:

                self.controller_rotate_offset = base_utility.vector.sub(
                    self.controller_rotate, self.controller_rotate_base
                )

                # if self.rotate_offset_multiply:

                #     self.controller_rotate_offset = base_utility.vector.multiply(
                #         self.controller_rotate_offset, self.rotate_offset_multiply
                #     )

                # self.controller_rotate = base_utility.vector.add(
                #     self.controller_rotate_base, self.controller_rotate_offset
                # )

            if self.controller_scale and self.controller_scale_base:

                self.controller_scale_offset = base_utility.vector.sub(
                    self.controller_scale, self.controller_scale_base
                )

                # if self.scale_offset_multiply:

                #     self.controller_scale_offset = base_utility.vector.multiply(
                #         self.controller_scale_offset, self.scale_offset_multiply
                #     )

                # self.controller_translate = base_utility.vector.add(
                #     self.controller_scale_base, self.controller_scale_offset
                # )

        if update_target:

            if self.target_translate and self.target_translate_base:

                self.target_translate_offset = base_utility.vector.sub(
                    self.target_translate, self.target_translate_base
                )

                # if self.translate_offset_multiply:

                #     self.target_translate_offset = base_utility.vector.multiply(
                #         self.target_translate_offset, self.translate_offset_multiply
                #     )

                #     self.target_translate = base_utility.vector.add(
                #         self.target_translate_base, self.target_translate_offset
                #     )

            if self.target_rotate and self.target_rotate_base:

                self.target_rotate_offset = base_utility.vector.sub(
                    self.target_rotate, self.target_rotate_base
                )

                # if self.rotate_offset_multiply:

                #     self.target_rotate_offset = base_utility.vector.multiply(
                #         self.target_rotate_offset, self.rotate_offset_multiply
                #     )

                #     self.controller_translate = base_utility.vector.add(
                #         self.target_rotate_base, self.target_rotate_offset
                #     )

            if self.target_scale and self.target_scale_base:

                self.target_scale_offset = base_utility.vector.sub(
                    self.target_scale, self.target_scale_base
                )

                # if self.scale_offset_multiply:

                #     self.target_scale_offset = base_utility.vector.multiply(
                #         self.target_scale_offset, self.scale_offset_multiply
                #     )

                #     self.controller_translate = base_utility.vector.add(
                #         self.target_scale_base, self.target_scale_offset
                #     )

    # ==================================================
    def get_clone(self):

        clone_info_item = TargetControllerInfoItem(self.root)

        clone_info_item.part = self.part

        clone_info_item.controller = self.controller
        clone_info_item.controller_name = self.controller_name

        clone_info_item.target = self.target
        clone_info_item.target_name = self.target_name

        clone_info_item.driver = self.driver
        clone_info_item.driver_name = self.driver_name

        clone_info_item.animation_layer_name = self.animation_layer_name

        if self.controller_translate:
            clone_info_item.controller_translate = self.controller_translate[:]

        if self.controller_rotate:
            clone_info_item.controller_rotate = self.controller_rotate[:]

        if self.controller_scale:
            clone_info_item.controller_scale = self.controller_scale[:]

        if self.controller_translate_base:
            clone_info_item.controller_translate_base = self.controller_translate_base[:]

        if self.controller_rotate_base:
            clone_info_item.controller_rotate_base = self.controller_rotate_base[:]

        if self.controller_scale_base:
            clone_info_item.controller_scale_base = self.controller_scale_base[:]

        if self.controller_translate_offset:
            clone_info_item.controller_translate_offset = self.controller_translate_offset[:]

        if self.controller_rotate_offset:
            clone_info_item.controller_rotate_offset = self.controller_rotate_offset[:]

        if self.controller_scale_offset:
            clone_info_item.controller_scale_offset = self.controller_scale_offset[:]

        if self.target_translate:
            clone_info_item.target_translate = self.target_translate[:]

        if self.target_rotate:
            clone_info_item.target_rotate = self.target_rotate[:]

        if self.target_scale:
            clone_info_item.target_scale = self.target_scale[:]

        if self.target_translate_base:
            clone_info_item.target_translate_base = self.target_translate_base[:]

        if self.target_rotate_base:
            clone_info_item.target_rotate_base = self.target_rotate_base[:]

        if self.target_scale_base:
            clone_info_item.target_scale_base = self.target_scale_base[:]

        if self.target_translate_offset:
            clone_info_item.target_translate_offset = self.target_translate_offset[:]

        if self.target_rotate_offset:
            clone_info_item.target_rotate_offset = self.target_rotate_offset[:]

        if self.target_scale_offset:
            clone_info_item.target_scale_offset = self.target_scale_offset[:]

        return clone_info_item

    # ==================================================
    def set_transform(self, is_controller, bake_frame, is_base, multiply_value):

        this_target = None

        this_translate = None
        this_rotate = None
        this_scale = None

        this_translate_offset = None
        this_rotate_offset = None
        this_scale_offset = None

        self.__update_controller_and_target()

        if is_controller:

            this_target = self.controller

            if is_base:

                this_translate = self.controller_translate_base
                this_rotate = self.controller_rotate_base
                this_scale = self.controller_scale_base

            else:

                this_translate = self.controller_translate
                this_rotate = self.controller_rotate
                this_scale = self.controller_scale

            this_translate_offset = self.controller_translate_offset
            this_rotate_offset = self.controller_rotate_offset
            this_scale_offset = self.controller_scale_offset

        else:

            this_target = self.target

            if is_base:

                this_translate = self.target_translate_base
                this_rotate = self.target_rotate_base
                this_scale = self.target_scale_base

            else:

                this_translate = self.target_translate
                this_rotate = self.target_rotate
                this_scale = self.target_scale

            this_translate_offset = self.target_translate_offset
            this_rotate_offset = self.target_rotate_offset
            this_scale_offset = self.target_scale_offset

        if not this_target:
            return

        if not cmds.objExists(this_target):
            return

        if bake_frame is not None:

            current_frame = cmds.currentTime(q=True)

            if bake_frame != current_frame:
                cmds.currentTime(bake_frame)

        if this_translate:

            if multiply_value != 1.0 and this_translate_offset:

                this_offset = \
                    base_utility.vector.multiply_value(
                        this_translate_offset, multiply_value - 1.0)

                this_translate = \
                    base_utility.vector.add(this_translate, this_offset)

            cmds.xform(this_target, ws=False, t=this_translate)

            if bake_frame is not None:

                cmds.setKeyframe(this_target + '.tx')
                cmds.setKeyframe(this_target + '.ty')
                cmds.setKeyframe(this_target + '.tz')

        if this_rotate:

            if multiply_value != 1.0 and this_rotate_offset:

                this_offset = \
                    base_utility.vector.multiply_value(
                        this_rotate_offset, multiply_value - 1.0)

                this_rotate = \
                    base_utility.vector.add(this_rotate, this_offset)

            cmds.xform(this_target, ws=False, ro=this_rotate)

            if bake_frame is not None:

                cmds.setKeyframe(this_target + '.rx')
                cmds.setKeyframe(this_target + '.ry')
                cmds.setKeyframe(this_target + '.rz')

        if this_scale:

            if multiply_value != 1.0 and this_scale_offset:

                this_offset = \
                    base_utility.vector.multiply_value(
                        this_scale_offset, multiply_value - 1.0)

                this_scale = \
                    base_utility.vector.add(this_scale, this_offset)

            cmds.xform(this_target, ws=False, s=this_scale)

            if bake_frame is not None:

                cmds.setKeyframe(this_target + '.sx')
                cmds.setKeyframe(this_target + '.sy')
                cmds.setKeyframe(this_target + '.sz')

    # ==================================================
    def write_info(self, parent_element):

        this_root_element = base_utility.xml.add_element(
            parent_element, 'ControllerInfoItem', None)

        base_utility.xml.add_element(
            this_root_element, 'Controller', self.controller)

        base_utility.xml.add_element(
            this_root_element, 'ControllerName', self.controller_name)

        base_utility.xml.add_element(
            this_root_element, 'ControllerTranslate', self.controller_translate)

        base_utility.xml.add_element(
            this_root_element, 'ControllerRotate', self.controller_rotate)

        base_utility.xml.add_element(
            this_root_element, 'ControllerScale', self.controller_scale)

        base_utility.xml.add_element(
            this_root_element, 'ControllerTranslateBase', self.controller_translate_base)

        base_utility.xml.add_element(
            this_root_element, 'ControllerRotateBase', self.controller_rotate_base)

        base_utility.xml.add_element(
            this_root_element, 'ControllerScaleBase', self.controller_scale_base)

        base_utility.xml.add_element(
            this_root_element, 'Target', self.target)

        base_utility.xml.add_element(
            this_root_element, 'TargetName', self.target_name)

        base_utility.xml.add_element(
            this_root_element, 'TargetTranslate', self.target_translate)

        base_utility.xml.add_element(
            this_root_element, 'TargetRotate', self.target_rotate)

        base_utility.xml.add_element(
            this_root_element, 'TargetScale', self.target_scale)

        base_utility.xml.add_element(
            this_root_element, 'TargetTranslateBase', self.target_translate_base)

        base_utility.xml.add_element(
            this_root_element, 'TargetRotateBase', self.target_rotate_base)

        base_utility.xml.add_element(
            this_root_element, 'TargetScaleBase', self.target_scale_base)

    # ===============================================
    def update_info_from_xml(self, parent_element):

        self.controller_translate = \
            base_utility.xml.get_element_value(
                parent_element, 'ControllerTranslate')

        self.controller_translate = base_utility.list.convert_from_string(
            self.controller_translate, float
        )

        self.controller_rotate = \
            base_utility.xml.get_element_value(
                parent_element, 'ControllerRotate')

        self.controller_rotate = base_utility.list.convert_from_string(
            self.controller_rotate, float
        )

        self.controller_scale = \
            base_utility.xml.get_element_value(
                parent_element, 'ControllerScale')

        self.controller_scale = base_utility.list.convert_from_string(
            self.controller_scale, float
        )

        self.controller_translate_base = \
            base_utility.xml.get_element_value(
                parent_element, 'ControllerTranslateBase')

        self.controller_translate_base = base_utility.list.convert_from_string(
            self.controller_translate_base, float
        )

        self.controller_rotate_base = \
            base_utility.xml.get_element_value(
                parent_element, 'ControllerRotateBase')

        self.controller_rotate_base = base_utility.list.convert_from_string(
            self.controller_rotate_base, float
        )

        self.controller_scale_base = \
            base_utility.xml.get_element_value(
                parent_element, 'ControllerScaleBase')

        self.controller_scale_base = base_utility.list.convert_from_string(
            self.controller_scale_base, float
        )

        self.target_translate = \
            base_utility.xml.get_element_value(
                parent_element, 'TargetTranslate')

        self.target_translate = base_utility.list.convert_from_string(
            self.target_translate, float
        )

        self.target_rotate = \
            base_utility.xml.get_element_value(
                parent_element, 'TargetRotate')

        self.target_rotate = base_utility.list.convert_from_string(
            self.target_rotate, float
        )

        self.target_scale = \
            base_utility.xml.get_element_value(
                parent_element, 'TargetScale')

        self.target_scale = base_utility.list.convert_from_string(
            self.target_scale, float
        )

        self.target_translate_base = \
            base_utility.xml.get_element_value(
                parent_element, 'TargetTranslateBase')

        self.target_translate_base = base_utility.list.convert_from_string(
            self.target_translate_base, float
        )

        self.target_rotate_base = \
            base_utility.xml.get_element_value(
                parent_element, 'TargetRotateBase')

        self.target_rotate_base = base_utility.list.convert_from_string(
            self.target_rotate_base, float
        )

        self.target_scale_base = \
            base_utility.xml.get_element_value(
                parent_element, 'TargetScaleBase')

        self.target_scale_base = base_utility.list.convert_from_string(
            self.target_scale_base, float
        )

        self.translate_offset_multiply = None
        self.rotate_offset_multiply = None
        self.scale_offset_multiply = None

        self.__update_controller_and_target()
        self.__update_offset(True, True)

    # ==================================================
    def __update_driver(self):

        self.driver = base_utility.node.search(
            self.driver_name, self.root.driver_root_name, 'transform'
        )

    # ===============================================
    def _delete_driver_attribute(self, driver_attribute):

        self.__update_driver()

        if not self.driver:
            return

        base_utility.attribute.delete(
            self.driver, driver_attribute
        )

    # ==================================================
    def _add_driver_attribute(self, driver_attribute, attribute_type, min_value, max_value):

        if not driver_attribute:
            return

        self.__update_driver()

        if not self.driver:
            return

        if attribute_type == int:

            base_utility.attribute.add(
                self.driver,
                driver_attribute,
                0
            )

        else:

            base_utility.attribute.add(
                self.driver,
                driver_attribute,
                0.0
            )

        cmds.setAttr(
            self.driver + '.' + driver_attribute,
            cb=False, k=True, l=False)

        cmds.addAttr(
            self.driver + '.' + driver_attribute,
            e=True,
            minValue=min_value,
            maxValue=max_value
        )

    # ==================================================
    def _set_driven_attribute_value(self, driver_attribute, driven_value):

        if not self.driver:
            return

        if not driver_attribute:
            return

        base_utility.attribute.set_value(
            self.driver, driver_attribute, driven_value
        )

    # ==================================================
    def _connect_driver_to_driven(self, driver_attribute, is_controller):

        if not self.driver:
            return

        if not driver_attribute:
            return

        if not cmds.objExists(self.driver):
            return

        self.__update_controller_and_target()

        this_target = None

        this_translate_offset = None
        this_rotate_offset = None
        this_scale_offset = None

        if is_controller:

            self.__update_offset(True, False)

            this_target = self.controller

            this_translate_offset = self.controller_translate_offset
            this_rotate_offset = self.controller_rotate_offset
            this_scale_offset = self.controller_scale_offset

        else:

            self.__update_offset(False, True)

            this_target = self.target

            this_translate_offset = self.target_translate_offset
            this_rotate_offset = self.target_rotate_offset
            this_scale_offset = self.target_scale_offset

        if not this_target:
            return

        if not cmds.objExists(this_target):
            return

        attr_name_list = []

        # モーション班の作業に支障がでるため、耳の移動と回転は必ずドリブンキーのセット対象に含む（TDN-7091）
        if this_translate_offset:

            if this_target.find('Ear_') >= 0:

                attr_name_list.append('translateX')
                attr_name_list.append('translateY')
                attr_name_list.append('translateZ')

            else:

                if this_translate_offset[0] != 0:
                    attr_name_list.append('translateX')

                if this_translate_offset[1] != 0:
                    attr_name_list.append('translateY')

                if this_translate_offset[2] != 0:
                    attr_name_list.append('translateZ')

        if this_rotate_offset:

            if this_target.find('Ear_') >= 0:

                attr_name_list.append('rotateX')
                attr_name_list.append('rotateY')
                attr_name_list.append('rotateZ')

            else:
                if this_rotate_offset[0] != 0:
                    attr_name_list.append('rotateX')

                if this_rotate_offset[1] != 0:
                    attr_name_list.append('rotateY')

                if this_rotate_offset[2] != 0:
                    attr_name_list.append('rotateZ')

        if this_scale_offset:

            if this_scale_offset[0] != 0:
                attr_name_list.append('scaleX')

            if this_scale_offset[1] != 0:
                attr_name_list.append('scaleY')

            if this_scale_offset[2] != 0:
                attr_name_list.append('scaleZ')

        if not attr_name_list:
            return

        for attr_name in attr_name_list:
            cmds.setDrivenKeyframe(
                this_target + '.' + attr_name,
                cd=self.driver + '.' + driver_attribute, itt='linear', ott='linear')
