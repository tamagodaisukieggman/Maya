from pathlib import Path
import maya.cmds as cmds
import maya.api.OpenMaya as om2

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

def check_cvs_value(fullPath="")->bool:
    selList = om2.MSelectionList()
    selList.add(fullPath)
    dagPath = selList.getDagPath(0)
    fullPath = dagPath.fullPathName()
    mesh_fn = None
    error_flag = False
    try:
        mesh_fn = om2.MFnMesh(dagPath)
    except Exception as e:
        # print(f' {CHECKER}: {e}: [ {fullPath} ]')
        pass

    if not mesh_fn:
        return error_flag

    plug = mesh_fn.findPlug('pnts', False)

    for i in range(plug.numElements()):
        _pos = plug.elementByPhysicalIndex(i).asMDataHandle().asFloat3()
        if str(_pos)  != '[0.0, 0.0, 0.0]':
            error_flag = True
            break

    return error_flag

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    if(maya_scene_data.current_category == 'ANIMATION' or
       maya_scene_data.current_category == 'ENVIRONMENT'):
        return

    checker.result.color = [77, 67, 128]

    for root_node in maya_scene_data.root_nodes:

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            if node.full_path_name in check_result.no_polygon_mesh:
                continue
            node: data.CustomNodeData = node
            flag = check_cvs_value(node.full_path_name)
            if flag:
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append('CVs value exists')




def freeze_cvs_value(node:str=""):
    _parent = cmds.listRelatives(node, parent=True, fullPath=True)[0]
    cmds.select(_parent, replace=True)
    ltd = cmds.lattice(divisions=(2, 2, 2), objectCentered=True)
    cmds.delete(_parent, constructionHistory=True)
    cmds.select(clear=True)

    _pnts = cmds.getAttr(f"{node}.pnts[*]")
    zero_values = [0]*len(_pnts)*3
    cmds.setAttr(f"{node}.pnts[*]", *zero_values )


def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    if modify_data and modify_data.error_nodes:
        for node in modify_data.error_nodes:
            if not cmds.objExists(node):
                continue
            _historys = cmds.listHistory(node, pruneDagObjects=True, interestLevel=2)
            if _historys:
                skinCluster = [x for x in _historys if cmds.nodeType(x) == 'skinCluster']
                if skinCluster:
                    modify_result.error_flag = True
                    modify_result.error_messages.append(f'!! Could Not Reset [ Bind Skin Node ] {node}')
                    print("{:+<100}  {}".format(node, "Reset CVs Values error"))
                else:
                    try:
                        modify_result.modify_flag = True
                        modify_result.modify_messages.append(f'Reset [ CVs Values ] {node}')
                        print("{:-<100}  {}".format(node, "Reset CVs Values"))
                    except Exception as e:
                        modify_result.error_flag = True
                        modify_result.error_messages.append(f'!! Could Not Reset [ CVs Values ] {node}')
                        print("{:+<100}  {}".format(node, "Reset CVs Values error"))
