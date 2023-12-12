from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

import maya.cmds as cmds
from .. import scene_data
from .. import settings


def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:str='')->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    all_node_type = cmds.allNodeTypes()
    delete_node_type:list = settings.load_config(config_name='DELETE_TARGET_NODE_TYPE')

    delete_node_type_exists:list = []
    delete_node_end_name:list = settings.load_config(config_name='DELETE_TARGET_NODE_NAME_END')
    delete_node_start_name:list = settings.load_config(config_name='DELETE_TARGET_NODE_NAME_START')

    for _del in delete_node_type:
        if _del in all_node_type:
            delete_node_type_exists.append(_del)

    if delete_node_type_exists:
        delete_nodes:list = cmds.ls(type=delete_node_type_exists)

    delete_name_nodes:list = []

    if delete_node_end_name:
        for _node_end_name in delete_node_end_name:
            _nodes = cmds.ls(f'*{_node_end_name}')
            if _nodes:
                delete_name_nodes.extend(_nodes)

    if delete_node_start_name:
        for _node_start_name in delete_node_start_name:
            _nodes = cmds.ls(f'{_node_start_name}*')
            if _nodes:
                delete_name_nodes.extend(_nodes)

    if delete_name_nodes:
        delete_nodes.extend(delete_name_nodes)

    for _node in delete_nodes:
        _result = scene_data.ResultData()
        _result.error_type_message = ERROR
        _result.checker_module = CHECKER
        _result.checker_category = CATEGORY
        _result.data_type_category = data_type_category
        _result.error_text = f"Exists [ {_node} ]"
        _result.error_nodes = [_node]
        _result.error_type_color = [10, 10, 50]

        if _result.error_type_message:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    if isinstance(modify_targets, str):
        modify_targets = eval(modify_targets)
    if not modify_targets:
        return success, message

    for modify_target in modify_targets:
        try:
            cmds.lockNode(modify_target, lock=False)
            cmds.delete(modify_target)
            message = f"Delete [ {modify_target} ]"
            success = 1
        except Exception as e:
            message = f"Could Not Delete [ {modify_target} ]"
            success = 0

    return success, message