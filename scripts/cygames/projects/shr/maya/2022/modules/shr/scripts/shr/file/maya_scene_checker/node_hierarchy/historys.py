from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
# CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CATEGORY = _current_file.parent.stem
CHECKER = _current_file.stem

from maya import cmds
from .. import scene_data
from .. import settings


import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim

from ....utils import gui_util

ERROR_COMP_WEIGHT = f'{ERROR}:comp weight'
ERROR_INFLUENCE = f'{ERROR}:influence'
ERROR_SKIN_WEIGHT = f'{ERROR}:skin weight'

NEED_JOINT_NAMES = ["skl", "helper", "dyn", "phy"]
NOT_NEED_JOINT_NAMES = ["0000", "mtp", "cnp", "move"]
# NOT_NEED_JOINT_NAMES = ["0000", "mtp", "move"]
ROOT_JOINT_NAME = "jnt_0000_skl_root"

inf_num = 4
round_num = 5


def get_skin_weight_data(skinCluster="", dag_path=None, data_type_category="", _result=scene_data.ResultData()):
    _m = ''
    global inf_num

    skinNode = om2.MGlobal.getSelectionListByName(skinCluster).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    singleIdComp = om2.MFnSingleIndexedComponent()
    vertexComp = singleIdComp.create(om2.MFn.kMeshVertComponent)
    weights = skinFn.getWeights(dag_path, vertexComp)

    infDags = skinFn.influenceObjects()
    inf_length = len(infDags)
    joints = [x.fullPathName().split("|")[-1] for x in infDags]

    inf_num = cmds.getAttr(f'{skinCluster}.maxInfluences')

    weight_error_vtxs = []
    sum_error_vtxs = []
    inf_error_joint = ""

    for vtx_id in range(int(len(weights[0])/inf_length)):

        vtx_weights = [weights[0][i + vtx_id * inf_length] for i in range(inf_length)]
        num_joints = []
        _sum_weight = 0

        for joint, weight in zip(joints, vtx_weights):
            if not weight:
                continue

            num_joints.append(joint)
            _sum_weight += weight

            joint_name_split = joint.split("_")

            if len(joint_name_split) < 3:
                continue

            if joint_name_split[1] in NOT_NEED_JOINT_NAMES:
                inf_error_joint = joint
                break

        if round(sum(vtx_weights), round_num) != 1.0:
            sum_error_vtxs.append("{}.vtx[{}]".format(dag_path.fullPathName(), vtx_id))

        if inf_num < len(num_joints):
            _m = f' : [ {inf_num} ] , [ {len(num_joints)} ]'
            weight_error_vtxs.append("{}.vtx[{}]".format(dag_path.fullPathName(), vtx_id))

    if sum_error_vtxs:
        _result.error_type_message = ERROR_COMP_WEIGHT
        _result.checker_module = CHECKER
        _result.checker_category = CATEGORY
        _result.data_type_category = data_type_category
        _result.error_text = "Value Over"
        _result.error_nodes = sum_error_vtxs

    if weight_error_vtxs:
        _result.error_type_message = ERROR_COMP_WEIGHT
        _result.checker_module = CHECKER
        _result.checker_category = CATEGORY
        _result.data_type_category = data_type_category
        _result.error_text = f"Influence Over {_m}"
        _result.error_nodes = weight_error_vtxs

    if inf_error_joint:
        if data_type_category != "prop" and inf_error_joint != ROOT_JOINT_NAME:
            _result.error_type_message = ERROR_INFLUENCE
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = f"[ {inf_error_joint} ] はインフルエンスにしてはいけない"
            _result.error_nodes = [dag_path.fullPathName(), inf_error_joint]



def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    skin_cluster_name = "skinCluster"
    exclusion_node_type = [skin_cluster_name, "tweak", "shadingEngine"]

    for node in check_targets:
        _children = cmds.listRelatives(node, allDescendents=True, fullPath=True)
        if not _children:
            continue
        for _child in _children:
            if cmds.nodeType(_child) != "mesh":
                continue
            _result = scene_data.ResultData()
            # bb_size = cmds.polyEvaluate(_child, boundingBox=True, accurateEvaluation=True)
            # if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            #     continue
            _bind_flag = False
            _transform_node = cmds.listRelatives(_child, parent=True, fullPath=True)
            if _transform_node:
                _transform_node = _transform_node[0]
            _historys = cmds.listHistory(_child, pruneDagObjects=True, interestLevel=2)
            _dag_poses = cmds.listConnections(_transform_node, type='dagPose')
            if _historys:
                _flag = False
                for _history in _historys:
                    if skin_cluster_name == cmds.nodeType(_history):
                        _bind_flag = _history

                    if not cmds.nodeType(_history) in exclusion_node_type:
                        _flag = True
                        break
                if _flag:
                    _result.error_type_message = ERROR
                    _result.checker_module = CHECKER
                    _result.checker_category = CATEGORY
                    _result.data_type_category = data_type_category
                    _result.error_text = "Has History"
                    _result.error_nodes = [_child]
                    _result.error_type_color = [90, 175, 90]

            if _dag_poses and not _bind_flag:
                _result.error_type_message = ERROR_SKIN_WEIGHT
                _result.checker_module = CHECKER
                _result.checker_category = CATEGORY
                _result.data_type_category = data_type_category
                _result.error_text = "Not Binding"
                _result.error_nodes = [_child, _dag_poses[0]]
                _result.error_type_color = [175, 175, 90]

            if _result.error_type_message:
                _result_datas.set_data_obj(_result)

    return _result_datas


def modify_weight(dagPath, _ids):
    skinCluster = cmds.ls(cmds.listHistory(dagPath.fullPathName()), type='skinCluster')[0]
    skinNode = om2.MGlobal.getSelectionListByName(skinCluster).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    indices = _ids

    fnCompNew = om2.MFnSingleIndexedComponent()
    vertexComp = fnCompNew.create(om2.MFn.kMeshVertComponent)
    fnCompNew.addElements(indices)
    weights = skinFn.getWeights(dagPath, vertexComp)

    infDags = skinFn.influenceObjects()
    inf_length = len(infDags)
    infIndices = om2.MIntArray(len(infDags), 0)

    _stop_flag = False
    _all_length = len(indices)

    for x in range(inf_length):
        infIndices[x] = x

    joints = [infDags[inf_id].fullPathName() for inf_id in range(inf_length)]

    reshape_weights = []
    for j in range(int(len(weights[0])/inf_length)):
        reshape_weights.append([weights[0][i+j*inf_length] for i in range(inf_length)])

    round_weights_list = []

    with gui_util.ProgressDialog(title='...', maxValue=_all_length) as prg:
        for i,_index in enumerate(indices):
            prg.step(i+1)
            if prg.wasCanceled():
                _stop_flag = True
                break

            weight_dic = dict(zip(joints, [round(x, round_num) for x in reshape_weights[i]]))
            weight_lists = []
            [weight_lists.extend([k,v]) for k,v in sorted(weight_dic.items(), key=lambda x:x[1], reverse=True)]

            _weights = weight_lists[1::2]
            _joints = weight_lists[0::2]

            if len(_weights) > inf_num:
                _zero_weights = [0.0 for x in range(len(_weights[inf_num:]))]
                del _weights[inf_num:]
                _weights.extend(_zero_weights)

            if sum(_weights) != 1.0:
                _weights[0] = round(1.0 - sum(_weights[1:]), round_num)
            round_weights_list.extend([_weights[_joints.index(_jnt)] for _jnt in joints])

    if not _stop_flag:
        skinFn.setWeights(dagPath,
                        vertexComp,
                        infIndices,
                        om2.MDoubleArray(round_weights_list),
                        False)

def get_weight_datas(node):
    _geometory = node[0].rsplit(".", 1)[0]
    selList = om2.MSelectionList()
    selList.add(_geometory)

    dagPath = selList.getDagPath(0)
    _ids = [int(x.split("[")[-1].split("]")[0]) for x in node]
    return dagPath, _ids


def delete_history(node):
    success = -1
    message = ""

    _bind_skin_flag = False
    _poly_bind_flag = False

    _historys = cmds.listHistory(node, pruneDagObjects=True, interestLevel=2)

    if _historys:
        if "skinCluster" in [cmds.nodeType(x) for x in _historys]:
            _bind_skin_flag = True
        if not _bind_skin_flag:
            # for _history in _historys:
            #     if cmds.nodeType(_history) in ["polyBlindData", "blindDataTemplate"]:
            #         try:
            #             cmds.delete(_history)
            #             _poly_bind_flag = True
            #         except:
            #             pass
            # if _poly_bind_flag:
            #     message = u"Delete [ PolyBlind ] [ {} ]".format(node)
            #     print("{:-<100}  {}".format(node, "delete history poly blind"))

            if cmds.listHistory(node, pruneDagObjects=True, interestLevel=2):
                try:
                    cmds.bakePartialHistory(node, preCache=True)
                    message = u"Delete [ Non Deformer History ] [ {} ]".format(node)
                    # print("{:-<100}  {}".format(node, "delete history"))
                    success = 1
                    # print(node, " -- delete history")
                except Exception as e:
                    message = u"!! Could Not Delete [ Non Deformer History ] [ {} ]".format(node)
                    # print(node, " ++ delete history error")
                    # print("{:+<100}  {}".format(node, "delete history error"))
                    success = 0
        else:
            try:
                cmds.bakePartialHistory(node, prePostDeformers=True)
                message = u"Delete [ Non Deformer History ] [ {} ]".format(node)
                # print("{:-<100}  {}".format(node, "delete history"))
                # print(node, " -- delete history")
                success = 1
            except Exception as e:
                message = u"!! Could Not Delete [ Non Deformer History ] [ {} ]".format(node)
                # print(node, " ++ delete history error")
                # print("{:+<100}  {}".format(node, "delete history error"))
                success = 0
    return success, message

def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    if isinstance(modify_targets, str):
        modify_targets = eval(modify_targets)
    if not modify_targets:
        return success, message

    for node in modify_targets:
        success, message = delete_history(node)

    return success, message