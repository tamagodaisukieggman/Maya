from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if maya_scene_data.current_category == 'ENVIRONMENT' or maya_scene_data.current_category == 'VAGETATIONS':
        return

    checker.result.color = [77, 100, 128]
    memory_nodes:list = []
    memory_nodes_dict:dict = {}
    for root_node in maya_scene_data.root_nodes:

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue
        for node in root_node.all_descendents:
            if not node.shapes:
                continue
            short_name = node.short_name.rsplit('|', 1)[-1]
            if short_name not in memory_nodes:
                memory_nodes.append(short_name)
                memory_nodes_dict[node.full_path_name] = short_name
            else:
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append('Same Node Name')
                _key = [k for k,v in memory_nodes_dict.items() if v==short_name]
                if _key:
                    checker.result.error_nodes.append(_key[0])
                    checker.result.error_message_list.append('Same Node Name')





def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    pass

