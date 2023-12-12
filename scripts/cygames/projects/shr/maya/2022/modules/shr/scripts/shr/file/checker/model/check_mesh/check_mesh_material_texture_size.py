# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds



# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Material_Texture_Size(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
#         _errors = []
#         _file_nodes = []
        
#         for _material in self.materials[mesh]:
#             _file_node = cmds.listConnections(_material, source=True, destination=False)
#             if _file_node:
#                 _file_nodes.append(_file_node[0])
#             else:
#                 _errors.append(_material)
        
#         if _file_nodes:
#             for _file_node in _file_nodes:
#                 _textrue_file_path = cmds.getAttr("{}.ftn".format(_file_node))
#                 _size_x = int(cmds.getAttr("{}.outSizeX".format(_file_node)))
#                 _size_y = int(cmds.getAttr("{}.outSizeY".format(_file_node)))
#                 if _size_x & (_size_x - 1) != 0 or _size_y & (_size_y - 1) != 0:
#                     _errors.append(_file_node)

#         return _errors

def _check_mesh_material_texture_size(meshes):
    errors = []
    _file_nodes = []

    if not meshes:
        return []
        
    _shading_engines = cmds.listConnections(meshes, type='shadingEngine')

    if not _shading_engines:
        return []
    
    materials = set()
    
    for _s in _shading_engines:
        _mat = cmds.listConnections(_s + '.surfaceShader')
        if _mat:
            materials.add(_mat[0])
    
    if materials:
        materials = list(materials)
        for material in materials:
            _file_node = cmds.listConnections(material, source=True, destination=False)

    if _file_nodes:
        for _file_node in _file_nodes:
            _textrue_file_path = cmds.getAttr("{}.ftn".format(_file_node))
            _size_x = int(cmds.getAttr("{}.outSizeX".format(_file_node)))
            _size_y = int(cmds.getAttr("{}.outSizeY".format(_file_node)))
            if _size_x & (_size_x - 1) != 0 or _size_y & (_size_y - 1) != 0:
                _errors.append(_file_node)
    
    return errors