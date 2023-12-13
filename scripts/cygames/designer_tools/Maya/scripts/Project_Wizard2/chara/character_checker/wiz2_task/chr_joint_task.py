import typing as tp
import functools

import yaml

import maya.cmds as cmds

from .. import utils as chara_utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.scene_data import MayaSceneDataBase
from ....common.maya_checker import utility
from ....common.maya_checker.data import ErrorType
from ....common.maya_checker.common_task.joint_task import JointCount


class Wiz2JointCount(JointCount):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ジョイント総数"

    def _get_max_count(self):
        scene_name_info = chara_utils.get_current_scene_info(self.maya_scene_data)
        if scene_name_info["body_type"] == "costume":
            max_count = 101
        else:
            max_count = 79
        return max_count


class Wiz2JointStructure(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "骨構造"

    def exec_task_method(self):
        has_error = False
        for i, root in enumerate(self.maya_scene_data.root_nodes):
            gender = self.get_gender(root)
            yaml_path = self.get_current_gender_yaml_path(gender)

            root_joint = None
            for descendent in root.all_descendents:
                if descendent.node_type == "joint":
                    if "Root" in descendent.short_name:
                        root_joint = descendent.full_path_name

            if root_joint:
                error_joints = self.compare_bone_structure_yaml(root_joint, yaml_path)
                is_reset_errordata = False
                if i == 0:
                    is_reset_errordata = True
                if error_joints:
                    self.set_error_data(
                        f"wiz2_joint_structure_{i}",
                        error_joints,
                        f"{root_joint}の骨構造に異なりがあります",
                        is_reset_debug_data=is_reset_errordata,
                    )
                    has_error = True

        if has_error == False:
            self.set_error_type(ErrorType.NOERROR)

    def get_gender(self, root):
        root_name = root.root_node_name
        gender = None
        if root_name in ["p0", "p1"]:
            gender = "men"
        elif root_name == "p2":
            gender = "women"
        return gender

    def get_current_gender_yaml_path(self, gender):
        chr_settings_path = chara_utils.get_chr_settings_directory()

        if gender in ["men", "common"]:
            return chr_settings_path + "/p1_joint_structure.yaml"
        elif gender == "women":
            return chr_settings_path + "/p2_joint_structure.yaml"

    @staticmethod
    def compare_bone_structure_yaml(character_root: str, yaml_file: str) -> bool:
        with open(yaml_file, "r") as yaml_fp:
            yaml_bone_structure = yaml.safe_load(yaml_fp)
        unmatched_bones = []
        Wiz2JointStructure.compare_bone_structure(
            character_root, yaml_bone_structure, unmatched_bones
        )
        return unmatched_bones

    @staticmethod
    def compare_bone_structure(node: str, bone_structure: dict, unmatched_bones: list):
        if not cmds.objExists(node) or not bone_structure:
            return
        node = Wiz2JointStructure.get_short_name(node)

        target_node_name = bone_structure["node"]
        target_node_name = Wiz2JointStructure.get_short_name(target_node_name)

        if node != target_node_name:
            if node not in unmatched_bones:
                unmatched_bones.append(node)

        yaml_children = bone_structure.get("children", [])
        children = sorted(
            [
                child
                for child in (
                    cmds.listRelatives(node, children=True, fullPath=True) or []
                )
                if "|UJ_" not in child
            ]
        )

        if len(yaml_children) != len(children):
            yaml_children_nodes = []
            for yaml_child in yaml_children:
                yaml_children_nodes.append(yaml_child["node"])
            diff = []
            for child in children:
                if child not in yaml_children_nodes and child not in unmatched_bones:
                    diff.append(child)

            unmatched_bones.extend(list(diff))

        for child in children:
            is_match = False

            for yaml_child in yaml_children:
                current_yaml_node = Wiz2JointStructure.get_short_name(
                    yaml_child["node"]
                )
                current_node = Wiz2JointStructure.get_short_name(child)
                if current_node == current_yaml_node:
                    is_match = True
                    Wiz2JointStructure.compare_bone_structure(
                        child, yaml_child, unmatched_bones
                    )
                    continue

            if is_match == False:
                unmatched_bones.append(child)

    @staticmethod
    def get_short_name(node):
        if "|" in node:
            node = node.split("|")[-1]
        return node


class Wiz2JointAttribute(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ベースジョイントの値"

    def exec_task_method(self):
        root_joint_name = "Root"
        has_error = False
        for i, root_node in enumerate(self.maya_scene_data.root_nodes):
            is_reset_errordata = False
            if i == 0:
                is_reset_errordata = True

            target_root_node_name = ""
            gender = self.get_gender(root_node)
            yaml_path = self.get_current_gender_yaml_path(gender)

            for descendent_node in root_node.all_descendents:
                if (
                    descendent_node.node_type == "joint"
                    or descendent_node.short_name == root_joint_name
                ):
                    target_root_node_name = descendent_node.full_path_name

            joints = cmds.listRelatives(target_root_node_name, ad=True, type="joint")
            error_joints = self.compare_nodes_attrs_from_yaml(joints, yaml_path)

            if error_joints:
                self.set_error_data(
                    "wiz2_joint_structure_{i}",
                    error_joints,
                    f"{root_node.root_node_name}のベースジョイントと値が異なります",
                    is_reset_debug_data=is_reset_errordata,
                )
                has_error = True

        if has_error == False:
            self.set_error_type(ErrorType.NOERROR)

    def get_gender(self, root):
        root_name = root.root_node_name
        gender = None
        if root_name in ["p0", "p1"]:
            gender = "men"
        elif root_name == "p2":
            gender = "women"
        return gender

    def get_current_gender_yaml_path(self, gender):
        chr_settings_path = chara_utils.get_chr_settings_directory()
        if gender == "men":
            return chr_settings_path + "/p1_joint_attributes.yaml"
        elif gender == "women":
            return chr_settings_path + "/p2_joint_attributes.yaml"
        elif gender == "common":
            return chr_settings_path + "/p1_joint_structure.yaml"

    @staticmethod
    def compare_nodes_attrs_from_yaml(
        node_names: tp.List[str], yaml_path: str
    ) -> tp.List[str]:
        """複数のノードの属性値を、YAMLファイルで保存された値と比較し、値が異なるノード名のリストを返す関数
        Args:
            node_names (List[str]): 属性を比較するジョイントノードのリスト
            yaml_path (str): 属性値が記録されているYAMLファイルのパス
        Returns:
            tp.List[str]: 値が異なるノード名のリスト
        """
        nodes_with_different_attrs = []
        nodes_with_different_attrs = Wiz2JointAttribute.compare_attrs_from_yaml(
            node_names, yaml_path
        )
        return nodes_with_different_attrs

    @staticmethod
    def compare_attrs_from_yaml(
        node_names: tp.List[str], yaml_path: str
    ) -> tp.List[str]:
        """対象のノードが事前に書き出したyamlのアトリビュート値と等しいかどうか確認する関数
        Args:
            node_name (str): 確認するノードの名前
            yaml_path (str): 属性値が記述されたYAMLファイルのパス
        Returns:
            bool: 属性値が等しいかどうかに応じてTrueまたはFalse
        """
        with open(yaml_path, "r") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        nodes_with_different_attrs = []
        for node_name in node_names:
            if node_name not in yaml_data:
                continue

            attrs = yaml_data[node_name]
            for attr_name, expected_value in attrs.items():
                if not cmds.attributeQuery(attr_name, node=node_name, exists=True):
                    continue

                current_value = cmds.getAttr(f"{node_name}.{attr_name}")
                temp_list = []
                try:
                    if isinstance(current_value, list):
                        for lp in current_value:
                            temp_list.append(list(lp))
                        current_value = temp_list
                except TypeError:
                    ...
                if not Wiz2JointAttribute.compare_value(current_value,expected_value,3):
                    nodes_with_different_attrs.append(f"{node_name}.{attr_name}")

        return nodes_with_different_attrs
    
    @staticmethod
    def round_nested_list(nested_list, n):
        if isinstance(nested_list, list):
            return [Wiz2JointAttribute.round_nested_list(x, n) for x in nested_list]
        elif isinstance(nested_list, float):
            return round(nested_list, n)
        else:
            return nested_list

    @staticmethod
    def compare_value(A, B, n):
        if isinstance(A, list) and isinstance(B, list):
            return Wiz2JointAttribute.round_nested_list(A, n) == Wiz2JointAttribute.round_nested_list(B, n)
        elif isinstance(A, float) and isinstance(B, float):
            return round(A, n) == round(B, n)
        else:
            return A == B

