import os
import typing as tp
from pathlib import Path

import maya.cmds as cmds


from .. import utils as chara_utils
from ....common.maya_checker import utility as utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.scene_data import MayaSceneDataBase
from ....common.maya_checker.data import ErrorType


class Wiz2TextureResolution(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "テクスチャ解像度"

    def exec_task_method(self):
        self.set_error_type(ErrorType.NOERROR)

        self.register_error_info_to_mesh_descendants(
            self.check_all_texture_resolution,
            "wiz2_texture_resolution",
            "テクスチャ解像度がレギュレーションと異なる",
        )

    def check_all_texture_resolution(self, objects: tp.List[str]) -> tp.List[str]:
        """全ての解像度に問題のあるテクスチャを返す

        Args:
            objects (tp.List[str]): 対象のオブジェクト

        Returns:
            tp.: _description_
        """
        shapes = utils.get_shapes(objects)
        materials = utils.get_assigned_material(shapes)
        scene_name_info = chara_utils.get_current_scene_info(self.maya_scene_data)
        body_type = scene_name_info["body_type"][0]
        def_texture_resolutions = chara_utils.get_character_info()[
            "texture_resolution"
        ][body_type]

        error_files = []

        # 一つだけならdefaultの解像度が設定対象
        def_resolution = []

        for material in materials:
            suffix = material.rsplit("_", 1)[-1]
            if suffix not in def_texture_resolutions:
                suffix = "default"
            def_resolution = def_texture_resolutions[suffix]
            file = utils.get_file_nodes([material])[0]
            if not self._check_file_resolution(def_resolution, file):
                error_files.append(file)

        return error_files

    def _check_file_resolution(
        self, def_resolution: tp.List[tp.Tuple[int, int]], file: str
    ) -> bool:
        """解像度が定義データと異なるかチェック。異なっていたらfile名を返す

        Args:
            def_resolution (tp.List[int,int]): _description_
            file (str): 対象となるテクスチャ(file)

        Returns:
            bool: 解像度が異なればFalse
        """
        resolutions = Wiz2TextureResolution.get_tga_resolution(file)
        if resolutions != def_resolution:
            return False
        else:
            return True

    @staticmethod
    def get_tga_resolution(file_node):
        """
        fileノードにアサインされているTGAテクスチャの解像度を調べる関数
        Args:
            file_node (str): fileノードの名前
        Returns:
            [int, int]: テクスチャの解像度（幅x高さ）
        """
        # パスを取得
        texture_path = cmds.getAttr(file_node + ".fileTextureName")
        if not os.path.isfile(texture_path):
            print("Texture file not found: {}".format(texture_path))
            return [-1, -1]
        # outSize アトリビュートから解像度を取得する
        width = cmds.getAttr(file_node + ".outSizeX")
        height = cmds.getAttr(file_node + ".outSizeY")
        return [width, height]


class Wiz2TextureLocation(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "テクスチャ階層"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self.get_error_textures,
            "Wiz2TextureLocation",
            "テクスチャーパスが規定の場所にありません",
        )

    def get_valid_sourceimages_path(self):
        current_scene_path = Path(cmds.file(q=True, sn=True))
        sourceimages_path = current_scene_path.parents[1] / "sourceimages"
        return sourceimages_path.as_posix()

    def get_error_textures(self, objects: tp.List[str]):
        shapes = utils.get_shapes(objects)
        materials = utils.get_assigned_material(shapes)
        files = utils.get_file_nodes(materials)
        error_path_files = []
        for file in files:
            texture_paths = self.get_assigned_texture_paths([file])
            for texture_path in texture_paths:
                valid_texture_path = self.get_valid_sourceimages_path()
                if valid_texture_path not in texture_path:
                    error_path_files.append(file)
        return error_path_files

    def get_assigned_texture_paths(self, file_nodes: tp.List[str]):
        """Mayaの全てのfileノードにアサインされているテクスチャのパスを取得する
        Returns:
            List[str]: テクスチャのパスのリスト
        """
        texture_paths = []

        for file_node in file_nodes:
            texture_path = cmds.getAttr(file_node + ".fileTextureName")
            texture_paths.append(texture_path)

        return texture_paths


class Wiz2TextureExist(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "使用されているテクスチャの種類"

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self.get_error_textures,
            "Wiz2TextureLocation",
            '使用されているテクスチャが"_decal"ではありません',
        )

    def get_error_textures(self, objects: tp.List[str]):
        shapes = utils.get_shapes(objects)
        materials = utils.get_assigned_material(shapes)
        files = utils.get_file_nodes(materials)
        error_path_files = []
        for file in files:
            texture_paths = self.get_assigned_texture_paths([file])
            for texture_path in texture_paths:
                basename = os.path.basename(texture_path)
                filename = basename.split(".")[0]
                if not filename.endswith("_decal"):
                    error_path_files.append(file)
        return error_path_files

    def get_assigned_texture_paths(self, file_nodes: tp.List[str]):
        """Mayaの全てのfileノードにアサインされているテクスチャのパスを取得する
        Returns:
            List[str]: テクスチャのパスのリスト
        """
        texture_paths = []

        for file_node in file_nodes:
            texture_path = cmds.getAttr(file_node + ".fileTextureName")
            texture_paths.append(texture_path)

        return texture_paths
