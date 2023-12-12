from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

import importlib
importlib.reload(data)

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if(maya_scene_data.current_category == 'ANIMATION' or
       maya_scene_data.current_category == 'ENVIRONMENT'):
        return

    checker.result.color = [40, 80, 90]
    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            # if node.full_path_name in check_result.skining_geometory:
            #     continue
            if node.shapes:
                for shape in node.shapes:
                    # if cmds.getAttr(f"{shape.full_path_name}.intermediateObject") and shape.full_path_name not in checker.result.error_nodes:
                    # print(shape, cmds.getAttr(f"{shape.full_path_name}.intermediateObject"))
                    if cmds.getAttr(f"{shape.full_path_name}.intermediateObject"):
                        if not node.full_path_name in check_result.skining_geometory:
                            checker.result.error_nodes.append(shape.full_path_name)
                            checker.result.error_message_list.append('Intermediate Object')

                        if shape.full_path_name not in check_result.intermediate_objects:
                            check_result.intermediate_objects.append(shape.full_path_name)





def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    pass
