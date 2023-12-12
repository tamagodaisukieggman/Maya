# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
from maya import cmds
from mtk.utils import getCurrentSceneFilePath

_model_group_name = "model"
_collision_group_name = "collision"
_need_group_names = [_model_group_name, _collision_group_name]
_lod_group_names = ["lod1", "lod2", "lod3"]
_collision_group_names = ["col_player","col_camera"]
_root_joint_group_name = "jnt_0000_skl_root"
_first_level = _need_group_names + _lod_group_names + [_root_joint_group_name]

def _check_name_hierarchy_root(node):
    if not node:
        return []
    scene_name = getCurrentSceneFilePath()
    
    if not scene_name:
        cmds.warning(u"階層のチェックはシーンを保存してから実行してください")
        return []
    
    errors = []
    base_name = os.path.basename(scene_name)
    
    _full_path = cmds.ls(node, long=True)[0]
    _root_node = _full_path.split("|")[1]

    if base_name.rsplit("_",1)[0] != _root_node.rsplit("_",1)[0]:
        errors.append(_root_node)
        # errors.append(0)
    
    if cmds.nodeType(_root_node) != "transform":
        errors.append(_root_node)
        # errors.append(1)
    
    if not _root_node.islower():
        errors.append(_root_node)
        # errors.append(2)

    return errors