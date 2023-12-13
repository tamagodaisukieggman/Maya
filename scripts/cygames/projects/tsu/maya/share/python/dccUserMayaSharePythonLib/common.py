# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : dccUserMayaSharePythonLib.common
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm
import os
import sys
#import time
#import json
#import stat
#from functools import partial
from collections import OrderedDict
from PySide2 import QtGui
from dccUserMayaSharePythonLib import file_dumspl as f
from dccUserMayaSharePythonLib import pyCommon as pcm

if sys.hexversion < 0x3000000:
    BYTES = str
    UNICODE = unicode
    BASESTR = basestring
    LONG = long
else:
    BYTES = bytes
    UNICODE = str
    BASESTR = str
    LONG = int


def setPyNodes(nodes):
    return [pm.PyNode(x) for x in nodes]


def getLocalVals(node):
    tx, ty, tz = cmds.getAttr(node + '.translate')[0]
    rx, ry, rz = cmds.getAttr(node + '.rotate')[0]
    sx, sy, sz = cmds.getAttr(node + '.scale')[0]
    return tx, ty, tz, rx, ry, rz, sx, sy, sz


def getWorldVals(node):
    node = pm.PyNode(node)
    tx, ty, tz = node.getTranslation(space='world')
    rx, ry, rz = node.getRotation(space='world')
    sx, sy, sz = node.getScale()
    return tx, ty, tz, rx, ry, rz, sx, sy, sz


def basename(name):
    name = name.rsplit(':', 1)[-1]
    name = name.rsplit('|', 1)[-1]
    return name


def trsList(dot=False, trans=True, rotate=True, scale=True, short=True):
    """TRSのアトリビュートタプルを返す"""

    if short:
        t = ['tx', 'ty', 'tz']
        r = ['rx', 'ry', 'rz']
        s = ['sx', 'sy', 'sz']
    else:
        t = ['translateX', 'translateY', 'translateZ']
        r = ['rotateX', 'rotateY', 'rotateZ']
        s = ['scaleX', 'scaleY', 'scaleZ']

    result = []
    if trans:
        result += t
    if rotate:
        result += r
    if scale:
        result += s

    if dot:
        tmpResult = result
        for i in range(len(tmpResult)):
            result[i] = '.' + result[i]

    return tuple(result)


def sameNameNodeSelect(parent_, child_, except_word=None):
    """parent_, child_　の階層以下の同じ名前のノードを相互に選択する"""

    if except_word is None:
        except_word = []
    p_names = [x for x in cmds.ls(parent_, dag=True, type=('transform', 'joint'))]
    c_names = [x for x in cmds.ls(child_, dag=True, type=('transform', 'joint'))]

    result_names = []
    for p_name in p_names:
        for c_name in c_names:
            if basename(p_name) == basename(c_name):
                if except_word:
                    if pcm.startswith_in_stringlist(p_name, except_word):
                        continue
                result_names.append([p_name, c_name])
                print(p_name, c_name)
                break

    if result_names:
        cmds.select(cl=True)
        for names in result_names:
            print(names)
            cmds.select(names, add=True)
        cmds.select(parent_, child_, d=True)

    '''
    #sels = cmds.ls(sl=True)
    #for i, sel in enumerate(sels):
    #	if i % 2 == 0:
    #		print(sels[i], sels[i + 1])
    '''
    return result_names


def selMeshHierarchy(node):
    dags = pm.ls(node, dag=True, transforms=True)
    meshs = [x for x in dags if x.getShape()]
    pm.select(meshs)


def resetTransform(node):
    node = pm.PyNode(node)
    node.setTranslation([0, 0, 0])
    node.setRotation([0, 0, 0])
    node.setScale([1, 1, 1])


def copy(src, tgt):
    p_tx, p_ty, p_tz, p_rx, p_ry, p_rz, p_sx, p_sy, p_sz = getLocalVals(src)
    cmds.setAttr(tgt + '.translate', *(p_tx, p_ty, p_tz))
    cmds.setAttr(tgt + '.rotate', *(p_rx, p_ry, p_rz))
    cmds.setAttr(tgt + '.scale', *(p_sx, p_sy, p_sz))


def match(src, tgt):
    sels = pm.selected()
    if pm.nodeType(tgt) == 'joint':
        pm.setAttr(tgt + '.jointOrientX', 0)
        pm.setAttr(tgt + '.jointOrientY', 0)
        pm.setAttr(tgt + '.jointOrientZ', 0)
    pm.select(tgt, src)
    loo = LockOnOff(tgt)
    loo.all_off()
    mm.eval('MatchTransform;')
    loo.restoration()
    pm.select(sels)


def mirrorTrans(src, tgt):
    src = pm.PyNode(src)
    tgt = pm.PyNode(tgt)
    src_trans = src.getTranslation(space='world')
    tgt.setTranslation([src_trans[0] * -1, src_trans[1], src_trans[2]], space='world')


def swap(node1, node2):
    p_tx, p_ty, p_tz, p_rx, p_ry, p_rz, p_sx, p_sy, p_sz = getLocalVals(node1)
    c_tx, c_ty, c_tz, c_rx, c_ry, c_rz, c_sx, c_sy, c_sz = getLocalVals(node2)

    cmds.setAttr(node1 + '.translate', *(c_tx, c_ty, c_tz))
    cmds.setAttr(node1 + '.rotate', *(c_rx, c_ry, c_rz))
    cmds.setAttr(node1 + '.scale', *(c_sx, c_sy, c_sz))
    cmds.setAttr(node2 + '.translate', *(p_tx, p_ty, p_tz))
    cmds.setAttr(node2 + '.rotate', *(p_rx, p_ry, p_rz))
    cmds.setAttr(node2 + '.scale', *(p_sx, p_sy, p_sz))


def compareVal(node1, node2):
    """node1とnode2のTRS値を比較、異なっていたらTrueを返す"""

    is_different = False
    if cmds.getAttr(node1 + '.t') != cmds.getAttr(node2 + '.t'):
        is_different = True
        return is_different
    if cmds.getAttr(node1 + '.r') != cmds.getAttr(node2 + '.r'):
        is_different = True
        return is_different
    if cmds.getAttr(node1 + '.s') != cmds.getAttr(node2 + '.s'):
        is_different = True
        return is_different
    return is_different


def compareHierarchyParentChildren(node1, node2, ignore_namespace=True, ignore_shape=True):
    """２つのノードの親子が同じ名前、数（子供）かどうかを比較し、親子が異なるノードの組み合わせを取得"""

    node1 = pm.PyNode(node1)
    node2 = pm.PyNode(node2)

    if ignore_shape:
        children_node1 = [x for x in node1.getChildren(type=('transform', 'joint'))]
        children_node2 = [x for x in node2.getChildren(type=('transform', 'joint'))]

    if ignore_namespace:
        parent_node1 = node1.getParent()
        if parent_node1 is not None:
            parent_node1 = basename(parent_node1)
        children_node1 = [basename(x) for x in children_node1]

        parent_node2 = node2.getParent()
        if parent_node2 is not None:
            parent_node2 = basename(parent_node2)
        children_node2 = [basename(x) for x in children_node2]
    else:
        parent_node1 = node1.getParent()
        parent_node2 = node2.getParent()

    different_nodes = ''
    if parent_node1 != parent_node2:
        different_nodes = [node1, node2]
    if children_node1 != children_node2:
        different_nodes = [node1, node2]
    return different_nodes


def getDifferentNodesIn2Hierarchy(node1, node2):
    """node1, node2、それぞれの階層内のノードを名前ベースで比較し、どちらかにしか無いノードを取得"""

    nodes_1 = [x for x in pm.ls(node1, dag=True, type=('transform', 'joint'))]
    nodes_2 = [x for x in pm.ls(node2, dag=True, type=('transform', 'joint'))]
    nodes_basename_1 = [basename(x) for x in nodes_1]
    nodes_basename_2 = [basename(x) for x in nodes_2]
    nodes_ns_dict_1 = {basename(x): x.namespace() for x in nodes_1}
    nodes_ns_dict_2 = {basename(x): x.namespace() for x in nodes_2}
    different_nodes = set(nodes_basename_1) ^ set(nodes_basename_2)

    result = []
    if different_nodes:
        result = []
        for node in list(different_nodes):
            if node in nodes_ns_dict_1:
                result.append(nodes_ns_dict_1[node] + node)
            elif node in nodes_ns_dict_2:
                result.append(nodes_ns_dict_2[node] + node)
    return result


def limit(node, set_limit=True):
    """
    現在の値で動かなくなるようにリミットをかける
    node: 対象ノード
    set_limit: Falseでリミットオフ
    return: None
    """

    tx, ty, tz, rx, ry, rz, sx, sy, sz = getLocalVals(node)

    if set_limit:
        cmds.setAttr(node + '.minTransXLimit', tx)
        cmds.setAttr(node + '.maxTransXLimit', tx)
        cmds.setAttr(node + '.minTransYLimit', ty)
        cmds.setAttr(node + '.maxTransYLimit', ty)
        cmds.setAttr(node + '.minTransZLimit', tz)
        cmds.setAttr(node + '.maxTransZLimit', tz)
    cmds.setAttr(node + '.minTransXLimitEnable', set_limit)
    cmds.setAttr(node + '.maxTransXLimitEnable', set_limit)
    cmds.setAttr(node + '.minTransYLimitEnable', set_limit)
    cmds.setAttr(node + '.maxTransYLimitEnable', set_limit)
    cmds.setAttr(node + '.minTransZLimitEnable', set_limit)
    cmds.setAttr(node + '.maxTransZLimitEnable', set_limit)

    if set_limit:
        cmds.setAttr(node + '.minRotXLimit', rx)
        cmds.setAttr(node + '.maxRotXLimit', rx)
        cmds.setAttr(node + '.minRotYLimit', ry)
        cmds.setAttr(node + '.maxRotYLimit', ry)
        cmds.setAttr(node + '.minRotZLimit', rz)
        cmds.setAttr(node + '.maxRotZLimit', rz)
    cmds.setAttr(node + '.minRotXLimitEnable', set_limit)
    cmds.setAttr(node + '.maxRotXLimitEnable', set_limit)
    cmds.setAttr(node + '.minRotYLimitEnable', set_limit)
    cmds.setAttr(node + '.maxRotYLimitEnable', set_limit)
    cmds.setAttr(node + '.minRotZLimitEnable', set_limit)
    cmds.setAttr(node + '.maxRotZLimitEnable', set_limit)

    if set_limit:
        cmds.setAttr(node + '.minScaleXLimit', sx)
        cmds.setAttr(node + '.maxScaleXLimit', sx)
        cmds.setAttr(node + '.minScaleYLimit', sy)
        cmds.setAttr(node + '.maxScaleYLimit', sy)
        cmds.setAttr(node + '.minScaleZLimit', sz)
        cmds.setAttr(node + '.maxScaleZLimit', sz)
    cmds.setAttr(node + '.minScaleXLimitEnable', set_limit)
    cmds.setAttr(node + '.maxScaleXLimitEnable', set_limit)
    cmds.setAttr(node + '.minScaleYLimitEnable', set_limit)
    cmds.setAttr(node + '.maxScaleYLimitEnable', set_limit)
    cmds.setAttr(node + '.minScaleZLimitEnable', set_limit)
    cmds.setAttr(node + '.maxScaleZLimitEnable', set_limit)


def getWorldTrans(node):
    t = pm.PyNode(node).getTranslation('world')
    return [t[0], t[1], t[2]]


def getDistance(node1, node2):
    node1 = pm.PyNode(node1).name()
    node2 = pm.PyNode(node2).name()
    # object_pos_1 = cmds.getAttr(node1 + ".translate")
    # object_pos_2 = cmds.getAttr(node2 + ".translate")
    object_pos_1 = cmds.xform(node1, q=True, ws=True, t=True)
    object_pos_2 = cmds.xform(node2, q=True, ws=True, t=True)

    mm.eval("vector $object_pos_1 = << %s , %s , %s >>; " % (object_pos_1[0], object_pos_1[1], object_pos_1[2]))
    mm.eval("vector $object_pos_2 = << %s , %s , %s >>; " % (object_pos_2[0], object_pos_2[1], object_pos_2[2]))
    mm.eval("vector $object_Vector = $object_pos_1 - $object_pos_2;")
    distance_value = mm.eval("mag $object_Vector;")
    return distance_value


def getDistanceFromValue(vac_val1, vec_val2):
    mm.eval("vector $object_pos_1 = << %s , %s , %s >>; " % (vac_val1[0], vac_val1[1], vac_val1[2]))
    mm.eval("vector $object_pos_2 = << %s , %s , %s >>; " % (vec_val2[0], vec_val2[1], vec_val2[2]))
    mm.eval("vector $object_Vector = $object_pos_1 - $object_pos_2;")
    distance_value = mm.eval("mag $object_Vector;")
    return distance_value


def getBoundingboxEdgeLengthSum(node):
    bb = cmds.xform(node, q=True, boundingBox=True, ws=True)
    return (bb[3] - bb[0]) + (bb[4] - bb[1]) + (bb[5] - bb[2])


def getBoundingboxVolume(node):
    bb = cmds.xform(node, q=True, boundingBox=True, ws=True)
    return (bb[3] - bb[0]) * (bb[4] - bb[1]) * (bb[5] - bb[2])


def getParent(node):
    p = cmds.listRelatives(node, p=True)
    if p is not None:
        return p[0]


def getRoot(node):
    p = cmds.listRelatives(node, p=True)
    if p is None:
        return node[0]
    else:
        return getRoot(p)


def getShape(node):
    return cmds.listRelatives(node, s=True)


class LockOnOff(object):
    """"nodesのロックを全て解放　restorationで元に戻す
    self.is_unlock = Falseで逆 """

    def __init__(self, nodes):
        self.nodes = pcm.make_list(nodes)
        self.onoff_list = []
        self.is_unlock = True
        self.connected_lock = False

    def all_off(self):
        for trs in trsList(dot=True):
            for node in self.nodes:
                at = node + trs
                locked = pm.getAttr(at, lock=True)

                if self.connected_lock:
                    if not locked:
                        s = pm.listConnections(at, s=True, d=False)
                        if s:
                            if 'animCurve' not in pm.nodeType(s[0]):
                                pm.setAttr(at, lock=True)
                                self.onoff_list.append(at)

                elif self.is_unlock:
                    if locked:
                        pm.setAttr(at, lock=False)
                        self.onoff_list.append(at)

                else:
                    if not locked:
                        pm.setAttr(at, lock=True)
                        self.onoff_list.append(at)

    def restoration(self):
        if self.connected_lock:
            self.is_unlock = False

        for l in self.onoff_list:
            pm.setAttr(l, lock=self.is_unlock)


# --------------------------------------------------------------------------
# Animation
# --------------------------------------------------------------------------
def getKeyTime(s_or_e, sels=None):
    """全カーブから最初のキーと最後のキーの平均値を取得"""

    if sels is None:
        sels = cmds.ls(sl=True)
    key_time_list = []
    for sel in sels:
        curves = cmds.keyframe(sel, name=True, q=True)
        if curves is None:
            continue

        for curve in curves:
            oCuvType = cmds.nodeType(curve)
            oCuvType = oCuvType.replace('animCurve', '')

            if oCuvType != 'UL' and oCuvType != 'UA' and oCuvType != 'UU':
                if s_or_e == 'start':
                    if len(cmds.keyframe(curve, q=True)) != 1:
                        key_time_list.append(cmds.keyframe(curve, q=True)[0])
                elif s_or_e == 'end':
                    if len(cmds.keyframe(curve, q=True)) != 1:
                        num = len(cmds.keyframe(curve, q=True)) - 1
                        key_time_list.append(cmds.keyframe(curve, q=True)[num])

    keyTimeListSet = sorted(set(key_time_list))

    keyTimeLenList = [0 for i in range(len(keyTimeListSet))]
    for i in range(len(keyTimeListSet)):
        for keyTimeL in key_time_list:
            if keyTimeL == keyTimeListSet[i]:
                keyTimeLenList[i] += 1

    if keyTimeListSet:
        oMax = keyTimeLenList[0]
        oKeyTime = keyTimeListSet[0]
        if len(keyTimeListSet) == 1:
            oKeyTime = keyTimeListSet[0]
        else:
            for i in range(len(keyTimeLenList)):
                if i != 0:
                    if oMax < keyTimeLenList[i]:
                        oMax = keyTimeLenList[i]
                        oKeyTime = keyTimeListSet[i]
    else:
        oKeyTime = 0

    return oKeyTime


def setAllKeyRange():
    """選択ノードのアニメーションの範囲にタイムレンジを合わせる"""
    sels = pm.selected()
    sf = getKeyTime('start')
    ef = getKeyTime('end')
    # print(sf, ef)
    pm.Env().setMinTime(sf)
    pm.Env().setMaxTime(ef)
    pm.select(sels)


def getAnimCurves():
    curves = []
    for node in pm.ls():
        if 'animCurve' in pm.nodeType(node):
            curves.append(node)
    return curves


def deleteKeysOtherSpecifiedFrame(nodes, frame):
    """frame（time）以外にあるキーを削除"""

    key_times = [x for x in cmds.keyframe(nodes, q=True, tc=True)]
    for k_time in list(set(key_times)):
        if k_time != frame:
            cmds.cutKey(t=(k_time, k_time), option='keys')


def getAnimCurveDiffMinMaxValue(anim_curve):
    """アニメーションカーブの最大値と最小値の差を取得"""

    keys = cmds.keyframe(anim_curve, q=True, vc=True)
    return max(keys) - min(keys)


def getNodeAnimationDiffMinMaxValue(node):
    """nodeのtrsのアニメーション値の差を辞書型で取得"""

    at_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    cuvs = cmds.keyframe(node, q=True, name=True, at=at_list)
    result_dict = {}
    for i in range(len(cuvs)):
        result_dict[at_list[i]] = getAnimCurveDiffMinMaxValue(cuvs[i])
    return result_dict


# --------------------------------------------------------------------------
# Joint
# --------------------------------------------------------------------------
def aimToChild(tgt, child, upv='', vec=[(1, 0, 0), (0, 0, 1)]):
    tgt = pm.PyNode(tgt)
    child = pm.PyNode(child)
    isParent = child.getParent()
    if isParent:
        pm.parent(child, w=True)

    if upv:
        aimC = pm.aimConstraint(child, tgt, aim=vec[0], u=vec[1], wut='object', wuo=upv)
    else:
        aimC = pm.aimConstraint(child, tgt, aim=vec[0], u=vec[1], wut='none')
    pm.delete(aimC)

    if isParent:
        pm.parent(child, tgt)

    import tsubasa.maya.rig.mergerotation as mergerotation
    mergerotation.merge_rotation([child], 'rotate', 1)


def getOppositeJoint(joint_):
    joint_ = pm.PyNode(joint_)
    target_joint = joint_
    if pm.nodeType(joint_) == 'joint':
        side = pm.getAttr(joint_ + '.side')
        if side == 1 or side == 2:
            op_side = 2 if side == 1 else 1
            j_type = pm.getAttr(joint_ + '.type')
            joints = pm.ls(getRoot(joint_.name()), dag=True, type='joint')
            for j in joints:
                if pm.getAttr(j + '.type') == j_type:
                    if pm.getAttr(j + '.side') == op_side:
                        target_joint = j
                        break
    return target_joint


# --------------------------------------------------------------------------
# Attribute
# --------------------------------------------------------------------------
def addAt(node, atName, value, overwrite=True, p_=None, keyable=False, enum=False):
    """
    アトリビュートの追加（型を自動判別）.
    overwrite : 値を上書き.
    p_ : compoundアトリビュートを指定
        ※追加のみで値はセットしない：coumpoundは指定数全ての子を追加してからでないとエラーが出る
    enum: enumの場合はフラグを立てる
    return　: 最終的なatNameの値を返す
    """

    atName = atName[1:] if atName.startswith('.') else atName
    nodeAttr = node + '.' + atName

    ##bool----
    if type(value) == bool:
        if not pm.objExists(nodeAttr):
            if p_ is None:
                pm.addAttr(node, ln=atName, nn=atName, at='bool')
                pm.setAttr(nodeAttr, value)
            else:
                pm.addAttr(node, p=p_, ln=atName, nn=atName, at='bool')
        elif overwrite:
            pm.setAttr(nodeAttr, value)

    ##int----
    elif isinstance(value, LONG):
        if not pm.objExists(nodeAttr):
            if p_ is None:
                pm.addAttr(node, ln=atName, nn=atName, at='long')
                pm.setAttr(nodeAttr, value)
            else:
                pm.addAttr(node, p=p_, ln=atName, nn=atName, at='long')
        elif overwrite:
            pm.setAttr(nodeAttr, value)

    ##float----
    elif isinstance(value, float):
        if not pm.objExists(nodeAttr):
            if p_ is None:
                pm.addAttr(node, ln=atName, nn=atName)
                pm.setAttr(nodeAttr, value)
            else:
                pm.addAttr(node, p=p_, ln=atName, nn=atName)
        elif overwrite:
            pm.setAttr(nodeAttr, value)

    ##list(Array)----
    elif isinstance(value, list):
        if value:
            if str(value[0]) == 'True' or str(value[0]) == 'False' or isinstance(value[0], LONG):
                if not pm.objExists(nodeAttr):
                    if p_ is None:
                        pm.addAttr(node, ln=atName, nn=atName, dt='Int32Array')
                        pm.setAttr(nodeAttr, value, type='Int32Array')
                    else:
                        pm.addAttr(node, p=p_, ln=atName, nn=atName, dt='Int32Array')
                elif overwrite:
                    pm.setAttr(nodeAttr, value, type='Int32Array')

            elif isinstance(value[0], BASESTR):
                if not pm.objExists(nodeAttr):
                    if p_ is None:
                        pm.addAttr(node, ln=atName, nn=atName, dt='stringArray')
                        pm.setAttr(nodeAttr, len(value), *value, type='stringArray')
                    else:
                        pm.addAttr(node, p=p_, ln=atName, nn=atName, dt='stringArray')
                elif overwrite:
                    pm.setAttr(nodeAttr, len(value), *value, type='stringArray')

            elif isinstance(value[0], float):
                if not pm.objExists(nodeAttr):
                    if p_ is None:
                        pm.addAttr(node, ln=atName, nn=atName, dt='floatArray')
                        pm.setAttr(nodeAttr, value, type='floatArray')
                    else:
                        pm.addAttr(node, p=p_, ln=atName, nn=atName, dt='floatArray')
                elif overwrite:
                    pm.setAttr(nodeAttr, value, type='floatArray')

    # enum----
    elif enum:
        if not pm.objExists(nodeAttr):
            if p_ is None:
                pm.addAttr(node, ln=atName, nn=atName, at='enum', en=value)
                # pm.setAttr(nodeAttr, value)
            else:
                pm.addAttr(node, p=p_, ln=atName, nn=atName, at='enum', en=value)
        elif overwrite:
            pm.deleteAttr(nodeAttr)
            pm.evalDeferred(pm.Callback(addAt, node, atName, value, overwrite, p_, keyable))

    # string----
    elif isinstance(value, BASESTR):
        if not pm.objExists(nodeAttr):
            if p_ is None:
                pm.addAttr(node, ln=atName, nn=atName, dt='string')
                pm.setAttr(nodeAttr, value, type='string')
            else:
                pm.addAttr(node, p=p_, ln=atName, nn=atName, dt='string')
        elif overwrite:
            pm.setAttr(nodeAttr, value, type='string')

    if p_ is None and value:
        try:
            pm.setAttr(nodeAttr, k=keyable)
            return pm.getAttr(nodeAttr, value)
        except:
            pass


def lockAt(node, at, islock=True):
    at_list = at if isinstance(at, list) else [at]
    for a in at_list:
        cmds.setAttr('{}.{}'.format(node, a), lock=islock)


# --------------------------------------------------------------------------
# Constraint
# --------------------------------------------------------------------------
def getConstraintTarget(nodes):
    """
    nodesがコンストレイントを持っている場合、コンストレイント先を取得する
    :param nodes: constrainted_nodes
    :return: {constrainted_node: [constraint_node, [constraint_target_nodes]]}
    """

    result_dict = {}
    for node in nodes:
        constraints = cmds.listConnections(node, type='constraint')
        if not constraints:
            print('Node:', node)
            print('No Constraints Found')
            result_dict[node] = None
            continue

        constraints = list(set(constraints))
        constrained_nodes = {}
        for constraint in constraints:
            # print(constraint)
            # constraint_type = cmds.nodeType(constraint)
            target_nodes = cmds.listConnections(
                constraint + '.target', destination=False, source=True, scn=True)
            if target_nodes is None:
                constrained_nodes[constraint] = None
            else:
                target_nodes = [x for x in target_nodes if 'Constraint' not in cmds.nodeType(x)]
                target_nodes = list(set(target_nodes))
                constrained_nodes[constraint] = target_nodes

        # print(constrained_nodes)

        if constrained_nodes:
            print('Node:', node)
            #result_list = []
            result_dict2 = {}
            for constrained_node, constraints in constrained_nodes.items():
                print('Constrained Node:', constrained_node)
                print('Constraints:', constraints)
                #result_list.append([constrained_node, constraints])
                result_dict2[constrained_node] = constraints
            result_dict[node] = result_dict2
        else:
            print('Node:', node)
            print('No Constraints Found')
            result_dict[node] = None
    return result_dict

# --------------------------------------------------------------------------
# CopyPaste
# --------------------------------------------------------------------------
def set_json(setting_json_file_name):
    setting_dir = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"), 'Documents', 'maya', 'Scripting_Files')
    setting_json = os.path.join(setting_dir, setting_json_file_name)
    if not os.path.isfile(setting_json):
        f.exportJson(setting_json)
    return setting_json

# setting_json = set_json('copyPasteTransform.json')


def getTransform(node):
    node = pm.PyNode(node)
    transforms = (
        (pm.getAttr(node + '.tx'), pm.getAttr(node + '.ty'), pm.getAttr(node + '.tz')),
        (pm.getAttr(node + '.rx'), pm.getAttr(node + '.ry'), pm.getAttr(node + '.rz')),
        (pm.getAttr(node + '.sx'), pm.getAttr(node + '.sy'), pm.getAttr(node + '.sz')),
        pm.xform(node, q=True, ws=True, t=True),
        pm.xform(node, q=True, ws=True, ro=True),
        pm.getAttr(node + '.rotateOrder')
    )
    return transforms


def whiteJsonTransforms(nodes, json_):
    dict_ = OrderedDict()
    for node in nodes:
        node = pm.PyNode(node)
        dict_[node.name()] = getTransform(node)
    f.exportJson(json_, dict_)
    return dict_


def setTransform(node, value_list, space='object', ignore_at=[]):
    node = pm.PyNode(node)

    # ignore_atがある場合は初期値を記憶する
    current_val_dict = {}
    if ignore_at:
        list_ = getTransform(node)
        current_val_dict['tx'] = list_[0][0]
        current_val_dict['ty'] = list_[0][1]
        current_val_dict['tz'] = list_[0][2]
        current_val_dict['rx'] = list_[1][0]
        current_val_dict['ry'] = list_[1][1]
        current_val_dict['rz'] = list_[1][2]
        current_val_dict['sx'] = list_[2][0]
        current_val_dict['sy'] = list_[2][1]
        current_val_dict['sz'] = list_[2][2]

    # セット値を成形
    if space == 'object':
        t = value_list[0]
        r = value_list[1]
    else:
        t = value_list[3]
        r = value_list[4]

    # セットする
    node.setTranslation(t, space=space)
    node.setRotation(r, space=space)
    node.setScale(value_list[2])

    # ignore_atがある場合は元に戻す
    if ignore_at:
        for at in ignore_at:
            pm.setAttr(node + '.' + at, current_val_dict[at])


def readJsonTransform(nodes, json_, match_method=0, space='object', ignore_at=[]):
    """
    nodesにjsonデータを読み込みトランスフォームを一致させる
    match_method; 組み合わせ方法　0=順番 1=名前
    ignore_at； trsの中で、除外するアトリビュートのリスト
    space; ローカルグローバル　'object'=ローカル 'world'=グローバル
    """
    dict_ = f.importJson(json_)

    match_list = []

    # 順番
    if match_method == 0:
        i = 0
        for key_node_name, value_list in dict_.items():
            if i < len(nodes):
                try:
                    setTransform(nodes[i], value_list, space=space, ignore_at=ignore_at)
                    match_list.append([key_node_name, nodes[i], ''])
                except:
                    match_list.append([key_node_name, nodes[i], 'error'])
                i += 1

    # 名前
    elif match_method == 1:
        for node in nodes:
            for key_node_name, value_list in dict_.items():
                if basename(node) == basename(key_node_name):
                    try:
                        setTransform(node, value_list, space=space, ignore_at=ignore_at)
                        match_list.append([key_node_name, node, ''])
                        break
                    except:
                        match_list.append([key_node_name, node, 'error'])

    return match_list


def readJsonName(nodes, json_):
    """
    nodesにjsonデータを読み込に名前を一致させる
    match_method; 組み合わせ方法　0=順番 1=名前
    ignore_at； trsの中で、除外するアトリビュートのリスト
    space; ローカルグローバル　'object'=ローカル 'world'=グローバル
    """
    nodes = setPyNodes(nodes)
    dict_ = f.importJson(json_)

    after_process_list = []
    i = 0
    for key_node_name, val in dict_.items():
        if i < len(nodes):
            key_node_name_base = basename(key_node_name)
            node_base = basename(nodes[i])
            new_name = nodes[i].replace(node_base, key_node_name_base)

            pm.rename(nodes[i], new_name)
            if basename(nodes[i]) != new_name:
                after_process_list.append([nodes[i], new_name])
            i += 1

    if after_process_list:
        for after_process in after_process_list:
            pm.rename(after_process[0], after_process[1])


# --------------------------------------------------------------------------
# HIK
# --------------------------------------------------------------------------
def changeHIKSource(character_name, source_name):
    pm.mel.eval('hikSetCurrentCharacter("{0}")'.format(character_name))
    for i, item in enumerate(cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)):
        if cmds.menuItem(item, q=True, l=True).lstrip() == source_name:
            cmds.optionMenu("hikSourceList|OptionMenu", e=True, select=i + 1)
            pm.mel.eval('hikUpdateCurrentSourceFromUI()')
            pm.mel.eval('hikUpdateContextualUI()')
            pm.mel.eval('hikControlRigSelectionChangedCallback')
            break


# --------------------------------------------------------------------------
# Etc
# --------------------------------------------------------------------------
def hum(message=''):
    """ヘッドアップメッセージを表示"""

    if message:
        cmds.headsUpMessage(' ' * 300 + message + ' ' * 300, t=3)
    else:
        cmds.headsUpMessage('', t=3)


def toClip(text):
    cpb = QtGui.QClipboard()
    cpb.setText(text)


def matchName(parent_, child_):
    p_base_name = basename(parent_)
    c_base_name = basename(child_)
    set_name = child_.replace(c_base_name, p_base_name)
    cmds.rename(child_, set_name)


def matchJointLabel(parent_, child_):
    s_val = pm.getAttr(parent_ + '.side')
    pm.setAttr(child_ + '.side', s_val)
    jt_val = pm.getAttr(parent_ + '.type')
    pm.setAttr(child_ + '.type', jt_val)
    ot_val = pm.getAttr(parent_ + '.otherType')
    pm.setAttr(child_ + '.otherType', ot_val)


def getShape(nodes):
    result = []
    for node in nodes:
        shapes = cmds.listRelatives(node, shapes=True)
        if shapes:
            for shape in shapes:
                result.append(shape)
    return result


def createWld(node):
    nodename = pm.PyNode(node).name()
    wld = pm.group(em=True, n=nodename + '_wld')
    dcomp = pm.shadingNode('decomposeMatrix', n=nodename + '_dmat', asUtility=True)

    pm.connectAttr(node + '.worldMatrix', dcomp + '.inputMatrix')
    pm.connectAttr(dcomp + '.outputRotate', wld + '.rotate')
    pm.connectAttr(dcomp + '.outputScale', wld + '.scale')
    pm.connectAttr(dcomp + '.outputShear', wld + '.shear')
    pm.connectAttr(dcomp + '.outputTranslate', wld + '.translate')

    return wld


def duplicate(node, set_child=False):
    dupnode = pm.duplicate(node, parentOnly=True, inputConnections=False)
    if set_child:
        pm.parent(dupnode, node)


def connectTrss(src, tgt):
    cmds.connectAttr(
        '{}.outputTranslate.outputTranslateX'.format(src),
        '{}.translate.translateX'.format(tgt), f=True)
    cmds.connectAttr(
        '{}.outputTranslate.outputTranslateY'.format(src),
        '{}.translate.translateY'.format(tgt), f=True)
    cmds.connectAttr(
        '{}.outputTranslate.outputTranslateZ'.format(src),
        '{}.translate.translateZ'.format(tgt), f=True)

    cmds.connectAttr('{}.outputRotate.outputRotateX'.format(src), '{}.rotate.rotateX'.format(tgt), f=True)
    cmds.connectAttr('{}.outputRotate.outputRotateY'.format(src), '{}.rotate.rotateY'.format(tgt), f=True)
    cmds.connectAttr('{}.outputRotate.outputRotateZ'.format(src), '{}.rotate.rotateZ'.format(tgt), f=True)

    cmds.connectAttr('{}.outputScale.outputScaleX'.format(src), '{}.scale.scaleX'.format(tgt), f=True)
    cmds.connectAttr('{}.outputScale.outputScaleY'.format(src), '{}.scale.scaleY'.format(tgt), f=True)
    cmds.connectAttr('{}.outputScale.outputScaleZ'.format(src), '{}.scale.scaleZ'.format(tgt), f=True)

    cmds.connectAttr('{}.outputShear.outputShearX'.format(src), '{}.shearXY'.format(tgt), f=True)
    cmds.connectAttr('{}.outputShear.outputShearY'.format(src), '{}.shearXZ'.format(tgt), f=True)
    cmds.connectAttr('{}.outputShear.outputShearZ'.format(src), '{}.shearYZ'.format(tgt), f=True)


class SetsCopyPaste(object):
    def __init__(self, top_set):
        self.top_set = top_set
        self.copy_set_dict = OrderedDict()
        self.copy_top_attr_dict = {}

    def copy(self):
        def main(set_):
            set_member_list = cmds.sets(set_, q=True)
            if set_member_list:
                tmp_list = []
                for set_member in set_member_list:
                    type_ = cmds.nodeType(set_member)
                    if type_ == 'objectSet':
                        main(set_member)
                    tmp_list.append([type_, set_member])
                self.copy_set_dict[set_] = tmp_list
        main(self.top_set)
        #for k, v in self.copy_set_dict.items():
        #    print(k, v)
        attr_list = cmds.listAttr(self.top_set, ud=True)
        if attr_list is not None:
            for at in attr_list:
                self.copy_top_attr_dict[at] = cmds.getAttr(self.top_set + '.' + at)

    def paste(self):
        top_dict = {}
        top_dict[self.top_set] = self.copy_set_dict[self.top_set]
        self._pasteMain(top_dict)
        self.copy_set_dict.pop(self.top_set)
        self._pasteMain(self.copy_set_dict)

        if self.copy_top_attr_dict:
            for at, v in self.copy_top_attr_dict.items():
                addAt(self.top_set, at, v)

    def _pasteMain(self, dict_):
        for set_name, menber in dict_.items():
            if not cmds.objExists(set_name):
                cmds.sets(em=True, n=set_name)

            for type_, m in menber:
                if type_ == 'objectSet' and not cmds.objExists(m):
                    cmds.sets(em=True, n=m)

        for set_name, menber in dict_.items():
            for type_, m in menber:
                if cmds.objExists(m):
                    cmds.sets(m, e=True, addElement=set_name)


def setWireFrameVis(set_on=True):
    selectedPanel = cmds.getPanel(wf=True)
    state_ = 'true' if set_on else 'false'
    #shadowedWireState = str(cmds.modelEditor(selectedPanel, q=True, wos=True)).lower()
    if cmds.modelEditor(selectedPanel, ex=True):
        mm.eval('setWireframeOnShadedOption {0} "{1}";'.format(state_, selectedPanel))


def setJointXrayVis(set_on=True):
    selectedPanel = cmds.getPanel(wf=True)
    if cmds.modelEditor(selectedPanel, ex=True):
        cmds.modelEditor(selectedPanel, e=True, jointXray=set_on)


def scalingAttrVal(node, attr_name, scale_val):
    val = cmds.getAttr(node + '.' + attr_name)
    cmds.setAttr(node + '.' + attr_name, val * scale_val)


def scalingADNMove(scale_val):
    adn_list = cmds.ls(type='AssistDriveNode')
    for adn in adn_list:
        if 'Move' in cmds.getAttr(adn + '.DriveType'):
            scalingAttrVal(adn, 'MoveOffset0', scale_val)
            scalingAttrVal(adn, 'MoveOffset1', scale_val)
            scalingAttrVal(adn, 'MoveOffset2', scale_val)
            scalingAttrVal(adn, 'MoveLength', scale_val)
            scalingAttrVal(adn, 'MoveRange0', scale_val)
            scalingAttrVal(adn, 'MoveRange1', scale_val)
            scalingAttrVal(adn, 'LimitTransMinX', scale_val)
            scalingAttrVal(adn, 'LimitTransMaxX', scale_val)
            scalingAttrVal(adn, 'LimitTransMinY', scale_val)
            scalingAttrVal(adn, 'LimitTransMaxY', scale_val)
            scalingAttrVal(adn, 'LimitTransMinZ', scale_val)
            scalingAttrVal(adn, 'LimitTransMaxZ', scale_val)