import logging
import os

from tatool.log import Stage, ToolLogging

tool_title = 'Maya Mutsunokami Module'
project = 'mutsunokami'
toolcategory = 'Maya'
stage = Stage.pr
version = 'v2021.8.19'

tool_logging = ToolLogging(projects=project,
                           toolcategory=toolcategory,
                           target_stage=stage,
                           tool_version=version)

logger = tool_logging.getTemplateLogger(tool_title)

# マルチカウントインポートによる重複ハンドリングの増加に対応
logger.handlers = []
logger.addHandler(tool_logging.get_streamhandler(tool_title, level=logging.DEBUG))
logger.addHandler(tool_logging.get_fluent_send_handler(tool_title, level=logging.DEBUG))
logger.propagate = False
logger.setLevel(logging.INFO)

if os.getenv('PRJ_MAYA_DEBUG'):
    # 環境変数でデバッグが有効になっていると、ログもDEBUGレベルに設定
    logger.setLevel(logging.DEBUG)
