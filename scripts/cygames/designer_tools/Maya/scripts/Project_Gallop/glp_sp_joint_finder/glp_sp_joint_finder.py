# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import sys
import subprocess

import maya.cmds as cmds
import shiboken2
from PySide2 import QtGui, QtWidgets
from maya import OpenMayaUI

from . import glp_joint_finder_gui, glp_dag_collector
from ..glp_common.classes.info import chara_info

from ..base_common import utility as base_utility

try:
    # Maya2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(chara_info)
reload(glp_joint_finder_gui)
reload(glp_dag_collector)


# ===============================================
def batch():
    main = GlpSpJointFinder()
    main.batch_export()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GlpSpJointFinder(object):

    # ===============================================
    def __init__(self):

        self.joint_finder_gui = glp_joint_finder_gui.GUI()

        self.chara_info = None
        self.root_long_name = ''
        self.collector = None

        self.result_group_list = None

        # バッチ出力する特殊骨の種類
        self.batch_output_prefixes = ['Sp_', 'Ex_', 'Tp_', 'Pc_']
        # ツールで表示する特需骨の種類はUIから取得する
        self.visible_prefixes = []

        self.no_spjoint_brush = None
        self.highlight_brush = None

        self.highlight_item_list = []
        self.highlight_joint_list = []

        self.default_batch_target_path = \
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model'
        self.default_batch_output_path = \
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/sp_joint_list.txt'

        self.no_spjoint_brush = QtGui.QBrush(QtGui.QColor(128, 128, 128))
        self.highlight_brush = QtGui.QBrush(QtGui.QColor(64, 64, 128))

    # ===============================================
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
                widget.close()          # クローズイベントを呼んでウインドウを閉じる
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

    # ===============================================
    def show_ui(self):
        """UIの呼び出し
        """

        self.deleteOverlappingWindow(self.joint_finder_gui)

        self.update()

        self.setup_view_event()
        self.joint_finder_gui.show()

    # ===============================================
    def setup_view_event(self):

        self.joint_finder_gui.ui.button_update.clicked.connect(lambda: self.update())
        self.joint_finder_gui.ui.button_copy.clicked.connect(lambda: self.copy())

        self.joint_finder_gui.ui.list_parts.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.joint_finder_gui.ui.list_parts.itemSelectionChanged.connect(lambda: self.list_parts_func())

        self.joint_finder_gui.ui.button_select_highlight.clicked.connect(lambda: self.select_highlight_joint())

        self.joint_finder_gui.ui.check_sp.clicked.connect(lambda: self.filter_check_func())
        self.joint_finder_gui.ui.check_ex.clicked.connect(lambda: self.filter_check_func())
        self.joint_finder_gui.ui.check_tp.clicked.connect(lambda: self.filter_check_func())
        self.joint_finder_gui.ui.check_pc.clicked.connect(lambda: self.filter_check_func())

        self.joint_finder_gui.ui.list_spjoint.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.joint_finder_gui.ui.list_spjoint.itemSelectionChanged.connect(lambda: self.list_group_func())

        self.joint_finder_gui.ui.text_target_path.setText(self.default_batch_target_path)
        self.joint_finder_gui.ui.button_select_root.clicked.connect(lambda: self.select_root_event())
        self.joint_finder_gui.ui.text_output_path.setText(self.default_batch_output_path)
        self.joint_finder_gui.ui.button_batch_exe.clicked.connect(lambda: self.batch_exe())

    # ===============================================
    def update(self, is_on_init=False):

        if is_on_init:
            self.initialize_collector()
        else:
            self.refresh_collector()

        if not self.root_long_name or not cmds.objExists(self.root_long_name):
            self.reset()
            return

        self.joint_finder_gui.ui.view_object_text.setText(self.root_long_name)

        self.visible_prefixes = self.get_visible_prefixes()

        self.refresh_result_group_list()
        self.update_ui_parts_list()
        self.update_ui_group_list()

    # ===============================================
    def initialize_collector(self):

        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info()

        if not self.root_long_name and self.chara_info.exists:
            if self.chara_info.part_info.exists:
                self.root_long_name = self.chara_info.part_info.root_node

        this_collector = glp_dag_collector.GlpDagCollector()
        if this_collector.initialize(self.root_long_name):
            self.collector = this_collector

    # ===============================================
    def refresh_collector(self):

        selection = cmds.ls(sl=True, fl=True, l=True)

        if selection:
            self.root_long_name = selection[0]
        else:
            self.root_long_name = ''

        self.initialize_collector()

    # ===============================================
    def refresh_result_group_list(self):

        if not self.collector:
            return

        self.result_group_list = []

        if not self.collector.dag_group_list:
            return

        for dag_group in self.collector.dag_group_list:

            # 下にSpを持たない枝は表示しない
            if dag_group.get_special_joint_prefix() not in self.visible_prefixes:
                if not dag_group.has_special_joint_in_descendents():
                    continue

            self.result_group_list.append(dag_group)

    # ===============================================
    def get_parts_list(self):

        parts_list = []

        if not self.collector:
            return parts_list

        if not self.collector.dag_group_list:
            return parts_list

        for dag_group in self.collector.dag_group_list:

            if not dag_group.joint_parts_name:
                continue

            if dag_group.get_special_joint_prefix() not in self.visible_prefixes:
                continue

            if dag_group.joint_parts_name not in parts_list:
                parts_list.append(dag_group.joint_parts_name)

        return parts_list

    # ===============================================
    def update_ui_parts_list(self):

        self.joint_finder_gui.ui.list_parts.clear()

        parts_list = self.get_parts_list()

        if not parts_list:
            return

        for part in parts_list:
            this_item = QtWidgets.QListWidgetItem(part)
            self.joint_finder_gui.ui.list_parts.addItem(this_item)

    # ===============================================
    def update_ui_group_list(self):

        if not self.result_group_list:
            return

        self.joint_finder_gui.ui.list_spjoint.clear()

        for dag_group in self.result_group_list:

            list_text = self.get_group_list_text(dag_group)
            if not list_text:
                continue

            this_item = QtWidgets.QListWidgetItem(list_text)

            if not dag_group.get_special_joint_prefix():
                this_item.setForeground(self.no_spjoint_brush)

            self.joint_finder_gui.ui.list_spjoint.addItem(this_item)

    # ===============================================
    def reset(self):
        """UIと変数の情報をリセットする
        """

        # dialogの複数回出現を抑制する為にシグナルを一時的に停止する
        self.joint_finder_gui.ui.list_parts.blockSignals(True)
        self.joint_finder_gui.ui.list_spjoint.blockSignals(True)
        self.joint_finder_gui.ui.check_sp.blockSignals(True)
        self.joint_finder_gui.ui.check_ex.blockSignals(True)
        self.joint_finder_gui.ui.check_tp.blockSignals(True)
        self.joint_finder_gui.ui.check_pc.blockSignals(True)

        self.joint_finder_gui.ui.view_object_text.setText('')
        self.joint_finder_gui.ui.list_parts.clear()
        self.joint_finder_gui.ui.list_spjoint.clear()

        self.highlight_item_list = []
        self.highlight_joint_list = []

        # 処理が終わったらシグナルを再開する
        self.joint_finder_gui.ui.list_parts.blockSignals(False)
        self.joint_finder_gui.ui.list_spjoint.blockSignals(False)
        self.joint_finder_gui.ui.check_sp.blockSignals(False)
        self.joint_finder_gui.ui.check_ex.blockSignals(False)
        self.joint_finder_gui.ui.check_tp.blockSignals(False)
        self.joint_finder_gui.ui.check_pc.blockSignals(False)

    # ===============================================
    def filter_check_func(self):

        if self.root_long_name and not cmds.objExists(self.root_long_name):
            QtWidgets.QMessageBox.warning(
                None,
                'エラー',
                '現在表示中のオブジェクトに指定されているオブジェクトがシーンに存在しないため、リストをリセットします',
                QtWidgets.QMessageBox.Ok
            )

            self.reset()
            return

        self.visible_prefixes = self.get_visible_prefixes()

        self.refresh_result_group_list()
        self.update_ui_parts_list()
        self.update_ui_group_list()

    # ===============================================
    def get_group_list_text(self, dag_group):

        if not dag_group:
            return ''

        if not cmds.objExists(dag_group.top_joint_info.long_name):
            return ''

        list_text = '   ' * dag_group.depth_from_root + '-'
        name = dag_group.base_name

        if dag_group.get_special_joint_prefix():
            name += ' [{}]'.format(str(len(dag_group.member_info_list)))
        else:
            name = '({})'.format(name)

        list_text = list_text + name

        return list_text

    # ===============================================
    def list_parts_func(self):

        if self.root_long_name and not cmds.objExists(self.root_long_name):
            QtWidgets.QMessageBox.warning(
                None,
                'エラー',
                '現在表示中のオブジェクトに指定されているオブジェクトがシーンに存在しないため、リストをリセットします',
                QtWidgets.QMessageBox.Ok
            )

            self.reset()
            return

        self.update_ui_group_list()
        selected_item_list = self.joint_finder_gui.ui.list_parts.selectedItems()

        if not selected_item_list:
            return

        target_parts_list = []

        for item in selected_item_list:
            if item.text not in target_parts_list:
                target_parts_list.append(item.text())

        if not target_parts_list:
            return

        if not self.result_group_list:
            return

        highlight_row_list = []
        self.highlight_item_list = []
        self.highlight_joint_list = []

        for i, group in enumerate(self.result_group_list):
            if group.joint_parts_name in target_parts_list and i not in highlight_row_list:
                if not cmds.objExists(group.top_joint_info.long_name):
                    continue

                highlight_row_list.append(i)
                menber_info_list = group.member_info_list
                if menber_info_list:
                    menber_joint_name_list = [info.long_name for info in menber_info_list if cmds.objExists(info.long_name)]
                    self.highlight_joint_list.extend(menber_joint_name_list)

        for row in highlight_row_list:
            item = self.joint_finder_gui.ui.list_spjoint.item(row)
            item.setBackground(self.highlight_brush)
            self.highlight_item_list.append(item)

        if highlight_row_list:
            item = self.joint_finder_gui.ui.list_spjoint.item(highlight_row_list[-1])
            self.joint_finder_gui.ui.list_spjoint.scrollToItem(item)

    # ===============================================
    def select_highlight_joint(self):
        """ハイライト表示されているJointを選択する
        """

        # 揺れ骨リストの選択状態を解除
        for row in range(self.joint_finder_gui.ui.list_spjoint.count()):
            item = self.joint_finder_gui.ui.list_spjoint.item(row)
            self.joint_finder_gui.ui.list_spjoint.setItemSelected(item, False)

        # Currentを設定して選択履歴(点線囲み)が残らないように
        if self.highlight_item_list:
            self.joint_finder_gui.ui.list_spjoint.setCurrentItem(self.highlight_item_list[-1])

        # ハイライトされている揺れ骨のリストを選択
        for item in self.highlight_item_list:
            self.joint_finder_gui.ui.list_spjoint.setItemSelected(item, True)

        cmds.select(self.highlight_joint_list)

    # ===============================================
    def list_group_func(self):

        if self.root_long_name and not cmds.objExists(self.root_long_name):
            QtWidgets.QMessageBox.warning(
                None,
                'エラー',
                '現在表示中のオブジェクトに指定されているオブジェクトがシーンに存在しないため、リストをリセットします',
                QtWidgets.QMessageBox.Ok
            )
            self.reset()
            return

        selection_row_list = self.get_selection_row_list(self.joint_finder_gui.ui.list_spjoint)

        if not selection_row_list:
            return

        select_info_list = []

        for index in selection_row_list:
            select_info_list.extend(self.result_group_list[index].member_info_list)

        select_list = []

        for info in select_info_list:

            if not cmds.objExists(info.long_name):
                QtWidgets.QMessageBox.warning(
                    None,
                    'エラー',
                    '選択したジョイントが存在しないため、リストをリセットします',
                    QtWidgets.QMessageBox.Ok
                )
                self.reset()
                cmds.select(cl=True)
                self.update()
                return

            select_list.append(info.long_name)

        cmds.select(select_list)

    # ===============================================
    def get_selection_row_list(self, list_widget):

        selected_item_list = list_widget.selectedItems()

        if not selected_item_list:
            return

        target_row_list = []

        for item in selected_item_list:
            target_row_list.append(list_widget.row(item))

        return target_row_list

    def get_visible_prefixes(self):

        # 表示をフィルターするチェックボックス
        prefix_filter_checks = [
            self.joint_finder_gui.ui.check_sp,
            self.joint_finder_gui.ui.check_ex,
            self.joint_finder_gui.ui.check_tp,
            self.joint_finder_gui.ui.check_pc,
        ]

        visible_prefixes = []

        # チェックされているラベル（＝接頭辞）を収集
        for check in prefix_filter_checks:
            if check.checkState():
                visible_prefixes.append(check.text())

        return visible_prefixes

    # ===============================================
    def copy(self):

        item_count = self.joint_finder_gui.ui.list_spjoint.count()

        if not item_count:
            return

        text = ''

        for index in range(item_count):
            item = self.joint_finder_gui.ui.list_spjoint.item(index)
            text += item.text() + '\n'

        result = self.copy_to_clipboard(text)
        if not result:
            print('Copy Failed')

    # ===============================================
    def copy_to_clipboard(self, text):
        try:
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            p.stdin.write(text.encode('utf-8'))
            p.stdin.close()

            retcode = p.wait()
            return True
        except Exception:
            return False

    # ===============================================
    def select_root_event(self):

        paths = cmds.fileDialog2(fileMode=3)
        if not paths:
            return

        path = paths[0]
        if not os.path.exists(path) or not os.path.isdir(path):
            return

        self.joint_finder_gui.ui.text_target_path.setText(path)

    # ===============================================
    def batch_exe(self):

        target_path = self.joint_finder_gui.ui.text_target_path.text()
        output_path = self.joint_finder_gui.ui.text_output_path.text()

        if not os.path.exists(target_path):
            return

        target_path_list = []
        for curDir, dirs, files in os.walk(target_path):
            for file in files:
                if file.endswith(".ma"):
                    target_path_list.append(os.path.join(curDir, file))

        base_utility.simple_batch.execute(
            '{0}{1}'.format(
                'import Project_Gallop.glp_sp_joint_finder.glp_sp_joint_finder;',
                'Project_Gallop.glp_sp_joint_finder.glp_sp_joint_finder.batch();'
            ),
            True,
            target_path_list=target_path_list,
            output_file_path=output_path
        )

    # ===============================================
    def batch_export(self):

        target_file_path_list = \
            base_utility.simple_batch.get_param_value(
                'target_path_list')

        output_file_path = \
            base_utility.simple_batch.get_param_value(
                'output_file_path')

        if not target_file_path_list:
            return

        fix_path_list = []

        result_str = ''

        for file_path in target_file_path_list:

            try:
                this_chara_info = chara_info.CharaInfo()
                this_chara_info.create_info(file_path)
            except Exception:
                continue

            if not this_chara_info.part_info:
                continue

            if not this_chara_info.part_info.maya_file_list:
                continue

            if not os.path.basename(file_path) == os.path.basename(this_chara_info.part_info.maya_file_list[0]):
                continue

            fix_path_list.append(file_path)

        for file_path in fix_path_list:

            result_str += '=' * 20 + '\n'
            result_str += 'FILE: {}'.format(file_path) + '\n' * 2

            try:
                base_utility.file.open(file_path)
                self.root_long_name = ''
                self.initialize_collector()
                self.visible_prefixes = self.batch_output_prefixes
                self.refresh_result_group_list()

                for group in self.result_group_list:
                    text = self.get_group_list_text(group)
                    result_str += text + '\n'

                result_str += '\n' * 2

            except Exception:
                result_str += 'ERROR: CANNOT OUTPUT!!!' + '\n' * 2

        try:
            with open(output_file_path, mode='w') as log:
                log.write(result_str)
        except Exception:
            pass
