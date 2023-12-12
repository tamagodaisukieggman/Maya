import re
from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

def get_assign_materials(node=""):
    # ノードに適用されたshadingEngine を全て返す
    materials = []
    shading_engines = cmds.listConnections(node,
                                        source=False,
                                        destination=True,
                                        type='shadingEngine')

    if not shading_engines:
        return materials

    shading_engines = list(set(shading_engines))

    for sg in shading_engines:
        materials = cmds.listConnections(sg + '.surfaceShader')
    return materials

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    if maya_scene_data.current_category == 'ANIMATION':
        return

    # エラー表示の色設定
    checker.result.color = [128, 77, 77]

    # マテリアルのプレフィックス
    MATERIAL_PREFIX: str = maya_scene_data.current_project_setting.get('MATERIAL_PREFIX')

    # コリジョングループの名前
    COLLISION_GROUP_NAME: str = maya_scene_data.current_project_setting.get('COLLISION_GROUP_NAME')

    # コリジョンマテリアルのプリフィックス
    COLLISION_MATERIAL_NAME_PREFIX: str = maya_scene_data.current_project_setting.get('COLLISION_MATERIAL_NAME_PREFIX')

    # 物理マテリアルアトリビュート
    PHY_MATERIAL_ATTRIBUTE_NAME: str = maya_scene_data.current_project_setting.get('PHY_MATERIAL_ATTRIBUTE_NAME')

    # 末尾に数字が使われているものを検出
    pattern = re.compile(r'\d+$')

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node:data.CustomNodeData = node
            if node.shapes:
                for shape in node.shapes:
                    shape:data.CustomNodeData = shape

                    # メッシュシェイプ以外は排除
                    if shape.node_type != 'mesh':
                        continue

                    # 中間オブジェクトは排除
                    if shape.full_path_name in check_result.intermediate_objects:
                        continue

                    # polySurfaceShape は排除
                    if shape.full_path_name.rsplit('|')[-1].startswith('polySurfaceShape'):
                        continue

                    check_prefix = MATERIAL_PREFIX
                    shape_name_split:list = shape.full_path_name.split('|')

                    # コリジョングループ以下のメッシュはプレフィックスを切り替える
                    # if shape_name_split[2] == COLLISION_GROUP_NAME:
                    #     check_prefix = COLLISION_MATERIAL_NAME_PREFIX

                    materials = get_assign_materials(node=shape)

                    # マテリアルがないもの検出
                    if not materials:
                        checker.result.error_nodes.append(shape.full_path_name)
                        checker.result.error_compornent[shape.full_path_name] = [shape.full_path_name, material]
                        checker.result.error_message_list.append("Not Assign Material")
                    else:

                        # 複数マテリアルの検出
                        check_result.mesh_shape_materials[shape.full_path_name] = materials
                        if check_prefix == MATERIAL_PREFIX and len(materials) != 1:
                            checker.result.error_nodes.append(node.full_path_name)
                            checker.result.error_message_list.append(f"Error Multiply Mateiral [{node.short_name}]")
                        for material in materials:

                            # 大文字検出
                            is_upper_flag = re.search('[A-Z]', material)
                            if is_upper_flag:
                                checker.result.error_nodes.append(material)
                                checker.result.error_message_list.append(f"Error Mateiral Name in Upper: [{material}]")

                            # マテリアルのプレフィックス検査
                            if check_prefix and not material.startswith(check_prefix) and node.full_path_name not in checker.result.error_nodes:
                                checker.result.error_nodes.append(node.full_path_name)
                                checker.result.error_message_list.append(f"Error Mateiral Prefix [{check_prefix}]: [{material}]")
                            elif check_prefix == COLLISION_MATERIAL_NAME_PREFIX:

                                # 物理マテリアルの場合マテリアルにアトリビュートが付けられる
                                if not cmds.attributeQuery(PHY_MATERIAL_ATTRIBUTE_NAME, node=material, exists=True):
                                    checker.result.error_nodes.append(node.full_path_name)
                                    checker.result.error_message_list.append(f"Error Physical Material Attribute: [{material}]")

                            # 背景以外は最後が数字ではない
                            if maya_scene_data.current_category != 'ENVIRONMENT':
                                result = pattern.search(material)
                                if result:
                                    checker.result.error_nodes.append(node.full_path_name)
                                    checker.result.error_message_list.append(f"Error Mateiral Name Suffix [{result.group()}]: [{material}]")





def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return
