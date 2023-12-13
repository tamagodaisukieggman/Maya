from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    skip_plugins: list = maya_scene_data.current_project_setting.get('NOT_DELETE_PLUGIN_NODE')
    unknown_plugings = cmds.unknownPlugin(query=True, list=True)

    checker.result.color = [10, 10, 50]

    if unknown_plugings:
        for unknown_pluging in unknown_plugings:
            skip_flag = False
            if skip_plugins:
                for skip_plugin in skip_plugins:
                    if unknown_pluging.startswith(skip_plugin):
                        skip_flag = True
                        break
            if skip_flag:
                continue
            checker.result.error_nodes.append(unknown_pluging)
            checker.result.error_message_list.append(f'Exists {unknown_pluging}')




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
