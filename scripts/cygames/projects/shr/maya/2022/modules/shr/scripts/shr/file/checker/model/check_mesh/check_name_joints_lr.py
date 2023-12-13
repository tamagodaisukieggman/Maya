# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds

_LEFT = "_L_"
_RIGHT = "_R_"

_root_joint = "jnt_0000_skl_root"
_with_index_joint_names = ["skl", "face", "helper"]
_no_index_joint_names = ["mtp", "cnp", "move"]

def _check_name_joints_lr(node):
    if not node:
        return []

    joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")

    if not joints:
        return []
    # joints = cmds.ls(joints, dagObjects=True)
    errors = []

    _root_exists_flag = False

    for jnt in joints:
        jnt_short_name = jnt.split("|")[-1]

        if jnt_short_name == _root_joint:
            _root_exists_flag = True
        else:
            name_split = jnt_short_name.split("_")
            if len(name_split) != 1 and name_split[0] == "jnt":

                    parent_jnt = cmds.listRelatives(jnt, parent=True, fullPath=True)[0]
                    parent_jnt_short_name = parent_jnt.split("|")[-1]

                    if len(name_split) > 4 and name_split[4] == "L" and name_split[2] == _with_index_joint_names[0]:
                        brother_joints = [x for x in cmds.listRelatives(parent_jnt, children=True, fullPath=True) if len(x.split("|")[-1].split("_")) > 4 and not x.split("|")[-1].split("_")[1] in _no_index_joint_names]
                        _current_type = jnt_short_name.split("_")[3]
                        # brother_joints = cmds.listRelatives(parent_jnt, children=True, path=True)
                        # print(jnt_short_name)
                        # print(parent_jnt_short_name)
                        # print(cmds.listRelatives(parent_jnt, children=True, path=True))
                        
                        same_type_joints = [x for x in brother_joints if x.split("|")[-1].split("_")[2] == name_split[2] and x.split("|")[-1].split("_")[3] == _current_type and x != jnt]
                        r_joint_name = [x for x in same_type_joints if x.split("|")[-1].split("_")[4] == "R"]
                        # print(jnt_short_name," ---jnt_short_name")
                        # print(_current_type," ---_current_type")
                        # print([x.split("|")[-1] for x in brother_joints]," ---brother_joints")
                        # print([x.split("|")[-1] for x in r_joint_name]," ---r_joint_name")
                        # print([x.split("|")[-1] for x in same_type_joints]," ---same_type_joints")
                        # print("----\n")
                        if r_joint_name:
                            # print([x.split("|")[-1] for x in brother_joints])
                            if not brother_joints.index(jnt) < brother_joints.index(r_joint_name[0]):
                                errors.append(r_joint_name[0])
                        elif same_type_joints:
                            same_type_joint = same_type_joints[0]
                            if same_type_joint.split("|")[-1].split("_")[4] != "R":
                                errors.append(same_type_joint)

                            # r_parent_jnt = cmds.listRelatives(r_joint_name, parent=True, fullPath=True)
                            # if r_parent_jnt:
                            #     r_parent_jnt = r_parent_jnt[0]
                            #     if jnt in brother_joints and r_parent_jnt != parent_jnt:
                            #         errors.append(jnt)
    # for x in errors:
    #     print(x.split("|")[-1],"+++++++++")
    return errors
    # if not node:
    #     return []

    # errors = []

    # joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")
    # if not joints:
    #     return []
    

    # for jnt in joints:
    #     jnt_short_name = jnt.split("|")[-1]
    #     if _LEFT in jnt_short_name:
    #         sym_name = "{0}_R_{1}".format(*jnt_short_name.split(_LEFT))
    #         parent_l = cmds.listRelatives(jnt, parent=True)
            
    #         if not sym_name in [x.split("|")[-1] for x in joints]:
    #             errors.append(jnt)
    #         else:
    #             sym_joint = cmds.ls(sym_name, long=True)
    #             parent_r = cmds.listRelatives(sym_joint, parent=True)
    #             if parent_l[0].split(_LEFT) != parent_r[0].split(_RIGHT):
    #                 errors.append(jnt)
    
    # return errors