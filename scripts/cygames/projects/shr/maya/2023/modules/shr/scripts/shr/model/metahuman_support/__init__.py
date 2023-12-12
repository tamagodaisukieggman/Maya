from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging
from tatool import log


TITLE = "Metahuman Support"
NAME = "{}".format("_".join(TITLE.lower().split()))

project = "shenron"

TOOL_NAME = "{} {}".format(project, TITLE)

tool_category = "Maya"
tool_version = 'v2023.05.17'


tool_title = TITLE
stage = log.Stage.development

logger = log.getToolLogger(
    tool_title=tool_title,
    projects=project,
    tool_category=tool_category,
    target_stage=log.Stage.development,
    tool_version=tool_version
)

if os.getenv('PRJ_MAYA_DEBUG'):
    # 環境変数でデバッグが有効になっていると、ログもDEBUGレベルに設定
    logger.setLevel(logging.DEBUG)
