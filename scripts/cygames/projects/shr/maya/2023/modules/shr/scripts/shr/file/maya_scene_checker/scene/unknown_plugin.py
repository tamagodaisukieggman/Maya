from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

import maya.cmds as cmds
from .. import scene_data
from .. import settings


def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    skip_plugins:list = settings.load_config(config_name='NOT_DELETE_PLUGIN_NODE')
    unknown_plugings = cmds.unknownPlugin(query=True, list=True)

    if unknown_plugings:
        for unknown_pluging in unknown_plugings:
            skip_flag = False
            for skip_plugin in skip_plugins:
                if unknown_pluging.startswith(skip_plugin):
                    skip_flag = True
                    break
            if skip_flag:
                continue
            _result = scene_data.ResultData()

            _result.error_type_message = ERROR
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = f"Exists [ {unknown_pluging} ]"
            _result.error_nodes = [unknown_pluging]
            _result.error_type_color = [10, 10, 50]

            if _result.error:
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
            cmds.unknownPlugin(modify_target, remove=True)
            message = f"Delete [ {modify_target} ]"
            success = 1
        except Exception as e:
            message = f"Could Not Delete [ {modify_target} ]"
            success = 0

    return success, message