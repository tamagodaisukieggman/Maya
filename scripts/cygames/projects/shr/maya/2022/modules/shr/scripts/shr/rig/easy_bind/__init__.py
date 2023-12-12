# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from tatool.log import ToolLogging, Stage


TITLE = "Easy Bind"
NAME = "{}".format("_".join(TITLE.lower().split()))

project = "shenron"

TOOL_NAME = "{} {}".format(project, TITLE)

tool_category = "Maya"

tool_version = 'v2022.11.29'

WEIGHT_FILE_FORMAT = {"xml": ".xml", "json": ".json"}
PROJECT_WEIGHT_FILE_FORMAT = "xml"

# 神田さんからもらった元辞書
JOINT_DISPLAY = {'_jnt':[0, 0,  0, (0,0,0), 0, (0.000,0.000,0.000), 0, 0, (0,0,0)],
                '_drv':[1, 0, 13, (0,0,0), 1, (1.000,0.000,0.000), 0, 0, (0,0,0)],
                '_end':[1, 0, 20, (0,0,0), 1, (1.000,0.690,0.690), 0, 0, (0,0,0)],
                '_sim':[1, 0, 28, (0,0,0), 1, (0.188,0.631,0.631), 0, 0, (0,0,0)],
                '_fce':[1, 0, 23, (0,0,0), 1, (0.000,0.600,0.329), 0, 0, (0,0,0)],
                '_mtp':[1, 0, 21, (0,0,0), 1, (0.784,0.000,0.784), 0, 0, (0,0,0)]
                }

JOINT_SUFFIX =     "jnt"
HELPER_JOINT =     "drv"
END_JOINT =        "end"
MOTION_POINT =     "mtp"
SIMULATION_JOINT = "sim"
FACE_JIONT =       "fce"

ROOT = "root"

JOINT_SUFFIXES = [
                JOINT_SUFFIX,
                HELPER_JOINT,
                END_JOINT,
                SIMULATION_JOINT,
                FACE_JIONT,
                MOTION_POINT,
                ]

JOINT_COLOR_INDEX = {
                    JOINT_SUFFIX:      0,
                    HELPER_JOINT:     13,
                    END_JOINT:        20,
                    SIMULATION_JOINT: 28,
                    FACE_JIONT:       23,
                    MOTION_POINT:     21,
                    }

JOINT_OUTLINER_COLOR = {
                        JOINT_SUFFIX:     (0.000, 0.000, 0.000),
                        HELPER_JOINT:     (1.000, 0.000, 0.000),
                        END_JOINT:        (1.000, 0.690, 0.690),
                        SIMULATION_JOINT: (0.188, 0.631, 0.631),
                        FACE_JIONT:       (0.000, 0.600, 0.329),
                        MOTION_POINT:     (0.784, 0.000, 0.784),
                        }

# モデルがリファレンスの際に正しくウェイトが読み書きできない問題の解決

# tool_version = 'v2021.08.23'
# ヘルプ追加

# tool_version = 'v2021.05.20'
# ウェイト転送にリジッドモード追加

# tool_version = 'v2021.04.27'
# # CNP を除外インフルエンスに追加

# tool_version = 'v2021.04.12'


# tool_logging = ToolLogging(
#                         projects=project,
#                         toolcategory=tool_category,
#                         target_stage=Stage.dev,
#                         tool_version=tool_version)

# logger = tool_logging.getTemplateLogger(TOOL_NAME)
