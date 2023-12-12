# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



def _check_transform_rootjoint(node):
    errors = []
    _root_joint = "jnt_0000_skl_root"
    # _root_joint = "root_jnt"
    joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")
    
    if not joints:
        return []
    
    name_error_flag = False
    root_jnts = [x for x in joints if x.split("|")[-1] == _root_joint]
    
    if not root_jnts:
        name_error_flag = True
        errors.append(node)

    if not name_error_flag:
        root_jnt = root_jnts[0]

        error_flag = False

        if [abs(round(x,2)) for x in cmds.getAttr("{}.t".format(root_jnt))[0]] != [0.0, 0.0, 0.0]:
            # print([abs(round(x,2)) for x in cmds.getAttr("{}.t".format(root_jnt))[0]],"----trans")
            error_flag = True
        if [abs(round(x,2)) for x in cmds.getAttr("{}.r".format(root_jnt))[0]] != [0.0, 0.0, 0.0]:
            # print([abs(round(x,2)) for x in cmds.getAttr("{}.r".format(root_jnt))[0]],"----rot")
            error_flag = True
        if [abs(round(x,2)) for x in cmds.getAttr("{}.s".format(root_jnt))[0]] != [1.0, 1.0, 1.0]:
            # print([abs(round(x,2)) for x in cmds.getAttr("{}.s".format(root_jnt))[0]],"-----sca")
            error_flag = True
        if [abs(round(x,2)) for x in cmds.getAttr("{}.jointOrient".format(root_jnt))[0]] != [0.0, 0.0, 0.0]:
            # print([abs(round(x,2)) for x in cmds.getAttr("{}.jointOrient".format(root_jnt))[0]],"-----jo")
            error_flag = True
        if [abs(round(x,2)) for x in cmds.getAttr("{}.rotatePivot".format(root_jnt))[0]] != [0.0, 0.0, 0.0]:
            # print([abs(round(x,2)) for x in cmds.getAttr("{}.rotatePivot".format(root_jnt))[0]],"---rp")
            error_flag = True
        if [abs(round(x,2)) for x in cmds.getAttr("{}.scalePivot".format(root_jnt))[0]] != [0.0, 0.0, 0.0]:
            # print([abs(round(x,2)) for x in cmds.getAttr("{}.scalePivot".format(root_jnt))[0]],"----sp")
            error_flag = True
        
        if error_flag:
            errors.append(root_jnt)

    return errors