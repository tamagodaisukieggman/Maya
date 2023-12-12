import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

import maya.cmds as cmds
from .. import scene_data

PLUGIN_NODES = ["ngSkinTools*"]
NODE_TYPES = [
        "ngst2SkinLayerData",
        "ngst2MeshDisplay",
        ]


def check(data_type="", scene_path="", node=None):
    _result_datas = scene_data.ResultDatas()
    _result = scene_data.ResultData()

    # if data_type != "chara":
    #     return

    plugin_nodes = cmds.ls(type=NODE_TYPES)
    if plugin_nodes:
        _result.error = ERROR
        _result.category = CATEGORY
        _result.data_type = data_type
        _result.error_text = f"Exists [ {plugin_nodes} ]"
        _result.error_nodes = plugin_nodes

    if _result.error:
        _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message