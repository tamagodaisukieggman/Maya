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


class Wiz2EnmJointCount(JointCount):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ジョイント総数"

    def _get_max_count(self):
        enm_type = chara_utils.parse_current_scene_name(self.maya_scene_data)[1]
        if enm_type == "b":
            max_count = 160
        elif enm_type == "m":
            max_count = 110
        
        return max_count