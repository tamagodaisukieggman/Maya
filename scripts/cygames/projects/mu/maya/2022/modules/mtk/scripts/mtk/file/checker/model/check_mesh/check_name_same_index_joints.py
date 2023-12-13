# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds

_root_joint = "jnt_0000_skl_root"
_with_index_joint_names = ["skl", "face", "helper"]
_no_index_joint_names = ["mtp", "cnp", "move"]

def _check_name_same_index_joints(node):
    if not node:
        return []

    joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")

    if not joints:
        return []
    # joints = cmds.ls(joints, dagObjects=True)
    # joint_dict = dict([x,[i,len(x.split("|")),x.split("|")[-1].split("_")[1],x.split("|")[-1]]] for i,x in enumerate(_joints) if x.split("|")[-1].split("_")[1].isdecimal())
    
    # joint_dict = dict()
    # for i, jnt in enumerate(joints):
    #     jnt_short_name = jnt.split("|")[-1]
    #     name_split = jnt_short_name.split("_")
    #     if name_split[1].isdecimal():
    #         joint_dict[jnt] = [i, len(jnt_short_name), name_split[1], jnt_short_name]
    
    errors = []

    _root_exists_flag = False

    _same_index_dict = dict()
    _indexes = []

    for jnt in joints:
        jnt_short_name = jnt.split("|")[-1]

        if jnt_short_name == _root_joint:
            _root_exists_flag = True
        else:
            name_split = jnt_short_name.split("_")
            if len(name_split) != 1:
                if name_split[0] == "jnt":

                    if name_split[1] in _no_index_joint_names:
                        continue
                    
                    _index = name_split[1]
                    # if not _index.isdecimal():
                    #     continue
                    # print(i, depth, jnt_short_name)
                    # _index = int(_index)

                    # if _indexes:
                    #     # print(_indexes)
                    #     print(jnt_short_name,i,_index)
                    #     print([(x,y,z) for (x,y,z) in _indexes if x[0] == _index[0] and x > _index and not i < y and depth == z])
                    #     _flag = [(x,y,z) for (x,y,z) in _indexes if x[0] == _index[0] and x > _index and not i < y and depth == z]
                    #     if _flag:
                    #         errors.append(jnt)
                    # _indexes.append([_index, i, depth])

                    # _index = int(_index)
                    if _index in _same_index_dict.keys():
                        _index_jnt = _same_index_dict[_index] + [jnt]
                        errors.extend(_index_jnt)
                    else:
                        _index_jnt = [jnt]
                    
                    _same_index_dict[_index] = _index_jnt
    
    return errors