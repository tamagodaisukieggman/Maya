# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import object
    from importlib import reload
except:
    pass

import os
import shutil

import maya.cmds as cmds

from ....base_common import utility as base_utility

from ....farm_common.classes.info import chara_info

reload(chara_info)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TransferToUnity(object):
    """unity転送
    """

    # ==================================================
    def __init__(self):

        self.unity_asset_dir_path = None
        self.transfer_type_list = None
        self.tail_id = None

        self.dialog_window_name = 'TransferToUnity'

        self.is_ready = False

    # ==================================================
    def initialize(self, unity_asset_dir_path, transfer_type_list):

        self.is_ready = False

        if not unity_asset_dir_path or not transfer_type_list:
            return

        if not unity_asset_dir_path.endswith('Assets'):
            return

        self.unity_asset_dir_path = unity_asset_dir_path
        self.transfer_type_list = transfer_type_list

        self.is_ready = True

    # ==================================================
    def transfer_to_unity(self):

        if not self.is_ready:
            return

        if not base_utility.ui.dialog.open_ok_cancel("確認", "Unityにデータを転送しますか?"):
            return

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info(unity_asset_path=self.unity_asset_dir_path)
        if not _chara_info.exists:
            return

        target_dir_path_list = []
        target_param_data_list = []
        result = []

        for transfer_type in self.transfer_type_list:

            if transfer_type == 'model':

                target_dir_path_list.append(_chara_info.part_info.maya_scenes_dir_path)
                target_param_data_list.append(_chara_info.part_info.model_param_list)

            if transfer_type == 'texture':

                target_dir_path_list.append(_chara_info.part_info.maya_sourceimages_dir_path)
                target_param_data_list.append(_chara_info.part_info.all_texture_param_list)

            if transfer_type == 'cloth':

                target_dir_path_list.append(_chara_info.part_info.maya_clothes_dir_path)
                target_param_data_list.append(_chara_info.part_info.cloth_param_list)

            if transfer_type == 'flare':

                target_dir_path_list.append(_chara_info.part_info.maya_flares_dir_path)
                target_param_data_list.append(_chara_info.part_info.flare_param_list)

        for target_dir, param_list in zip(target_dir_path_list, target_param_data_list):
            result.extend(self.__transfer_target_files(target_dir, param_list))

        if len(result) > 0:
            self.__show_dialog_window('転送結果', result)

    # ===============================================
    def __transfer_target_files(self, original_dir_path, transfer_param_list):

        transferd_files = []

        for transfer_param in transfer_param_list:

            if 'name' not in transfer_param:
                break

            if 'unity_dir_path' not in transfer_param:
                break

            name = transfer_param['name']
            unity_dir_path = transfer_param['unity_dir_path']
            short_name = name.split('/')[-1]

            original_file_path = '{0}/{1}'.format(original_dir_path, name)
            target_file_path = '{0}/{1}'.format(unity_dir_path, short_name)

            if not os.path.isfile(original_file_path):
                print('file not exists : {}'.format(original_file_path))
                continue

            try:

                shutil.copyfile(original_file_path, target_file_path)
                transferd_files.append(name)

            except Exception:

                print('copy出来ませんでした : {0} -> {1}'.format(original_file_path, target_file_path))

        return transferd_files

    # ===============================================
    def __show_dialog_window(self, title, show_list):

        base_utility.ui.window.remove_same_id_window(self.dialog_window_name)

        cmds.window(self.dialog_window_name, title="転送結果")
        cmds.window(self.dialog_window_name, e=True, widthHeight=(500, 240), s=False)

        cmds.columnLayout()
        cmds.text(label='以下のファイルを転送しました',)
        cmds.textScrollList(
            numberOfRows=len(show_list), allowMultiSelection=True,
            append=show_list, h=200, w=500)
        cmds.button(label='閉じる', c=self.__delete_dialog_window, w=500)
        cmds.setParent('..')

        cmds.showWindow(self.dialog_window_name)

    # ===============================================
    def __delete_dialog_window(self, *args):

        cmds.deleteUI(self.dialog_window_name, window=True)