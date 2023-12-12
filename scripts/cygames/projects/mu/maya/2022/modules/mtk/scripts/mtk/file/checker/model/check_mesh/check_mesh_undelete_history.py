# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Undelete_History(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
#         exclusion_node_type = ["skinCluster", "tweak", "shadingEngine"]
#         _flag = False
#         _historys = cmds.listHistory(mesh, pruneDagObjects=True, interestLevel=2)
#         if _historys:
#             for _history in _historys:
#                 if not _history in exclusion_node_type:
#                     _flag = True
#                     break
            
#             if _flag:
#                 return [mesh]
#             else:
#                 return []
#         else:
#             return []

def _check_mesh_undelete_history(meshes):
    exclusion_node_type = ["skinCluster", "tweak", "shadingEngine"]
    
    errors = []
    for mesh in meshes:
        _historys = cmds.listHistory(mesh, pruneDagObjects=True, interestLevel=2)
        if _historys:
            _flag = False
            for _history in _historys:
                if not cmds.nodeType(_history) in exclusion_node_type:
                    _flag = True
                    break
            if _flag:
                _transform_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
                errors.append(_transform_node)

    return errors