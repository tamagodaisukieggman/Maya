import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))


from maya import cmds
import maya.api.OpenMaya as om2
from .. import scene_data


def check_locked_face_vtxs_normal(full_path="", dag_path=None, data_type="env", _result=None):
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
        # if data_type == "env":
        #     _result.error = ERROR
        #     _result.category = CATEGORY
        #     _result.data_type = data_type
        #     _result.error_text = "法線のロック  [ 背景データでは自動修正されません ]"
        #     _result.error_nodes = [full_path]
        # else:
        _result.error = ERROR
        _result.category = CATEGORY
        _result.data_type = data_type
        _result.error_text = "法線のロック"
        _result.error_nodes = [full_path]


def check(data_type="env", scene_path="", nodes=None):

    # キャラの法線は確認しない
    if data_type == "chara":
        return

    selList = om2.MSelectionList()
    _result_datas = scene_data.ResultDatas()
    for node in nodes:
        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue

        _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]
        selList.add(_transform_node)

    for x in range(selList.length()):

        dagPath = selList.getDagPath(x)
        fullPath = dagPath.fullPathName()
        path_split = fullPath.split("|")

        # ルートノード排除用
        # if len(path_split) == 1:
        #     continue

        # LODグループ排除用
        if path_split[2] != "model":
            continue

        _result = scene_data.ResultData()
        check_locked_face_vtxs_normal(fullPath, dagPath, data_type, _result)

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
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