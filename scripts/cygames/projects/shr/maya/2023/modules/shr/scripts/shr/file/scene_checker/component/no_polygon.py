from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if maya_scene_data.current_category == 'ANIMATION':
        return

    checker.result.color = [205, 51, 51]

    ATTRIBUTE_NUMBER_OF_DIGITS: list = maya_scene_data.current_project_setting.get('ATTRIBUTE_NUMBER_OF_DIGITS')
    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node: data.CustomNodeData = node
            if not node.shapes:
                continue
            for shape in node.shapes:
                shape: data.CustomNodeData = shape
                bb_size = cmds.polyEvaluate(shape.full_path_name, boundingBox=True, accurateEvaluation=True)
                bb_size = [[round(x[0], ATTRIBUTE_NUMBER_OF_DIGITS), round(x[1], ATTRIBUTE_NUMBER_OF_DIGITS)] for x in bb_size]
                if bb_size == ((0.0, 0.0), (0.0, 0.0), (0.0, 0.0)):
                    checker.result.error_nodes.append(shape.full_path_name)
                    checker.result.error_message_list.append('Not Exists Meshes')
                    check_result.no_polygon_mesh.append(shape.full_path_name)


def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    pass
