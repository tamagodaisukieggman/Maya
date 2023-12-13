# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import OrderedDict

import os
import maya.cmds as cmds
import maya.mel

from . import TITLE
from . import NAME
from . import HDA_PATH
from . import LOD_CREATE_HDA_NAME
from . import gui_util
# reload(gui_util)


def get_parents(node = ""):
    """ルートノード取得

    Args:
        node (str)): Maya ノードの文字列

    Yields:
        [type]: [description]
    """
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in get_parents(parent):
            yield p

def get_scene_lod_create_hdas(suffix = ""):
    _hdas = cmds.ls("*" + suffix, l=True, type="houdiniAsset")

    if _hdas:
        return _hdas
    else:
        return

def get_scene_lod_create_hda():
    _hda = cmds.ls("|{}*".format(LOD_CREATE_HDA_NAME), l=True)

    if _hda:
        return _hda[0]
    else:
        return _hda

def check_asset(hda_name):
    error = ""
    _hda = cmds.ls("*{}*".format(hda_name))

    if _hda:
        error = u"[ {} ] がすでにシーンにあります\n".format(_hda[0])
        error += u"[ 生成確定 ] を行ってから再度実行してください"
    return error


def check_hda(hda_name):
    hda_path = os.path.join(HDA_PATH,
                hda_name + ".hda").replace(os.sep, '/')

    _asset_name = cmds.houdiniAsset(listAssets=hda_path)
    return _asset_name

def load_hda(hda_name, asset_name):
    hda_path = os.path.join(HDA_PATH, hda_name + ".hda").replace(os.sep, '/')
    _hda = cmds.houdiniAsset(loadAsset=[hda_path, asset_name])
    return _hda

def apply_hda(hda_name, suffix):
    root_node = ""
    _asset_name = check_hda(hda_name)
    if not _asset_name:
        _m = u"[ {} ] が読み込めませんでした".format(hda_name)
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return None, None

    _asset_name = _asset_name[0]
    selection = cmds.ls(sl=True, l=True, type="transform")
    if not selection:
        _m = u"[ トランスフォームノード ] を選択してから実行してください"
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return None, None

    if len(selection) != 1:
        _m = u"選択する [ トランスフォームノード ] は一つで実行してください"
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return None, None

    meshes = cmds.listRelatives(selection, ad=True, fullPath=True, type="mesh")
    if not meshes:
        _m = u"選択範囲にメッシュがありませんでした"
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return None, None

    meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]

    if not meshes:
        _m = u"選択範囲にメッシュがありませんでした"
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return None, None

    if "houdiniInputGeometry" in [cmds.nodeType(x) for x in cmds.listConnections(meshes)]:
        _m = u"既に Houdini Digital Asset が適用されております\n"
        _m += u"bake asset を行うか、違うジオメトリに適用してください"
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return None, None

    for parent in get_parents(selection):
        root_node = parent

    if not root_node:
        root_node = selection[0]

    name_seach = root_node + suffix
    if name_seach in cmds.ls(assemblies=True, l=True):
        _m = u"[ {} ] はすでに存在します\n\n".format(name_seach)
        _m += u"[ {} ] の名前を変更するか\n\n".format(root_node)
        _m += u"[ {} ] を削除してから再度実行してください".format(name_seach)
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return None, None

    mel_string_array = '{{ {} }}'.format(', '.join(['"{}"'.format(s) for s in meshes]))

    _hda = load_hda(hda_name, _asset_name)
    _hda = cmds.ls(_hda, l=True)[0]

    maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(
        _hda + ".input[0].inputNodeId", mel_string_array))

    return _hda, root_node

def apply_lod_create_hda(suffix = ""):
    hda, root = apply_hda(LOD_CREATE_HDA_NAME, suffix)
    return hda, root

def get_base_transform_nodes(hda):
    meshes = cmds.listRelatives(hda, ad=True, fullPath=True, type="mesh")
    if not meshes:
        return
    meshes = [x for x in meshes
                    if x and not cmds.getAttr("{}.intermediateObject".format(x))]
    if not meshes:
        return

    shapes = [cmds.ls(x, l=True)[0] for x in cmds.listHistory(meshes, af=True)
                                                    if cmds.nodeType(x)=="mesh"]
    if not shapes:
        return
    shapes = [x for x in shapes if len(x.split(hda))==1]
    if not shapes:
        return

    transform_nodes = cmds.listRelatives(shapes, p=True, fullPath=True, type="transform")

    if transform_nodes:
        return transform_nodes
    else:
        return

def get_sets_faces(sets_name):
    faces = []
    for face in cmds.ls(cmds.sets(sets_name, q=True), fl=True, l=True):
        faces.append(face)
    return faces

def duplicate_node(node, new_name, ids):
    dup_obj = cmds.duplicate(node, rc=True)[0]
    dup_obj_long_name = cmds.ls(dup_obj, l=True)[0]
    dup_base_name = dup_obj_long_name.rsplit("_", 1)[0]

    all_face_ids = [x.rsplit("[", 1)[-1].rsplit("]")[0] for x in cmds.ls("{}.f[*]".format(
                                                                dup_obj_long_name), fl=True)]
    del_ids = [x for x in all_face_ids if x not in ids]
    if del_ids:
        del_faces = ["{}.f[{}]".format(dup_obj_long_name, x) for x in del_ids]
        cmds.delete(del_faces)
    dup_obj = cmds.rename(dup_obj, new_name)
    dup_obj = cmds.ls(dup_obj, l=True)[0]
    world_dup_obj = cmds.ls(cmds.parent(dup_obj, world=True), l=True)[0]

    return world_dup_obj

def sort_outliner(root_node):
    _new_list = []
    _order = ["model", "lod", "collision"]

    _cld = cmds.listRelatives(root_node, c=True, fullPath=True, type="transform")
    _lods = [x for x in _cld if x.split("|")[-1].startswith("lod")]
    _lods = sorted(_lods)

    _model = None
    _collision = None
    _other = []

    for _c in _cld:
        _short_name = _c.rsplit("|")[-1]
        if _short_name == "model":
            _model = _c
            _new_list.append(_c)
        elif _short_name == "collision":
            _collision = _c
        elif _c not in _lods:
            _other.append(_c)

    _new_list.extend(_lods)
    if _collision:
        _new_list.append(_collision)
    if _other:
        _new_list.extend(_other)

    for _ in _new_list:
        cmds.reorder(_, b=True)

def sync_asset(hda, sync_attribute=False, sync_output=False):
    if not cmds.objExists(hda):
        return
    if not cmds.attributeQuery("outputHiddenObjects", n=hda, ex=True):
        hidden_flag = cmds.getAttr(hda + ".outputHiddenObjects")
    else:
        hidden_flag = False
    if not cmds.attributeQuery("outputTemplatedGeometries", n=hda, ex=True):
        template_flag = cmds.getAttr(hda + ".outputTemplatedGeometries")
    else:
        template_flag = False
    cmds.houdiniAsset(sync=hda, sa=sync_attribute, so=sync_output, shi=hidden_flag, stm=template_flag)

def bake_asset(hda, lods):
    sync_asset(hda, sync_output=True)
    base_nodes = get_base_transform_nodes(hda)
    base_short_node = ""
    root_node = None
    lod_groups = OrderedDict()
    _keep_lod_group = []

    if base_nodes:
        node_name = base_nodes[0]
        base_short_node = node_name.rsplit("|", 1)[-1]
        for _p in get_parents(node_name):
            root_node = _p
    else:
        base_short_node = hda.rsplit("|")[-1] + "_mesh"

    if root_node:
        _lod_groups = cmds.listRelatives(root_node, c=True, fullPath=True, type="transform")
        if _lod_groups:
            for _l in _lod_groups:
                if _l.rsplit("|", 1)[-1].startswith("lod"):
                    _lod_num = _l.split("lod")[-1]
                    lod_groups[_lod_num] = _l

    _error = []
    with gui_util.ProgressWindowBlock(title='...', maxValue=lods) as prg:
        for i in range(1, lods + 1):
            lod = "lod{}".format(i)

            prg.step(1)
            prg.status = '{} ...'.format(lod)
            if prg.is_cancelled():
                break

            new_name = base_short_node + "_{}".format(lod)
            lod_sets_name = "{}_*".format(lod)
            lod_group = lod_groups.get(str(i), None)
            lod_set = cmds.ls(lod_sets_name, type="objectSet")

            if not lod_set:
                _error.append(lod)
                continue

            _faces = cmds.ls(cmds.sets(lod_sets_name, q=True), fl=True, l=True)

            _source_name = _faces[0].rsplit(".", 1)[0]
            _face_ids = [x.rsplit("[", 1)[-1].rsplit("]")[0] for x in _faces]
            dup_obj = duplicate_node(_source_name, new_name, _face_ids)

            if lod_group:
                _keep_lod_group.append(lod_group)
                _lod_nodes = cmds.listRelatives(lod_group,
                                        c=True, fullPath=True, type="transform")
                if _lod_nodes:
                    cmds.delete(_lod_nodes)
                cmds.parent(dup_obj, lod_group)
            elif root_node:
                lod_group = cmds.createNode('transform', n=lod, ss=True)
                cmds.parent(dup_obj, lod_group)
                cmds.parent(lod_group, root_node)

    if root_node:
        sort_outliner(root_node)

    _delete_lod_groups = set(lod_groups.values()) - set(_keep_lod_group)

    if _delete_lod_groups:
        cmds.delete(list(_delete_lod_groups))

    if _error:
        _m = u"[ {} ] \n".format(", ".join(_error))
        _m += u"はポリゴン数がゼロのため生成されませんでした"
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()

def get_lod_sets():
    _set = cmds.ls("lod*", type="objectSet")
    return _set

def get_lod_set(num):
    _set = cmds.ls("lod{}_*".format(num), type="objectSet")
    return _set

def delete_sets():
    _set = get_lod_sets()
    if _set:
        cmds.delete(_set)
