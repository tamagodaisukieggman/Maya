from pathlib import Path
import maya.cmds as cmds
import maya.api.OpenMaya as om2

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check_ngon_api2(fullPath=''):
    selList = om2.MSelectionList()
    selList.add(fullPath)
    dagPath = selList.getDagPath(0)
    mesh_fn = None
    ngon_compornents:list = []

    try:
        mesh_fn = om2.MFnMesh(dagPath)
    except Exception as e:
        pass

    if not mesh_fn:
        return

    _length = mesh_fn.numPolygons

    for num in range(_length):
        if mesh_fn.polygonVertexCount(num) > 4:
            _m = f"{fullPath}.f[{num}]"
            ngon_compornents.append(_m)
    return ngon_compornents


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if maya_scene_data.current_category == 'ANIMATION':
        return

    checker.result.color = [77, 27, 128]
    message = 'Ngon'

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            if node.full_path_name in check_result.no_polygon_mesh:
                continue
            error_compornents = check_ngon_api2(fullPath=node.full_path_name)
            if error_compornents:

                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_compornent[f'{message}.{node.full_path_name}'] = error_compornents
                checker.result.error_message_list.append(message)




def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    pass
