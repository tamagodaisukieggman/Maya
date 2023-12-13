# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from tatool.log import ToolLogging, Stage


TITLE = "Joint Motion Manager"
NAME = "{}".format("_".join(TITLE.lower().split()))

project = "shenron"

TOOL_NAME = "{} {}".format(project, TITLE)

tool_category = "Maya"

tool_version = 'v2021.06.10'

JOINT_SUFFIX =     "jnt"
HELPER_JOINT =     "drv"
END_JOINT =        "end"
MOTION_POINT =     "mtp"
SIMULATION_JOINT = "sim"
FACE_JIONT =       "fce"

NOT_MOVE_JOINTS = [
                    HELPER_JOINT,
                    END_JOINT,
                    SIMULATION_JOINT,
                ]

JOINT_SUFFIXES = [
                JOINT_SUFFIX,
                HELPER_JOINT,
                END_JOINT,
                SIMULATION_JOINT,
                FACE_JIONT,
                MOTION_POINT,
                ]

# tool_logging = ToolLogging(
#                         projects=project,
#                         toolcategory=tool_category,
#                         target_stage=Stage.dev,
#                         tool_version=tool_version)

# logger = tool_logging.getTemplateLogger(TOOL_NAME)

