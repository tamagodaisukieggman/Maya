# -*- coding: utf-8 -*-
"""ear_target.maからear_target.fbxを出力する
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
from . import util

import maya.cmds as cmds

from . import target_info, fbx_exporter

try:
    from builtins import object
except Exception:
    pass


class EarTargetExport(object):

    def __init__(self):
        """_summary_
        """

        self.target_file_path = ''
        self.target_file_name = ''
        self.target_file_name_without_ext = ''
        self.target_dir_path = ''
        self.model_ma_path = ''

        self.ear_target_suffix = '_ear_target'

        self.exporter = fbx_exporter.FbxExporter()

    def export(self, target_file_path):

        if not self.__check_data_path(target_file_path):
            return

        # ファイルを開く前に一度new scene
        cmds.file(new=True, force=True)

        # ファイルを開く
        cmds.file(target_file_path, o=True, f=True)

        if not self.__set_data_param():
            return

        self.__export_ear_target()

    def __check_data_path(self, target_file_path):
        """_summary_
        """

        self.target_file_path = target_file_path.replace(os.path.sep, '/')
        if not os.path.exists(self.target_file_path):
            return False

        # ear_target以外は対象としない
        if self.target_file_path.find(self.ear_target_suffix) < 0:
            return False

        # ear_targetのファイル名
        self.target_file_name = os.path.basename(self.target_file_path)

        # ear_targetのファイル名拡張子抜き
        self.target_file_name_without_ext = os.path.splitext(self.target_file_name)[0]

        # ディレクトリパス
        self.target_dir_path = os.path.dirname(self.target_file_path)

        # 元モデルのパス
        self.model_ma_path = self.target_file_path.replace(self.ear_target_suffix, '')
        if not os.path.exists(self.model_ma_path):
            return False

        return True

    def __set_data_param(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        # ルートノード名
        self.model_root_node = self.target_file_name_without_ext.replace(self.ear_target_suffix, '')
        # リファレンス環境で見つからなかったらFalse
        if not cmds.ls(self.model_root_node, l=True, r=True):
            return False

        return True

    def __export_ear_target(self):
        """_summary_
        """

        this_target_info = target_info.TargetInfo()
        this_target_info.create_info_from_csv('ear_target_info', 'ear_controller_info')
        this_target_info.target_controller_info.controller_root_name = 'Rig_ear'
        this_target_info.target_controller_info.target_root_name = 'Neck'
        this_target_info.update_info(False, True)

        # 元モデルファイルを開く
        cmds.file(self.model_ma_path, o=True, f=True)

        this_target_info.bake_transform(False, True, False)

        # オイラー角がフリップしていることがあったのでフィルターをかける
        util.apply_euler_filter()

        self.exporter.reset()
        self.exporter.target_node_list = [self.model_root_node]
        self.exporter.is_ascii = False
        self.exporter.fbx_file_path = os.path.join(
            self.target_dir_path, '{}_ear_target.fbx'.format(self.model_root_node)
        ).replace(os.path.sep, '/')

        return self.exporter.export()
