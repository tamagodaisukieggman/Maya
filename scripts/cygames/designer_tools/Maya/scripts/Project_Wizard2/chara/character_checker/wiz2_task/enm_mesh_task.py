import typing as tp
import functools
import maya.cmds as cmds
 
from .. import utils as chara_utils
from ....common.maya_checker.data import ErrorType
from ..wiz2_task.chr_mesh_task import Wiz2PolyCount


class Wiz2EnmPolyCount(Wiz2PolyCount):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ポリゴン数"

    def get_current_max_count(self):
        enm_type = chara_utils.parse_current_scene_name(self.maya_scene_data)[1]
        current_max_count = 0
        if enm_type == "b":
            current_max_count = 60000
        elif enm_type == "m":
            current_max_count = 15000
        if current_max_count != 0:
            return current_max_count
        

    def exec_task_method(self):
        current_max_count = self.get_current_max_count()
        enm_type = chara_utils.parse_current_scene_name(self.maya_scene_data)[1]
        enm_type_full = ""
        if enm_type == "b":
            enm_type_full = "boss"
        elif enm_type == "m":
            enm_type_full = "minion"
            
        self.set_error_type(ErrorType.NOERROR)
        print("poly_count_debug_data:")
        has_error, debug_datas = self.get_check_poly_count_results_for_multroot(current_max_count,self.maya_scene_data.root_nodes)
        #current_max_count = 4000
        self.set_error_type(ErrorType.NOERROR)
        has_error, debug_datas = self.get_check_poly_count_results_for_multroot(current_max_count,self.maya_scene_data.root_nodes)
        debug_datas = debug_datas[0]
        print(debug_datas)
        if has_error == True:
            self.error_type = ErrorType.WARNING
            self.set_error_data(
                f"wiz2_enemy_poly_count",
                debug_datas["check_targets"],
                f"enemy の {enm_type_full}  の規定ポリゴン数({current_max_count}tris)を超えています\n現在の合計ポリゴン数は{debug_datas['total_poly_count']}tris です。",
                is_reset_debug_data=True,
            )
        else:
            self.error_type = ErrorType.NOERROR
            self.set_error_data(
                f"wiz2_enemy_poly_count",
                debug_datas["check_targets"],
                f"enemy の {enm_type_full}  の規定ポリゴン数({current_max_count}tris)内です。\n現在の合計ポリゴン数は{debug_datas['total_poly_count']}tris です。",
                is_reset_debug_data=True,
            ) 