import pathlib
_current_file = pathlib.Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
ERROR_COLLISION_ATTRIBUTE = f"{ERROR}:collision attribute"
CATEGORY = " ".join(_current_file.parent.stem.split("_"))

from maya import cmds
from .. import scene_data

COLLISION_GROUP_NAME = "collision"

COL_NAME = "col"

COL_TYPES = [
            "character",
            "player",
            "camera",
            "detailed",
            "sight",
            "water",
            "bush",
            ]

PHY_COLLISION_ATTRIBUTE_LIST = [
                    "phyActorType",
                    "phyShapeType",
                    "phyCollisionTypeName",
                    "phyQueryFilterPresetName",
                    ]


PHY_COLLISION_ATTRIBUTE_VALUES = {
    "default":
    {
            "phyActorType": "default",
            "phyShapeType": "default",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "object",
    },
    "mesh_detailed":
    {
            "phyActorType": "default",
            "phyShapeType": "default",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "object",
    },
    "mesh":
    {
            "phyActorType": "default",
            "phyShapeType": "default",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "detailed_object",
    },
    "col_character_detailed":
    {
            "phyActorType": "default",
            "phyShapeType": "default",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "object_without_camera",
    },
    "col_character":
    {
            "phyActorType": "default",
            "phyShapeType": "default",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "detailed_object_without_camera",
    },
    "col_player":
    {
            "phyActorType": "default",
            "phyShapeType": "No Simulation",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "player",
    },
    "col_camera":
        {
            "phyActorType": "default",
            "phyShapeType": "No Simulation",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "camera",
    },
    "col_detailed":
        {
            "phyActorType": "default",
            "phyShapeType": "default",
            "phyCollisionTypeName": "detailed",
            "phyQueryFilterPresetName": "detailed",
    },
    "col_sight":
        {
            "phyActorType": "default",
            "phyShapeType": "No Simulation",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "sight",
    },
    "col_water":
    {
            "phyActorType": "default",
            "phyShapeType": "default",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "water_surface",
    },
    "col_bush":
    {
            "phyActorType": "default",
            "phyShapeType": "No Simulation",
            "phyCollisionTypeName": "default",
            "phyQueryFilterPresetName": "bush",
    },
}



def check_collision(data_type="env", nodes=[]):

    _detailed_flag = [x for x in nodes if x.endswith("detailed")]
    _result_datas = scene_data.ResultDatas()

    for col_cld in nodes:
        _result = scene_data.ResultData()
        col_short_name = col_cld.split("|")[-1]

        # 「collision」グループ以下にグループノードがある場合のチェック
        # 直接メッシュの場合は、命名は見ずにアトリビュートだけ見る
        # 「_」一つで区切られている
        # 「col」で始まる
        # "character",　"player", "camera", "detailed", "sight", "water"
        # で終わる

        _name_error_flag = False
        _collision_type = ""

        if not cmds.listRelatives(col_cld, s=True, path=True):
            split_name = col_short_name.split("_")
            if len(split_name) == 2:
                if split_name[0] != "col":
                    _name_error_flag = True

                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = f'[ {split_name[0]} ]_{"_".join(split_name[1:])} 不正な命名 [col]_ でない'
                    _result.error_nodes = [col_cld]

                elif split_name[-1] not in COL_TYPES:
                    _name_error_flag = True

                    _result.error = ERROR
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = f'{split_name[0]}_[ {"_".join(split_name[1:])} ] 不正な命名 col_[type] でない'
                    _result.error_nodes = [col_cld]

                else:
                    _collision_type = "col_{}".format(split_name[-1])
            elif col_cld not in _result.error_nodes:
                _name_error_flag = True

                _result.error = ERROR
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"[ {col_short_name} ] 不正な命名　[col_type] でない"
                _result.error_nodes = [col_cld]

        else:
            _collision_type = "mesh"

        _attr_error_flag = False

        for _attr in PHY_COLLISION_ATTRIBUTE_LIST:

            if not cmds.attributeQuery(_attr, node=col_cld, exists=True):
                _attr_error_flag = True

                _result.error = ERROR_COLLISION_ATTRIBUTE
                _result.category = CATEGORY
                _result.data_type = data_type
                _result.error_text = f"[ {_attr} ] アトリビュートがない"
                _result.error_nodes = [col_cld]
                break

        if not _name_error_flag and not _attr_error_flag:
            inside_group_clds = cmds.listRelatives(col_cld, c=True, path=True)
            if not inside_group_clds:
                continue

            if _detailed_flag:
                if _collision_type == "col_character" or _collision_type == "mesh":
                    _collision_type += "_detailed"

            for _attr, _value in PHY_COLLISION_ATTRIBUTE_VALUES[_collision_type].items():
                current_value = cmds.getAttr("{}.{}".format(col_cld, _attr))
                if current_value != _value:
                    _result.error = ERROR_COLLISION_ATTRIBUTE
                    _result.category = CATEGORY
                    _result.data_type = data_type
                    _result.error_text = "ｱﾄﾘﾋﾞｭｰﾄの値が　[ detailed_object_without_camera ] ではない"
                    _result.error_nodes = [col_cld]

        if _result.error:
            _result_datas.set_data_obj(_result)

    return _result_datas

def check(data_type="env", scene_path="", nodes=None):
    _result_datas = None

    for _cld in cmds.listRelatives(nodes, children=True, fullPath=True):
        _cld_short_name = _cld.split("|")[-1]

        if _cld_short_name == COLLISION_GROUP_NAME:
            col_clds = cmds.listRelatives(_cld, children=True, fullPath=True)
            if col_clds:
                _result_datas = check_collision(data_type, col_clds)

    return _result_datas

def add_attribute(node):

    _result = []

    for _attr in PHY_COLLISION_ATTRIBUTE_LIST:
        if not cmds.attributeQuery(_attr, n=node, ex=True):
                cmds.addAttr(node, longName=_attr,
                            dataType="string"
                            )
                _result.append([node, _attr])

    return _result

def chenge_collision_attr(node):
    node_short_name = node.split("|")[-1]
    detaild_flag = False
    _result = []
    _parent = cmds.listRelatives(node, parent=True, fullPath=True, type="transform")
    for _brother in cmds.listRelatives(_parent,
                                        children=True,
                                        fullPath=True,
                                        type="transform"):
        _brother_short_name = _brother.split("|")[-1]
        if "col_detailed" in _brother_short_name:
            detaild_flag = True
            break

    # コリジョンタイプからアトリビュートを適用する準備
    if node_short_name in PHY_COLLISION_ATTRIBUTE_VALUES:
        col_type = node_short_name
    else:
        col_type = "default"

    # ディテールコリジョンのあるなし、キャラクターコリジョンで分岐
    current_attr_settings = PHY_COLLISION_ATTRIBUTE_VALUES.get(col_type, None)
    if current_attr_settings:
        for _attr, setting in current_attr_settings.items():
            if(node_short_name == "col_character" and
                    "phyQueryFilterPresetName" == _attr):
                if detaild_flag:
                    cmds.setAttr('{}.{}'.format(node, _attr),
                                        "object_without_camera", type="string")
                else:
                    cmds.setAttr('{}.{}'.format(node, _attr),
                                        "detailed_object_without_camera", type="string")
                _result.append([node, _attr])
            else:
                if cmds.getAttr("{}.{}".format(node, _attr)) != setting:
                    cmds.setAttr('{}.{}'.format(node, _attr), setting, type="string")
                    _result.append([node, _attr])

    return _result

def modify(data_type="env", scene_path="", error_detail="", node=None):
    success = -1
    message = ""

    if error_detail == "collision attribute":
        _collision_attr = add_attribute(node)

        if _collision_attr:
            success = 1
            _collision_attr = _collision_attr[0]
            print("{:-<100}  {}  [ {} ]".format(_collision_attr[0],
                                                "Add Collision Attribute",
                                                _collision_attr[1]))

            message += f"[ {_collision_attr[0]} ] に "
            message += f"[ {_collision_attr[1]} ] のコリジョンアトリビュート追加\n"

        _collision_attr_modify = chenge_collision_attr(node)
        if _collision_attr_modify:
            success = 1
            _collision_attr_modify = _collision_attr_modify[0]

            print("{:-<100}  {}  [ {} ]".format(_collision_attr_modify[0],
                                                "Modify Collision Attribute",
                                                _collision_attr_modify[1]))

            message += f"[ {_collision_attr_modify[0]} ] の "
            message += f"[ {_collision_attr_modify[1]} ] のコリジョンアトリビュート変更\n"

    return success, message