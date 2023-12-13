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

from . import chara_utility
from . import chara_fbx
from . import chara_outline
from . import vertex_color
from . import bind_rebind
from .chara_other_tools import OtherTools

reload(chara_fbx)
reload(chara_outline)
reload(vertex_color)
reload(bind_rebind)

import maya.cmds as cmds

from importlib import reload
from ..character_checker import app as chr_checker
# from ..unity_data_setter.controller import UnityDataSenderWidget

g_tool_name = "Wizard2CharaUtility"
CURRENT_PATH = os.path.dirname(__file__)
YAML_PATH = (
    r"C:\cygames\wiz2\tools\maya\settings\character_utility" + r"\utility_settings.yaml"
)


class FrameLayout(object):
    """QTDesignerでFrameLayoutを作るクラス"""

    def __init__(self, titleBar, frame):
        self.titleBar = titleBar  # 開閉ボタン
        self.frame = frame  # 開閉するウィジェット
        self.collapse = False  # 開閉している状態フラグ
        self.setSignals()  # シグナルをセット

    def setSignals(self):
        """シグナルを設定する"""
        self.titleBar.clicked.connect(self.setCollapse)

    def setCollapse(self):
        """フレームを開閉するアクション"""
        # 現在のステータスを反転する
        self.collapse = not self.collapse
        # フレームのビジビリティを変更する
        self.frame.setHidden(self.collapse)

        # 開閉状況に合わせてアロータイプを変更する
        if self.collapse:
            # 閉じている時は右に向ける
            self.titleBar.setArrowType(QtCore.Qt.RightArrow)
        else:
            # 開いている時は下へ向ける
            self.titleBar.setArrowType(QtCore.Qt.DownArrow)


class CharaUtilityWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """キャラユーティリティWindow"""

    def __init__(self, parent=None):
        super(CharaUtilityWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, "wiz2_chara_utility.ui")
        self.UI = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.UI)
        self.setWindowTitle(g_tool_name)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.UI.action_manual.triggered.connect(show_manual)
        # FBXエクスポート
        self.frameLayout1 = FrameLayout(
            self.UI.expand_fbx_export, self.UI.frame_fbx_export
        )
        self.UI.btn_export_fbx.clicked.connect(
            functools.partial(
                chara_fbx.export_fbx,
                self.UI.chk_export_parts,
                self.UI.chk_only_visible,
                self.UI.chk_save_before,
            )
        )
        self.initialize_settings()

        # data_sender_widget = UnityDataSenderWidget(
        #     self.UI.unity_resource_path_txt.text()
        # )
        # self.UI.send_unity_lay.addWidget(data_sender_widget)

        # バインド (Dominion > Wizard2)
        self.UI.btn_bind.clicked.connect(bind_rebind.BindSkinCmd.project_bind)
        # リバインド (Dominion > Wizard2)
        self.UI.btn_rebind_new.clicked.connect(bind_rebind.BindSkinCmd.rebind)

        # アウトライン
        self.frameLayout3 = FrameLayout(
            self.UI.expand_create_outline, self.UI.frame_create_outline
        )
        self.UI.btn_create_outline.clicked.connect(chara_outline.create_outline)
        # 足先非表示の頂点カラー設定
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

        self.frameLayout5 = FrameLayout(
            self.UI.expand_checker_tools, self.UI.frame_checker_tools
        )

        self.frameLayout4 = FrameLayout(
            self.UI.expand_other_tools, self.UI.frame_other_tools
        )
        self.UI.btn_segmentscale_off.clicked.connect(self.clicked_btn_segmentscale_off)
        self.UI.btn_character_checker.clicked.connect(
            self.clicked_btn_character_checker
        )

        self.UI.unity_resource_path_txt.textChanged.connect(
            self.set_unity_resource_path
        )

        self.UI.get_local_wizard2Resources_btn.clicked.connect(self.clicked_get_local_wizard2Resources_btn)

    def initialize_settings(self):
        """ツール設定周りの初期化関数"""
        current_resource_path = self.get_unity_resource_path(YAML_PATH)
        if not os.path.exists(current_resource_path):
            cmds.warning("有効なLocal__WizardResourcesが設定されていません。settingsから設定してください。")
            return 0

        self.UI.unity_resource_path_txt.setText(current_resource_path)

    def clicked_btn_segmentscale_off(self):
        selected = cmds.ls(sl=True)
        OtherTools.set_segment_scale(False, selected)

    def clicked_btn_character_checker(self):
        chr_checker.show_checker_gui()

    def clicked_get_local_wizard2Resources_btn(self):
        folder = chara_utility.get_folder_path()
        if folder:
            self.UI.unity_resource_path_txt.setText(folder)
            cmds.warning("Settingsが更新されました。Wizard2CharaUtilityを再起動します。")
            main()

    def set_unity_resource_path(self):
        current_resource_path = self.UI.unity_resource_path_txt.text()
        CharaUtilityWindow.update_unity_resource_path(YAML_PATH, current_resource_path)

    @staticmethod
    def get_unity_resource_path(yaml_file: str) -> str:
        """
        指定されたYAMLファイル内の 'unity_resource_path' の値を取得します
        Args:
            yaml_file (str): YAMLファイルのパス
        Returns:
            str: YAMLファイル内の 'unity_resource_path' の値
        """
        if not os.path.exists(yaml_file):
            return ""

        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file)

        if "unity_resource_path" in data:
            return data["unity_resource_path"]
        else:
            raise KeyError(f"unity_resource_path not found in {yaml_file}")

    @staticmethod
    def update_unity_resource_path(yaml_file: str, new_resource_path: str) -> None:
        """
        指定されたYAMLファイルの 'unity_resource_path' を更新します。YAMLファイルが存在しない場合、新しいYAMLファイルを作成します。

        Args:
            yaml_file (str): YAMLファイルのパス
            new_resource_path (str): 新しいユニティリソースパス

        Returns:
            None
        """

        # 親フォルダのパスを取得
        parent_folder = os.path.dirname(yaml_file)

        # 親フォルダが存在しない場合、フォルダを作成
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)

        if not os.path.exists(yaml_file):
            with open(yaml_file, "w") as file:
                yaml.dump({"unity_resource_path": new_resource_path}, file)
        else:
            with open(yaml_file, "r") as file:
                data = yaml.safe_load(file)
            if "unity_resource_path" in data:
                data["unity_resource_path"] = new_resource_path
            else:
                raise KeyError("unity_resource_path not found in YAML file")
            with open(yaml_file, "w") as file:
                yaml.dump(data, file)


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
        CharaUtilityWindow: ツールウィンドウのインスタンス
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = CharaUtilityWindow()
    ui.show()
    return ui
