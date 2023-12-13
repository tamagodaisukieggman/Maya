import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data

_mat_prefix = "mtl"

COLLISION_GROUP_NAME = "collision"


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



def check(data_type="env", scene_path="", nodes=None):

    _result_datas = scene_data.ResultDatas()

    for node in nodes:
        _result = scene_data.ResultData()
        node_split_name = node.split("|")

        # コリジョンは別のチェックなので排除
        if node_split_name[2] == COLLISION_GROUP_NAME:
            continue

        # マテリアルなので一応大きさがないものも確認しておく
        # bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)
        # if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
        #     continue

        _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]

        materials = get_assign_materials(node)
        if not materials:
            _result.error = ERROR
            _result.category = CATEGORY
            _result.data_type = data_type
            _result.error_text = "マテリアルがない"
            _result.error_nodes = [_transform_node]
            continue

        for _material in materials:
            _exists = _result_datas.is_exists_nodes(_material)
            if _exists:
                continue
            if not _material.startswith(_mat_prefix):
                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"プレフィックスが [ {_mat_prefix} ] ではない"
                _result.error_nodes = [_material, _transform_node]

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message