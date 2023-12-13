# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from .data import BoneCheckedData


# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
MAIN_UIFILEPATH = filePath + "/ui/compare_bone_tool_detail.ui"
TOOL_TITLE = "CompareBoneDetails"


class DetailView(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, check_data: BoneCheckedData, parent=None):
        super(DetailView, self).__init__(parent)
        self.setObjectName(TOOL_TITLE)
        self.setWindowTitle(TOOL_TITLE)

        # UIのパスを指定
        self.gui = QUiLoader().load(MAIN_UIFILEPATH)

        # ウィジェットをセンターに配置s
        self.setCentralWidget(self.gui)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.reset_detail_data(check_data)
        self.set_table_header()

    def reset_detail_data(self, check_data: BoneCheckedData):
        for attribute in check_data.result:
            if check_data.result[attribute]["has_error"]:
                self.add_item_table(attribute, check_data.result[attribute])

    def add_item_table(self, attribute_name: str, check_attribute_data: dict):
        """itemをテーブルに追加
        itemの情報を辞書で受け取る

        Args:
            item_data (dict): _description_
        """
        self.gui.detail_table.setStyleSheet(
            "QListWidget::item { margin: 0px; padding: 0px; }"
        )
        table = self.gui.detail_table
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(
            row_position,
            0,
            QtWidgets.QTableWidgetItem(attribute_name),
        )
        table.setItem(
            row_position,
            1,
            QtWidgets.QTableWidgetItem(str(check_attribute_data["source_value"])),
        )
        table.setItem(
            row_position,
            2,
            QtWidgets.QTableWidgetItem(str(check_attribute_data["target_value"])),
        )

    def set_table_header(self):
        """tableのヘッダーを初期化"""
        table = self.gui.detail_table
        table.setColumnCount(3)
        
        self._fit_and_set_interactive(table)

    def _fit_and_set_interactive(self,table_widget:QtWidgets.QTableWidget):
        """列の幅をコンテンツに併せ、インタラクティブに設定

        Args:
            table_widget (QtWidgets.QHeaderView): 対象のtable
        """
        # 最初に ResizeToContents を適用
        table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # 列の幅を一時的に保存
        widths = []
        for i in range(table_widget.columnCount()):
            widths.append(table_widget.columnWidth(i))

        # Interactive モードに変更
        table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        # 保存しておいた幅を設定
        for i in range(table_widget.columnCount()):
            table_widget.setColumnWidth(i, widths[i])

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
