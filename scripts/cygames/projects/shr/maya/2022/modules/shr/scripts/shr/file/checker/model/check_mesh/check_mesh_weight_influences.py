# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim


exclusion_node_type = ["skinCluster", "tweak", "shadingEngine"]


def _check_mesh_weight_influences(meshes):
    errors = []
    for mesh in meshes:
        _historys = cmds.listHistory(mesh)
        if _historys :
            for _history in _historys:
                if cmds.nodeType(_history) == "skinCluster":
                    _max_influences = cmds.getAttr("{}.maxInfluences".format(_history))
                    _vtxs = cmds.ls("{}.vtx[*]".format(mesh), long=True, fl=True)
                    for _vtx in _vtxs:
                        _weight_values = [x for x in cmds.skinPercent(_history, _vtx, query=True, value=True ) if round(x, 6) > 0.0]
                        if len(_weight_values) > 4:
                            errors.append(_vtx)


    return errors






def _check_mesh_weight_influences_api2(meshes):
    _sel = cmds.ls(sl=True, long=True, type="transform")
    sel_list = om2.MSelectionList()
    [sel_list.add(x) for x in _sel]
    _dags = []
    mesh_fns = []
    _deps = []
    for i in range(sel_list.length()):
        dag_path = sel_list.getDagPath(i)
        dep = sel_list.getDependNode(i)
        _dags.append(dag_path)
        _deps.append(dep)
        mesh_fns.append(om2.MFnMesh(dag_path))


    for mesh_fn,_dag,_dep in zip(mesh_fns,_dags,_deps):
        _historys = [x for x in cmds.listHistory(_dag) if cmds.nodeType(x) == "skinCluster"]
        if _historys:

            _history = _historys[0]
            skinNode  = om2.MGlobal.getSelectionListByName(_history).getDependNode(0)
            skinFn = om2anim.MFnSkinCluster(skinNode)
            
            meshVerItFn = om2.MItMeshVertex(_dag)
            indices = range(meshVerItFn.count())
            vertexComp = om2.MFnSingleIndexedComponent().create(om2.MFn.kMeshVertComponent)

            vertWeights = skinFn.getWeights(_dag, vertexComp)
            
            weights = list(vertWeights[-2])
            
            infCount = vertWeights[-1]
            infDags = skinFn.influenceObjects()
            #infDags = [x.fullPathName() for x in infDags]
            print(weights,infCount)
            print([[x,int(x+infCount)] for x in range(0,len(weights),infCount)])
            weights = [weights[x:x+infCount] for x in range(0,len(weights),infCount)]
            weightsDict = dict([infDags[x:x+infCount],weights[x:x+infCount]] for x in range(0,len(weights),infCount))
            print(weights)
            dicty = {}
            
            #for i, weight in enumerate(weights):
            #    if i in indices:
            #        dicty.update({i:weight})
            #
            #print dicty.items()

def get_dagPath_and_comps(objects):
    """MDagPath と MObject(component) (API 1.0)を取得
    :param list objects: オブジェクトのリスト
    :return: MDagPath, MObject(component) (API 1.0) を取得
    :rtype: tuple (MDagPath, MObject(component))
    """

    sel_list = OpenMaya.MSelectionList()
    [sel_list.add(x) for x in objects]
    dag_path = OpenMaya.MDagPath()
    comps = OpenMaya.MObject()
    sel_list.getDagPath(0, dag_path, comps)
    return dag_path, comps


def get_MObject(object_name):
    """MObject (API 1.0)を取得
    :param str object_name: オブジェクト名
    :return: MObject (API 1.0) を取得
    :rtype: MObject (API 1.0)
    """

    sel_list = OpenMaya.MSelectionList()
    sel_list.add(object_name)
    m_obj = OpenMaya.MObject()
    sel_list.getDependNode(0, m_obj)

    return m_obj

def _check_mesh_weight_influences_api(meshes):
    for mesh in meshes:
        _historys = cmds.listHistory(mesh, pruneDagObjects=True, interestLevel=2)
        if _historys :
            for _h in _historys:
                if cmds.nodeType(_h) == "skinCluster":
                    dag_path, comps = get_dagPath_and_comps(['{}.cp[*]'.format(mesh)])

                    sc_obj = get_MObject(_h)
                    sc_fn = OpenMayaAnim.MFnSkinCluster(sc_obj)
                
                    weights = OpenMaya.MDoubleArray()
                    infl_indices = OpenMaya.MIntArray()
                    infls = OpenMaya.MDagPathArray()
                    util = OpenMaya.MScriptUtil()
                    int_ptr = util.asUintPtr()
                
                    sc_fn.influenceObjects(infls)
                    for i in range(infls.length()):
                        infl_indices.append(sc_fn.indexForInfluenceObject(infls[i]))
                
                    sc_fn.getWeights(dag_path, comps, weights, int_ptr)
                    py_weights = [v for v in weights]
                    py_infls = []
                    for i in range(infls.length()):
                        py_infls.append(infls[i].partialPathName())
                    py_infl_indices = [v for v in infl_indices]
            
                    # print py_weights, py_infls, py_infl_indices


                    # _vtxs = cmds.ls("{}.vtx[*]".format(mesh),fl=1)
                    # print _vtxs
                    # for _vtx in _vtxs:
                    #     print [round(x, 6) for x in cmds.skinPercent(_h, _vtx, query=True, value=True ) if round(x, 6) > 0.0]


