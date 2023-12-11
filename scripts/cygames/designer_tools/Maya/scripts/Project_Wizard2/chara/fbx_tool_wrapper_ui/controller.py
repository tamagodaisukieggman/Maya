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

from ..fbx_exporter.main import CharaExporterMainWindow
from ..fbx_exporter import chara_fbx
from ..unity_data_sender.controller import UnityDataSenderMainWindow
from ..unity_data_sender import controller as unityDatasenderController


g_tool_name = "FBX_Tools"
UI_PATH = os.path.dirname(__file__) + "/ui"


class FBXToolsMainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(FBXToolsMainWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        uiFilePath = os.path.join(UI_PATH, "main.ui")
        self.ui = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.ui)
        self.setWindowTitle(g_tool_name)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.chara_exporter = CharaExporterMainWindow()
        self.unity_sender = UnityDataSenderMainWindow()

        self.ui.fbx_exporter_lay.addWidget(self.chara_exporter)
        self.ui.unity_data_sender_lay.addWidget(self.unity_sender)

        self.ui.export_fbx_and_forward_to_unity_btn.clicked.connect(
            self.exec_export_fbx_and_forward_to_unity_btn
        )

        # UIのリセットをこのMainWindowで行うように上書き
        unityDatasenderController.main = main
        # fbxexporter側のボタンは使用しないので非表示
        self.chara_exporter.ui.btn_export_fbx.hide()

    def exec_export_fbx_and_forward_to_unity_btn(self):
        """fbxを出力して、unityへ転送をまとめて行う"""
        fbx_paths = chara_fbx.export_fbx(
            self.chara_exporter.ui.chk_export_parts,
            self.chara_exporter.ui.chk_only_visible,
            self.chara_exporter.ui.chk_save_before,
        )

        if self.ui.used_send_unity_cbox.isChecked():
            for fbx_path in fbx_paths:
                self.unity_sender.data_sender.send_to_unity(fbx_path)


def main():
    """Windowの起動
    Returns:
        EdgeSetMainWindow: ツールウィンドウのインスタンス
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = FBXToolsMainWindow()
    ui.show()
    return ui
