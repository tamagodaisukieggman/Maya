import os
import typing as tp
import maya.cmds as cmds
import maya.mel as mel


class BoneImporter:
    def __init__(self):
        self.selected_objects = []
        self.root_joint = None
        self.all_joints = []
        self.bound_meshes = []

    def initialize_selected_datas(self):
        """選択したオブジェクトを取得"""
        joints = cmds.ls(sl=True, type="joint")

        if not joints:
            raise ValueError("対象となる骨を選択してください")

        self.root_joint = self.get_root_joint(joints[0])
        self.all_joints = (
            cmds.listRelatives(self.root_joint, ad=True, type="joint") or []
        )
        # 骨からインフルエンスのメッシュを取得
        self.bound_meshes = self.get_bound_meshes(self.all_joints)

    def get_root_joint(self, selected_joint: str) -> str:
        """
        選択した骨関節のルート（根元）を返します。
        Args:
            selected_joint (str): ルートを調査したい骨関節の名前
        Returns:
            str: 選択骨関節のルート骨関節の名前。骨関節が存在しない場合はNoneを返します。
        """
        while True:
            parent_joint = cmds.listRelatives(selected_joint, parent=True)
            if parent_joint is None:
                return selected_joint
            selected_joint = parent_joint[0]

    def get_bound_meshes(self, bones: tp.List[str]):
        """
        指定した複数の骨にバインドされているメッシュをすべて取得します。
        Args:
            bones (List[str]): バインドされているメッシュを探したい骨のリスト
        Returns:
            List[str]: バインドされているメッシュのリスト。バインドされているメッシュがない場合は空のリストを返します。
        """
        bound_meshes = []
        for bone in bones:
            skin_clusters = cmds.listConnections(bone, type="skinCluster")
            if skin_clusters:
                for skin_cluster in skin_clusters:
                    meshes = cmds.listConnections(skin_cluster, type="mesh")
                    if meshes:
                        bound_meshes.extend(meshes)
        return list(set(bound_meshes))

    def get_skin_clusters(self, selected_object: str) -> list:
        """
        選択したオブジェクトのヒストリーからスキンクラスタをすべて取得します。
        Args:
            selected_object (str): スキンクラスタを取得したいオブジェクトの名前
        Returns:
            list: スキンクラスタのリスト。スキンクラスタが存在しない場合は空のリストを返します。
        """
        history = cmds.listHistory(selected_object)
        skin_clusters = cmds.ls(history, type="skinCluster")
        return list(set(skin_clusters))

    def import_fbx(self, file_path: str) -> None:
        """
        指定したファイルパスのFBXファイルをインポートします。
        Args:
            file_path (str): インポートしたいFBXファイルのパス
        Returns:
            None
        """

        # self.set_fbx_import_preset("bone")

        cmds.file(
            file_path,
            i=True,
            type="FBX",
            mergeNamespacesOnClash=False,
            ignoreVersion=True,
            options="v=0;p=17;f=0",
            pr=True,
            ra=True,
            importTimeRange="combine",
        )

        # self.set_fbx_import_preset("animation")

    def get_character_type(self) -> str:
        """現在開いたパスからキャラクターの種類を取得

        Returns:
            str: キャラクターの種類/現在はp1 or p2
        """
        file_name = os.path.basename(cmds.file(sn=True, q=True))
        if file_name.startswith("p1") or file_name.startswith("p0"):
            return "p1"
        elif file_name.startswith("p2"):
            return "p2"
        return None

    def import_fbx_by_character_type(self, character_type: str):
        """キャラクターの種類からfbxをインポートする

        Args:
            character_type (str): キャラクターの種類(p0/p1/p2)
        """
        base_path = "C:/tkgpublic/wiz2/team/3dcg/chr/cmn/bone/basebone01/fbx"
        if character_type == "p1":
            self.import_fbx(f"{base_path}/p1_basebone01.fbx")
        elif character_type == "p2":
            self.import_fbx(f"{base_path}/p2_basebone01.fbx")

    def set_fbx_import_preset(self, preset_type):
        """load presetの設定"""
        if preset_type == "animation":
            preset_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    ".",
                    "chara_animation_import.fbximportpreset",
                )
            ).replace("\\", "/")
            mel.eval('FBXLoadImportPresetFile -f "{}"'.format(preset_path))

        elif preset_type == "bone":
            preset_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), ".", "chara_bone_import.fbximportpreset"
                )
            ).replace("\\", "/")
            mel.eval('FBXLoadImportPresetFile -f "{}"'.format(preset_path))

    def _import_fbx_preset(preset_name: str):
        preset_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), ".", f"{preset_name}.fbximportpreset"
            )
        ).replace("\\", "/")
        mel.eval('FBXLoadImportPresetFile -f "{}"'.format(preset_path))

    def execute(self, is_import_only: bool):
        character_type = self.get_character_type()

        if character_type is None:
            cmds.warning("Character type is not valid")
            return

        # インポートのみであればここで終了
        if is_import_only:
            self.import_fbx_by_character_type(character_type)
            return

        # ターゲットオブジェクトの情報取得
        self.initialize_selected_datas()

        # ウエイトの書き出し
        skin_clusters = self.get_skin_clusters(self.bound_meshes)
        path = os.path.dirname(__file__)
        # path = r"D:\tech-designer\maya_legacy\scripts\Project_Wizard2\chara\chara_bone_importer"
        cmds.deformerWeights(
            "__temp_weight_data.xml", path=path, ex=True, deformer=skin_clusters
        )
        cmds.delete(self.bound_meshes, constructionHistory=True)

        self.import_fbx_by_character_type(character_type)

        for bound_mesh in self.bound_meshes:
            skinCluster = cmds.skinCluster(bound_mesh, *self.all_joints)
            # ウエイトのインポート
            cmds.select(bound_mesh, r=True)
            cmds.deformerWeights(
                "__temp_weight_data.xml",
                im=True,
                method="index",
                deformer=skinCluster[0],
                path=path,
            )
            print(skinCluster)
