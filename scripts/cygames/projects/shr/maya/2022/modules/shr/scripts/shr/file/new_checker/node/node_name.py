import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))


from maya import cmds
from .. import scene_data


MODEL_GROUP_NAME = "model"

# LOD の名前「lod1」のように「lod」「整数」となるリストを10まで作成
LOD_NAME = "lod"
COLLISION_GROUP_NAME = "collision"


def check(data_type="env", scene_path="", nodes=None):

    _lod_num = 0
    _model_group = []
    _result_datas = scene_data.ResultDatas()
    _all_result = scene_data.ResultData()
    _model_name_flag = False

    for _cld in cmds.listRelatives(nodes, children=True, fullPath=True):
        if cmds.nodeType(_cld) == "joint":
            continue
        _cld_short_name = _cld.split("|")[-1]
        _result = scene_data.ResultData()

        if cmds.nodeType(_cld) == "transform":
            if MODEL_GROUP_NAME in _cld_short_name:
                _model_name_flag = True
                if _cld_short_name != MODEL_GROUP_NAME:
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = f"[ {_cld_short_name} ]不正な命名"
                    _result.error_nodes = [_cld]
                else:
                    _model_group.append(_cld)

            elif COLLISION_GROUP_NAME in _cld_short_name:
                if _cld_short_name != COLLISION_GROUP_NAME:
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = f"[ {_cld_short_name} ]不正な命名"
                    _result.error_nodes = [_cld]

            elif LOD_NAME in _cld_short_name:
                _check_lod_name = _cld_short_name[:3]
                _check_lod_num = _cld_short_name[3:]
                if _check_lod_name != LOD_NAME:
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = f"[ {_check_lod_name} ]不正な命名"
                    _result.error_nodes = [_cld]

                if not _check_lod_num.isdigit():
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = f"[ {_check_lod_num} ]不正な命名"
                    _result.error_nodes = [_cld]

                else:
                    _lod_num += 1
                    if int(_check_lod_num) != _lod_num:
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = "数字の順番違い"
                        _result.error_nodes = [_cld]
            else:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = "仕様にないノード名"
                _result.error_nodes = [_cld]

        else:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "仕様にないノード名"
            _result.error_nodes = [_cld]
        if _result.category:
            _result_datas.set_data_obj(_result)

    if not _model_name_flag and not _model_group:
        _all_result.error = ERROR
        _all_result.category = CATEGORY
        _all_result.data_type = data_type
        _all_result.error_text = f"[ {MODEL_GROUP_NAME} ] グループがない"
        _all_result.error_nodes = nodes

    # if _all_result.category:
    #     _result_datas.set_data_obj(_all_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message