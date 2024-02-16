# -'''- coding: utf-8 -'''-
import os

from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

import maya.cmds as cmds


filePath = os.path.dirname(__file__).replace("\\", "/")
DETAIL_UIFILEPATH = filePath + "/ui/details.ui"
TOOL_TITLE = "detail_window" + "WorkspaceControl"


class DetailMainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QDialog):
    def __init__(self, task_name, debug_data, parent=None):
        super(DetailMainWindow, self).__init__(parent)
        self.debug_data = debug_data
        # UIのパスを指定
        self.UI = QUiLoader().load(DETAIL_UIFILEPATH)

        self.edit = QtWidgets.QLabel(task_name)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.UI)
        self.setLayout(layout)
        self.set_header_size()
        self._set_debug_data()
        self.UI.detail_table.cellClicked.connect(self.on_cell_clicked)

        # tableをreadonlyに設定
        self.UI.detail_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def on_cell_clicked(self, row, column):
        cmds.select(clear=True)
        selected_items = self.UI.detail_table.selectedItems()
        for item in selected_items:
            node_name = item.text()
            if cmds.objExists(node_name):
                cmds.select(node_name, add=True)

    # セルがクリックされたときに on_cell_clicked 関数を呼び出す

    def set_header_size(self):
        self.UI.detail_table.setColumnCount(3)
        self.UI.detail_table.setHorizontalHeaderLabels(
            ["エラーの種類", "エラーメッセージ", "対象オブジェクト"]
        )

        # Set the column width ratio
        header = self.UI.detail_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # class
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # label
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(False)
        self.UI.detail_table.setColumnHidden(0, True)

    def _set_debug_data(self):
        # error_target_info
        table = self.UI.detail_table
        for task_type in self.debug_data.error_target_info:
            row = table.rowCount()
            table.insertRow(row)
            error_message = self.debug_data.error_target_info[task_type][
                "error_messages"
            ]
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(task_type))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(error_message))
            for target in self.debug_data.error_target_info[task_type][
                "target_objects"
            ]:
                if target:
                    table.setItem(row, 2, QtWidgets.QTableWidgetItem(target))
                    row = table.rowCount()
                    table.insertRow(row)


if __name__ == "__main__":
    form = DetailMainWindow()
    form.show()
