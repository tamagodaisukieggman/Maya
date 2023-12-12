from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))

def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    if(maya_scene_data.current_category == 'ENVIRONMENT' or
       maya_scene_data.current_category == 'VAGETATIONS' or
       maya_scene_data.current_category == 'ANIMATION'
       ):
        return

    # エラー表示の色設定
    checker.result.color = [10, 100, 10]

    # セッティングから読み込むサンプル
    ATTRIBUTE_NUMBER_OF_DIGITS: list = maya_scene_data.current_project_setting.get('ATTRIBUTE_NUMBER_OF_DIGITS')

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            node:data.CustomNodeData = node

            # ジョイントオリエントの値チェック
            if node.node_type == 'joint':
                _orient_value_x = cmds.getAttr(f'{node.full_path_name}.jointOrientX')
                _orient_value_y = cmds.getAttr(f'{node.full_path_name}.jointOrientY')
                _orient_value_z = cmds.getAttr(f'{node.full_path_name}.jointOrientZ')
                _orient_value:list = [
                                    round(_orient_value_x, ATTRIBUTE_NUMBER_OF_DIGITS),
                                    round(_orient_value_y, ATTRIBUTE_NUMBER_OF_DIGITS),
                                    round(_orient_value_z, ATTRIBUTE_NUMBER_OF_DIGITS)
                                    ]
                if _orient_value != [0.0, 0.0, 0.0]:
                    checker.result.error_nodes.append(node.full_path_name)
                    checker.result.error_message_list.append("Joint Orient Value Error")
            else:

                if node.is_locator:
                    continue

                _os_scale_pivot = cmds.xform(node.full_path_name, q=True, scalePivot=True, objectSpace=True)
                _os_rotate_pivot = cmds.xform(node.full_path_name, q=True, rotatePivot=True, objectSpace=True)
                _ws_scale_pivot = cmds.xform(node.full_path_name, q=True, scalePivot=True, worldSpace=True)
                _ws_rotate_pivot = cmds.xform(node.full_path_name, q=True, rotatePivot=True, worldSpace=True)
                _os_scale_pivot = [round(x, ATTRIBUTE_NUMBER_OF_DIGITS) for x in _os_scale_pivot]
                _os_rotate_pivot = [round(x, ATTRIBUTE_NUMBER_OF_DIGITS) for x in _os_rotate_pivot]
                _ws_scale_pivot = [round(x, ATTRIBUTE_NUMBER_OF_DIGITS) for x in _ws_scale_pivot]
                _ws_rotate_pivot = [round(x, ATTRIBUTE_NUMBER_OF_DIGITS) for x in _ws_rotate_pivot]

                if(_os_rotate_pivot != [0.0, 0.0, 0.0] and
                   _os_scale_pivot != [0.0, 0.0, 0.0] and
                   _ws_scale_pivot != [0.0, 0.0, 0.0] and
                   _ws_rotate_pivot != [0.0, 0.0, 0.0]):
                    checker.result.error_nodes.append(node.full_path_name)
                    checker.result.error_message_list.append("Pivot Value Error")

                if not node.shapes:
                    continue

                _transform_value = cmds.xform(node.full_path_name, q=True, translation=True, objectSpace=True)
                _rotate_value = cmds.xform(node.full_path_name, q=True, rotation=True, objectSpace=True)

                _scale_value = cmds.getAttr("{}.s".format(node.full_path_name))[0]

                _transform_value = [round(x, ATTRIBUTE_NUMBER_OF_DIGITS) for x in _transform_value]
                _rotate_value = [round(x, ATTRIBUTE_NUMBER_OF_DIGITS) for x in _rotate_value]
                _scale_value = [round(x, ATTRIBUTE_NUMBER_OF_DIGITS) for x in _scale_value]

                # トランスフォームの値チェック、桁数丸める
                if _transform_value != [0.0, 0.0, 0.0]:
                    checker.result.error_nodes.append(node.full_path_name)
                    checker.result.error_message_list.append("Transform Value Error")

                # ローテーションの値チェック
                if _rotate_value != [0.0, 0.0, 0.0]:
                    checker.result.error_nodes.append(node.full_path_name)
                    checker.result.error_message_list.append("Rotation Value Error")

                # スケールの値
                if _scale_value != [1.0, 1.0, 1.0]:
                # if _scale_value != [1.0, 1.0, 1.0] and node.full_path_name not in checker.result.error_nodes:
                    checker.result.error_nodes.append(node.full_path_name)
                    checker.result.error_message_list.append("Scale Value Errir")

                if node.shapes:
                    for shape in node.shapes:
                        # 中間オブジェクトは排除
                        if shape.full_path_name in check_result.intermediate_objects:
                            continue


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