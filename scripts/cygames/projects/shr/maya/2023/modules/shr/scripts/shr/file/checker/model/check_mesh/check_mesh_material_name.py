# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Material_Name(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
        
#         _error_names = []
#         if mesh in self.materials.keys():
#             for material in self.materials[mesh]:
#                 if not material.startswith("mtl_"):
#                     _error_names.append(material)
#             if _error_names:
#                 return _error_names
#             else:
#                 return []
#         else:
#             return [mesh]

def _check_mesh_material_name(meshes):
    errors = []
        
    # _shading_engines = cmds.listConnections(mesh, type="shadingEngine", source=True)
    # materials = list(set(cmds.ls(cmds.listConnections(_shading_engines, source=True, destination=False), materials=True)))

    if not meshes:
        return []

    _shading_engines = []

    for mesh in meshes:
        shading_engine = cmds.listConnections(mesh, type='shadingEngine')
        if shading_engine:
            _shading_engines.extend(shading_engine)
        else:
            errors.append(mesh)
    
    if _shading_engines:

        materials = set()

        for _s in _shading_engines:
            _mat = cmds.listConnections(_s + '.surfaceShader')
            if _mat:
                materials.add(_mat[0])
    
        if materials:
            materials = list(materials)
            for material in materials:
                if not material.startswith("mtl_"):
                    errors.append(material)
    
    return errors