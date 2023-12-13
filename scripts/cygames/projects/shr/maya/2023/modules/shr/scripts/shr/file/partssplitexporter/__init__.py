from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tatool.log import ToolLogging, Stage


TITLE = "Parts Split Exporter"
NAME = "{}".format("".join(TITLE.split()))


project = "mutsunokami"

TOOL_NAME = "{} {}".format(project, TITLE)

PRESET_NAME = "Parts_Scene"
NODE_CHILDREN = "NodeChildren"
GROUP_ROOTNODES = "GroupRootNodes"

UPPER_BODY = "upper_body"
LOWER_BODY = "lower_body"
BODY_NAMES = [UPPER_BODY, LOWER_BODY]
SKL_PELVIS_C = "skl_pelvis_C"

ROOT_JOINT = "jnt_0000_skl_root"
MODEL_GROUP = "model"

TEMP_NODE = "{}_temp_group".format(NAME)

tool_category = "Maya"


tool_version = 'v2021.08.06'
# リリース


tool_logging = ToolLogging(
                        projects=project,
                        toolcategory=tool_category,
                        target_stage=Stage.dev,
                        tool_version=tool_version)

logger = tool_logging.getTemplateLogger(TOOL_NAME)

