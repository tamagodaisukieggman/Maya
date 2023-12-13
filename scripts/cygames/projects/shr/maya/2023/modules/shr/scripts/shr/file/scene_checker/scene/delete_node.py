from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # if maya_scene_data.current_category == 'ANIMATION' or maya_scene_data.current_category == 'RIG':
    #     return

    checker.result.color = [30, 50, 100]

    # ノードタイプでのデリート
    all_node_type = maya_scene_data.all_node_type

    delete_node_type: list = maya_scene_data.current_project_setting.get('DELETE_TARGET_NODE_TYPE')
    if not delete_node_type:
        return

    delete_node_type_exists: list = []

    if delete_node_type:
        for _del in delete_node_type:
            if _del in all_node_type:
                delete_node_type_exists.append(_del)

    if delete_node_type_exists:
        delete_nodes: list = cmds.ls(type=delete_node_type_exists, long=True)
        for delete_node in delete_nodes:
            checker.result.error_nodes.append(delete_node)
            checker.result.error_message_list.append(f"Exists [ {delete_node} ]")



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
