# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
from maya import cmds
from mtk.utils import getCurrentSceneFilePath

_tex_prefix = "tex_"

def _check_mesh_material_texture_name(meshes):
    # _mutsunokami_path = "Z:/mtk/work/resources"

    if not meshes:
        return []

    _mutsunokami_path = "Z:/mtk/work"
    _current_work_space = cmds.workspace(fullName=True)

    scene_name = getCurrentSceneFilePath()

    if not scene_name:
        cmds.warning(u"テクスチャ名のチェックはシーンを保存してから実行してください")
        return []

    base_name = os.path.basename(scene_name)
    name_base = os.path.splitext(base_name)[0]
    _name_check = name_base.split("_", 1)[-1]

    errors = set()
    _file_nodes = []

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
            _file_node = cmds.ls(cmds.listConnections(material, source=True, destination=False), type="file")
            if _file_node:
                _file_nodes.extend(_file_node)

    if _file_nodes:
        for _file_node in _file_nodes:
            _textrue_file_path = cmds.getAttr("{}.ftn".format(_file_node))
            if not _textrue_file_path:
                errors.add(_file_node)
                # errors.add(1)
                # break

            if not os.path.exists(_textrue_file_path):
                errors.add(_file_node)
                # errors.add(2)
                # break

            if len(_textrue_file_path.split(_mutsunokami_path)) != 2:
                errors.add(_file_node)
                # errors.add(3)
                # break

            _basename = os.path.basename(_textrue_file_path)

            if not _basename.startswith(_tex_prefix):
                errors.add(_file_node)
                # errors.add(4)
                # break

            _name = os.path.splitext(_basename)[0].split(_tex_prefix)[-1]
            if not _name.startswith(_name_check):
                errors.add(_file_node)
                # errors.add(5)

    return list(errors)
