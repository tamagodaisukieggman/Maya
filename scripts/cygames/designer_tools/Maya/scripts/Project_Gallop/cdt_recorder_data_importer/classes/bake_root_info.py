# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
    from builtins import range
    from builtins import object
except Exception:
    pass

import os
import glob
import re
from xml.etree import cElementTree

import maya.cmds as cmds

from .. import common
from . import bake_transform_info

reload(common)
reload(bake_transform_info)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeRootInfo(object):

    # ==================================================
    def __init__(self, main):

        self.exists = False

        self.main = main

        self.target_data_dir_path = None

        self.time_data_path = None
        self.transform_info_data_path_list = None

        self.target_transform_list = None

        self.target_transform_dict = None

        self.fps = 0

        self.scale_factor = 100

        self.bake_start_frame = 0
        self.bake_end_frame = 0

        self.sampling_start_frame = 0
        self.sampling_end_frame = 0

        self.sampling_start_time = 0
        self.sampling_end_time = 0

        self.sampling_time_offset = 0.25

        self.transform_filter_list = None
        self.attr_filter_list = None

        self.max_progress = 5
        self.current_progress = 0

        self.time_start_index = -1
        self.time_list = None
        self.frame_list = None

        self.transform_info_list = None

        self.rotate_max_position = [-10000000] * 3
        self.rotate_min_position = [10000000] * 3
        self.rotate_position_offset = [0] * 3

        # Unityのノード名ではなく、代わりにMayaのノード名でXMLの名前と照合する為の置換リスト
        self.another_platform_replacement_info_dict = {}

    # ==================================================
    def bake(self):

        common.utility.maya.ui.progressbar.start('Import Recorder Data')

        self.__bake_base()
        self.__finalize_for_bake()

        common.utility.maya.ui.progressbar.end()

    # ==================================================
    def __bake_base(self):

        self.__read_xml()

        if not self.exists:
            return

        self.__initialize_for_bake()

        if not self.exists:
            return

        self.__initialize_for_bake_later()

        if not self.exists:
            return

        self.__bake_transform()

        if not self.exists:
            return

    # ==================================================
    def __read_xml(self):

        self.exists = False

        if not os.path.isdir(self.target_data_dir_path):
            return

        self.__create_target_transform_dict()

        if not self.target_transform_dict:
            return

        self.__create_fps()
        self.__create_frame_and_time()
        self.__create_filter()

        self.__create_xml_path()

        if self.time_data_path is None:
            return

        if not self.transform_info_data_path_list:
            return

        self.__read_time_data()

        if not self.time_list:
            return

        self.__read_transform_info_data()

        if not self.exists:
            return

        if not self.transform_info_list:
            return

        self.exists = True

    # ==================================================
    def __create_target_transform_dict(self):

        self.target_transform_dict = {}

        if not self.target_transform_list:
            return

        # 存在しないアイテムが含まれていた場合には処理を中止する
        invalid_items = []
        for target_transform in self.target_transform_list:
            if not cmds.objExists(target_transform):
                invalid_items.append(target_transform)

        if invalid_items:
            cmds.warning('{0}が存在しません'.format(invalid_items))
            return

        cmds.select(cl=True)
        cmds.select(self.target_transform_list, r=True)
        cmds.select(hi=True)

        all_target_transform_list = cmds.ls(sl=True, l=True, typ='transform')

        if not all_target_transform_list:
            return

        for target_transform in all_target_transform_list:

            this_name = target_transform.split('|')[-1]
            this_name = this_name.split(':')[-1]

            if this_name not in self.target_transform_dict:
                self.target_transform_dict[this_name] = []

            self.target_transform_dict[this_name].append(target_transform)

        if not self.target_transform_dict:
            return

    # ==================================================
    def __create_fps(self):

        time_string = cmds.currentUnit(q=True, t=True)

        if time_string.find('fps') >= 0:
            self.fps = float(time_string.replace('fps', ''))
        elif time_string.find('ntsc') >= 0:
            self.fps = 30
        elif time_string.find('ntscf') >= 0:
            self.fps = 60
        elif time_string.find('game') >= 0:
            self.fps = 15
        elif time_string.find('film') >= 0:
            self.fps = 24
        elif time_string.find('pal') >= 0:
            self.fps = 25
        elif time_string.find('show') >= 0:
            self.fps = 48
        elif time_string.find('palf') >= 0:
            self.fps = 50
        else:
            self.fps = 30

    # ==================================================
    def __create_frame_and_time(self):

        self.bake_start_frame = min(self.bake_start_frame, self.bake_end_frame)

        if self.bake_start_frame == 0 and self.bake_end_frame == 0:
            self.bake_start_frame = 0
            self.bake_end_frame = 1000000

        self.sampling_start_frame = max(0, self.sampling_start_frame)

        self.sampling_end_frame = self.sampling_start_frame + \
            self.bake_end_frame - self.bake_start_frame

        self.sampling_start_time = self.sampling_start_frame / self.fps
        self.sampling_end_time = self.sampling_end_frame / self.fps

    # ==================================================
    def __create_filter(self):

        if self.transform_filter_list is None:
            self.transform_filter_list = []

        if self.attr_filter_list is None:
            self.attr_filter_list = []

        max_length = -10000

        if len(self.transform_filter_list) > max_length:
            max_length = len(self.transform_filter_list)

        if len(self.attr_filter_list) > max_length:
            max_length = len(self.attr_filter_list)

        self.transform_filter_list = \
            common.utility.base.list.get_same_length_list(
                self.transform_filter_list, max_length, '')

        self.attr_filter_list = \
            common.utility.base.list.get_same_length_list(
                self.attr_filter_list, max_length, '')

    # ==================================================
    def __create_xml_path(self):

        self.time_data_path = None
        self.transform_info_data_path_list = []

        file_list = glob.glob(self.target_data_dir_path + '/*')

        if not file_list:
            return

        for file in file_list:

            file_name = os.path.basename(file)

            if file_name.find('TimeList') >= 0:
                self.time_data_path = file

            elif file_name.find('TransformInfo') >= 0:
                self.transform_info_data_path_list.append(file)

    # ==================================================
    def __read_time_data(self):

        self.time_list = []

        elementTree = cElementTree.parse(self.time_data_path)

        if elementTree is None:
            return

        root_element = elementTree.getroot()

        if root_element is None:
            return

        time_list_element = root_element.find('TimeList')

        if time_list_element is None:
            return

        time_element_list = list(time_list_element)

        if not time_element_list:
            return

        count = -1
        for time_element in time_element_list:
            count += 1

            this_time = float(time_element.attrib['Time'])

            if this_time < self.sampling_start_time - self.sampling_time_offset:
                continue

            if this_time > self.sampling_end_time + self.sampling_time_offset:
                break

            if self.time_start_index < 0:
                self.time_start_index = count

            self.time_list.append(this_time)

    # ==================================================
    def __read_transform_info_data(self):

        self.exists = False

        self.transform_info_list = []

        self.current_progress += 1

        count = -1
        for transform_info_xml_path in self.transform_info_data_path_list:
            count += 1

            if not common.utility.maya.ui.progressbar.update(
                "Read Transform Info",
                count + 1, len(self.transform_info_data_path_list),
                    self.current_progress, self.max_progress):
                return

            file_name = os.path.basename(transform_info_xml_path)

            matchobj = re.search('____.*\.', file_name)

            if matchobj is None:
                continue

            transform_name = matchobj.group()
            transform_name = transform_name.replace('____', '')
            transform_name = transform_name.replace('.', '')

            # Unityのノード名が別プラットフォーム置換リストに存在する場合は
            # Unityのノード名ではなくMayaのノード名で検索する
            if transform_name in list(self.another_platform_replacement_info_dict.keys()):
                transform_name = self.another_platform_replacement_info_dict.get(transform_name).get('maya_node')

            if transform_name not in self.target_transform_dict:
                continue

            elementTree = cElementTree.parse(transform_info_xml_path)

            if elementTree is None:
                continue

            root_element = elementTree.getroot()

            if root_element is None:
                continue

            transform_info_element = root_element.find('TransformInfo')

            if transform_info_element is None:
                continue

            # 対象のtransform名を別プラットフォーム置換リストで置換している場合があるため
            # transform Nameも書き換えておく
            transform_info_element.attrib['Name'] = transform_name

            new_transform_info = bake_transform_info.BakeTransformInfo(self)
            new_transform_info.read_xml(transform_info_element)

            if not new_transform_info.exists:
                continue

            self.transform_info_list.append(new_transform_info)

        self.exists = True

    # ==================================================
    def __bake(self):

        self.__initialize_for_bake()

        self.__initialize_for_bake_later()

        self.__bake_transform()

        self.__finalize_for_bake()

    # ==================================================
    def __initialize_for_bake(self):

        self.exists = False

        self.frame_list = []
        for time in self.time_list:
            self.frame_list.append(time * self.fps)

        cmds.currentTime(self.bake_start_frame)

        self.current_progress += 1

        count = -1
        for transform_info in self.transform_info_list:
            count += 1

            if not common.utility.maya.ui.progressbar.update(
                    "First init", count + 1, len(self.transform_info_list), self.current_progress, self.max_progress):
                return

            transform_info.initialize_for_bake()

        self.exists = True

    # ==================================================
    def __initialize_for_bake_later(self):

        self.exists = False

        self.rotate_position_offset[0] = \
            (self.rotate_min_position[0] + self.rotate_max_position[0]) * 0.5

        self.rotate_position_offset[1] = self.rotate_min_position[1]

        self.rotate_position_offset[2] = \
            (self.rotate_min_position[2] + self.rotate_max_position[2]) * 0.5

        self.current_progress += 1

        count = -1
        for transform_info in self.transform_info_list:
            count += 1

            if not common.utility.maya.ui.progressbar.update(
                    "Second init", count + 1, len(self.transform_info_list), self.current_progress, self.max_progress):
                return

            transform_info.initialize_for_bake_later()

        self.exists = True

    # ==================================================
    def __bake_transform(self):

        self.exists = False

        cmds.currentTime(self.bake_start_frame)

        self.current_progress += 1

        count = -1
        for frame in self.frame_list:
            count += 1

            if not common.utility.maya.ui.progressbar.update(
                    "Bake To Temp", count + 1, len(self.frame_list), self.current_progress, self.max_progress):
                return

            fix_frame = frame - self.sampling_start_frame + self.bake_start_frame

            for transform_info in self.transform_info_list:
                transform_info.bake_to_temp_transform(count, fix_frame)

        cmds.currentTime(self.bake_start_frame)

        bake_duration = self.bake_end_frame - self.bake_start_frame + 1

        self.current_progress += 1

        count = -1
        for bake_frame in range(self.bake_start_frame, self.bake_end_frame + 1):
            count += 1

            if not common.utility.maya.ui.progressbar.update(
                    "Bake To Target", count + 1, bake_duration, self.current_progress, self.max_progress):
                return

            for transform_info in self.transform_info_list:
                transform_info.bake_to_target(bake_frame)

        cmds.currentTime(self.bake_start_frame)

        self.exists = True

    # ==================================================
    def __finalize_for_bake(self):

        self.exists = False

        if self.transform_info_list:

            for transform_info in self.transform_info_list:
                transform_info.finalize_for_bake()

        self.exists = True
