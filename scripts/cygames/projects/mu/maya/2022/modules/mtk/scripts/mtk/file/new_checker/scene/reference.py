import os
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
    """読み込まれたリファレンスのファイルが見つからないものを検査

    Args:
        data_type (str, optional): [description]. Defaults to "".
        scene_path (str, optional): [description]. Defaults to "".
        node ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    _result_datas = scene_data.ResultDatas()
    _result = scene_data.ResultData()

    _reference_nodes = [x for x in cmds.ls(type='reference',
                                    long=True) if "sharedReferenceNode" != x]

    if _reference_nodes:
        for _reference_node in _reference_nodes:
            if not cmds.referenceQuery(_reference_node, isNodeReferenced = True):
                continue
            reference_file_path = cmds.referenceQuery(_reference_node, filename = True)

            if not os.path.exists(reference_file_path):
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = "リファレンスが存在しない"
                _result.error_nodes = [_reference_node]


    if _result.error:
        _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message