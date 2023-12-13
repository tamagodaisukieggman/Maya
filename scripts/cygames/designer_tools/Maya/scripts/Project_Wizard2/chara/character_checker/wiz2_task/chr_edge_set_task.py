import typing as tp
import functools

import yaml

import maya.cmds as cmds

from .. import utils as chara_utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.scene_data import MayaSceneDataBase
from ....common.maya_checker import utility
from ....common.maya_checker.data import ErrorType

from ...edge_set_creator.app import EdgeSetChecker, EdgeSetTools
from ...edge_set_creator.data import EdgeSetType


class Wiz2CompareEdgeSet(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "エッジセットの各頂点の値の一致確認"

    def exec_fix_method(self):
        id = "_edge_sets"
        print('')
        edge_sets = cmds.ls(f"*{id}", l=True)
        for edge_set in edge_sets:
            if "|" in edge_set:
                edge_set = edge_set.split("|")[-1]
            current_name = edge_set.replace("_edge_sets", "")

            current_type = self.get_current_type(current_name)
            manager = EdgeSetTools(current_type)
            manager.set_default_value_to_edge()

    def exec_task_method(self):
        id = "_edge_sets"
        edge_sets = cmds.ls(f"*{id}", l=True)
        self.set_error_type(ErrorType.NOERROR)
        for edge_set in edge_sets:
            if "|" in edge_set:
                edge_set = edge_set.split("|")[-1]
            current_name = edge_set.replace("_edge_sets", "")

            current_type = self.get_current_type(current_name)
            checker = EdgeSetChecker(current_type)
            info = checker.get_no_match_vertices()

            no_match_position_vertices = info["position"]

            if no_match_position_vertices:
                self.set_error_data(
                    f"wiz2_{current_name}_position_compare_edge_set",
                    no_match_position_vertices,
                    f"{current_name}のエッジセットのうち、positionが一致しない頂点",
                    is_reset_debug_data=False,
                )

            no_match_normal_vertices = info["normal"]

            if no_match_normal_vertices:
                self.set_error_data(
                    f"wiz2_{current_name}_normal_compare_edge_set",
                    no_match_normal_vertices,
                    f"{current_name}のエッジセットのうち、normalが一致しない頂点",
                    is_reset_debug_data=False,
                )

            no_match_weight_vertices = info["weight"]

            if no_match_weight_vertices:
                self.set_error_data(
                    f"wiz2_{current_name}_weight_compare_edge_set",
                    no_match_weight_vertices,
                    f"{current_name}のエッジセットのうち、weightが一致しない頂点",
                    is_reset_debug_data=False,
                )

    def get_current_type(self, current_name):
        current_type = None
        if current_name == "neck":
            current_type = EdgeSetType.NECK
        elif current_name == "hair":
            current_type = EdgeSetType.HAIR
        elif current_name == "waist":
            current_type = EdgeSetType.WAIST
        return current_type
