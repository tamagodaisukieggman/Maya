from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

from maya import cmds
import maya.api.OpenMaya as om2

from .. import scene_data
from .. import settings


def check_locked_face_vtxs_normal(full_path="", dag_path=None, data_type_category="ENVIRONMENT", _result:scene_data.ResultData=None)->scene_data.ResultData:
    mesh_fn = om2.MFnMesh(dag_path)
    _lock_flag = False
    num_polygon = mesh_fn.numPolygons
    normal_ids = []

    for x in range(num_polygon):
        normal_ids.extend(mesh_fn.getFaceNormalIds(x))

    for normal_id in normal_ids:
        if mesh_fn.isNormalLocked(normal_id):
            _lock_flag = True
            break

    if _lock_flag:
        _result.error_type_message = ERROR
        _result.checker_module = CHECKER
        _result.checker_category = CATEGORY
        _result.data_type_category = data_type_category
        _result.error_text = "Locked Normal"
        _result.error_nodes = [full_path]
    return _result

def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    # キャラの法線は確認しない
    if data_type_category == "CHARACTER":
        return _result_datas

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    selList = om2.MSelectionList()

    for node in check_targets:
        if cmds.getAttr("{}.intermediateObject".format(node)):
            continue

        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue

        _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]
        selList.add(_transform_node)

    for x in range(selList.length()):

        dagPath = selList.getDagPath(x)
        fullPath = dagPath.fullPathName()

        _result = scene_data.ResultData()
        check_locked_face_vtxs_normal(fullPath, dagPath, data_type_category, _result)

        if _result.error_type_message:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    if isinstance(modify_targets, str):
        modify_targets = eval(modify_targets)
    if not modify_targets:
        return success, message
    # try:
    #     cmds.polyNormalPerVertex(node, ufn=True)
    #     message = f'[ {node} ] のノーマルロックを解除'
    #     cmds.bakePartialHistory(node, ppt=True)
    #     success = 1
    #     print(f'{node:-<100}  {"Unlock Normal"}')
    # except Exception as e:
    #     message = f'[ {node} ] のノーマルロックを解除できない'
    #     success = 0
    #     print(f'{node:-<100}  {"Unlock Normal Error"}')
    return success, message