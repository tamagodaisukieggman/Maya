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
except Exception:
    pass

import os
import shutil

from PySide2 import QtWidgets

import maya.cmds as cmds

from ....base_common import utility as base_utility

from ....glp_common.classes.info import chara_info

reload(chara_info)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TransferToUnity(object):
    """unity転送
    """

    # ==================================================
    def __init__(self):

        self.unity_asset_dir_path = None
        self.data_type = None
        self.tail_id = None

        self.dialog_window_name = 'TransferToUnity'

        self.is_ready = False

    # ==================================================
    def initialize(self, unity_asset_dir_path, data_type, tail_id):

        self.is_ready = False

        if not unity_asset_dir_path or not data_type:
            return

        if not unity_asset_dir_path.endswith('Assets'):
            return

        self.unity_asset_dir_path = unity_asset_dir_path
        self.data_type = data_type
        self.tail_id = tail_id

        self.is_ready = True

    # ==================================================
    def transfer_to_unity(self):

        if not self.is_ready:
            return

        if self.data_type == 'cloth' or self.data_type == 'flare' or self.data_type == 'extensions':
            text = 'Unityにデータを転送しますか?\nSVN側のUnityプレファブ・アセットが古い場合巻き戻りが発生する可能性があります'
            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
            if result_button != QtWidgets.QMessageBox.Ok:
                return

        else:
            text = 'Unityにデータを転送しますか?'
            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
            if result_button != QtWidgets.QMessageBox.Ok:
                return

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info(unity_asset_path=self.unity_asset_dir_path)
        if not _chara_info.exists:
            return

        # general_tail対応 general_tailの場合は指定したidのtextureのみ転送する
        if _chara_info.part_info.data_type.endswith('general_tail'):
            if not self.tail_id:
                return
            _chara_info.tail_char_id = self.tail_id
            _chara_info.create_info(unity_asset_path=self.unity_asset_dir_path)
            if not _chara_info.exists:
                return

        target_dir_path_list = []
        target_param_data_list = []
        result = []

        if self.data_type == 'model' or self.data_type == 'both':

            target_dir_path_list.append(_chara_info.part_info.maya_scenes_dir_path)
            target_param_data_list.append(_chara_info.part_info.model_param_list)

        if self.data_type == 'texture' or self.data_type == 'both':

            target_dir_path_list.append(_chara_info.part_info.maya_sourceimages_dir_path)
            target_param_data_list.append(_chara_info.part_info.all_texture_param_list)

        if self.data_type == 'cloth':

            target_dir_path_list.append(_chara_info.part_info.maya_clothes_dir_path)
            target_param_data_list.append(_chara_info.part_info.cloth_param_list)

        if self.data_type == 'flare':

            target_dir_path_list.append(_chara_info.part_info.maya_flares_dir_path)
            target_param_data_list.append(_chara_info.part_info.flare_param_list)

        if self.data_type == 'extensions':

            target_dir_path_list.append(_chara_info.part_info.maya_extensions_dir_path)
            target_param_data_list.append(_chara_info.part_info.extensions_param_list)

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

                if not os.path.isdir(unity_dir_path):
                    os.mkdir(unity_dir_path)

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
