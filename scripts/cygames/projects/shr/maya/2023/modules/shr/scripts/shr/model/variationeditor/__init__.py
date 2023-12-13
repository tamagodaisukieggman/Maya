# -*- coding: utf-8 -*-
from tatool.log import ToolLogging, Stage



TITLE = "Variation Editor"
NAME = "{}".format("".join(TITLE.split()))

project = "mutsunokami"

TOOL_NAME = "{} {}".format(project, TITLE)


tool_category = "Maya"
tool_version = 'v2021.05.07'

tool_logging = ToolLogging(
                        projects=project,
                        toolcategory=tool_category,
                        target_stage=Stage.dev,
                        tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)
