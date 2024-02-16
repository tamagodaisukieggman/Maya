# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import time
import typing as tp
import functools

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.cmds as cmds
from ...common.maya_checker.data import DebugData, ErrorType
from ...common.maya_checker.checker import Checker
from .detail_controller import DetailMainWindow
from .fix_controller import FixMainWindow
from . import utils

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
MAIN_UIFILEPATH = filePath + "/ui/main.ui"
SELECTOR_UIFILEPATH = filePath + "/ui/task_sub.ui"


class CheckerMainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    def __init__(self, parent=None, **kwargs):
        super(CheckerMainWindow, self).__init__(parent)

        checker_name = kwargs["checker_name"]
        checker_version = kwargs["checker_ui_version"]

        self.tool_title = f"{checker_name}_{checker_version}"

        self.setWindowTitle(self.tool_title)

        self.checker_tasks = kwargs["tasks"]

        checker_helps = kwargs["helps"]
        checker_tools = kwargs["tools"]
        self.checker_settings = kwargs["checker_settings"]

        # post_process_settingsはデフォルトの設定でも使用できるように
        self.post_process_settings = []
        if "post_process_settings" in kwargs:
            self.post_process_settings = kwargs["post_process_settings"]

        self.initialize_main_menu(self.checker_settings, checker_helps, checker_tools)

        self.setObjectName(self.tool_title)

        self.delete_instances()
        # UIのパスを指定
        self.UI = QUiLoader().load(MAIN_UIFILEPATH)

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # cehckerの初期化
        self.initialize()

        self.UI.all_select_btn.clicked.connect(self.execute_all_select_btn)
        self.UI.remove_select_btn.clicked.connect(self.execute_remove_select_btn)
        self.UI.reset_btn.clicked.connect(self.execute_reset_btn)
        self.UI.all_check_btn.clicked.connect(self.execute_all_check_btn)

    def initialize_main_menu(self, checker_settings, checker_helps, checker_tools):
        menubar = self.menuBar()
        if checker_settings["use_helps"]:
            self.rebuild_menu(menubar, "helps", checker_helps)
        if checker_settings["use_tools"]:
            self.rebuild_menu(menubar, "tools", checker_tools)

    def add_new_action(self, menu, action_name, function):
        """
        メニューに新しいアクションを追加する関数

        :param menu: 追加したいメニュー
        :param action_name: アクションの名前
        :param function: アクションがクリックされた際に実行される関数
        """
        new_action = QtWidgets.QAction(action_name, self)
        new_action.triggered.connect(function)
        menu.addAction(new_action)

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def initialize_checker_table(self):
        """CheckerTableWidgetを一度clearして再度生成"""
        self._clear_layout(self.UI.checker_table_lay)
        help_url = None
        if self.checker_settings["use_task_help_link"]:
            help_url = self.checker_settings["task_help_url"]

        self.table = CheckerTableWidget(help_url)
        self.UI.checker_table_lay.addWidget(self.table)

    def initialize_root_nodes(self):
        """reset時に実行されるtargetのrootオブジェクトをリセットする"""
        selected = cmds.ls(sl=True)
        if selected:
            self.root_nodes = self._get_top_parent_nodes(selected)
        else:
            self.root_nodes = self._get_world_parented_groups_without_cameras()
        self.UI.target_object_txt.setText(str(self.root_nodes))

    def check_exist_target_nodes(self) -> bool:
        """root_nodeに値が入っているか
        targetが設定されているか確認するために使用

        Returns:
            bool : root_nodeに値が入っているか
        """
        if self.root_nodes:
            return True
        return False

    def initialize(self):
        """初期化"""
        self.initialize_checker_table()
        self.initialize_root_nodes()

        current_task_datas = self.checker_tasks
        checker_title = self.tool_title
        current_task_names = []
        extra_datas = {}

        # extradataの作成
        self._set_extra_data(current_task_datas, current_task_names, extra_datas)

        self.checker = Checker(
            checker_title,
            current_task_names,
            extra_datas,
            self.root_nodes,
            self.post_process_settings,
        )
        self._initialized_task_table(current_task_datas)
        self.set_error_label()

    @staticmethod
    def _get_world_parented_groups_without_cameras():
        all_transform_nodes = cmds.ls(
            type="transform", l=True
        )  # シーン内のすべてのトランスフォームノードを取得
        all_cameras = cmds.ls(type="camera")  # シーン内のすべてのカメラを取得
        camera_transform_nodes = [
            cmds.listRelatives(camera, parent=True, fullPath=True)[0]
            for camera in all_cameras
        ]  # カメラのトランスフォームノードのリスト
        world_parented_groups = []

        for node in all_transform_nodes:
            # トランスフォームノードがカメラのものでないかどうかをチェック
            if node not in camera_transform_nodes:
                parent = cmds.listRelatives(node, parent=True)  # トランスフォームノードのペアレントを取得
                # ペアレントが存在しない場合は、ワールドにペアレントされているとみなす
                if not parent:
                    world_parented_groups.append(node)

        return world_parented_groups

    def _set_extra_data(
        self,
        current_task_datas: dict,
        current_task_names: tp.List[str],
        extra_datas: dict,
    ):
        """extra dataの作成

        Args:
            current_task_datas (dict): yamからtaskの引っ張ってきたdict
            current_task_names (tp.List[str]): taskの名前の配列
            extra_datas (dict): 参照で変更するextra_data
        """
        for task_data in current_task_datas:
            if task_data["type"] != "task":
                continue

            task_name = task_data["name"]

            current_task_names.append(task_name)
            if "extra_data" in task_data and task_data["extra_data"]:
                extra_datas.update({task_name: task_data["extra_data"]})

    def _get_top_parent_nodes(self, targets: tp.List[str]) -> tp.List[str]:
        """対象のオブジェクトまたはコンポーネントの最も親となるノードを取得する関数

        Args:
            targets (tp.List[str]): 対象のオブジェクト名またはコンポーネント名のリスト

        Returns:
            tp.List[str]: 最も親となるノード名のリスト
        """
        top_parent_nodes = []
        for target in targets:
            # コンポーネントが対象の場合、そのオブジェクトを対象にする
            if "." in target:
                target = target.split(".")[0]
            # 最も親となるノードを取得する
            parent = cmds.listRelatives(target, parent=True, pa=True)
            while parent:
                target = parent[0]
                parent = cmds.listRelatives(target, parent=True, pa=True)
            if target not in top_parent_nodes:
                top_parent_nodes.append(target)
        return top_parent_nodes

    def _initialized_task_table(self, current_task_datas):
        """task_tableの初期化

        Args:
            current_task_datas (dict): {taskname:taskdata}
        """
        for task_data in current_task_datas:
            self.add_list(task_data)

    def add_list(self, task_data: dict):
        """task_dataに基づいて行追加

        Args:
            task_data (dict): 追加する行の元になる情報
        """
        if task_data["type"] == "separator":
            self._insert_seperator(task_data)
            ...
        elif task_data["type"] == "task":
            self._insert_task_line(task_data)

    def _insert_seperator(self, task_data: dict):
        """seperatorの作成

        Args:
            task_data (dict): taskのyamlで定義しているdict
        """
        separator_label = task_data["label"]

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(separator_label))

        label_item = self.table.item(row, 2)
        font = label_item.font()
        font.setBold(True)
        label_item.setFont(font)

        if "back_ground_color" in task_data:
            back_ground_color = QtGui.QColor(task_data["back_ground_color"])

        else:
            back_ground_color = QtGui.QColor("gray")

        if "text_color" in task_data:
            text_color = QtGui.QColor(task_data["text_color"])

        else:
            text_color = QtGui.QColor("white")

        label_item.setForeground(text_color)

        for column in range(self.table.columnCount()):
            item = self.table.item(row, column)
            if item is None:
                item = QtWidgets.QTableWidgetItem("")
                self.table.setItem(row, column, item)
            self.table.item(row, column).setBackground(back_ground_color)

    # TODO: task_nameをtask_dataにする(separatorと統一する)
    def _insert_task_line(self, task_data: dict):
        """seperatorの作成

        Args:
            task_name (str): taskのyamlで定義している名前
        """
        task_name = task_data["name"]
        # 対象となるタスク
        task = self.checker._get_new_task_by_taskname(task_name)

        # 行追加
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(task_name))

        # タスク名の設定

        task_label = task.checker_info.label_name
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(task_label))

        # チェックボタンを生成
        button = QtWidgets.QPushButton(self)
        button.clicked.connect(self.execute_single_check_btn)
        button.setText("チェック")
        self.table.setCellWidget(row, 3, button)

        # 詳細ボタン追加
        detail_button = QtWidgets.QPushButton(self)
        detail_button.clicked.connect(self.execute_detail_btn)
        detail_button.setText("詳細")
        self.table.setCellWidget(row, 5, detail_button)

        if "use_fixed_method" in task_data:
            if task_data["use_fixed_method"] == True:
                # 修正ボタン追加
                fixed_button = QtWidgets.QPushButton(self)
                fixed_button.clicked.connect(self.execute_fixed_btn)
                fixed_button.setText("修正")
                self.table.setCellWidget(row, 6, fixed_button)
                # fixed_button.setEnabled(False)

        # checkboxの追加
        checked = True
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)
        self.table.setItem(row, 1, item)

        self.table._update_error_status(row, task.debug_data.error_type)

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            cmds.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    def show_manual(self):
        """コンフルのツールマニュアルページを開く"""
        try:
            utils.search_website(
                "https://wisdom.cygames.jp/pages/viewpage.action?pageId=673570123", ""
            )
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")

    def execute_detail_btn(self):
        """taskの詳細パネル（デバッグパネル）を開く"""
        # ボタンを推した行のitemを取得
        # ボタンを推した行のitemを取得

        row = self.table._get_pushed_button_row(self.sender())
        task_name = self.table._get_current_task_name(row)
        debug_data = self.checker.get_debug_data(task_name)
        sub_detail_window = DetailMainWindow(task_name, debug_data)
        sub_detail_window.show()

    def execute_fixed_btn(self):
        """修正ボタンを押したときの実行"""

        row = self.table._get_pushed_button_row(self.sender())
        task_name = self.table._get_current_task_name(row)

        before_debug_data = self.checker.get_debug_data(task_name)

        progress_window, progress_bar = utils.create_progress_bar(1)
        cmds.progressBar(progress_bar, edit=True, step=1)
        time.sleep(0.1)

        error_names = list(before_debug_data.error_target_info.keys())
        error_objects = []
        for error_name in error_names:
            error_objects.extend(
                before_debug_data.error_target_info[error_name]["target_objects"]
            )

        is_missing_object = False
        for error_object in error_objects:
            if error_object and not cmds.objExists(error_object):
                is_missing_object = True

        if is_missing_object:
            self.exec_task_by_task_name(task_name)
            before_debug_data = self.checker.get_debug_data(task_name)

        if before_debug_data.error_type in [ErrorType.NOERROR, ErrorType.NOCHECKED]:
            cmds.warning("現在修正する対象は存在しません。")
            cmds.deleteUI(progress_window)
            return

        self.exec_fix_by_task_name(task_name)
        self.execute_single_check_btn()

        after_debug_data = self.checker.get_debug_data(task_name)

        sub_detail_window = FixMainWindow(
            task_name, before_debug_data, after_debug_data
        )
        sub_detail_window.show()

        cmds.deleteUI(progress_window)

    def execute_single_check_btn(self):
        """単体のチェックボタンを押したときの実行"""

        progress_window, progress_bar = utils.create_progress_bar(1)

        cmds.progressBar(progress_bar, edit=True, step=1)
        time.sleep(0.1)

        # ボタンを推した行のitemを取得
        self.checker._reset_maya_scene_data()
        # ボタンを推した行のitemを取得
        row = self.table._get_pushed_button_row(self.sender())
        task_name = self.table._get_current_task_name(row)
        self.exec_task_by_task_name(task_name)

        # デバッグ表示の更新
        debugdata = self.checker.get_debug_data(task_name)
        self.table.update_error_status_by_task_name(task_name, debugdata.error_type)
        self.set_error_label()

        cmds.deleteUI(progress_window)

    def execute_all_select_btn(self):
        """全てのタスクを選択状態にする"""
        for task_name in self.checker.current_tasks:
            self.table.set_checkstate_by_task_name(task_name, True)

    def execute_remove_select_btn(self):
        """チェックボックスをオフ"""
        for task_name in self.checker.current_tasks:
            self.table.set_checkstate_by_task_name(task_name, False)

    def execute_reset_btn(self):
        """チェック状態のリセット/選択ノードの再取得"""
        self.initialize()

    def execute_all_check_btn(self):
        """全ての選択taskを実行"""
        progress_window, progress_bar = utils.create_progress_bar(
            len(self.checker.current_tasks)
        )
        self.checker._reset_maya_scene_data()
        for task_name in self.checker.current_tasks:
            state = self.table.get_checkstate_by_task_name(task_name)
            if state:
                self.exec_task_by_task_name(task_name)
                debugdata = self.checker.get_debug_data(task_name)
                self.table.update_error_status_by_task_name(
                    task_name, debugdata.error_type
                )
            cmds.progressBar(progress_bar, edit=True, step=1)

        self.set_error_label()

        cmds.deleteUI(progress_window)

    def exec_task_by_task_name(self, task_name: str):
        """task_nameに当たるタスクを取得してチェック実行
        併せて事前チェックも実行(対象が設定されているかどうか)

        Args:
            task_name (str): タスク名
        """
        is_valid = self.check_exist_target_nodes()
        if is_valid:
            self.checker.exec_task_by_taskname(task_name)
        else:
            cmds.warning("Root node of target is not set. Finish processing.")

    def exec_fix_by_task_name(self, task_name: str):
        """task_nameに当たるタスクを取得して修正実行
        併せて事前チェックも実行(対象が設定されているかどうか)

        Args:
            task_name (str): タスク名
        """
        is_valid = self.check_exist_target_nodes()
        if is_valid:
            self.checker.exec_fix_by_taskname(task_name)
        else:
            cmds.warning("Root node of target is not set. Finish processing.")

    def exec_action_export_joint_attributes(self):
        # other_tools.export_selected_joint_attributes()
        ...

    def set_error_label(self):
        """現在のデバッグ情報に合わせてerror_labelを更新する"""
        counts = self.get_error_count(self.checker.debug_datas)
        self.UI.error_txt.setAutoFillBackground(True)
        self.UI.error_txt.setAlignment(QtCore.Qt.AlignCenter)
        if counts["error_count"] > 0:
            self.UI.error_txt.setText(f'error >> {counts["error_count"]}')
            self.UI.error_txt.setAutoFillBackground(True)
            self.UI.error_txt.setStyleSheet(
                "QLabel { background-color: red; color: white; }"
            )
        elif counts["error_count"] <= 0 and counts["warning_count"] > 0:
            self.UI.error_txt.setText(f'warning >> {counts["warning_count"]}')
            self.UI.error_txt.setStyleSheet(
                "QLabel { background-color: yellow; color: black; }"
            )
        else:
            self.UI.error_txt.setText(f"NoError")
            self.UI.error_txt.setStyleSheet(
                "QLabel { background-color: lightgreen; color: black; }"
            )

    def get_error_count(self, debug_datas: tp.List[DebugData]) -> dict:
        """error数を取得する

        Args:
            debug_datas (tp.List[DebugData]): debugデータの配列

        Returns:
            dict: エラーの各カウント
        """
        count = {}
        count["error_count"] = 0
        count["warning_count"] = 0
        count["noerror_count"] = 0

        for task_name in debug_datas:
            debug_data = debug_datas[task_name]
            if debug_data.error_type == ErrorType.ERROR:
                count["error_count"] = count["error_count"] + 1
            elif debug_data.error_type == ErrorType.WARNING:
                count["warning_count"] = count["warning_count"] + 1
            elif debug_data.error_type == ErrorType.NOERROR:
                count["noerror_count"] = count["noerror_count"] + 1
        return count

    def add_actions(self, menu, datas):
        """メニュー追加

        Args:
            menu (QMenu): アクションを追加するメニュー
            datas (dict):
        """
        func = None
        for data in datas:
            if data["type"] == "link":
                func = functools.partial(utils.search_website, data["value"], "")
            elif data["type"] == "command":
                temp_exec = lambda value: exec(value)
                func = functools.partial(temp_exec, data["command"])
            self.add_new_action(menu, data["name"], func)

    def add_new_action(self, menu: QtWidgets.QMenu, action_name: str, function) -> None:
        """
        メニューに新しいアクションを追加する関数
        Args:
            menu (QMenu): 追加したいメニュー
            action_name (str): アクションの名前
            function: アクションがクリックされた際に実行される関数
        """
        new_action = QtWidgets.QAction(action_name, self)
        new_action.triggered.connect(function)
        menu.addAction(new_action)

    def rebuild_menu(self, menubar, menu_name, datas):
        menu = menubar.addMenu(menu_name)
        # TODO:再構築
        self.add_actions(menu, datas)


class CheckerTableWidget(QtWidgets.QTableWidget):
    def __init__(self, help_url: str = None, parent=None):
        super(CheckerTableWidget, self).__init__(parent)
        background_color = "rgb(56, 56, 56)"
        style = f"QTableWidget {{ background-color: {background_color}; }}"
        self.setStyleSheet(style)

        self.set_header_size()

        self.help_url = None
        if help_url:
            self.help_url = help_url

        # tableをread onlyに設定
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.cellDoubleClicked.connect(self.on_cell_double_clicked)

    def on_cell_double_clicked(self, row, column):
        if column == 2:
            item = self.item(row, column)
            self.show_manual(item.text())

    def set_header_size(self):
        # project用に決め打ち
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(
            ["class", "", "チェック項目", "チェックの実行", "エラーステータス", "", "", ""]
        )

        # Set the column width ratio
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)  # class(非表示)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents
        )  # 選択チェックボックス
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)  # label
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)  # チェック実行
        header.setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeToContents
        )  # エラーステータス
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)  # 詳細
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)  # 修正
        # header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        self.setColumnHidden(0, True)

    def _get_pushed_button_row(self, sender):
        button = sender
        index = self.indexAt(button.pos())
        return index.row()

    def _get_current_task_name(self, row):
        item = self.item(row, 0)
        return item.text()

    # TODO: any
    def _get_checkbox_by_task_name(self, task_name: str) -> any:
        """タスク名空チェックボックスの取得

        Args:
            task_name (str): _description_
        """
        column = 0
        checkbox_column = 1
        checkbox_item = None
        for row in range(self.rowCount()):
            curren_task_name = self.item(row, column).text()
            if task_name == curren_task_name:
                checkbox_item = self.item(row, checkbox_column)

        return checkbox_item

    def get_checkstate_by_task_name(self, task_name: str) -> bool:
        """タスク名から現在の該当するチェックボックスのcheckedを取得

        Args:
            task_name (str): タスク名

        Returns:
            bool: _description_
        """
        checkbox_item = self._get_checkbox_by_task_name(task_name)
        if checkbox_item:
            state = checkbox_item.checkState()
            state_bool = state == QtCore.Qt.Checked
        return state_bool

    def set_checkstate_by_task_name(self, task_name: str, state: bool):
        """タスク名から現在の該当するチェックボックスのON/OFF

        Args:
            task_name (str): タスク名
            state (bool): チェックボックスのstate
        """
        checkbox_item = self._get_checkbox_by_task_name(task_name)
        if checkbox_item:
            check_state = QtCore.Qt.Checked if state else QtCore.Qt.Unchecked
            checkbox_item.setCheckState(check_state)

    def _set_cell_text_and_background(
        self,
        row: int,
        column: int,
        text: str,
        background_color: str,
        text_color: str = "White",
    ):
        """cellにテキストをセットし、背景色を指定

        Args:
            row (int): 行番号
            column (int): 列番号
            text (str): セットするテキスト
            background_color (str): 背景色
            text_color (str, optional): テキストの色. Defaults to "White".
        """
        item = QtWidgets.QTableWidgetItem(text)
        item.setBackground(QtGui.QBrush(QtGui.QColor(background_color)))
        item.setForeground(QtGui.QBrush(QtGui.QColor(text_color)))

        self.setItem(row, column, item)

    def _get_row_by_task_name(self, task_name: str) -> int:
        """タスク名からrowを取得

        Args:
            task_name (str): タスク名

        Returns:
            int: 行(row)
        """
        column = 0
        for row in range(self.rowCount()):
            curren_task_name = self.item(row, column).text()
            if task_name == curren_task_name:
                return row

    def update_error_status_by_task_name(self, task_name: str, error_status: ErrorType):
        """errorstatusのupdateをtask_nameから行えるように

        Args:
            task_name (str): タスク名
            error_status (ErrorType):エラーの
        """
        row = self._get_row_by_task_name(task_name)
        self._update_error_status(row, error_status)
        self.update_fixed_button_status(row, error_status)

    def _update_error_status(self, row: int, error_status: ErrorType):
        """指定したerror_statusに合わせて行番号のエラー表示の切り替え

        Args:
            row (int): _description_
            error_status (ErrorType): _description_

        """
        column = 4
        if error_status == ErrorType.NOERROR:
            background_color = "lightGreen"
            self._set_cell_text_and_background(
                row, column, "OK", background_color, "black"
            )

        elif error_status == ErrorType.WARNING:
            background_color = "yellow"
            self._set_cell_text_and_background(
                row, column, "WARNING", background_color, "black"
            )

        elif error_status == ErrorType.ERROR:
            background_color = "RED"
            self._set_cell_text_and_background(row, column, "Error", background_color)

        elif error_status == ErrorType.NOCHECKED:
            background_color = "gray"
            self._set_cell_text_and_background(
                row, column, "NO CHECK", background_color
            )

        elif error_status == ErrorType.PROGRAMERROR:
            background_color = "darkblue"
            self._set_cell_text_and_background(
                row, column, "Prog_Error", background_color
            )

        item = self.item(row, column)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item.text()

    def update_fixed_button_status(self, row: int, error_status: ErrorType):
        column = 6
        button = self.cellWidget(column, row)
        # if error_status == ErrorType.ERROR:
        #     button.setEnabled(False)
        # else:
        #     button.setEnabled(True)

    def show_manual(self, task_name: str):
        """コンフルのツールマニュアルページを開く"""
        try:
            if self.help_url:
                utils.search_website(self.help_url, task_name)
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")


def show(**kwargs):
    if CheckerMainWindow._instance:
        CheckerMainWindow._instance.close()
    CheckerMainWindow._instance = CheckerMainWindow(**kwargs)

    CheckerMainWindow._instance.show(
        dockable=True,
    )
