# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import shutil
import stat

from pathlib import Path
import typing as tp

from PySide2.QtWidgets import QLayout, QCheckBox

import maya.cmds as cmds


# データの各パスを管理するクラス
class DataSender:
    def __init__(self, p4_path: str, unity_path: str):
        self.unity_path = unity_path
        self.p4_path = p4_path

    def get_workspace_path(self):
        "p4のワークスペース用のパスを取得"
        current_path = Path(cmds.file(sn=True, q=True).lower())
        workspace_dir = current_path.parent.parent.as_posix()
        return workspace_dir

    def get_unity_path(self):
        """unityのプロジェクトパスを取得"""
        current_scene_path = cmds.file(sn=True, q=True).lower()
        unity_workspace_path = current_scene_path.replace(self.p4_path, self.unity_path)
        current_path = Path(unity_workspace_path)
        workspace_dir = current_path.parent.parent.as_posix()
        return workspace_dir

    def get_texture_paths(self) -> tp.List[str]:
        """p4側のtextureのパスを取得

        Returns:
            tp.List[str]: p4のテクスチャのパスを全て取得
        """
        sourceimages_path = self.get_workspace_path() + "/sourceimages"
        tgas = self.get_all_files_with_extension(sourceimages_path, "tga")
        return tgas

    def get_fbx_paths(self) -> tp.List[str]:
        """p4側のfbxのパスを取得

        Returns:
            tp.List[str]: p4側のfbxのパスを取得
        """
        sourceimages_path = self.get_workspace_path() + "/fbx"
        fbx = self.get_all_files_with_extension(sourceimages_path, "fbx")
        return fbx

    def convert_p4_to_unity_path(self, p4_full_path: str) -> str:
        """p4のパスをunityのパスに変換

        Args:
            p4_full_path (str): p4のフルパス

        Returns:
            str: unity上のパスを返す
        """
        p4_full_path = p4_full_path.lower()
        unity_path = p4_full_path.replace(self.p4_path, self.unity_path)
        return unity_path

    def exec_send_unity_data(self):
        # tgas = self.get_texture_paths()
        fbxs = self.get_fbx_paths()

        for fbx in fbxs:
            self.send_to_unity(fbx)

    def send_to_unity(self, fbx_path: str):
        """与えられたfbxパスをunityのfbxのパスに変換して転送

        Args:
            fbx_path (str): fbxのフルパス
        """
        unity_path = self.convert_p4_to_unity_path(fbx_path)
        DataSender.copy_file(fbx_path, unity_path, True)
        print(f"{fbx_path} >> {unity_path} 移行完了")
        return unity_path

    def get_current_file_name(self):
        current_file_path = cmds.file(sn=True, q=True)
        current_file_name = os.path.basename(current_file_path).split(".")[0]
        return current_file_name

    @staticmethod
    def get_all_files_with_extension(folder_path: str, extension: str) -> list:
        """
        指定されたフォルダ以下にあるすべての特定の拡張子を持つファイルを再帰的に取得します。
        Args:
            folder_path (str): ファイルを検索するフォルダのパス
            extension (str): 検索対象となる拡張子（例：'.txt'）
        Returns:
            list: 指定された拡張子のファイルのパスのリスト
        """
        extension_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(extension.lower()):
                    extension_files.append(os.path.join(root, file))
        return extension_files

    @staticmethod
    def copy_file(
        source_path: str, destination_path: str, overwrite: bool = False
    ) -> None:
        """
        与えられたパスAのファイルをパスBにコピーします。
        コピー先のフォルダが存在しない場合、フォルダを作成します。
        コピー先に既存のファイルが存在する場合、指定されたブール値引数に従って上書きまたはスキップします。
        Args:
            source_path (str): コピー元ファイルのパス
            destination_path (str): コピー先のパス
            overwrite (bool): 上書きする場合はTrue、スキップする場合はFalse
        Returns:
            None
        """
        destination_folder = os.path.dirname(destination_path)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        if os.path.exists(destination_path):
            if overwrite:
                # 上書きの場合
                shutil.copy2(source_path, destination_path)
            else:
                # スキップの場合、何も行わない
                pass
        else:
            # コピー先にファイルが存在しない場合、コピーを実行
            shutil.copy2(source_path, destination_path)

    @staticmethod
    def unlock_file(filepath: str) -> None:
        """
        指定されたファイルが読み取り専用である場合、属性を外します。
        Args:
            filepath (str): ファイルへのパス
        Returns:
            None
        """
        if os.path.isfile(filepath):
            os.chmod(filepath, os.stat(filepath).st_mode | stat.S_IWUSR)
        else:
            raise FileNotFoundError(f"File not found: {filepath}")
