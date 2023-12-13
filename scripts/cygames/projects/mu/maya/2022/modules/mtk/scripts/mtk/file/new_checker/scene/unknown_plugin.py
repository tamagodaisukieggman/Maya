import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

import maya.cmds as cmds
from .. import scene_data

skip_plugins = [
    "stereoCamera",
    "mtoa",
]

def check(data_type="", scene_path="", node=None):

    _result_datas = scene_data.ResultDatas()
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

            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = f"[ {unknown_pluging} ] がある"
            _result.error_nodes = [unknown_pluging]

            if _result.error:
                _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""

    try:
        cmds.unknownPlugin(node, r=True)
        message = f"[ {node} ] を削除"
        success = 1
    except Exception as e:
        message = f"[ {node} ] が消せない"
        success = 0

    return success, message