# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from tatool.log import ToolLogging, Stage


TITLE = "Variation Model Changer"
NAME = "{}_ui".format("_".join(TITLE.lower().split()))

project = "mutsunokami"

TOOL_NAME = "{}".format("".join(TITLE.split()))


tool_category = "Maya"


tool_version = 'v2021.10.19'
# シーンに読み込まれた複数リファレンスに対応

# tool_version = 'v2021.05.28'

tool_logging = ToolLogging(
                        projects=project,
                        toolcategory=tool_category,
                        target_stage=Stage.dev,
                        tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)



DEFAULT_REFERENCE_NAME = "ply00_m_000_000:mdl_ply00_m_000RN"
DEFAULT_REFERENCE_PATH = "Z:/mtk/work/resources/characters/player/00/000/model/mdl_ply00_m_000.ma"

MTK_ROOT_PATH = "Z:/mtk/work/resources"
THUMBNAIL_ROOT_PATH = "Z:/mtk/.cas/p4/meta-extra/original/resources"
CHARACTER_DIR_NAME = "characters"
CHARACTER_MODEL_ROOT_PATH = os.path.join(MTK_ROOT_PATH, CHARACTER_DIR_NAME)

CY_THUMBNAIL_EXT = ".mdli.cy-asset-prv"

EXT_DICT = {
    "ma": "mayaAscii",
    "mb": "mayaBinary"
}