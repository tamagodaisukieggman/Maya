# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import csv
import datetime
import hashlib
import os
import re
import subprocess
import sys

import shiboken2
from PySide2 import QtWidgets

import maya.cmds as cmds
from maya import OpenMayaUI
from . import view, cleanup_cmd

# Maya2022-
try:
    from importlib import reload
except Exception:
    pass

reload(view)
reload(cleanup_cmd)


class Main(object):

    def __init__(self):

        self.view = view.View()

        # クリーンアップを実行する際のUIやfunction等の情報辞書リスト
        # force_flagはexec_cleanup_event実行時に強制実行フラグTrueの場合に実行するかどうか
        self.cleanup_event_dict_list = [
            {
                'checkbox': self.view.ui.fix_initial_node_cb,
                'func': cleanup_cmd.fix_irregular_lock_node,
                'message': '不正にロックされたノードのロックの解除を実行しました　※この処理はエラーの有無に関わらず実行されます',
                'label': 'initialエラー',
                'force_flag': True
            },
            {
                'checkbox': self.view.ui.delete_unknown_nodes_and_plugins_cb,
                'func': cleanup_cmd.delete_unknown_nodes_and_plugins,
                'message': 'unknownノードとプラグインを削除しました',
                'label': 'unknown削除',
                'force_flag': True
            },
            {
                'checkbox': self.view.ui.delete_vaccine_cb,
                'func': cleanup_cmd.delete_vaccine,
                'message': '不正なスクリプトをシーンから削除しました',
                'label': '不正スクリプト削除',
                'force_flag': True
            },
            {
                'checkbox': self.view.ui.reset_ui_callback_cb,
                'func': cleanup_cmd.reset_ui_callback,
                'message': 'UI関連のCallback(uiConfiguration)をリセットしました',
                'label': 'Callbackリセット',
                'force_flag': False
            },
            {
                'checkbox': self.view.ui.delete_script_nodes_cb,
                'func': cleanup_cmd.delete_script_nodes,
                'message': '既定以外のScriptNodeを削除しました',
                'label': '規定以外のScriptNode削除',
                'force_flag': True
            },
            {
                'checkbox': self.view.ui.delete_outliner_panel_select_command_cb,
                'func': cleanup_cmd.delete_outliner_panel_select_command,
                'message': 'アウトライナー選択時エラーの原因のコマンドを削除しました　※この処理はエラーの有無に関わらず実行されます',
                'label': 'アウトライナー選択時エラーの原因のコマンドを削除',
                'force_flag': True
            },
        ]

        # cleanupの処理を行うためのcheckboxのリスト
        self.cleanup_cb_list = [
            self.view.ui.fix_initial_node_cb,
            self.view.ui.delete_unknown_nodes_and_plugins_cb,
            self.view.ui.delete_vaccine_cb,
            self.view.ui.reset_ui_callback_cb,
            self.view.ui.delete_script_nodes_cb,
            self.view.ui.delete_outliner_panel_select_command_cb,
        ]

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    def show_ui(self):
        """UI表示
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.view.ui.exec_cleanup_btn.clicked.connect(lambda: self.exec_cleanup_event())
        self.view.ui.exec_batch_cleanup_btn.clicked.connect(lambda: self.exec_batch_cleanup_event())
        self.view.ui.set_batch_cleanup_target_dir_btn.clicked.connect(lambda: self.set_batch_cleanup_target_dir())
        self.view.ui.all_cleanup_on_btn.clicked.connect(lambda: self.all_cleanup_cb_op(True))
        self.view.ui.all_cleanup_off_btn.clicked.connect(lambda: self.all_cleanup_cb_op(False))

        self.view.show()

    def all_cleanup_cb_op(self, status):
        """cleanup用のチェックボックスの一括管理

        Args:
            status (bool): チェックボックスをONに設定するかOFFに設定するか
        """
        for checkbox in self.cleanup_cb_list:
            checkbox.setChecked(status)

    def exec_cleanup_event(self, force=False):
        """クリーンアップを実行するEvent

        実行後、戻り値を取得して対応するメッセージを表示

        Args:
            force (bool, optional): 強制的に全ての項目を実行するか. Defaults to False.
        """

        # 強制クリーンアップモードを除いてクリーンアップで実行するコマンドが一つもチェックされていない場合ははじく
        if not any([checkbox.isChecked() for checkbox in self.cleanup_cb_list]) and not force:
            QtWidgets.QMessageBox.information(None, '情報', '対象のクリーンアップコマンドを一つ以上選択したうえで実行してください', QtWidgets.QMessageBox.Ok)
            return

        current_path = cmds.file(q=True, sn=True)
        if not current_path:
            cmds.warning('シーンを保存してから実行して下さい')
            return

        # unknownノード、プラグインの削除を実行する場合、実行前にリファレンスにクリーン対象があるかチェックする
        should_cleanup_reference = False

        for cleanup_event_dict in self.cleanup_event_dict_list:

            label = cleanup_event_dict.get('label')

            if label != 'unknown削除':
                continue

            checkbox = cleanup_event_dict.get('checkbox')
            force_flag = cleanup_event_dict.get('force_flag')

            if (force and force_flag) or checkbox.isChecked():
                should_cleanup_reference = cleanup_cmd.has_reference_unknown_nodes_or_plugins()

            break

        result_list = self.cleanup(force)
        error_str_list = [self.cleanup_event_dict_list[i].get('message') for i, result in enumerate(result_list) if result]

        if error_str_list:
            message = '\n\nメッセージ:\n{}'.format('\n'.join(error_str_list))
            warning = ''
            if should_cleanup_reference:
                warning = '\n\n警告:\nリファレンスシーンにunknownノードかプラグインが含まれています\nリファレンスシーンでSceneCleanerを実行してください'
            QtWidgets.QMessageBox.information(
                None, '情報', 'ファイルのクリーンアップを実行しました{}{}'.format(message, warning), QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(None, '情報', 'クリーンアップ項目が見つかりませんでした', QtWidgets.QMessageBox.Ok)

    def exec_batch_cleanup_event(self):
        """実行対象フォルダ以下のmaファイルに対してクリーンアップを実行するevent

        実行するクリーンアップコマンドはUI
        """

        # クリーンアップで実行するものとしてして一つもチェックされていない場合ははじく
        if not any([checkbox.isChecked() for checkbox in self.cleanup_cb_list]):
            QtWidgets.QMessageBox.information(None, '情報', '対象のクリーンアップコマンドを一つ以上選択したうえで実行してください', QtWidgets.QMessageBox.Ok)
            return

        target_dir_path = self.view.ui.exec_batch_cleanup_target_dir_edit.text()
        if not os.path.exists(target_dir_path):
            QtWidgets.QMessageBox.warning(None, '注意', '実行対象フォルダが指定されていないか、存在しません。', QtWidgets.QMessageBox.Ok)
            return

        target_file_path_list = self.get_target_ma_file_path_list(
            target_dir_path, self.view.ui.exec_cleanup_for_child_hierarchy_cb.isChecked())

        if not target_file_path_list:
            QtWidgets.QMessageBox.warning(None, '注意', '実行対象フォルダ以下に対象がありません', QtWidgets.QMessageBox.Ok)
            return

        target_dict_list = []
        for target_file_path in target_file_path_list:

            cmds.file(new=True, f=True)
            cmds.file(target_file_path, o=True, f=True)
            result_list = self.cleanup()
            target_dict_list.append({'target_file_path': target_file_path, 'result_list': result_list})

        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        header_label_list = ['ファイルパス'] + [cleanup_event_dict.get('label') for cleanup_event_dict in self.cleanup_event_dict_list]
        header_label_list = [header_label.encode('cp932') for header_label in header_label_list]
        csv_file_path = 'D:\\batch_cleanup_result_{}.csv'.format(now_time)
        with open(csv_file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header_label_list)

            for target_dict in target_dict_list:
                write_str_list = [target_dict.get('target_file_path')] + target_dict.get('result_list')
                write_str_list = [str(write_str).encode('cp932') for write_str in write_str_list]
                writer.writerow(write_str_list)

        subprocess.Popen(['start', csv_file_path], shell=True)

        QtWidgets.QMessageBox.information(None, '情報', '実行が完了しました。\n', QtWidgets.QMessageBox.Ok)

    def cleanup(self, force=False):
        """クリーンアップを実行

        Args:
            force (bool, optional): 強制的に全ての項目を実行するか. Defaults to False.

        Returns:
            list: funcの実行結果のboolが入ったlist
        """

        result_list = []

        for cleanup_event_dict in self.cleanup_event_dict_list:

            checkbox = cleanup_event_dict.get('checkbox')
            func = cleanup_event_dict.get('func')
            force_flag = cleanup_event_dict.get('force_flag')

            result = False
            if (force and force_flag) or checkbox.isChecked():
                result = func()

            result_list.append(result)

        self.create_certificate_file()

        return result_list

    def create_certificate_file(self):
        """認証ファイルを作成する
        """
        file_path = cmds.file(q=True, sn=True)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_hash = self.get_file_hash(file_path)
        target_dir = os.path.dirname(file_path)

        # フォルダー内に古いcertファイルがないか確認し、あったら削除
        for file in os.listdir(target_dir):
            if re.match('^cleanup_log_' + file_name + '_[0-9]{12}.txt$', file):
                os.remove(os.path.join(target_dir, file))

        # 証明書作成
        data_str = datetime.datetime.now().strftime('%Y%m%d%H%M')
        cert_file_path = os.path.join(target_dir, 'cleanup_log_{0}_{1}.txt'.format(file_name, data_str))
        with open(cert_file_path, 'w') as f:
            f.write(file_hash)

    def get_file_hash(self, file_path):
        """SHA256形式でファイルハッシュを求める

        Args:
            file_path (str): ファイルのパス

        Returns:
            str: ファイルのハッシュ
        """
        file_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(2048 * file_hash.block_size), b''):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def set_batch_cleanup_target_dir(self):
        """実行対象フォルダEditLineにバッチクリーンアップ用のフォルダパスをファイルダイアログから設定する
        """

        dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'フォルダ選択')
        if dir:
            self.view.ui.exec_batch_cleanup_target_dir_edit.setText(dir)

    def get_target_ma_file_path_list(self, target_dir_path, is_get_child_hierarchy):
        """target_dir_path以下にある.maファイルの一覧を取得する

        Args:
            target_dir_path (str): .maファイルの一覧を取得する親フォルダのパス
            is_get_child_hierarchy (bool): 親フォルダ以下の階層全てを取得するかどうか Trueですべて取得

        Returns:
            list: target_dir_path以下にある.maファイルの一覧
        """

        target_file_list = []
        for current_dir, _, file_name_list in os.walk(target_dir_path):
            for file_name in file_name_list:
                if file_name.endswith('.ma'):
                    target_file_list.append(os.path.join(current_dir, file_name))

            if not is_get_child_hierarchy:
                break

        return target_file_list


if __name__ == '__main__':

    main = Main()
    main.show_ui()
