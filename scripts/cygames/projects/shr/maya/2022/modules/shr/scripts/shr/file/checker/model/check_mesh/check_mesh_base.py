# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from maya import cmds


class Check_Mesh(object):
    
    def __init__(self, *args):

        self.selections = []
        self.meshes = []
        self.materials = {}
        self.get_selections()
        
    def do(self):
        errors = []
        for mesh in self.meshes:
            error = self._check(mesh)
            if error:
                errors.extend(error)
        return errors

    def _check(self):
        pass

    def _get_selection_mesh_materials(self, mesh):
        _flag = True
        
        # _shading_engines = cmds.listConnections(mesh, type="shadingEngine")
        _shading_engines = cmds.listConnections(mesh, type="shadingEngine", source=True)
        if not _shading_engines:
            _flag = False
        
        materials = list(set(cmds.ls(cmds.listConnections(_shading_engines, source=True, destination=False), materials=True)))
        # materials = list(set(cmds.listConnections(_shading_engine + ".surfaceShader")[0] for _shading_engine in _shading_engines))
        
        if not materials:
            _flag = False
        
        if _flag:
            self.materials[mesh] = materials
        else:
            self.materials[mesh] = []

    def get_selections(self, *args):

        selections = cmds.ls(sl=True, type="transform", long=True)
        # if not selections:
        #     cmds.confirmDialog(message=u"トランスフォームノードを選択してください",
        #                     title=u'選択の確認',
        #                     button=['OK'],
        #                     defaultButton='OK',
        #                     cancelButton="OK",
        #                     dismissString="OK")
        #     return
            
        self.selections = selections
        
        for selection in selections:
            meshes = [x for x in cmds.listRelatives(selection, allDescendents=True, fullPath=True, type="mesh") if not cmds.getAttr("{}.intermediateObject".format(x))]
            # 中間オブジェクトは抜かす
            if meshes:
                self.meshes.extend(meshes)
                for mesh in meshes:
                    self._get_selection_mesh_materials(mesh)


