from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    if maya_scene_data.current_category == 'ANIMATION':
        return

    # エラー表示の色設定
    checker.result.color = [154, 51, 51]

    # セッティングから読み込むサンプル
    NEED_LAYERS: list = maya_scene_data.current_project_setting.get('NOT_DELETE_DISPLAY_LAYER')
    if not NEED_LAYERS:
        return

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node:data.CustomNodeData = node
            if cmds.keyframe(node, q=True):
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append("Has Keyframe")


def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return
    # if modify_data and modify_data.error_nodes:
    #     for node in modify_data.error_nodes:
    #         if not cmds.objExists(node):
    #             continue
    #         try:
    #             cmds.cutKey(node, clear=True)
    #             # 修正成功フラグ
    #             modify_result.modify_flag = True
    #             modify_result.modify_messages.append(f'delete keyframe {node}')
    #             print("{:-<100}  {}".format(node, "delete keyframe"))
    #         except Exception as e:

    #             # 修正失敗フラグ
    #             modify_result.error_flag = True
    #             modify_result.error_messages.append(f'!!Could Not Delete Keyframe {node}')
    #             print("{:+<100}  {}".format(node, "delete keyframe error"))
