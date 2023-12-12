# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Uvset(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
#         uv_sets = cmds.polyUVSet(mesh, q=True, allUVSets=True)
#         if not uv_sets:
#             return [mesh]
#         # elif len(uv_sets) > 1:
#         #     return [mesh]
#         else:
#             return []

def _check_mesh_uvset(meshes):
    errors = []
    for mesh in meshes:
        uv_sets = cmds.polyUVSet(mesh, q=True, allUVSets=True)
        if not uv_sets:
            errors.append(mesh)
    return errors