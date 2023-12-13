import os
import json
import maya.cmds as cmds
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
                               QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QListWidget,
                               QListWidgetItem, QMenu)
from PySide2.QtGui import QColor, QFont
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class AttributeTransferTool(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(AttributeTransferTool, self).__init__(parent)
        self.setWindowTitle("Attribute Transfer Tool")
        self.setMinimumWidth(550)
        self.setMinimumHeight(350)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.browse_button = QPushButton("Browse")
        self.folder_label = QLabel("Folder:")
        self.folder_path = QLineEdit()
        self.file_list = QListWidget()
        self.file_list.setFixedHeight(80)
        self.export_name_label = QLabel("Export File Name:")
        self.export_name = QLineEdit()
        self.export_button = QPushButton("Export")
        self.import_button = QPushButton("Import")
        self.compare_button = QPushButton("Compare")
        self.match_checkbox = QCheckBox("Show Match")
        self.match_checkbox.setChecked(True)
        self.mismatch_checkbox = QCheckBox("Show Mismatch")
        self.mismatch_checkbox.setChecked(True)
        self.not_found_checkbox = QCheckBox("Show Not Found")
        self.not_found_checkbox.setChecked(True)
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Object", "Attribute", "Current Value", "New Value", "Result"])
        self.results_table.setContextMenuPolicy(Qt.CustomContextMenu)  
        for i in range(5):
            self.results_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    def create_layouts(self):
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(self.browse_button)
        export_layout = QHBoxLayout()
        export_layout.addWidget(self.export_name_label)
        export_layout.addWidget(self.export_name)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.export_button)
        buttons_layout.addWidget(self.import_button)
        buttons_layout.addWidget(self.compare_button)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(export_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.match_checkbox)
        main_layout.addWidget(self.mismatch_checkbox)
        main_layout.addWidget(self.not_found_checkbox)
        main_layout.addWidget(self.results_table)

    def create_connections(self):
        self.browse_button.clicked.connect(self.browse_folder)
        self.folder_path.textChanged.connect(self.populate_file_list)
        self.export_button.clicked.connect(self.export_attributes)
        self.import_button.clicked.connect(self.import_attributes)
        self.compare_button.clicked.connect(self.compare_attributes)
        self.match_checkbox.stateChanged.connect(self.filter_results)
        self.mismatch_checkbox.stateChanged.connect(self.filter_results)
        self.not_found_checkbox.stateChanged.connect(self.filter_results)
        self.results_table.customContextMenuRequested.connect(self.select_object_in_scene)  

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path.setText(folder)

    def populate_file_list(self):
        self.file_list.clear()
        folder = self.folder_path.text()
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith(".json"):
                    item = QListWidgetItem(file)
                    self.file_list.addItem(item)

    def get_selected_file(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            return os.path.join(self.folder_path.text(), selected_items[0].text())
        return None

    def select_object_in_scene(self, pos):
        # クリックされたセルの行を取得
        row = self.results_table.rowAt(pos.y())
        # 行が有効な場合のみ、オブジェクトを選択
        if row != -1:
            object_name = self.results_table.item(row, 0).text()
            # オブジェクトがシーンに存在する場合、選択
            if cmds.objExists(object_name):
                # ポップアップメニューを作成
                menu = QMenu(self)
                select_object_action = menu.addAction("Select Object")
                action = menu.exec_(self.results_table.viewport().mapToGlobal(pos))
                # メニューアクションがクリックされた場合
                if action == select_object_action:
                    cmds.select(object_name, replace=True)
            else:
                cmds.warning(f"Object {object_name} not found in the scene.")

    def export_attributes(self):
        _selected_objects_ = cmds.ls(selection=True, long=True)
        if not _selected_objects_:
            cmds.warning("No objects selected.")
            return
        _attributes_dict_ = {}
        for _obj_ in _selected_objects_:
            _short_obj_name_ = cmds.ls(_obj_, shortNames=True)[0]  # Get the short name of the object
            _attributes_ = cmds.listAttr(_obj_, keyable=True, unlocked=True)
            if _attributes_:
                _attributes_dict_[_short_obj_name_] = {}  # Use the short name for the key in _attributes_dict_
                for _attr_ in _attributes_:
                    _attributes_dict_[_short_obj_name_][_attr_] = cmds.getAttr(_obj_ + "." + _attr_)
        if not _attributes_dict_:
            cmds.warning("No keyable and unlocked attributes found.")
            return
        _export_file_name_ = self.export_name.text()
        if not _export_file_name_:
            cmds.warning("Please provide a file name for the export.")
            return
        _export_file_path_ = os.path.join(self.folder_path.text(), _export_file_name_ + ".json")
        # Check if a file with the same name exists
        if os.path.exists(_export_file_path_):
            # Show a dialog to confirm overwriting
            _msg_box_ = QMessageBox()
            _msg_box_.setText("A file with the same name already exists. Do you want to overwrite it?")
            _msg_box_.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            _result_ = _msg_box_.exec_()
            # If overwriting is rejected, stop the process
            if _result_ == QMessageBox.No:
                return
        with open(_export_file_path_, "w") as _export_file_:
            json.dump(_attributes_dict_, _export_file_, indent=4)
        self.populate_file_list()

    def import_attributes(self):
        _selected_file_ = self.get_selected_file()
        if not _selected_file_:
            cmds.warning("Please select a JSON file to import.")
            return
        # Show a dialog to confirm importing
        _msg_box_ = QMessageBox()
        _msg_box_.setText("Are you sure you want to import the attributes?")
        _msg_box_.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        _result_ = _msg_box_.exec_()
        # If importing is rejected, stop the process
        if _result_ == QMessageBox.No:
            return
        with open(_selected_file_, "r") as _import_file_:
            _attributes_dict_ = json.load(_import_file_)

        # Start undo group
        cmds.undoInfo(openChunk=True)
        try:
            for _obj_, _attributes_ in _attributes_dict_.items():
                for _attr_, _value_ in _attributes_.items():
                    if cmds.objExists(_obj_) and cmds.attributeQuery(_attr_, node=_obj_, exists=True):
                        # Check if the attribute is locked or connected
                        _is_locked_ = cmds.getAttr(_obj_ + "." + _attr_, lock=True)
                        _is_connected_ = cmds.listConnections(_obj_ + "." + _attr_, destination=False, source=True)
                        if not _is_locked_ and not _is_connected_:
                            cmds.setAttr(_obj_ + "." + _attr_, _value_)
                        else:
                            cmds.warning(f"Attribute {_obj_}.{_attr_} is locked or connected and cannot be modified.")
                    else:
                        cmds.warning(f"Object {_obj_} or attribute {_attr_} not found in the scene.")
        except Exception as e:
            cmds.warning(f"Error importing attributes: {e}")
        finally:
            # End undo group
            cmds.undoInfo(closeChunk=True)

        # Update the table after import
        self.compare_attributes()
        # Check all checkboxes after importing
        self.check_all_checkboxes()

    def compare_attributes(self):
        selected_file = self.get_selected_file()
        if not selected_file:
            cmds.warning("Please select a JSON file to compare.")
            return
        # Get the JSON file name without the extension
        json_file_name = os.path.splitext(os.path.basename(selected_file))[0]
        with open(selected_file, "r") as compare_file:
            attributes_dict = json.load(compare_file)
        self.results_table.setRowCount(0)
        # Update the header labels to display the JSON file name
        self.results_table.setHorizontalHeaderLabels(["Object", "Attribute", "Current Value", f"{json_file_name} Value", "Result"])
        for obj, attributes in attributes_dict.items():
            for attr, value in attributes.items():
                if cmds.objExists(obj) and cmds.attributeQuery(attr, node=obj, exists=True):
                    current_value = cmds.getAttr(obj + "." + attr)
                    # Round the values to 3 decimal places
                    current_value_rounded = round(current_value, 3)
                    value_rounded = round(value, 3)
                    row = self.results_table.rowCount()
                    self.results_table.insertRow(row)
                    self.results_table.setItem(row, 0, QTableWidgetItem(obj))
                    self.results_table.setItem(row, 1, QTableWidgetItem(attr))
                    self.results_table.setItem(row, 2, QTableWidgetItem(str(current_value_rounded)))
                    self.results_table.setItem(row, 3, QTableWidgetItem(str(value_rounded)))
                    result_item = QTableWidgetItem()
                    if current_value_rounded == value_rounded:
                        result_item.setText("Match")
                        result_item.setForeground(QColor(Qt.green))
                    else:
                        result_item.setText("Mismatch")
                        result_item.setForeground(QColor(Qt.red))
                    self.results_table.setItem(row, 4, result_item)
                else:
                    row = self.results_table.rowCount()
                    self.results_table.insertRow(row)
                    self.results_table.setItem(row, 0, QTableWidgetItem(obj))
                    self.results_table.setItem(row, 1, QTableWidgetItem(attr))
                    self.results_table.setItem(row, 2, QTableWidgetItem("Not Found"))
                    result_item = QTableWidgetItem()
                    result_item.setText("Not Found")
                    result_item.setForeground(QColor(Qt.darkGray))
                    self.results_table.setItem(row, 4, result_item)
        self.filter_results()
        # Check all checkboxes after comparing
        self.check_all_checkboxes()

    def filter_results(self):
        for _row_ in range(self.results_table.rowCount()):
            _result_item_ = self.results_table.item(_row_, 4)
            if _result_item_:
                _result_text_ = _result_item_.text()
                if _result_text_ == "Match":
                    self.results_table.setRowHidden(_row_, not self.match_checkbox.isChecked())
                elif _result_text_ == "Mismatch":
                    self.results_table.setRowHidden(_row_, not self.mismatch_checkbox.isChecked())
                elif _result_text_ == "Not Found":
                    self.results_table.setRowHidden(_row_, not self.not_found_checkbox.isChecked())

    def check_all_checkboxes(self):
        self.match_checkbox.setChecked(True)
        self.mismatch_checkbox.setChecked(True)
        self.not_found_checkbox.setChecked(True)


def main():
    global attr_transfer_tool
    try:
        attr_transfer_tool.close()
        attr_transfer_tool.deleteLater()
    except:
        pass
    attr_transfer_tool = AttributeTransferTool()
    attr_transfer_tool.show()
