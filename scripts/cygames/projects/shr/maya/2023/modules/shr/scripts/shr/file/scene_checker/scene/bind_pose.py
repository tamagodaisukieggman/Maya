from collections import Counter
from pathlib import Path
import maya.cmds as cmds
import maya.mel

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # if maya_scene_data.current_category == 'ANIMATION' or maya_scene_data.current_category == 'RIG':
    #     return

    checker.result.color = [175, 175, 90]

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node
        _all_dag_poses = cmds.dagPose(root_node.full_path_name, q=True, bindPose=True)
        if _all_dag_poses:
            _counter = Counter(_all_dag_poses)
            if len(_counter) > 1:
                checker.result.error_nodes.append(root_node)
                checker.result.error_message_list.append("Multiple Bind Pose")


def reset_bind_pose(root_node):
    selections = cmds.ls(sl=True)
    meshes = cmds.listRelatives(root_node, allDescendents=True, fullPath=True, type="mesh")
    meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]
    _all_joint = sorted([x for x in cmds.listRelatives(root_node,
                                                       allDescendents=True,
                                                       fullPath=True)if cmds.nodeType(x) == "joint"])

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

def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    if modify_data and modify_data.error_nodes:
        for node in modify_data.error_nodes:
            try:
                reset_bind_pose(node)
                modify_result.modify_flag = True
                modify_result.modify_messages.append(f'Reset Bind Pose {node}')
                print("{:-<100}  {}".format(node, "Reset Bind Pose"))
            except Exception as e:
                modify_result.error_flag = True
                modify_result.error_messages.append(f'!!Could not Reset BinePose {node}')
                print("{:-<100}  {}".format(node, "can not reset bind pose"))
