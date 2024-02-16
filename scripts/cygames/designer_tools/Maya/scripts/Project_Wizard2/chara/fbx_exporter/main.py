# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

import os
import functools
import webbrowser

from PySide2 import QtWidgets ,QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from . import chara_fbx

reload(chara_fbx)

import maya.cmds as cmds

from importlib import reload

g_tool_name = "FBX_Exporter"
UI_PATH = os.path.dirname(__file__) + "/ui"


class CharaExporterMainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """キャラユーティリティWindow"""

    def __init__(self, parent=None):
        super(CharaExporterMainWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        uiFilePath = os.path.join(UI_PATH, "main.ui")
        self.ui = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.ui)
        self.setWindowTitle(g_tool_name)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        # self.ui.action_manual.triggered.connect(show_manual)

        # FBXエクスポート
        self.ui.btn_export_fbx.clicked.connect(
            functools.partial(
                chara_fbx.export_fbx,
                self.ui.chk_export_parts,
                self.ui.chk_only_visible,
            )
        )
        self.ui.chk_save_before.setVisible(False)

        self.ui.chk_export_parts.setChecked(True)
        self.ui.chk_export_parts.setVisible(False)


def show_manual():
    """コンフルのツールマニュアルページを開く"""
    try:
        webbrowser.open(
            "https://wisdom.cygames.jp/pages/viewpage.action?pageId=440909007"
        )
    except Exception:
        cmds.warning("マニュアルページがみつかりませんでした")


def main():
    """Windowの起動
    Returns:
        CharaExporterMainWindow: ツールウィンドウのインスタンス
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = CharaExporterMainWindow()
    ui.show()
    return ui
