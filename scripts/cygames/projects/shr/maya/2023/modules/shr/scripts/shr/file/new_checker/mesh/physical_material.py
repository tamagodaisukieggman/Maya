import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

import yaml

from maya import cmds
from .. import scene_data
from . import material


material_list_path = "z:/mtk/work/engine/material/material.matdecl"

_collision_group_name = "collision"



# 物理マテリアルを見に行く
def load_yaml(material_list_path):
    with open(material_list_path) as f:
        _items = yaml.safe_load(f)
        print(list(_items.keys())[0])
        print(list(_items.values())[0])


# 物理マテリアルのアトリビュートの設定
PHY_MATERIAL_NAME = "phyMaterialName"
PHT_MATERIALS = [
"default",
"metal000",
"stone000",
"wood000",
"wood001",
"grass000",
"grass002",
"bush000",
"bush001",
"gravel000",
"gravel001",
"mud000",
"mud001",
"water000",
"rock000",
"cloth000",
"straw000",
"moss000",
"rubble000",
"ivy000",
"leaf000",
"bigleaf000",
        ]




NO_CHECK_COLLISION = [
    "col_player",
    "col_camera",
    "col_sight",
]


def check(data_type="env", scene_path="", nodes=None):

    _result_datas = scene_data.ResultDatas()

    for node in nodes:
        _result = scene_data.ResultData()

        materials = material.get_assign_materials(node)
        if not materials:
            continue

        mesh_name_split = node.split("|")
        if _collision_group_name in mesh_name_split:

            collision_name_check = mesh_name_split[mesh_name_split.index(_collision_group_name)+1]
            if collision_name_check in NO_CHECK_COLLISION:
                continue

            for _material in materials:

                _exists = _result_datas.is_exists_nodes(_material)
                if _exists:
                    continue

                if not cmds.attributeQuery(PHY_MATERIAL_NAME, node=_material, exists=True):
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = "物理マテリアル設定がない"
                    _result.error_nodes = [_material]
                elif not cmds.getAttr("{}.{}".format(_material, PHY_MATERIAL_NAME)):
                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = "物理マテリアル設定がない"
                    _result.error_nodes = [_material]

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""
    return success, message