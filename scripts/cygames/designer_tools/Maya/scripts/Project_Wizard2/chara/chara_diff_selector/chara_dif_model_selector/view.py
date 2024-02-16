# -*- coding: utf-8 -*-
from __future__ import print_function

import os

import typing as tp

import functools
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
#from maya.app.general.mayaMixin import MayaQWidgetDockableMixin



# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
MAIN_UIFILEPATH = filePath + "/ui/main.ui"
SELECTOR_UIFILEPATH = filePath + "/ui/selector.ui"
TOOL_TITLE = "DifModelSelector"

class ModelSelectorMainWindow(QtWidgets.QWidget):
    on_change_index_combobox = QtCore.Signal(int)
    def __init__(self, parent=None):
        super(ModelSelectorMainWindow, self).__init__(parent)
        self.setObjectName(TOOL_TITLE)

        # UIのパスを指定
        self.gui = QUiLoader().load(MAIN_UIFILEPATH)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.gui)
        self.setLayout(layout)
        # ウィジェットをセンターに配置
        #self.setCentralWidget(self.gui)

        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    
    def initialize_list(self,diff_datas:dict):
        if diff_datas != None:
            self.diff_datas = diff_datas
        self.gui.selector_list.clear()
        self.selectors = []
        for i,target_object in enumerate(self.diff_datas):
            selector = SelectorWidget(target_object = target_object,
                                    dif_ids=self.diff_datas[target_object])
            
            self.selectors.append(selector)

            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(selector.sizeHint())

            self.gui.selector_list.setStyleSheet(
                "QListWidget::item { margin: 0px; padding: 0px; }"
            )
            self.gui.selector_list.setSpacing(0)

            self.gui.selector_list.addItem(item)
            self.gui.selector_list.setItemWidget(item, selector)

            # emitter = functools.partial(self.emit_signal,i) 
            
            #emitter = lambda :self.emit_signal(i)
            selector.gui.dif_object_index_cmbbox.currentIndexChanged.connect(self.make_cmbbox_change_slot(i))

    def set_root_name(self,root_node_name:str):
        self.gui.target_obj_txt.setText(root_node_name)

    def make_cmbbox_change_slot(self, i):
        @QtCore.Slot()
        def slot():
            self.on_change_index_combobox.emit(i) 
        return slot

class SelectorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None,target_object:str = "",dif_ids:tp.List[str] = []):
        super(SelectorWidget, self).__init__(parent)

        self.gui = QUiLoader().load(SELECTOR_UIFILEPATH)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.gui)
        self.setLayout(layout)
        self.set_title(target_object)
        self.gui.before_btn.clicked.connect(self.clicked_before_btn)
        self.gui.next_btn.clicked.connect(self.clicked_next_btn)
        self.initialize(dif_ids)

    def initialize(self,dif_ids:tp.List[str]):
        for dif_id in dif_ids:
            self.gui.dif_object_index_cmbbox.addItem(dif_id)

    def set_title(self,target_object:str):
        self.gui.target_object_txt.setText(target_object)


    def increment_index(self, is_plus: bool):
        value = -1
        if is_plus:
            value = 1
        current_index = self.gui.dif_object_index_cmbbox.currentIndex()
        max = self.gui.dif_object_index_cmbbox.count() - 1
        new_index = current_index + value
        if new_index > max or 0 > new_index:
            return
        else:
            self.gui.dif_object_index_cmbbox.setCurrentIndex(new_index)

    def clicked_before_btn(self):
        self.increment_index(False)

    def clicked_next_btn(self):
        self.increment_index(True)

    def get_current_diff_index(self):
        index = self.gui.dif_object_index_cmbbox.currentText()
        return index
    
    def get_current_parts_id(self):
        return self.gui.target_object_txt.text()
    
    def change_dif_object_index_cmbbox(self):
        index = self.gui.dif_object_index_cmbbox.currentText()

