from pathlib import Path
import re
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

import maya.cmds as cmds
from .. import scene_data
from .. import settings

LAMBERT1 = 'lambert1'


def get_assign_materials(node="")->list:
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


def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    for node in check_targets:
        if cmds.getAttr("{}.intermediateObject".format(node)):
            continue

        bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            continue
        _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)
        _result = scene_data.ResultData()
        materials = get_assign_materials(node)

        if not materials:
            _result.error_type_message = ERROR
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = "No Materials"
            _result.error_nodes = _transform_node
            _result.error_type_color = [120, 60, 110]

        if LAMBERT1 in materials:
            _result.error_type_message = ERROR
            _result.checker_module = CHECKER
            _result.checker_category = CATEGORY
            _result.data_type_category = data_type_category
            _result.error_text = f'has material: [ {LAMBERT1} ]'
            _result.error_nodes = _transform_node
            _result.error_type_color = [120, 60, 110]

        for material in materials:
            is_upper_flag = re.search('[A-Z]', material)
            if is_upper_flag:
                _result.error_type_message = ERROR
                _result.checker_module = CHECKER
                _result.checker_category = CATEGORY
                _result.data_type_category = data_type_category
                _result.error_text = f'upper case: [ {material} ]'
                _result.error_nodes = material
                _result.error_type_color = [120, 60, 110]


        if _result.error_type_message:
            _result_datas.set_data_obj(_result)

    return _result_datas


def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    if isinstance(modify_targets, str):
        modify_targets = eval(modify_targets)
    if not modify_targets:
        return success, message
    return success, message