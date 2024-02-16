# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI

import sys
import shiboken2
import os
import re

import maya.cmds as cmds

from . import view
from . import copy_work_data
from . import utility
from . import const
from .ui import model

try:
    # Maya2022-
    from builtins import str
    from builtins import object
    from builtins import range
    from importlib import reload
except Exception:
    pass

reload(view)
reload(copy_work_data)
reload(utility)
reload(const)
reload(model)


class Main(object):

    def __init__(self):
        """
        """

        self.view = view.View(self)
        self.view.setWindowTitle(const.TOOL_NAME + const.TOOL_VERSION)

        self.copy_src_dir_path = ''
        self.copy_dst_dir_path = ''
        self.replace_old_str = ''
        self.replace_new_str = ''

        self.copy_data_info_list = []

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)
        self.initialize_ui()
        self.setup_view_event()
        self.view.show()

    def initialize_ui(self):

        self.info_table_model = model.InfoTableModel(self.view)
        self.view.ui.info_table_view.setModel(self.info_table_model)
        self.view.ui.info_table_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def setup_view_event(self):
        """UIのevent設定
        """

        gui = self.view.ui

        gui.src_folder_line.editingFinished.connect(self.src_line_edit)
        gui.replace_old_line.editingFinished.connect(self.replace_str_edit)
        gui.replace_new_line.editingFinished.connect(self.replace_str_edit)
        gui.dst_folder_line.editingFinished.connect(self.dst_line_edit)

        gui.get_scene_root_button.clicked.connect(self.get_src_from_scene)
        gui.src_folder_select_button.clicked.connect(self.src_folder_select_button_event)
        gui.src_folder_open_button.clicked.connect(self.src_folder_open_button_event)
        gui.sync_src_parent_button.clicked.connect(self.sync_src_parent_button_event)
        gui.dst_folder_open_button.clicked.connect(self.dst_folder_open_button_event)

        gui.all_select_button.clicked.connect(self.all_select_button_evenet)
        gui.no_select_button.clicked.connect(self.no_select_button_event)
        gui.default_select_button.clicked.connect(self.default_select_button_event)
        gui.table_refresh_button.clicked.connect(self.reload_button_event)

        gui.info_table_view.customContextMenuRequested.connect(self.info_table_context_menu)

        self.view.ui.exec_copy_button.clicked.connect(self.exec_copy_button_event)

    def update_replace_param_from_ui(self):
        """UI情報からメンバー変数を更新
        """

        self.copy_src_dir_path = utility.normalize_path(self.view.ui.src_folder_line.text())
        self.copy_dst_dir_path = utility.normalize_path(self.view.ui.dst_folder_line.text())
        self.replace_old_str = self.view.ui.replace_old_line.text()
        self.replace_new_str = self.view.ui.replace_new_line.text()

    def src_line_edit(self):
        """コピー元フォルダ入力時イベント
        """

        input_src_path = self.view.ui.src_folder_line.text()

        # 変更がない場合は処理が走らないようにする
        if input_src_path == self.copy_src_dir_path:
            return

        # IDを含まないパスを指定しようとした場合は元に戻して受け付けない
        if not self.is_id_folder_path(input_src_path):
            self.view.ui.src_folder_line.setText(self.copy_src_dir_path)
            cmds.confirmDialog(m='「コピー元フォルダ」のパスが不適切です。データID名のフォルダを指定してください。')
            return

        src_base_name = ''
        if input_src_path:
            src_base_name = os.path.basename(input_src_path)

        # 置換前フォルダ名を同期させる
        self.view.ui.replace_old_line.setText(src_base_name)

        # 置換後フォルダ名が入力されていないかidを含むフォルダ名でなければ、置換前と同じフォルダを入れておく
        if not self.view.ui.replace_new_line.text() or not self.is_id_folder_path(self.view.ui.replace_new_line.text()):
            self.view.ui.replace_new_line.setText(src_base_name)

        # コピー先が入力されていなければ、いったんコピー元を入力
        if not self.view.ui.dst_folder_line.text():
            self.view.ui.dst_folder_line.setText(input_src_path)

        # 置換後フォルダ名と同期
        current_path = self.view.ui.dst_folder_line.text()
        current_base_name = os.path.basename(current_path)
        self.view.ui.dst_folder_line.setText(current_path.replace(current_base_name, self.view.ui.replace_new_line.text()))

        # 選択状態は保持せずテーブル更新
        self.update_replace_param_from_ui()
        self.update_copy_data_info_list()
        self.refresh_info_table()

    def get_src_from_scene(self):
        """シーンからコピー元フォルダを取得
        運用上一番よくつかわれるscenesの親をコピーフォルダとして指定する
        """

        scene_path = cmds.file(q=True, sn=True)

        if not scene_path:
            cmds.confirmDialog(m='シーンを保存してください')
            return

        root_path = utility.normalize_path(scene_path).split('/scenes/')[0]

        if root_path == scene_path:
            cmds.confirmDialog(m='scenesフォルダを見つけられませんでした')
            return

        self.view.ui.src_folder_line.setText(root_path)
        self.src_line_edit()

    def src_folder_select_button_event(self):
        """コピー元フォルダ選択時イベント
        """

        select_root = self.view.ui.src_folder_line.text()

        if not select_root or not os.path.exists(select_root):
            select_root = const.FOLDER_SELECT_ROOT if os.path.exists(const.FOLDER_SELECT_ROOT) else 'D:\\'

        # 存在するならキャラのルートフォルダから開く
        path = QtWidgets.QFileDialog.getExistingDirectory(None, 'コピー元フォルダ選択', select_root)

        if path:
            self.view.ui.src_folder_line.setText(path)
            self.src_line_edit()

    def is_id_folder_path(self, path):
        """IDのフォルダかどうか
        フォルダ名から内部の置換を行うためにはIDのフォルダ（bdy1001_00等）が指定されている必要があるためチェックする

        Args:
            path (str): path

        Returns:
            bool: IDのフォルダかどうか
        """

        return True if re.search(const.REG_ID_FOLDER_PATTERN, os.path.basename(path)) else False

    def src_folder_open_button_event(self):
        """コピー元開くボタンイベント
        """

        path = self.view.ui.src_folder_line.text()

        if not os.path.exists(path):
            cmds.confirmDialog(m='パスが存在しません')
            return

        utility.show_in_explorer([path])

    def dst_folder_open_button_event(self):
        """コピー先開くボタンイベント
        """

        path = self.view.ui.dst_folder_line.text()

        if not os.path.exists(path):
            cmds.confirmDialog(m='パスが存在しません')
            return

        utility.show_in_explorer([path])

    def replace_str_edit(self):
        """置換フォルダ名入力時イベント
        """

        current_new_str = self.view.ui.replace_new_line.text()

        # 変更がない場合は処理が走らないようにする
        if current_new_str == self.replace_new_str:
            return

        # 置換フォルダに禁止文字が入っていた場合は除外
        if re.search(const.REG_FOLDER_NG_RULE, current_new_str):
            current_new_str = re.sub(const.REG_FOLDER_NG_RULE, '', current_new_str)
            self.view.ui.replace_new_line.setText(current_new_str)

        # IDを含まないパスを指定しようとした場合は元に戻して受け付けない
        if not self.is_id_folder_path(current_new_str):
            self.view.ui.replace_new_line.setText(self.replace_new_str)
            cmds.confirmDialog(m='置換IDが不適切です。データIDを含む文字列を入力してください。')
            return

        # 置換後フォルダ名更新時はコピー先のパスも更新
        current_dst_path = self.view.ui.dst_folder_line.text()
        if current_dst_path:
            current_basename = os.path.basename(current_dst_path)
            self.view.ui.dst_folder_line.setText(current_dst_path.replace(current_basename, current_new_str))

        # 選択状態を保持してテーブル更新
        state_dict = self.get_table_state_dict()
        self.update_replace_param_from_ui()
        self.update_copy_data_info_list()
        self.refresh_info_table()
        self.set_table_state_from_dict(state_dict)

    def dst_line_edit(self):
        """コピー先編集時イベント
        """

        current_dst_path = self.view.ui.dst_folder_line.text()

        # 変更がない場合は処理が走らないようにする
        if current_dst_path == self.copy_dst_dir_path:
            return

        # 置換フォルダに禁止文字が入っていた場合は除外
        if re.search(const.REG_PATH_NG_RULE, current_dst_path):
            current_dst_path = re.sub(const.REG_PATH_NG_RULE, '', current_dst_path)
            self.view.ui.dst_folder_line.setText(current_dst_path)

        # IDを含まないパスを指定しようとした場合は元に戻して受け付けない
        if not self.is_id_folder_path(current_dst_path):
            self.view.ui.dst_folder_line.setText(self.copy_dst_dir_path)
            cmds.confirmDialog(m='「コピー先フォルダ」のパスが不適切です。データID名のフォルダを指定してください。')
            return

        # 編集時に置換フォルダ名も自動で変更する
        current_base_name = os.path.basename(current_dst_path)
        self.view.ui.replace_new_line.setText(current_base_name)

        # 選択状態を保持してテーブル更新
        state_dict = self.get_table_state_dict()
        self.update_replace_param_from_ui()
        self.update_copy_data_info_list()
        self.refresh_info_table()
        self.set_table_state_from_dict(state_dict)

    def sync_src_parent_button_event(self):
        """コピー元とコピー先の親を合わせる
        headをtonn_propなどにコピーした後でリセットしたくなった場合などを想定
        """

        src_path = self.view.ui.src_folder_line.text()
        if not src_path:
            return

        dst_path = self.view.ui.dst_folder_line.text()

        if not dst_path:
            self.view.ui.dst_folder_line.setText(src_path)
        else:
            dst_folder = os.path.basename(dst_path)
            src_parent = os.path.dirname(src_path)
            self.view.ui.dst_folder_line.setText(os.path.join(src_parent, dst_folder))

        self.dst_line_edit()

    def all_select_button_evenet(self):
        """すべて選択イベント
        """

        count = self.info_table_model.rowCount(None)

        for i in range(count):
            self.info_table_model.setCheckState(i, True)

    def no_select_button_event(self):
        """すべて解除イベント
        """

        count = self.info_table_model.rowCount(None)

        for i in range(count):
            self.info_table_model.setCheckState(i, False)

    def default_select_button_event(self):
        """初期選択に戻すイベント
        """

        self.set_default_state()

    def set_default_state(self):
        """テーブルのアイテムに初期のチェック状態をセットする
        """

        # ブラックリストに乗っている拡張子はデフォでチェックを外す
        count = self.info_table_model.rowCount(None)

        for i in range(count):
            item = self.info_table_model.items[i]
            src_path = item.copy_data_info.src_path
            if os.path.splitext(src_path)[-1] in const.EXT_DEFAULT_BLACK_LIST:
                self.info_table_model.setCheckState(i, False)
            else:
                self.info_table_model.setCheckState(i, True)

    def reload_button_event(self):
        """リロードボタンイベント
        """

        # 選択状態を保持してテーブル更新
        state_dict = self.get_table_state_dict()
        self.update_replace_param_from_ui()
        self.update_copy_data_info_list()
        self.refresh_info_table()
        self.set_table_state_from_dict(state_dict)

    def update_copy_data_info_list(self):
        """コピーデータ情報を更新
        """

        self.copy_data_info_list = []

        if not all([self.copy_src_dir_path, self.copy_dst_dir_path]):
            self.copy_data_info_list = []
            return

        count = 0
        for curDir, dirs, files in os.walk(self.copy_src_dir_path):
            for file in files:

                if count > const.FILE_COUNT_LIMIT:
                    cmds.confirmDialog(m='コピーするファイル数が多すぎます。「コピー元フォルダ」のパスを確認してください。')
                    self.copy_data_info_list = []
                    return

                src_path = os.path.join(curDir, file)
                src_path = utility.normalize_path(src_path)
                src_relative = src_path.replace(utility.normalize_path(self.copy_src_dir_path), '')
                dst_relative = src_relative.replace(self.replace_old_str, self.replace_new_str)
                dst_path = utility.normalize_path(self.copy_dst_dir_path) + dst_relative

                self.copy_data_info_list.append(
                    copy_work_data.CopyDataInfo(
                        self.copy_src_dir_path,
                        self.copy_dst_dir_path,
                        src_path,
                        dst_path,
                        self.replace_old_str,
                        self.replace_new_str
                    ))

                count += 1

    def refresh_info_table(self):
        """テーブルを更新
        """

        self.info_table_model.refresh(self.copy_data_info_list)
        self.set_default_state()

    def get_table_state_dict(self):
        """テーブルの選択状態を辞書で取得

        Returns:
            {src_path(str): state(bool)}: 選択状態の辞書
        """

        result_dict = {}
        count = self.info_table_model.rowCount(None)

        for i in range(count):
            item = self.info_table_model.items[i]
            src_path = item.copy_data_info.src_path
            value = item.is_enable
            result_dict[src_path] = value

        return result_dict

    def set_table_state_from_dict(self, table_state_dict):
        """辞書からテーブルの選択状態を設定
        リフレッシュ前にget_table_state_dict()で保存していた選択の復元に使用

        Args:
            table_state_dict ({src_path(str): state(bool)}): 選択状態の辞書
        """

        count = self.info_table_model.rowCount(None)

        for i in range(count):
            item = self.info_table_model.items[i]
            src_path = item.copy_data_info.src_path

            val = table_state_dict.get(src_path)
            if val is not None:
                self.info_table_model.setCheckState(i, val)

    def info_table_context_menu(self, pos):

        indexes = self.view.ui.info_table_view.selectedIndexes()
        current_data = None

        for index in indexes:

            if index.column() != 0:
                continue

            if index.isValid():
                item = self.info_table_model.items[index.row()]
                current_data = item.copy_data_info
                break

        if not current_data:
            return

        action_dict_list = []

        action_dict_list.append(
            {
                'label': const.MENU_OPEN_SRC,
                'function': utility.show_in_explorer,
                'arg': [current_data.src_path],
                'enable': os.path.exists(current_data.src_path),
            })

        action_dict_list.append(
            {
                'label': const.MENU_OPEN_DST,
                'function': utility.show_in_explorer,
                'arg': [current_data.dst_path],
                'enable': os.path.exists(current_data.dst_path),
            })

        utility.create_qt_context_menu(self.view.ui.info_table_view, pos, action_dict_list)

    def exec_copy_button_event(self):
        """コピー実行ボタンのイベント
        """

        # 実行前にリロードして最新のステータスを確認しておく
        self.reload_button_event()

        count = self.info_table_model.rowCount(None)

        error_item_dict_list = []
        warning_item_dict_list = []
        copy_data_infos = []

        for i in range(count):
            item = self.info_table_model.items[i]

            # チェックが無効のものをはじく
            if not item.is_enable:
                continue

            copy_data_info = item.copy_data_info
            copy_data_infos.append(copy_data_info)

            # エラーステータスのデータをリスト
            if copy_data_info.status in const.ERROR_STATUSES:
                this_error_dict = {}
                this_error_dict['src'] = os.path.basename(copy_data_info.src_path)
                this_error_dict['dst'] = os.path.basename(copy_data_info.dst_path)
                this_error_dict['status'] = copy_data_info.status
                error_item_dict_list.append(this_error_dict)

            # 警告ステータスのデータをリスト
            elif copy_data_info.status in const.WARNING_STATUSES:
                this_warning_dict = {}
                this_warning_dict['src'] = os.path.basename(copy_data_info.src_path)
                this_warning_dict['dst'] = os.path.basename(copy_data_info.dst_path)
                this_warning_dict['status'] = copy_data_info.status
                warning_item_dict_list.append(this_warning_dict)

        if not copy_data_infos:
            cmds.confirmDialog(m='コピーするデータがありません')
            return

        # エラーがあれば実行しない
        if error_item_dict_list:
            message = 'コピーを実行できません。以下のファイルのエラーを解消してください。'
            infos = []
            for item_dict in error_item_dict_list:
                infos.append('{} : {} >>> {}'.format(item_dict['status'], item_dict['src'], item_dict['dst']))

            self.create_list_dialog('エラー', message, infos, True)
            return

        # 警告は確認して実行
        if warning_item_dict_list:
            message = '以下のファイルに警告があります。コピーを実行しますか？'
            infos = []
            for item_dict in warning_item_dict_list:
                infos.append('{} : {} >>> {}'.format(item_dict['status'], item_dict['src'], item_dict['dst']))

            result = self.create_list_dialog('警告', message, infos)

            if not result:
                return

        # SVN確認（作業者要望）
        result = cmds.confirmDialog(
            title='SVN確認',
            m='SVNのデータが最新になっていることを確認してから実行してください。\nコピーを実行しますか？',
            button=['OK', 'キャンセル'],
            defaultButton='OK',
            dismissString='キャンセル')
        
        if result == 'キャンセル':
            return

        copy_work_data.copy_datas(copy_data_infos)

        cmds.confirmDialog(m='コピーが完了しました！')

    def create_list_dialog(self, title, message, str_list, is_only_ok=False):
        """簡易的なリスト表示するダイアログを出す

        Args:
            title (str): ダイアログタイトル
            message (str): 説明
            str_list ([str]): リスト表示する文字列のリスト
            is_only_ok (bool, optional): OKボタンのみの表示にするか. Defaults to False.

        Returns:
            bool: OKされたかどうか
        """

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(title)
        dialog.resize(600, 300)

        v_layout = QtWidgets.QVBoxLayout(dialog)

        message_lable = QtWidgets.QLabel(dialog)
        message_lable.setText(message)
        v_layout.addWidget(message_lable)

        info_list = QtWidgets.QListWidget(dialog)
        info_list.addItems(str_list)
        v_layout.addWidget(info_list)

        if is_only_ok:
            button_box = QtWidgets.QDialogButtonBox(dialog)
            button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
            v_layout.addWidget(button_box)

            button_box.accepted.connect(dialog.accept)

        else:
            button_box = QtWidgets.QDialogButtonBox(dialog)
            button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
            v_layout.addWidget(button_box)

            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)

        return dialog.exec_() == QtWidgets.QDialog.Accepted
