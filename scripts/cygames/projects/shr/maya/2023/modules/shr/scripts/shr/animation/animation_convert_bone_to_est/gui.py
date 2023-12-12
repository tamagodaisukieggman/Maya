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

import shr.animation.animation_convert_bone_to_est.maya_command as maya_command
import shr.animation.animation_convert_bone_to_est.utils as ca


UIFILEPATH = os.path.dirname(__file__).replace("\\", "/") + "/ui/gui.ui"
TITLE = "animation_converter"


class ConvertAnimationGUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(ConvertAnimationGUI, self).__init__(parent)
        self.setObjectName(TITLE)
        self.delete_instances()
        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)
        self.send_logger()

        self.UI.get_fbx_path_btn.clicked.connect(self.exec_get_fbx_path_btn)
        self.UI.get_defaultscene_path_btn.clicked.connect(
            self.exec_get_defaultscene_path_btn
        )
        self.UI.convert_btn.clicked.connect(self.exec_convert_btn)

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def dockCloseEventTriggered(self):
        self.delete_instances()

    def send_logger(self) -> None:
        """ログ送信用"""
        version = "v2023.03.28"
        logger_type = "animation_converter"

        logger = tool_log.get_logger(logger_type, version)
        logger.send_launch("")

    # Connection
    def exec_get_fbx_path_btn(self) -> None:
        """fbxのパス取得"""
        path = maya_command.exec_get_filepath_dialog()
        if path != None:
            self.UI.fbx_path_txt.setText(path[0])

    def exec_get_defaultscene_path_btn(self) -> None:
        """defaultsceneのパス取得"""
        path = maya_command.exec_get_filepath_dialog()
        if path != None:
            self.UI.defaultscene_path_txt.setText(path[0])

    def exec_convert_btn(self) -> None:
        """アニメーションのコンバートの実行"""
        fbx_path = self.UI.fbx_path_txt.text()
        default_scene_path = self.UI.defaultscene_path_txt.text()
        name_space = self.UI.namespace_text.text()
        conv = ca.eSTAnimationConverter(name_space)
        conv.convert_animation(default_scene_path, fbx_path)


def show(**kwargs):
    if ConvertAnimationGUI._instance is None:
        ConvertAnimationGUI._instance = ConvertAnimationGUI()

    ConvertAnimationGUI._instance.show(
        dockable=True,
    )

    ConvertAnimationGUI._instance.setWindowTitle(TITLE)
