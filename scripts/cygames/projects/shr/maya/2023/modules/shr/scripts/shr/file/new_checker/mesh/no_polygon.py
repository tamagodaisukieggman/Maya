import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data


def check(data_type="env", scene_path="", nodes=None):

    _result_datas = scene_data.ResultDatas()

    for node in nodes:
        _result = scene_data.ResultData()

        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)
        _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "Not Exists Meshes"
            _result.error_nodes = [_transform_node]
            _result.error_type_color = [10, 10, 10]

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", nodes=None):
    success = -1
    message = ""
    for node in nodes:
        try:
            cmds.delete(node)
            success = 1
            message = f'[ {node} ] delete Node'
            print("{:-<100}  {}".format(node, "delete Node"))
        except Exception as e:
            success = 0
            message = f'[ {node} ] delete Node error'
            print("{:+<100}  {}".format(node, "delete Node error"))
    return success, message