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


class Wiz2ProJointCount(JointCount):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ジョイント総数"

    def _get_max_count(self):
        max_count = 20
        return max_count


class Wiz2ProRootJointAttr(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "Rootのアトリビュート"
    
    def exec_task_method(self):
        error_nodes = []
        for root in self.maya_scene_data.root_nodes:
            target_nodes = []
            for child_node in root.all_descendents:
                if child_node.deep == 1:
                    target_nodes.append(child_node)
        
            for deep_1_node in target_nodes:
                if deep_1_node.node_type == "joint" and deep_1_node.short_name == "Root":
                    if not self.check_default_attributes(deep_1_node.full_path_name):
                        error_nodes.append(deep_1_node.full_path_name)
        has_error = False
        if error_nodes:
            self.set_error_data(
                f"wiz2_pro_root_joint_attr",
                error_nodes,
                f"Rootのアトリビュートが規定値になっていません",
                is_reset_debug_data=True,
            )
            has_error = True

        if has_error == False:
            self.set_error_type(ErrorType.NOERROR)

    @staticmethod
    def check_default_attributes(node):
        transform_attrs = {"translate": (0, 0, 0), "rotate": (0, 0, 0), "scale": (1, 1, 1)}
        others_attrs = {"preferredAngle": (0, 0, 0), "jointOrient": (0, 0, 0)}
        default = True

        for attr, default_values in transform_attrs.items():
            for axis, default_value in zip(['X', 'Y', 'Z'], default_values):
                real_value = cmds.getAttr(node + "." + attr + axis)
                if real_value != default_value:
                    default = False
                    break

        for attr, default_values in others_attrs.items():
            real_values = cmds.getAttr(node + "." + attr)[0]  # getAttr for these attributes returns a list containing one tuple.
            if real_values != default_values:
                default = False
                break

        return default