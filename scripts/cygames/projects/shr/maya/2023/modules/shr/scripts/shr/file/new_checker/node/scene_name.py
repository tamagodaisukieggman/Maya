import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))


from maya import cmds
from .. import scene_data

def check(data_type="env", scene_path="", node=None):

    if data_type == "env":
        return

    _result_datas = scene_data.ResultDatas()

    _result = scene_data.ResultData()

    node_short_name = cmds.ls(node, shortNames=True)[0]
    scene_name_obj = pathlib.Path(scene_path)

    # if node_short_name != scene_name_obj.stem:
    #     _result.error = ERROR
    #     _result.category = CATEGORY
    #     _result.data_type = data_type
    #     _result.error_text = f"シーン名と違う [ {node_short_name} ]"
    #     _result.error_nodes = [node]
    # if _result.error:
    #     _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message