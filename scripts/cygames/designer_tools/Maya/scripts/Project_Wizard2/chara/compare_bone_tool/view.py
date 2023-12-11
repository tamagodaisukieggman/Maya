# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from .data import CheckState


# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
MAIN_UIFILEPATH = filePath + "/ui/compare_bone_tool_main.ui"
TOOL_TITLE = "CompareBoneTool"
VERSION = "1.0.0"


class View(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    on_clicked_detail_button = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setObjectName(TOOL_TITLE)
        self.setWindowTitle(TOOL_TITLE + ":" + VERSION)

        # UIのパスを指定
        self.gui = QUiLoader().load(MAIN_UIFILEPATH)

        # ウィジェットをセンターに配置s
        self.setCentralWidget(self.gui)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.initialize_table_settings()
        self.set_table_header()

    def initialize_table_settings(self):
        table = self.gui.compare_table
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def reset_item_table(self):
        table = self.gui.compare_table
        table.setRowCount(0)

    def add_item_table(self, item_data: dict):
        """itemをテーブルに追加
        itemの情報を辞書で受け取る

        Args:
            item_data (dict): _description_
        """
        self.gui.compare_table.setStyleSheet(
            "QListWidget::item { margin: 0px; padding: 0px; }"
        )
        table = self.gui.compare_table
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(
            row_position, 0, QtWidgets.QTableWidgetItem(item_data["source_joint_name"])
        )

        table.setItem(
            row_position, 1, QtWidgets.QTableWidgetItem(item_data["target_joint_name"])
        )
        table.setItem(
            row_position,
            4,
            QtWidgets.QTableWidgetItem(item_data["simple_error_message"]),
        )

        if item_data["target_joint_name"] == "<Nothing>":
            item = table.item(row_position, 1)
            item.setForeground(QtGui.QBrush(QtGui.QColor("gray")))

        check_state = item_data["check_data"].check_state

        button = QtWidgets.QPushButton("詳細")
        table.setCellWidget(row_position, 3, button)

        button.clicked.connect(self.make_clicked_index_slot(row_position))

        if check_state != CheckState.HAS_ERROR:
            button.setEnabled(False)

        self._update_error_status(row_position, check_state)

    def set_table_header(self):
        """tableのヘッダーを初期化"""
        table = self.gui.compare_table
        table.setColumnCount(5)
        header = table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents
        )  # class(非表示)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents
        )  # 選択チェックボックス
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def reset_window_size(self):
        table = self.gui.compare_table
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header_length = sum([header.sectionSize(i) for i in range(header.count())])
        # self.setCentralWidget(table)
        vheader = table.verticalHeader()
        header_length += vheader.width()
        self.resize(header_length, self.height())

    def _update_error_status(self, row: int, check_status: CheckState):
        """指定したerror_statusに合わせて行番号のエラー表示の切り替え

        Args:
            row (int): _description_
            check_status (ErrorType): _description_

        """
        column = 2
        if check_status == CheckState.NO_ERROR:
            background_color = "lightGreen"
            self._set_cell_text_and_background(
                row, column, "OK", background_color, "black"
            )

        elif check_status == CheckState.HAS_ERROR:
            background_color = "RED"
            self._set_cell_text_and_background(row, column, "Error", background_color)

        elif check_status == CheckState.NO_CHECKED:
            background_color = "gray"
            self._set_cell_text_and_background(
                row, column, "NO CHECK", background_color
            )

        elif check_status == CheckState.EXIST_ERROR:
            background_color = "orange"
            self._set_cell_text_and_background(
                row, column, "Not Exist", background_color
            )

        item = self.gui.compare_table.item(row, column)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item.text()

    def change_all_error_status_color(self, background_color: str, text_color: str):
        """総チェック結果の色変更用関数

        Args:
            background_color (str): 指定される背景色
            text_color (str): 指定されるテキスト色
        """
        status_label = self.gui.all_error_status_txt
        self.change_background_color(status_label, background_color)
        self.change_text_color(status_label, text_color)

    @staticmethod
    def change_background_color(label, color):
        """
        この関数は指定されたラベルの背景色を変更します。
        引数:
        label (QLabel): 背景色を変更するラベル
        color (str): 背景を設定する色（例："red"、"blue"など）
        """
        # ラベルの背景色を書き換え可能に設定
        label.setAutoFillBackground(True)

        # パレットを取得して、その背景色を変更する
        palette = label.palette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(color))

        # パレットをラベルに適用する
        label.setPalette(palette)

    @staticmethod
    def change_text_color(label, color):
        """
        この関数は指定されたラベルのテキストの色を変更します。
        引数:
        label (QLabel): テキストの色を変更するラベル
        color (str): 色を設定するテキスト（例："red"、"blue"など）
        """
        # パレットを取得して、そのテキストの色を変更する
        palette = label.palette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(color))

        # パレットをラベルに適用する
        label.setPalette(palette)

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

        self.gui.compare_table.setItem(row, column, item)

    def make_clicked_index_slot(self, i):
        @QtCore.Slot()
        def slot():
            self.on_clicked_detail_button.emit(i)

        return slot
