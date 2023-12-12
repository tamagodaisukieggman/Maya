# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Non_Manifold_Vertices(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
#         _check = cmds.ls(cmds.polyInfo(mesh, nonManifoldVertices=True), fl=True, long=True)
#         if _check:
#             return _check
#         else:
#             return []

def _check_mesh_non_manifold_vertices(meshes):
    errors = []
    for mesh in meshes:
        _check = cmds.ls(cmds.polyInfo(mesh, nonManifoldVertices=True), fl=True, long=True)
        if _check:
            errors.extend(_check)
    return errors