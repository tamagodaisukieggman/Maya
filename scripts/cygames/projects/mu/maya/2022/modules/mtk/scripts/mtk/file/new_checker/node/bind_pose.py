import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from collections import Counter

from maya import cmds
import maya.mel
from .. import scene_data

def check(data_type="env", scene_path="", node=None):

    _result_datas = scene_data.ResultDatas()

    _all_dag_poses = cmds.dagPose(node, q=True, bp=True)

    _result = scene_data.ResultData()
    if _all_dag_poses:
        _counter = Counter(_all_dag_poses)
        if len(_counter) > 1:

            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "multiple bind pose"
            _result.error_nodes = [node]
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

    # _all_dag_poses = cmds.listConnections(root_node, t='dagPose')
    _all_dag_poses = cmds.dagPose(root_node, q=True, bp=True)
    _counter = Counter(_all_dag_poses)

    for mesh in meshes:
        cmds.select(mesh, r=True)
        maya.mel.eval("GoToBindPose;")
    _pose = _counter.most_common()[0][0]
    cmds.delete(_all_dag_poses)
    cmds.select(_all_joint, r=True)
    cmds.dagPose(bp=True, s=True, sl=True, name=_pose)

    if selections:
        cmds.select(selections, r=True)
    else:
        cmds.select(cl=True)
    return True

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    try:
        reset_bind_pose(node)
        message = f'[ {node} ] reset bind pose'
        success = 1
        print("{:-<100}  {}".format(node, "reset bind pose"))
    except Exception as e:
        success = 0
        message = f'[ {node} ] can not reset bind pose'
        print("{:-<100}  {}".format(node, "can not reset bind pose"))
        print(e)
    return success, message