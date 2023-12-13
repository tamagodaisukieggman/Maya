# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from PySide2 import QtWidgets, QtGui, QtCore
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

import shr.animation.create_reverse_foot.command as sacrc

UIFILEPATH = os.path.dirname(__file__).replace("\\", "/") + "/ui/gui.ui"
TITLE = "create_reverse_foot"


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
        self.UI.create_rf_btn.clicked.connect(self.create_rf)
        self.UI.delete_rf_rig_btn.clicked.connect(self.exec_delete_rf_rig_btn)

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def create_rf(self):
        side = self.get_checked_rbtn()
        rot_order_index = self.UI.rotation_order_cmbbox.currentIndex()
        sacrc.create_rf_rig(side, rot_order_index)

    def get_checked_rbtn(self):
        checked_btn = self.UI.foot_btngrp.checkedButton()
        current_btn_text = checked_btn.text()
        if current_btn_text == "両足":
            return "LR"
        elif current_btn_text == "左足":
            return "L"
        elif current_btn_text == "右足":
            return "R"
        else:
            return 0

    def exec_delete_rf_rig_btn(self):
        sacrc.bake_and_delete_anim()
        return 1

    def dockCloseEventTriggered(self):
        self.delete_instances()


def show(**kwargs):
    if RFTool._instance is None:
        RFTool._instance = RFTool()

    RFTool._instance.show(
        dockable=True,
    )

    RFTool._instance.setWindowTitle(TITLE)
