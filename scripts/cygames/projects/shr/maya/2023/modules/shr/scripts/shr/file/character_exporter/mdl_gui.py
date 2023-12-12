# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from functools import partial

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
import shr.file.character_exporter.command as command
from shr.file.character_exporter.ue import ue_gui_utils


UIFILEPATH = os.path.dirname(__file__).replace("\\", "/") + "/ui/mdl_gui.ui"
TITLE = "Character_Exporter"


class MdlMainTool(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(MdlMainTool, self).__init__(parent)
        self.setObjectName(TITLE)

        self.delete_instances()
        self.exporter = command.Exporter("model")
        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # UIの初期化
        ue_gui_utils.initialize_ue_import_settings(self.UI)

        self.initialize_fbx_exporter()

        # Connected
        self.UI.is_create_skeleton_cbox.stateChanged.connect(
            self.state_change_is_create_skeleton_cbox
        )
        # self.UI.unreal_import_cbox.stateChanged.connect(
        #     self.state_change_unreal_import_cbox
        # )

        self.UI.export_btn.clicked.connect(self.exec_export)
        self.UI.only_import_btn.clicked.connect(self.exec_only_import)
        self.UI.refresh_btn.clicked.connect(self.re_open)

        # ue用uiのinitialize
        initialize_ue = partial(ue_gui_utils.initialize_ue_import_settings, self.UI)
        self.UI.check_connection_btn.clicked.connect(initialize_ue)

        self.UI.fbx_path_txt.textChanged.connect(self.save_ui_info)
        self.UI.fbx_name_txt.textChanged.connect(self.save_ui_info)

    def initialize_fbx_exporter(self):
        # UIの設定
        self.load_ui_info()

    def re_open(self):
        import shr.file.character_exporter.mdl_gui as aeg
        from importlib import reload

        reload(aeg)
        aeg.show()

    def exec_export(self) -> bool:
        """exportを実行"""
        create_skeleton = self.UI.is_create_skeleton_cbox.isChecked()
        if create_skeleton:
            skeleton_name = self.UI.skeleton_name_txt.text()
        else:
            skeleton_name = self.UI.skeleton_cmbbox.currentText()

        import_unreal = self.UI.unreal_import_cbox.isChecked()
        command.character_export(import_unreal, skeleton_name, create_skeleton)

    def state_change_is_create_skeleton_cbox(self):
        checked = self.UI.is_create_skeleton_cbox.isChecked()
        self.UI.skeleton_name_txt.setEnabled(checked)
        self.UI.skeleton_cmbbox.setEnabled(not checked)

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    # -------------------------------
    # ueへのインポート処理
    # -------------------------------

    def exec_only_import(self):
        """importを実行"""
        create_skeleton = self.UI.is_create_skeleton_cbox.isChecked()
        skeleton_name = ue_gui_utils.get_skeleton_name(self.UI)
        command.ue_import_enginefile(create_skeleton, skeleton_name)

    # -------------------------------
    # UIの情報保存/読み込み
    # -------------------------------

    def save_ui_info(self):
        """ui情報の保存"""
        cmds.fileInfo("model_export_path", self.UI.fbx_path_txt.text())
        cmds.fileInfo("model_export_name", self.UI.fbx_name_txt.text())

    def load_ui_info(self):
        """ui情報の読み込み"""
        if cmds.fileInfo("model_export_path", q=True) == []:
            self.exporter.initialize_ui_info()

        self.UI.fbx_path_txt.setText(cmds.fileInfo("model_export_path", query=True)[0])
        self.UI.fbx_name_txt.setText(cmds.fileInfo("model_export_name", query=True)[0])


def show(**kwargs):
    if MdlMainTool._instance is None:
        MdlMainTool._instance = MdlMainTool()

    MdlMainTool._instance.show(
        dockable=True,
    )

    MdlMainTool._instance.setWindowTitle(TITLE)
