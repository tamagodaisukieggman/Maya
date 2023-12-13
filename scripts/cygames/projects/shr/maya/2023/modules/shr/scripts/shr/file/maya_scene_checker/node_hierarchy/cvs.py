from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CHECKER = _current_file.stem

from maya import cmds
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

from .. import scene_data
from .. import settings


def check_cvs_value(full_path="", dag_path=None, data_type_category="ENVIRONMENT", _result:scene_data.ResultData=None)->scene_data.ResultData:
    mesh_fn = None
    error_flag = False
    try:
        mesh_fn = om2.MFnMesh(dag_path)
    except Exception as e:
        print(f' {CHECKER}: {e}: [ {full_path} ]')
        pass

    if not mesh_fn:
        return _result

    plug = mesh_fn.findPlug('pnts', False)

    for i in range(plug.numElements()):
        _pos = plug.elementByPhysicalIndex(i).asMDataHandle().asFloat3()
        if str(_pos)  != '[0.0, 0.0, 0.0]':
            error_flag = True
            break

    if error_flag:
        _result.error_type_message = ERROR
        _result.checker_module = CHECKER
        _result.checker_category = CATEGORY
        _result.data_type_category = data_type_category
        _result.error_text = "CVs value exists"
        _result.error_nodes = [full_path]
    return _result

def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:

    _result_datas = scene_data.ResultDatas()

    if (data_type_category == 'ENVIRONMENT' or
        data_type_category == 'METAHUMAN'):
        return _result_datas

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    selList = om2.MSelectionList()

    for node in check_targets:

        _children = cmds.listRelatives(node, allDescendents=True, fullPath=True, type='mesh')
        if not _children:
            continue
        for _child in _children:

            _result = scene_data.ResultData()
            # bb_size = cmds.polyEvaluate(_child, boundingBox=True, accurateEvaluation=True)
            # if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            #     continue
            _transform_node = cmds.listRelatives(_child, parent=True, fullPath=True)[0]
            selList.add(_transform_node)

            if _result.error_type_message:
                _result_datas.set_data_obj(_result)

    if selList:
        for x in range(selList.length()):

            dagPath = selList.getDagPath(x)
            fullPath = dagPath.fullPathName()
            _result = scene_data.ResultData()
            check_cvs_value(fullPath, dagPath, data_type_category, _result)

            if _result.error_type_message:
                _result_datas.set_data_obj(_result)


    return _result_datas


def freeze_cvs_value(node:str=""):
    _parent = cmds.listRelatives(node, parent=True, fullPath=True)[0]
    cmds.select(_parent, replace=True)
    ltd = cmds.lattice(divisions=(2, 2, 2), objectCentered=True)
    cmds.delete(_parent, constructionHistory=True)
    cmds.select(clear=True)

    _pnts = cmds.getAttr(f"{node}.pnts[*]")
    zero_values = [0]*len(_pnts)*3
    cmds.setAttr(f"{node}.pnts[*]", *zero_values )


def modify(data_type="ENVIRONMENT", scene_path="", error_type_message="", modify_targets=None)->tuple:
    success = -1
    message = ""

    if isinstance(modify_targets, str):
        modify_targets = eval(modify_targets)
    if not modify_targets:
        return success, message

    for node in modify_targets:
        if not cmds.objExists(node):
            continue

        try:
            freeze_cvs_value(node)
            message = u"Reset [ CVs Values ] [ {} ]".format(node)
            print("{:-<100}  {}".format(node, "Reset CVs Values"))
            success = 1
        except Exception as e:
            message = u"!! Could Not Reset [ CVs Values ] [ {} ]".format(node)
            print("{:+<100}  {}".format(node, "Reset CVs Values error"))
            success = 0

    return success, message




