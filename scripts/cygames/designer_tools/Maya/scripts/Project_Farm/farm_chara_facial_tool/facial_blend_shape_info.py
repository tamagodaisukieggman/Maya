# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import os
import sys
import re
import glob
import time

import maya.cmds as cmds
from maya import OpenMayaUI

from ..base_common import classes as base_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialBlendShapeInfo(object):

    # ===============================================
    def __init__(self):

        self.SHAPE_CSV_HEDER_STR = 'BlendShapeDictList'
        self.SHAPE_CSV_INDEX_LABEL = 'INDEX'
        self.SHAPE_CSV_TARGET_LABEL = 'SHAPE_TARGET'

        self.script_path = os.path.abspath(__file__)
        self.target_csv_path = os.path.dirname(self.script_path) + '/resources/facial_target.csv'
        self.csv_reader = base_class.csv_reader.CsvReader()

        self.blend_shape_item_list = None
        self.is_initialized = False

    # ===============================================
    def initialize(self):

        self.is_initialized = False

        self.blend_shape_item_list = []
        self.__create_shape_item()

        self.is_initialized = True

    # ===============================================
    def __create_shape_item(self):

        self.csv_reader.read(self.target_csv_path, 'utf-8')
        self.csv_reader.update(self.SHAPE_CSV_HEDER_STR, None, 1)

        shape_value_dict_list = self.csv_reader.get_value_dict_list()

        if not shape_value_dict_list:
            return

        for shape_value_dict in shape_value_dict_list:

            index = shape_value_dict[self.SHAPE_CSV_INDEX_LABEL]
            target = shape_value_dict[self.SHAPE_CSV_TARGET_LABEL]
            facial_type = self.__get_facial_type(target)

            this_item = BlendShapeItem()
            this_item.initialize(target, index, facial_type)

            self.blend_shape_item_list.append(this_item)

    # ===============================================
    def __get_facial_type(self, target):

        facial_type = 'facial'

        if target.startswith('eye_'):
            facial_type = 'look'

        if target.startswith('eyelight_'):
            facial_type = 'look'

        mouth_pattern = re.compile(r'^mouth_[aiueo]_\d{2}$')

        if mouth_pattern.match(target):
            print(target)
            facial_type = 'mouth'

        return facial_type


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BlendShapeItem(object):

    # ===============================================
    def __init__(self):

        self.target = ''
        self.index = -1
        self.facial_type = ''

        self.part = ''
        self.label = ''

    # ===============================================
    def initialize(self, target, index, facial_type):

        self.target = target
        self.index = index
        self.facial_type = facial_type

        self.part = self.target.split('_')[0]
        self.label = self.target.replace(self.part + '_', '')
