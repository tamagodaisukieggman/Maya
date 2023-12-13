import os
import re
import sys
import maya.cmds as cmds
from PySide2 import QtWidgets, QtGui, QtCore
from ueremoteclient import Client

# Shenronの骨配置場所
SHR_SKEL_PATH = "/Game/shr/Resources/Rigs/Skeleton/"


class ue_client:
    @classmethod
    def check_connection(cls):
        try:
            Client().run_command("print('Connection')")
        except RuntimeError:
            cmds.warning("failed connection UE.")
            return False
        return True

    @classmethod
    def get_all_shr_skeletons(cls) -> list:
        """全ての"skel_"が含まれる骨を取得

        Returns:
            list: "skel_"が含まれるすべての骨
        """
        pattern = re.compile(r"Name\(\"(skel_.*?)\"\)")
        result = str(Client().run_file("get_skeletons_from_directory", [SHR_SKEL_PATH]))
        all_skeltons = re.findall(pattern, result)
        return all_skeltons


class ue_gui_utils:
    @classmethod
    def initialize_ue_import_settings(cls, UI):
        connection = ue_gui_utils.exec_check_connection(UI)
        if connection:
            cls.set_current_skeleton_combo_box(UI)
        cls.set_enable_ue_tools(UI, connection)

    @classmethod
    def exec_check_connection(cls, UI) -> bool:
        """_summary_

        Args:
            UI (_type_): 変更処理を行うUI

        Returns:
            bool: connectionの可否
        """
        connection = False
        if ue_client.check_connection():
            style = "QLabel{color : #2eff00;background-color: rgb(33, 33, 33);}"
            text = "ue_enabled"
            connection = True
            cls._set_import_cbox(UI, True)
        else:
            style = "QLabel{color : #ff0000;background-color: rgb(33, 33, 33);}"
            text = "ue_disabled"
            cls._set_import_cbox(UI, False)

        UI.ue5_enable_txt.setStyleSheet(style)
        UI.ue5_enable_txt.setText(text)

        return connection

    @classmethod
    def _set_import_cbox(cls, UI: any, enable: bool) -> bool:
        """import checkboxが存在していればステータスを変更

        Args:
            UI (any): _description_
            enable (bool): _description_

        Returns:
            bool: _description_
        """
        try:
            if enable:
                UI.unreal_import_cbox.setCheckState(QtCore.Qt.Checked)
                UI.unreal_import_cbox.setEnabled(True)
            else:
                UI.unreal_import_cbox.setCheckState(QtCore.Qt.Unchecked)
                UI.unreal_import_cbox.setEnabled(False)

            return True

        except:
            cmds.warning("unreal_import_cbox is missing.")
            return False

    @classmethod
    def set_current_skeleton_combo_box(cls, UI):
        """
        shotgridからSkeletonタイプのアセットをget
        """
        UI.skeleton_cmbbox.clear()
        try:
            assets = ue_client.get_all_shr_skeletons()
            for lp in assets:
                UI.skeleton_cmbbox.addItem(lp)

        except RuntimeError:
            cmds.warning("UnrealEngine is not open. can't get skeleton name.")

    @classmethod
    def set_enable_ue_tools(cls, UI, enabled):
        for lp in ["unreal_import_tools_grpbox", "unreal_import_settings_grpbox"]:
            try:
                grp_box = eval("UI.{}".format(lp))
                grp_box.setEnabled(enabled)
            except AttributeError:
                continue

    @staticmethod
    def _get_ws_type(prep_type: str) -> str:
        """get_ws_nameで使用するtypeをprep type から予想して出力
        一旦characterしか使用していないので、characterを決め打ち

        Args:
            prep_type (str): _description_

        Returns:
            str: _description_
        """
        return "Character"

    @classmethod
    def _get_asset_data(cls, id: str):  # -> Optional[AssetData]:
        """assetidの取得

        Args:
            id (str): from_asset_nameに流し込むid

        Returns:
            assetdata: assetdata
        """
        path = "C:\\cygames\\shrdev\\shr\\tools\\in\\sta\\shrcmd"
        if not path in sys.path:
            sys.path.append(path)
        from commands.workflow.modules import get_ws_name

        asset_data = get_ws_name.from_asset_name(id, cls._get_ws_type("model"))
        workspace = asset_data.workspace

        # workspaceの末端の階層名がply0000_basemodelに値するので取得
        text = str(workspace).rsplit("\\", 1)[-1]

        pattern = r"\w{3}\d{4}_(.*)"
        match = re.match(pattern, text)
        # 開発名称がない場合空の文字列が返ってくるのでraise
        if match.groups()[0] == "":
            raise ValueError(
                "Development name is not set. Please set the development name on shotgrid and try again."
            )
        return asset_data

    @classmethod
    def get_anim_fbx_path(cls, file_name: str):
        pattern = re.compile(r".*([a-z]{3}\d{4}).*")
        id = re.findall(pattern, file_name)[0]
        asset_data = cls._get_asset_data(id)
        fbx_path = str(asset_data.workspace).replace("characters", "animations")

        fbx_path = fbx_path + "\\fbx"

        return fbx_path

    @classmethod
    def get_skeleton_name(cls, UI) -> str:
        """骨の名前を取得

        Returns:
            str: UIから、対象となる骨名
        """
        try:
            create_skeleton = UI.is_create_skeleton_cbox.isChecked()
            if create_skeleton:
                skeleton_name = UI.skeleton_name_txt.text()
            else:
                skeleton_name = UI.skeleton_cmbbox.currentText()
            return skeleton_name
        except:
            return UI.skeleton_cmbbox.currentText()

    @classmethod
    def get_sk_uaaset_path(cls, fbx_path: str) -> str:
        """skのuassetのインポート先のパスを取得
        Returns:
            str: ファイルパス
        """
        file_name = os.path.basename(fbx_path)

        # 正規表現パターンを作成
        pattern = re.compile(r".*([a-z]{3}\d{4}).*")
        id = re.findall(pattern, file_name)[0]

        asset_data = cls._get_asset_data(id)

        if asset_data == None:
            return None

        asset_path = str(asset_data.enginespace)

        # 実際にインポートする階層は/Mesh
        asset_path = asset_path + "\\Mesh\\"

        # 相対pathをGamePathに変換
        asset_path = asset_path.replace(
            "C:\\cygames\\shrdev\\shr\\project\\ShenronProto\\Content\\", "\\Game\\"
        )

        return asset_path.replace("\\", "/")

    @classmethod
    def get_absolute_path(cls, asset_path):

        asset_path = asset_path.replace("\\", "/")
        asset_path = asset_path.replace(
            "/Game/", "C:/cygames/shrdev/shr/project/ShenronProto/Content/"
        )
        return asset_path

    @classmethod
    def get_anim_uasset_path(cls, fbx_path: str) -> str:
        """アニメーションシーケンスのuassetのインポート先のパスを取得
        Returns:
            str: ファイルパス
        """
        file_name = os.path.basename(fbx_path)

        # 正規表現パターンを作成
        pattern = re.compile(r".*([a-z]{3}\d{4}).*")

        id = re.findall(pattern, file_name)[0]

        asset_data = cls._get_asset_data(id)

        if asset_data == None:
            return None

        # キャラクターのパスから生成
        asset_path = str(asset_data.enginespace).replace("Characters", "Animations")

        # 実際にインポートする階層は/AnimationSequence
        asset_path = asset_path + "/AnimationSequence/"

        # 相対pathをGamePathに変換
        asset_path = asset_path.replace(
            "C:\\cygames\\shrdev\\shr\\project\\ShenronProto\\Content\\", "\\Game\\"
        )

        return asset_path.replace("\\", "/")


class ue_importer:
    @classmethod
    def sk_uasset_import(
        cls,
        create_skeleton: bool,
        skeleton_name: str,
        export_paths: list,
    ) -> None:
        for i, fbx_path in enumerate(export_paths):
            import_path = ue_gui_utils.get_sk_uaaset_path(fbx_path)  # + fbx_file_name

            if not fbx_path.endswith(".fbx"):
                fbx_path += ".fbx"
            job_name = ""

            if create_skeleton:
                job_name = "skeleton"
            else:
                job_name = "skeletal_mesh"

            job_info = {
                "job_name": job_name,
                "fbx_path": fbx_path,
                "ue_path": import_path,
                "target_skeleton": "{0}{1}.{1}".format(SHR_SKEL_PATH, skeleton_name),
            }

            # try:
            Client().run_file("import_asset", [job_info])

    @classmethod
    def anim_uasset_import(cls, skeleton_name: str, fbx_path: str) -> None:
        import_path = ue_gui_utils.get_anim_uasset_path(fbx_path)
        job_info = {
            "job_name": "animation",
            "fbx_path": fbx_path,
            "ue_path": import_path,
            "target_skeleton": "{0}{1}.{1}".format(SHR_SKEL_PATH, skeleton_name),
        }
        # try:
        Client().run_file("import_asset", [job_info])
