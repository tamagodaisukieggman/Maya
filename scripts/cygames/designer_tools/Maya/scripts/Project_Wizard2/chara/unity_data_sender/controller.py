# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os
import webbrowser
from pathlib import Path
import typing as tp

import yaml

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.cmds as cmds

from .app import DataSender
from ..chara_utility import utility as chara_utility

g_tool_name = "Unity_Sender"
UI_PATH = os.path.dirname(__file__) + "/ui"
YAML_PATH = (
    r"C:\cygames\wiz2\tools\maya\settings\character_utility" + r"\utility_settings.yaml"
)


class UnityDataSenderMainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UnityDataSenderMainWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        ui_file_path = os.path.join(UI_PATH, "main.ui")
        self.UI = loader.load(ui_file_path)  # QMainWindow
        self.setCentralWidget(self.UI)
        self.setWindowTitle(g_tool_name)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.initialize_unity_settings()
        self.unity_path = self.UI.unity_resource_path_txt.text()
        self.initialize_settings(self.unity_path)
        # self.UI.data_send_to_unity_btn.clicked.connect(
        #     self.clicked_data_send_to_unity_btn
        # )
        self.UI.get_unity_path_btn.clicked.connect(self.clicked_reset_path_btn)
        self.UI.open_unity_folder_btn.clicked.connect(self.clicked_open_folder_btn)
        self.UI.open_workspace_folder_btn.clicked.connect(
            self.clicked_open_workspace_folder_btn
        )
        self.UI.unity_resource_path_txt.textChanged.connect(
            self.set_unity_resource_path
        )

        self.UI.get_local_wizard2Resources_btn.clicked.connect(
            self.clicked_get_local_wizard2Resources_btn
        )

    def initialize_settings(self, unity_path: str):
        """設定の初期化

        Args:
            unity_path (str): unityのパス
        """
        unity_path = Path(unity_path + "\\3d\\chr").as_posix()

        p4_path = Path("c:\\cygames\\wiz2\\team\\3dcg\\chr").as_posix()
        self.data_sender = DataSender(p4_path, unity_path)

        unity_path = self.data_sender.get_unity_path()
        workspace_path = self.data_sender.get_workspace_path()
        if not unity_path.startswith(self.unity_path):
            cmds.warning(f"Local__WizardResourcesが適切に設定されていません。")
            return
        self.UI.unity_folder_path_txt.setText(unity_path)
        self.UI.workspace_folder_path_txt.setText(workspace_path)

    def clicked_reset_path_btn(self):
        self.initialize_settings(self.unity_path)

    def clicked_data_send_to_unity_btn(self):
        try:
            is_override = self.UI.force_override_cbox.isChecked()
            self.data_sender.exec_send_unity_data(is_override)
        except:
            import traceback

            traceback.print_exc()
        message = "Unityへのデータの転送が完了しました。詳細はスクリプトエディターを参照ください。"
        cmds.inViewMessage(assistMessage=message, position="midCenterTop", fade=True)

    def clicked_open_folder_btn(self):
        folder = self.UI.unity_folder_path_txt.text()
        create_folder_if_not_exists_with_confirmation(folder)
        open_folder(folder)

    def clicked_open_workspace_folder_btn(self):
        folder = self.UI.workspace_folder_path_txt.text()
        create_folder_if_not_exists_with_confirmation(folder)
        open_folder(folder)

    def initialize_unity_settings(self):
        """ツール設定周りの初期化関数"""
        current_resource_path = self.get_unity_resource_path(YAML_PATH)
        if not os.path.exists(current_resource_path):
            cmds.warning("有効なLocal__WizardResourcesが設定されていません。settingsから設定してください。")
            return 0

        self.UI.unity_resource_path_txt.setText(current_resource_path)

    def clicked_get_local_wizard2Resources_btn(self):
        folder = chara_utility.get_folder_path()
        if folder:
            self.UI.unity_resource_path_txt.setText(folder)
            cmds.warning("Settingsが更新されました。Wizard2CharaUtilityを再起動します。")
            main()

    def set_unity_resource_path(self):
        current_resource_path = self.UI.unity_resource_path_txt.text()
        self.update_unity_resource_path(YAML_PATH, current_resource_path)

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
        CharaRebinderMainWindow: ツールウィンドウのインスタンス
    """
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = UnityDataSenderMainWindow()
    ui.show()
    return ui


def open_folder(folder_path: str) -> None:
    """
    指定されたフォルダパスをWindowsのエクスプローラで開く。
    Args:
        folder_path (str): 開きたいフォルダの絶対パス。
    Returns: None
    """
    os.startfile(folder_path)


def create_folder_if_not_exists_with_confirmation(folder_path: str) -> None:
    """
    指定されたフォルダが存在しない場合にconfirmDialogを表示し、
    ユーザーがYesを選んだ場合にフォルダを作成する関数。
    Args:
        folder_path (str): 作成または確認したいフォルダのパス
    Returns: なし
    """
    if not os.path.exists(folder_path):
        result = cmds.confirmDialog(
            title="Create Folder?",
            message=f"対象となるフォルダーが存在しません。作成しますか？\n {folder_path}?",
            button=["Yes", "No"],
            defaultButton="Yes",
            cancelButton="No",
            dismissString="No",
        )
        if result == "Yes":
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print("Folder creation canceled.")
    else:
        print(f"Folder already exists: {folder_path}")
