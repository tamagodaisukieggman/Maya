from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    if maya_scene_data.current_category != 'CHARACTER' and maya_scene_data.current_category != 'RIG':
        return

    # エラー表示の色設定
    checker.result.color = [130, 60, 70]

    # ジョイント名の初めに必要な名前
    # 付いていないものを検出させる
    NEED_JOINT_NAME_STARTS: list = maya_scene_data.current_project_setting.get('NEED_JOINT_NAME_STARTS')
    JOINT_TYPE_NAME: list = maya_scene_data.current_project_setting.get('JOINT_TYPE_NAME')


    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node:data.CustomNodeData = node

            if node.category_group != JOINT_TYPE_NAME:
                continue

            if node.node_type != 'joint':
                continue

            exists_flag: bool = False
            for need_joint_name_start in NEED_JOINT_NAME_STARTS:
                if node.short_name.startswith(need_joint_name_start):
                    exists_flag = True
                    break

            if not exists_flag:
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append("Not Exists Joint Name")



def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    # if modify_data and modify_data.error_nodes:
    #     for node in modify_data.error_nodes:
    #         if not cmds.objExists(node):
    #             continue
    #         try:
    #             cmds.delete(node)

    #             # 修正成功フラグ
    #             modify_result.modify_flag = True
    #             modify_result.modify_messages.append(f'delete Node {node}')
    #             print("{:-<100}  {}".format(node, "delete Node"))
    #         except Exception as e:

    #             # 修正失敗フラグ
    #             modify_result.error_flag = True
    #             modify_result.error_messages.append(f'!!Could Not Delete {node}')
    #             print("{:+<100}  {}".format(node, "delete Node error"))
    return