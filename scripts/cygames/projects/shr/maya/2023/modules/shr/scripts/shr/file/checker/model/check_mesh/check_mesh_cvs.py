# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds
import maya.api.OpenMaya as om2


# from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_base
# reload(check_mesh_base)

# class Check_Mesh_Cvs(check_mesh_base.Check_Mesh):

#     def _check(self, mesh):
#         _vtxs = cmds.ls("{}.vtx[*]".format(mesh), fl=True, long=True)
#         error = []
#         for _vtx in _vtxs:
#             _pnt = cmds.getAttr("{}".format(_vtx))
#             if str(_pnt) != "[(0.0, 0.0, 0.0)]":
#                 error.append(_vtx)
#         if error:
#             return error
#         else:
#             return []

# import maya.api.OpenMaya as om
# ​
# def get_pnts_value(obj_name):
#     sel_list = om2.MSelectionList()
#     sel_list.add(obj_name)
#     dag_path = sel_list.getDagPath(0)
#     if not dag_path.hasFn(om2.MFn.kMesh):
#         return []
#     mesh_fn = om2.MFnMesh(dag_path)
#     plug = mesh_fn.findPlug('pnts', False)
#     return [plug.elementByPhysicalIndex(i).asMDataHandle().asFloat3() for i in range(plug.numElements())]

# _sel = cmds.ls(sl=True)
# print(get_pnts_value(_sel[0]))


def _check_mesh_cvs_api(meshes):
    errors = []

    for mesh in meshes:

        selList = om2.MSelectionList()
        selList.add(mesh)

        for x in range(selList.length()):
            dagPath = selList.getDagPath(x)
            mesh_fn = om2.MFnMesh(dagPath)
            plug = mesh_fn.findPlug('pnts', False)
            for i in range(plug.numElements()):
                errors.append(plug.elementByPhysicalIndex(i))

    return errors

def _check_mesh_cvs(meshes):
    errors = []
    for mesh in meshes:
        _vtxs = cmds.ls("{}.vtx[*]".format(mesh), fl=True, long=True)
        error = []
        for _vtx in _vtxs:
            _pnt = cmds.getAttr("{}".format(_vtx))
            if _pnt != [(0.0, 0.0, 0.0)]:
                errors.append(_vtx)
    return errors