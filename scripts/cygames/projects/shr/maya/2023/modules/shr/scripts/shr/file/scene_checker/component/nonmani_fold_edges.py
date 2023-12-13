from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除「ENVIRONMENT」「CHARACTER」「PROP」「ANIMATION」「RIG」「UNKNOWN」
    if maya_scene_data.current_category == 'ANIMATION':
        return

    # エラー表示の色設定
    checker.result.color = [77, 77, 128]
    message = 'Non Manifold Edges'

    # セッティングから読み込むサンプル

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            # コンポーネントの検出の場合このif 文を使って大きさのないポリゴンを排除できる
            if node.full_path_name in check_result.no_polygon_mesh:
                continue
            i_flag = cmds.polyInfo(node, nonManifoldEdges=True)
            if i_flag:
                # エラーが出たらこのようにリストに追加
                checker.result.error_nodes.append(node.full_path_name)
                # エラー表示のメッセージ
                checker.result.error_message_list.append(message)
                # print(node.full_path_name)
                # print(cmds.ls(i_flag, flatten=True))
                # コンポーネントの場合はこれを使うとUIで対象のコンポーネントを選択できる
                checker.result.error_compornent[f'{message}.{node.full_path_name}'] = cmds.ls(i_flag, flatten=True)

                # ワーニング表示、直さなくても問題ない
                # checker.result.warning_nodes.append(node)
                # checker.result.warning_message_list.append("Message")




def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    if modify_data and modify_data.error_nodes:
        for node in modify_data.error_nodes:
            if not cmds.objExists(node):
                continue
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
