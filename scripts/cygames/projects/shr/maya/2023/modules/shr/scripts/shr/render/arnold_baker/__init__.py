# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import sys

from tatool.log import ToolLogging, Stage


TITLE = "Map Baker Arnold"
NAME = "{}_ui".format("_".join(TITLE.lower().split()))

project = "mutsunokami"

TOOL_NAME = "{}{}".format(project.capitalize(), "".join(TITLE.split()))
AUTOMATION_TOOL_KIT = "Z:/mtk/tools/standalone/substance_automation_toolkit"

#PYSBS = "Z:/mtk/tools/maya/python/python27-64/lib/site-packages"
PYSBS = "Z:/mtk/tools/standalone/substance_automation_toolkit/Python API/site-packages"

if PYSBS not in sys.path:
    sys.path.append(PYSBS)

tool_version = 'v2021.05.12'

# imageMagick のcrop サイズ修正
tool_version = 'v2021.06.24'


tool_logging = ToolLogging(
                        projects=project,
                        toolcategory="Maya",
                        target_stage=Stage.dev,
                        tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)

RESOLUTIONS_DICT = {
    32      :5,
    64      :6,
    128     :7,
    256     :8,
    512     :9,
    1024    :10,
    2048    :11,
    4096    :12,
    8192    :13,
}

