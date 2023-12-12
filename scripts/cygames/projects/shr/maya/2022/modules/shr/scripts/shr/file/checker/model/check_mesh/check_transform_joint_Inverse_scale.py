# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



def _check_transform_joint_Inverse_scale(node):
    if not node:
        return []

    errors = []

    joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")
    if not joints:
        return []
    
    for joint in joints:
        joint_short_name = joint.split("|")[-1]
        parent = cmds.listRelatives(joint, parent=True, fullPath=True, type="joint")
        
        if parent:
            parent = parent[0]
            parent_short_name = parent.split("|")[-1]
            inverseScale = cmds.listConnections(parent, plugs=True, source=True, type="joint")
            if not inverseScale:
                errors.append(joint)
            else:
                inverseScale = [x for x in inverseScale if x.endswith("inverseScale") and x.startswith(joint_short_name)]
                if not inverseScale:
                    errors.append(joint)
    
    return errors