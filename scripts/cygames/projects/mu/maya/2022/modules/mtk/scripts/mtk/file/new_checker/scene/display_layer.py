import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data

NEED_LAYERS = [
    "model_objLay",
    "bind_joints_objLay",
    "rig_objLay"
]

DEFAULT_LAYER_NAME = "defaultLayer"


def check(data_type="", scene_path="", node=None):

    # 背景では特に問題が起きていないので消さない
    if data_type == "env":
        return

    _result_datas = scene_data.ResultDatas()

    layers = [x for x in cmds.ls(type="displayLayer") if not x.startswith("defaultLayer")]

    if layers:
        for layer in layers:
            _result = scene_data.ResultData()
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = f"[ {layer} ] がある"
            _result.error_nodes = [layer]
            if _result.error:
                _result_datas.set_data_obj(_result)

    default_layer = cmds.ls("defaultLayer*", type="displayLayer")

    if not default_layer:
        _result = scene_data.ResultData()
        _result.error = ERROR
        _result.category = CATEGORY
        _result.data_type = data_type
        _result.error_text = f'[ {DEFAULT_LAYER_NAME} ] がない'
        _result.error_nodes = [""]
        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""

    try:
        cmds.delete(node)
        message = u"[ {} ] を削除".format(node)
        print("{:-<100}  {}".format(node, "delete Node"))
    except Exception as e:
        message = u"!! [ {} ] を削除できない".format(node)
        print("{:+<100}  {}".format(node, "delete Node error"))

    return success, message