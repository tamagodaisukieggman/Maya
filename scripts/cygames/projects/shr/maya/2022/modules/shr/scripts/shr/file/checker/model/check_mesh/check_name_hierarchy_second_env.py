# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
from maya import cmds

_model_group_name = "model"
_collision_group_name = "collision"
_need_group_names = [_model_group_name, _collision_group_name]
_lod_group_names = ["lod1", "lod2", "lod3"]
_collision_group_names = ["col_player","col_camera"]
_root_joint_group_name = "root_jnt"
_first_level = _need_group_names + _lod_group_names + [_root_joint_group_name]

def _check_name_hierarchy_second_env(node):
    if not node:
        return []
    
    errors = []
    
    _full_path = cmds.ls(node, long=True)[0]
    _root_node = _full_path.split("|")[1]

    _first_children = cmds.listRelatives(_root_node, children=True, fullPath=True)
    _second_childern = []
    
    _model_name_flag = False
    _collision_name_flag = False
    for _cld in _first_children:
        _childern = cmds.listRelatives(_cld, children=True, fullPath=True)
        if _childern:
            _second_childern.extend(_childern)
    
    if _second_childern:
        for _cld in _second_childern:
            _name_split = _cld.split("|")
            _parent = _name_split[-2]
            _name = _name_split[-1]
            if _parent == _collision_group_name:
                if cmds.nodeType(_cld) != "transform":
                    errors.append(_cld)
                    # errors.append(5)
                if not _name in _collision_group_names:
                    errors.append(_cld)
                    # errors.append(6)

    return errors