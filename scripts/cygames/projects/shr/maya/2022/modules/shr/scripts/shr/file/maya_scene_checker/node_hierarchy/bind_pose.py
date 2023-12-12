from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

from maya import cmds
from .. import scene_data
from .. import settings

from collections import Counter
import maya.mel


def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    _all_dag_poses = cmds.dagPose(check_targets, q=True, bindPose=True)

    _result = scene_data.ResultData()
    if _all_dag_poses:
        _counter = Counter(_all_dag_poses)
        if len(_counter) > 1:

            _result.error_type_message = ERROR
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = "Multiple Bind Pose"
            _result.error_nodes = check_targets
            _result.error_type_color = [175, 175, 90]
        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas

def reset_bind_pose(root_node):
    selections = cmds.ls(sl=True)
    meshes = cmds.listRelatives(root_node, allDescendents=True, fullPath=True, type="mesh")
    meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]
    _all_joint = sorted([x for x in cmds.listRelatives(root_node,
                                                allDescendents=True,
                                                fullPath=True)if cmds.nodeType(x)=="joint"])

    _all_dag_poses = cmds.dagPose(root_node, q=True, bindPose=True)
    _counter = Counter(_all_dag_poses)

    for mesh in meshes:
        cmds.select(mesh, r=True)
        maya.mel.eval("GoToBindPose;")
    _pose = _counter.most_common()[0][0]
    cmds.delete(_all_dag_poses)
    cmds.select(_all_joint, r=True)
    cmds.dagPose(bindPose=True, save=True, selection=True, name=_pose)

    if selections:
        cmds.select(selections, replace=True)
    else:
        cmds.select(clear=True)
    return True

def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    if isinstance(modify_targets, str):
        modify_targets = eval(modify_targets)
    if not modify_targets:
        return success, message

    for modify_target in modify_targets:
        try:
            reset_bind_pose(modify_target)
            message = f'Reset Bind Pose [ {modify_target} ]'
            success = 1
            # print("{:-<100}  {}".format(modify_target, "reset bind pose"))
        except Exception as e:
            success = 0
            message = f'Could not Reset BinePose [ {modify_target} ]'
            # print("{:-<100}  {}".format(modify_target, "can not reset bind pose"))
            print(e)
    return success, message