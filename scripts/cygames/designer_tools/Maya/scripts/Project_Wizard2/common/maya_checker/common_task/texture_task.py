import os
import typing as tp
import functools
import maya.cmds as cmds

from ...maya_checker import utility as utils

from ..task import CheckTaskBase
from ..scene_data import MayaSceneDataBase
from ..data import ErrorType


class TextureExtension(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "テクスチャ拡張子"

        if self.extra_data == None:
            raise ValueError(f"{self.checker_info.label_name}:にはextradataが必要です")

        self.extension = self.extra_data["extension"]

    def exec_task_method(self):
        current_func = functools.partial(self.get_non_tga_file_multiple)
        self.register_error_info_to_mesh_descendants(
            current_func,
            "texture_extension",
            f"{str(self.extension)}ではない拡張子のfileノード",
        )

    @staticmethod
    def get_assigned_materials(objects: tp.List[str]):
        materials = set()

        for obj in objects:
            shading_groups = cmds.listConnections(obj, type="shadingEngine")
            if not shading_groups:
                continue

            for sg in shading_groups:
                connected_materials = cmds.ls(cmds.listConnections(sg), materials=True)
                if connected_materials:
                    materials.update(connected_materials)

            # フェースにアサインされているマテリアルを取得
            num_faces = cmds.polyEvaluate(obj, face=True)
            for i in range(num_faces):
                face = "{}.f[{}]".format(obj, i)
                shading_group = cmds.listConnections(face, type="shadingEngine")
                if shading_group:
                    connected_material = cmds.ls(
                        cmds.listConnections(shading_group), materials=True
                    )
                    if connected_material:
                        materials.update(connected_material)

        return list(materials)

    @staticmethod
    def get_file_nodes(material: str) -> tp.List[str]:
        """マテリアルにアサインされているすべてのfileノードを取得する関数

        Args:
            material (str): マテリアル名

        Returns:
            tp.List[str]: fileノード名のリスト
        """
        file_nodes = cmds.listConnections(material, type="file")
        return file_nodes if file_nodes else []

    @staticmethod
    def check_non_tga_file_nodes(file_nodes: tp.List[str]) -> tp.List[str]:
        """与えられたすべてのfileノードからテクスチャのパスを取得し、拡張子がtga以外のパスで終わるfileノードをすべて戻り値で返す関数

        Args:
            file_nodes (tp.List[str]): fileノード名のリスト

        Returns:
            tp.List[str]: 拡張子がtga以外のパスで終わるfileノード名のリスト
        """
        non_tga_file_nodes = []
        for file_node in file_nodes:
            texture_path = cmds.getAttr(file_node + ".fileTextureName")
            _, ext = os.path.splitext(texture_path)
            if ext.lower() != ".tga":
                non_tga_file_nodes.append(file_node)
        return non_tga_file_nodes

    def get_non_tga_file_multiple(self, objects: tp.List[str]):
        # トランスフォームの配列から各トランスフォームが所有するshapeを取得する
        objects = utils.get_shapes(objects)
        files = []
        # for object in objects:
        obj_material = self.get_assigned_materials(objects)
        if obj_material:
            file_nodes = self.get_file_nodes(obj_material)
            non_tga_file_nodes = self.check_non_tga_file_nodes(file_nodes)
            files.extend(non_tga_file_nodes)
        return list(set(files))


class TextureFilterType(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "テクスチャのfilterType"

    def exec_task_method(self):
        current_func = functools.partial(self.check_texture_filter)
        self.register_error_info_to_mesh_descendants(
            current_func,
            "texture_filter_type",
            f"テクスチャのfilterTypeがQuadraticではないオブジェクト",
            error_type=self.error_type,
        )

    def exec_fix_method(self):
        error_objects = self.get_debug_target_objects("texture_filter_type")
        TextureFilterType.change_filterType_to_quadratic(error_objects)

    @staticmethod
    def change_filterType_to_quadratic(file_nodes: tp.List[str]) -> None:
        """
        対象のfileノードのアトリビュートのfilterTypeがQuadratic以外ならQuadraticに変更する関数
        Args:
            file_nodes (List[str]): 対象のfileノードのリスト
        Returns: なし
        """
        for node in file_nodes:
            if cmds.nodeType(node) == "file":
                filter_type = cmds.getAttr(node + ".filterType")
                if filter_type != "Quadratic":
                    cmds.setAttr(node + ".filterType", 3)

    @staticmethod
    def check_non_quadratic_filter_type(file_nodes: tp.List[str]) -> tp.List[str]:
        """与えられたすべてのfileノードからFilterTypeを取得し、FilterTypeがQuadraticになっていないものを配列で返す関数

        Args:
            file_nodes (tp.List[str]): fileノード名のリスト

        Returns:
            tp.List[str]: FilterTypeがQuadraticになっていないfileノード名のリスト
        """
        non_quadratic_file_nodes = []
        for file_node in file_nodes:
            filter_type = cmds.getAttr(file_node + ".filterType")
            if filter_type != 3:  # 3 is the value for the Quadratic filter type
                non_quadratic_file_nodes.append(file_node)
        return non_quadratic_file_nodes

    def check_texture_filter(self, objects: tp.List[str]):
        non_quadratic_file_nodes = []
        objects = utils.get_shapes(objects)
        for object in objects:
            obj_material = utils.get_assigned_material([object])
            if obj_material:
                file_nodes = utils.get_file_nodes(obj_material)
                non_quadratic_file_nodes = self.check_non_quadratic_filter_type(
                    file_nodes
                )
        return non_quadratic_file_nodes
