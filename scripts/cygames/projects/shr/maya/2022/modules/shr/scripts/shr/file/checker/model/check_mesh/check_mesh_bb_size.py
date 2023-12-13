# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_BB_Size(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):

#         bb_size = cmds.polyEvaluate(mesh, boundingBox=True, accurateEvaluation=True)
#         if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
#             return [mesh]
#         else:
#             return []

def _check_mesh_bb_size(meshes):
    errors = []
    for mesh in meshes:
        bb_size = cmds.polyEvaluate(mesh, boundingBox=True, accurateEvaluation=True)
        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            _transform_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
            errors.append(_transform_node)
    return errors