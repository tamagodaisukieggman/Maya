from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from tatool.log import ToolLogging, Stage

TITLE = "Houdini Maps Baker for Maya"
NAME = "{}".format("_".join(TITLE.lower().split()))
project = "mutsunokami"
TOOL_NAME = "MtkHoudiniMapsBaker"


tool_version = 'v2021.12.28'


tool_logging = ToolLogging(
    projects=project,
    toolcategory="Maya",
    target_stage=Stage.dev,
    tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)
