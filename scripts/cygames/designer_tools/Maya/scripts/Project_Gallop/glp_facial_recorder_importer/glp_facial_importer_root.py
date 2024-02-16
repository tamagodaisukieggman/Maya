# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from past.utils import old_div
    from builtins import object
except Exception:
    pass

import os
import re
import glob
import itertools
import sys

from xml.etree import cElementTree

import maya.cmds as cmds


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GlpFacialImporterRoot(object):

    # ===============================================
    def __init__(self):

        self.gui_root = None

        self.target_data_dir_path = None
        self.time_data_path = None
        self.driven_key_info_data_path_list = None

        self.record_time_list = None
        self.record_data_list = None

        self.fps = 0
        self.frame_offset = 0
        self.frame_time_dict_list = None

        self.log_list = None

        self.TARGET_NODE_DICT = {
            "EyeL": "Eye_L_Base_Ctrl",
            "EyeR": "Eye_R_Base_Ctrl",
            "EyebrowL": "Eyebrow_L_Base_Ctrl",
            "EyebrowR": "Eyebrow_R_Base_Ctrl",
            "Mouth": "Mouth_Base_Ctrl",
            "EarL0": "Ear_01_L_Ctrl",
            "EarL1": "Ear_02_L_Ctrl",
            "EarL2": "Ear_03_L_Ctrl",
            "EarR0": "Ear_01_R_Ctrl",
            "EarR1": "Ear_02_R_Ctrl",
            "EarR2": "Ear_03_R_Ctrl",
            "Cheek": "Cheek_Ctrl",
            "Eyehi": "Cheek_Ctrl",
        }

        self.FACIAL_CTRL_ROOT = '|facial_Ctrl'
        self.CHEEK_GROUP_TYPE = 'Cheek'
        self.CHEEK_DRIVEN0 = 'cheek0'
        self.CHEEK_DRIVEN1 = 'cheek1'

        self.EYEHI_GROUP_TYPE = 'Eyehi'
        self.EYEHI_DRIVEN_DICT = {
            'tearful': {'channel': 'namida', 'value': 1},
            'Teary': {'channel': 'hitomi', 'value': 1},
            'Twinkle': {'channel': 'hitomi', 'value': 2},
        }

        # 整数値で切り替えを行うチャンネル
        self.USE_FOR_FLAG_ATTR_LIST = [
            'namida', 'hitomi'
        ]

    # ==================================================
    def initialize(self, target_data_dir_path, gui_root=None):

        self.__init__()

        self.gui_root = gui_root
        self.target_data_dir_path = target_data_dir_path

        if not os.path.exists(self.target_data_dir_path):
            return

        self.__create_xml_path()

        if not self.time_data_path:
            return
        self.__read_time_data()

        if not self.driven_key_info_data_path_list:
            return
        self.__create_record_data_list()

        self.__create_fps()
        self.__create_frame_time_dict_list()

    # ==================================================
    def bake_facial(self, frame_offset=0, target_root=''):

        self.log_list = []

        if not self.record_data_list:
            return False

        if not frame_offset == 0:
            self.frame_offset = frame_offset

        facial_ctrl_root = self.FACIAL_CTRL_ROOT
        if target_root:
            facial_ctrl_root = target_root

        # initialize後にfps変更の可能性があるので直前に再取得
        self.__create_fps()
        self.__create_frame_time_dict_list()

        if not self.frame_time_dict_list:
            return

        for record_data in self.record_data_list:

            this_log = record_data.face_group_type

            this_target = self.TARGET_NODE_DICT.get(record_data.face_group_type)

            if not this_target:
                self.__add_log(this_log + ' : SKIP')
                continue

            # facial_ctrl_rootにネームスペースが入っていたら、取得
            name_space = ''
            match = re.search(r'\|(.+\:)', facial_ctrl_root)
            if match:
                name_space = match.group(1)

            this_target = '{}|{}{}'.format(facial_ctrl_root, name_space, this_target)

            if not cmds.objExists(this_target):
                self.__add_log(this_log + ' : SKIP')
                continue

            self.__bake_facial_from_record_data(record_data, this_target)
            self.__add_log(this_log + ' : FINISH')

        return True

    # ==================================================
    def __create_xml_path(self):

        self.time_data_path = None
        self.driven_key_info_data_path_list = []

        file_list = glob.glob(self.target_data_dir_path + '/*')

        if not file_list:
            return

        for file in file_list:

            file_name = os.path.basename(file)

            if file_name.find('TimeList') >= 0:
                self.time_data_path = file

            elif file_name.find('DrivenKeyInfo') >= 0:
                self.driven_key_info_data_path_list.append(file)

    # ==================================================
    def __read_time_data(self):

        self.record_time_list = []

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

        for time_element in time_element_list:

            this_time = float(time_element.attrib['Time'])

            self.record_time_list.append(this_time)

    # ==================================================
    def __create_record_data_list(self):
        """
        先に__read_time_data()が呼ばれていて、record_time_listは作成済みのものとする
        """

        self.record_data_list = []

        for driven_key_info_xml_path in self.driven_key_info_data_path_list:

            elementTree = cElementTree.parse(driven_key_info_xml_path)

            if elementTree is None:
                continue

            root_element = elementTree.getroot()

            if root_element is None:
                continue

            driven_key_info_element = root_element.find('DrivenKeyInfo')

            if driven_key_info_element is None:
                continue

            this_face_group_type = driven_key_info_element.get('FaceGroupType')

            this_key_info_dict_list = []

            # Unityの記録とMayaの仕組みを各パーツごとに合わせる
            # 最終的には{'チャネル名': 値}のdictのリストにする
            for key_info in root_element.iter('KeyInfo'):

                # 頬
                if this_face_group_type == self.CHEEK_GROUP_TYPE:

                    this_dict = {
                        self.CHEEK_DRIVEN0: 0,
                        self.CHEEK_DRIVEN1: 0,
                    }

                    index = key_info.get('index')

                    if index == '0':
                        this_dict[self.CHEEK_DRIVEN0] = 1
                    elif index == '1':
                        this_dict[self.CHEEK_DRIVEN1] = 1

                    this_key_info_dict_list.append(this_dict)

                # 瞳・涙
                elif this_face_group_type == self.EYEHI_GROUP_TYPE:

                    this_dict = {}

                    for rec_key, rec_val in list(key_info.items()):

                        deriven_dict = self.EYEHI_DRIVEN_DICT.get(rec_key)

                        if deriven_dict is None:
                            continue

                        if rec_val == '1':
                            this_dict[deriven_dict['channel']] = deriven_dict['value']
                        else:
                            # 既にそのチャネルに値が入っていたら0で上がかない
                            if not this_dict.get(deriven_dict['channel']):
                                this_dict[deriven_dict['channel']] = 0

                    this_key_info_dict_list.append(this_dict)

                # それ以外
                else:
                    this_key_info_dict_list.append(key_info.attrib)

            this_record_data = FacialRecordData()
            this_record_data.create(this_face_group_type, this_key_info_dict_list, self.record_time_list)

            self.record_data_list.append(this_record_data)

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
    def __create_frame_time_dict_list(self):

        self.frame_time_dict_list = []

        if not self.record_time_list or not self.fps:
            return

        frame = 0
        time = 0.0
        final_record_time = self.record_time_list[-1]

        while time <= final_record_time:

            this_dict = {}

            this_dict['frame'] = frame + self.frame_offset
            this_dict['time'] = time

            self.frame_time_dict_list.append(this_dict)

            frame += 1
            time += (1.0 / self.fps)

    # ==================================================
    def __bake_facial_from_record_data(self, record_data, target_node):

        if not record_data.record_key_dict_list:
            return

        # 全て同じキーを持っているはずなので最初のkeyのリストをとる
        drivenkey_list = list(record_data.record_key_dict_list[0].keys())
        attr_list = cmds.listAttr(target_node, unlocked=True, keyable=True)

        for drivenkey, time_dict in itertools.product(drivenkey_list, self.frame_time_dict_list):

            # ドリブンキーとアトリビュート名は同じはず
            if drivenkey not in attr_list:
                continue

            value = 0

            if drivenkey in self.USE_FOR_FLAG_ATTR_LIST:
                value = record_data.get_value(time_dict['time'], drivenkey, True)
            else:
                value = record_data.get_value(time_dict['time'], drivenkey, False)

            cmds.setKeyframe(target_node, at=drivenkey, v=value, t=time_dict['frame'])

    # ==================================================
    def __add_log(self, log):

        if self.log_list is None:
            self.log_list = []

        self.log_list.append(log)

        # uiがあればuiのログにも記載
        if self.gui_root:
            self.gui_root.write_log(log)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialRecordData(object):

    # ===============================================
    def __init__(self):

        self.face_group_type = ''
        self.record_key_dict_list = None
        self.record_time_list = None

    # ===============================================
    def create(self, face_group_type, record_key_dict_list, record_time_list):

        self.face_group_type = face_group_type
        self.record_key_dict_list = record_key_dict_list
        self.record_time_list = record_time_list

    # ===============================================
    def get_value(self, time, key, is_int_value=False):

        if not self.record_time_list or not self.record_key_dict_list:
            return 0.0

        # 負の値など、サンプリングした時間より前を指定した場合
        if time < self.record_time_list[0]:
            if is_int_value:
                return round(float(self.record_key_dict_list[0].get(key, 0.0)))
            else:
                return float(self.record_key_dict_list[0].get(key, 0.0))

        # サンプリングした時間より後を指定した場合
        if time > self.record_time_list[-1]:
            if is_int_value:
                return round(float(self.record_key_dict_list[-1].get(key, 0.0)))
            else:
                return float(self.record_key_dict_list[-1].get(key, 0.0))

        for i, (record_time, record_key_dict) in enumerate(zip(self.record_time_list, self.record_key_dict_list)):

            # サンプルした時間を指定した場合
            if time == record_time:
                if is_int_value:
                    return round(float(record_key_dict.get(key, 0.0)))
                else:
                    return float(record_key_dict.get(key, 0.0))

            # サンプル時間の間を指定した場合、線形補間
            if record_time > time:

                prev_value = float(self.record_key_dict_list[i - 1].get(key, 0.0))
                next_value = float(record_key_dict.get(key, 0.0))

                prev_time = self.record_time_list[i - 1]
                next_time = record_time

                record_interval = next_time - prev_time
                if sys.version_info.major == 2:
                    prev_ratio = (next_time - time) / record_interval
                    next_ratio = (time - prev_time) / record_interval
                else:
                    # for Maya 2022-
                    prev_ratio = old_div((next_time - time), record_interval)
                    next_ratio = old_div((time - prev_time), record_interval)

                if is_int_value:
                    return round((prev_value * prev_ratio) + (next_value * next_ratio))
                else:
                    return (prev_value * prev_ratio) + (next_value * next_ratio)


