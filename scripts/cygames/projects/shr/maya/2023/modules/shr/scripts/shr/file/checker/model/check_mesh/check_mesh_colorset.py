# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Colorset(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
#         color_sets = cmds.polyColorSet(mesh, q=True, allColorSets=True)
#         if color_sets:
#             return [mesh]
#         else:
#             return []

def _check_mesh_colorset(meshes):
    errors = []
    for mesh in meshes:
        color_sets = cmds.polyColorSet(mesh, q=True, allColorSets=True)
        if color_sets:
            errors.append(mesh)

    return errors