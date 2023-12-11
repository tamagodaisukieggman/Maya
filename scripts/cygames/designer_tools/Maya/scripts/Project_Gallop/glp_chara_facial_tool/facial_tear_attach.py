# -*- coding: utf-8 -*-

from __future__ import absolute_import
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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialTearAttach(object):

    # ===============================================
    def __init__(self):

        pass

    # ===============================================
    def attach(self):
        """
        アタッチ
        """

        self.check_data()

        if not self.exists:
            return

        self.create_attach_info_dict_list()

        if not self.attach_info_dict_list:
            return

        self.__attach_tear()

    # ===============================================
    def dettach(self):
        """
        デタッチ
        """

        self.check_data()

        if not self.exists:
            return

        self.create_attach_info_dict_list()

        if not self.attach_info_dict_list:
            return

        self.__dettach_tear()

    # ===============================================
    def check_data(self):
        """
        データチェック
        """

        self.exists = False

        current_path = cmds.file(q=True, sn=True)

        if not current_path:
            return

        if not os.path.isfile(current_path):
            return

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.target_file_path = \
            current_path.replace('\\', '/')

        self.target_file_name = \
            os.path.basename(self.target_file_path)

        self.target_dir_path = \
            os.path.dirname(self.target_file_path)

        self.target_file_name_noext, self.target_file_ext = \
            os.path.splitext(self.target_file_name)

        # モブはfaceフォルダが存在するため一階層深い
        if self.target_file_name.find('chr0001') >= 0 or self.target_file_name.find('chr0900') >= 0:
            face_dir_path = os.path.dirname(self.target_file_path)
            self.scene_dir_path = os.path.dirname(face_dir_path)
        else:
            self.scene_dir_path = \
                os.path.dirname(self.target_file_path)

        self.head_dir_path = \
            os.path.dirname(self.scene_dir_path)

        self.head_root_dir_path = \
            os.path.dirname(self.head_dir_path)

        self.root_dir_path = \
            os.path.dirname(self.head_root_dir_path)

        self.tear001_file_path = \
            self.root_dir_path + '/common/tear/tear001/scenes/mdl_chr_tear001.ma'

        if not os.path.isfile(self.tear001_file_path):
            return

        self.exists = True

    # ===============================================
    def create_attach_info_dict_list(self):
        """
        アタッチ情報の作成
        """

        self.attach_info_dict_list = []

        if os.path.isfile(self.tear001_file_path):

            info_dict_l = {
                'namespace': 'tear0001_L',
                'path': self.tear001_file_path,
                'attach_dict_list': [
                    {
                        'src_transform': '*1_L:joint000',
                        'dst_transform': 'Eye_tear_attach_02_L',
                    },
                    {
                        'src_transform': '*1_L:joint001',
                        'dst_transform': 'Eye_tear_attach_01_L',
                    },
                    {
                        'src_transform': '*1_L:joint002',
                        'dst_transform': 'Eye_tear_attach_03_L',
                    },
                ]
            }

            info_dict_r = {
                'namespace': 'tear0001_R',
                'path': self.tear001_file_path,
                'attach_dict_list': [
                    {
                        'src_transform': '*1_R:joint000',
                        'dst_transform': 'Eye_tear_attach_02_R',
                        'scale': [-1, 1, 1],
                        'scale_offset': [-1, 1, 1],
                    },
                    {
                        'src_transform': '*1_R:joint001',
                        'dst_transform': 'Eye_tear_attach_01_R',
                        'scale_offset': [1, 1, -1],
                    },
                    {
                        'src_transform': '*1_R:joint002',
                        'dst_transform': 'Eye_tear_attach_03_R',
                        'scale_offset': [1, 1, -1],
                    },
                ]
            }

            self.attach_info_dict_list.append(info_dict_l)
            self.attach_info_dict_list.append(info_dict_r)

    # ===============================================
    def __attach_tear(self):
        """
        tearモデルをアタッチ
        """

        if not self.attach_info_dict_list:
            return

        for attach_info_dict in self.attach_info_dict_list:

            self.__attach_tear_base(attach_info_dict)

    # ===============================================
    def __attach_tear_base(self, attach_info_dict):
        """
        tearモデルをアタッチ情報をもとにアタッチ
        """

        if not attach_info_dict:
            return

        file_path = attach_info_dict.get('path')

        if not file_path:
            return

        namespace = attach_info_dict.get('namespace')

        if not namespace:
            return

        attach_dict_list = attach_info_dict.get('attach_dict_list', [])

        base_utility.reference.unload(file_path, namespace)
        base_utility.reference.load(file_path, namespace)

        # コンストレイントの設定
        self.__set_constraint(attach_dict_list)

    # ===============================================
    def __dettach_tear(self):
        """
        tearモデルをデタッチ
        """

        if not self.attach_info_dict_list:
            return

        for attach_info_dict in self.attach_info_dict_list:

            self.__dettach_tear_base(attach_info_dict)

    # ===============================================
    def __dettach_tear_base(self, attach_info_dict):
        """
        tearモデルをアタッチ情報をもとにデタッチ
        """

        if not attach_info_dict:
            return

        # コンストレイントの消去
        attach_dict_list = attach_info_dict.get('attach_dict_list', [])
        self.__set_constraint(attach_dict_list, True)

        # リファレンスのアンロード
        file_path = attach_info_dict.get('path')

        if not file_path:
            return

        namespace = attach_info_dict.get('namespace')

        if not namespace:
            return

        base_utility.reference.unload(file_path, namespace)

    # ===============================================
    def __set_constraint(self, attach_dict_list, is_remove=False):
        """
        コンストレイントの作成と除去
        """

        if not attach_dict_list:
            return

        for attach_dict in attach_dict_list:

            src_transform_name = attach_dict.get('src_transform')

            if not src_transform_name:
                continue

            src_transform = \
                cmds.ls(src_transform_name, r=True, l=True)

            if not src_transform:
                continue

            src_transform = src_transform[0]

            dst_transform_name = attach_dict.get('dst_transform')

            if not dst_transform_name:
                continue

            dst_transform = \
                cmds.ls(dst_transform_name, r=True, l=True)

            if not dst_transform:
                continue

            dst_transform = dst_transform[0]

            if is_remove:
                cmds.pointConstraint(dst_transform, src_transform, e=True, rm=True)
                cmds.scaleConstraint(dst_transform, src_transform, e=True, rm=True)

            else:

                scale = attach_dict.get('scale', [1, 1, 1])
                scale_offset = attach_dict.get('scale_offset', [1, 1, 1])

                cmds.pointConstraint(
                    dst_transform, src_transform, offset=[0] * 3, weight=1)

                cmds.scaleConstraint(
                    dst_transform, src_transform, offset=scale_offset, weight=1)

                base_utility.attribute.set_value(src_transform, 'scale', scale)

