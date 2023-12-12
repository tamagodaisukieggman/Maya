from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

import re

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    if maya_scene_data.current_category != 'CHARACTER':
        return

    # エラー表示の色設定
    checker.result.color = [77, 100, 128]

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node:data.CustomNodeData = node

            if node.shapes:
                sharpe_count:int = 0
                for shape in node.shapes:
                    shape:data.CustomNodeData = shape

                    if shape.full_path_name in check_result.intermediate_objects:
                        continue

                    sharpe_count += 1
                    if shape.node_type != 'mesh':
                        continue

                    # メッシュのシェイプノードの名前が、トランフォームノードの名前 + Shape であるかを確認

                    # body_parts01_lod1Shape の場合
                    node_base_shape_name = f'{node.short_name}Shape'
                    if node_base_shape_name != shape.short_name:
                        checker.result.error_nodes.append(shape.full_path_name)
                        checker.result.error_message_list.append(f'Error Shape Name: [{ node_base_shape_name}] [{shape.short_name}]')

                    # # body_parts01_lodShape1 の場合
                    # pattern = re.compile(r'\d+$')
                    # pattern_result = pattern.search(node.short_name)
                    # if pattern_result:
                    #     node_base_shape_name:str = f'{node.short_name}Shape{pattern_result.group()}'
                    # else:
                    #     node_base_shape_name:str = f'{node.short_name}Shape'

                    # if node_base_shape_name != shape.short_name:
                    #     checker.result.error_nodes.append(shape.full_path_name)
                    #     checker.result.error_message_list.append(f'Error Shape Name: [{node.short_name}] [{shape.short_name}]')
                if sharpe_count != 1:
                    checker.result.error_nodes.append(node.full_path_name)
                    checker.result.error_message_list.append(f'Multiply Shape Nodes: [{node.short_name}]')


def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    if modify_data and modify_data.error_nodes:
        for node in modify_data.error_nodes:
            if not cmds.objExists(node):
                continue

            transform_node:str = cmds.listRelatives(node, parent=True, path=True)[0]
            node_short_name:str = node.rsplit('|', 1)[-1]
            from_transform_node_name:str = f'{transform_node}Shape'
            try:
                cmds.rename(node, from_transform_node_name)
                # 修正成功フラグ
                modify_result.modify_flag = True
                modify_result.modify_messages.append(f'rename Node : {node_short_name} > {from_transform_node_name}')
                print("{:-<100}  {}".format(from_transform_node_name, "rename Node"))
            except Exception as e:

                # 修正失敗フラグ
                modify_result.error_flag = True
                modify_result.error_messages.append(f'!!Could Not Rename {node_short_name} > {from_transform_node_name}')
                print("{:+<100}  {}".format(node, "rename Node error"))
