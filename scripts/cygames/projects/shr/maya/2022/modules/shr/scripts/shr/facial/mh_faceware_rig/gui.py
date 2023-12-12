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

import tool_log
from shr.facial.mh_faceware_rig.command import (
    RigGUICommands,
    RigUtilCommands,
    DrivenGUICommands,
)

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
UIFILEPATH = filePath + "/ui/gui.ui"
# 開発中かどうか
DEV = False


class MHFaceWareRig(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(MHFaceWareRig, self).__init__(parent)
        self.setObjectName("MHFaceWareRig")
        self.delete_instances()

        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)

        if not DEV:
            self.send_logger()

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.UI.create_subrig_gui_btn.clicked.connect(self.exec_create_subrig_gui_btn)
        self.UI.delete_subrig_gui_btn.clicked.connect(self.exec_delete_subrig_gui_btn)
        self.UI.create_drive_rig_btn.clicked.connect(self.exec_create_drive_rig_btn)
        self.UI.select_corresponding_rig_btn.clicked.connect(
            self.exec_select_corresponding_rig_btn
        )
        self.UI.enable_sub_rig_cbox.stateChanged.connect(
            self.change_enable_sub_rig_cbox
        )
        self.UI.bake_animation_btn.clicked.connect(self.exec_bake_animation_btn)

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    def send_logger(self) -> None:
        """ログ送信用"""
        logger_type = ""
        version = "v2022.01.23"

        logger_type = "MHFaceWareSubRig"

        logger = tool_log.get_logger(logger_type, version)
        logger.send_launch("")

    # -------------------------------
    # ボタン押したときの処理
    # -------------------------------
    def exec_create_subrig_gui_btn(self):
        # sub_rigの作成
        RigGUICommands.create_sub_rig()

    def exec_delete_subrig_gui_btn(self):
        RigGUICommands.delete_sub_rig_gui()

    def exec_select_corresponding_rig_btn(self):
        if RigGUICommands.get_ref_assetname("mh_sub_rigs_grps"):
            rigs = RigUtilCommands.get_corresponding_rig(pm.ls(sl=True))
            pm.select(rigs, r=True)
        else:
            pm.warning("subrig_gui does not exist.")

    def exec_bake_animation_btn(self):
        RigUtilCommands.select_mainrig()
        RigUtilCommands.bake_mainrig_animation()

    def exec_create_drive_rig_btn(self):
        rig_name = self.UI.rig_name_txt.text()
        DrivenGUICommands.create_driven_rig(rig_name)

    def change_enable_sub_rig_cbox(self):
        enable = self.UI.enable_sub_rig_cbox.isChecked()
        RigGUICommands.set_main_rig_enable(enable)


def show(**kwargs):
    if MHFaceWareRig._instance is None:
        MHFaceWareRig._instance = MHFaceWareRig()

    MHFaceWareRig._instance.show(
        dockable=True,
    )

    MHFaceWareRig._instance.setWindowTitle("MHFaceWareRig")
