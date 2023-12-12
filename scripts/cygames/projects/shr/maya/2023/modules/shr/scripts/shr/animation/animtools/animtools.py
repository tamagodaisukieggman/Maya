# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import yaml
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
from importlib import reload as reload

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
art_path = (
    filePath.split("shr/script", 1)[0]
    + "shr3d\\scripts\\shr3d\\animation\\animation_exporter_settings"
)
art_path = art_path.replace("\\", "/")

UI_FILE_PATH = filePath + "/ui/gui.ui"
ANIMTOOL_YAML = filePath + "/animtools.yaml"
ANIMTOOL_PROJECT_YAML = art_path + "/animtools_project.yaml"
ANIMTOOL_USER_YAML = art_path + "/animtools_user.yaml"


# widgets example to add
class AnimToolMainTool(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    _instance = None

    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return "{}.{}".format(self.__module__, self.__class__.__name__)

    def __init__(self, parent=None):
        super(AnimToolMainTool, self).__init__(parent)
        self.setObjectName("AnimToolMainTool")

        self.delete_instances()

        # UIのパスを指定
        self.UI = QUiLoader().load(UI_FILE_PATH)
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.commands = []

        if os.path.isfile(ANIMTOOL_YAML):
            with open(ANIMTOOL_YAML, encoding="utf-8") as file:
                self.commands.append(yaml.safe_load(file)["commands"])
        if os.path.isfile(ANIMTOOL_PROJECT_YAML):
            with open(ANIMTOOL_PROJECT_YAML, encoding="utf-8") as file:
                self.commands.append(yaml.safe_load(file)["commands"])
        if os.path.isfile(ANIMTOOL_USER_YAML):
            with open(ANIMTOOL_USER_YAML, encoding="utf-8") as file:
                self.commands.append(yaml.safe_load(file)["commands"])

        for grp, command in zip(
            [self.UI.ta_grp, self.UI.project_grp, self.UI.user_grp],
            self.commands,
        ):
            if command != None:
                self.register_commands(grp, command)

        # self.UI.refresh_btn.clicked.connect(lambda :self.setWindowTitle("AnimToolMainTool"))

    def delete_instances(self):
        workspace_control_name = self.objectName() + "WorkspaceControl"
        if cmds.workspaceControl(workspace_control_name, exists=True):
            pm.deleteUI(workspace_control_name)

    def register_commands(self, grp, commands):
        for command in commands:
            btn = QtWidgets.QPushButton(command["label"])

            # カテゴリ分け（多くなりそうなら自動化？）
            # self.UI.utility_grp.addWidget(btn)
            grp.addWidget(btn)

            if "color" in command:
                style = "QPushButton{}".format("{" + command["color"] + "}")
                btn.setStyleSheet(style)

            # set enable
            btn.setEnabled(command["enable"])

            # set tooltips
            btn.setToolTip(command["tooltip"])

            # connect
            btn.clicked.connect(
                lambda checked=None, script=command["command"]: exec(script)
            )

            # generate optionbutton
            if command.get("option") != None:
                option_btn = QtWidgets.QPushButton("⚙")
                option_btn.clicked.connect(
                    lambda checked=None, script=command["option"]: exec(script)
                )

                option_btn.setEnabled(command["enable"])

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

    def dockCloseEventTriggered(self):
        self.delete_instances()


def show(**kwargs):
    if AnimToolMainTool._instance is None:
        AnimToolMainTool._instance = AnimToolMainTool()

    AnimToolMainTool._instance.show(
        dockable=True,
    )

    AnimToolMainTool._instance.setWindowTitle("Animator Tools")
