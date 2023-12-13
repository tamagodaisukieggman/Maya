# -*- coding: utf-8 -*-
import functools
import os
import typing as tp

from ..task import CheckTaskBase
from ..scene_data import MayaSceneDataBase
from ..data import ErrorType

import maya.cmds as cmds
from .. import utility as utils


class MaterialType(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "Materialの種類"

        if self.extra_data == None:
            raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

        self.material_types = self.extra_data["material_types"]

    def exec_task_method(self):
        current_func = functools.partial(
            self._check_specified_materials, material_types=self.material_types
        )
        self.register_error_info_to_mesh_descendants(
            current_func,
            "material_type",
            f"{str(self.material_types)}ではないマテリアルを保有するオブジェクト",
        )

    def _check_specified_materials(
        self, objects: tp.List[str], material_types: tp.List[str]
    ) -> tp.List[str]:
        """対象オブジェクトに使用されているマテリアルの種類が指定されたマテリアルの種類に含まれているか確認する関数

        Args:
            objects (tp.List[str]): 対象オブジェクトのリスト
            material_types (tp.List[str]): チェックするマテリアルの種類のリスト

        Returns:
            tp.List[str]: 指定されたマテリアルの種類に含まれているオブジェクト名の配列
        """
        specified_material_objects = []
        # transformの配列をshapeの配列に変更
        objects = utils.get_shapes(objects)
        for obj in objects:
            shading_groups = cmds.listConnections(obj, type="shadingEngine")
            if shading_groups:
                for sg in shading_groups:
                    materials = cmds.ls(cmds.listConnections(sg), materials=True)
                    for mat in materials:
                        if cmds.nodeType(mat) not in material_types:
                            specified_material_objects.append(obj)
                            break

        return list(set(specified_material_objects))


# class Wiz2MaterialName(CheckTaskBase):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.checker_info.label_name = "マテリアル名"

#     def exec_task_method(self):
#         current_func = functools.partial(self.check_not_bound_object)

#         self.register_error_info_to_mesh_descendants(
#             current_func, "not_bound_object", "バインドされていないオブジェクト"
#         )

#     def get_error_textures(self):
#         materials = utils.get_assigned_material()
#         for material in materials:
#             files = utils.get_file_nodes(material)
#             for file in files:
#                 Wiz2MaterialName.get_tga_resolution(file)

#     @staticmethod
#     def get_tga_resolution(file_node: str) -> tp.List[int]:
#         """
#         fileノードにアサインされているTGAテクスチャの解像度を調べる関数
#         Args:
#             file_node (str): fileノードの名前
#         Returns:
#             [int, int]: テクスチャの解像度（幅x高さ）
#         """
#         # パスを取得
#         texture_path = cmds.getAttr(file_node + ".fileTextureName")
#         if not texture_path or not texture_path.lower().endswith(".tga"):
#             print("{} is not assigned a TGA texture.".format(file_node))
#             return [-1, -1]
#         if not os.path.isfile(texture_path):
#             print("Texture file not found: {}".format(texture_path))
#             return [-1, -1]
#         # outSize アトリビュートから解像度を取得する
#         width = cmds.getAttr(file_node + ".outSizeX")
#         height = cmds.getAttr(file_node + ".outSizeY")
#         return [width, height]
