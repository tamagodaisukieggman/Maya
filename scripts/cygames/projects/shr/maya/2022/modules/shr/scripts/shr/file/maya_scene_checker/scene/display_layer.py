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

    NEED_LAYERS:list = settings.load_config(config_name='NOT_DELETE_DISPLAY_LAYER')
    DEFAULT_LAYER_NAME:str = settings.load_config(config_name='DEFAULT_LAYER_NAME')

    # 背景では特に問題が起きていないので消さない
    # if data_type_category == "ENVIRONMENT":
    #     return

    _result_datas = scene_data.ResultDatas()

    layers = [x for x in cmds.ls(type="displayLayer") if not x.startswith(DEFAULT_LAYER_NAME)]

    if layers:
        for layer in layers:
            if layer in NEED_LAYERS:
                continue
            _result = scene_data.ResultData()
            _result.error_type_message = ERROR
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = f"Exists [ {layer} ]"
            _result.error_nodes = [layer]
            if _result.error_type_message:
                _result_datas.set_data_obj(_result)

    default_layer = cmds.ls(f"{DEFAULT_LAYER_NAME}*", type="displayLayer")

    if not default_layer:
        _result = scene_data.ResultData()
        _result.error_type_message = ERROR
        _result.checker_module = CHECKER
        _result.checker_category = CATEGORY
        _result.data_type_category = data_type_category
        _result.error_text = f'Not Exists [ {DEFAULT_LAYER_NAME} ]'
        _result.error_nodes = [""]
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
            cmds.delete(modify_target)
            message = u"Delete [ {} ]".format(modify_target)
            print("{:-<100}  {}".format(modify_target, "delete Node"))
        except Exception as e:
            message = u"!!Could Not Delete [ {} ]".format(modify_target)
            print("{:+<100}  {}".format(modify_target, "delete Node error"))

    return success, message