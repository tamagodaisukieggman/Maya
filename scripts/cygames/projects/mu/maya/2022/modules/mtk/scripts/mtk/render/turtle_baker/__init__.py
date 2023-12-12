# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import sys

from tatool.log import ToolLogging, Stage


TITLE = "Map Baker Truetle"
# NAME = "{}_ui".format("_".join(TITLE.lower().split()))
NAME = "{}".format("_".join(TITLE.lower().split()))

project = "mutsunokami"

# TOOL_NAME = "{}{}".format(project.capitalize(), "".join(TITLE.split()))
# TOOL_NAME = "{} {}".format(project, TITLE)
TOOL_NAME = "Mtk_MapBaker"

tool_version = 'v2021.12.14'
# AO の頂点カラーベイク時に法線の許容値を追加

# tool_version = 'v2021.12.10'
# 頂点カラーのベイクが汚くなる原因調査
# フィルタのサンプルサイズ変更

# AO のuniformSampling を0 に変更
# 貰ったサンプルシーンではこの設定の方がきれいになったので変更
# tool_version = 'v2021.07.19'

# tool_version = 'v2021.07.13'

tool_logging = ToolLogging(
                        projects=project,
                        toolcategory="Maya",
                        target_stage=Stage.dev,
                        tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)

