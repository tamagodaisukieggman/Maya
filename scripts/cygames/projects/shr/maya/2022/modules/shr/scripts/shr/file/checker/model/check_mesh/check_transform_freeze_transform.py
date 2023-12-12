# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Transform_Freeze_Transform(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):

#         _transform_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
#         _transform_value = cmds.getAttr("{}.t".format(_transform_node))
#         _rotate_value = cmds.getAttr("{}.r".format(_transform_node))
#         if _transform_value != [(0.0, 0.0, 0.0)] or _rotate_value != [(0.0, 0.0, 0.0)]:
#             return [_transform_node]
#         else:
#             return []

def _check_transform_freeze_transform(meshes):
    errors = []
    for mesh in meshes:
        _transform_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        _transform_value = cmds.getAttr("{}.t".format(_transform_node))
        _rotate_value = cmds.getAttr("{}.r".format(_transform_node))
        if _transform_value != [(0.0, 0.0, 0.0)] or _rotate_value != [(0.0, 0.0, 0.0)]:
            errors.append(_transform_node)
    return errors
