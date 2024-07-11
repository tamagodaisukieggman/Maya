# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os
import functools
import webbrowser
import yaml

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from . import vertex_color
import maya.cmds as cmds

from importlib import reload

g_tool_name = "Hidden_vertex_color"
UI_PATH = os.path.dirname(__file__)+"/ui"

class HiddenVertexColorMainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """キャラユーティリティWindow"""

    def __init__(self, parent=None):
        super(HiddenVertexColorMainWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        uiFilePath = os.path.join(UI_PATH, "main.ui")
        self.UI = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.UI)
        self.setWindowTitle(g_tool_name)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        #self.UI.action_manual.triggered.connect(show_manual)

        self.UI.btn_pumps.clicked.connect(
            functools.partial(vertex_color.set_vertex_color_for_shoes, "パンプス用")
        )
        self.UI.btn_foot.clicked.connect(
            functools.partial(vertex_color.set_vertex_color_for_shoes, "低い靴用")
        )
        self.UI.btn_ankle.clicked.connect(
            functools.partial(vertex_color.set_vertex_color_for_shoes, "中間の靴用")
        )
        self.UI.btn_boots.clicked.connect(
            functools.partial(vertex_color.set_vertex_color_for_shoes, "高い靴用")
        )
        self.UI.btn_visible.clicked.connect(
            functools.partial(vertex_color.set_vertex_color_for_shoes, "消さない部分用")
        )
        # Paint Vertex Color Tool 起動
        self.UI.btn_paint_vtx_tool.clicked.connect(
            vertex_color.paint_vertex_color_tool_options
        )
        # 頂点カラー表示・非表示切り替え
        self.UI.btn_toggle_display_color.clicked.connect(
            vertex_color.toggle_display_colors_attr
        )



def show_manual():
    """コンフルのツールマニュアルページを開く"""
    try:
        webbrowser.open(
            "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=440909007"
        )
    except Exception:
        cmds.warning("マニュアルページがみつかりませんでした")


def main():
    """Windowの起動
    Returns:
        HiddenVertexColorMainWindow: ツールウィンドウのインスタンス
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = HiddenVertexColorMainWindow()
    ui.show()
    return ui
