from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

from maya import cmds
from .. import scene_data
from .. import settings


def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    for node in check_targets:
        if cmds.getAttr("{}.intermediateObject".format(node)):
            continue

        _result = scene_data.ResultData()

        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)
        # _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            _result.error_type_message = ERROR
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = "Not Exists Meshes"
            _result.error_nodes = [node]
            _result.error_type_color = [10, 10, 10]

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

    for node in modify_targets:
        try:
            # _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]
            cmds.delete(node)
            success = 1
            message = f'[ {node} ] delete Node'
            # print("{:-<100}  {}".format(node, "delete Node"))
        except Exception as e:
            success = 0
            message = f'[ {node} ] delete Node error'
            # print("{:+<100}  {}".format(node, "delete Node error"))
    return success, message