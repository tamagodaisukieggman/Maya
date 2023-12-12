# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# shibokenの読み込み
try:
    import shiboken2 as shiboken
except:
    import shiboken

import pymel.core as pm
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import shr.animation.create_eST_constrain.command as cecc

UIFILEPATH = os.path.dirname(__file__).replace("\\", "/") + "/ui/gui.ui"
TITLE = "create_eST_constraint"
METHOD_TYPE = ["orient", "point", "parent"]

# 順番をmayaの標準と同じにしてあるので入れ替えない
ROT_ORDER = ["xyz", "yzx", "zxy", "xzy", "yxz", "zyx"]


class RFTool(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(RFTool, self).__init__(parent)
        self.setObjectName(TITLE)
        self.delete_instances()
        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)
        self.UI.create_locator_btn.clicked.connect(self.exec_create_locator_btn)
        self.UI.delete_locator_btn.clicked.connect(self.exec_delete_locator_btn)
        self.UI.get_rotation_order_btn.clicked.connect(self.exec_get_rotation_order_btn)
        self.initialize_ui()

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    def initialize_ui(self) -> None:
        """UIの初期設定(コンボボックスなど)"""
        self.UI.method_type_cmbbox.addItems(METHOD_TYPE)
        self.UI.rotation_order_cmbbox.addItems(ROT_ORDER)

    def exec_create_locator_btn(self):
        current_rot_order = self.UI.rotation_order_cmbbox.currentIndex()
        method = METHOD_TYPE[self.UI.method_type_cmbbox.currentIndex()]
        maintain_offset = self.UI.rotation_offset_cbox.isChecked()
        cecc.generate_eST_constraint(maintain_offset, current_rot_order, method)

    def exec_delete_locator_btn(self):
        cecc.delete_locator()
        ...

    def exec_get_rotation_order_btn(self):
        index = cecc.get_rotation_order()
        self.UI.rotation_order_cmbbox.setCurrentIndex(index)


def show(**kwargs):
    if RFTool._instance is None:
        RFTool._instance = RFTool()

    RFTool._instance.show(
        dockable=True,
    )

    RFTool._instance.setWindowTitle(TITLE)
