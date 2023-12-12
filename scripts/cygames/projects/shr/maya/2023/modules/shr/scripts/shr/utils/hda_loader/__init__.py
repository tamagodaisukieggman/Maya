# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path
# from tatool.log import ToolLogging, Stage


TITLE = "HDA Loader"
NAME = "{}".format("_".join(TITLE.lower().split()))

HDA_PATH = r"C:\cygames\shrdev\shr\tools\in\ext\maya\share\hda"
LOD_CREATE_HDA_NAME = "mtk_lod_create"

project = "shenron"

TOOL_NAME = "{} {}".format(project, TITLE)

tool_category = "Maya"

tool_version = 'v2021.08.06'
# アラインした際のノーマルとそうでない時のノーマル表示を統一


# tool_version = 'v2021.08.05'
# 複数のHDA が存在する場合に正しく動作しなかったバグを修正

# tool_version = 'v2021.08.04'
# リリース



# tool_logging = ToolLogging(
#                         projects=project,
#                         toolcategory=tool_category,
#                         target_stage=Stage.dev,
#                         tool_version=tool_version)

# logger = tool_logging.getTemplateLogger(TOOL_NAME)

INIT_FILE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "houdini_engine_settings.yaml"
