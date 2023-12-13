from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

import re

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    if maya_scene_data.current_category == 'ANIMATION':
        return

    NAME_SPACE:str = ':'


    # 第一階層の命名、ノードタイプチェック
    MODEL_GROUP_NODE_NAME:dict = maya_scene_data.current_project_setting.get('MODEL_GROUP_NODE_NAME')

    if maya_scene_data.current_category == 'ENVIRONMENT':
        MODEL_GROUP_NODE_TYPE:dict = maya_scene_data.current_project_setting.get('MODEL_GROUP_NODE_TYPE_ENVIRONMENT')
    else:
        MODEL_GROUP_NODE_TYPE:dict = maya_scene_data.current_project_setting.get('MODEL_GROUP_NODE_TYPE_CHARACTER')
    _model_group_nodetype:str = MODEL_GROUP_NODE_TYPE.get(MODEL_GROUP_NODE_NAME)

    LOD_GROUP_NAME_STARTSWITH:dict = maya_scene_data.current_project_setting.get('LOD_GROUP_NAME_STARTSWITH')
    LOD_START_COUNT:dict = maya_scene_data.current_project_setting.get('LOD_START_COUNT')
    LOD_GROUP_TYPE:dict = maya_scene_data.current_project_setting.get('LOD_GROUP_TYPE_CHARA')

    if maya_scene_data.current_category == 'ENVIRONMENT':
        LOD_GROUP_TYPE:dict = maya_scene_data.current_project_setting.get('LOD_GROUP_TYPE_ENV')

    COLLISION_GROUP_NAME_TYPE:dict = maya_scene_data.current_project_setting.get('COLLISION_GROUP_NAME_TYPE')

    JOINT_TYPE_NAME:dict = maya_scene_data.current_project_setting.get('JOINT_TYPE_NAME')

    SUBLEVELNAME:dict = maya_scene_data.current_project_setting.get('SUBLEVELNAME')
    if maya_scene_data.current_category == 'RIG':
        SUBLEVELNAME:dict = maya_scene_data.current_project_setting.get('SUBLEVELNAME_RIG')

    SUBLEVELNAME_RIG_RIGGROUP:dict = maya_scene_data.current_project_setting.get('SUBLEVELNAME_RIG_RIGGROUP')

    # エラー表示の色設定
    checker.result.color = [77, 128, 128]

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        _model_group_exists:bool = False
        _model_group_type_error:bool = False
        _joint_exists:bool = False
        _collision_group_exists:bool = False
        _lod_group_exists:bool = False
        _lod_num_error:str = ''
        lod_num:int = LOD_START_COUNT
        _rig_group:bool = False

        # リグデータではルートにあるノードもチェックする
        if maya_scene_data.current_category == 'RIG':
            if root_node.node_name == 'rig':
                _rig_group = True
                SUBLEVELNAME = SUBLEVELNAME_RIG_RIGGROUP

        # ルートのネームスペース確認
        if NAME_SPACE in root_node.node_name:
            checker.result.error_nodes.append(root_node.full_path_name)
            checker.result.error_message_list.append(f'Has Name Space: [{root_node.node_name}]')

        for node in root_node.all_descendents:
            node:data.CustomNodeData = node

            # 第一階層チェック
            if node.deep == 2:

                # mesh グループチェック
                if node.short_name == MODEL_GROUP_NODE_NAME:
                    _model_group_exists = True
                    if _model_group_nodetype and node.node_type != _model_group_nodetype:
                        _model_group_type_error = True

                # collision グループチェック
                _collision_group_nodetype:str = COLLISION_GROUP_NAME_TYPE.get(node.short_name)
                if _collision_group_nodetype and node.node_type == _collision_group_nodetype:
                    _collision_group_exists = True

                # joint チェック
                if node.node_type == 'joint':
                    _joint_nodename:str = JOINT_TYPE_NAME.get(node.node_type)
                    if _joint_nodename:
                        if _joint_nodename != node.short_name:
                            checker.result.error_nodes.append(node.full_path_name)
                            checker.result.error_message_list.append(f'Joint Name Error: [{node.short_name}]')
                            _joint_exists = True
                else:
                    current_node_type:str = SUBLEVELNAME.get(node.short_name)
                    if not current_node_type:
                        checker.result.error_nodes.append(node.full_path_name)
                        checker.result.error_message_list.append(f'Unkown Node: [{node.short_name}]')
                    elif current_node_type != node.node_type:
                        checker.result.error_nodes.append(node.full_path_name)
                        checker.result.error_message_list.append(f'Node Type Error: [{node.short_name}]')

                if node.short_name == 'rig_grp' and node.full_path_name not in check_result.no_confirmation_required_nodes:
                    check_result.no_confirmation_required_nodes.append(node.full_path_name)

            if node.deep == 3:
                # LOD グループチェック
                if node.short_name.startswith(LOD_GROUP_NAME_STARTSWITH):
                    _lod_group_exists = True

                    # LOD グループの順番確認
                    _lod_name:str = f'{LOD_GROUP_NAME_STARTSWITH}{lod_num}'
                    if node.short_name != _lod_name:
                        _lod_num_error = node.full_path_name
                        checker.result.error_nodes.append(node.full_path_name)
                        checker.result.error_message_list.append(f'LOD Number Error: [{node.short_name}]')
                    lod_num += 1

            # ルート以下のネームスペース確認
            if NAME_SPACE in node.full_path_name:
                checker.result.error_nodes.append(node.full_path_name)
                checker.result.error_message_list.append(f'Has Name Space: [{node.short_name}]')

        # model グループはないといけない
        if not _model_group_exists:
            checker.result.error_nodes.append(root_node.full_path_name)
            checker.result.error_message_list.append(f'Not Exists [{ MODEL_GROUP_NODE_NAME }] Group: [{root_node.node_name}]')
        if _model_group_exists and _model_group_type_error:
            checker.result.error_nodes.append(root_node.full_path_name)
            checker.result.error_message_list.append(f'Node Type Error Not [{ _model_group_nodetype }] Group: [{root_node.node_name}]')

        # collision グループはワーニング　コリジョンはない場合もある
        # if not _collision_group_exists:
        #         checker.result.warning_nodes.append(root_node.full_path_name)
        #         checker.result.warning_message_list.append(f'Not Exists [collistion] Group: [{root_node.node_name}]')

        # LOD グループはエラー
        if maya_scene_data.current_category != 'ENVIRONMENT' and not _lod_group_exists:
                checker.result.error_nodes.append(root_node.full_path_name)
                checker.result.error_message_list.append(f'Not Exists [LOD] Group: [{root_node.node_name}]')


def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return
