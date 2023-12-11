import typing as tp
import maya.cmds as cmds
import os


from .. import utils as chara_utils
from ....common.maya_checker import utility as utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType


class Wiz2MaterialName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "マテリアル名"

    def exec_task_method(self):
        self.set_error_type(ErrorType.NOERROR)

        self.register_error_info_to_mesh_descendants(
            self.check_all_material_names, "wiz2_material_name", "マテリアル名に誤りがある"
        )

    def check_all_material_names(self, objects: tp.List):
        shapes = utils.get_shapes(objects)
        materials = utils.get_assigned_material(shapes)
        invalid_material_names = []
        for material in materials:
            if not self.check_material_name_pattern(material):
                invalid_material_names.append(material)
        return invalid_material_names

    def check_material_name_pattern(self, material: str) -> bool:
        """input_stringの値を該当するマテリアル名に当たるか調べる

        Args:
            input_string (str): _description_

        Returns:
            bool: 該当するマテリアル名に当たるかどうか
        """

        is_valid_material = False

        scene_name_info = chara_utils.get_current_scene_info(self.maya_scene_data)
        body_type = scene_name_info["body_type"][0]
        element_naming_rules = chara_utils.get_character_info()[
            "irregular_naming_rules"
        ]

        material_name = f"mt_{self.maya_scene_data.basename}"

        irragular_suffix = ["a", "p"]
        for suffix in irragular_suffix:
            if material.endswith(f"_{suffix}"):
                material = material.rsplit("_", 1)[0]

        temp_material_name = ""
        is_valid_material = False
        if material_name != material:
            temp_material_name = material_name
            if body_type in element_naming_rules:
                irregular_parts = element_naming_rules[body_type]
                for parts_name in irregular_parts:
                    # 今のところlegだけ特殊処理
                    if parts_name == "leg":
                        temp_material_name = f"mt_{self.maya_scene_data.basename[:2]}_l_socks"
                        irregular_material_name = temp_material_name
                    else:
                        irregular_material_name = f"{material_name}_{parts_name}"
                    if irregular_material_name == material:
                        is_valid_material = True
        else:
            is_valid_material = True

        return is_valid_material

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
        if not texture_path or not texture_path.lower().endswith(".tga"):
            print("{} is not assigned a TGA texture.".format(file_node))
            return [-1, -1]
        if not os.path.isfile(texture_path):
            print("Texture file not found: {}".format(texture_path))
            return [-1, -1]
        # outSize アトリビュートから解像度を取得する
        width = cmds.getAttr(file_node + ".outSizeX")
        height = cmds.getAttr(file_node + ".outSizeY")
        return [width, height]
