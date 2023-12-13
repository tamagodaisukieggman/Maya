import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

import maya.cmds as cmds
from .. import scene_data

skip_nodes = [
    "MayaNodeEditorSavedTabsInfo",
    "hyperShadePrimaryNodeEditorSavedTabsInfo",
    "nodeGraphEditorInfo",
]



def check(data_type="", scene_path="", node=None):

    _result_datas = scene_data.ResultDatas()

    # unknown_plugings = cmds.unknownPlugin(query=True, list=True)
    unknown_nodes = cmds.ls(type="unknown")

    if unknown_nodes:
        for unknown_node in unknown_nodes:
            skip_flag = False
            for skip_node in skip_nodes:
                if unknown_node.startswith(skip_node):
                    skip_flag = True
                    break
            # print("skip_flag -----", skip_flag)
            if skip_flag:
                continue

            _result = scene_data.ResultData()

            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = f"[ {unknown_node} ] がある"
            _result.error_nodes = [unknown_node]

            # cmds.lockNode(unknown_node, l=False)
            # try:
            #     cmds.delete(unknown_node)
            #     _result.error = "warning"
            #     _result.category = CATEGORY
            #     _result.data_type = data_type
            #     _result.error_text = f"[ {unknown_node} ] を削除"
            #     _result.error_nodes = [unknown_node]
            # except Exception as e:
            #     _result.error = ERROR
            #     _result.category = CATEGORY
            #     _result.data_type = data_type
            #     _result.error_text = f"[ {unknown_node} ] が消せない"
            #     _result.error_nodes = [unknown_node]
            #     print(e)
            if _result.error:
                _result_datas.set_data_obj(_result)


    # if unknown_plugings:
    #     for unknown_pluging in unknown_plugings:
    #         _result = scene_data.ResultData()

    #         _result.error = ERROR
    #         _result.category = CATEGORY
    #         _result.data_type = data_type
    #         _result.error_text = f"[ {unknown_pluging} ] がある"
    #         _result.error_nodes = [unknown_pluging]

    #         # try:
    #         #     cmds.unknownPlugin(unknown_pluging, r=True)
    #         #     _result.error = "warning"
    #         #     _result.category = CATEGORY
    #         #     _result.data_type = data_type
    #         #     _result.error_text = f"[ {unknown_pluging} ] を削除"
    #         #     _result.error_nodes = [unknown_pluging]
    #         # except Exception as e:
    #         #     _result.error = ERROR
    #         #     _result.category = CATEGORY
    #         #     _result.data_type = data_type
    #         #     _result.error_text = f"[ {unknown_pluging} ] が消せない"
    #         #     _result.error_nodes = [unknown_pluging]
    #         #     print(e)
    #         if _result.error:
    #             _result_datas.set_data_obj(_result)

    return _result_datas

def delete_node(node=None):
    success = -1
    message = ""
    cmds.lockNode(node, lock=False)
    try:
        cmds.delete(node)
        message = f"[ {node} ] を削除"
        success = 1
    except Exception as e:
        message = f"[ {node} ] が消せない"
        success = 0
    return success, message

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""

    try:
        cmds.lockNode(node, lock=False)
        cmds.delete(node)
        message = f"[ {node} ] を削除"
        success = 1
    except Exception as e:
        message = f"[ {node} ] が消せない"
        success = 0
    return success, message