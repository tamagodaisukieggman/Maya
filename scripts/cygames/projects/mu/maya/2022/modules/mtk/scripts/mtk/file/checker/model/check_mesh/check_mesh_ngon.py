# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division



import maya.api.OpenMaya as om2


# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Ngon(check_mesh_base.Check_Mesh):
  
#     def _check(self, mesh):
#         selList = om2.MSelectionList()
#         selList.add(mesh)

#         errors = []
#         for x in range(selList.length()):
#             dagPath = selList.getDagPath(x)
#             mesh_fn = om2.MFnMesh(dagPath)
#             for num in range(mesh_fn.numPolygons):
#                 if mesh_fn.polygonVertexCount(num)  > 4:
#                     errors.append("{}.f[{}]".format(mesh, num))
#         if errors:
#             return errors
#         else:
#             return []

def _check_mesh_ngon(meshes):
    errors = []

    for mesh in meshes:

        selList = om2.MSelectionList()
        selList.add(mesh)

        for x in range(selList.length()):
            dagPath = selList.getDagPath(x)
            mesh_fn = om2.MFnMesh(dagPath)

            try:
                for num in range(mesh_fn.numPolygons):
                    if mesh_fn.polygonVertexCount(num)  > 4:
                        errors.append("{}.f[{}]".format(mesh, num))
            except:pass
    return errors
