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
    checker.result.color = [128, 51, 128]

    for root_node in maya_scene_data.root_nodes:
        root_node:data.RootNodeData = root_node

        # チェック除外のルートノードを排除
        if root_node.full_path_name in check_result.no_confirmation_required_nodes:
            continue

        for node in root_node.all_descendents:
            if node.shapes:
                for shape in node.shapes:
                    materials = check_result.mesh_shape_materials.get(shape.full_path_name)
                    if materials:
                        for material in materials:
                            file_nodes = cmds.ls(cmds.listConnections(material,
                                                                source=True,
                                                                destination=False),
                                                                type="file")

                            if file_nodes:
                                continue






def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return
