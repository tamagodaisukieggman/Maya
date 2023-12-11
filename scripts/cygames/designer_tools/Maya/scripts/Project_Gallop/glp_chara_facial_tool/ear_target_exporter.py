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

import os

import maya.cmds as cmds

from ..base_common import utility as base_utility
from ..base_common import classes as base_class
from ..glp_common.classes.info import chara_info
from . import target_info


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EarTargetExporter(object):

    # ===============================================
    def __init__(self, main):

        self.main = main

        self.target_file_path = None
        self.target_file_name = None
        self.target_dir_path = None

        self.model_file_path = None

        self.chara_info = None

        self.is_checked = False

        self.exporter = None

    # ===============================================
    def export(self):

        base_utility.logger.reset()
        base_utility.logger.set_encode_type('shift-jis')
        base_utility.logger.is_print(True)

        base_utility.logger.write()
        base_utility.logger.write_line(0)
        base_utility.logger.write('EarTargetエクスポート')
        base_utility.logger.write_line(0)
        base_utility.logger.write()

        self.__check_data()

        if not self.is_checked:
            return

        self.__export_ear_target()

        base_utility.logger.write()
        base_utility.logger.write('完了')
        base_utility.logger.write_line(1)

    # ===============================================
    def __check_data(self):

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('データチェック')
        base_utility.logger.write()

        self.is_checked = False

        self.target_file_path = cmds.file(q=True, sn=True)

        if not self.target_file_path:
            return

        if self.target_file_path.find('_ear_target') < 0:
            return

        self.target_file_path = \
            self.target_file_path.replace('\\', ' / ')

        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = os.path.dirname(self.target_file_path)

        model_file_name = base_utility.string.get_string_by_regex(
            self.target_file_name, 'mdl_.*_ear_target'
        )

        if not model_file_name:
            return

        model_file_name = model_file_name.replace('_ear_target', '') + '.ma'

        self.model_file_path = \
            self.target_dir_path + '/' + model_file_name

        if not os.path.isfile(self.model_file_path):
            return

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(file_path=self.model_file_path)

        if not self.chara_info.exists:
            return

        self.exporter = base_class.fbx_exporter.FbxExporter()

        base_utility.logger.write(
            'フォルダ : {0}'.format(self.target_dir_path))
        base_utility.logger.write(
            'ターゲット : {0}'.format(self.target_file_name))
        base_utility.logger.write(
            'モデル : {0}'.format(model_file_name))

        self.is_checked = True

    # ===============================================
    def __export_ear_target(self):

        # -----------------------
        # リグファイルのからフェイシャル情報を取得

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('ear_target_infoから情報を取得')
        base_utility.logger.write()

        this_target_info = target_info.TargetInfo()

        this_target_info.target_controller_info.controller_root_name = 'Rig_ear'
        this_target_info.target_controller_info.target_root_name = 'Neck'

        this_target_info.create_info_from_csv(
            'ear_target_info', 'ear_controller_info')

        this_target_info.update_info(False, True)

        # -----------------------
        # フェイシャルターゲットの出力

        base_utility.logger.write()
        base_utility.logger.write_line()
        base_utility.logger.write('ear_target.fbxの出力')
        base_utility.logger.write()

        base_utility.file.open(self.model_file_path)

        this_target_info.bake_transform(False, True, False)

        # オイラー角がフリップしていることがあったのでフィルターをかける
        self.main.apply_euler_filter()

        self.exporter.reset()

        self.exporter.target_node_list = [self.chara_info.part_info.root_node]
        self.exporter.is_ascii = False

        self.exporter.fbx_file_path = self.target_dir_path + '/'

        self.exporter.fbx_file_path += \
            'mdl_' + self.chara_info.part_info.data_id + "_ear_target.fbx"
        base_utility.logger.write(self.exporter.fbx_file_path)
        base_utility.logger.write()
        self.exporter.export()
