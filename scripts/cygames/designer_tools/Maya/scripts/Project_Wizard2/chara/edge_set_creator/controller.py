# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.cmds as cmds

from .app import EdgeSetTools
from .app import EdgeSetModifier
from .data import EdgeSetType
from .view import View

g_tool_name = "Edge_Set_Editor"
UI_PATH = os.path.dirname(__file__) + "/ui"


class EdgeSetController():
    def __init__(self):
        self.ui = View()  # QMainWindow

        self.edge_set_manager = EdgeSetTools(EdgeSetType.NECK)
        self.edge_set_modifire = EdgeSetModifier(EdgeSetType.NECK)
        self._init_edge_set_type()

        self.edge_set_type = EdgeSetType.NECK
        self.setup_ui()

    def setup_ui(self):
        self.ui.gui.set_default_pos_and_normal_btn.clicked.connect(
            self.exec_set_default_pos_and_normal_btn
        )
        self.ui.gui.create_edge_set_btn.clicked.connect(self.exec_create_edge_set_btn)
        self.ui.gui.edge_set_remove_btn.clicked.connect(self.exec_edge_set_remove_btn)
        self.ui.gui.delete_edge_set_btn.clicked.connect(self.exec_delete_edge_set_btn)
        self.ui.gui.selects_sets_member_btn.clicked.connect(
            self.exec_selects_sets_member_btn
        )
        self.ui.gui.edge_set_type_cmbbox.currentIndexChanged.connect(
            self.change_edge_set_type_cmbbox
        )

    def _init_edge_set_type(self):
        edge_types = [edge_type.name for edge_type in EdgeSetType]
        for edge_set_type in edge_types:
            self.ui.gui.edge_set_type_cmbbox.addItem(str(edge_set_type))

    def exec_set_default_pos_and_normal_btn(self):
        self.edge_set_modifire.set_default_value_to_edge()

    def exec_create_edge_set_btn(self):
        self.edge_set_manager.create_edge_set()

    def exec_edge_set_remove_btn(self):
        self.edge_set_manager.remove_edge_set()

    def exec_delete_edge_set_btn(self):
        self.edge_set_manager.delete_edge_set()

    def exec_selects_sets_member_btn(self):
        self.edge_set_manager.select_sets_member()

    def change_edge_set_type_cmbbox(self):
        current_edge_set_type_str = self.ui.gui.edge_set_type_cmbbox.currentText()
        for edge_type in EdgeSetType:
            if edge_type.name == current_edge_set_type_str:
                self.edge_set_manager = EdgeSetTools(edge_type)
                self.edge_set_modifire = EdgeSetModifier(edge_type)


    def show_ui(self):
        self.ui.show()

    def close_ui(self):
        self.ui.close()