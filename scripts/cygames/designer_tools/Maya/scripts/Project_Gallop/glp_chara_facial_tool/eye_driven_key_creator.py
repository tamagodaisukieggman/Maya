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

import maya.cmds as cmds

from ..base_common import utility as base_utility


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EyeDrivenKeyCreator(object):

    # ===============================================
    def __init__(self, facial_target_info):

        self.target_info = facial_target_info

        self.eye_l_driver = None
        self.eye_l_driven = None

        self.eye_r_driver = None
        self.eye_r_driven = None

        self.eye_all_driver = None

        self.rig_head = 'Rig_head'
        self.facial_root = 'facial'

        self.is_check_data = False

        self.driven_key_attr_list = [
            'translateX',
            'translateY',
        ]

    # ===============================================
    def create_driven_key(self):

        if not self.target_info:
            return

        self.__check_data()

        if not self.is_check_data:
            return

        self.__create_driven_key_attribute()

        self.__reset_driver()

        range_x_l_facial_target_info_item = None
        range_y_l_facial_target_info_item = None
        range_x_r_facial_target_info_item = None
        range_y_r_facial_target_info_item = None

        for info_item in \
                self.target_info.info_item_list:

            if not info_item.label:
                continue

            if info_item.label == "XRange" and info_item.part == 'Eye_L':
                range_x_l_facial_target_info_item = info_item
            elif info_item.label == "YRange" and info_item.part == 'Eye_L':
                range_y_l_facial_target_info_item = info_item
            elif info_item.label == "XRange" and info_item.part == 'Eye_R':
                range_x_r_facial_target_info_item = info_item
            elif info_item.label == "YRange" and info_item.part == 'Eye_R':
                range_y_r_facial_target_info_item = info_item

        self.__set_eye_driven_key(range_x_l_facial_target_info_item,
                                  range_x_r_facial_target_info_item,
                                  self.eye_l_driver,
                                  'translateX',
                                  self.eye_l_driven,
                                  True
                                  )

        self.__set_eye_driven_key(range_y_l_facial_target_info_item,
                                  range_y_r_facial_target_info_item,
                                  self.eye_l_driver,
                                  'translateY',
                                  self.eye_l_driven,
                                  False
                                  )

        self.__set_eye_driven_key(range_x_l_facial_target_info_item,
                                  range_x_r_facial_target_info_item,
                                  self.eye_r_driver,
                                  'translateX',
                                  self.eye_r_driven,
                                  False
                                  )

        self.__set_eye_driven_key(range_y_l_facial_target_info_item,
                                  range_y_r_facial_target_info_item,
                                  self.eye_r_driver,
                                  'translateY',
                                  self.eye_r_driven,
                                  False
                                  )

        self.__set_eye_driven_key(range_x_l_facial_target_info_item,
                                  range_x_r_facial_target_info_item,
                                  self.eye_all_driver,
                                  'translateX',
                                  self.eye_l_driven,
                                  True
                                  )

        self.__set_eye_driven_key(range_x_l_facial_target_info_item,
                                  range_x_r_facial_target_info_item,
                                  self.eye_all_driver,
                                  'translateX',
                                  self.eye_r_driven,
                                  False
                                  )

        self.__set_eye_driven_key(range_y_l_facial_target_info_item,
                                  range_y_r_facial_target_info_item,
                                  self.eye_all_driver,
                                  'translateY',
                                  self.eye_l_driven,
                                  False
                                  )

        self.__set_eye_driven_key(range_y_l_facial_target_info_item,
                                  range_y_r_facial_target_info_item,
                                  self.eye_all_driver,
                                  'translateY',
                                  self.eye_r_driven,
                                  False
                                  )

        self.__reset_driver()

    # ===============================================
    def __check_data(self):

        self.is_check_data = False

        self.eye_l_driver = \
            base_utility.node.search(
                'Eyeball_L_Ctrl$', self.facial_root)

        self.eye_l_driven = \
            base_utility.node.search(
                'Eye_L_Ctrl$', self.rig_head)

        self.eye_r_driver = \
            base_utility.node.search(
                'Eyeball_R_Ctrl$', self.facial_root)

        self.eye_r_driven = \
            base_utility.node.search(
                'Eye_R_Ctrl$', self.rig_head)

        self.eye_all_driver = \
            base_utility.node.search(
                'Eyeball_all_Ctrl$', self.facial_root)

        if self.eye_l_driver is None:
            return

        if self.eye_l_driven is None:
            return

        if self.eye_r_driver is None:
            return

        if self.eye_r_driven is None:
            return

        if self.eye_all_driver is None:
            return

        self.is_check_data = True

    # ===============================================
    def __create_driven_key_attribute(self):

        self.__create_eye_driven_key_attribute(self.eye_l_driver)
        self.__create_eye_driven_key_attribute(self.eye_r_driver)
        self.__create_eye_driven_key_attribute(self.eye_all_driver)

    # ===============================================
    def __create_eye_driven_key_attribute(self, eye_driver):

        for driven_attr in self.driven_key_attr_list:

            base_utility.attribute.add(
                eye_driver, driven_attr, 0
            )

            cmds.setAttr(
                eye_driver + '.' + driven_attr,
                cb=False, k=True, l=False)

    # ===============================================
    def __set_eye_driven_key(self,
                             target_info_item_l,
                             target_info_item_r,
                             eye_driver,
                             driver_attr,
                             eye_diriven,
                             invert,
                             ):

        base_eye_driven_r = self.eye_r_driven
        base_eye_driven_l = self.eye_l_driven

        if invert:

            base_eye_driven_r = self.eye_l_driven
            base_eye_driven_l = self.eye_r_driven

        base_utility.attribute.set_value(
            eye_driver, driver_attr, 0
        )

        target_info_item_l.set_transform(True, False, False, True, 1)
        target_info_item_r.set_transform(True, False, False, True, 1)

        for target_attr in self.driven_key_attr_list:

            base_value = base_utility.attribute.get_value(
                base_eye_driven_r, target_attr
            )

            base_utility.attribute.set_value(
                eye_diriven, target_attr, base_value
            )

            cmds.setDrivenKeyframe(
                eye_diriven + '.' + target_attr,
                cd=eye_driver + '.' + driver_attr, itt='linear', ott='linear')

        base_utility.attribute.set_value(
            eye_driver, driver_attr, 1
        )

        target_info_item_l.set_transform(True, False, False, False, 1)
        target_info_item_r.set_transform(True, False, False, False, 1)

        for target_attr in self.driven_key_attr_list:

            base_value = base_utility.attribute.get_value(
                base_eye_driven_l, target_attr
            )

            base_utility.attribute.set_value(
                eye_diriven, target_attr, base_value
            )

            cmds.setDrivenKeyframe(
                eye_diriven + '.' + target_attr,
                cd=eye_driver + '.' + driver_attr, itt='linear', ott='linear')

        base_utility.attribute.set_value(
            eye_driver, driver_attr, -1
        )

        target_info_item_l.set_transform(True, False, False, False, 1)
        target_info_item_r.set_transform(True, False, False, False, 1)

        for target_attr in self.driven_key_attr_list:

            base_value = base_utility.attribute.get_value(
                base_eye_driven_r, target_attr
            )

            base_utility.attribute.set_value(
                eye_diriven, target_attr, base_value
            )

            cmds.setDrivenKeyframe(
                eye_diriven + '.' + target_attr,
                cd=eye_driver + '.' + driver_attr, itt='linear', ott='linear')

        self.__reset_driver()

    # ===============================================
    def __reset_driver(self):

        cmds.setAttr(self.eye_l_driver + '.translateX', 0)
        cmds.setAttr(self.eye_l_driver + '.translateY', 0)

        cmds.setAttr(self.eye_r_driver + '.translateX', 0)
        cmds.setAttr(self.eye_r_driver + '.translateY', 0)

        cmds.setAttr(self.eye_all_driver + '.translateX', 0)
        cmds.setAttr(self.eye_all_driver + '.translateY', 0)
