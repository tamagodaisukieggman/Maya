import os
import typing as tp
import maya.cmds as cmds


from .. import utils as chara_utils
from ....common.maya_checker import utility as utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType

class Wiz2ProTextureResolution(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "テクスチャ解像度"

    def exec_task_method(self):
        self.set_error_type(ErrorType.NOERROR)

        self.register_error_info_to_mesh_descendants(
            self.check_all_texture_resolution,
            "wiz2_pro_texture_resolution",
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

        error_files = []

        for material in materials:
            file = utils.get_file_nodes([material])[0]
            if not self._check_file_resolution([1024,1024], file):
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
        resolutions = Wiz2ProTextureResolution.get_tga_resolution(file)
        for res,def_res in zip(resolutions,def_resolution):
            if def_res < res:
                return False 
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
