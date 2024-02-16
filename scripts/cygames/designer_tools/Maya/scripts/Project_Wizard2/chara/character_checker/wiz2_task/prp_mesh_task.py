import typing as tp
import functools
import maya.cmds as cmds

from .. import utils
from ....common.maya_checker.data import ErrorType
from ..wiz2_task.chr_mesh_task import Wiz2PolyCount


class Wiz2ProPolyCount(Wiz2PolyCount):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ポリゴン数"

    def exec_task_method(self):
        current_max_count = 2000
        self.set_error_type(ErrorType.NOERROR)

        #for i,root_node in enumerate(self.maya_scene_data.root_nodes):
        has_error, debug_datas = self.get_check_poly_count_results_for_multroot(current_max_count,self.maya_scene_data.root_nodes)
        debug_datas = debug_datas[0]

        if has_error == True:
            self.error_type = ErrorType.WARNING
            self.set_error_data(
                f"wiz2_prop_poly_count",
                debug_datas["check_targets"],
                f"prop の規定ポリゴン数({current_max_count}tris)を超えています\n現在の合計ポリゴン数は{debug_datas['total_poly_count']}tris です。",
                is_reset_debug_data=True,
            )
        else:
            self.error_type = ErrorType.NOERROR
            self.set_error_data(
                f"wiz2_prop_poly_count",
                debug_datas["check_targets"],
                f"prop の規定ポリゴン数({current_max_count}tris)内です。\n現在の合計ポリゴン数は{debug_datas['total_poly_count']}tris です。",
                is_reset_debug_data=True,
            ) 
            

                