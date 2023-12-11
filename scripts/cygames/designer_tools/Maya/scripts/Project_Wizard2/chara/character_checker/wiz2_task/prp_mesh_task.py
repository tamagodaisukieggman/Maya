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

        has_error, has_error_targets, reset_message = self.get_check_poly_count_results(current_max_count)

        if has_error == True:
            self.set_error_data(
                f"wiz2_prop_poly_count",
                has_error_targets,
                f"prop の規定ポリゴン数({current_max_count})を超えています",
                is_reset_debug_data=reset_message,
            )

        elif has_error == False:
            self.set_error_type(ErrorType.NOERROR)

    