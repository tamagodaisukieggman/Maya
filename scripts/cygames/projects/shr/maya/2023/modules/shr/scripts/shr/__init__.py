import os
import logging
from tatool import log


tool_title = 'Maya Shenron Module'
project = 'shenron'
tool_category = 'Maya'
stage = log.Stage.development
version = 'v2022.6.9'

logger = log.getToolLogger(
    tool_title=tool_title,
    projects=project,
    tool_category=tool_category,
    target_stage=log.Stage.development,
    tool_version=version
)

if os.getenv('PRJ_MAYA_DEBUG'):
    # 環境変数でデバッグが有効になっていると、ログもDEBUGレベルに設定
    logger.setLevel(logging.DEBUG)
