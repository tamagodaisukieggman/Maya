from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # if maya_scene_data.current_category == 'ANIMATION' or maya_scene_data.current_category == 'RIG':
    #     return

    checker.result.color = [50, 10, 10]

    skip_nodes = maya_scene_data.current_project_setting.get('CHECK_SKIP_NODE')
    unknown_nodes = cmds.ls(type="unknown")

    if unknown_nodes:
        for unknown_node in unknown_nodes:
            skip_flag = False
            for skip_node in skip_nodes:
                if unknown_node.startswith(skip_node):
                    skip_flag = True
                    break
            if skip_flag:
                continue
            checker.result.error_nodes.append(unknown_node)
            checker.result.error_message_list.append(f"Exists {unknown_node}")


def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    if modify_data and modify_data.error_nodes:
        for node in modify_data.error_nodes:
            if not cmds.objExists(node):
                continue
            try:
                cmds.delete(node)
                modify_result.modify_flag = True
                modify_result.modify_messages.append(f'delete Node {node}')
                print("{:-<100}  {}".format(node, "delete Node"))
            except Exception as e:
                modify_result.error_flag = True
                modify_result.error_messages.append(f'!!Could Not Delete {node}')
                print("{:+<100}  {}".format(node, "delete Node error"))
