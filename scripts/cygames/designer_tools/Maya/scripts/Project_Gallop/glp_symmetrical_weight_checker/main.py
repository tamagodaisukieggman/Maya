# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

from PySide2 import QtGui, QtWidgets
from maya import OpenMayaUI
import maya.cmds as cmds
import shiboken2

from ..base_common import utility as base_utility

from . import glp_symmetrical_weight_checker_gui
from . import symmetrical_weight_checker

reload(symmetrical_weight_checker)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):
    """処理等を記載していくメインのクラス
    """

    # ===============================================
    def __init__(self):

        self.tool_gui = glp_symmetrical_weight_checker_gui.GUI()
        self.manager = None
        self.result_symmetrical_item_list = []
        self.result_info_dict_list = []

        self.result_tabel_col_size = 2
        self.result_title = ['-', '+']

        self.target_transform = ''
        self.symmetrical_axis = 'x'
        self.joint_search_type = 'name'
        self.symmetrical_str_list = ['L', 'R']
        self.torlerance = 0.001
        self.filter_list = []

        self.no_pair_bg_brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        self.inf_error_brush = QtGui.QBrush(QtGui.QColor(64, 0, 0))
        self.weight_error_brush = QtGui.QBrush(QtGui.QColor(0, 0, 64))

        self.symmetrical_axis_tooltip = \
            '対称を確認する座標を選択してください'
        self.influence_check_type_tooltip = \
            '頂点のインフルエンスの対称性を\n　・ジョイント名\n　・ジョイント位置\nが対称かで判定します'

    # ===============================================
    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        try:
            main_window = shiboken2.wrapInstance(
                long(main_window), QtWidgets.QMainWindow)
        except Exception:
            # Maya 2022-
            main_window = shiboken2.wrapInstance(
                int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if type(target) == type(widget):
                widget.close()          # クローズイベントを呼んでウインドウを閉じる
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

    # ===============================================
    def show_ui(self):
        """UIの呼び出し
        """

        self.deleteOverlappingWindow(self.tool_gui)

        self.__setup_view_event()
        self.tool_gui.show()
        self.__initialize_ui()

    # ===============================================
    def __setup_view_event(self):

        self.tool_gui.addCallback('SelectionChanged', self.__target_select_func)

        # メイン設定
        self.tool_gui.ui.axis_x_radio_button.clicked.connect(self.__update_symmetry_axis)
        self.tool_gui.ui.axis_y_radio_button.clicked.connect(self.__update_symmetry_axis)
        self.tool_gui.ui.axis_z_radio_button.clicked.connect(self.__update_symmetry_axis)

        self.tool_gui.ui.axis_x_radio_button.setToolTip(self.symmetrical_axis_tooltip)
        self.tool_gui.ui.axis_y_radio_button.setToolTip(self.symmetrical_axis_tooltip)
        self.tool_gui.ui.axis_z_radio_button.setToolTip(self.symmetrical_axis_tooltip)

        self.tool_gui.ui.by_name_radio_button.clicked.connect(self.__update_search_type)
        self.tool_gui.ui.by_pos_radio_button.clicked.connect(self.__update_search_type)

        self.tool_gui.ui.by_name_radio_button.setToolTip(self.influence_check_type_tooltip)
        self.tool_gui.ui.by_pos_radio_button.setToolTip(self.influence_check_type_tooltip)

        # オプション設定
        self.tool_gui.ui.symmetrical_str.textChanged.connect(self.__update_symmetrical_str)
        self.tool_gui.ui.torelance.textChanged.connect(self.__update_torelance)

        # リストフィルター
        self.tool_gui.ui.inf_error_checkbox.stateChanged.connect(self.__update_result_table)
        self.tool_gui.ui.weight_error_checkbox.stateChanged.connect(self.__update_result_table)
        self.tool_gui.ui.normal_pair_checkbox.stateChanged.connect(self.__update_result_table)
        self.tool_gui.ui.no_pair_checkbox.stateChanged.connect(self.__update_result_table)

        # 実行ボタン
        self.tool_gui.ui.exe_button.clicked.connect(self.do_check)

        # 結果テーブル
        self.tool_gui.ui.result_vtx_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tool_gui.ui.result_vtx_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tool_gui.ui.result_vtx_table.verticalHeader().setVisible(False)
        self.tool_gui.ui.result_vtx_table.horizontalHeader().setStretchLastSection(True)

        self.tool_gui.ui.result_vtx_table.itemSelectionChanged.connect(self.__result_table_func)
        self.tool_gui.ui.result_vtx_table.itemClicked.connect(self.__result_table_func)

        # 情報リスト
        self.tool_gui.ui.result_info_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tool_gui.ui.result_info_list.itemSelectionChanged.connect(self.__result_info_func)
        self.tool_gui.ui.result_info_list.itemClicked.connect(self.__result_info_func)

        # ウェイト修正
        self.tool_gui.ui.all_negative_button.clicked.connect(self.__adjust_weight_all_negative)
        self.tool_gui.ui.all_positive_button.clicked.connect(self.__adjust_weight_all_positive)
        self.tool_gui.ui.select_negative_button.clicked.connect(self.__adjust_weight_selection_negative)
        self.tool_gui.ui.select_positive_button.clicked.connect(self.__adjust_weight_selection_positive)

    # ===============================================
    def __initialize_ui(self, arg=None):

        # オプション設定
        self.tool_gui.ui.symmetrical_str.setText('L,R')
        self.tool_gui.ui.torelance.setText(str(self.torlerance))

        # 表示項目
        self.tool_gui.ui.inf_error_checkbox.setChecked(True)
        self.tool_gui.ui.weight_error_checkbox.setChecked(True)

        # table
        self.__update_result_table()

        self.__target_select_func()

    # ===============================================
    def do_check(self, arg=None):

        self.target_transform = self.tool_gui.ui.target_obj_text.text()

        if not self.target_transform:
            return

        # できればrootのTransformを選択していてもroot_jointを取得できると良いが、現状はお知らせで済ます
        isMeshSelected = True
        try:
            cmds.select(self.target_transform)
            shape = cmds.listRelatives(cmds.ls(sl=True)[0], shapes=True, fullPath=True, ni=True)
            if not shape or cmds.nodeType(shape) != "mesh":
                isMeshSelected = False
        except Exception:
            isMeshSelected = False

        if not isMeshSelected:
            self.tool_gui.ui.target_obj_text.setText('「メッシュ」を選択して実行してください')
            return

        root_joint = base_utility.mesh.skin.get_skin_root_joint(self.target_transform)

        if not root_joint:
            self.tool_gui.ui.target_obj_text.setText('ルートジョイントが見つかりません。正しくスキニングされているか確認してください')
            return

        # GoToBindPose
        root_list = cmds.ls(root_joint, l=True, r=True)
        if root_list:
            cmds.dagPose(root_list[0], restore=True, g=True, bindPose=True)

        self.tool_gui.ui.result_vtx_table.clear()
        self.tool_gui.ui.result_info_list.clear()

        self.manager = None
        self.manager = symmetrical_weight_checker.SymmetricalPairManager()
        self.manager.initialize(
            self.target_transform,
            self.symmetrical_axis,
            self.joint_search_type,
            self.symmetrical_str_list,
            self.torlerance,
        )
        self.__update_manager_and_ui()

    # ===============================================
    def __update_manager_and_ui(self, is_selection=True):

        if not self.manager or not self.manager.is_ready:
            return

        if is_selection:
            self.manager.create_info()

        if not self.manager.symmetrical_pair_item_list:
            return

        self.__update_result_table()

    # ===============================================
    def __show_axis_tooltip(self, arg=None):

        QtGui.QToolTip.showText(
            QtGui.QCursor.pos(),
            self.symmetrical_axis_tooltip,
        )

    # ===============================================
    def __update_symmetry_axis(self, arg=None):

        if self.tool_gui.ui.axis_x_radio_button.isChecked():
            self.symmetrical_axis = 'x'
        elif self.tool_gui.ui.axis_y_radio_button.isChecked():
            self.symmetrical_axis = 'y'
        elif self.tool_gui.ui.axis_z_radio_button.isChecked():
            self.symmetrical_axis = 'z'
        else:
            self.symmetrical_axis = 'x'

    # ===============================================
    def __update_search_type(self, arg=None):

        if self.tool_gui.ui.by_name_radio_button.isChecked():
            self.joint_search_type = 'name'
        elif self.tool_gui.ui.by_pos_radio_button.isChecked():
            self.joint_search_type = 'pos'
        else:
            self.joint_search_type = 'name'

    # ===============================================
    def __update_symmetrical_str(self, arg=None):

        self.symmetrical_str_list = self.tool_gui.ui.symmetrical_str.text().split(',')

    # ===============================================
    def __update_torelance(self, arg=None):

        current_str = str(self.torlerance)
        new_str = self.tool_gui.ui.torelance.text()

        try:
            self.torlerance = float(new_str)
        except Exception:
            self.tool_gui.ui.torelance.setText(current_str)
            self.torlerance = float(current_str)

    # ===============================================
    def __update_filter_list(self, arg=None):

        self.filter_list = []

        if self.tool_gui.ui.inf_error_checkbox.isChecked():
            self.filter_list.append('inf_error')
        if self.tool_gui.ui.weight_error_checkbox.isChecked():
            self.filter_list.append('weight_error')
        if self.tool_gui.ui.normal_pair_checkbox.isChecked():
            self.filter_list.append('normal_pair')
        if self.tool_gui.ui.no_pair_checkbox.isChecked():
            self.filter_list.append('no_pair')

    # ===============================================
    def __target_select_func(self, arg=None):

        select_list = cmds.ls(sl=True, et='transform', fl=True, l=True)

        if not select_list:
            self.target_transform = ''
            self.tool_gui.ui.target_obj_text.setText('メッシュを選択してください')
            return

        self.tool_gui.ui.target_obj_text.setText(select_list[0])

    # ===============================================
    def __update_result_table(self):

        self.tool_gui.ui.result_vtx_table.clear()
        self.tool_gui.ui.result_info_list.clear()

        self.tool_gui.ui.result_vtx_table.setColumnCount(self.result_tabel_col_size)
        self.tool_gui.ui.result_vtx_table.setHorizontalHeaderLabels(self.result_title)
        self.tool_gui.ui.result_vtx_table.setRowCount(0)

        if not self.manager:
            return

        self.__update_filter_list()

        self.result_symmetrical_item_list = self.manager.get_filtered_item_list(self.filter_list)

        if not self.result_symmetrical_item_list:
            return

        self.tool_gui.ui.result_vtx_table.setRowCount(len(self.result_symmetrical_item_list))
        for i, symmetrical_item in enumerate(self.result_symmetrical_item_list):

            this_label_list = symmetrical_item.get_vtx_pair_label_list()

            this_nagetive_item = QtWidgets.QTableWidgetItem(this_label_list[1])
            this_positive_item = QtWidgets.QTableWidgetItem(this_label_list[0])

            # カラムの背景色指定
            this_brush = None

            if not symmetrical_item.check_result:
                # エラーの場合
                this_brush = self.__get_error_color_brush_from_item(symmetrical_item)

            elif not symmetrical_item.has_pair:
                # ペアがない場合
                this_brush = self.no_pair_bg_brush

            if this_brush:
                this_nagetive_item.setBackground(this_brush)
                this_positive_item.setBackground(this_brush)

            self.tool_gui.ui.result_vtx_table.setItem(i, 0, this_nagetive_item)
            self.tool_gui.ui.result_vtx_table.setItem(i, 1, this_positive_item)

    # ===============================================
    def __result_table_func(self):

        current_target = self.tool_gui.ui.target_obj_text.text()
        selected_item_list = self.tool_gui.ui.result_vtx_table.selectedItems()

        if not selected_item_list:
            return

        target_row_list = []

        for item in selected_item_list:
            target_row_list.append(item.row())

        target_row_list = list(set(target_row_list))

        target_item_list = []

        for i, item in enumerate(self.result_symmetrical_item_list):
            if i in target_row_list:
                target_item_list.append(item)

        # 選択
        vtx_list = []

        for item in target_item_list:
            if item.positive_vtx_data:
                vtx_list.append(item.positive_vtx_data.name)
            if item.negative_vtx_data:
                vtx_list.append(item.negative_vtx_data.name)

        cmds.select(vtx_list)
        self.tool_gui.ui.target_obj_text.setText(current_target)

        # 情報リスト更新
        self.__update_result_info(target_item_list)

    # ===============================================
    def __update_result_info(self, item_list):

        self.tool_gui.ui.result_info_list.clear()
        self.result_info_dict_list = []

        if not item_list:
            return

        for item in item_list:

            this_info_dict_list = self.__get_item_info_dict_list(item)
            self.result_info_dict_list.extend(this_info_dict_list)

            # スペーサー
            space_item = QtWidgets.QListWidgetItem('')
            self.result_info_dict_list.append({'list_item': space_item, 'target_data': None})

        for result_info_dict in self.result_info_dict_list:
            this_item = result_info_dict['list_item']
            self.tool_gui.ui.result_info_list.addItem(this_item)

    # ===============================================
    def __get_item_info_dict_list(self, item):

        result_info_dict_list = []

        # ヘッダー
        header_str = ''
        target_data_list = []

        if not item.positive_vtx_data:
            header_str = '== {} =='.format(item.negative_vtx_data.label)
            target_data_list = [item.negative_vtx_data]
        elif not item.negative_vtx_data:
            header_str = '== {} =='.format(item.positive_vtx_data.label)
            target_data_list = [item.positive_vtx_data]
        else:
            header_str = '== {} / {} =='.format(item.negative_vtx_data.label, item.positive_vtx_data.label)
            target_data_list = [item.negative_vtx_data, item.positive_vtx_data]

        header_item = QtWidgets.QListWidgetItem(header_str)
        result_info_dict_list.append({'list_item': header_item, 'target_data_list': target_data_list})

        # ジョイント、ウェイト情報
        for influence_pair_item in item.influence_pair_item_list:

            indent_str = '    '
            positive_dict = None
            negative_dict = None
            error_dict = None
            this_brush = None

            if influence_pair_item.positive_joint_data:
                joint_data = influence_pair_item.positive_joint_data
                weight = influence_pair_item.positive_weight
                positive_info_str = indent_str + '[＋] {}: {}'.format(joint_data.label, str(weight))
                positive_item = QtWidgets.QListWidgetItem(positive_info_str)
                positive_dict = {'list_item': positive_item, 'target_data_list': [joint_data]}
            else:
                positive_info_str = indent_str + '[＋] [     ]'
                positive_item = QtWidgets.QListWidgetItem(positive_info_str)
                positive_dict = {'list_item': positive_item, 'target_data_list': []}

            if influence_pair_item.negative_joint_data:
                joint_data = influence_pair_item.negative_joint_data
                weight = influence_pair_item.negative_weight
                negative_info_str = indent_str + '[―] {}: {}'.format(joint_data.label, str(weight))
                negative_item = QtWidgets.QListWidgetItem(negative_info_str)
                negative_dict = {'list_item': negative_item, 'target_data_list': [joint_data]}
            else:
                negative_info_str = indent_str + '[―] [     ]'
                negative_item = QtWidgets.QListWidgetItem(negative_info_str)
                negative_dict = {'list_item': negative_item, 'target_data_list': []}

            error_str_list = []
            mix_brush_list = []

            if not item.check_result:

                if influence_pair_item.is_symmetrical_inf and not influence_pair_item.is_symmetrical_weight:
                    mix_brush_list.append(self.weight_error_brush)
                    error_str_list.append('ウェイトが非対称です')

                if not influence_pair_item.is_symmetrical_inf:

                    mix_brush_list.append(self.inf_error_brush)

                    if self.manager.joint_search_type == 'pos':
                        error_str_list.append('対称位置のジョイントがありません')
                    elif self.manager.joint_search_type == 'name':
                        error_str_list.append('対称な名前（階層も含む）のジョイントがありません')
                    else:
                        error_str_list.append('不明なインフルエンスエラー')

            if error_str_list:
                error_info_str = indent_str + '***' + ','.join(error_str_list) + '***'
                error_item = QtWidgets.QListWidgetItem(error_info_str)
                error_dict = {'list_item': error_item, 'target_data_list': []}

            if mix_brush_list:
                this_brush = self.__get_mix_brush(mix_brush_list)

            if this_brush:
                error_dict['list_item'].setBackground(this_brush)
                if positive_dict:
                    positive_dict['list_item'].setBackground(this_brush)
                if negative_dict:
                    negative_dict['list_item'].setBackground(this_brush)

            if negative_dict:
                result_info_dict_list.append(negative_dict)
            if positive_dict:
                result_info_dict_list.append(positive_dict)
            if error_dict:
                result_info_dict_list.append(error_dict)

            space_item = QtWidgets.QListWidgetItem('')
            result_info_dict_list.append({'list_item': space_item, 'target_data_list': []})

        return result_info_dict_list

    # ===============================================
    def __result_info_func(self):

        current_target = self.tool_gui.ui.target_obj_text.text()
        selected_item_list = self.tool_gui.ui.result_info_list.selectedItems()

        if not selected_item_list:
            return

        target_row_list = []

        for item in selected_item_list:
            target_row_list.append(self.tool_gui.ui.result_info_list.row(item))

        target_row_list = list(set(target_row_list))

        select_target_list = []

        for index in target_row_list:
            this_select_dict = self.result_info_dict_list[index]

            if not this_select_dict['target_data_list']:
                continue

            for target_data in this_select_dict['target_data_list']:

                if not cmds.objExists(target_data.name):
                    continue

                select_target_list.append(target_data.name)

        cmds.select(select_target_list)
        self.tool_gui.ui.target_obj_text.setText(current_target)

    # ===============================================
    def __adjust_weight_all_positive(self):
        self.manager.adjust_weight_all('positive')
        if self.tool_gui.ui.refresh_list_checkbox.isChecked():
            self.__update_manager_and_ui()

    # ===============================================
    def __adjust_weight_all_negative(self):
        self.manager.adjust_weight_all('negative')
        if self.tool_gui.ui.refresh_list_checkbox.isChecked():
            self.__update_manager_and_ui()

    # ===============================================
    def __adjust_weight_selection_positive(self):
        self.manager.adjust_weight_selection('positive')
        if self.tool_gui.ui.refresh_list_checkbox.isChecked():
            self.__update_manager_and_ui(False)

    # ===============================================
    def __adjust_weight_selection_negative(self):
        self.manager.adjust_weight_selection('negative')
        if self.tool_gui.ui.refresh_list_checkbox.isChecked():
            self.__update_manager_and_ui(False)

    # ===============================================
    def __get_error_color_brush_from_item(self, item):

        if not item:
            return

        mix_brush_list = []

        if not item.is_symmetrical_inf:
            mix_brush_list.append(self.inf_error_brush)

        if not item.is_symmetrical_weight:
            mix_brush_list.append(self.weight_error_brush)

        return self.__get_mix_brush(mix_brush_list)

    # ===============================================
    def __get_mix_brush(self, brush_list):

        if not brush_list:
            return

        final_red = 0
        final_green = 0
        final_blue = 0

        for brush in brush_list:
            q_color = brush.color()

            final_red += q_color.red()
            final_green += q_color.green()
            final_blue += q_color.blue()

        return QtGui.QBrush(QtGui.QColor(final_red, final_green, final_blue))
