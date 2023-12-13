# -*- coding: utf-8 -*-
u"""テクスチャをUnityの指定フォルダに転送する
フォルダパスの指定にはchara_infoを利用する
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import shutil
from PySide2 import QtWidgets

import maya.cmds as cmds
from maya.app.general import mayaMixin

from ..glp_common.classes.info import chara_info

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class Main(object):

    def __init__(self, unity_assets_path='', target_ma_file_dir_path='', target_ma_regex=r'', target_file_regex=r'', transfer_texture_type_list=[]):

        # UnityのAssetsフォルダ
        default_unity_assets_path = 'W:\\gallop\\client\\Assets'
        self.unity_assets_path = unity_assets_path if unity_assets_path else default_unity_assets_path

        # 取得したいファイルの親フォルダ
        default_target_ma_file_dir_path = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model\\head'
        self.target_ma_file_dir_path = target_ma_file_dir_path if target_ma_file_dir_path else default_target_ma_file_dir_path

        # 取得したいmaファイルの命名規則
        default_target_ma_regex = r'mdl_chr[0-9]{4}_[0-9]{2}(_face|_hair|)([0-9]{3}|)\.ma'
        self.target_ma_regex = target_ma_regex if target_ma_regex else default_target_ma_regex

        # 取得したいファイルの命名規則
        default_target_file_regex = r'chr[0-9]{4}_[0-9]{2}\/sourceimages(\/face|\/hair|)\/tex_chr[0-9]{4}_[0-9]{2}(_face|_hair)([0-9]{3}_[0-9]|)_'
        self.target_file_regex = target_file_regex if target_file_regex else default_target_file_regex

        # 転送したいテクスチャの種類
        default_transfer_texture_type_list = ['diff', 'shad_c', 'ctrl', 'base']
        self.transfer_texture_type_list = transfer_texture_type_list if transfer_texture_type_list else default_transfer_texture_type_list

        # 転送できたテクスチャのログの出力先とリスト
        self.transferred_file_list_log_path = '{}\\transferred_file_list_log.txt'.format(self.target_ma_file_dir_path)
        # エラーファイルログの出力先とリスト
        self.error_info_list_log_path = '{}\\error_info_list_log_path.txt'.format(self.target_ma_file_dir_path)

        self.transfer_target_file_info_list = []

        self.dialog_widget = None

    def check_transfer_texture_file(self):

        target_ma_scene_list = self.__get_target_file_list()
        if not target_ma_scene_list:
            cmds.confirmDialog(title=u'警告', message=u'出力対象が見つかりません')
            return

        if not os.path.exists(self.unity_assets_path):
            cmds.confirmDialog(
                title=u'警告',
                message=u'UnityのAssetsのパスが設定されていないか見つかりません\n{}'.format(
                    self.unity_assets_path
                )
            )
            return

        for target_ma_scene in target_ma_scene_list:

            target_file_info = chara_info.CharaInfo()
            target_file_info.create_info(file_path=target_ma_scene, unity_asset_path=self.unity_assets_path)
            if not target_file_info.exists:
                self.error_info_list.append(
                    {'error_value': 'CharaInfo is not found.', 'target_file': target_ma_scene}
                )
                continue

            texture_param_list = target_file_info.part_info.all_texture_param_list
            if not texture_param_list[0].get('unity_dir_path'):
                self.error_info_list.append(
                    {
                        'error_value': 'UnityDirPath key is not found. data_type is {}'.format(target_file_info.data_type),
                        'target_file': target_ma_scene
                    }
                )
                continue

            for texture_param in texture_param_list:

                texture_name = texture_param.get('name')
                unity_dir_path = texture_param.get('unity_dir_path')

                original_file_path = os.path.join(
                    target_file_info.part_info.maya_sourceimages_dir_path, texture_name
                ).replace('\\', '/')

                if self.transfer_texture_type_list:
                    for texture_type in self.transfer_texture_type_list:
                        if re.search(r'{}\.tga$'.format(texture_type), texture_name):
                            break
                    else:
                        continue
                else:
                    if not re.search(r'\.tga$', texture_name):
                        continue

                if not re.search(self.target_file_regex, original_file_path):
                    continue

                target_file_path = os.path.join(unity_dir_path, texture_name)

                self.transfer_target_file_info_list.append(
                    {
                        'target_ma_file': target_ma_scene,
                        'texture_name': texture_name,
                        'unity_dir_path': unity_dir_path,
                        'original_file_path': original_file_path,
                        'target_file_path': target_file_path
                    }
                )

        self.__show_transfer_target_dialog_window()

    def __exec_transfar(self):

        transferred_file_list = []
        error_info_list = []

        for transfer_target_file_info in self.transfer_target_file_info_list:

            target_ma_file = transfer_target_file_info.get('target_ma_file')
            texture_name = transfer_target_file_info.get('texture_name')
            unity_dir_path = transfer_target_file_info.get('unity_dir_path')
            original_file_path = transfer_target_file_info.get('original_file_path')
            target_file_path = transfer_target_file_info.get('target_file_path')

            if original_file_path is None or target_file_path is None:
                continue

            if not os.path.exists(original_file_path):
                error_info_list.append(
                    {
                        'error_value': 'original texture not exists. {}'.format(texture_name),
                        'target_file': target_ma_file
                    }
                )
                continue

            try:

                if not os.path.isdir(unity_dir_path):
                    os.mkdir(unity_dir_path)

                shutil.copyfile(original_file_path, target_file_path)

            except Exception:

                error_info_list.append(
                    {
                        'error_value': 'texture copy failed. {}'.format(texture_name),
                        'target_file': target_ma_file
                    }
                )
                continue

            transferred_file_list.append(original_file_path)

        if transferred_file_list:
            with open(self.transferred_file_list_log_path, 'w') as f:
                f.writelines('\r\n'.join(transferred_file_list))

        if error_info_list:
            error_str_list = [
                'target_file: {} error: {}'.format(
                    error_info.get('target_file'), error_info.get('error_value')
                ) for error_info in error_info_list
            ]
            with open(self.error_info_list_log_path, 'w') as f:
                f.writelines('\r\n'.join(error_str_list))

        cmds.confirmDialog(title=u'完了', message=u'Unityへの一括ファイル転送が完了しました')
        self.dialog_widget.close()

    def __get_target_file_list(self):

        file_list = []

        if not os.path.exists(self.target_ma_file_dir_path):
            return []

        for root, dirs, files in os.walk(self.target_ma_file_dir_path):
            if not re.search(r'scenes(\\face|\\hair|)$', root):
                continue
            for filename in files:
                if not re.search(self.target_ma_regex, filename):
                    continue
                file_list.append(os.path.join(root, filename))

        return file_list

    def __show_transfer_target_dialog_window(self):

        self.dialog_widget = OutputDialog()
        self.dialog_widget.ok_button.clicked.connect(lambda: self.__exec_transfar())
        self.dialog_widget.ng_button.clicked.connect(lambda: self.dialog_widget.close())
        target_texture_list = [
            target_file_info.get('original_file_path') for target_file_info in self.transfer_target_file_info_list
        ]
        self.dialog_widget.target_texture_list.addItems(target_texture_list)
        self.dialog_widget.show()


class OutputDialog(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):

    def __init__(self, parent=None):

        super(OutputDialog, self).__init__(parent)
        self.create_ui()

    def create_ui(self):

        self.container = QtWidgets.QVBoxLayout(self)

        self.target_texture_list = QtWidgets.QListWidget(self)

        self.set_button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(self)
        self.ok_button.setText('OK')
        self.ng_button = QtWidgets.QPushButton(self)
        self.ng_button.setText('Cancel')
        self.set_button_layout.addWidget(self.ok_button)
        self.set_button_layout.addWidget(self.ng_button)

        self.container.addWidget(self.target_texture_list)
        self.container.addLayout(self.set_button_layout)
