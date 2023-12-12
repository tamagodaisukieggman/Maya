# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from functools import wraps
import time

import os
import sys
import subprocess
import random

try:
    from pysbs import context, batchtools
except:pass

import maya.api.OpenMaya as om2
import maya.cmds as cmds

from . import RESOLUTIONS_DICT
from . import AUTOMATION_TOOL_KIT
from . import PYSBS
# from . import DEV_MODE



MAYA_PATH = os.environ["MAYA_LOCATION"]
IMAGE_MAGICK_PATH = os.path.join(MAYA_PATH, "bin/magick.exe")

# AUTOMATION_TOOL_KIT = "Z:/mtk/tools/standalone/substance_automation_toolkit"

# CACHE_DIR = os.path.join(os.environ["HOME"], "_".join(TITLE.lower().split()))
# CACHE_DIR = os.path.join(os.environ["APPDATA"], "_".join(TITLE.lower().split()))

# if not os.path.exists(CACHE_DIR):
#     os.makedirs(CACHE_DIR)

VTX_COLOR_SET_NAME = "ar_vtx_color"
DEFAULT_UV_SET = "map1"

# if not DEV_MODE:
#     from . import logger





def image_magick_exists():
    if os.path.exists(IMAGE_MAGICK_PATH):
        return IMAGE_MAGICK_PATH
    else:
        return None


def keep_selections(func):
    u"""選択を保持するdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _keep_selections_wrapper(func, *args, **kwargs)
    return wrapper


def _keep_selections_wrapper(func, *args, **kwargs):
    u"""選択を保持"""
    selection = cmds.ls(sl=True, type="tansform")
    result = func(*args, **kwargs)
    if selection:
        cmds.select(selection, ne=True)
    else:
        cmds.select(cl=True)
    return result

def get_parents(node):
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in get_parents(parent):
            yield p

def timeit(ndigits=2):
    """Print execution time [sec] of function/method
    - message: message to print with time
    - ndigits: precision after the decimal point
    """
    def outer_wrapper(func):
        # @wraps: keep docstring of "func"
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print("[ {} ] Function time for : {sec} [sec]".format(
                func.func_name,
                sec=round(end-start, ndigits))
            )
            return result
        return inner_wrapper
    return outer_wrapper


template_path = "Z:/mtk/tools/maya/modules/mtku/scripts/mtku/maya/menus/rendering/arnold_baker/sbs_tmplate/converter.sbs"
gsplit_template_path = "Z:/mtk/tools/maya/modules/mtku/scripts/mtku/maya/menus/rendering/arnold_baker/sbs_tmplate/converter_gsplit.sbs"
bsplit_template_path = "Z:/mtk/tools/maya/modules/mtku/scripts/mtku/maya/menus/rendering/arnold_baker/sbs_tmplate/converter_bsplit.sbs"
gray_template_path = "Z:/mtk/tools/maya/modules/mtku/scripts/mtku/maya/menus/rendering/arnold_baker/sbs_tmplate/converter_gray.sbs"

AI_UTIL_SHADER_MODE = {
    "ndoteye"   :0,
    "lambert"   :1,
    "flat"      :2,
    "ambocc"    :3,
    "plastic"   :4,
    "metal"     :5,
    }


AI_UTIL_COLOR_MODE = {
    "color"     :0,
    "normal"    :3,
    "uv"        :5,
    "v"         :7,
    "position"  :10,
}



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

        # self._start_time = datetime.datetime.now()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # logger.info('[ {} ] : End : Calculation time : {}'.format(self.title, calc_time))

        if self._show_progress:
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)
            # cmds.progressWindow(e=True,
            #         status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, self.status))

    def _set_status(self, status):
        if self._show_progress:
            # self.status = status
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


@timeit(ndigits=2)
def get_polygon_shell(node):
    island_list = []

    face_conut = cmds.polyEvaluate(node, face=True)
    with ProgressWindowBlock(title='Random Color', maxValue=face_conut) as prg:
        for i in range(face_conut):
            _li = list(set(cmds.polySelect(node, q=True, extendToShell=i, ns=True)))
            if not island_list:
                island_list = [_li]
            elif _li not in island_list:
                island_list = island_list + [_li]
            prg.status = '{} ...'.format(node)
            if prg.is_cancelled():
                break
            prg.step(1)
    return island_list

def get_polygon_shell_dict(node):
    island_dict = {}
    for i in range(cmds.polyEvaluate(node, face=True)):
        _li = set(cmds.polySelect(node, q=True, extendToShell=i, ns=True))
        if not island_dict:
            island_dict[i] = [_li]
        elif _li not in island_dict:
            island_dict[i] = island_dict[i] + [_li]
    return island_dict

@timeit(ndigits=2)
def set_color(mesh_fn, cColorArry, id):
    mesh_fn.setVertexColors(cColorArry, id)

@timeit(ndigits=2)
def assign_vtx_color_on_polygon_shell(mesh_fn, island_list, prg=None):
    _v = []
    cColorArry = om2.MColorArray()
    for face_ids in island_list:
        shell_color = om2.MColor((random.random(), random.random(), random.random(), 1.0))
        for face_id in face_ids:
            for v in mesh_fn.getPolygonVertices(face_id):
                if prg:
                    prg.step(1)
                cColorArry.append(shell_color)
                _v.append(v)
    mesh_fn.setVertexColors(cColorArry, _v)
    mesh_fn.updateSurface()

@timeit(ndigits=2)
def set_func():
    transform_nodes = cmds.ls(sl=True, type="transform", l=True)
    if not transform_nodes:
        return
    # vtx_count = cmds.polyEvaluate(transform_nodes, v=True)

    for node in transform_nodes:

        sel_list = om2.MGlobal.getSelectionListByName(node)
        dagPath = sel_list.getDagPath(0)

        meshes = cmds.listRelatives(node, s=True, fullPath=True, type="mesh")
        meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]
        if not meshes:
            continue
        mesh = meshes[0]
        sel_list = om2.MGlobal.getSelectionListByName(mesh)
        dagPath = sel_list.getDagPath(0)
        print(dagPath.fullPathName())
        print(dagPath.hasFn(om2.MFn.kMesh))

        if not dagPath.hasFn(om2.MFn.kMesh):
            continue

        mesh_fn = om2.MFnMesh(dagPath)
        island_list = get_polygon_shell(node)
        assign_vtx_color_on_polygon_shell(mesh_fn, island_list)
        cmds.setAttr(dagPath.fullPathName() + ".displayColors", 1)



class AutomationToolKit(object):

    aContext = context.Context()
    context.Context.setAutomationToolkitInstallPath(automationToolkitInstallPath = AUTOMATION_TOOL_KIT)

    def __init__(self, template_path, image_path, output_name, output_path, output_size):

        if output_name.endswith("Root"):
            self.template_path = gsplit_template_path
        elif output_name.endswith("Depth"):
            self.template_path = bsplit_template_path
        elif output_name.endswith("Vcolor"):
            self.template_path = gray_template_path
        else:
            self.template_path = template_path
        self.output_name = output_name
        self.output_path =output_path
        self.base_color_image_connect = 'input@path@' + image_path + '@format@JPEG'
        self.output_size = output_size

        self.create_sbs()
        self.create_sbsar()
        self.create_image()


    def create_sbs(self):
        proc = batchtools.sbsmutator_edit(
            input = self.template_path,
            presets_path = self.aContext.getDefaultPackagePath(),
            output_name = self.output_name,
            output_path = self.output_path,
            # output_path = CACHE_DIR,
            connect_image = self.base_color_image_connect + '@format@RAW',
            stderr = subprocess.PIPE
            # set_value = ('$outputsize@%s,%s' % (self.output_size, self.output_size))
            )
        (out, err) = proc.communicate()
        proc.wait()
        if err:
            print(err)
            sys.exit(1)


    def create_sbsar(self):
        proc = batchtools.sbscooker(
            # inputs = os.path.join(CACHE_DIR, self.output_name) + '.sbs',
            inputs = os.path.join(self.output_path, self.output_name) + '.sbs',
            includes = self.aContext.getDefaultPackagePath(),
            size_limit = 13,
            output_path = self.output_path,
            # output_path = CACHE_DIR
            )
        (out, err) = proc.communicate()
        proc.wait()

        if err:
            print(err)
            sys.exit(1)


    def create_image(self):
        proc = batchtools.sbsrender_render(
            # inputs = os.path.join(CACHE_DIR, self.output_name) + '.sbsar',
            inputs = os.path.join(self.output_path, self.output_name) + '.sbsar',
            output_name = '{inputName}',
            output_path = self.output_path,
            output_format = 'tga',
            set_value = ('$outputsize@%s,%s' % (self.output_size, self.output_size))
            )
        (out, err) = proc.communicate()
        proc.wait()
        if err:
            print(err)
            sys.exit(1)



class SGInMembers:
    def __init__(self, SG="", members=[]):
        self.SG = SG
        self.members = members

    def __repr__(self):
        return self.SG



class ArnoldRenderTextureBake(object):
    def __init__(self, export_path="", targets=[], sources=[], uv_set_id=0, assign_shader=False):
        self.sg_members = []
        self.export_path = export_path
        self.targets = targets
        self.sources = sources
        self.uv_set_id = uv_set_id
        self.assign_shader = assign_shader
        self.target_uv = {}
        self._show_hide_flags = {}
        self.alpha_map = ""
        self.set_up_bake()

        # self.remove_exr()

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
            shape = shape[0].replace("|", "_")
            exr = os.path.join(self.export_path, "{}.exr".format(shape))
        return exr.replace(os.sep, '/')

    def remove_exr(self):
        """exr を消すために作った、使っていない
        """
        target_meshes = []
        for node in self.targets:
            shape = cmds.listRelatives(node, s=True, path=True)
            if shape:
                target_meshes.append(shape[0])

        if target_meshes:
            for node in target_meshes:
                exr = os.path.join(self.export_path, "{}.exr".format(node))
                if os.path.exists(exr):
                    os.remove(exr)

    def set_up_bake(self):
        """ベイクの前準備
        ベイク時に、ソースとターゲットのみを表示にしたい
        先に全てのトランスフォームノードを非表示にし、その後ソースとターゲットを表示
        最初の表示、非表示状態を覚えておき、ベイク終了時に再適用
        マテリアルを変更する場合に備え、元のマテリアルと所属メンバーを取得し最後に適用
        アルファ抜きAOのためのアルファ取得
        UVセット切り替えのためのUVセット取得
        """
        target_nodes = self.targets + self.sources
        # _all_transform = cmds.ls(type="transform", long=True)
        _all_transform = cmds.ls(assemblies=True ,l=True)
        self._show_hide_flags = {}
        uv_set = ""
        for _transform in _all_transform:

            self._show_hide_flags[_transform] = cmds.getAttr("{}.v".format(_transform))
            cmds.setAttr("{}.v".format(_transform), 0)

        for node_longname in target_nodes:
            if not cmds.objExists(node_longname):
                continue
            cmds.setAttr("{}.v".format(node_longname), 1)
            for parent in get_parents(node_longname):
                cmds.setAttr("{}.v".format(parent), 1)
            shape = cmds.listRelatives(node_longname, s=True, fullPath=True, type="mesh")
            print(shape, " ---- shape")
            if shape:
                SGs = list(set(cmds.listConnections(shape, s=False, d=True, t='shadingEngine')))
                for SG in SGs:
                    mat = list(set(cmds.ls(cmds.listConnections(SG, s=True, d=False), mat=True)))
                    file_node = cmds.listConnections(mat, c=True, d=False, p=True, type='file')

                    if file_node:
                        if file_node[0].endswith("opacity") or file_node[0].endswith("transparency"):
                            self.alpha_map = file_node[1].split(".")[0]
                    members = [x for x in cmds.ls(cmds.sets(SG, q=True), l=True)if x.split(".")[0] in target_nodes or x.split(".")[0] in shape]
                    mem = SGInMembers(SG, members)
                    self.sg_members.append(mem)
                if self.uv_set_id:
                    uvs = cmds.polyUVSet(shape, q=True, allUVSets=True)
                    if len(uvs) > self.uv_set_id:
                        uv_set = uvs[self.uv_set_id]
            self.target_uv[node_longname] = uv_set

    def end_procces(self):
        """ベイク終了時に表示を元に戻す
        """
        if not self._show_hide_flags:
            return
        for name, value in self._show_hide_flags.items():
            cmds.setAttr("{}.v".format(name), value)

    def create_material(self, map_type):
        """マテリアル生成、map_typeに応じたマテリアルを生成

        Args:
            map_type (str): 出力マップタイプ

        Returns:
            [list]: マップ生成時に作ったシェーダを戻しまとめて消す
        """
        shader = []

        if map_type == "Normal":
            shader = self.normal(map_type)
        elif map_type == "Flow":
            shader = self.flow(map_type)
        elif map_type == "AO":
            shader = self.ao(map_type)
        elif map_type == "Root":
            shader = self.root(map_type)
        elif map_type == "Depth":
            shader = self.depth(map_type)
        elif map_type == "Alpha":
            shader = self.alpha(map_type)
        elif map_type == "Vcolor":
            shader = self.vtx_color(map_type)
        return shader


    def normal(self, map_type):
        sg= cmds.sets(n="{}SG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type, ss=True)
        cmds.setAttr("{}.shadeMode".format(shader), 2)
        cmds.setAttr("{}.colorMode".format(shader), 3)

        cmds.connectAttr('{}.outColor'.format(shader) ,'{}.surfaceShader'.format(sg), f=True)
        cmds.sets(self.all_shapes, edit=True, forceElement=sg)
        return [sg, shader]

    def flow(self, map_type):
        sg= cmds.sets(n="{}SG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type, ss=True)
        sampler_node = cmds.shadingNode('samplerInfo', name="{}_info".format(map_type), asUtility=True, ss=True)
        range_node = cmds.shadingNode('setRange', asUtility=True, name="{}_range".format(map_type), ss=True)
        cmds.setAttr("{}.shadeMode".format(shader), 2)
        cmds.setAttr("{}.colorMode".format(shader), 0)
        cmds.connectAttr(sampler_node + '.tangentVCamera', range_node + '.value', force=True)
        cmds.connectAttr(range_node + '.outValue', shader + '.color', force=True)
        cmds.setAttr(range_node + '.max', 1, 1, 1)
        cmds.setAttr(range_node + '.oldMin', -1, -1, -1)
        cmds.setAttr(range_node + '.oldMax', 1, 1, 1)
        cmds.connectAttr('{}.outColor'.format(shader) ,'{}.surfaceShader'.format(sg), f=True)
        cmds.sets(self.all_shapes, edit=True, forceElement=sg)
        return [sg, sampler_node, range_node, shader]

    def ao(self, map_type):
        fg_sg= cmds.sets(n="{}fgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        bg_sg= cmds.sets(n="{}bgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode("aiStandardSurface", asShader=True, name=map_type+"fg", ss=True)
        fg_ao_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"fgao", ss=True)
        bg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"bg", ss=True)

        cmds.setAttr("{}.shadeMode".format(fg_ao_shader), 3)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(fg_ao_shader), 0)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)
        cmds.setAttr("{}.emission".format(fg_shader), 1.0)


        if self.black_bg_flag:
            cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        else:
            cmds.setAttr("{}.color".format(bg_shader), 1, 1, 1, type="double3")

        cmds.connectAttr('{}.outColor'.format(fg_ao_shader) ,'{}.emissionColor'.format(fg_shader), f=True)
        cmds.connectAttr('{}.outColor'.format(fg_shader) ,'{}.surfaceShader'.format(fg_sg), f=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader) ,'{}.surfaceShader'.format(bg_sg), f=True)

        if self.alpha_map:
            cmds.connectAttr("{}.outColor".format(self.alpha_map), "{}.opacity".format(fg_shader), f=True)

        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)
        return[fg_sg, fg_shader, bg_sg, bg_shader, fg_ao_shader]


    def root(self, map_type):
        fg_sg= cmds.sets(n="{}fgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        bg_sg= cmds.sets(n="{}bgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"fg", ss=True)
        bg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"bg", ss=True)
        cmds.setAttr("{}.shadeMode".format(fg_shader), 2)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(fg_shader), 5)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)

        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)
        cmds.connectAttr('{}.outColor'.format(fg_shader) ,'{}.surfaceShader'.format(fg_sg), f=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader) ,'{}.surfaceShader'.format(bg_sg), f=True)
        return[fg_sg, fg_shader, bg_sg, bg_shader]

    def depth(self, map_type):
        fg_sg= cmds.sets(n="{}fgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        bg_sg= cmds.sets(n="{}bgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"fg", ss=True)
        bg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"bg", ss=True)

        cmds.setAttr("{}.shadeMode".format(fg_shader), 2)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        # cmds.setAttr("{}.colorMode".format(fg_shader), 9)
        cmds.setAttr("{}.colorMode".format(fg_shader), 10)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)

        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)

        cmds.connectAttr('{}.outColor'.format(fg_shader) ,'{}.surfaceShader'.format(fg_sg), f=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader) ,'{}.surfaceShader'.format(bg_sg), f=True)
        return[fg_sg, fg_shader, bg_sg, bg_shader]


    def alpha(self, map_type):
        fg_sg= cmds.sets(n="{}fgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        bg_sg= cmds.sets(n="{}bgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        fg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"fg", ss=True)
        bg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"bg", ss=True)
        cmds.setAttr("{}.shadeMode".format(fg_shader), 2)
        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(fg_shader), 0)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)
        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")
        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)
        cmds.connectAttr('{}.outColor'.format(fg_shader) ,'{}.surfaceShader'.format(fg_sg), f=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader) ,'{}.surfaceShader'.format(bg_sg), f=True)
        return[fg_sg, fg_shader, bg_sg, bg_shader]


    def vtx_color(self, map_type):
        fg_sg= cmds.sets(n="{}fgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        bg_sg= cmds.sets(n="{}bgSG".format(map_type), renderable=True, noSurfaceShader=True, empty=True)
        bg_shader = cmds.shadingNode("aiUtility", asUtility=True, name=map_type+"bg", ss=True)

        fg_shader = cmds.shadingNode("aiUserDataColor", asUtility=True, name=map_type+"fg", ss=True)
        cmds.setAttr("{}.colorAttrName".format(fg_shader), VTX_COLOR_SET_NAME, type="string")

        cmds.setAttr("{}.shadeMode".format(bg_shader), 2)
        cmds.setAttr("{}.colorMode".format(bg_shader), 0)

        cmds.setAttr("{}.defaultValue".format(fg_shader), 1, 1, 1, type="double3")
        cmds.setAttr("{}.color".format(bg_shader), 0, 0, 0, type="double3")

        cmds.sets(self.target_shapes, edit=True, forceElement=bg_sg)
        cmds.sets(self.source_shapes, edit=True, forceElement=fg_sg)

        cmds.connectAttr('{}.outColor'.format(fg_shader) ,'{}.surfaceShader'.format(fg_sg), f=True)
        cmds.connectAttr('{}.outColor'.format(bg_shader) ,'{}.surfaceShader'.format(bg_sg), f=True)
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
            all_color_sets = cmds.polyColorSet(target, q=True, allColorSets=True)
            if all_color_sets and all_color_sets[0] != VTX_COLOR_SET_NAME:
                cmds.polyColorSet(target, rename=True, colorSet=all_color_sets[0], newColorSet=VTX_COLOR_SET_NAME)
                cmds.polyColorSet(target, currentColorSet=True, colorSet=VTX_COLOR_SET_NAME)
            cmds.setAttr("{}.aiExportColors".format(target), value)
            cmds.setAttr("{}.displayColors".format(target), value)

    @keep_selections
    def arnold_render_textures(
                self,
                file_name = "",
                export_maps = [],
                resolution = 1024,
                aa_samples = 3,
                filter = "box",
                filter_width = 1.0,
                normal_offset = 2.0,
                enable_aovs = False,
                extend_edges = False,
                delete_shader = True,
                black_bg_flag = True,
                _crop_uv_flag = True
                ):
        """Arnold設定グローバル版

        Args:
            file_name (str, optional): [description]. Defaults to "".
            export_maps (list, optional): [description]. Defaults to [].
            resolution (int, optional): [description]. Defaults to 1024.
            aa_samples (int, optional): [description]. Defaults to 3.
            filter (str, optional): [description]. Defaults to "box".
            filter_width (float, optional): [description]. Defaults to 1.0.
            normal_offset (float, optional): [description]. Defaults to 2.0.
            enable_aovs (bool, optional): [description]. Defaults to False.
            extend_edges (bool, optional): [description]. Defaults to False.
        """
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
        self.black_bg_flag = black_bg_flag
        self.crop_uv = _crop_uv_flag

        self.shader = ""
        self.resolution = resolution
        self.aa_samples = aa_samples
        self.filter = filter
        self.filter_width = filter_width
        self.normal_offset = normal_offset
        self.enable_aovs = enable_aovs
        self.extend_edges = extend_edges
        self.file_name = file_name

        self.target_shapes = self.get_mesh_shapes(self.targets)
        self.source_shapes = self.get_mesh_shapes(self.sources)
        self.all_shapes = self.target_shapes + self.source_shapes

        self.switch_occlusion(True)
        self.switch_vtx_color(True)

        shader = ""
        if not export_maps:
            for target in self.targets:
                self.arnold_render_texture(target)
        else:
            for map_type in export_maps:
                if self.assign_shader:
                    shader = self.create_material(map_type)
                for target in self.targets:
                    self.arnold_render_texture(target, map_type)
                if shader:
                    if delete_shader:
                        cmds.delete(shader)
                    for _ in self.sg_members:
                        cmds.sets(_.members, edit=True, forceElement=_.SG)
        self.end_procces()


    def get_mesh_shapes(self, nodes):
        """メッシュシェイプ抽出

        Args:
            nodes (list): トランスフォームノード

        Returns:
            [list]: メッシュシェイプ
        """
        shapes = []
        for node in nodes:
            shape = cmds.listRelatives(node, s=True, fullPath=True, type="mesh")
            if shape:
                shapes.extend(shape)
        return shapes

    def get_target_uv_size_u_min_max(self, target):
        maps = cmds.ls(cmds.polyListComponentConversion(target, tuv=True), fl=True)

        uv_values = cmds.polyEditUV(maps, q=True, v=True)
        u_values = uv_values[0::2]
        v_values = uv_values[1::2]

        return min(u_values), max(u_values), min(v_values), max(v_values)


    def arnold_render_texture(self, target, map_type=""):
        """Arnold設定ローカル版
        各マップの名前による分岐部分
        シャドウと頂点カラーのスイッチをこっちに入れても良いかもしれないが
        全部一緒にやっても良いだろう、ということでグローバルに入れた

        Args:
            target ([type]): [description]
            map_type (str, optional): [description]. Defaults to "".
        """
        cmds.select(target, r=True)

        uv_set = self.target_uv[target]

        # if map_type == "AO":
        #     self.switch_occlusion(True)
        # elif map_type == "Vcolor":
        #     self.switch_vtx_color(True)
        # else:
        #     self.switch_vtx_color(False)
        #     self.switch_occlusion(False)

        cmds.arnoldRenderToTexture(
            folder = self.export_path,
            shader = self.shader,
            resolution = self.resolution,
            aa_samples = self.aa_samples,
            filter = self.filter,
            filter_width = self.filter_width,
            all_udims = self.all_udims,
            udims = self.udims,
            uv_set = uv_set,
            normal_offset = self.normal_offset,
            enable_aovs = self.enable_aovs,
            extend_edges = self.extend_edges,
            u_start = self.uStart,
            u_scale = self.uScale,
            v_start = self.vStart,
            v_scale = self.vScale,
            sequence = self.useSequence,
            frame_start = self.frameStart,
            frame_end = self.frameEnd,
            frame_step = self.frameStep,
            frame_padding = self.framePadding
            )

        exr_path = self.create_exr_path(target)
        if map_type:
            new_file_name = "{}_{}".format(self.file_name, map_type)
        else:
            new_file_name = self.file_name

        new_file_name_ext = "{}.exr".format(new_file_name)
        new_file_path = os.path.split(exr_path)[0]
        new_file_path = os.path.join(new_file_path, new_file_name_ext).replace(os.sep, '/')

        if os.path.exists(new_file_path):
            try:
                os.remove(new_file_path)
            except Exception as e:
                # logger.error(u'Can Not Remove File {}'.format(new_file_path))
                print(e)
        try:
            os.rename(exr_path, new_file_path)
        except Exception as e:
            # logger.error(u'Can Not Rename FIle {}'.format(exr_path))
            print(e)

        if not os.path.exists(AUTOMATION_TOOL_KIT) or not os.path.exists(PYSBS):
            return


        attk = AutomationToolKit(
                    template_path,
                    new_file_path,
                    new_file_name,
                    self.export_path,
                    self.output_size
                    )

        if self.crop_uv:
            u_min, u_max, v_min, v_max = self.get_target_uv_size_u_min_max(target)
            x_min = self.resolution * u_min
            x_max = self.resolution * u_max
            y_min = self.resolution * (1.0 - v_min)
            y_max = self.resolution * (1.0 - v_max)
            x_size = x_max - x_min
            y_size = y_min - y_max

            print("u_min, u_max, v_min, v_max", u_min, u_max, v_min, v_max)
            print("image_magick_exists() -- ", image_magick_exists())

            if image_magick_exists():
                _crop_image_file = os.path.join(self.export_path, new_file_name).replace(os.sep, '/')
                _command = "{} convert ".format(IMAGE_MAGICK_PATH)
                _command += "{}.tga -crop ".format(_crop_image_file)
                _command += "{:.0f}x{:.0f}+{:.0f}+{:.0f} ".format(x_size, y_size, x_min, y_max)
                _command += "{}.tga".format(_crop_image_file)
                print("_command - ", _command)
                subprocess.Popen(_command)
            else:
                cmds.error(u"image converter が見つかりません")

