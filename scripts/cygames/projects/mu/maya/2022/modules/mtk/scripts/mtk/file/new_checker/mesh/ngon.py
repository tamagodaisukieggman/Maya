import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds

import maya.api.OpenMaya as om2
from .. import scene_data



def check_ngon_api2(data_type="", mesh_fn="", dagPath="", _result_datas=None):

    fullPath = dagPath.fullPathName()
    _length = mesh_fn.numPolygons

    for num in range(_length):
        _result = scene_data.ResultData()
        if mesh_fn.polygonVertexCount(num) > 4:
            _m = f"{fullPath}.f[{num}]"

            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "多角形"
            _result.error_nodes = [_m]

            if _result.error_nodes:
                _result_datas.set_data_obj(_result)


def check(data_type="env", scene_path="", nodes=None):

    selList = om2.MSelectionList()
    _result_datas = scene_data.ResultDatas()

    for node in nodes:
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
        check_ngon_api2(data_type, mesh_fn, dagPath, _result_datas)

    return _result_datas



def modify(data_type="env", scene_path="", error_detail="", nodes=None):
    success = -1
    message = ""

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