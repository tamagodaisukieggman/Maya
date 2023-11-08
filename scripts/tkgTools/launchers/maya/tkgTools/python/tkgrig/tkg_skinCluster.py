# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

import base64
import codecs
from collections import OrderedDict
import csv
import fnmatch
from functools import partial
import glob
import io
import json
import math
import re
import os
import pickle
import sys
from timeit import default_timer as timer
import time
import traceback

import maya.OpenMaya as OpenMaya
import maya.api.OpenMaya as OpenMaya2
import maya.api.OpenMayaAnim as OpenMayaAnim2
import maya.cmds as cmds
import maya.mel as mel

#_time = time.time
_time = time.clock

class TKGSkinWeights():
    def __init__(self):
        self.mesh = None
        self.meshShape = None
        self.skinClusterNode = None
        self.numInfluences = None
        self.influences = None
        # self.infIndexes = None
        self.vertIndices = None
        self.weightData = None
        self.seqInfNumList = None
        self.seqInfIdxList = None
        self.seqVertNumList = None
        self.seqVertIdxList = None

        self.set_rate = 1.0

        self.roundWeights = None
        self.roundDigit = 3

        self.forceMaxInfluence = None
        self.maxInfluence = 4

        self.soft_weights = None
        self.soft_weights_values = None

        self.colorWeights = None
        self.pointWeights = None

        self.closestPoints = None

        self.export_file = None
        self.import_file = None


    def get_skinWeights(self, sel=None):
        u''' Get SkinWeights Function
        :param list sel
        '''

        self.sel = sel

        if not self.sel:
            self.sel = cmds.ls(os=1, fl=1)
        else:
            cmds.select(self.sel, r=1)

        mel.eval('ConvertSelectionToVertices;')

        vtxs = cmds.ls(os=1, fl=1)
        vtxs = [vtx for vtx in vtxs if not cmds.objectType(vtx) in ['joint']]

        cmds.select(self.sel, r=1)

        self.mesh = vtxs[0].split('.')[0]
        self.meshShape = cmds.listRelatives(self.mesh, s=1)[0] or None

        self.skinClusterNode = mel.eval('findRelatedSkinCluster {};'.format(self.mesh))

        # スキンクラスタ取得
        skinNode = getDagPathDepNode( self.skinClusterNode )
        skinFn = OpenMayaAnim2.MFnSkinCluster( skinNode )

        # シェイプの取得
        shapePath = getDagPathDepNode( self.meshShape )
        meshNode = shapePath.node()

        # 取得対象の頂点
        #     今回はすべての頂点を取得したいので[0,1,2,,,,,MaxVertex]となっている。
        meshVerItFn = OpenMaya2.MItMeshVertex( meshNode )
        # vertIndices = range( meshVerItFn.count() )
        self.vertIndices = [int(re.sub('{}.vtx\[|\]'.format(self.mesh),"",vtx)) for vtx in vtxs]

        if self.soft_weights:
            self.soft_weights_values = get_soft_selection_weights()

            for swi in self.soft_weights_values.keys():
                if not swi in self.vertIndices:
                    self.vertIndices.append(swi)

        self.vertIndices = sorted(self.vertIndices)

        # 指定の頂点をコンポーネントとして取得する。
        singleIdComp = OpenMaya2.MFnSingleIndexedComponent()
        vertexComp = singleIdComp.create( OpenMaya2.MFn.kMeshVertComponent )
        singleIdComp.addElements( self.vertIndices )

        # setWeights()で指定するためのインフルエンスIntArrayを作成
        infDags = skinFn.influenceObjects()
        self.numInfluences = OpenMaya2.MIntArray( len( infDags ) , 0 )
        for x in range( len( infDags ) ):
            self.numInfluences[x] = int( skinFn.indexForInfluenceObject( infDags[x] ) )

        self.numInfluences = [ni for ni in self.numInfluences]

        self.influences = [inf.partialPathName() for inf in infDags]

        # すべてのウエイトの値を取得
        self.weightData = skinFn.getWeights( shapePath , vertexComp )
        self.weightData = [w for w in self.weightData[0]]


        return self.get_skinClusterData()


    def get_objects_weights(self, sel=None):
        u""" Get Objects Weight
        param: list: sel
        """
        s = _time()

        if '.' in sel[0]:
            objects_skinWeights_data = [self.get_skinWeights(sel)]

        else:
            objects_skinWeights_data = [self.get_skinWeights(obj) for obj in sel]

        get_time = _time() - s
        print("getWeights()", get_time, "s")

        return OrderedDict(zip(sel, objects_skinWeights_data))

    def get_skinClusterData(self):
        u""" Get SkinClusterData
        """
        skinClusterData = OrderedDict()

        skinClusterAttributes = [
            'skinningMethod',
            'useComponents',
            'deformUserNormals',
            'normalizeWeights',
            'weightDistribution',
            'maxInfluences',
            'maintainMaxInfluences',
        ]

        skinClusterData['mesh'] = self.mesh
        skinClusterData['meshShape'] = self.meshShape
        skinClusterData['skinClusterNode'] = self.skinClusterNode
        skinClusterData['numInfluences'] = self.numInfluences
        skinClusterData['influences'] = self.influences
        # skinClusterData['infIndexes'] = self.infIndexes
        skinClusterData['vertIndices'] = self.vertIndices
        skinClusterData['skinClusterAttributes'] = OrderedDict()
        for attr in skinClusterAttributes:
            skinClusterData['skinClusterAttributes'][attr] = cmds.getAttr('{}.{}'.format(self.skinClusterNode, attr))

        skinClusterData['weightData'] = self.weightData

        return skinClusterData


    def set_obj_weights(self, obj=None, skinWeightsData=None):
        u""" Set Object Weight from SkinClusterData
        param: self.import_file = bool: Set Object weight from data
        param: self.forceMaxInfluence = int: Force Set Object Maxinfluence
        param: self.roundWeights = bool: Set Round Weight
        """
        mesh = skinWeightsData['mesh']
        meshShape = skinWeightsData['meshShape']
        skinClusterNode = skinWeightsData['skinClusterNode']
        numInfluences = skinWeightsData['numInfluences']
        influences = skinWeightsData['influences']
        vertIndices = skinWeightsData['vertIndices']
        weightData = skinWeightsData['weightData']
        skinClusterAttributes = skinWeightsData['skinClusterAttributes']

        if self.import_file:
            skinClusters, skinedGeos = get_geometories_from_skinClusters(obj)
            mesh = obj

            if not skinClusters:
                print('BindSkin')
                skinClusterNode = cmds.skinCluster(
                    influences,
                    obj,
                    toSelectedBones=True,
                    bindMethod=skinClusterAttributes['skinningMethod'],
                    normalizeWeights=skinClusterAttributes['normalizeWeights'],
                    weightDistribution=skinClusterAttributes['weightDistribution'],
                    maximumInfluences=skinClusterAttributes['maxInfluences'],
                    obeyMaxInfluences=skinClusterAttributes['maintainMaxInfluences'],
                    dropoffRate=4,
                    removeUnusedInfluence=False,
                    name=skinClusterNode
                )[0]
            else:
                skinClusterNode = skinClusters[0]

        # SetAttr
        # for attr, val in skinClusterAttributes.items():
        #     cmds.setAttr('{}.{}'.format(skinClusterNode, attr), val)
        # weightData_values = [wd * self.set_rate for wd in weightData]

        weightList = list_mult_stab(weightData, numInfluences)

        sorted_closest_ids = {}
        if self.closestPoints:
            closest_vert_ids = get_closest_vert_ids(self.closestPoints[0], self.closestPoints[1])
            for tgt_id, base_id in closest_vert_ids.items():
                if not base_id in sorted_closest_ids.keys():
                    sorted_closest_ids[base_id] = []

                sorted_closest_ids[base_id].append(tgt_id)

            print('closest', sorted_closest_ids)

                # if base_id in vertIndices:
                #     closest_vert_idx = vertIndices.index(base_id)
                #     # vertIndices[closest_vert_idx] = tgt_id

        if self.forceMaxInfluence or self.roundWeights:
            weightList = self.create_new_weightList(self.compile_weightList(), numInfluences)

        if self.colorWeights:
            self.create_colorWeights(weightList, numInfluences, influences, vertIndices)

        if self.pointWeights:
            self.create_pointWeights(weightList, numInfluences, influences, vertIndices)

        if self.soft_weights:
            cmds.error('##############')
            return
            unlocked_infs = []
            for inf in influences:
                if self.sel[-1] == inf:
                    soft_weights_inf_idx = influences.index(inf)

                if not cmds.getAttr('{}.liw'.format(inf)):
                    unlocked_infs.append(influences.index(inf))

            for i, w in enumerate(weightList):
                if i in self.soft_weights_values.keys():
                    if soft_weights_inf_idx in unlocked_infs:

                        unlocked_infs_list = []
                        for ui in unlocked_infs:
                            unlocked_infs_list.append(weightList[i][ui])
                            # weightList[i][ui] = weightList[i][ui] * self.soft_weights_values[i]

                        set_value = sum(unlocked_infs_list) * self.soft_weights_values[i]
                        separate_value = (sum(unlocked_infs_list) - set_value) / (len(unlocked_infs) - 1)

                        for m, j in enumerate(unlocked_infs):
                            if not j == soft_weights_inf_idx:
                                unlocked_infs_list[m] = unlocked_infs_list[m] + separate_value
                            else:
                                unlocked_infs_list[m] = set_value

                        unlocked_infs_list = [float(k)/max(unlocked_infs_list) for k in unlocked_infs_list]

                        for m, j in enumerate(unlocked_infs):
                            weightList[i][j] = unlocked_infs_list[m]


        # inf_str_list, inf_int_list = combine_sequence(numInfluences)

        lock_infs = [inf for inf in influences if cmds.getAttr('{}.liw'.format(inf))]
        [cmds.setAttr('{}.liw'.format(inf), 0) for inf in lock_infs]

        cmds.skinCluster(skinClusterNode, e=True, nw=0)

        normalize_vertices = []
        for i, (v, w) in enumerate(zip(vertIndices, weightList)):
            # for j, (slice_str, slice_idx) in enumerate(zip(inf_str_list, inf_int_list)):
            #     spix = slice_idx.split(':')
            #     cmds.setAttr('{}.wl[{}].w[{}]'.format(skinClusterNode, v, slice_str),
            #                  *w[int(spix[0]):int(spix[1])+1],
            #                  size=len(w[int(spix[0]):int(spix[1])+1]))

            if sorted_closest_ids:
                if v in sorted_closest_ids.keys():
                    tgt_closest_verticies = sorted_closest_ids[v]
                    for close_v in tgt_closest_verticies:
                        cmds.skinPercent(skinClusterNode, '{}.vtx[{}]'.format(mesh, close_v), tv=zip(influences, w))

            else:
                cmds.skinPercent(skinClusterNode, '{}.vtx[{}]'.format(mesh, v), tv=zip(influences, w))
            # normalize_vertices.append('{}.vtx[{}]'.format(mesh, v))


        # api set weights
        # skinNode = getDagPathDepNode( skinClusterNode )
        # skinFn = OpenMayaAnim2.MFnSkinCluster( skinNode )

        # singleIdComp = OpenMaya2.MFnSingleIndexedComponent()
        # vertexComp = singleIdComp.create( OpenMaya2.MFn.kMeshVertComponent )
        # singleIdComp.addElements( vertIndices )

        # meshShape = cmds.listRelatives(mesh, s=1)[0] or None
        # shapePath = getDagPathDepNode( meshShape )

        # m_numInfluences = OpenMaya2.MIntArray( numInfluences )
        # m_weightData = OpenMaya2.MDoubleArray( weightData )

        # print(m_numInfluences , m_weightData)

        # skinFn.setWeights( shapePath , vertexComp , m_numInfluences , m_weightData )

        cmds.skinCluster(skinClusterNode, e=True, nw=1)

        # cmds.skinPercent(skinClusterNode, normalize_vertices, nrm=1)

        [cmds.setAttr('{}.liw'.format(inf), 1) for inf in lock_infs]

        self.print_options()


    def set_objects_weights(self, skinClusterDatas=None, fromSelected=None):
        s = _time()

        if fromSelected:
            self.import_file = True

        i = 0
        for obj, skinWeightsData in skinClusterDatas.items():
            if fromSelected:
                obj = fromSelected[i]
            self.set_obj_weights(obj, skinWeightsData)
            i += 1

        # [self.set_obj_weights(obj, skinWeightsData) for obj, skinWeightsData in skinClusterDatas.items()]

        set_time = _time() - s
        print("setWeights()", set_time, "s")


    def compile_weightList(self):
        weightList = list_mult_stab(self.weightData, self.numInfluences)

        saveWeights_dict = OrderedDict()
        for vert_index, weights in enumerate(weightList):
            savedWeightsNumIdx = []
            savedWeights = []
            zeroWeights = []
            for i, w in enumerate(weights):
                if w == 0.0:
                    zeroWeights.append(self.numInfluences[i])
                else:
                    savedWeightsNumIdx.append(self.numInfluences[i])
                    savedWeights.append(w)

            saved_strs, saved_ints = combine_sequence(savedWeightsNumIdx)
            zero_strs, zero_ints = combine_sequence(zeroWeights)

            saveWeights_dict[self.vertIndices[vert_index]] = [[saved_strs, savedWeights], zero_strs]

        return saveWeights_dict


    def create_new_weightList(self, file_weightData=None, numInfluences=None):
        #
        new_weightList = []
        for vert_i, weights in file_weightData.items():
            ex_val_strs = [a for a in separate_sequence(weights[0][0])]

            if self.forceMaxInfluence:
                if self.maxInfluence < len(weights[0][1]):
                    cut_idx = []
                    cut_list = cut_float_list_by_max(weights[0][1], self.maxInfluence, cut_idx)

                    [ex_val_strs.remove(ex_val_strs[i]) for i in cut_idx]

            if self.roundWeights:
                weights[0][1] = round_num_list_up_to(weights[0][1], self.roundDigit)

            set_weights_list = []
            ex_idx = 0
            for i in numInfluences:
                ex_values = weights[0][1]
                if i in ex_val_strs:
                    set_weights_list.append(ex_values[ex_idx])
                    ex_idx += 1
                else:
                    set_weights_list.append(0.0)

            new_weightList.append(set_weights_list)

        return new_weightList


    def create_colorWeights(self, weightList, numInfluences, influences, vertIndices):
        sel = cmds.ls(os=1)

        color_inf_id = []
        for inf in sel:
            if inf in influences:
                inf_idx = influences.index(inf)
                color_inf_id.append(numInfluences[inf_idx])

        unlocked_infs = [ulinf for ulinf in influences if not cmds.getAttr('{}.liw'.format(ulinf))]
        unlocked_infs_id = []
        for uinf in unlocked_infs:
            uinf_idx = influences.index(uinf)
            unlocked_infs_id.append(numInfluences[uinf_idx])

        unlocked_sum_list = []
        for vtx, w in enumerate(weightList):
            ul_temp_sum = 0
            for unl_idx in unlocked_infs_id:
                ul_temp_sum += w[unl_idx]

            unlocked_sum_list.append(ul_temp_sum)

        rgb_at_pnts_vts = []
        for vtx in self.rgb_at_pnts.keys():
            finded_num = re.findall(r"\d+", vtx)
            if 1 == len(finded_num):
                rgb_at_pnts_vts.append(int(finded_num[0]))

            elif 1 < len(finded_num):
                rgb_at_pnts_vts.append(int(finded_num[1]))

        rgb_at_pnts_vals = [val[0] for val in self.rgb_at_pnts.values()]

        for vtx, w in enumerate(weightList):
            if vertIndices[vtx] in rgb_at_pnts_vts:
                for i, set_idx in enumerate(w):
                    if i == color_inf_id[0]:
                        w[i] = unlocked_sum_list[vtx] * (1 - rgb_at_pnts_vals[vtx])
                    elif i == color_inf_id[1]:
                        w[i] = unlocked_sum_list[vtx] * rgb_at_pnts_vals[vtx]

    def create_pointWeights(self, weightList, numInfluences, influences, vertIndices):
        sel = cmds.ls(os=1)

        color_inf_id = []
        for inf in sel:
            if inf in influences:
                inf_idx = influences.index(inf)
                color_inf_id.append(numInfluences[inf_idx])

        unlocked_infs = [ulinf for ulinf in influences if not cmds.getAttr('{}.liw'.format(ulinf))]
        unlocked_infs_id = []
        for uinf in unlocked_infs:
            uinf_idx = influences.index(uinf)
            unlocked_infs_id.append(numInfluences[uinf_idx])

        unlocked_sum_list = []
        for vtx, w in enumerate(weightList):
            ul_temp_sum = 0
            for unl_idx in unlocked_infs_id:
                ul_temp_sum += w[unl_idx]

            unlocked_sum_list.append(ul_temp_sum)

        rgb_at_pnts_vts = []
        for vtx in self.rgb_at_pnts.keys():
            finded_num = re.findall(r"\d+", vtx)
            if 1 == len(finded_num):
                rgb_at_pnts_vts.append(int(finded_num[0]))

            elif 1 < len(finded_num):
                rgb_at_pnts_vts.append(int(finded_num[1]))


        distances = [self.get_distance(key_vtx, value_pos[0]) for key_vtx, value_pos in self.rgb_at_pnts.items()]

        # distances = []
        # for key_vtx, value_pos in self.rgb_at_pnts.items():
        #     print(value_pos[0], type(value_pos[0]))
        #     print(re.split('[(),\s]', value_pos[0]))
        #     float_pos = [sstl for sstl in re.split('[(),\s]', value_pos[0]) if not sstl == '']
        #     distances.append(self.get_distance(key_vtx, float_pos))

        max_dis = max(distances)
        distances = [dis / max_dis for dis in distances]

        rgb_at_pnts_vals = OrderedDict(zip(rgb_at_pnts_vts, distances))

        for vtx, w in enumerate(weightList):
            if vertIndices[vtx] in rgb_at_pnts_vts:
                for i, set_idx in enumerate(w):
                    if i == color_inf_id[0]:
                        w[i] = unlocked_sum_list[vtx] * (1 - rgb_at_pnts_vals[vertIndices[vtx]])
                    elif i == color_inf_id[1]:
                        w[i] = unlocked_sum_list[vtx] * rgb_at_pnts_vals[vertIndices[vtx]]


    def get_distance(self, objA, objB):
        if cmds.objExists(str(objA)):
            gObjA = cmds.xform(objA, q=True, t=True, ws=True)
        else:
            gObjA = objA

        if cmds.objExists(str(objB)):
            gObjB = cmds.xform(objB, q=True, t=True, ws=True)
        else:
            gObjB = objB

        return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))


    def get_rgb_at_points(self, mesh=None, rgb_texture=None):
        if rgb_texture:
            shapesInSel =  cmds.ls(mesh, dag=1,o=1,s=1)
            shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
            shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)
            texture = cmds.ls(cmds.listConnections(shaders),tex=1)

        sel = cmds.ls(os=1)

        self.rgb_at_pnts = OrderedDict()
        closest_shape = cmds.listRelatives(mesh, s=1)[0] or None
        if 'mesh' == cmds.objectType(closest_shape):
            cpt = cmds.createNode('closestPointOnMesh', ss=1)
            cmds.connectAttr(closest_shape+'.outMesh', cpt+'.inMesh', f=1)
            cmds.connectAttr(closest_shape+'.worldMatrix[0]', cpt+'.inputMatrix', f=1)

            mel.eval('ConvertSelectionToVertices;')

            vtxs = cmds.ls(os=1, fl=1)
            vtxs = [vtx for vtx in vtxs if not cmds.objectType(vtx) in ['joint']]

            for vtx in vtxs:
                cmds.setAttr(cpt+'.inPosition', *cmds.xform(vtx, q=1, t=1, ws=1))

                uval = cmds.getAttr(cpt+'.parameterU')
                vval = cmds.getAttr(cpt+'.parameterV')

                if rgb_texture:
                    rgb = cmds.colorAtPoint(texture[0], o='RGB', u=uval, v=vval)
                    self.rgb_at_pnts[vtx] = rgb

                else:
                    self.rgb_at_pnts[vtx] = cmds.getAttr(cpt+'.position')

        cmds.delete(cpt)
        cmds.select(sel, r=1)

    def print_options(self):
        if self.roundWeights:
            print('Round Weights')

        if self.forceMaxInfluence:
            print('Force Maxinfluence')

        if self.soft_weights:
            print('Soft Weights')

        if self.export_file:
            print('Export File')

        if self.import_file:
            print('Import File')


def list_mult_stab(numbers=None, baseNum=None):
    stackList = []
    stack = []
    for i, w in enumerate(numbers):
        back_idx = i % len(baseNum)
        stack.append(w)
        if back_idx == len(baseNum) - 1:
            stackList.append(stack)
            stack = []

    return stackList


def round_num_list_up_to(nums=None, digit=3, max_value=1.0):
    rounded_list = [round(i, digit) for i in nums]
    for i, rl in enumerate(rounded_list):
        if rl < 0.0 or 'e' in str(rl):
            rounded_list[i] = 0.0

    orig_total = sum(rounded_list)
    fixed_total = round(orig_total, digit)
    step = (10 ** -digit)

    # check digit
    zero_nums = [a for a in rounded_list if not a == 0.0]
    if not zero_nums:
        return rounded_list

    sum_sts = None

    if sum(nums) == max_value:
        sum_sts = True

    dig_sts = []
    for cn in nums:
        if len(list(str(step))) >= len(list(str(cn))) or cn == 0.0:
            dig_sts.append(True)

    if sum_sts == True and len(dig_sts) == len(nums):
        return nums

    # rounded_total > max_value
    if fixed_total > max_value:
        sorted_nums = sorted(rounded_list)
        sorted_nums = [sn for sn in sorted_nums if not sn == 0.0]

        n = int(round((fixed_total - max_value) / step, digit))

        for j in range(n):
            mult = j // len(rounded_list)

            if j < len(rounded_list):
                idx = j

            else:
                idx = j - len(rounded_list) * mult

            source_idx = rounded_list.index(sorted_nums[idx])

            rounded_list[source_idx] = round(sorted_nums[idx] - step, digit)
            sorted_nums[idx] = round(sorted_nums[idx] - step, digit)

    # rounded_total < max_value
    if fixed_total < max_value:
        sorted_nums = sorted(rounded_list, reverse=True)
        sorted_nums = [sn for sn in sorted_nums if not sn == 0.0]

        n = int(round((max_value - fixed_total) / step, digit))

        for j in range(n):
            mult = j // len(rounded_list)

            if j < len(rounded_list):
                idx = j

            else:
                idx = j - len(rounded_list) * mult

            source_idx = rounded_list.index(sorted_nums[idx])

            rounded_list[source_idx] = round(sorted_nums[idx] + step, digit)
            sorted_nums[idx] = round(sorted_nums[idx] + step, digit)


    return rounded_list


def getDagPathDepNode( name ):
    sellist = OpenMaya2.MGlobal.getSelectionListByName( name )
    try:
        return sellist.getDagPath(0)
    except:
        return sellist.getDependNode(0)


def get_soft_selection_weights():
    """
    cmds.softSelect(sse=1,ssc='0,1,3, 0.05,0.75,3, 0.18,0.5,3, 0.45,0.25,3, 0.7,0.1,3, 1,0,1',ssf=1)
    # ssc = "right << weight1, pos1, curveType1 weight2, pos2, curveType2 >> left"
    """
    sel = OpenMaya.MSelectionList()
    softSelection = OpenMaya.MRichSelection()
    OpenMaya.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(sel)

    dagPath = OpenMaya.MDagPath()
    component = OpenMaya.MObject()

    iter = OpenMaya.MItSelectionList(sel, OpenMaya.MFn.kMeshVertComponent)
    soft_weights = {}

    while not iter.isDone():

        iter.getDagPath( dagPath, component )
        dagPath.pop()
        node = dagPath.partialPathName()
        fnComp = OpenMaya.MFnSingleIndexedComponent(component)

        for i in range(fnComp.elementCount()):
            weight = 1.0
            if fnComp.hasWeights():
                weight = fnComp.weight(i).influence()

            soft_weights[fnComp.element(i)] = weight

        iter.next()

    return soft_weights


def combine_sequence(numInfluences):
    u"""
    param: list: [1,2,3,4] -> [[1:4], [0:3]]
    """
    accum_str = None
    accum_str_list = []
    accum_idx_list = []
    for i, numi in enumerate(numInfluences):
        if i == 0:
            accum_str = '{}'.format(numi)
            accum_idx = '{}'.format(i)

        elif numInfluences[i-1] + 1 == numi:
            accum_str = '{}:{}'.format(accum_str.split(':')[0], numi)
            accum_idx = '{}:{}'.format(accum_idx.split(':')[0], i)

        else:
            accum_str_list.append(accum_str)
            accum_idx_list.append(accum_idx)

            accum_str = '{}'.format(numi)
            accum_idx = '{}'.format(i)

        if i == len(numInfluences) - 1:
            accum_str_list.append(accum_str)
            accum_idx_list.append(accum_idx)

    return accum_str_list, accum_idx_list


def separate_sequence(sequence):
    for seq in sequence:
        if ':' in seq:
            spix = seq.split(':')
            for i in range(int(spix[0]), int(spix[1])+1):
                yield i
        else:
            yield int(seq)


def cut_float_list_by_max(float_list, max_val, del_index):
    if not len(float_list) == max_val:
        max_num = max(float_list)
        min_num = min(float_list)

        preci = len(list(str(max_num))) - 2

        del_index.append(float_list.index(min_num))

        float_list.remove(min_num)

        dif = round(1.0 - sum(float_list), preci)

        try:
            plus = dif / len(float_list)

        except ZeroDivisionError:
            plus = 0.0

        for j, n in enumerate(float_list):
            float_list[j] = n + plus

    else:
        return float_list

    return cut_float_list_by_max(float_list, max_val, del_index)

def get_geometories_from_skinClusters(node=None):
    skinClusters, skinedGeos, geos = None, None, None

    if node:
        try:
            shapes = cmds.listRelatives(node, pa=1, s=1, ni=1, type='controlPoint')
            history = cmds.listHistory(shapes, pdo=1)
            skinClusters = cmds.ls(history, typ='skinCluster') or None
        except RuntimeError:
            return skinClusters, skinedGeos

        return skinClusters, skinedGeos


    skinClusters = cmds.ls(type='skinCluster')
    if skinClusters:
        geoShapes = [cmds.skinCluster(scn, q=1, g=1) for scn in skinClusters]
        if geoShapes:
            geos = [cmds.listRelatives(gshape[0], p=1, pa=1) for gshape in geoShapes]

    if geos:
        skinedGeos = [geo[0] for geo in geos]

    return skinClusters, skinedGeos


def json_transfer(fileName=None, operation=None, export_values=None, export_type=None, import_type=None):
    if operation == 'export':
        if not export_type:
            with open(fileName, "w") as f:
                json.dump(export_values, f)

        if export_type == 'utf-8':
            with codecs.open(fileName, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

        elif export_type == 'pickle':
            s = base64.b64encode(pickle.dumps(export_values)).decode("utf-8")
            d = {"pickle": s}
            with open(fileName, "w") as f:
                json.dump(d, f)

    elif operation == 'import':
        if not import_type:
            with open(fileName) as f:
                return json.load(f)

        elif import_type == 'utf-8':
            with codecs.open(fileName, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)

        elif import_type == 'pickle':
            with open(fileName) as f:
                d = json.load(f)
            s = d["pickle"]
            return pickle.loads(base64.b64decode(s.encode()))

def fileDialog_export():
    filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=0)
    if filename is None:
        return False
    return filename[0]


def fileDialog_import():
    filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=1)
    if filename is None:
        return
    return filename[0]

def get_closest_vert_ids(base_mesh=None, target_mesh=None):
    u"""
    return: {target_mesh[vertexID]:base_mesh[closestID]}
    """
    sel = cmds.ls(os=1)

    base_selection_list = OpenMaya2.MSelectionList()
    base_selection_list.add(base_mesh)
    base_dag_path = base_selection_list.getDagPath(0)
    base_mesh_name = base_dag_path.fullPathName().split('|')[1]
    base_mfn_mesh = OpenMaya2.MFnMesh(base_dag_path)

    # closest
    cmds.select(target_mesh, r=1)
    mel.eval('ConvertSelectionToVertices;')
    tgt_vert_selection = OpenMaya2.MGlobal.getActiveSelectionList()

    tgt_iter = OpenMaya2.MItSelectionList(tgt_vert_selection, OpenMaya2.MFn.kMeshVertComponent)
    iter_dag, iter_cmp = tgt_iter.getComponent()
    tgt_fnComp = OpenMaya2.MFnSingleIndexedComponent(iter_cmp)
    tgt_verticies = tgt_fnComp.getElements()
    tgt_mesh_name = iter_dag.fullPathName().split('|')[1]

    closest_id_dict = OrderedDict()
    mesh_face_iterator = OpenMaya2.MItMeshPolygon(iter_dag)
    while not mesh_face_iterator.isDone():
        vert_id = mesh_face_iterator.getVertices()[0]
        target_MPoint = mesh_face_iterator.getPoints(OpenMaya2.MSpace.kWorld)[0]
        closest_point, closest_id = base_mfn_mesh.getClosestPoint(target_MPoint, OpenMaya2.MSpace.kWorld) # closest_idはbaseのid
        closest_id_dict[vert_id] = closest_id

        mesh_face_iterator.next()

    if sel:
        cmds.select(sel,r=1)

    return closest_id_dict

# sel = cmds.ls(os=1)
# closest_ids = get_closest_vert_ids(sel[0], sel[1])



# for key, val in closest_ids.items():
#     sets_name = 'set_{}_{}'.format(sel[0], val)
#     if not cmds.objExists(sets_name):
#         cmds.sets(em=1, n=sets_name)

#     cmds.sets('{}.vtx[{}]'.format(sel[0], val), add=sets_name)
#     cmds.sets('{}.vtx[{}]'.format(sel[1], key), add=sets_name)



"""
tkg_sw = TKGSkinWeights()
sel = cmds.ls(os=1)

# forceMaxInfluence
tkg_sw.forceMaxInfluence = True
tkg_sw.maxInfluence = 4
getWeightsValues = tkg_sw.get_objects_weights(sel)
tkg_sw.set_objects_weights(getWeightsValues)


# round
tkg_sw.roundWeights = True
tkg_sw.roundDigit = 3
getWeightsValues = tkg_sw.get_objects_weights(sel)
tkg_sw.set_objects_weights(getWeightsValues)


# softweights
tkg_sw.soft_weights = True
getWeightsValues = tkg_sw.get_objects_weights(sel)
tkg_sw.set_objects_weights(getWeightsValues)


# export
tkg_sw.export_file = True
getWeightsValues = tkg_sw.get_objects_weights(sel)

fileName=fileDialog_export()
json_transfer(fileName, 'export', export_values=getWeightsValues)


# import
tkg_sw.import_file = True
fileName=fileDialog_import()
getWeightsValues = json_transfer(fileName, 'import', export_type='pickle', )

tkg_sw.set_objects_weights(getWeightsValues)

# color
tkg_sw.colorWeights = True
getWeightsValues = tkg_sw.get_objects_weights(sel)
tkg_sw.get_rgb_at_points('pPlane3', True)
tkg_sw.get_rgb_at_points('blurA', True)
tkg_sw.get_rgb_at_points('blurB', True)

tkg_sw.set_rate = 0.7
tkg_sw.set_objects_weights(getWeightsValues)

# points
tkg_sw.pointWeights = True
getWeightsValues = tkg_sw.get_objects_weights(sel)
tkg_sw.get_rgb_at_points('pSphere1', None)
tkg_sw.set_objects_weights(getWeightsValues)
tkg_sw.rgb_at_pnts

# pickle
# b = pickle.dumps(sel)
s = base64.b64encode(pickle.dumps(test)).decode("utf-8")
d = {"pickle": s}
with open(fileName, "w") as f:
    json.dump(d, f)

# d = {}
# with open(fileName) as f:
#     d = json.load(f)
# s = d["pickle"]
# o = pickle.loads(base64.b64decode(s.encode()))

# closestpoints
tkg_sw = TKGSkinWeights()

sel = cmds.ls(os=1)
tkg_sw.closestPoints = sel
getWeightsValues = tkg_sw.get_objects_weights([sel[0]])
tkg_sw.set_objects_weights(skinClusterDatas=getWeightsValues, fromSelected=[sel[1]])


"""
