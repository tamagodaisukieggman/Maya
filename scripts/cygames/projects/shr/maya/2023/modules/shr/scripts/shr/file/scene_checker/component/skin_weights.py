from pathlib import Path
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check_skin_weight_data(
                fullPath:str = '',
                skinCluster:str = '',
                weight_influence_number:int= 4 ,
                weight_number_of_digits:int = 4,
                checker:data.Checker = None,
                do_not_use_influence: list = [],
                ):

    # 各エラーメッセージ
    message:str = 'Weight Error'
    total_value_error_message:str = 'Total Value Error'
    influence_error_message:str = 'Influence Length Error'
    do_not_use_influence_error_message:str = 'Do Not Use Infuluence'

    # コンポーネントの入れ物
    error_compornents: list = []
    total_value_error_component: list = []
    influence_error_compornent: list = []
    do_not_use_influence_error_compornent: list = []

    # エラーメッセージ
    error_message:list = []

    # エラーフラグ
    sum_error: bool = False
    influence_error: bool = False
    not_use_infuluence_error: bool = False

    selList = om2.MSelectionList()
    selList.add(fullPath)
    dagPath = selList.getDagPath(0)

    skinNode = om2.MGlobal.getSelectionListByName(skinCluster).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    singleIdComp = om2.MFnSingleIndexedComponent()
    vertexComp = singleIdComp.create(om2.MFn.kMeshVertComponent)
    weights = skinFn.getWeights(dagPath, vertexComp)

    infDags = skinFn.influenceObjects()
    inf_length = len(infDags)
    joints = [x.fullPathName().split("|")[-1] for x in infDags]

    if not weight_influence_number:
        weight_influence_number = cmds.getAttr(f'{skinCluster}.maxInfluences')

    for vtx_id in range(int(len(weights[0]) / inf_length)):

        vtx_weights = [weights[0][i + vtx_id * inf_length] for i in range(inf_length)]
        num_joints = []
        _sum_weight = 0

        for joint, weight in zip(joints, vtx_weights):
            inf_error_joint: str = ''
            if not weight:
                continue

            num_joints.append(joint)
            _sum_weight += weight

        #     # インフルエンスを振り分けてはいけないジョイントの検出
        #     joint_name_split = joint.split("_")

        #     if len(joint_name_split) < 3:
        #         continue

        #     for inf in do_not_use_influence:
        #         if joint_name_split[1] in inf:
        #             inf_error_joint = joint
        #             break
        #     if inf_error_joint:
        #         break

        # 合計値エラーの検出
        if round(sum(vtx_weights), weight_number_of_digits) != 1.0:
            total_value_error_component.append("{}.vtx[{}]".format(fullPath, vtx_id))
            sum_error = True

        # インフルエンス数エラーの検出
        if weight_influence_number < len(num_joints):
            influence_error_compornent.append("{}.vtx[{}]".format(fullPath, vtx_id))
            influence_error = True

    # 合計値が１ではない
    if sum_error:
        if fullPath not in checker.result.error_nodes:
            checker.result.error_nodes.append(fullPath)
        error_message.append(total_value_error_message)

    # インフルエンス数のエラー
    if influence_error:
        if fullPath not in checker.result.error_nodes:
            checker.result.error_nodes.append(fullPath)
        error_message.append(influence_error_message)

    # 対象のコンポーネント
    if error_compornents:
        checker.result.error_compornent[f'{message}.{fullPath}'] = error_compornents

    # 合計値エラー
    if total_value_error_component:
        checker.result.error_compornent[f'{total_value_error_message}.{fullPath}'] = total_value_error_component

    # インフルエンス数エラー
    if influence_error_compornent:
        checker.result.error_compornent[f'{influence_error_message}.{fullPath}'] = influence_error_compornent

    # エラーメッセージ
    if error_message:
        checker.result.error_message_list.append(' ,'.join(error_message))

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    if maya_scene_data.current_category != 'CHARACTER':
        return

    # cyllista コンフィグロード用
    from .. import setting

    # エラー表示の色設定
    checker.result.color = [77, 102, 128]
    message = 'Weight Error'

    # スキンクラスタのインフルエンス数
    WEIGHT_INFLUENCE_NUMBER:int = setting.get_influence_length_from_cyllista_config()
    # WEIGHT_INFLUENCE_NUMBER: int = maya_scene_data.current_project_setting.get('WEIGHT_INFLUENCE_NUMBER')
    # if not WEIGHT_INFLUENCE_NUMBER:
    #     WEIGHT_INFLUENCE_NUMBER = 4

    # スキンウェイトの桁数設定
    WEIGHT_NUMBER_OF_DIGITS: int = maya_scene_data.current_project_setting.get('WEIGHT_NUMBER_OF_DIGITS')
    if not WEIGHT_NUMBER_OF_DIGITS:
        WEIGHT_NUMBER_OF_DIGITS = 3

    # インフルエンスに設定してはいけないジョイント
    DO_NOT_USE_INFLUENCE: list = maya_scene_data.current_project_setting.get('DO_NOT_USE_INFLUENCE')

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            # コンポーネントの検出の場合このif 文を使って大きさのないポリゴンを排除できる
            if node.full_path_name in check_result.no_polygon_mesh:
                continue

            skinCluster:str =  check_result.skining_geometory.get(node.full_path_name)
            if not skinCluster:
                continue
            check_skin_weight_data(
                                    fullPath=node.full_path_name,
                                    skinCluster=skinCluster,
                                    weight_influence_number=WEIGHT_INFLUENCE_NUMBER,
                                    weight_number_of_digits=WEIGHT_NUMBER_OF_DIGITS,
                                    checker=checker,
                                    do_not_use_influence=DO_NOT_USE_INFLUENCE,
                                    )
            # エラーが出たらこのようにリストに追加
            # checker.result.error_nodes.append(node.full_path_name)
            # エラー表示のメッセージ
            # checker.result.error_message_list.append("Message")
            # コンポーネントの場合はこれを使うとUIで対象のコンポーネントを選択できる
            # checker.result.error_compornent[node.full_path_name] = error_compornents

            # ワーニング表示、直さなくても問題ない
            # checker.result.warning_nodes.append(node.full_path_name)
            # checker.result.warning_message_list.append("Message")
            # checker.result.warning_compornent[node.full_path_name] = warning_compornents




def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return
