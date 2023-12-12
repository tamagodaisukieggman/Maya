# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Transform_Scale_Value(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
#         _transform_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
#         _scale_value = cmds.getAttr("{}.s".format(_transform_node))
#         if _scale_value != [(1.0, 1.0, 1.0)]:
#             return [_transform_node]
#         else:
#             return []

def _check_transform_scale_value(meshes):
    errors = []
    for mesh in meshes:
        _transform_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        _scale_value = cmds.getAttr("{}.s".format(_transform_node))
        if _scale_value != [(1.0, 1.0, 1.0)]:
            errors.append(_transform_node)
    return errors