from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if maya_scene_data.current_category == 'ANIMATION':
        return

    checker.result.color = [77, 87, 128]
    message = 'invalid Vertices'

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            if node.full_path_name in check_result.no_polygon_mesh:
                continue
            i_flag = cmds.polyInfo(node, invalidVertices=True)
            if i_flag:
                checker.result.error_nodes.append(node.full_path_name)
                error_compornents = cmds.ls(i_flag, long=True, flatten=True)
                checker.result.error_compornent[f'{message}.{node.full_path_name}'] = error_compornents
                checker.result.error_message_list.append(message)



def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    pass
