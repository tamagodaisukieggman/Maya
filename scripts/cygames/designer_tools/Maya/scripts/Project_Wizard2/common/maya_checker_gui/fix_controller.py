# -'''- coding: utf-8 -'''-
import os

from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

import maya.cmds as cmds


filePath = os.path.dirname(__file__).replace("\\", "/")
FIX_UIFILEPATH = filePath + "/ui/fix.ui"
TOOL_TITLE = "fix_window" + "WorkspaceControl"


class FixMainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QDialog):
    def __init__(self, task_name, before_debug_data, after_debug_data, parent=None):
        super(FixMainWindow, self).__init__(parent)
        self.before_debug_data = before_debug_data
        self.after_debug_data = after_debug_data
        # UIのパスを指定
        self.UI = QUiLoader().load(FIX_UIFILEPATH)

        self.edit = QtWidgets.QLabel(task_name)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.UI)
        self.setLayout(layout)
        self.set_header_size()
        self._set_debug_data()
        self.UI.before_fix_table.cellClicked.connect(self.on_cell_clicked)

        # tableをreadonlyに設定
        self.UI.before_fix_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

    def on_cell_clicked(self, row, column):
        cmds.select(clear=True)
        selected_items = self.UI.before_fix_table.selectedItems()
        for item in selected_items:
            node_name = item.text()
            if cmds.objExists(node_name):
                cmds.select(node_name, add=True)

    # セルがクリックされたときに on_cell_clicked 関数を呼び出す

    def set_header_size(self):
        self.UI.before_fix_table.setColumnCount(3)
        self.UI.before_fix_table.setHorizontalHeaderLabels(
            ["エラーの種類", "エラーメッセージ", "修正前エラーオブジェクト"]
        )

        # Set the column width ratio
        header = self.UI.before_fix_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # class
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # label
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(True)
        self.UI.before_fix_table.setColumnHidden(0, True)

        self.UI.after_fix_table.setColumnCount(3)
        self.UI.after_fix_table.setHorizontalHeaderLabels(
            ["エラーの種類", "エラーメッセージ", "修正後エラーオブジェクト"]
        )

        # Set the column width ratio
        header = self.UI.after_fix_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # class
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # label
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(True)
        self.UI.after_fix_table.setColumnHidden(0, True)

    def _set_debug_data(self):
        # error_target_info
        tables = [self.UI.before_fix_table, self.UI.after_fix_table]
        debug_datas = [self.before_debug_data, self.after_debug_data]

        for table, debug_data in zip(tables, debug_datas):
            for task_type in debug_data.error_target_info:
                row = table.rowCount()
                table.insertRow(row)
                error_message = debug_data.error_target_info[task_type][
                    "error_messages"
                ]
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(task_type))
                table.setItem(row, 1, QtWidgets.QTableWidgetItem(error_message))
                for target in debug_data.error_target_info[task_type]["target_objects"]:
                    if target:
                        table.setItem(row, 2, QtWidgets.QTableWidgetItem(target))
                        row = table.rowCount()
                        table.insertRow(row)


if __name__ == "__main__":
    form = FixMainWindow()
    form.show()
