from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

import maya.cmds as cmds
import maya.api.OpenMaya as om2

from .. import scene_data
from .. import settings


def check_ngon_api2(data_type_category="", mesh_fn="", dagPath="", _result_datas:scene_data.ResultDatas=None):

    fullPath = dagPath.fullPathName()
    _length = mesh_fn.numPolygons

    for num in range(_length):
        _result = scene_data.ResultData()
        if mesh_fn.polygonVertexCount(num) > 4:
            _m = f"{fullPath}.f[{num}]"

            _result.error_type_message = ERROR
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = "Ngon"
            _result.error_nodes = [_m]
            _result.error_type_color = [90, 0, 90]

            if _result.error_type_message:
                _result_datas.set_data_obj(_result)


def check(data_type_category:str='', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

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

    if not selList:
        return

    for x in range(selList.length()):
        dagPath = selList.getDagPath(x)
        mesh_fn = om2.MFnMesh(dagPath)
        check_ngon_api2(data_type_category, mesh_fn, dagPath, _result_datas)

    return _result_datas



def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    # if isinstance(modify_targets, str):
    #     modify_targets = eval(modify_targets)
    # if not modify_targets:
    #     return success, message

    # try:
    #     cmds.polyTriangulate(nodes, constructionHistory=False, caching=False, nodeState=0)
    #     message = f'[ {nodes[0]} ] Trianglate'
    #     success = 1
    #     print(f'{nodes[0]:-<100}  Trianglate')
    # except Exception as e:
    #     success = 0
    #     message = f'[ {nodes[0]} ] could not Trianglate'
    #     print(f'{nodes[0]:-<100}  could not Trianglate')
    #     print(e)

    return success, message