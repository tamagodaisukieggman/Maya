# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets
from maya import OpenMayaUI

import sys
import shiboken2
import os
import datetime

import maya.cmds as cmds

from . import view
from ..base_common import utility as base_utility

try:
    # Maya2022-
    from builtins import range
    from builtins import object
except Exception:
    pass


# ===============================================
def main(root_path_list, is_export_log, export_log_dir_path):

    scanner = ScannerMain(root_path_list, is_export_log, export_log_dir_path)
    scanner.scan()


# ===============================================
def reload_reference_for_root_path_list(root_path_list):

    scanner = ScannerMain(root_path_list)
    scanner.reload_reference_for_root_path_list()


class ScanScene(object):

    def __init__(self):
        """
        """

        self.view = view.View()
        self.target_dir_path_layout_list = []
        self.creaned_target_path_list = []

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
            if type(target) == type(widget):
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)
        self.setup_view_event()
        self.view.show()

    def setup_view_event(self):
        """UIのevent設定
        """

        self.view.ui.okButton.clicked.connect(
            lambda: self.exec_scan('OK')
        )

        self.view.ui.setTargetDirListButton.clicked.connect(
            lambda: self.add_target_dir_path_layout()
        )

        self.view.ui.setLogExportTargetDirButton.clicked.connect(
            lambda: self.set_log_export_dir_path()
        )

        self.view.ui.referenceRepairButton.clicked.connect(
            lambda: self.repair_reference()
        )

    def set_log_export_dir_path(self):
        """
        """

        path = self.view.ui.logExportTargetDirEdit.text()
        if not os.path.exists(path) or not os.path.isdir(path):
            path = 'D:\\'

        # ディレクトリ選択ダイアログを表示
        path = QtWidgets.QFileDialog.getExistingDirectory(None, "rootpath", path)
        if path:
            self.view.ui.logExportTargetDirEdit.setText(path)

    def exec_scan(self, _str):
        """
        """

        target_dir_path_list = []
        for target_dir_path_layout in self.target_dir_path_layout_list:
            target_dir_path_list.append(target_dir_path_layout.target)

        if not target_dir_path_list:
            cmds.confirmDialog(title='Warning', message='対象フォルダのリストが取得できません')
            return

        self.view.ui.referenceRepairButton.setEnabled(False)

        is_export_log = self.view.ui.isLogExportCheckBox.isChecked()
        export_log_dir_path = self.view.ui.logExportTargetDirEdit.text()

        scanner_main = ScannerMain(target_dir_path_list, is_export_log, export_log_dir_path)
        self.creaned_target_path_list = scanner_main.scan()

        cmds.confirmDialog(
            title='Information',
            message='{0}件のファイルが該当し、スキャンが完了しました。'.format(
                len(self.creaned_target_path_list)
            ))

        if len(self.creaned_target_path_list) > 0:
            self.view.ui.referenceRepairButton.setEnabled(True)

    def add_target_dir_path_layout(self):
        """
        """

        root_path = os.path.abspath(os.path.dirname("__file__"))
        # ディレクトリ選択ダイアログを表示
        path = QtWidgets.QFileDialog.getExistingDirectory(None, "select direcotry", root_path)
        if not path:
            return

        tmp_box_layout = TargetDirPathLyaoutWidget(self, path)
        self.target_dir_path_layout_list.append(tmp_box_layout)
        self.view.ui.targetDirListLayout.insertLayout(
            self.view.ui.targetDirListLayout.count() - 1, tmp_box_layout)

    def delete_target_object_layout(self, value):
        """対象のランダム配置対象オブジェクトを削除する

        Args:
            value(TargetObjectLayoutWidget): 削除対象のWidget
        """

        if value in self.target_dir_path_layout_list:
            self.target_dir_path_layout_list.remove(value)

    def repair_reference(self):
        """
        """

        self.view.ui.referenceRepairButton.setEnabled(False)

        base_utility.simple_batch.execute(
            '{0}{1}'.format(
                'import Project_Gallop.glp_scan_scene.scan_scene;',
                'Project_Gallop.glp_scan_scene.scan_scene.ScannerMain().reload_reference_for_simple_batch();'
            ),
            True,
            target_path_list=self.creaned_target_path_list
        )

        cmds.confirmDialog(
            title='Information',
            message='{0}件のリファレンス修復が完了しました'.format(
                len(self.creaned_target_path_list)
            ))


class TargetDirPathLyaoutWidget(QtWidgets.QHBoxLayout):
    """
    """

    def __init__(self, main, target, parent=None):

        super(TargetDirPathLyaoutWidget, self).__init__(parent)

        self.main = main
        self.target = target
        self.spin_box = None
        self.delete_button = None

        self.set_ui()

    def set_ui(self):

        label = QtWidgets.QLabel()
        label.setObjectName(self.target)
        label.setText(self.target)

        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setObjectName("pushButton2")
        self.delete_button.clicked.connect(self._clicked_delete_button_event)
        self.delete_button.setText("削除")

        self.addWidget(label)
        self.addWidget(self.delete_button)

        self.setStretch(0, 5)
        self.setStretch(1, 1)

    def _clicked_delete_button_event(self):
        """
        """

        for i in range(self.count()):
            b = self.itemAt(i)
            wid = b.widget()
            if wid:
                wid.deleteLater()

        self.main.delete_target_object_layout(self)
        self.deleteLater()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ScannerMain(object):

    # ===============================================
    def __init__(self, root_path_list=[], is_export_log=True, export_log_dir_path=''):

        # 実行コマンド
        self.batch_command = 'mayabatch.exe -noAutoloadPlugins -command "file -force -loadReferenceDepth ""none"" -open ""{0}"" ; evalDeferred (""loadPlugin MayaScanner; MayaScan;"")";'

        # リストパス以下のma,mbを検索
        self.search_root_path_list = root_path_list
        # ログを出力するかどうか
        self.is_export_log = is_export_log
        self.export_log_dir_path = export_log_dir_path
        # logの出力先
        self.log_file_path = os.path.join(self.export_log_dir_path, 'scan_log.txt')

    # ===============================================
    def get_target_path_list(self, root_path):

        result_path_list = []

        for curDir, dirs, files in os.walk(root_path):
            for file in files:
                if file.endswith(".ma") or file.endswith(".mb"):
                    this_path = os.path.join(curDir, file).replace("\\", "/")
                    result_path_list.append(this_path)

        return result_path_list

    # ===============================================
    def scan(self):

        clearned_file_path_list = []

        if not cmds.pluginInfo('MayaScannerCB', q=True, loaded=True) or not cmds.pluginInfo('MayaScanner', q=True, loaded=True):
            cmds.confirmDialog(title='Warning', message='MayaScannerプラグインがロードされていません')
            return clearned_file_path_list

        if not os.path.exists(self.export_log_dir_path) or not os.path.isdir(self.export_log_dir_path):
            self.is_export_log = False

        for search_root_path in self.search_root_path_list:

            self.write_log_by_line('=' * 20)
            self.write_log_by_line('SCAN ROOT : {}'.format(search_root_path))
            self.write_log_by_line('START TIME : {}'.format(datetime.datetime.now().isoformat()))

            target_path_list = self.get_target_path_list(search_root_path)
            target_count = len(target_path_list)
            current_count = 0

            for target_path in target_path_list:

                current_count += 1
                org_mtime = os.path.getmtime(target_path)

                self.write_log_by_line('*' * 10)
                self.write_log_by_line('{}/{} : {}'.format(current_count, target_count, os.path.basename(target_path)))
                self.write_log_by_line('==scan start==')

                com = self.batch_command.format(target_path)
                try:

                    os.system(com)
                    this_mtime = os.path.getmtime(target_path)

                    if not org_mtime == this_mtime:
                        self.write_log_by_line('file fixed!!!!!')
                        clearned_file_path_list.append(target_path)

                    else:
                        self.write_log_by_line('no change')

                except Exception:
                    self.write_log_by_line('exec failed!!!!!')

                self.write_log_by_line('==scan finish==')
                self.write_log_by_line('\n')

        self.write_log_by_line('ALL SCAN FINISHED NORMALLY')

        return clearned_file_path_list

    # ===============================================
    def write_log_by_line(self, log_str):

        if not self.is_export_log:
            return

        try:

            if not os.path.exists(self.log_file_path):

                with open(self.log_file_path, mode='w') as log:
                    log.write('\n' + log_str)

            else:

                with open(self.log_file_path, mode='a') as log:
                    log.write('\n' + log_str)

        except Exception:

            # 2byte文字があるとasciiエラーになる
            if not os.path.exists(self.log_file_path):

                with open(self.log_file_path, mode='w') as log:
                    log.write('\n' + 'xxxxxxxxxx')

            else:

                with open(self.log_file_path, mode='a') as log:
                    log.write('\n' + 'xxxxxxxxxx')

    # ===============================================
    def reload_reference_for_root_path_list(self):

        for search_root_path in self.search_root_path_list:

            target_path_list = self.get_target_path_list(search_root_path)

            self.reload_reference(target_path_list)

    # ===============================================
    def reload_reference_for_simple_batch(self):

        target_path_list = \
            base_utility.simple_batch.get_param_value(
                'target_path_list')

        self.reload_reference(target_path_list)

    # ===============================================
    def reload_reference(self, target_path_list):

        for target_path in target_path_list:

            cmds.file(target_path, o=True, f=True)

            all_ref_nodes = cmds.ls(typ='reference')

            if not all_ref_nodes:
                return

            is_loaded = False
            for ref in all_ref_nodes:

                try:

                    # ゴミノードが以下のクエリでエラーになる
                    # もっとうまいやり方がありそう
                    cmds.referenceQuery(ref, f=True)

                    if cmds.referenceQuery(ref, il=True):
                        print('this ref has already been loaded')
                    else:
                        cmds.file(lr=ref, f=True)
                        is_loaded = True

                except Exception:

                    continue

            if is_loaded:
                cmds.file(s=True, f=True)
