# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import yaml
import webbrowser

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

import maya.cmds as cmds
from importlib import reload as reload

# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")

UI_FILE_PATH = filePath + "/ui/main.ui"
SETTINGS_YAML = filePath + "/chara_tools_launcher_settings.yaml"
ICON_PATH = filePath + "/icons"
TOOL_NAME = "Character_Tool_Launcher"

# widgets example to add
class CharaToolLauncherMainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CharaToolLauncherMainWindow, self).__init__(parent)
        # UIのパスを指定
        self.UI = QUiLoader().load(UI_FILE_PATH)
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.category_layouts = {}
        
        tools = []
        if os.path.isfile(SETTINGS_YAML):
            with open(SETTINGS_YAML, encoding="utf-8") as file:
                yaml_data = yaml.safe_load(file)
                tools = yaml_data["tools"]
                setting_pathes = yaml_data["sub_settings_path"]

        for path in setting_pathes:
            if os.path.exists(path):
                with open(path, encoding="utf-8") as file:
                    yaml_data = yaml.safe_load(file)
                    tool = yaml_data["tools"]
                    if tool:
                        tools.extend(tool)

        main_v_layout = self.UI.main_vbox

        self.UI.action_tool_document.triggered.connect(show_manual)

        self.register_tools(main_v_layout, tools)
        

    def register_tools(self, lay:QtWidgets.QBoxLayout, tools:dict):
        """toolのtype情報に基づいてlayに新しいボタンを追加する

        Args:
            lay (QtWidgets.QBoxLayout): ボタンが追加されるlayout
            tools (dict): 追加されるボタンの情報
        """
        last_category_layout = None

        for tool in tools:
            if tool["type"] == "category":
                new_category_v_lay = self.register_category(lay,tool["label"])
                self.category_layouts[tool["name"]] = new_category_v_lay
                last_category_layout = new_category_v_lay

                continue
            
            category_lay = None
            if "category" in tool:
                category_lay = self.category_layouts[tool["category"]]
            else:
                if last_category_layout:
                    category_lay = last_category_layout
                else:
                    cmds.warning(f"有効なcategoryが存在しないため{tool['name']}を追加できません。")

            if tool["type"] == "command":
                self.register_command(category_lay, tool)

            elif tool["type"] == "nest":
                self.register_nest_objects(category_lay, tool)

    def get_exec_script(self, tool: dict) -> str:
        return tool["command"]

    def register_command(self, lay, tool):
        btn = QtWidgets.QPushButton(tool["label"])
        lay.addWidget(btn)
        if "icon" in tool:
            if "/" in tool['icon']:
                self.add_icon_to_button(btn, f"{ICON_PATH}/{tool['icon']}")
            else:
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

            lay.addLayout(layout)

    def register_nest_objects(self,lay:QtWidgets.QBoxLayout,tool:dict):
        """nestタイプのオブジェクト追加
        toolsに入っているオブジェクトをhorizontal layoutに並べる
        nest type
        """

        # lauoutの作成
        tools_h_lay_box = QtWidgets.QHBoxLayout()
        title_h_lay_box = QtWidgets.QHBoxLayout()
        v_lay_box = QtWidgets.QVBoxLayout()
        
        # groupの作成
        groupBox = QtWidgets.QGroupBox(self)

        groupBox.setObjectName(tool["name"])
        groupBox.setTitle("")
        groupBox.setStyleSheet(
            """
            QGroupBox {
                border: 1px solid;
                border-color: gray;
                font-size: 5em;
                border-radius: 6px;
            }
            
            QGroupBox::title {
                color: #fff;
                background: transparent;
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0.4em 0 0 0;
            }
            
            """
        )

        # title設定
        title_label = QtWidgets.QLabel(tool["label"])
        # 文字サイズ
        font = title_label.font()
        font.setPointSize(8)
        title_label.setFont(font)

        # icon設定
        icon_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f":/{tool['icon']}")
        resized_pixmap = pixmap.scaled(20, 20)
        icon_label.setPixmap(resized_pixmap)
        
        # 中央寄せのhorizon layout作成
        title_h_lay_box.addStretch()
        title_h_lay_box.addWidget(icon_label)
        title_h_lay_box.addWidget(title_label)
        title_h_lay_box.addStretch() 
        

        #　verticalのlayoutにまとめる
        v_lay_box.addLayout(title_h_lay_box)
        v_lay_box.addLayout(tools_h_lay_box)
        groupBox.setLayout(v_lay_box)
        

        lay.addWidget(groupBox)

        # toolをhorizonの中に追加していく
        for tool in tool["tools"]:
            self.register_command(tools_h_lay_box,tool)

    def register_category(self, lay:QtWidgets.QBoxLayout,text: str) -> QtWidgets.QVBoxLayout:
        """separatorの登録
        ---エクスポーター---
        のようなカテゴリ分けに使用

        Args:
            lay (QtWidgets.QBoxLayout): ボタンが追加されるlayout
            text (str): separatorのタイトル
        """
        category_layout = QtWidgets.QVBoxLayout()
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

        category_layout.addLayout(layout)
        lay.addLayout(category_layout)

        return category_layout

    def add_icon_to_button(self, button: QtWidgets.QPushButton, icon_path: str):
        icon = QtGui.QIcon(icon_path)
        font_metrics = QtGui.QFontMetrics(button.font())
        text_height = font_metrics.height()
        icon_size = QtCore.QSize(text_height + 8, text_height + 8)
        button.setIcon(icon)
        button.setIconSize(icon_size)
        button.setText(" " + button.text())


def show_manual():
    """コンフルのツールマニュアルページを開く"""
    try:
        webbrowser.open(
            "https://wisdom.cygames.jp/pages/viewpage.action?pageId=720604797"
        )
    except Exception:
        cmds.warning("マニュアルページがみつかりませんでした")

def show():
    """Windowの起動
    """
    tool_name = TOOL_NAME
    
    workspace_control_name = tool_name + "WorkspaceControl"
    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name)
    ui = CharaToolLauncherMainWindow()
    
    ui.setWindowTitle(tool_name)
    ui.setObjectName(tool_name)
    ui.show(dockable=True,)

