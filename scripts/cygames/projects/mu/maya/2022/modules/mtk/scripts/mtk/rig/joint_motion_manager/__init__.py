# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tatool.log import ToolLogging, Stage


TITLE = "Joint Motion Manager"
NAME = "{}".format("_".join(TITLE.lower().split()))


project = "mutsunokami"

TOOL_NAME = "{} {}".format(project, TITLE)


tool_category = "Maya"

tool_version = 'v2021.06.10'

tool_logging = ToolLogging(
                        projects=project,
                        toolcategory=tool_category,
                        target_stage=Stage.dev,
                        tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)

