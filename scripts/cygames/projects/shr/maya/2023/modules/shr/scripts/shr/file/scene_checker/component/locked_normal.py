from pathlib import Path
import maya.cmds as cmds
import maya.api.OpenMaya as om2

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check_locked_face_vtxs_normal(full_path=""):
    _lock_flag = False
    normal_ids = []

    selList = om2.MSelectionList()
    selList.add(full_path)
    dagPath = selList.getDagPath(0)
    mesh_fn = None

    try:
        mesh_fn = om2.MFnMesh(dagPath)
    except Exception as e:
        pass

    if not mesh_fn:
        return

    num_polygon = mesh_fn.numPolygons

    for x in range(num_polygon):
        normal_ids.extend(mesh_fn.getFaceNormalIds(x))

    for normal_id in normal_ids:
        if mesh_fn.isNormalLocked(normal_id):
            _lock_flag = True
            break

    return _lock_flag

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if maya_scene_data.current_category == 'ANIMATION' or maya_scene_data.current_category == 'RIG' or maya_scene_data.current_category == 'CHARACTER':
        return

    checker.result.color = [128, 128, 230]

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            if node.full_path_name in check_result.no_polygon_mesh:
                continue
            lock_flag = check_locked_face_vtxs_normal(node.full_path_name)
            if lock_flag:
                checker.result.warning_nodes.append(node.full_path_name)
                checker.result.warning_message_list.append("Lock Normal")






def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    pass
