from pathlib import Path
_current_file = Path(__file__)
ERROR = " ".join(_current_file.stem.split("_"))
# CATEGORY = " ".join(_current_file.parent.stem.split("_"))
CATEGORY = _current_file.parent.stem
CHECKER = _current_file.stem

from maya import cmds
from .. import scene_data
from .. import settings


def check(data_type_category:str='ENVIRONMENT', scene_path:str='', check_targets:list=[])->scene_data.ResultDatas:
    _result_datas = scene_data.ResultDatas()

    if data_type_category == 'ENVIRONMENT':
        return _result_datas

    if isinstance(check_targets, str):
        check_targets = eval(check_targets)

    if not check_targets:
        return _result_datas

    for node in check_targets:
        _children = cmds.listRelatives(node, allDescendents=True, fullPath=True)
        if not _children:
            continue
        for _child in _children:
            _result = scene_data.ResultData()
            # bb_size = cmds.polyEvaluate(_child, boundingBox=True, accurateEvaluation=True)
            # if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            #     continue
            if cmds.getAttr("{}.intermediateObject".format(_child)):
                _result.error_type_message = ERROR
                _result.checker_module = CHECKER
                _result.checker_category = CATEGORY
                _result.data_type_category = data_type_category
                _result.error_text = "Intermediate Object"
                _result.error_nodes = [_child]
                _result.error_type_color = [175, 130, 90]

            if _result.error_type_message:
                _result_datas.set_data_obj(_result)

    return _result_datas


def deleteIntermediate(node:str='', sDivisions:int=3, tDivisions:int=3, uDivisions:int=3):
    _parent = cmds.listRelatives(node, parent=True, fullPath=True, type='transform')[0]
    #cmds.delete(node)
    _children = cmds.listRelatives(_parent, children=True, fullPath=True, type='mesh')
    # for _ch in _children:
    #     mesh_node = _ch

    tempTransform = cmds.createNode('transform', skipSelect=True, name=f'tmp_{_parent}')
    tempLattice = cmds.createNode('lattice', skipSelect=True, name=f'tmp_{_parent}Shape', parent=tempTransform)
    tempBaseTransform = cmds.createNode('transform', skipSelect=True, name=f'tmpBase_{_parent}')
    tempBaseLattice = cmds.createNode('baseLattice', skipSelect=True, name=f'tmpBase_{_parent}Shape', parent=tempBaseTransform)
    ffd = cmds.createNode('ffd', skipSelect=True, name=f'tmpFfd_{_parent}')
    # print(_parent, tempTransform, tempLattice , " --------------------")

    cmds.setAttr(tempLattice+'.sDivisions',sDivisions)
    cmds.setAttr(tempLattice+'.tDivisions',tDivisions)
    cmds.setAttr(tempLattice+'.uDivisions',uDivisions)

    cmds.delete(_parent, constructionHistory=True)


def freeze_cv_value(node:str=""):
    _parent = cmds.listRelatives(node, parent=True, fullPath=True)[0]
    cmds.delete(node)
    cmds.select(_parent, replace=True)
    ltd = cmds.lattice(divisions=(2, 2, 2), objectCentered=True)
    cmds.delete(_parent, constructionHistory=True)
    cmds.select(clear=True)

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
        if cmds.getAttr("{}.intermediateObject".format(node)):
            _transform_node = cmds.listRelatives(node, parent=True, fullPath=True)[0]
            _historys = cmds.listHistory(_transform_node, pruneDagObjects=True, interestLevel=2)
            if _historys:
                skinCluster = [x for x in _historys if cmds.nodeType(x) == 'skinCluster']
                if skinCluster:
                    message = u"!! Skinning mesh Could Not Delete [ Intermediate Object ] [ {} ]".format(node)
                    success = 0
                    continue
            try:
                # deleteIntermediate(node)
                freeze_cv_value(node)
                message = u"Delete [ Intermediate Object ] [ {} ]".format(node)
                # print("{:-<100}  {}".format(node, "delete Intermediate Object"))
                success = 1
            except Exception as e:
                message = u"!! Could Not Delete [ Intermediate Object ] [ {} ]".format(node)
                # print("{:+<100}  {}".format(node, "delete Intermediate Object  error"))
                success = 0

    return success, message
