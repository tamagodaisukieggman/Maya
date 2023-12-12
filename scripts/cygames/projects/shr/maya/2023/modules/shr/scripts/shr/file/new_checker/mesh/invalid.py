import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data

def check(data_type="env", scene_path="", nodes=None):

    _result_datas = scene_data.ResultDatas()
    for node in nodes:
        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue

        _result = scene_data.ResultData()
        i_flag = cmds.polyInfo(node, invalidVertices=True)

        if i_flag:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "invalidVertices"
            _result.error_nodes = cmds.ls(i_flag, flatten=True)
            _result.error_type_color = [0, 90, 90]
        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message