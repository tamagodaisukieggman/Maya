from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

from maya import cmds
from .. import scene_data
from .. import settings


def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    """読み込まれたリファレンスのファイルが見つからないものを検査

    Args:
        data_type (str, optional): [description]. Defaults to "".
        scene_path (str, optional): [description]. Defaults to "".
        node ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    _result_datas = scene_data.ResultDatas()

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    _result_datas = scene_data.ResultDatas()
    _result = scene_data.ResultData()

    _reference_nodes = [x for x in cmds.ls(type='reference',
                                    long=True) if not "sharedReferenceNode" in x]

    if _reference_nodes:
        for _reference_node in _reference_nodes:
            if not cmds.referenceQuery(_reference_node, isNodeReferenced = True):
                continue
            reference_file_path = Path(cmds.referenceQuery(_reference_node, filename = True))

            if not reference_file_path.exists():
                _result.error_type_message = ERROR
                _result.checker_module = CHECKER
                _result.checker_category = CATEGORY
                _result.data_type_category = data_type_category
                _result.error_text = "Not Exists Reference"
                _result.error_nodes = [_reference_node]

    if _result.error_type_message:
        _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    # if isinstance(modify_targets, str):
    #     modify_targets = eval(modify_targets)
    # if not modify_targets:
    #     return success, message

    return success, message