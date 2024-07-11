# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import yaml
import webbrowser

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# shibokenの読み込み
try:
    import shiboken2 as shiboken
except:
    import shiboken

# import pymel.core as pm
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
from importlib import reload as reload

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")

UI_FILE_PATH = filePath + "/ui/main.ui"
ANIMTOOL_YAML = filePath + "/chara_tools_launcher_settings.yaml"


# widgets example to add
class CharaToolLauncherMainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(CharaToolLauncherMainWindow, self).__init__(parent)
        self.setObjectName("CharaToolLauncherMainWindow")

        self.delete_instances()

        # UIのパスを指定
        self.UI = QUiLoader().load(UI_FILE_PATH)
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        tools = []

        if os.path.isfile(ANIMTOOL_YAML):
            with open(ANIMTOOL_YAML, encoding="utf-8") as file:
                tools = yaml.safe_load(file)["tools"]

        lay = self.UI.main_vbox

        self.UI.action_tool_document.triggered.connect(show_manual)

        self.register_tools(lay, tools)

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            cmds.deleteUI(workspace_control_name)

    def register_tools(self, grp, tools):
        for tool in tools:
            if tool["type"] == "command":
                self.register_command(grp, tool)
            elif tool["type"] == "separator":
                lay = self.create_layout_with_lines_and_label(tool["name"])
                grp.addLayout(lay)

    def get_exec_script(self, tool: dict) -> str:
        return tool["command"] + f';print("shelfに登録する場合は以下のコマンドをコピー:{tool["command"]}")'

    def register_command(self, grp, tool):
        btn = QtWidgets.QPushButton(tool["label"])
        grp.addWidget(btn)
        if "icon" in tool:
            self.add_icon_to_button(btn, f":/{tool['icon']}")

        if "color" in tool:
            style = "QPushButton{}".format("{" + tool["color"] + "}")
            btn.setStyleSheet(style)

        # set enable
        btn.setEnabled(tool["enable"])

        # set tooltips
        btn.setToolTip(tool["tooltip"])

        script = self.get_exec_script(tool)
        # connect
        btn.clicked.connect(
            lambda checked=None, script=self.get_exec_script(tool): exec(script)
        )

        # 文字サイズ
        font = btn.font()
        font.setPointSize(8)
        btn.setFont(font)

        # generate optionbutton
        if tool.get("option") != None:
            option_btn = QtWidgets.QPushButton("⚙")
            option_btn.clicked.connect(
                lambda checked=None, script=tool["option"]: exec(script)
            )

            option_btn.setEnabled(tool["enable"])

            # HLayoutを作ってボタンを入れる
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(btn)
            layout.addWidget(option_btn)

            # ボタンのサイズポリシーを取得
            sizePolicy1 = btn.sizePolicy()
            sizePolicy2 = option_btn.sizePolicy()
            sizePolicy1.setHorizontalStretch(1)
            sizePolicy2.setHorizontalStretch(0)
            # サイズポリシーをセット
            btn.setSizePolicy(sizePolicy1)
            option_btn.setSizePolicy(sizePolicy2)

            grp.addLayout(layout)

    def create_layout_with_lines_and_label(self, text: str) -> QtWidgets.QHBoxLayout:
        layout = QtWidgets.QHBoxLayout()

        # Horizon line 1
        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.HLine)
        layout.addWidget(line1)

        # Label with text
        label = QtWidgets.QLabel(text)
        layout.addWidget(label)

        font = label.font()
        font.setPointSize(9)
        label.setFont(font)

        # Horizon line 2
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        layout.addWidget(line2)

        layout.setStretchFactor(line1, 1)
        layout.setStretchFactor(line2, 1)

        return layout

    def add_icon_to_button(self, button: QtWidgets.QPushButton, icon_path: str):
        icon = QtGui.QIcon(icon_path)
        font_metrics = QtGui.QFontMetrics(button.font())
        text_height = font_metrics.height()
        icon_size = QtCore.QSize(text_height + 4, text_height + 4)
        button.setIcon(icon)
        button.setIconSize(icon_size)
        button.setText(" " + button.text())

    def dockCloseEventTriggered(self):
        self.delete_instances()


def show_manual():
    """コンフルのツールマニュアルページを開く"""
    try:
        webbrowser.open(
            "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=720604797"
        )
    except Exception:
        cmds.warning("マニュアルページがみつかりませんでした")


def show(**kwargs):
    if CharaToolLauncherMainWindow._instance is None:
        CharaToolLauncherMainWindow._instance = CharaToolLauncherMainWindow()

    CharaToolLauncherMainWindow._instance.show(
        dockable=True,
    )

    CharaToolLauncherMainWindow._instance.setWindowTitle("Character Tool Launcher")
