# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tatool.log import ToolLogging, Stage


TITLE = "Easy Bind"
NAME = "{}_ui".format("_".join(TITLE.lower().split()))

project = "mutsunokami"

TOOL_NAME = "{} {}".format(project, TITLE)


tool_category = "Maya"

tool_version = 'v2021.11.22'
# モデルがリファレンスの際に正しくウェイトが読み書きできない問題の解決

# tool_version = 'v2021.08.23'
# ヘルプ追加

# tool_version = 'v2021.05.20'
# ウェイト転送にリジッドモード追加

# tool_version = 'v2021.04.27'
# # CNP を除外インフルエンスに追加

# tool_version = 'v2021.04.12'


tool_logging = ToolLogging(
                        projects=project,
                        toolcategory=tool_category,
                        target_stage=Stage.dev,
                        tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)
