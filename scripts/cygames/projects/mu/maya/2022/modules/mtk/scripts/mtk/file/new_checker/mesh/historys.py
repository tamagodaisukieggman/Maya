import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

ERROR_COMP_WEIGHT = f'{ERROR}:comp weight'
ERROR_INFLUENCE = f'{ERROR}:influence'
ERROR_SKIN_WEIGHT = f'{ERROR}:skin weight'

import sys

from maya import cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim

from .. import scene_data
from .. import gui_util


config_node = None
CYLISTA_SCRIPT_PATH = "Z:/cyllista/tools/maya/modules/cyllista/scripts/"


if CYLISTA_SCRIPT_PATH not in sys.path:
    sys.path.append(CYLISTA_SCRIPT_PATH)


try:
    import cyllista.config_node as config_node
except Exception:
    print('can\'t import "config_node"')
    exit(1)


NEED_JOINT_NAMES = ["skl", "helper", "dyn", "phy"]
NOT_NEED_JOINT_NAMES = ["0000", "mtp", "cnp", "move"]
# NOT_NEED_JOINT_NAMES = ["0000", "mtp", "move"]
ROOT_JOINT_NAME = "jnt_0000_skl_root"

inf_num = 4
round_num = 5


def get_skin_weight_data(skinCluster="", dag_path=None, data_type="", _result=None):
    global inf_num

    # Cyllista 対応
    if config_node:
        config = config_node.get_config()
        inf_num = config.get("cySkinInfluenceCountMax", inf_num)

    skinNode = om2.MGlobal.getSelectionListByName(skinCluster).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    singleIdComp = om2.MFnSingleIndexedComponent()
    vertexComp = singleIdComp.create(om2.MFn.kMeshVertComponent)
    weights = skinFn.getWeights(dag_path, vertexComp)

    infDags = skinFn.influenceObjects()
    inf_length = len(infDags)
    joints = [x.fullPathName().split("|")[-1] for x in infDags]

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
            weight_error_vtxs.append("{}.vtx[{}]".format(dag_path.fullPathName(), vtx_id))

    if sum_error_vtxs:
        _result.error = ERROR_COMP_WEIGHT
        _result.category = CATEGORY
        _result.data_type = data_type
        _result.error_text = "ウェイト合計値が 1.0 でない"
        _result.error_nodes = sum_error_vtxs

    if weight_error_vtxs:
        _result.error = ERROR_COMP_WEIGHT
        _result.category = CATEGORY
        _result.data_type = data_type
        _result.error_text = "インフルエンス数"
        _result.error_nodes = weight_error_vtxs

    if inf_error_joint:
        if data_type != "prop" and inf_error_joint != ROOT_JOINT_NAME:
            _result.error = ERROR_INFLUENCE
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = f"[ {inf_error_joint} ] はインフルエンスにしてはいけない"
            _result.error_nodes = [dag_path.fullPathName(), inf_error_joint]



def check(data_type="env", scene_path="", nodes=None):

    skin_cluster_name = "skinCluster"
    exclusion_node_type = [skin_cluster_name, "tweak", "shadingEngine"]
    skining_meshe_flags = []

    selList = om2.MSelectionList()
    _result_datas = scene_data.ResultDatas()

    for node in nodes:

        _result = scene_data.ResultData()
        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue

        _bind_flag = False
        _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]
        _historys = cmds.listHistory(node, pruneDagObjects=True, interestLevel=2)

        _dag_poses = cmds.listConnections(_transform_node, t='dagPose')
        selList.add(_transform_node)

        if _historys:
            _flag = False

            for _history in _historys:
                if skin_cluster_name == cmds.nodeType(_history):
                    _bind_flag = _history

                if not cmds.nodeType(_history) in exclusion_node_type:
                    _flag = True
                    break

            if _flag:
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = "ヒストリーがある"
                _result.error_nodes = [node]

        if _dag_poses and not _bind_flag:
            _result.error = ERROR_SKIN_WEIGHT
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "スキニングされていない"
            _result.error_nodes = [node]

        if _result.error_nodes:
            _result_datas.set_data_obj(_result)

        skining_meshe_flags.append(_bind_flag)

    if not selList:
        return _result_datas

    for x in range(selList.length()):
        _result = scene_data.ResultData()

        if skining_meshe_flags and skining_meshe_flags[x]:

            dagPath = selList.getDagPath(x)

            get_skin_weight_data(skining_meshe_flags[x], dagPath, data_type, _result)

        if _result.error_nodes:
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

    with gui_util.ProgressWindowBlock(title='...', maxValue=len(indices)) as prg:
        prg.status = 'Modify Weight ...'
        prg.step(1)

        for x in range(inf_length):
            infIndices[x] = x

        joints = [infDags[inf_id].fullPathName() for inf_id in range(inf_length)]

        reshape_weights = []
        for j in range(int(len(weights[0])/inf_length)):
            reshape_weights.append([weights[0][i+j*inf_length] for i in range(inf_length)])

        round_weights_list = []

        for i,_index in enumerate(indices):
            prg.step(1)
            prg.status = 'Modify Weight ...'
            if prg.is_cancelled():
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
            for _history in _historys:
                if cmds.nodeType(_history) in ["polyBlindData", "blindDataTemplate"]:
                    try:
                        cmds.delete(_history)
                        _poly_bind_flag = True
                    except:
                        pass
            if _poly_bind_flag:
                message = u"[ {} ] の [ PolyBlind ] を削除".format(node)
                print("{:-<100}  {}".format(node, "delete history poly blind"))
                # print(node, " -- delete history poly bind")

            if cmds.listHistory(node, pruneDagObjects=True, interestLevel=2):
                try:
                    cmds.bakePartialHistory(node, pc=True)
                    message = u"[ {} ] の [ Non Deformer History ] を削除".format(node)
                    print("{:-<100}  {}".format(node, "delete history"))
                    success = 1
                    # print(node, " -- delete history")
                except Exception as e:
                    message = u"!! [ {} ] の [ Non Deformer History ] を削除でない".format(node)
                    # print(node, " ++ delete history error")
                    print("{:+<100}  {}".format(node, "delete history error"))
                    success = 0
        else:
            try:
                cmds.bakePartialHistory(node, ppt=True)
                message = u"[ {} ] の [ Non Deformer History ] を削除".format(node)
                print("{:-<100}  {}".format(node, "delete history"))
                # print(node, " -- delete history")
                success = 1
            except Exception as e:
                message = u"!! [ {} ] の [ Non Deformer History ] を削除できない".format(node)
                # print(node, " ++ delete history error")
                print("{:+<100}  {}".format(node, "delete history error"))
                success = 0
    return success, message

def modify(data_type="env", scene_path="", error_detail="", nodes=None):

    success = -1
    message = ""

    if error_detail == "comp weight":
        dagPath, _ids = get_weight_datas(nodes)
        modify_weight(dagPath = dagPath, _ids = _ids)
        success = 1
        message = u"[ {} ] の ウェイト値を修正".format(dagPath.fullPathName())
        print("{:-<100}  {}".format(dagPath.fullPathName(), "Modify weight"))

    else:
        for node in nodes:
            success, message = delete_history(node)

    return success, message