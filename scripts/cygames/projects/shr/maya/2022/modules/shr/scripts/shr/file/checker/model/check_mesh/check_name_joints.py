# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds

_root_joint = "jnt_0000_skl_root"
_with_index_joint_names = ["skl", "face", "helper"]
_no_index_joint_names = ["mtp", "cnp", "move"]

def _check_name_joints(node):
    if not node:
        return []

    joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")

    if not joints:
        return []
    # joints = cmds.ls(joints, dagObjects=True)

    errors = []

    _root_exists_flag = False
    _indexes = []
    _indes_dict = {}

    for jnt in joints:
        jnt_short_name = jnt.split("|")[-1]

        if jnt_short_name == _root_joint:
            _root_exists_flag = True
        else:
            name_split = jnt_short_name.split("_")
            if len(name_split) == 1:
                print(jnt_short_name," --- name_split length")
                errors.append(jnt)
            else:
                if name_split[0] != "jnt":
                    print(jnt_short_name," --- jnt prefix")
                    errors.append(jnt)
                else:
                    if name_split[1] in _no_index_joint_names:
                        continue

                    # if name_split[1] in _indexes:
                    #     print(jnt_short_name," --- exists index")
                    #     errors.append(jnt)

                    # _indexes.append(name_split[1])

                    parent_jnt = cmds.listRelatives(jnt, parent=True, fullPath=True)[0]
                    parent_jnt_short_name = parent_jnt.split("|")[-1]
                    current_index = name_split[1]
                    current_index_int = int(current_index)

                    if current_index.isdecimal():
                        if len(current_index) != 4:
                            print(jnt_short_name," --- joint index length")
                            errors.append(jnt)
                        else:
                            
                            if name_split[2] in _with_index_joint_names:
                                if name_split[2] == _with_index_joint_names[0]:
                                    if not 0 < current_index_int < 3000:
                                        print(jnt_short_name, " --- < 3000")
                                        errors.append(jnt)
                                elif name_split[2] == _with_index_joint_names[1]:
                                    if not 3000 <= current_index_int < 4000:
                                        print(jnt_short_name, " --- < 4000")
                                        errors.append(jnt)
                                elif name_split[2] == _with_index_joint_names[2]:
                                    if not 4000 <= current_index_int < 5000:
                                        print(jnt_short_name," --- < 5000")
                                        errors.append(jnt)
                            else:
                                print(jnt_short_name," --- not with index")
                                errors.append(jnt)

                            # brother_joints = [x for x in cmds.listRelatives(parent_jnt, children=True, fullPath=True) if len(x.split("|")[-1].split("_")) > 4 and not x.split("|")[-1].split("_")[1] in _no_index_joint_names]

                            brother_joints = cmds.listRelatives(parent_jnt, children=True, fullPath=True)
                            for i,brother_joint in enumerate(brother_joints):
                                brother_joint_short_name = brother_joint.split("|")[-1]
                                brother_index = brother_joint_short_name.split("_")
                                if len(brother_index) > 4 and not brother_index in _no_index_joint_names:
                                    brother_index = brother_index[1]
                                    brother_index_int = int(brother_index)
                                    if current_index[0] == brother_index[0]:
                                        if brother_index_int > current_index_int and brother_joints.index(jnt) > i:
                                            print(jnt_short_name," --- brother index value")
                                            errors.append(jnt)

                            if parent_jnt_short_name.split("_")[1].isdecimal():
                                if not int(parent_jnt_short_name.split("_")[1]) < current_index_int:
                                    child_jnt = [x for x in cmds.listRelatives(jnt, children=True, path=True)]
                                    if child_jnt:
                                        child_jnt = child_jnt[0].split("|")[-1]
                                        if not int(child_jnt.split("_")[1]) > current_index_int:
                                            print(child_jnt," --- not child index > current index")
                                            errors.append(child_jnt)
                                        elif not int(parent_jnt_short_name.split("_")[1]) < int(child_jnt.split("_")[1]):
                                            print(parent_jnt_short_name," --- not parent index < child index")
                                            errors.append(parent_jnt)
                                        else:
                                            print(jnt_short_name," --- ")
                                            errors.append(jnt)
                                    else:
                                        errors.append(jnt)

                    else:
                        errors.append(jnt)
    return errors