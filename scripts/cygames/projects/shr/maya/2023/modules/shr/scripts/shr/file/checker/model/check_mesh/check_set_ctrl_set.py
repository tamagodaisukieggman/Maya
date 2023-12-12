# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds

def get_set_menbers(_set):
    _sets = []
    if cmds.nodeType(_set) == "objectSet":
        _menbers = cmds.sets(_set, q=True)
        for _menber in _menbers:
            res = get_set_menbers(_menber)
            _sets.extend(res)
    else:
        _sets.append(_set)
    return _sets

def _check_set_ctrl_set():
    errors = []
    set_name = "CtrlSet"

    _ctrl_nodes = [x for x in cmds.ls("*_ctrl",
            type="transform") if cmds.listRelatives(x, p=False, type="nurbsCurve")]
    
    if not _ctrl_nodes:
        return errors

    _set = cmds.ls(set_name, type="objectSet")

    if not _set:
        return errors
    
    _all_set_menbers_func = get_set_menbers(_set)
    # print(len(_all_set_menbers_func))

    # _set_menber = cmds.sets(_set, q=True)
    # _all_set_menbers = []
    
    # for _menber in _set_menber:
    #     _menbers = cmds.sets(_menber, q=True)
    #     if _menbers:
    #         _all_set_menbers.extend(cmds.sets(_menber, q=True))
    #     else:
    #         _all_set_menbers.append(_menber)
    # print(len(_all_set_menbers))
    # print(set(_all_set_menbers_func) & set(_all_set_menbers))
    # print(sorted(_all_set_menbers_func))
    # print(sorted(_all_set_menbers))
    
    for _node in _ctrl_nodes:
        if not _node in _all_set_menbers_func:
            errors.append(_node)

    return errors