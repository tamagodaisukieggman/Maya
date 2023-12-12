# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



def _check_transform_joint_bindpose(node):
    errors = []

    root_jnt_name = "root_jnt"
    joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")
    
    if not joints:
        return []
    
    root_jnts = [x for x in joints if x.split("|")[-1] == root_jnt_name]
    
    for root_jnt in root_jnts:
        error_flag = False

        _pose = cmds.listConnections(x, t='dagPose')
        if _pose:
            if len(set(_pose)) > 1:
                errors.append(root_jnt)
        
    return errors