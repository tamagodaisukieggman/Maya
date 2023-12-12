# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
from maya import cmds

_model_group_name = "model"
_root_joint_name = "jnt_0000_skl_root"
_collision_group_name = "collision"
_need_group_names = [_model_group_name, _collision_group_name]
_lod_group_names = ["lod1", "lod2", "lod3", "lod4", "lod5"]
_collision_group_names = ["col_player","col_camera"]
_root_joint_group_name = "jnt_0000_skl_root"
_first_level = _need_group_names + _lod_group_names + [_root_joint_group_name]

def _check_name_hierarchy_first(node):
    if not node:
        return []
    
    errors = []
    
    _full_path = cmds.ls(node, long=True)[0]
    _root_node = _full_path.split("|")[1]
    
    _first_children = cmds.listRelatives(_root_node, children=True, fullPath=True)
    # _second_childern = []
    
    _model_name_flag = False
    _collision_name_flag = False
    for _cld in _first_children:
        _name = _cld.split("|")[-1]
        if not _name in _first_level:
            errors.append(_cld)
            # errors.append(2)
        # if cmds.nodeType(_cld) != "transform":
        #     errors.append(_cld)
        #     errors.append(3)
        if _name == _model_group_name:
            _model_name_flag = True
        if _name == _collision_group_name:
            _collision_name_flag = True
        if cmds.nodeType(_cld) == "joint":
            if _name != _root_joint_name:
                errors.append(_cld)
                # errors.append(5)
        elif cmds.nodeType(_cld) != "transform":
            errors.append(_cld)
            # errors.append(3)
            
        # _childern = cmds.listRelatives(_cld, children=True, fullPath=True)
        # if _childern:
        #     _second_childern.extend(_childern)
    
    if not _model_name_flag:
        errors.append(_cld)
        # errors.append(4)

    return errors