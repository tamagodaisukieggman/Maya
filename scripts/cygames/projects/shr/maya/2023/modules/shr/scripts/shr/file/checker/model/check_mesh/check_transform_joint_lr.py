# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import maya.api.OpenMaya as om2
from maya import cmds

_LEFT = "_L"

def _check_transform_joint_lr(node):

    if not node:
        return []

    errors = []

    joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")
    joint_short_names = [x.split("|")[-1] for x in joints]

    if not joints:
        return []
    

    for joint in joints:
        joint_short_name = joint.split("|")[-1]
        name_split = joint_short_name.split("_")

        if len(name_split) > 4 and "L" in name_split[4]:

            same_type_joints = [x for x in joint_short_names if len(x.split("_")) > 4 and x.split("_")[2] == name_split[2] and x.split("_")[3] == name_split[3] and "R" in x.split("_")[4]]
            
            sym_name = ""

            if not same_type_joints:
                continue

            if len(same_type_joints) != 1:
                if len(name_split[4]) != 1:
                    _check = name_split[4][0]
                    same_type_joint = [x for x in same_type_joints if x.split("_")[4][0] == _check]

                elif len(name_split) > 5:
                    same_type_joint = [x for x in same_type_joints if x.split("_")[-1] == name_split[-1]]

                if same_type_joint:
                    sym_name = same_type_joint[0]
            else:
                sym_name = same_type_joints[0]
            
            if not sym_name:
                continue

            sym_joint = cmds.ls(sym_name, long=True)[0]

            _l_joint_position = [round(x,2) for x in cmds.joint(joint, q=True, position=True)]
            _r_joint_position = [round(x,2) for x in cmds.joint(sym_joint, q=True, position=True)]
            _l_joint_orientation = om2.MVector([round(x,2) for x in cmds.getAttr("{}.r".format(joint))[0]])
            _r_joint_orientation = om2.MVector([round(x,2) for x in cmds.getAttr("{}.r".format(sym_joint))[0]])
            # _l_joint_orientation = [round(x,2) for x in cmds.joint(joint, q=True, orientation=True)]
            # _r_joint_orientation = [round(x,2) for x in cmds.joint(sym_joint, q=True, orientation=True)]

            if [_l_joint_position[0]*-1,_l_joint_position[1],_l_joint_position[2]] != _r_joint_position:
                errors.append(sym_joint)
                # print(joint_short_name,"+++++")
                # print([_l_joint_position[0]*-1,_l_joint_position[1],_l_joint_position[2]], _r_joint_position)
            if _l_joint_orientation != -_r_joint_orientation or not _l_joint_orientation == _r_joint_orientation:
                if not [abs(x) for x in _l_joint_orientation] == [abs(x) for x in _r_joint_orientation]:
                    # ちょっと強引、、
                    errors.append(sym_joint)
                    # print(joint_short_name,"-----")
                    # print(_l_joint_orientation, _r_joint_orientation, -_r_joint_orientation)
                    # print([abs(x) for x in _l_joint_orientation],[abs(x) for x in _r_joint_orientation])
                    # print([abs(x) for x in _l_joint_orientation] == [abs(x) for x in _r_joint_orientation])
                    # print("-------------\n")

    return errors