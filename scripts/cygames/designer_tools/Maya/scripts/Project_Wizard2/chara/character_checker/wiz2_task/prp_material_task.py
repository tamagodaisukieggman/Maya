import typing as tp
import maya.cmds as cmds
import os
import re

from .. import utils as chara_utils
from ....common.maya_checker import utility as utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType

class Wiz2ProMaterialName(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "マテリアル名"

    def exec_task_method(self):
        self.set_error_type(ErrorType.NOERROR)

        self.register_error_info_to_mesh_descendants(
            self.check_all_material_names, "wiz2_prop_material_name", "マテリアル名に誤りがある"
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

        return self.check_string_format(material,self.maya_scene_data.basename)


    @staticmethod
    def check_string_format(s: str,scene_name:str) -> bool:
        """対象の文字列が以下の規則になっているかどうかを調べます。
        mt_pro_"gかc"_"自由な文字列""数字2文字"
        Args:
            input_str (str): チェックする対象の文字列
        Returns:
            bool: 指定された規則に従っている場合はTrue、それ以外はFalse
        """
        pattern = f"mt_{scene_name}"
        return pattern == s
