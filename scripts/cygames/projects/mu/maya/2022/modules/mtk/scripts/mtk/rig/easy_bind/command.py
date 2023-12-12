# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
from collections import Counter
import glob
import os
import json

import traceback
import time
from functools import wraps
import sys

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim

import maya.cmds as cmds
import maya.mel


from . import TITLE


MODEL_GROUP_NAME = "model"
ROOT_NAME = "root"
NEED_JOINT_NAMES = ["skl", "helper", "dyn", "phy"]

# 本来はインフルエンスではないが、エクスポータ周りの対応で入ってしまっているものがある
# 後々これは抜かす
CNP_NAME = "cnp"

COLORS = {
    "skl": 3,
    "helper": 5,
    "cnp": 1,
    "mtp": 0,
    "dyn": 7,
    "phy": 7,
}

ROUND_DIGIT = 6

WEIGHT_FILE_EXT = ".sw"

config_node = None
CYLISTA_SCRIPT_PATH = "Z:/cyllista/tools/maya/modules/cyllista/scripts/"


if CYLISTA_SCRIPT_PATH not in sys.path:
    sys.path.append(CYLISTA_SCRIPT_PATH)



def _confirm_dialog(message="", title=""):
    if not title:
        title = TITLE
    rflag = False
    flag = True
    while flag:
        result = cmds.confirmDialog(title=title,
            messageAlign="center",
            message=message,
            button=["OK", "Cansel"],
            defaultButton="OK",
            cancelButton="Cansel",
            dismissString="Cansel")
        if result == "Cansel":
            rflag = False
            flag = False
        else:
            rflag = True
            flag = False
    return rflag

def _message_dialog(message="", title=""):
    """Maya UI のメッセージダイアログ表示関数

    Args:
        message (str): メッセージ内容
        title (str): タイトル
    """
    if not title:
        title = TITLE

    cmds.confirmDialog(
        message=message,
        title=title,
        button=['OK'],
        defaultButton='OK',
        cancelButton="OK",
        dismissString="OK")

    print(u"{}".format(message))


class ProgressWindowBlock(object):
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self, title='', progress=0,  minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
        self._show_progress = show_progress and (not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None
        self.status = None

    def __enter__(self):
        # logger.info('[ {} ] : Start'.format(self.title))

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status='[ {} ] : Start'.format(self.title),
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )

        self._start_time = datetime.datetime.now()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        calc_time = datetime.datetime.now() - self._start_time
        # logger.info('[ {} ] : End : Calculation time : {}'.format(self.title, calc_time))

        if self._show_progress:
            _status = 'End : Calculation time : {}'.format(calc_time)
            print(_status)
            cmds.progressWindow(e=True, status=_status)
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)
            # cmds.progressWindow(e=True,
            #         status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, self.status))

    def _set_status(self, status):
        if self._show_progress:
            cmds.progressWindow(e=True,
                    status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, status))

    def _get_status(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, status=True)

    status = property(_get_status, _set_status)

    def _set_progress(self, progress):
        if self._show_progress:
            cmds.progressWindow(e=True, progress=progress)

    def _get_progress(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, progress=True)

    progress = property(_get_progress, _set_progress)

    def is_cancelled(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, ic=True)

    @staticmethod
    def wait(sec=1.0):
        cmds.pause(sec=sec)




def get_skincluster(mesh):
    """スキンクラスタ取得

    Args:
        mesh (str): メッシュノード名

    Returns:
        [str]: スキンクラスタ名
    """
    skin_cluster = None
    _historys = cmds.listHistory(mesh)
    if _historys:
        for _history in _historys:
            if cmds.nodeType(_history) == "skinCluster":
                skin_cluster = _history
                break
    return skin_cluster


def root_mdl_name_check(long_name=""):
    """ルートノードの名前が[mdl_]で始まっているかの確認

    Args:
        long_name (str): maya node long name

    Returns:
        [bool]: [description]
    """
    mdl_flag = False
    split_name = long_name.split("|")

    if split_name[1].startswith("mdl_"):
        mdl_flag = True
    return mdl_flag

def get_need_joints(mutsu_flag=True):
    """バインドに必要なジョイントを返す

    Returns:
        [list]: バインドに必要なジョイントのロングネーム
    """
    joints = [x for x in cmds.ls(type="joint", long=True)
                                    if root_mdl_name_check(x)]
    bind_joints = []

    if mutsu_flag:
        for jnt in joints:
            # if not root_mdl_name_check(jnt):
            #     continue
            short_name = jnt.split("|")[-1]
            name_split = short_name.split("_")

            if len(name_split) < 3:
                continue

            # CNP_NAME の部分は本来あってはいけないものだが
            # とりあえずの対応としていれてある

            # 最後の部分が「"root"」のものはインフルエンスに含めない、
            # 三番目の部分が、["skl", "helper", "dyn", "phy"]
            # ものはインフルエンスに含める
            if (
                name_split[-1] != ROOT_NAME
                and name_split[2] in NEED_JOINT_NAMES
                # or name_split[1] == CNP_NAME
                ):
                bind_joints.append(jnt)
    else:
        bind_joints = joints

    return bind_joints


def get_mesh_shape_node(nodes):
    """mesh node から中間オブジェクトを抜かして返す

    Args:
        nodes (list): maya mesh nodes

    Returns:
        [list]: maya mesh nodes
    """
    meshes = cmds.listRelatives(nodes, c=True, type="mesh", fullPath=True)

    if meshes:
        meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]
    return meshes

def get_meshes():
    """選択トランスフォームノードからメッシュを取り出す

    Returns:
        [list]: mesh node list
    """
    sel = cmds.ls(sl=True, type="transform")

    if not sel:
        _message_dialog(u"トランスフォームノードを選択してください")
        return
    meshes = get_mesh_shape_node(sel)

    if not meshes:
        _message_dialog(u"選択にメッシュシェイプが見つかりませんでした")
        return
    return meshes

def get_skin_cluster(node):
    skin_cluster = ""
    _historys = cmds.listHistory(node)
    if _historys:
        for _history in _historys:
            if cmds.nodeType(_history) == "skinCluster":
                skin_cluster = _history
                break
    return skin_cluster



def get_alldescendents_mesh_nodes(node):
    meshes = cmds.listRelatives(node, ad=True, type="mesh", fullPath=True)
    if meshes:
        meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]
    return meshes

def get_group_in_meshes(node, full_path=False):
    transform_meshes = {}
    meshes = cmds.listRelatives(node, ad=True, type="mesh", fullPath=True)
    if meshes:
        for mesh in meshes:
            if cmds.getAttr("{}.intermediateObject".format(mesh)):
                continue
            if not full_path:
                parent = cmds.listRelatives(mesh, p=True, type="transform", path=True)
            else:
                parent = cmds.listRelatives(mesh, p=True, type="transform", fullPath=True)

            transform_meshes[parent[0]] = mesh

    return transform_meshes

def get_select_node_in_meshes(nodes, full_path=False):

    transform_meshes = {}
    for node in nodes:
        meshes = cmds.listRelatives(node, ad=True, type="mesh", fullPath=True)
        if not meshes:
            continue
        # meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]
        for mesh in meshes:
            if cmds.getAttr("{}.intermediateObject".format(mesh)):
                continue
            if not full_path:
                parent = cmds.listRelatives(mesh, p=True, type="transform", path=True)
            else:
                parent = cmds.listRelatives(mesh, p=True, type="transform", fullPath=True)

            transform_meshes[parent[0]] = mesh

    return transform_meshes


def get_model_node_in_meshes(scene_basename, full_path=False):
    root_nodes = cmds.ls(assemblies=True)
    model_group = ""
    transform_meshes = {}
    for node in root_nodes:
        if node not in scene_basename:
            continue
        clds = cmds.listRelatives(node, c=True, type="transform", fullPath=True)
        if clds:
            for cld in clds:
                if MODEL_GROUP_NAME in cld.split("|")[-1]:
                    model_group = cld
    if model_group:

        transform_meshes = get_group_in_meshes(model_group, full_path)

    return transform_meshes

def get_lods():
    root_nodes = cmds.ls(assemblies=True)

    lod_groups = []
    for _node in root_nodes:
        _cld = cmds.listRelatives(_node, c=True, type="transform")
        if _cld:
            for _c in _cld:
                if _c.startswith("lod"):
                    lod_groups.extend(cmds.ls(_c, l=True))

    return lod_groups

def set_joint_color(flag=0):
    """ジョイントの色変え
    for文の途中でif文を使うのでなく、最初に持ってきてみた

    Args:
        flag (int, useObjectColor flag): アトリビュート、オブジェクトカラーのスイッチ
    """

    all_joints = cmds.ls(type="joint", l=True)
    if not all_joints:
        return

    over_ride_attr_name = "overrideEnabled"
    use_color_attr_name = "useObjectColor"
    overrideColor = "overrideColor"
    if flag:
        for j in all_joints:
            # if cmds.attributeQuery(over_ride_attr_name, n=j, ex=True):
            #     cmds.setAttr("{}.{}".format(j, over_ride_attr_name), l=False)
            #     cmds.setAttr("{}.{}".format(j, use_color_attr_name), l=False)
            try:
                cmds.setAttr("{}.{}".format(j, over_ride_attr_name), 0)
                cmds.setAttr("{}.{}".format(j, use_color_attr_name), flag)
            except:pass
            short_name = j.rsplit("|", 1)[-1]
            for _name, _color_id in COLORS.items():
                if short_name.find(_name) != -1:
                    try:
                        cmds.setAttr("{}.objectColor".format(j), _color_id)
                    except:pass
    else:
        for j in all_joints:
            try:
                cmds.setAttr("{}.{}".format(j, over_ride_attr_name), 0)
                cmds.setAttr("{}.{}".format(j, use_color_attr_name), 0)
            except:pass
            # if cmds.attributeQuery(over_ride_attr_name, n=j, ex=True):
            # cmds.setAttr("{}.{}".format(j, over_ride_attr_name), l=False)
            # try:
            #     cmds.setAttr("{}.{}".format(j, over_ride_attr_name), 0)
            #     # cmds.setAttr("{}.{}".format(j, use_color_attr_name), flag)
            # except:pass



def bind_skin(nodes, joints):
    skin_clusters = []

    with ProgressWindowBlock(title='Bind Skin', maxValue=len(nodes)) as prg:
        prg.step(1)
        for node in nodes:
            shortName = node.rsplit("|", 1)[-1]
            prg.step(1)
            prg.status = '{} ...'.format(shortName)
            if prg.is_cancelled():
                break
            bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

            if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
                continue
            if not cmds.getAttr("{}.v".format(node)):
                continue
            skin_cluster = get_skincluster(node)
            if skin_cluster:
                continue

            skin_cluster = cmds.skinCluster(
                joints,
                node,
                toSelectedBones=True,
                bindMethod=0,
                normalizeWeights=True,
                weightDistribution=0,
                maximumInfluences=4,
                obeyMaxInfluences=False,
                dropoffRate=4,
                removeUnusedInfluence=False,
                name='{}_skinCluster'.format(shortName)
                # name='{}_skinCluster'.format(node[1:].replace('|', '__'))
            )
            skin_clusters.extend(skin_cluster)

    set_joint_color(1)
    return skin_clusters

def delete_joint_history(joints):
    """骨に対してヒストリの削除、

    Args:
        joints ([type]): [description]
    """
    for j in joints:
        if cmds.lockNode(j, q=True, lock=True):
            continue
        cmds.delete(j, ch=True)
        # if cmds.getAttr("{}.useObjectColor".format(j)):
        #     cmds.setAttr("{}.useObjectColor".format(j), 0)



def go_to_bindpose():
    """mel の go to bind を模倣

    Args:
        nodes (list): transform nodes
    """
    nodes = cmds.ls(type="transform", l=True)
    if not nodes:
        return
    bind_store = []

    for node in nodes:

        mesh = cmds.listRelatives(node, children=True, fullPath=True, type="mesh")
        if not mesh:
            continue
        bindPose = cmds.dagPose(node, q=True, bindPose=True)
        if not bindPose:
            continue
        if len(bindPose) == 1:
            cmds.dagPose(node, restore=True, g=True, bindPose=True)
            continue

        historys = cmds.listHistory(mesh)
        skin_cluster = [x for x in historys if cmds.nodeType(x) == "skinCluster"]

        if not skin_cluster:
            continue
        skin_cluster = skin_cluster[0]
        skinBindPosePlug = skin_cluster + ".bindPose"

        bindPose = cmds.listConnections(skinBindPosePlug,
                                        destination=False,
                                        source=True,
                                        type='dagPose')

        if bindPose:
            bindPose = bindPose[0]
            if bindPose in bind_store:
                continue
            bind_store.append(bindPose)
            try:
                cmds.dagPose(bindPose, restore=True, g=True)
            except Exception as e:
                print(e)
        else:
            influences = cmds.skinCluster(skin_cluster, q=True, inf=True)
            for inf in influences:
                bindPose = cmds.dagPose(inf, q=True, bindPose=True)
                if not bindPose:
                    continue

                bindPose = bindPose[0]
                if bindPose in bind_store:
                    continue
                bind_store.append(bindPose)
                try:
                    cmds.dagPose(bindPose, restore=True, g=True)
                except Exception as e:
                    print(e)


def unbind_skin(nodes, joints):
    """バインドの解除、ノードに対して解除、ジョイントに対してヒストリの削除

    Args:
        nodes ([type]): [description]
        joints ([type]): [description]
    """

    delete_joint_history(joints)

    with ProgressWindowBlock(title='Un Bind Skin', maxValue=len(nodes)) as prg:
        prg.step(1)
        for node in nodes:
            prg.step(1)
            prg.status = '{} ...'.format(node.rsplit("|",1)[-1])
            if prg.is_cancelled():
                break

            historys = cmds.listHistory(node)

            if [x for x in historys if cmds.nodeType(x) == "skinCluster"]:
                cmds.skinCluster(node, e=True, unbind=True)
                # cmds.bindSkin(node, unbind=True)


    bindPose = cmds.ls(type="dagPose")
    if bindPose:
        for bp in bindPose:
            if cmds.lockNode(bp, q=True, lock=True):
                continue
            try:
                cmds.delete(bindPose)
            except Exception as e:
                print(e)
    set_joint_color()

def weight_copy(src=None, dst=None):
    """ウェイトのコピー

    Args:
        src (str, skinCluster): [skinCluster name]. スキンクラスタの名前（skinCluster30）
        dst (str, skinCluster): [skinCluster name]. スキンクラスタの名前（skinCluster30）
    """

    if not src or not dst:
        return
    cmds.copySkinWeights(sourceSkin=src,
                        destinationSkin=dst,
                        noMirror=True,
                        surfaceAssociation="closestPoint",
                        influenceAssociation='oneToOne',
                        # influenceAssociation=('label', 'oneToOne', 'closestJoint'),
                        noBlendWeight=True,
                        normalize=True)

def save_weight_file_cmds(shape="",
                        export_path="",
                        file_name="",
                        scene_basename="",
                        deformer=""):
    """ウェイトの書き出し

    Args:
        shape (str): mesh node name
        export_path (str): file path
        file_name (str): file name
        scene_basename (str): scene name
        deformer (str): パターンを使用する場合
    """
    if not export_path:
        export_path = os.path.join(os.environ["HOME"], "easy_bind", scene_basename).replace(os.sep, '/')

    if not os.path.exists(export_path):
        os.makedirs(export_path)

    cmds.deformerWeights(
            file_name,
            export = True,
            shape = shape,
            # deformer = deformer,
            path = export_path,
            # method = method,
            weightPrecision = 6,
            defaultValue = 0.0,
            # vertexConnections = True,
            )



def load_weight_file_cmds(shape= "",
                        import_path="",
                        file_name="",
                        scene_basename="",
                        deformer="",
                        method="index"):

    """ウェイトファイル読み込み
    Maya 標準機能を使った

    Args:
        shape (str): mesh node name
        import_path (str): file path
        file_name (str): file name
        scene_basename (str): scene name
        deformer (str): パターンを使用する場合
        method (str): メソッドここでは index のみ

    Returns:
        [type]: [description]
    """

    if not import_path:
        import_path = os.path.join(os.environ["HOME"], "easy_bind", scene_basename)

    cmds.deformerWeights(
            file_name,
            im = True,
            shape = shape,
            # deformer = deformer,
            path = import_path,
            method = method,
            weightPrecision = 6,
            defaultValue = 0.0,
            ignoreName = False
            )

    return True

def set_weight_zero(mesh, skinCluster):
    """ウェイトに強制的に0 を割り当て

    Args:
        mesh ([type]): [description]
        skinCluster ([type]): [description]
    """
    sel_list = om2.MSelectionList()
    sel_list.add(mesh)

    dag_path = sel_list.getDagPath(0)
    mesh_fn = om2.MFnMesh(dag_path)

    skinNode = om2.MGlobal.getSelectionListByName(skinCluster).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    indices = range(mesh_fn.numVertices)
    fnCompNew = om2.MFnSingleIndexedComponent()
    vertexComp = fnCompNew.create(om2.MFn.kMeshVertComponent)
    fnCompNew.addElements(indices)

    infDags = skinFn.influenceObjects()
    infIndices = om2.MIntArray(len(infDags), 0)
    shape = len(infDags)

    for x in range(shape):
        infIndices[x] = x

    set_weights = [0.0] * (len(indices) * shape)
    skinFn.setWeights(dag_path, vertexComp, infIndices, om2.MDoubleArray(set_weights), False)




def get_polygon_shell(node):
    """ポリゴンシェル（ポリゴンアイランド）のリストごとに
    ポリゴンIDがリストで入る

    Args:
        node ([str]): maya_mesh_node

    Returns:
        [list]: [[0, 1], [2, 3]]
    """
    island_list = []
    for i in range(cmds.polyEvaluate(node, face=True)):
        _li = list(set(cmds.polySelect(node, q=True, extendToShell=i, ns=True)))
        if not island_list:
            island_list = [_li]
        elif _li not in island_list:
            island_list = island_list + [_li]
    return island_list


def get_boundary_one_vtx(node_name, polygon_shell):
    """入力されたポリゴンシェルの境界にある一つの頂点と
    ポリゴンシェルの全頂点のリスト、抽出した一つの頂点の位置を返す

    Args:
        node_name (str): maya mesh node
        polygon_shell (list): polygon face ids

    Returns:
        _id [int]: 境界にある一つの頂点
        all_vtx [list]: ポリゴンシェルの頂点ID
        _position [MPoint]: 一つの頂点の場所
    """
    all_vtx = []
    _id = None
    _position = None

    selection = om2.MSelectionList()
    selection.add(node_name)
    dag_path = selection.getDagPath(0)
    space = om2.MSpace.kWorld
    mitMeshPolygonIns = om2.MItMeshPolygon(dag_path)

    for n in polygon_shell:
        mitMeshVertIns = om2.MItMeshVertex(dag_path)
        mitMeshPolygonIns.setIndex(n)
        vids = mitMeshPolygonIns.getVertices()
        all_vtx.extend(vids)

        for v in vids:
            mitMeshVertIns.setIndex(v)
            if mitMeshVertIns.onBoundary():
                _id = v
                _position = mitMeshVertIns.position(space)
                boundry_flag = True
                break

    return _id, list(set(all_vtx)), _position

