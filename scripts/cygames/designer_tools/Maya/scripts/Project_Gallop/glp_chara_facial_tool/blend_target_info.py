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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BlendTargetInfo(object):

    # ===============================================
    def __init__(self):

        self.target_info = None

        self.csv_file_name = None

        self.script_file_path = None
        self.script_dir_path = None

        self.target_file_path = None
        self.target_file_name = None
        self.target_file_name_noext = None
        self.target_file_ext = None
        self.target_dir_path = None

        self.info_item_list = None

        self.is_init = False

        self.is_created = False

    # ===============================================
    def create_info_from_csv(self, target_info, csv_file_name):

        self.is_created = False

        current_path = cmds.file(q=True, sn=True)

        if not current_path:
            return

        if not os.path.isfile(current_path):
            return

        if not target_info:
            return

        if not csv_file_name:
            return

        self.target_info = target_info

        self.csv_file_name = csv_file_name

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.target_file_path = current_path.replace('\\', '/')
        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = os.path.dirname(self.target_file_path)
        self.target_file_name_noext, self.target_file_ext = \
            os.path.splitext(self.target_file_name)

        self.info_item_list = []

        self.__read_info()

        if not self.info_item_list:
            return

        self.is_created = True

    # ===============================================
    def __read_info(self):
        """
        facial_blend_info.csv を読み、self.info_item_list に BlendTargetInfoItem オブジェクトを格納
        """
        info_file_path = \
            self.target_dir_path + '/' + self.csv_file_name + '.csv'

        # 個々のキャラのscenesフォルダにfacial_blend_info.csvがあればそれを読むが、無ければツールのresoucesフォルダのcsv
        if not os.path.isfile(info_file_path):
            info_file_path = \
                self.script_dir_path + \
                '/resource/' + self.csv_file_name + '.csv'

        if not os.path.isfile(info_file_path):
            return

        with open(info_file_path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            for this_read_line_split in csv_reader:

                if len(this_read_line_split) < 7:
                    continue
                # csvのEnable列
                if this_read_line_split[0] != '1':
                    continue

                new_info_item = BlendTargetInfoItem(self)

                new_info_item.label = this_read_line_split[1]

                new_info_item.eyebrow_l_label = this_read_line_split[2]
                new_info_item.eyebrow_r_label = this_read_line_split[3]

                new_info_item.eye_l_label = this_read_line_split[4]
                new_info_item.eye_r_label = this_read_line_split[5]

                new_info_item.mouth_label = this_read_line_split[6]

                new_info_item.create_info()

                if not new_info_item.is_created:
                    continue

                self.info_item_list.append(new_info_item)

    # ===============================================
    def update_info(self, update_controller, update_target):

        if not self.is_created:
            return

        for info_item in self.info_item_list:
            info_item.update_info(update_controller, update_target)

    # ===============================================
    def set_transform(self, is_controller, frame):

        if not self.is_created:
            return

        min_frame = frame
        max_frame = frame + len(self.info_item_list) - 1

        cmds.playbackOptions(
            min=min_frame, max=max_frame, ast=min_frame, aet=max_frame)

        cmds.currentTime(frame)

        count = -1
        for info_item in self.info_item_list:

            count += 1

            info_item.set_transform(is_controller, frame + count, False)

        cmds.currentTime(frame)

    # ===============================================
    def delete_driven_key(self):

        if not self.is_created:
            return

        for info_item in self.info_item_list:

            info_item.delete_driven_key()

    # ===============================================
    def create_driven_key(self, is_controller):

        if not self.is_created:
            return

        max_count = len(self.info_item_list)

        count = -1
        for info_item in self.info_item_list:
            count += 1

            print("{0}/{1}".format(count, max_count))

            info_item.create_driven_key(is_controller)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BlendTargetInfoItem(object):

    # ===============================================
    def __init__(self, parent):

        self.parent = parent

        self.is_created = False

        self.label = None

        self.index = 0
        self.frame = 0

        self.eyebrow_l_label = None
        self.eyebrow_r_label = None

        self.eye_l_label = None
        self.eye_r_label = None

        self.mouth_label = None

        self.eyebrow_l_blend_info_list = None
        self.eyebrow_r_blend_info_list = None

        self.eye_l_blend_info_list = None
        self.eye_r_blend_info_list = None

        self.mouth_blend_info_list = None

        self.blend_controller_info_item_list = None

    # ===============================================
    def create_info(self):

        self.is_created = False

        if not self.label:
            return

        self.eyebrow_l_blend_info_list = self.__get_blend_list(
            self.eyebrow_l_label)
        self.eyebrow_r_blend_info_list = self.__get_blend_list(
            self.eyebrow_r_label)

        self.eye_l_blend_info_list = self.__get_blend_list(self.eye_l_label)
        self.eye_r_blend_info_list = self.__get_blend_list(self.eye_r_label)

        self.mouth_blend_info_list = self.__get_blend_list(self.mouth_label)

        self.is_created = True

    # ===============================================
    def __get_blend_list(self, target_label):

        if not target_label:
            return []

        if target_label.find('|') < 0:
            return [{'Label': target_label, 'Blend': 100}]

        result_list = []

        split_str_list = target_label.split('|')

        for split_str in split_str_list:

            this_split_str_list = split_str.split('__')

            if not this_split_str_list:
                continue

            this_label = this_split_str_list[0]
            this_blend = int(this_split_str_list[1])

            result_list.append({'Label': this_label, 'Blend': this_blend})

        return result_list

    # ===============================================
    def update_info(self, update_controller, update_target):

        this_target_info_item_clone = \
            self.parent.target_info.base_info_item.get_clone()

        self.blend_controller_info_item_list = \
            this_target_info_item_clone.controller_info_item_list

        self.__update_part(self.eyebrow_l_blend_info_list,
                           'Eyebrow_L', update_controller, update_target)
        self.__update_part(self.eyebrow_r_blend_info_list,
                           'Eyebrow_R', update_controller, update_target)

        self.__update_part(self.eye_l_blend_info_list,
                           'Eye_L', update_controller, update_target)
        self.__update_part(self.eye_r_blend_info_list,
                           'Eye_R', update_controller, update_target)

        self.__update_part(self.mouth_blend_info_list,
                           'Mouth', update_controller, update_target)

    # ===============================================
    def __update_part(self, blend_info_list, part, update_controller, update_target):

        if not blend_info_list:
            return

        for blend_info in blend_info_list:

            this_label = blend_info['Label']
            this_blend = blend_info['Blend'] / 100.0

            for info_item in self.parent.target_info.info_item_list:

                if info_item.part != part:
                    continue

                if info_item.label != this_label:
                    continue

                for p in range(len(self.blend_controller_info_item_list)):

                    this_blend_ctrl_info_item = self.blend_controller_info_item_list[p]
                    this_ctrl_info_item = info_item.controller_info_item_list[p]

                    if this_ctrl_info_item.part != part:
                        continue

                    if update_controller:

                        if not this_blend_ctrl_info_item.controller or not this_ctrl_info_item.controller:
                            continue

                        this_blend_ctrl_info_item.controller_translate = base_utility.vector.add(
                            this_blend_ctrl_info_item.controller_translate,
                            base_utility.vector.multiply_value(
                                this_ctrl_info_item.controller_translate_offset, this_blend)
                        )

                        this_blend_ctrl_info_item.controller_rotate = base_utility.vector.add(
                            this_blend_ctrl_info_item.controller_rotate,
                            base_utility.vector.multiply_value(
                                this_ctrl_info_item.controller_rotate_offset, this_blend)
                        )

                        this_blend_ctrl_info_item.controller_scale = base_utility.vector.add(
                            this_blend_ctrl_info_item.controller_scale,
                            base_utility.vector.multiply_value(
                                this_ctrl_info_item.controller_scale_offset, this_blend)
                        )

                    if update_target:

                        if not this_blend_ctrl_info_item.target or not this_ctrl_info_item.target:
                            continue

                        this_blend_ctrl_info_item.target_translate = base_utility.vector.add(
                            this_blend_ctrl_info_item.target_translate,
                            base_utility.vector.multiply_value(
                                this_ctrl_info_item.target_translate_offset, this_blend)
                        )

                        this_blend_ctrl_info_item.target_rotate = base_utility.vector.add(
                            this_blend_ctrl_info_item.target_rotate,
                            base_utility.vector.multiply_value(
                                this_ctrl_info_item.target_rotate_offset, this_blend)
                        )

                        this_blend_ctrl_info_item.target_scale = base_utility.vector.add(
                            this_blend_ctrl_info_item.target_scale,
                            base_utility.vector.multiply_value(
                                this_ctrl_info_item.target_scale_offset, this_blend)
                        )

    # ===============================================
    def set_transform(self, is_controller, frame, is_base):

        if not self.blend_controller_info_item_list:
            return

        for controller_info_item in self.blend_controller_info_item_list:

            controller_info_item.set_transform(
                is_controller, frame, is_base, 1.0)

    # ===============================================
    def delete_driven_key(self):

        if not self.blend_controller_info_item_list:
            return

        for blend_ctrl_info_item in self.blend_controller_info_item_list:

            blend_ctrl_info_item._delete_driver_attribute(self.label)

    # ===============================================
    def create_driven_key(self, is_controller):

        if not self.blend_controller_info_item_list:
            return

        for blend_ctrl_info_item in self.blend_controller_info_item_list:
            blend_ctrl_info_item._add_driver_attribute(self.label, float, 0, 1)

        for blend_ctrl_info_item in self.blend_controller_info_item_list:
            blend_ctrl_info_item._set_driven_attribute_value(self.label, 0)

        self.set_transform(is_controller, False, True)

        for blend_ctrl_info_item in self.blend_controller_info_item_list:

            blend_ctrl_info_item._connect_driver_to_driven(
                self.label, is_controller)

        for blend_ctrl_info_item in self.blend_controller_info_item_list:
            blend_ctrl_info_item._set_driven_attribute_value(self.label, 1)

        self.set_transform(is_controller, False, False)

        for blend_ctrl_info_item in self.blend_controller_info_item_list:

            blend_ctrl_info_item._connect_driver_to_driven(
                self.label, is_controller)

        for blend_ctrl_info_item in self.blend_controller_info_item_list:
            blend_ctrl_info_item._set_driven_attribute_value(self.label, 0)
