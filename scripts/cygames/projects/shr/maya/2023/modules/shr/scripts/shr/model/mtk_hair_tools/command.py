# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
from pathlib import Path
from collections import OrderedDict
import glob
import os
import subprocess
import random
import webbrowser

import importlib

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import maya.mel

from . import TITLE
from . import NAME

from . import util
from . import gui_util

from . import IMAGE_MAGICK_PATH
from . import VTX_COLOR_SET_NAME
from . import RESOLUTIONS_DICT
from . import PRESET_TEXTURE_PREFEX
from . import HOUDINI_ENGINE_PLUGIN_NAME
from . import HOUDINI_ENGINE_PLUGIN_EXT
from . import HOUDINI_PLUGIN_PATH
from . import HDA_NAME
from . import REMOVE_HDA_NAME
from . import HDA_PATH
from . import ONE_CARD
from . import ALL_CARD
from . import BAKE_SOURCE_NAME
from . import BAKE_TARGET_NAME
from . import FINAL_NAME
from . import MAP_SAMPLING_LIST
from . import EXPORT_MAP_TYPES
from . import HAIR_CARD_NAME
from . import SHADING_NODE_NAME

from . import automation_tool_kit
from mtk.utils.hda_loader import houdini_util


importlib.reload(houdini_util)
importlib.reload(util)
importlib.reload(gui_util)
importlib.reload(automation_tool_kit)


def speed_check(func):
    def _wrapper(*args, **keywargs):
        start_time = time.time()

        result = func(*args, **keywargs)
        result_time = time.time() - start_time

        if result_time > 60:
            result_time = f'{result_time / 60.0:.6f} [min]'
        elif result_time > 3600:
            result_time = f'{result_time / 3600.0:.6f} [hours]'
        elif result_time > 86400:
            result_time = f'{result_time / 86400.0:.6f} [days]'
        else:
            result_time = f'{result_time:.6f} [sec]'

        print(
            f'function: [ {func.__name__} ]:  time: {result_time}')
        return result
    return _wrapper


def jump_confluence():
    _web_site = "https://wisdom.cygames.jp/pages/viewpage.action?pageId=193868945"
    try:
        webbrowser.open(_web_site)
    except Exception as e:
        print("error--- ", e)


def get_parents(node):
    """再帰的にMayaのノードの親をたどりルートを返す

    Args:
        node (str): maya dag node

    Yields:
        [str]: dag_root_node
    """
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in get_parents(parent):
            yield p


def image_magick(image_magick_path):
    _com = ""
    image_magick_path = image_magick_path.replace(os.sep, '/')
    image_magick_exists = os.path.exists(image_magick_path)
    if image_magick_exists:
        _com = "{} convert ".format(image_magick_path)
    return _com


def get_polygon_shell(node):
    """メッシュを受け取りポリゴンアイランドごとの
    フェイスインデックスリストを返す

    Args:
        node (str): maya mesh node

    Returns:
        [[list], [list]]: [インデックスごとのリスト]
    """
    island_list = []

    face_conut = cmds.polyEvaluate(node, face=True)
    with gui_util.ProgressWindowBlock(title='Random Color', maxValue=face_conut) as prg:
        for i in range(face_conut):
            _li = list(
                set(cmds.polySelect(node, q=True, extendToShell=i, ns=True)))
            if not island_list:
                island_list = [_li]
            elif _li not in island_list:
                island_list = island_list + [_li]
            prg.status = '{} ...'.format(node)
            if prg.is_cancelled():
                break
            prg.step(1)
    return island_list


def assign_vtx_color_on_polygon_shell(mesh_fn, island_list, prg=None):
    """API2.0 を使用
    meshFn とインデックスリストの二次元配列を受け取り、
    各リストごとにランダムな頂点カラーを適用

    Args:
        mesh_fn (meshFn): API2.0 meshFn
        island_list ([[list], [list]]): フェイスインデックスが入った二次元リスト
        prg ([maya プログレスオブジェクト]): [description]. Defaults to None.
    """
    _v = []
    cColorArry = om2.MColorArray()
    for face_ids in island_list:
        shell_color = om2.MColor(
            (random.random(), random.random(), random.random(), 1.0))
        for face_id in face_ids:
            for v in mesh_fn.getPolygonVertices(face_id):
                if prg:
                    prg.step(1)
                cColorArry.append(shell_color)
                _v.append(v)
    mesh_fn.setVertexColors(cColorArry, _v)
    mesh_fn.updateSurface()


def get_mesh_fns(selections):
    dag_path_mesh_fn = OrderedDict()
    for node in selections:

        # sel_list = om2.MGlobal.getSelectionListByName(node)
        # dagPath = sel_list.getDagPath(0)

        meshes = cmds.listRelatives(node, s=True, fullPath=True, type="mesh")
        meshes = [x for x in meshes
                  if x and not cmds.getAttr("{}.intermediateObject".format(x))]
        if not meshes:
            continue

        mesh = meshes[0]
        sel_list = om2.MGlobal.getSelectionListByName(mesh)
        dagPath = sel_list.getDagPath(0)

        if not dagPath.hasFn(om2.MFn.kMesh):
            continue

        mesh_fn = om2.MFnMesh(dagPath)
        dag_path_mesh_fn[dagPath.fullPathName()] = mesh_fn

    return dag_path_mesh_fn


def apply_random_vertex_color_polygon_shell():
    selection = cmds.ls(sl=True, type="transform")
    if not selection:
        return

    dag_path_mesh_fn = get_mesh_fns(selection)

    _m = u"現在選択されている [ {} ] 個のメッシュの\n".format(len(dag_path_mesh_fn))
    _m += u"ポリゴンシェルに対して"
    _m += u"ランダムな頂点カラーを割り当てます\n\n"
    _m += u"よろしいですか？"

    _d = gui_util.ConformDialogResult(title=TITLE, message=_m)
    result = _d.exec_()
    if not result:
        return

    cmds.optionVar(intValue=("polyAutoShowColorPerVertex", 1))

    for dag_name, mesh_fn in dag_path_mesh_fn.items():
        vtx_color = [x for x in cmds.listHistory(dag_name, af=True)
                     if cmds.nodeType(x) == "polyColorPerVertex"]

        if vtx_color:
            cmds.delete(vtx_color)

        island_list = get_polygon_shell(dag_name)
        assign_vtx_color_on_polygon_shell(mesh_fn, island_list)
        # cmds.setAttr(dag_name + ".displayColors", 1)

    for s in selection:
        cmds.polyOptions(s, colorShadedDisplay=True)
        cmds.polyOptions(s, colorMaterialChannel="none")


def check_source_node(node):
    _ornatrix_guide_node = ""
    for parent in get_parents(node):
        # print(parent, " ----------------------------- parent")
        _p_historys = cmds.listHistory(parent, force=True)
        _p_historys = [cmds.nodeType(x) for x in _p_historys if cmds.nodeType(
            x) == "GuidesFromMeshNode"]
        if _p_historys:
            _ornatrix_guide_node = parent
    return _ornatrix_guide_node


def check_transform_selection():
    selections = cmds.ls(sl=True, type="transform", l=True)
    if not selections or len(selections) != 2:
        _m = u"2つのトランスフォームノードを選択してから実行してください"
        _d = gui_util.ConformDialog(title=u"選択確認",
                                    message=_m)
        _d.exec_()
        return None

    nodes = []
    source_check = check_source_node(selections[0])

    if source_check:
        nodes.append(source_check)
    else:
        nodes.append(selections[0])
    nodes.append(selections[-1])

    return nodes


def check_export_path(export_path):
    if not os.path.exists(export_path):
        _m = u"ディレクトリ\n[ {} ]\nが存在しません、ご確認ください".format(export_path)
        _d = gui_util.ConformDialog(title=u"フォルダ確認", message=_m)
        _d.exec_()
        return False
    else:
        return True


def check_preset_name(preset_name):
    _check_text = r':;/\|,*?"<>'
    _m = ""
    if not preset_name:
        _m = u"ヘアプリセットの名前を設定してください"

    for _ in preset_name:
        if _ in _check_text:
            _m = u"ヘアプリセット名に [ {} ] の文字列は使用できません".format(_check_text)
            break

    if _m:
        _d = gui_util.ConformDialog(title=u"名前の確認", message=_m)
        _d.exec_()
        return False
    else:
        return True


def check_preset_path(export_path):
    flag = True
    if os.path.exists(export_path):
        _m = u"出力フォルダ\n[ {} ]\nは既に存在します".format(
            export_path.replace(os.sep, '/'))
        _m += u"既にあるものを削除し、新たに作りますか？"
        _d = gui_util.ConformDialogResult(title=u"フォルダ確認", message=_m)
        result = _d.exec_()
        if not result:
            return False
        util.cleat_directory(export_path)
    os.makedirs(export_path)
    return True


def get_target_uv_size_u_min_max(target):
    maps = cmds.ls(cmds.polyListComponentConversion(target, tuv=True), fl=True)

    uv_values = cmds.polyEditUV(maps, q=True, v=True)
    u_values = uv_values[0::2]
    v_values = uv_values[1::2]

    return min(u_values), max(u_values), min(v_values), max(v_values)


class SGInMembers:
    def __init__(self, SG="", members=[]):
        self.SG = SG
        self.members = members

    def __repr__(self):
        return self.SG


class ArnoldRenderTextureBake(object):
    def __init__(self,
                 hair_preset_path="",
                 export_path="",
                 source_node=None,
                 target_node=None,
                 export_maps=[],
                 file_name="",
                 resolution=1024,
                 aa_samples=3,
                 _filter="box",
                 filter_width=1.0,
                 normal_offset=10.0,
                 enable_aovs=False,
                 extend_edges=False,
                 _crop_uv_flag=True,
                 black_bg_flag=False
                 ):
        self._show_hide_flags = OrderedDict()

        self.all_udims = False
        self.udims = ""
        self.uStart = 0.0
        self.uScale = 1.0
        self.vStart = 0.0
        self.vScale = 1.0
        self.useSequence = False
        self.frameStart = 0.0
        self.frameEnd = 10.0
        self.frameStep = 1.0
        self.framePadding = 0.0

        self.output_size = RESOLUTIONS_DICT[resolution]

        self.hair_preset_path = hair_preset_path
        self.export_path = export_path
        self.source_node = source_node
        self.target_node = target_node
        self.export_maps = export_maps

        self.file_name = file_name
        self.resolution = resolution
        self.aa_samples = aa_samples
        self._filter = _filter
        self.filter_width = filter_width
        self.normal_offset = normal_offset
        self.enable_aovs = enable_aovs
        self.extend_edges = extend_edges
        self.crop_uv = _crop_uv_flag
        self.black_bg_flag = black_bg_flag

        self.target_nodes = self.get_mesh_nodes(target_node)
        self.source_nodes = self.get_mesh_nodes(source_node)
        self.exr_path = self.create_exr_path(target_node)

    def set_visible_node(self, node_type="source"):
        _dict = self.source_nodes if node_type == "source" else self.target_nodes
        _check_node = self.source_node if node_type == "source" else self.target_node

        for transform, mesh in _dict.items():

            if transform not in self._show_hide_flags:
                self._show_hide_flags[transform] = cmds.getAttr(
                    "{}.v".format(transform))
            cmds.setAttr("{}.v".format(transform), 1)

            for parent in get_parents(transform):
                # ヘアジオメトリを直接選択した状態でも正しくベイクしたいが
                # 難しい
                # _historys = cmds.listHistory(parent, f=True)
                # _historys = [x for x in _historys if cmds.nodeType(x) == "GuidesFromMeshNode"]
                # if _historys:
                #     cmds.setAttr("{}.v".format(mesh), 0)
                if parent not in self._show_hide_flags:
                    self._show_hide_flags[parent] = cmds.getAttr(
                        "{}.v".format(parent))
                cmds.setAttr("{}.v".format(parent), 1)

            if mesh not in self._show_hide_flags:
                self._show_hide_flags[mesh] = cmds.getAttr("{}.v".format(mesh))
            if node_type == "source":
                # ヘアジオメトリを直接選択した状態でも正しくベイクしたいが
                # 難しい
                # _guides = cmds.listHistory(transform, f=True)
                # _guides = [x for x in _guides if cmds.nodeType(x) == "EditGuidesShape"]
                if transform == _check_node:
                    _guides = cmds.listHistory(transform, f=True)
                    _guides = [x for x in _guides if cmds.nodeType(
                        x) == "EditGuidesShape"]
                    if _guides:
                        cmds.setAttr("{}.v".format(mesh), 0)
                    else:
                        cmds.setAttr("{}.v".format(mesh), 1)
                else:
                    self.check_ornatrix_uv_attr(mesh)
                    cmds.setAttr("{}.v".format(mesh), 1)
            else:
                cmds.setAttr("{}.v".format(mesh), 1)

    def check_ornatrix_uv_attr(self, node):
        _historys = [x for x in cmds.listHistory(
            node) if cmds.nodeType(x) == "MeshFromStrandsNode"]
        if not _historys:
            return
        _history = _historys[0]
        for _attr in cmds.listAttr(_history):
            if _attr.endswith("usePerStrandMapping"):
                if cmds.getAttr(_history + "." + _attr) == [0]:
                    cmds.setAttr(_history + "." + _attr,
                                 [1], type="Int32Array")
                    break

    def set_visible_transform(self):
        _all_transform = cmds.ls(type="transform", l=True)
        for _transform in _all_transform:
            if _transform not in self._show_hide_flags:
                self._show_hide_flags[_transform] = cmds.getAttr(
                    "{}.v".format(_transform))
            cmds.setAttr("{}.v".format(_transform), 0)

    def set_up_bake_process(self):
        self._show_hide_flags = OrderedDict()
        _folder_remove_error = None
        try:
            util.clear_temp_directory()
        except Exception as e:
            _folder_remove_error = e

        if not _folder_remove_error:
            self.set_visible_transform()
            self.set_visible_node("source")
            self.set_visible_node("target")

            self.get_shading_groups()
        return _folder_remove_error

    def end_bake_process(self):
        for node, flag in self._show_hide_flags.items():
            if cmds.objExists(node):
                cmds.setAttr("{}.v".format(node), flag)

    def get_mesh_nodes(self, node):
        """受け取ったノード以下のメッシュノードを全部取得
        メッシュの親のトランスフォームノードをキーにしてシェイプを格納

        Args:
            node (str): Maya Transform node

        Returns:
            [OrderdDict]: [transform node: mesh node]
        """
        mesh_parent_dict = OrderedDict()
        _cld = cmds.listRelatives(
            node, allDescendents=True, fullPath=True, type="mesh")
        if _cld:
            for c in _cld:
                _p = cmds.listRelatives(c, p=True, fullPath=True)
                if _p:
                    mesh_parent_dict[_p[0]] = c
        return mesh_parent_dict

    def get_shading_groups(self):
        self.sg_members = []
        target_shape_nodes = list(
            self.source_nodes.values()) + list(self.target_nodes.values())
        target_nodes = list(self.source_nodes.keys()) + \
            list(self.target_nodes.keys())

        for node_longname in target_shape_nodes:
            if not cmds.objExists(node_longname):
                continue
            sg = cmds.listConnections(
                node_longname, s=False, d=True, t='shadingEngine')
            if not sg:
                continue
            SGs = list(set(cmds.listConnections(
                node_longname, s=False, d=True, t='shadingEngine')))
            for SG in SGs:
                members = [x for x in cmds.ls(cmds.sets(SG, q=True), l=True)if x.split(
                    ".")[0] in target_nodes or x.split(".")[0] in node_longname]
                mem = SGInMembers(SG, members)
                self.sg_members.append(mem)

    def create_exr_path(self, node):
        """ファイルリネームをするためあらかじめファイル名を作っておく
        ファイル名はArnoldのデフォルトでシェイプ名になる

        Args:
            node (str): トランスフォームノード

        Returns:
            [str]: Arnoldで生成されるファイル名
        """
        exr = ""
        shape = cmds.listRelatives(node, s=True, path=True)
        if shape:
            exr = os.path.join(self.export_path, "{}.exr".format(shape[0]))
        return exr.replace(os.sep, '/')

    def create_material(self, map_type):
        """マテリアル生成、map_typeに応じたマテリアルを生成

        Args:
            map_type (str): 出力マップタイプ

        Returns:
            [list]: マップ生成時に作ったシェーダを戻しまとめて消す
        """
        shader = []

        if map_type == "normal":
            shader = self.normal(map_type)
        elif map_type == "flow":
            shader = self.flow(map_type)
        elif map_type == "ao":
            shader = self.ao(map_type)
        elif map_type == "root":
            shader = self.root(map_type)
        elif map_type == "depth":
            shader = self.depth(map_type)
        elif map_type == "alpha":
            shader = self.alpha(map_type)
        elif map_type == "vcolor":
            shader = self.vtx_color(map_type)
        return shader

    def normal(self, map_type):
        sg = cmds.sets(n="{}SG".format(map_type), renderable=True,
                       noSurfaceShader=True, empty=True)
        shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type, skipSelect=True)
        cmds.setAttr("{}.shadeMode".format(shader), 2)
        cmds.setAttr("{}.colorMode".format(shader), 3)

        cmds.connectAttr('{}.outColor'.format(shader),
                         '{}.surfaceShader'.format(sg), force=True)
        cmds.sets(self.all_shapes, edit=True, forceElement=sg)
        return [sg, shader]

    def flow(self, map_type):
        sg = cmds.sets(n="{}SG".format(map_type), renderable=True,
                       noSurfaceShader=True, empty=True)
        shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type, skipSelect=True)
        sampler_node = cmds.shadingNode('samplerInfo', name="{}_info".format(
            map_type), asUtility=True, skipSelect=True)
        range_node = cmds.shadingNode(
            'setRange', asUtility=True, name="{}_range".format(map_type), skipSelect=True)
        cmds.setAttr("{}.shadeMode".format(shader), 2)
        cmds.setAttr("{}.colorMode".format(shader), 0)
        cmds.connectAttr(sampler_node + '.tangentVCamera',
                         range_node + '.value', force=True)
        cmds.connectAttr(range_node + '.outValue',
                         shader + '.color', force=True)
        cmds.setAttr(range_node + '.max', 1, 1, 1)
        cmds.setAttr(range_node + '.oldMin', -1, -1, -1)
        cmds.setAttr(range_node + '.oldMax', 1, 1, 1)
        cmds.connectAttr('{}.outColor'.format(shader),
                         '{}.surfaceShader'.format(sg), force=True)
        cmds.sets(self.all_shapes, edit=True, forceElement=sg)
        return [sg, sampler_node, range_node, shader]

    def ao(self, map_type):
        fg_sg = cmds.sets(n="{}fgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        bg_sg = cmds.sets(n="{}bgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode(
            "aiStandardSurface", asShader=True, name=map_type+"fg", skipSelect=True)
        fg_ao_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"fgao", skipSelect=True)
        bg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"bg", skipSelect=True)

        cmds.setAttr("{}.shadeMode".format(fg_ao_shader), 3)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(fg_ao_shader), 0)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)
        cmds.setAttr("{}.emission".format(fg_shader), 1.0)

        if self.black_bg_flag:
            cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        else:
            cmds.setAttr("{}.color".format(bg_shader), 1, 1, 1, type="double3")

        cmds.connectAttr('{}.outColor'.format(fg_ao_shader),
                         '{}.emissionColor'.format(fg_shader), force=True)
        cmds.connectAttr('{}.outColor'.format(fg_shader),
                         '{}.surfaceShader'.format(fg_sg), force=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader),
                         '{}.surfaceShader'.format(bg_sg), force=True)

        # if self.alpha_map:
        #     cmds.connectAttr("{}.outColor".format(self.alpha_map), "{}.opacity".format(fg_shader), force=True)

        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)
        return[fg_sg, fg_shader, bg_sg, bg_shader, fg_ao_shader]

    def root(self, map_type):
        fg_sg = cmds.sets(n="{}fgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        bg_sg = cmds.sets(n="{}bgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"fg", skipSelect=True)
        bg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"bg", skipSelect=True)
        cmds.setAttr("{}.shadeMode".format(fg_shader), 2)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(fg_shader), 5)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)

        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)
        cmds.connectAttr('{}.outColor'.format(fg_shader),
                         '{}.surfaceShader'.format(fg_sg), force=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader),
                         '{}.surfaceShader'.format(bg_sg), force=True)
        return[fg_sg, fg_shader, bg_sg, bg_shader]

    def depth(self, map_type):
        fg_sg = cmds.sets(n="{}fgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        bg_sg = cmds.sets(n="{}bgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"fg", skipSelect=True)
        bg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"bg", skipSelect=True)

        cmds.setAttr("{}.shadeMode".format(fg_shader), 2)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        # cmds.setAttr("{}.colorMode".format(fg_shader), 9)
        cmds.setAttr("{}.colorMode".format(fg_shader), 10)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)

        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)

        cmds.connectAttr('{}.outColor'.format(fg_shader),
                         '{}.surfaceShader'.format(fg_sg), force=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader),
                         '{}.surfaceShader'.format(bg_sg), force=True)
        return[fg_sg, fg_shader, bg_sg, bg_shader]

    def alpha(self, map_type):
        fg_sg = cmds.sets(n="{}fgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        bg_sg = cmds.sets(n="{}bgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"fg", skipSelect=True)
        bg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"bg", skipSelect=True)
        cmds.setAttr("{}.shadeMode".format(fg_shader), 2)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(fg_shader), 0)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)
        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)
        cmds.connectAttr('{}.outColor'.format(fg_shader),
                         '{}.surfaceShader'.format(fg_sg), force=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader),
                         '{}.surfaceShader'.format(bg_sg), force=True)
        return[fg_sg, fg_shader, bg_sg, bg_shader]

    def vtx_color(self, map_type):
        fg_sg = cmds.sets(n="{}fgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        bg_sg = cmds.sets(n="{}bgSG".format(map_type),
                          renderable=True, noSurfaceShader=True, empty=True)
        bg_shader = cmds.shadingNode(
            "aiUtility", asUtility=True, name=map_type+"bg", skipSelect=True)

        fg_shader = cmds.shadingNode(
            "aiUserDataColor", asUtility=True, name=map_type+"fg", skipSelect=True)
        cmds.setAttr("{}.colorAttrName".format(fg_shader),
                     VTX_COLOR_SET_NAME, type="string")

        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)

        cmds.setAttr("{}.defaultValue".format(
            fg_shader), 1, 1, 1, type="double3")
        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")

        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)

        cmds.connectAttr('{}.outColor'.format(fg_shader),
                         '{}.surfaceShader'.format(fg_sg), force=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader),
                         '{}.surfaceShader'.format(bg_sg), force=True)
        return[fg_sg, fg_shader, bg_sg, bg_shader]

    def switch_occlusion(self, value=True):
        """Arnold用AOベイク時のシャドウ設定（シェイプに対して）

        Args:
            value (bool, optional): [description]. Defaults to True.
        """
        for target in self.target_shapes:
            cmds.setAttr("{}.castsShadows".format(target), 0)
            cmds.setAttr("{}.aiSelfShadows".format(target), 0)
        for target in self.source_shapes:
            cmds.setAttr("{}.castsShadows".format(target), value)
            cmds.setAttr("{}.aiSelfShadows".format(target), value)

    def switch_vtx_color(self, value=True):
        """Arnold用頂点カラー反映のための関数

        Args:
            value (bool, optional): [description]. Defaults to True.
        """
        for target in self.source_shapes:
            all_color_sets = cmds.polyColorSet(
                target, q=True, allColorSets=True)
            if all_color_sets and all_color_sets[0] != VTX_COLOR_SET_NAME:
                cmds.polyColorSet(
                    target, rename=True, colorSet=all_color_sets[0], newColorSet=VTX_COLOR_SET_NAME)
                cmds.polyColorSet(target, currentColorSet=True,
                                  colorSet=VTX_COLOR_SET_NAME)
            cmds.setAttr("{}.aiExportColors".format(target), value)
            cmds.setAttr("{}.displayColors".format(target), value)

    def arnold_render_textures(self):
        self.target_shapes = list(self.target_nodes.values())
        self.source_shapes = list(self.source_nodes.values())
        self.all_shapes = self.target_shapes + self.source_shapes

        self.switch_occlusion(True)
        self.switch_vtx_color(True)

        shader = ""
        errors = []

        for map_type in self.export_maps:

            shader = self.create_material(map_type)
            for target in list(self.target_nodes.keys()):
                _m = self.arnold_render_texture(target, map_type)
                if _m:
                    errors.append(_m)
            if shader:
                cmds.delete(shader)
                for _ in self.sg_members:
                    cmds.sets(_.members, edit=True, forceElement=_.SG)
        return errors

    def arnold_render_texture(self, target, map_type=""):
        """Arnold設定ローカル版
        各マップの名前による分岐部分
        シャドウと頂点カラーのスイッチをこっちに入れても良いかもしれないが
        全部一緒にやっても良いだろう、ということでグローバルに入れた

        Args:
            target ([type]): [description]
            map_type (str, optional): [description]. Defaults to "".
        """
        errors = ""
        uv_set = ""

        print(
            f"folder = {self.export_path}\n",
            f"shader = \n",
            f"resolution = {self.resolution}\n",
            f"aa_samples = {self.aa_samples}\n",
            f"filter = {self._filter}\n",
            f"filter_width = {self.filter_width}\n",
            f"all_udims = {self.all_udims}\n",
            f"udims = {self.udims}\n",
            f"uv_set = {uv_set}\n",
            f"normal_offset = {self.normal_offset}\n",
            f"enable_aovs = {self.enable_aovs}\n",
            f"extend_edges = {self.extend_edges}\n",
            f"u_start = {self.uStart}\n",
            f"u_scale = {self.uScale}\n",
            f"v_start = {self.vStart}\n",
            f"v_scale = {self.vScale}\n",
            f"sequence = {self.useSequence}\n",
            f"frame_start = {self.frameStart}\n",
            f"frame_end = {self.frameEnd}\n",
            f"frame_step = {self.frameStep}\n",
            f"frame_padding = {self.framePadding}\n",
        )

        cmds.arnoldRenderToTexture(
            folder=self.export_path,
            shader="",
            resolution=self.resolution,
            aa_samples=self.aa_samples,
            filter=self._filter,
            filter_width=self.filter_width,
            all_udims=self.all_udims,
            udims=self.udims,
            uv_set=uv_set,
            normal_offset=self.normal_offset,
            enable_aovs=self.enable_aovs,
            extend_edges=self.extend_edges,
            u_start=self.uStart,
            u_scale=self.uScale,
            v_start=self.vStart,
            v_scale=self.vScale,
            sequence=self.useSequence,
            frame_start=self.frameStart,
            frame_end=self.frameEnd,
            frame_step=self.frameStep,
            frame_padding=self.framePadding
        )

        exr_path = self.create_exr_path(target)

        if map_type:
            new_file_name = "{}_{}".format(self.file_name, map_type)
        else:
            new_file_name = self.file_name

        new_file_name_ext = "{}.exr".format(new_file_name)
        new_file_path = os.path.split(exr_path)[0]
        new_file_path = os.path.join(
            new_file_path, new_file_name_ext).replace(os.sep, '/')

        if os.path.exists(new_file_path):
            try:
                os.remove(new_file_path)
            except Exception as e:
                print(e)
                errors += 'Can Not Remove File {}'.format(new_file_path)

        try:
            os.rename(exr_path, new_file_path)
        except Exception as e:
            print(e)
            errors += 'Can Not Rename FIle [ {} to {} ]'.format(
                exr_path, new_file_path)

        attk = automation_tool_kit.AutomationToolKit(
            new_file_path,
            new_file_name,
            self.export_path,
            self.output_size
        )
        _m = attk.create_sbs()
        if _m:
            errors += "Can Not Create SBS file [ message: {} ]".format(_m)
        _m = attk.create_sbsar()
        if _m:
            errors += "Can Not Create SBSAR file [ message: {} ]".format(_m)
        _m = attk.create_image()
        if _m:
            errors += "Can Not Create Image file [ message: {} ]".format(_m)

        image_magick_exists = os.path.exists(IMAGE_MAGICK_PATH)

        if IMAGE_MAGICK_PATH and image_magick_exists:
            _crop_image_file = os.path.join(self.export_path,
                                            new_file_name).replace(os.sep, '/')

            _hair_preset_path = os.path.join(self.hair_preset_path,
                                             new_file_name).replace(os.sep, '/')

            _command = "{} convert ".format(IMAGE_MAGICK_PATH)
            # 2022でpng を出力すると上下が反転するので、その対応
            _command += "-flip "
            _command += "{}.tga ".format(_crop_image_file)

            if self.crop_uv:
                u_min, u_max, v_min, v_max = get_target_uv_size_u_min_max(
                    target)
                x_min = self.resolution * u_min
                x_max = self.resolution * u_max
                y_min = self.resolution * (1.0 - v_min)
                y_max = self.resolution * (1.0 - v_max)
                x_size = x_max - x_min
                y_size = y_min - y_max
                _command += "-crop "
                _command += f"{x_size:.0f}x{y_size:.0f}+{x_min:.0f}+{y_max:.0f} "

            _command += "{}.png".format(_hair_preset_path)
            print("_command - ", _command)
            subprocess.Popen(_command)
        else:
            errors += "image converter is not exists"
            # cmds.error(u"image converter が見つかりません")

        return errors


class HairMterial(object):
    __slider = None
    __button = None

    def __init__(self, material):
        self.material = material
        self.connections = None
        self.blend_attribute = None
        self.blend_color = None
        self.blend_value = None

        # self._slider = None
        # self._button = None

        self.get_connections()

    def get_connections(self):
        con = cmds.listConnections(
            self.material, s=True, d=False, p=True, c=True)
        if not con:
            return
        self.connections = zip(*[iter(con)]*2)
        for c in con:
            if "blendColor" in c:
                _blend_attr = "{}.{}".format(c.split(".")[0], "blender")
                _blend_color = "{}.{}".format(c.split(".")[0], "color2")
                self.blend_attribute = _blend_attr
                self.blend_color = cmds.getAttr(_blend_color)
                self.blend_value = cmds.getAttr(_blend_attr)

    def __repr__(self):
        return self.material

    @property
    def slider(self):
        return self.__slider

    @slider.setter
    def slider(self, qslider):
        if qslider:
            self.__slider = qslider

    @property
    def button(self):
        return self.__button

    @button.setter
    def button(self, button):
        if button:
            self.__button = button


def delete_unused_materials():
    maya.mel.eval(
        'hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')


def get_hair_materials():
    hair_mats = []
    hair_materials = [x for x in cmds.ls(
        mat=True) if x.startswith(PRESET_TEXTURE_PREFEX)]
    if not hair_materials:
        return
    for mat in hair_materials:
        m = HairMterial(mat)
        hair_mats.append(m)
    return hair_mats


def get_texture_from_tree(fileModel):
    select = fileModel.selectedIndexes()
    if not select:
        _d = gui_util.ConformDialog(title=u"一覧から選択してください",
                                    message=u"マテリアルに適用するテクスチャを選択してから実行してください")
        _d.exec_()
        return False
    return select


def get_file_path_from_tree_selection(path):
    need_maps = ["depth", "alpha"]
    path = os.path.join(path, "ph_*.png")
    png_files = glob.glob(path)

    if not png_files:
        _d = gui_util.ConformDialog(title=u"PNG がない",
                                    message=u"選択されたディレクトリに「 PNG 」ファイルがありません")
        _d.exec_()
        return False

    _flags = []
    need_map_files = OrderedDict()
    for png_file in png_files:
        _, basename = os.path.split(png_file)
        basename, ext = basename.rsplit(".", 1)
        basename_lower = basename.rsplit("_")[-1].lower()
        for _map_type in need_maps:
            need_map_files[basename_lower] = png_file
            if basename_lower.endswith(_map_type):
                _flags.append(_map_type)

    _not_in_flag = set(need_maps) - set(_flags)
    if _not_in_flag:
        _not_in_flag = list(_not_in_flag)
        _m = u"選択されたディレクトリに[ {} ]ファイルがありません".format(", ".join(_not_in_flag))
        _d = gui_util.ConformDialog(title=u"PNG がない",
                                    message=_m)
        _d.exec_()
        return False

    return need_map_files


def get_shapes():
    selections = cmds.ls(sl=True)
    shapes = cmds.listRelatives(selections,
                                allDescendents=True,
                                fullPath=True,
                                type="mesh")
    return shapes


def get_current_face_selections():
    selection = cmds.ls(sl=True)
    _face = cmds.polyListComponentConversion(selection, toFace=True)
    _face = cmds.filterExpand(_face, selectionMask=34, expand=True)

    if not _face:
        _m = u"マテリアルをアサインする対象が選ばれておりません\n"
        _m += u"マテリアルアサインをせずにマテリアルを生成しますか？"
        _d = gui_util.ConformDialogResult(title=u"マテリアル生成",
                                          message=_m)
        result = _d.exec_()
        if not result:
            return False
    return _face


def get_scene_materials():
    mats_obj = []
    mats = [x for x in cmds.ls(
        mat=True) if x.startswith(PRESET_TEXTURE_PREFEX)]

    if not mats:
        return mats_obj

    for m in mats:
        _m = HairMterial(m)
        mats_obj.append(_m)

    return mats_obj


def create_blend_color_utility(file_node, shader, color=[0, 0, 0], blend_switch_flag=False):
    utility = cmds.shadingNode("blendColors", asUtility=True, skipSelect=True)
    cmds.connectAttr('{}.outColor'.format(file_node),
                     '{}.color1'.format(utility))
    cmds.connectAttr('{}.output'.format(utility), '{}.color'.format(shader))
    cmds.setAttr("{}.color2".format(utility),
                 color[0], color[1], color[2],
                 type="double3")

    if blend_switch_flag:
        cmds.setAttr("{}.blender".format(utility), 1.0)
    else:
        cmds.setAttr("{}.blender".format(utility), 0.0)


def create_reverse_utility(alpha_path, shader, no_suffix=False):
    path, basename = os.path.split(alpha_path)
    file_name, ext = os.path.splitext(basename)
    if no_suffix:
        suffix = ""
        texture_name = file_name
    else:
        suffix = file_name.rsplit("_", 1)
        texture_name, suffix = suffix
    ext = ext[1:]

    file_node_name = "{}_{}".format(file_name, ext)
    file_node = cmds.ls(file_node_name, type="file")
    if not file_node:
        file_node = cmds.shadingNode(
            "file", asTexture=True, name=file_node_name, skipSelect=True)
        cmds.setAttr('{}.fileTextureName'.format(file_node),
                     alpha_path.replace(os.sep, '/'), type='string')
    else:
        file_node = file_node[0]

    utility = cmds.shadingNode("reverse", asUtility=True, skipSelect=True)
    cmds.connectAttr('{}.outColor'.format(
        file_node), '{}.input'.format(utility))
    cmds.connectAttr('{}.output'.format(utility),
                     '{}.transparency'.format(shader))


def create_new_material(file_path="",
                        alpha_path="",
                        assign_faces=[],
                        color=[0, 0, 0],
                        blend_switch_flag=False,
                        no_suffix=False):

    path, basename = os.path.split(file_path)
    file_name, ext = os.path.splitext(basename)
    if no_suffix:
        suffix = ""
        texture_name = file_name
        shader_name = "{}_{}".format(texture_name, "mtl")
    else:
        suffix = file_name.rsplit("_", 1)
        texture_name, suffix = suffix
        shader_name = "{}_{}_{}".format(texture_name, suffix, "mtl")
    ext = ext[1:]

    shading_engine_name = "{}{}".format(shader_name, "SG")
    file_node_name = "{}_{}".format(file_name, ext)

    file_node = cmds.ls(file_node_name, type="file")
    if file_node:
        file_node = file_node[0]
    else:
        file_node = cmds.shadingNode(
            "file", asTexture=True, name=file_node_name, skipSelect=True)
        cmds.setAttr('{}.fileTextureName'.format(file_node),
                     file_path.replace(os.sep, '/'), type='string')

    shader = cmds.ls(shader_name, mat=True)
    if not shader:
        shader = cmds.shadingNode(
            "blinn", asShader=True, name=shader_name, skipSelect=True)
    else:
        shader = shader[0]
    cmds.setAttr("{}.specularColor".format(shader), 0, 0, 0, type="double3")
    shading_engine = cmds.ls(shading_engine_name, type="shadingEngine")
    if shading_engine:
        sg = shading_engine[0]
    else:
        sg = cmds.sets(n=shading_engine_name, renderable=True,
                       noSurfaceShader=True, empty=True)
        cmds.connectAttr('{}.outColor'.format(shader),
                         '{}.surfaceShader'.format(sg))
        create_blend_color_utility(file_node, shader, color, blend_switch_flag)
        create_reverse_utility(alpha_path, shader, no_suffix)

    if assign_faces:
        cmds.sets(assign_faces, edit=True, forceElement=sg)


def select_material(material):
    if cmds.objExists(material):
        cmds.select(material, r=True)


def select_material_face(material):
    flag = False
    if cmds.objExists(material):
        cmds.select(material, r=True)
        sg = cmds.listConnections(
            material, s=False, d=True, type='shadingEngine')
        members = cmds.ls(cmds.sets(sg, q=True), fl=True)
        if members:
            flag = members

    if flag:
        cmds.select(flag, r=True)
    else:
        cmds.select(cl=True)


def all_poly_unite(_guides: list) -> None:
    """ヘアガイドシェイプをマテリアルごとにコンバイン

    :param _guides: ヘアガイド
    :return: None

    """
    if not _guides:
        return

    node_name = "{}_combine_mesh".format(NAME)

    _pre_duplicate_nodes = []
    for _guide, sym_history in _guides.items():
        if sym_history:
            _guide_dup = cmds.duplicate(
                _guide, returnRootsOnly=True, fullPath=True)[0]
            _meshes = cmds.listRelatives(
                _guide_dup, allDescendents=True, fullPath=True, type="mesh")
            _meshes = [x for x in _meshes if not cmds.getAttr(
                "{}.intermediateObject".format(x))]
            sym = [x for x in cmds.listHistory(_meshes)
                   if cmds.nodeType(x) == "SymmetryNode"]
            if sym:
                cmds.setAttr(sym[0] + ".nodeState", 0)
            cmds.polyMirrorFace(_guide,
                                cutMesh=False,
                                axis=0,
                                axisDirection=1,
                                direction=0,
                                mergeMode=3,
                                mergeThresholdType=0,
                                mergeThreshold=0.001,
                                mirrorAxis=2,
                                mirrorPosition=0,
                                smoothingAngle=30,
                                flipUVs=1,
                                ch=True)
            cmds.delete(_guide)
            _guide = cmds.rename(_guide_dup.split(
                "|")[-1], _guide.split("|")[-1])
        _pre_duplicate_nodes.append(_guide)

    _duplicate_nodes = cmds.duplicate(
        _pre_duplicate_nodes, returnRootsOnly=True, fullPath=True)

    if len(_guides) > 1:
        _comb = cmds.polyUnite(_duplicate_nodes, muv=1, cp=True, ch=False,
                               name=node_name)
        try:
            cmds.delete(_duplicate_nodes)
        except Exception as e:
            print(e)
    else:
        cmds.rename(_duplicate_nodes, node_name)


def get_type_nodes(root_node: list) -> OrderedDict:
    """Ornatrix のガイドを検出する
    シンメトリのヒストリを値とする
    guideNode: symmetry history

    Args:
        root_node (list): maya mesh nodes

    Returns:
        OrderedDict: [guideNode: symmetry history]
    """
    _target_nodes = OrderedDict()

    for _node in root_node:
        _mesh_shapes = cmds.listRelatives(_node,
                                          allDescendents=True,
                                          fullPath=True,
                                          type="mesh")
        try:
            _guides = cmds.listRelatives(_node,
                                         allDescendents=True,
                                         fullPath=True,
                                         type="EditGuidesShape")
        except Exception as e:
            print(e)
            _guides = []

        if not _guides:
            _guides = _mesh_shapes
        if not _guides:
            continue

        for _guide in _mesh_shapes:
            _parent = cmds.listRelatives(_guide, parent=True, fullPath=True)
            sym_history = [x for x in cmds.listHistory(_guide, allFuture=True)
                           if cmds.nodeType(x) == "SymmetryNode"]

            if _parent[0] in _target_nodes:
                continue

            if sym_history:
                _target_nodes[_parent[0]] = sym_history[0]
            else:
                _target_nodes[_parent[0]] = False

    return _target_nodes


def get_hair_gides():
    _m = u""
    selections = cmds.ls(sl=True, long=True, type="transform")
    if not selections:
        _m = u"選択してから実行してください"

    guides = get_type_nodes(selections)
    if not guides:
        _m = u"選択ノード以下にメッシュがありませんでした"

    # if len(guides) > 1:
    #     _m = u""

    if _m:
        _d = gui_util.ConformDialog(title=TITLE, message=_m)
        _d.exec_()
        return
    else:
        all_poly_unite(guides)


def get_reduction_hda():
    hda_path = os.path.split(HDA_PATH)[0]
    hda_path = os.path.join(hda_path, REMOVE_HDA_NAME +
                            ".hda").replace(os.sep, '/')
    _asset_name = cmds.houdiniAsset(listAssets=hda_path)
    hda_asset_name = _asset_name[0]
    return _asset_name


def get_hda():
    hda_path = os.path.join(HDA_PATH, HDA_NAME + ".hda").replace(os.sep, '/')
    _asset_name = cmds.houdiniAsset(listAssets=hda_path)
    if _asset_name:
        return _asset_name[0]
    else:
        return
    # hda_asset_name = _asset_name[0]
    # return _asset_name


def get_remove_hda_nodes():
    _hdas = []

    selections = cmds.ls(sl=True, type="transform", l=True)
    if not selections:
        return
    for selection in selections:
        short_name = selection.rsplit("|")[-1]
        if(cmds.nodeType(selection) == "houdiniAsset"
                and short_name.startswith(REMOVE_HDA_NAME)):
            _hdas.append(selection)

    if _hdas:
        return _hdas[0]
    else:
        return


def get_hda_nodes():
    _hdas = []

    selections = cmds.ls(sl=True, type="transform", l=True)
    if not selections:
        return
    for selection in selections:
        short_name = selection.rsplit("|")[-1]
        if(cmds.nodeType(selection) == "houdiniAsset"
                and short_name.startswith(HDA_NAME)):
            _hdas.append(selection)

    if _hdas:
        return _hdas[0]
    else:
        return


def apply_redction_hda():

    selections = cmds.ls(sl=True, type="transform", l=True)
    if not selections:
        return u"トランスフォームノードを選択して実行してください"
    # nodes = cmds.listRelatives(selections, allDescendents=True, fullPath=True)

    # flag = False
    # for node in nodes:
    #     if cmds.nodeType(node) == "houdiniAsset":
    #         flag = True
    # if flag:
    #     return u"選択の階層に houdiniAsset があります\n処理ができません"

    # shape_node = cmds.listRelatives(selections, c=True, fullPath=True, type="mesh")
    shape_node = cmds.listRelatives(
        selections, allDescendents=True, fullPath=True, type="mesh")
    if not shape_node:
        return u"メッシュを持つトランスフォームノードを選択してから実行してください"
    shape_node = shape_node[0]

    _z_drive_check = set_active_z_drive_plugin()
    if not _z_drive_check:
        return u"Z ドライブのプラグインを読み込めませんでした"

    _asset_name = get_reduction_hda()
    if not _asset_name:
        return u"HDA の読み込みに失敗しました"

    _asset_name = _asset_name[0]

    hda_path = os.path.split(HDA_PATH)[0]
    hda_path = os.path.join(hda_path, REMOVE_HDA_NAME +
                            ".hda").replace(os.sep, '/')
    _hda = cmds.houdiniAsset(loadAsset=[hda_path, _asset_name])

    mel_string = '{{ {} }}'.format('"{}"'.format(shape_node))

    maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(
        _hda + ".input[0].inputNodeId", mel_string))

    if _hda:
        cmds.select(_hda, r=True)
    else:
        return u"HDA を適用できませんでした"
    return


def apply_hda() -> str:
    """HoudiniDigtalAsset 適用

    Returns:
        str: [description]
    """

    _hdas = []
    node_name = "{}_combine_mesh".format(NAME)
    selections = cmds.ls(sl=True, long=True, type="transform")
    if not selections:
        return u"[ {} ]\nの名前で始まるノードを選択してから実行してください".format(node_name)

    _houdiniengine_flag = houdini_util.main()
    if not _houdiniengine_flag:
        return ""

    _asset_name = get_hda()
    if not _asset_name:
        return u"HDA の読み込みに失敗しました"

    for selection in selections:
        selection_short_name = selection.split("|")[-1]

        if selection_short_name.startswith(node_name):
            _hda = cmds.houdiniAsset(loadAsset=[HDA_PATH, _asset_name])
            shape_node = cmds.listRelatives(
                selection, allDescendents=True, fullPath=True, type="mesh")
            if not shape_node:
                continue
            mel_string = '{{ {} }}'.format('"{}"'.format(shape_node[0]))
            _hdas.append(_hda)

            maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(
                _hda + ".input[0].inputNodeId", mel_string))

    if _hdas:
        cmds.select(_hdas, r=True)
    else:
        return u"[ {} ]\nの名前で始まるノードを選択してから実行してください".format(node_name)
    return ""


def create_plane(source_name="", num=0, bb=om2.MBoundingBox()):
    """API2.0 でのプレーンメッシュ作成

    Args:
        source_name (str): [description]. Defaults to "".
        num (int): [description]. Defaults to 0.
        bb ([type]): [description]. Defaults to om2.MBoundingBox().

    Returns:
        [str, str]: transform node name, mesh shape node name
    """

    bb_center = bb.center
    bb_width = bb.width
    bb_heigit = bb.height
    bb_depth = bb.depth

    if bb.width > bb.depth:
        _p1 = om2.MPoint(bb_center.x-bb_width/2, bb.min.y, bb_center.z)
        _p2 = om2.MPoint(bb_center.x+bb_width/2, bb.min.y, bb_center.z)
        _p3 = om2.MPoint(bb_center.x-bb_width/2, bb.max.y, bb_center.z)
        _p4 = om2.MPoint(bb_center.x+bb_width/2, bb.max.y, bb_center.z)
    else:
        _p1 = om2.MPoint(bb_center.x-bb_depth/2, bb.min.y, bb_center.z)
        _p2 = om2.MPoint(bb_center.x+bb_depth/2, bb.min.y, bb_center.z)
        _p3 = om2.MPoint(bb_center.x-bb_depth/2, bb.max.y, bb_center.z)
        _p4 = om2.MPoint(bb_center.x+bb_depth/2, bb.max.y, bb_center.z)

    points = [_p1, _p2, _p3, _p4]

    vtxs = [0, 1, 3, 2]
    u_values = om2.MFloatArray([0.0, 1.0, 0.0, 1.0])
    v_values = om2.MFloatArray([0.0, 0.0, 1.0, 1.0])

    vertexArray = om2.MPointArray(points)
    polygonCounts = om2.MIntArray([4])

    polygonConnects = om2.MIntArray(vtxs)

    if not source_name:
        node_name = "{}_{}".format(HAIR_CARD_NAME, num)
    else:
        node_name = "{}_{}_{}".format(source_name, HAIR_CARD_NAME, num)

    dagModifier = om2.MDagModifier()
    meshTransformObj = dagModifier.createNode('transform')
    meshFn = om2.MFnMesh()

    meshShapeObj = meshFn.create(vertexArray,
                                 polygonCounts,
                                 polygonConnects,
                                 parent=meshTransformObj)

    meshFn.setUVs(u_values, v_values)
    meshFn.assignUVs(polygonCounts, polygonConnects)

    meshFn.setName('{}Shape'.format(node_name))

    dagshapeNodeFn = om2.MFnDagNode(meshShapeObj)
    meshShapeDagPath = dagshapeNodeFn.getPath()

    transformFn = om2.MFnTransform(meshTransformObj)
    dagtransformNodeFn = om2.MFnDagNode(meshTransformObj)
    meshTransformDagPath = dagtransformNodeFn.getPath()

    transformFn.setRotatePivot(bb.center, om2.MSpace.kTransform, False)
    transformFn.setScalePivot(bb.center, om2.MSpace.kTransform, False)
    # transformFn.setTranslation(om2.MVector(0, 2, 0), om2.MSpace.kTransform)

    transformFn.setName(node_name)

    # これがないと処理が行われないので注意
    dagModifier.doIt()

    return meshTransformDagPath.fullPathName(), meshShapeDagPath.fullPathName()


def create_plane_meshes(source_name="", bb_size=[], _count=1, scale_value=1.05) -> list:
    """プレーンメッシュの作成

    Args:
        source_name (str): [description]. Defaults to "".
        bb_size (list): [description]. Defaults to [].
        _count (int): [description]. Defaults to 1.
        scale_value (float): [description]. Defaults to 1.05.

    Returns:
        list: [description]
    """

    _exists_flag = False
    _exists_nodes = []

    for i in range(_count):
        _bill_bord_name = "{}_{}_{}".format(source_name, HAIR_CARD_NAME, i)
        if cmds.objExists(_bill_bord_name):
            _exists_flag = True
            _exists_nodes.append(_bill_bord_name)

    if _exists_flag:
        # cmds.select(_exists_nodes, r=True)
        _m = u"[ {} ] ノードはすでにシーンに存在してます　削除してから再度実行してください".format(
            ", ".join(_exists_nodes))
        cmds.warning(_m)
        return []

    point1 = om2.MPoint(bb_size[0][0], bb_size[1][0], bb_size[2][0])
    point2 = om2.MPoint(bb_size[0][1], bb_size[1][1], bb_size[2][1])

    bb = om2.MBoundingBox()
    bb.expand(point1)
    bb.expand(point2)

    _mul = scale_value
    _planes = []
    _plane_transform = []

    for i in range(_count):
        _plane, _plane_shape = create_plane(source_name, i, bb)
        # cmds.select(_plane)

        cmds.sets(_plane_shape, e=True, forceElement=SHADING_NODE_NAME)

        cmds.setAttr("{}.receiveShadows".format(_plane_shape), 0)
        cmds.setAttr("{}.castsShadows".format(_plane_shape), 0)
        cmds.setAttr("{}.s".format(_plane), _mul, _mul, _mul)
        cmds.setAttr("{}.tz".format(_plane), -(bb.depth / 2))

        if i == 1:
            cmds.setAttr("{}.r".format(_plane), 0, 90, 0)
        elif i == 2:
            cmds.setAttr("{}.r".format(_plane), 0, 45, 0)
        elif i == 3:
            cmds.setAttr("{}.r".format(_plane), 0, -45, 0)

        cmds.u3dOptimize(_plane, ite=5, pow=1, sa=1,
                         bi=1, tf=1, ms=1024, rs=10)
        cmds.u3dLayout(_plane, res=256, rot=4, scl=3, box=[0, 1, 0, 1])

        _planes.append(_plane_shape)
        _plane_transform.append(_plane)

    return _planes


def create_billbord(scale_value=1.05):
    """ヘアカード用のプレーンメッシュ作成

    Args:
        scale_value (float): ヘアジオメトリよりもちょっと大きいサイズ
        デフォルトは「1.05」にしている
    """
    _m = u""
    _planes = []
    selections = cmds.ls(sl=True, type="transform", l=True)
    if not selections:
        return

    for selection in selections:
        _flag = False
        for parent in get_parents(selection):
            if parent in selections:
                _flag = True
                break
        if _flag:
            continue

        _cld = cmds.listRelatives(
            selection, allDescendents=True, fullPath=True, type="mesh")
        bb_size = cmds.polyEvaluate(
            _cld, boundingBox=True, accurateEvaluation=True)
        if isinstance(bb_size, tuple):
            if len(selections) == 1:
                _plane = create_plane_meshes(
                    selections[0], bb_size, 1, scale_value)
            else:
                _plane = create_plane_meshes("", bb_size, 1, scale_value)
            _planes.append(_plane[0])
        else:
            _m += u"[ {} ]\n".format(selection)

    if _m:
        _m += u"\n選択ジオメトリが適切ではありません"
        _d = gui_util.ConformDialog(title=TITLE, message=_m)
        _d.exec_()

    if _planes:
        cmds.select(_planes, r=True)


def change_uv_link(mesh):
    """UV リンクの切り替え

    Args:
        mesh ([type]): [description]
    """
    mesh_shape = cmds.listRelatives(
        mesh, allDescendents=True, fullPath=True, type="mesh")
    if mesh_shape:
        for _link in cmds.uvLink(q=True, uvSet="{}.uvSet[0].uvSetName".format(mesh_shape[0])):
            if _link:
                cmds.uvLink(make=True, uvSet="{}.uvSet[1].uvSetName".format(
                    mesh_shape[0]), texture=_link)
                cmds.uvLink(uvSet="{}.uvSet[1].uvSetName".format(
                    mesh_shape[0]), texture=_link)


def get_inputs(mesh) -> OrderedDict:
    """ mesh からマテリアルとそれにつながるインプット、アウトプットを取得

    Args:
        mesh (str, mesh_shape): [description]

    Returns:
        [dict]: mtl_hair_G3 :
                [(u'mtl_hair_G3.color', u'ramp1.outColor'),
                (u'mtl_hair_G3.transparency', u'reverse15.output')]
    """

    if not mesh:
        return

    mesh_shape = cmds.listRelatives(
        mesh, allDescendents=True, fullPath=True, type="mesh")

    if not mesh_shape:
        return

    sg = cmds.listConnections(mesh_shape, s=False, d=True, t='shadingEngine')
    mats = cmds.ls(cmds.listConnections(sg, s=True, d=False), mat=True)

    mat_inputs = OrderedDict()
    for mat in mats:
        con = cmds.listConnections(mat, s=True, d=False, p=True, c=True)
        if con:
            mat_inputs[mat] = zip(*[iter(con)]*2)

    return mat_inputs


def delete_same_name_mesh(node: str, suffix: str) -> str:
    """すでに同名のノードがあれば削除する

    Args:
        node ([type]): [description]
        suffix ([type]): [description]

    Returns:
        [type]: [description]
    """
    new_name = "{}_{}".format(node, suffix)
    for root in cmds.ls(assemblies=True):
        if len(root.split(new_name)) == 2:
            cmds.delete(root)
    return new_name


def duplicate_meshes(meshes: list, use_type="bake", meshes_select_ids=None) -> None:
    """source bake final のメッシュを抽出する

    Args:
        meshes (list): [description]
        use_type (str, optional): [description]. Defaults to "bake".
        meshes_select_ids ([type], optional): [description]. Defaults to None.
    """
    dup_objs = cmds.duplicate(meshes, returnRootsOnly=True)

    for dup_obj in dup_objs:
        dup_obj_long_name = cmds.ls(dup_obj, long=True)[0]
        dup_base_name = dup_obj_long_name.rsplit("_", 1)[0]
        root = dup_obj_long_name.split("|")[1]
        del_ids = []
        all_face_ids = [x.rsplit("[", 1)[-1].rsplit("]")[0] for x in cmds.ls("{}.f[*]".format(
            dup_obj_long_name), fl=True)]

        for src_mesh, _ids in meshes_select_ids.items():
            src_base_name = src_mesh.rsplit("_", 1)[0]
            if dup_base_name == src_base_name:
                if use_type == "bake" or use_type == "source":
                    del_ids = [x for x in all_face_ids if x not in _ids]
                elif use_type == "final":
                    del_ids = _ids

        if del_ids:
            if use_type == "bake" or use_type == "source":
                for x in _ids:
                    face_id = "{}.f[{}]".format(
                        dup_obj_long_name.rsplit("|")[-1], x)
                    cmds.sets(face_id, remove=ONE_CARD)
            del_faces = ["{}.f[{}]".format(
                dup_obj_long_name, x) for x in del_ids]
            cmds.delete(del_faces)

        if use_type != "final":
            cmds.hide(dup_obj_long_name)

        if use_type == "bake":
            new_name = delete_same_name_mesh(root, BAKE_TARGET_NAME)
        elif use_type == "final":
            new_name = delete_same_name_mesh(root, FINAL_NAME)
        elif use_type == "source":
            new_name = delete_same_name_mesh(root, BAKE_SOURCE_NAME)
            change_uv_link(dup_obj_long_name)

        cmds.rename(dup_obj, new_name)
        cmds.parent(new_name, world=True)


def extract_face(faces: list) -> None:
    """フェイスを抽出

    Args:
        faces (list): [description]
    """
    " Need Flatten face id list"

    meshes = []
    meshes_select_ids = dict()

    for face in faces:
        mesh = face.rsplit(".", 1)[0]
        face_id = face.rsplit("[", 1)[-1].rsplit("]")[0]
        if mesh not in meshes:
            meshes.append(mesh)
            meshes_select_ids[mesh] = [face_id]
        else:
            meshes_select_ids[mesh] = meshes_select_ids[mesh] + [face_id]

    if not meshes:
        return

    for _type in ["bake", "source", "final"]:
        duplicate_meshes(meshes, _type, meshes_select_ids)


def get_sets_faces(transform_node: str) -> list:
    """sets にあるフェースの情報を取得

    Args:
        transform_node (str): [description]

    Returns:
        list: face list
    """

    faces = []

    for face in cmds.ls(cmds.sets(ONE_CARD, q=True), fl=True, l=True):
        split_name = face.split("|")
        if len(split_name) > 2 and split_name[1] == transform_node:
            faces.append(face)

    return faces


def get_need_datas(transform_nodes: list) -> list:
    """surfaceSampler に必要なデータの準備
    ソースとターゲットの抽出

    Args:
        transform_nodes (list): maya dag nodes

    Returns:
        list: [description]
    """
    if not cmds.objExists(ONE_CARD) or not cmds.objExists(ALL_CARD):
        return []

    targets_sources = []
    root_nodes = cmds.ls(assemblies=True, l=True)

    for transform_node in transform_nodes:
        if transform_node in root_nodes:
            if "|" in transform_node:
                transform_node = transform_node[1:]

            target_name = "{}_{}".format(transform_node, BAKE_TARGET_NAME)
            source_name = "{}_{}".format(transform_node, BAKE_SOURCE_NAME)
            final_name = "{}_{}".format(transform_node, FINAL_NAME)
            # had_need_data[transform_node] = [target_name, source_name, final_name]
            target_flag = False
            source_flag = False
            final_flag = False

            for root in root_nodes:
                if root.startswith(target_name):
                    target_flag = True
                if root.startswith(source_name):
                    source_flag = True
                if root.startswith(final_name):
                    final_flag = True
            if not target_flag or not source_flag or not final_flag:
                face_data = get_sets_faces(transform_node)
                extract_face(face_data)

            if cmds.objExists(target_name) and cmds.objExists(source_name):
                targets_sources.append([target_name, source_name])

    return targets_sources


@speed_check
def surface_sampler(
        source="",
        target="",
        path="",
        file_ext="tga",
        sampling="1",
        resolution="1024",
        filter_type=0,
        filter_size=1.0) -> bool:
    """surfaceSampler

    Args:
        source (str): source mesh
        target (str): target mesh
        path (str): export file path 拡張子なしのファイル名まで
        file_ext (str): 拡張子
        sampling (str): [description]. Defaults to "1".
        resolution (str): [description]. Defaults to "1024".
        filter_type (int): [description]. Defaults to 0.
        filter_size (float): [description]. Defaults to 1.0.

    Returns:
        [bool]:
    """
    _cancel_flag = True

    cmds.surfaceSampler(
        target=target,
        uvSet="map1",
        searchOffset=0,
        # maxSearschDistance=0,
        searchCage="",
        source=source,
        mapOutput="diffuseRGB",
        # mapOutput="litAndShadedRGB",
        # mapOutput="alpha",
        mapWidth=int(resolution),
        mapHeight=int(resolution),
        maximumValue=0,
        mapSpace="object",
        ignoreTransforms=False,
        mapMaterials=False,
        shadows=False,
        filename=path,
        fileFormat=file_ext,
        superSampling=int(sampling),
        filterType=filter_type,
        filterSize=filter_size,
        overscan=100,
        searchMethod=0,
        useGeometryNormals=False,
        ignoreMirroredFaces=False,
        flipU=False, flipV=False
    )

    return _cancel_flag


def get_material_textures(source=[]) -> OrderedDict:
    """入力されたノード以下のメッシュノードにあるマテリアルを取得し
    「depth」の文字列があるファイルノードを抽出している

    Args:
        source (list): maya dag nodes

    Returns:
        [OrderedDict]: materialNode: fileNode
    """
    material_texture = OrderedDict()

    mesh_shape = cmds.listRelatives(
        source, allDescendents=True, fullPath=True, type="mesh")

    if not mesh_shape:
        return material_texture

    sg = cmds.listConnections(mesh_shape, s=False,
                              d=True, t='shadingEngine')

    if not sg:
        return material_texture

    mats = cmds.ls(cmds.listConnections(sg, s=True, d=False), mat=True)

    for m in mats:
        file_nodes = cmds.ls(cmds.listHistory(m), type="file")
        for _file in file_nodes:
            if "depth" in _file:
                #     continue
                # _file_path = cmds.getAttr(_file + ".ftn")
                # if _file_path.startswith(PRESET_TEXTURE_PREFEX):
                #     path, basename = os.path.split(_file_path)
                #     file_name = _file.rsplit("_", 2)[0]
                #     file_name = file_name + ".png"
                #     path = os.path.join(path, file_name)
                material_texture[m] = _file

    return material_texture


def import_texture_file(map_type="", file_node=None):
    base_file_path = cmds.getAttr(file_node + ".ftn")
    _file_path, basename = os.path.split(base_file_path)
    _file_name = file_node.rsplit("_", 2)[0]
    _file_name = "{}_{}.png".format(_file_name, map_type)
    _file_path = os.path.join(_file_path, _file_name).replace(os.sep, '/')
    _file_node_name = "{}_{}_png".format(_file_name, map_type)

    if not os.path.exists(_file_path):
        return
    map_type_file_node = cmds.shadingNode(
        "file", asTexture=True, name=_file_node_name, skipSelect=True)
    cmds.setAttr('{}.fileTextureName'.format(
        map_type_file_node), _file_path, type='string')
    return map_type_file_node


def transfar_map(
        source="",
        target="",
        path="",
        file_name="",
        file_ext="tga",
        sampling="1",
        resolution="1024",
        filter_type=0,
        filter_size=1.0,
        export_maps=[],
        irda_map_flag=True,):

    suffix = "irda"
    mat_inputs = get_inputs(source)

    if not mat_inputs:
        return

    material_textures = get_material_textures(source)

    if not material_textures:
        return

    if file_name:
        pack_file_name = "{}_{}".format(file_name, suffix)
    else:
        pack_file_name = suffix

    pack_export_path = os.path.join(path, pack_file_name).replace(os.sep, '/')

    # パックテクスチャ確認用
    _error = []

    # AutomationToolKit 確認用
    errors = ""

    export_paths = OrderedDict()
    for i, map_type in enumerate(export_maps):
        for material, file_node in material_textures.items():

            base_file_path = cmds.getAttr(file_node + ".ftn")
            _file_path, basename = os.path.split(base_file_path)
            _file_name = file_node.rsplit("_", 2)[0]
            _file_name = "{}_{}.png".format(_file_name, map_type)
            _file_path = os.path.join(_file_path, _file_name)

            if not os.path.exists(_file_path):
                continue
            cmds.setAttr(file_node + ".ftn", _file_path, type="string")
            cmds.connectAttr('{}.{}'.format(file_node, "outColor"),
                             '{}.{}'.format(material, "color"), force=True)
        if file_name:
            export_path = os.path.join(path, "{}_{}".format(
                file_name, map_type)).replace(os.sep, '/')
        else:
            export_path = os.path.join(
                path, "{}".format(map_type)).replace(os.sep, '/')

        surface_sampler(
            source=source,
            target=target,
            path=export_path,
            file_ext=file_ext,
            sampling=sampling,
            resolution=resolution,
            filter_type=filter_type,
            filter_size=filter_size
        )

        png_path = export_path + "." + file_ext

        if os.path.exists(png_path):
            export_paths[map_type] = png_path
            cmds.setAttr(file_node + ".ftn", base_file_path, type="string")

    for mat, connections in mat_inputs.items():
        for input_output in connections:
            _in = input_output[0]
            _out = input_output[-1]
            cmds.connectAttr('{}'.format(_out),
                             '{}'.format(_in), force=True)

    _packing_tex = ""
    if export_paths and irda_map_flag:
        _id = export_paths.get("vcolor", None)
        _root = export_paths.get("root", None)
        _depth = export_paths.get("depth", None)
        _alpha = export_paths.get("alpha", None)
        if not _id:
            _error.append(u"[ {} マップ ]".format("ID"))
        if not _root:
            _error.append(u"[ {} マップ ]".format("Root"))
        if not _depth:
            _error.append(u"[ {} マップ ]".format("Depth"))
        if not _alpha:
            _error.append(u"[ {} マップ ]".format("Alpha"))
        if not _error:
            _image_magick = image_magick(IMAGE_MAGICK_PATH)
            if _image_magick:
                _command = _image_magick
                _command += "{} ".format(_id)
                _command += "{} ".format(_root)
                _command += "{} ".format(_depth)
                _command += "{} ".format(_alpha)
                _command += "-channel RGBA -combine "
                _packing_tex = "{}.tga".format(pack_export_path)
                _command += _packing_tex

                subprocess.Popen(_command)

                _message = u"{}\n\n".format(
                    u"\n".join(list(export_paths.values())))
                _message += u"{}\n\n".format(_packing_tex)

                _message += u"を出力しました"
                _d = gui_util.ConformDialog(title=TITLE, message=_message)
                _d.exec_()

    if _error:
        _m = u"{}\n\n{}".format(u"\n".join(
            _error), u"がなかったので、パッキングテクスチャを出力できませんでした")
        _d = gui_util.ConformDialog(title=TITLE, message=_m)
        _d.exec_()

    if errors:
        _m = errors
        _d = gui_util.ConformDialog(title=TITLE, message=_m)
        _d.exec_()


def check_data(path="", export_maps=[], hdas=[]):
    _m = ""

    if not export_maps:
        _m = "最低一つのマップのチェックを入れてください"

    if not _m:
        if not path:
            _m = "[ アトラステクスチャ出力先 ]\n\nに出力先を入力してください"
        else:
            if not os.path.exists(path):
                _m = "[ アトラステクスチャ出力先 ] に入力されたパス\n\n[ {} ]\n\nが存在しません".format(
                    path)

        if not _m and not hdas:
            _m = "[ {} ] の名前で始まる\n\nHoudiniDigitalAssets\n\nを選択してください".format(
                HDA_NAME)

    if _m:
        _d = gui_util.ConformDialog(title=TITLE, message=_m)
        _d.exec_()
        return

    return True


def create_atlus_texture(path="",
                         file_name="",
                         resolution="2048",
                         quality="Preview",
                         filter_type=0,
                         filter_size=1.0,
                         file_format="tga",
                         export_maps=[],
                         irda_map_flag=True,
                         create_material=False):

    _hdas = []
    _final_meshes = []

    selections = cmds.ls(sl=True, type="transform", l=True)

    for selection in selections:
        # ロングネーム用の[1:]を入れているので注意
        if cmds.nodeType(selection) == "houdiniAsset" and selection[1:].startswith(HDA_NAME):
            if cmds.attributeQuery("houdiniAssetParm_view_cage", node=selection, ex=True):
                cmds.setAttr(selection + ".houdiniAssetParm_view_cage", 0)
            _hdas.append(selection)

    if not check_data(path, export_maps, _hdas):
        return

    targets_sources = get_need_datas(_hdas)
    if not targets_sources:
        return

    for transform_node, target_source in zip(_hdas, targets_sources):
        if "|" in transform_node:
            transform_node = transform_node[1:]

        transfar_map(
            target=target_source[0],
            source=target_source[1],
            path=path,
            file_name=file_name,
            file_ext=file_format,
            sampling=MAP_SAMPLING_LIST.index(quality),
            resolution=resolution,
            filter_type=filter_type,
            filter_size=filter_size,
            export_maps=export_maps,
            irda_map_flag=irda_map_flag)

        _final_mesh_name = "{}_{}".format(transform_node, FINAL_NAME)
        if cmds.objExists(_final_mesh_name):
            _final_meshes.append(_final_mesh_name)

    if _final_meshes:
        cmds.select(_final_meshes, r=True)
        if create_material:
            if file_name:
                _depth_file_name = "{}_{}.tga".format(file_name, "depth")
                _alpha_file_name = "{}_{}.tga".format(file_name, "alpha")
            else:
                _depth_file_name = "{}.tga".format("depth")
                _alpha_file_name = "{}.tga".format("alpha")
            _depth_path = os.path.join(path, _depth_file_name)
            _alpha_path = os.path.join(path, _alpha_file_name)
            if os.path.exists(_depth_path) and os.path.exists(_alpha_path):
                create_new_material(
                    _depth_path,
                    _alpha_path,
                    _final_meshes,
                    [1, 1, 1],
                    blend_switch_flag=True,
                    no_suffix=True
                )
    else:
        cmds.select(_hdas, r=True)


def bake_asset(_hda):
    maya.mel.eval('houdiniEngine_bakeAsset {};'.format(_hda))


def _bake_asset():
    selections = cmds.ls(sl=True, type="houdiniAsset", l=True)
    if not selections:
        return

    for selection in selections:
        short_name = selection.rsplit("|")[-1]
        if short_name.startswith(REMOVE_HDA_NAME):
            bake_asset(selection)
