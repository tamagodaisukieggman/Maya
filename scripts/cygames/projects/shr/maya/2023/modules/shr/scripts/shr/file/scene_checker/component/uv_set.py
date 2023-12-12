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

    KEEP_UV_SET_NAME: list = maya_scene_data.current_project_setting.get('KEEP_UV_SET_NAME')
    COLLISION_GROUP_NAME: list = maya_scene_data.current_project_setting.get('COLLISION_GROUP_NAME')
    # エラー表示の色設定
    checker.result.color = [50, 140, 170]


    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node:data.CustomNodeData = node

            # シェイプがないノードは見ない
            if not node.shapes:
                continue

            # メッシュがないトランスフォームを排排除
            if not node.has_mesh:
                continue

            # コンポーネントの検出の場合このif 文を使って大きさのないポリゴンを排除できる
            if node.full_path_name in check_result.no_polygon_mesh:
                continue

            # シェイプがないものを排除
            if not node.shapes:
                continue

            # コリジョングループは見ない
            if  node.category_group == COLLISION_GROUP_NAME:
                continue

            remove_uv_sets:list = []
            _uv_sets = cmds.polyUVSet(node.full_path_name, q=True, allUVSets=True)

            # uv セットがない場合
            if not _uv_sets:
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append("Not Exists UV Set")

            else:

                for _uv_set in _uv_sets:
                    _exists_flag: bool = False
                    if _uv_set in KEEP_UV_SET_NAME:
                        _exists_flag = True
                    else:
                        remove_uv_sets.append(_uv_set)

                # 必要なuv セットがない場合
                # if not _exists_flag:
                #     checker.result.error_nodes.append(node.full_path_name)
                #     checker.result.error_message_list.append(f'Not Exists UV Set: {KEEP_UV_SET_NAME}')

                # 不要なUVセットを格納
                if len(_uv_sets) != 1:
                    checker.result.error_nodes.append(node.full_path_name)
                    checker.result.error_message_list.append("Multiple UV Sets")
                    checker.result.remove_target_uv_sets[node.full_path_name] = remove_uv_sets



def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    if modify_data and modify_data.error_nodes:
        for node in modify_data.error_nodes:
            if not cmds.objExists(node):
                continue

            remove_uv_sets = modify_data.remove_target_uv_sets.get(node)
            if remove_uv_sets:
                for uv_set in remove_uv_sets:
                    try:
                        cmds.polyUVSet(delete=True, uvSet=uv_set)
                        modify_result.modify_flag = True
                        modify_result.modify_messages.append(f'remove uv set {node}')
                        print("{:-<100}  {}".format(node, "remove uv set"))
                    except Exception as e:
                        modify_result.error_flag = True
                        modify_result.error_messages.append(f'!!Could Not remove uv set {node}')
                        print("{:+<100}  {}".format(node, "remove uv set error"))

