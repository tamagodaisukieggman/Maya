# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import webbrowser

from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# shibokenの読み込み
try:
    import shiboken2 as shiboken
except:
    import shiboken

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

from .app import TextureSelector, MaterialGetter

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
MAIN_UIFILEPATH = filePath + "/ui/main.ui"
SELECTOR_UIFILEPATH = filePath + "/ui/selector.ui"
TOOL_TITLE = "TextureSelector"


class TextureSelectorMainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(TextureSelectorMainWindow, self).__init__(parent)
        self.setObjectName(TOOL_TITLE)

        self.delete_instances()
        # UIのパスを指定
        self.UI = QUiLoader().load(MAIN_UIFILEPATH)

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.research_materials()

        self.UI.re_search_btn.clicked.connect(self.clicked_research_btn)
        self.UI.action_manual.triggered.connect(self.show_manual)

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            cmds.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    def _set_current_object(self):
        selected = cmds.ls(sl=True, type="transform")
        if len(selected) == 0:
            cmds.warning("オブジェクトが選択されていません")
            return
        self.current_object = cmds.ls(sl=True, type="transform")[0]
        self.UI.target_obj_txt.setText(self.current_object)

    def research_materials(self):
        self._set_current_object()

        materials = []
        materials = MaterialGetter.get_object_assigned_materials()

        # もしマテリアルが０個だったらreturn
        if len(materials) == 0:
            cmds.warning("No assigned materials. It suspends processing.")
            return
        self.selectors = []

        self.UI.selector_list.clear()
        for material in materials:
            selector = self.create_selector(material)
            self.selectors.append(selector)
            selector_widget = self._create_selector_widget(selector)

            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(selector_widget.sizeHint())

            self.UI.selector_list.setStyleSheet(
                "QListWidget::item { margin: 0px; padding: 0px; }"
            )
            self.UI.selector_list.setSpacing(0)

            self.UI.selector_list.addItem(item)
            self.UI.selector_list.setItemWidget(item, selector_widget)

    def _create_selector_widget(self, selector):
        selector_widget = SelectorWidget(selector)
        return selector_widget

    def create_selector(self, material):
        selector = TextureSelector(material)
        return selector

    def clicked_research_btn(self):
        self.research_materials()

    def show_manual(self):
        """コンフルのツールマニュアルページを開く"""
        try:
            webbrowser.open(
                "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=660614235"
            )
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")


class SelectorWidget(QtWidgets.QWidget):
    def __init__(self, selector, parent=None):
        super(SelectorWidget, self).__init__(parent)
        self.selector = selector

        self.UI = QUiLoader().load(SELECTOR_UIFILEPATH)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.UI)
        self.setLayout(layout)
        self.UI.target_material.setText(selector.material)

        self.UI.before_btn.clicked.connect(self.clicked_before_btn)
        self.UI.next_btn.clicked.connect(self.clicked_next_btn)
        self.UI.texture_index_cmbbox.currentIndexChanged.connect(
            self.change_texture_index_cmbbox
        )
        self.initialize()

    def initialize(self):
        for key in self.selector.texture_paths.keys():
            self.UI.texture_index_cmbbox.addItem(str(key))

    def increment_index(self, is_plus: bool):
        value = -1
        if is_plus:
            value = 1
        current_index = self.UI.texture_index_cmbbox.currentIndex()
        max = self.UI.texture_index_cmbbox.count() - 1
        new_index = current_index + value
        if new_index > max or 0 > new_index:
            return
        else:
            self.UI.texture_index_cmbbox.setCurrentIndex(new_index)

    def clicked_before_btn(self):
        self.increment_index(False)

    def clicked_next_btn(self):
        self.increment_index(True)

    def change_texture_index_cmbbox(self):
        index = self.UI.texture_index_cmbbox.currentText()
        if index != "":
            self.selector.change_base_color_texture_by_index(index)


def show(**kwargs):
    if TextureSelectorMainWindow._instance is None:
        TextureSelectorMainWindow._instance = TextureSelectorMainWindow()

    TextureSelectorMainWindow._instance.show(
        dockable=True,
    )

    TextureSelectorMainWindow._instance.setWindowTitle(TOOL_TITLE)
