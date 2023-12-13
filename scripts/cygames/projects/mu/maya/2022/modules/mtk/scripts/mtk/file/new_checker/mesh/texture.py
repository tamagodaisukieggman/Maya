import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

import os
from maya import cmds
from .. import scene_data

from . import material

_mat_prefix = "mtl"
_mutsunokami_path = "z:/mtk/work"
_tex_prefix = "tex_"

def check(data_type="env", scene_path="", nodes=None):
    # 背景はMayaでテクスチャを確認するわけではないのでチェックしない
    if data_type == "env":
        return

    base_name = os.path.basename(scene_path)
    name_base = os.path.splitext(base_name)[0]
    _name_check = name_base.split("_",1)[-1]
    _name_check = "_".join(_name_check.split("_")[:2])

    _result_datas = scene_data.ResultDatas()

    for node in nodes:
        _result = scene_data.ResultData()

        # マテリアルなので一応大きさがないものも確認しておく
        # bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)
        # if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
        #     continue

        # _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]

        materials = material.get_assign_materials(node)

        if not materials:
            continue

        for _material in materials:
            _exists = _result_datas.is_exists_nodes(_material)
            if _exists:
                continue
            _file_nodes = cmds.ls(cmds.listConnections(_material,
                                                source=True,
                                                destination=False),
                                                type="file")

            for _file_node in _file_nodes:
                _exists = _result_datas.is_exists_nodes(_file_node)
                if _exists:
                    continue
                _textrue_file_path = cmds.getAttr(f'{_file_node}.ftn').lower().replace(os.sep, '/')
                if not _textrue_file_path:
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = "テクスチャが存在しない"
                    _result.error_nodes = [_file_node]

                elif not os.path.exists(_textrue_file_path):
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = "テクスチャが存在しない"
                    _result.error_nodes = [_file_node]

                elif len(_textrue_file_path.split(_mutsunokami_path)) != 2:
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = f"[ {_mutsunokami_path} ] にない"
                    _result.error_nodes = [_file_node]

                else:
                    _basename = os.path.basename(_textrue_file_path)
                    if not _basename.startswith(_tex_prefix):
                        _result.error = ERROR
                        _result.category = CATEGORY
                        _result.data_type = data_type
                        _result.error_text = f"[ {_tex_prefix} ] で始まってない"
                        _result.error_nodes = [_file_node]

                    else:
                        _name = os.path.splitext(_basename)[0].split(_tex_prefix)[-1]
                        if not _name.startswith(_name_check):
                            _result.error = ERROR
                            _result.category = CATEGORY
                            _result.data_type = data_type
                            _result.error_text = f"[ {_tex_prefix}{_name_check} ] で始まってない"
                            _result.error_nodes = [_file_node]

                        else:
                            _size_x = int(cmds.getAttr("{}.outSizeX".format(_file_node)))
                            _size_y = int(cmds.getAttr("{}.outSizeY".format(_file_node)))
                            if _size_x & (_size_x - 1) != 0 or _size_y & (_size_y - 1) != 0:
                                _result.error = ERROR
                                _result.category = CATEGORY
                                _result.data_type = data_type
                                _result.error_text = "テクスチャサイズが２のべぎ乗ではない"
                                _result.error_nodes = [_file_node]


        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message