from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # if maya_scene_data.current_category == 'ANIMATION' or maya_scene_data.current_category == 'RIG':
    #     return

    checker.result.color = [10, 10, 10]

    NEED_LAYERS: list = maya_scene_data.current_project_setting.get('NOT_DELETE_DISPLAY_LAYER')
    DEFAULT_LAYER_NAME: str = maya_scene_data.current_project_setting.get('DEFAULT_LAYER_NAME')

    layers = [x for x in cmds.ls(type="displayLayer") if not x.startswith(DEFAULT_LAYER_NAME)]

    if layers:
        for layer in layers:
            if NEED_LAYERS and layer in NEED_LAYERS:
                continue
            checker.result.error_nodes.append(layer)
            checker.result.error_message_list.append(f"Exists [ {layer} ]")

    if DEFAULT_LAYER_NAME:
        default_layer = cmds.ls(f"{DEFAULT_LAYER_NAME}*", type="displayLayer")
        if not default_layer:
            checker.result.error_nodes.append('')
            checker.result.error_message_list.append(f'Not Exists [ {DEFAULT_LAYER_NAME} ]')



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
