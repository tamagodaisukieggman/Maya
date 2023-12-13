# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
"""
キャラインフォからオブジェクトを追加
"""

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import maya.cmds as cmds

from ....farm_common.classes.info import chara_info


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AddCharaInfoObj(object):

    # ==================================================
    def __init__(self, data_option={}):
        """
        """

        self.chara_info = None

        self.joint_scale_dict = {}

        self.is_ready = False

        self.data_option = data_option

    # ==================================================
    def __initialize(self):
        """
        """

        self.is_ready = False

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(data_option=self.data_option)
        if not self.chara_info.exists:
            return

        if not self.chara_info.part_info.exists:
            return

        joint_list = self.chara_info.part_info.joint_list

        for joint in joint_list:

            if not cmds.objExists(joint):
                continue

            joint_scale = cmds.xform(joint, q=True, r=True, s=True)

            if not joint_scale == [1, 1, 1]:
                self.joint_scale_dict[joint] = joint_scale

        self.is_ready = True

    # ==================================================
    def add_obj(self, type_name, short_name, position=[0, 0, 0], rotate=[0, 0, 0], is_world=False, should_reset_scale=True, should_init=False):
        """
        """

        self.__initialize()

        if not self.is_ready:
            return

        target_info_list = None

        if type_name == 'joint':
            target_info_list = self.chara_info.part_info.joint_list
        elif type_name == 'locator':
            target_info_list = self.chara_info.part_info.locator_list

        if not target_info_list:
            return

        this_obj_path = self.__get_target_obj_path(target_info_list, short_name)

        if not this_obj_path:
            return

        # 既にある場合は何もしないか、新規で作り直すかで分岐
        if cmds.objExists(this_obj_path):
            if should_init:
                cmds.delete(this_obj_path)
            else:
                return

        this_parent_path = self.__get_parent_obj_path(this_obj_path)

        if not this_parent_path == '' and not cmds.objExists(this_parent_path):
            return

        new_obj = None

        if type_name == 'joint':
            new_obj = '|' + cmds.joint(n=short_name)
        elif type_name == 'locator':
            new_obj = '|' + cmds.spaceLocator(n=short_name)[0]

        if not new_obj:
            return

        result_obj = None

        if this_parent_path:
            result_obj = cmds.parent(new_obj, this_parent_path)[0]
        else:
            result_obj = new_obj

        if should_reset_scale:
            # 一度全jointのスケールを切ってオフセットを代入
            # 諸々の処理をした後スケールは1に戻す
            self.__clear_original_joint_scale()

        cmds.xform(result_obj, ws=is_world, t=position, ro=rotate)

        if should_reset_scale:
            self.__retrive_original_joint_scale()

        cmds.xform(result_obj, s=[1, 1, 1])

        return result_obj

    # ==================================================
    def __get_target_obj_path(self, target_list, short_name):
        """
        """

        target_obj_path = ''

        for obj in target_list:

            if not obj.endswith(short_name):
                continue

            target_obj_path = obj
            break

        return target_obj_path

    # ==================================================
    def __get_parent_obj_path(self, long_name):
        """
        """

        if not long_name:
            return

        short_name = long_name.split('|')[-1]
        parent_path = long_name.replace('|{}'.format(short_name), '')

        return parent_path

    # ==================================================
    def __clear_original_joint_scale(self):
        """
        """

        if not self.joint_scale_dict:
            return

        for joint in self.joint_scale_dict:

            if not cmds.objExists(joint):
                continue

            cmds.xform(joint, s=[1, 1, 1])
    
    # ==================================================
    def __retrive_original_joint_scale(self):
        """
        """

        if not self.joint_scale_dict:
            return

        for joint in self.joint_scale_dict:

            if not cmds.objExists(joint):
                continue
            
            original_scale = self.joint_scale_dict[joint]

            cmds.xform(joint, s=original_scale)
