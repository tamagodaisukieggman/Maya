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
    checker.result.color = [77, 47, 128]

    # セッティングから読み込むサンプル
    KEEP_COLOR_SET_NAME: list = maya_scene_data.current_project_setting.get('KEEP_COLOR_SET_NAME')


    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            # コンポーネントの検出の場合このif 文を使って大きさのないポリゴンを排除できる
            if node.full_path_name in check_result.no_polygon_mesh:
                continue
            color_sets = cmds.polyColorSet(node, q=True, allColorSets=True)

            if not color_sets:
                continue

            # エラーが出たらこのようにリストに追加
            checker.result.error_nodes.append(node.full_path_name)
            # エラー表示のメッセージ
            checker.result.error_message_list.append("Has Color Set")
            # コンポーネントの場合はこれを使うとUIで対象のコンポーネントを選択できる
            # checker.result.error_compornent[node.full_path_name] = error_compornents

            # ワーニング表示、直さなくても問題ない
            # checker.result.warning_nodes.append(node.full_path_name)
            # checker.result.warning_message_list.append("Message")
            # checker.result.warning_compornent[node.full_path_name] = warning_compornents



def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return
    # if modify_data and modify_data.error_nodes:
    #     for node in modify_data.error_nodes:
    #         if not cmds.objExists(node):
    #             continue
    #         print(node)
    #         color_sets = cmds.polyColorSet(node, q=True, allColorSets=True)

    #         if not color_sets:
    #             continue

    #         for i, color_set in enumerate(color_sets):
    #             try:
    #                 cmds.polyColorSet(node, delete=True, colorSet=color_set)
    #                 modify_result.modify_messages.append(f'delete Node {node}')
    #                 print(f'{node:-<100}  delete ColorSet [ {color_set} ]')
    #             except Exception as e:
    #                 modify_result.error_flag = True
    #                 modify_result.error_messages.append(f'!!Could Not Delete {node}')
    #                 print(f'{node:-<100}  could not delete ColorSet [ {color_set} ]')
    #                 print(e)



    # for node in nodes:
    #     color_sets = cmds.polyColorSet(node, q=True, allColorSets=True)

    #     if not color_sets:
    #         continue

    #     keep_color_set_index = 0
    #     color_set_exists = COLOR_SET_NAME in color_sets

    #     if color_set_exists:
    #         keep_color_set_index = color_sets.index(COLOR_SET_NAME)

    #     for i, color_set in enumerate(color_sets):
    #         if color_set_exists and color_set != COLOR_SET_NAME:
    #             try:
    #                 cmds.polyColorSet(node, delete=True, colorSet=color_set)
    #                 message = f'[ {node} ] delete ColorSet [ {color_set} ]'
    #                 success = 1
    #                 print(f'{node:-<100}  delete ColorSet [ {color_set} ]')
    #             except Exception as e:
    #                 success = 0
    #                 message = f'[ {node} ] could not delete ColorSet [ {color_set} ]'
    #                 print(f'{node:-<100}  could not delete ColorSet [ {color_set} ]')
    #                 print(e)
    #         elif i == keep_color_set_index:
    #             try:
    #                 cmds.polyColorSet(node, rename=True, colorSet=color_set, newColorSet=COLOR_SET_NAME)
    #                 message = f'[ {node} ] rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]'
    #                 success = 1
    #                 print(f'{node:-<100} rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]')
    #             except Exception as e:
    #                 success = 0
    #                 message = f'[ {node} ] could not rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]'
    #                 print(f'{node:-<100}  could not rename ColorSet name [ {color_set} ] to [ {COLOR_SET_NAME} ]')
    #                 print(e)
