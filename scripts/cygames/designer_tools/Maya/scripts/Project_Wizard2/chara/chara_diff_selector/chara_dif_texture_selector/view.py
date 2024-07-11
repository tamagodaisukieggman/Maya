# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function

import os
import webbrowser
import typing as tp

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
#from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.cmds as cmds


from .app import *

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
MAIN_UIFILEPATH = filePath + "/ui/main.ui"
SELECTOR_UIFILEPATH = filePath + "/ui/selector.ui"
TOOL_TITLE = "TextureSelector"


class TextureSelectorMainWindow(QtWidgets.QWidget):
    texture_index_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(TextureSelectorMainWindow, self).__init__(parent)
        self.setObjectName(TOOL_TITLE)
        # UIのパスを指定
        self.gui = QUiLoader().load(MAIN_UIFILEPATH)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.gui)
        self.setLayout(layout)

    def _set_current_object(self):
        selected = cmds.ls(sl=True, type="transform")
        if len(selected) == 0:
            cmds.warning("オブジェクトが選択されていません")
            return
        self.current_object = cmds.ls(sl=True, type="transform")[0]
        self.gui.target_obj_txt.setText(self.current_object)

    def _create_selector_widget(self, material_name, indexes):
        selector_widget = SelectorWidget(material_name, indexes)
        return selector_widget

    def show_manual(self):
        """コンフルのツールマニュアルページを開く"""
        try:
            webbrowser.open(
                "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=660614235"
            )
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")

    def add_item_selector_list(self, material, indexes):
        selector_widget = self._create_selector_widget(material, indexes)

        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(selector_widget.sizeHint())

        self.gui.selector_list.setStyleSheet(
            "QListWidget::item { margin: 0px; padding: 0px; }"
        )
        self.gui.selector_list.setSpacing(0)

        self.gui.selector_list.addItem(item)
        self.gui.selector_list.setItemWidget(item, selector_widget)

        return selector_widget

    def get_list_widget_items(self) -> tp.List[any]:
        """listの中のwidgetを取得

        Returns:
            tp.List[SelectorWidget]: _description_
        """
        widget_list = []
        for i in range(self.gui.selector_list.count()):
            item = self.gui.selector_list.item(i)
            widget = self.gui.selector_list.itemWidget(item)
            if widget:
                widget_list.append(widget)
        return widget_list

    def get_selector_widget_from_material_name(
        self, material_name: str
    ) -> QtWidgets.QWidget:
        for selector in self.get_list_widget_items():
            current_material_name = selector.gui.target_obj_txt.text()
            if material_name == current_material_name:
                return selector

    def clear_material_list(self):
        self.gui.selector_list.clear()


class SelectorWidget(QtWidgets.QWidget):
    # combboxの値に変更が入った際に発信
    combo_index_changed = QtCore.Signal(str)

    def __init__(self, material_name: str, indexes_dict: dict, parent=None):
        super(SelectorWidget, self).__init__(parent)

        self.gui = QUiLoader().load(SELECTOR_UIFILEPATH)
        self.current_indexes_cmbboxes = {}
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.gui)
        self.setLayout(layout)
        self.gui.target_obj_txt.setText(material_name)
        self.initialize(indexes_dict)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        for key in self.current_indexes_cmbboxes:
            self.current_indexes_cmbboxes[key].combo_box.currentIndexChanged.connect(
                self.on_combo_changed
            )

    def on_combo_changed(self):
        self.combo_index_changed.emit(self.gui.target_obj_txt.text())

    def initialize(self, indexes_dict):
        for key in indexes_dict:
            current_indexes = indexes_dict[key]
            index_selector = IndexSelectorWidget(current_indexes)
            self.gui.selector_lay.addWidget(index_selector)
            self.current_indexes_cmbboxes[key] = index_selector

    def get_current_indexes(self) -> dict:
        """現在のindex情報をdictで返す

        Returns:
            dict: {"model_diff_indexes":"01"}
        """
        rtn_index = {}
        for index_type in self.current_indexes_cmbboxes:
            index_selector = self.current_indexes_cmbboxes[index_type]
            current_index = index_selector.get_current_index()
            rtn_index[index_type] = current_index
        return rtn_index
    
    def set_indexes(self,diff_datas:dict):
        for index_type in self.current_indexes_cmbboxes:
            for current_index_type in diff_datas:
                if index_type in current_index_type:
                    self.current_indexes_cmbboxes[index_type].change_index_by_str(diff_datas[index_type])
                    break

class IndexSelectorWidget(QtWidgets.QWidget):
    def __init__(self, indexes: tp.List[str], parent=None):
        super(IndexSelectorWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        # コンボボックスの作成
        self.combo_box = QtWidgets.QComboBox()
        for index in indexes:
            self.combo_box.addItem(index)
        layout.addWidget(self.combo_box)

        # 2つのボタンの作成
        button1 = QtWidgets.QPushButton("<<前")
        button2 = QtWidgets.QPushButton("次>>")
        layout.addWidget(button1)
        layout.addWidget(button2)

        button1.clicked.connect(self.clicked_before_btn)
        button2.clicked.connect(self.clicked_next_btn)

    def clicked_before_btn(self):
        self.increment_index(False)

    def clicked_next_btn(self):
        self.increment_index(True)

    def increment_index(self, is_plus: bool):
        value = -1
        if is_plus:
            value = 1
        current_index = self.combo_box.currentIndex()
        max = self.combo_box.count() - 1
        new_index = current_index + value
        if new_index > max or 0 > new_index:
            return
        else:
            self.combo_box.setCurrentIndex(new_index)

    def get_current_index(self):
        return self.combo_box.currentText()
    
    def change_index_by_str(self,string):
        index = self.combo_box.findText(string)
        if index >= 0:
            self.combo_box.setCurrentIndex(index)

