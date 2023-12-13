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
_root_joint_group_name = "jnt_0000_skl_root"
_first_level = _need_group_names + _lod_group_names + [_root_joint_group_name]

def _check_name_hierarchy(node):
    if not node:
        return []

    errors = []
    names = {}
    
    for _cld in cmds.listRelatives(node, allDescendents=True, fullPath=True):
        if cmds.nodeType(_cld) == "transform":
            names[_cld] = _cld.split("|")[-1]
    
    for _long_name, _name in names.items():
        if names.values().count(_name) > 1:
            errors.append(_long_name)

    return errors