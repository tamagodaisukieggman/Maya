# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds


def _check_controller(node):

    errors = []
    _ctrl_sets_name = "CtrlSet"
    _ctrl_sets = cmds.ls(_ctrl_sets_name, long=True)
    
    if not _ctrl_sets:
        return []

    for _ctrl in cmds.sets(_ctrl_sets, q=True):
        _constraint = cmds.listRelatives(_ctrl, type="constraint", fullPath=True)
        if _constraint:
            errors.append(_ctrl)
        if not _ctrl.endswith("_ctrl"):
            errors.append(_ctrl)
        else:
            if [abs(round(x)) for x in cmds.getAttr("{}.t".format(_ctrl))[0]] != [0.0, 0.0, 0.0]:
                errors.append(_ctrl)
            if [abs(round(x)) for x in cmds.getAttr("{}.r".format(_ctrl))[0]] != [0.0, 0.0, 0.0]:
                errors.append(_ctrl)
            if [abs(round(x)) for x in cmds.getAttr("{}.s".format(_ctrl))[0]] != [1.0, 1.0, 1.0]:
                errors.append(_ctrl)


    return errors