# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds

exclusion_node_type = ["skinCluster", "tweak", "shadingEngine"]

def _check_mesh_skincluster_method(meshes):
    errors = []
    for mesh in meshes:
        _historys = [x for x in cmds.listHistory(mesh) if cmds.nodeType(x) == "skinCluster"]
        if _historys :
            for _history in _historys:
                _method = cmds.skinCluster(_history, q=True, skinMethod=True)
                if _method != 0:
                    errors.append(mesh)

    return errors