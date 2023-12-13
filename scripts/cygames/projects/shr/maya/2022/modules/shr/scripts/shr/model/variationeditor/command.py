# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import glob
from collections import OrderedDict
import os
import json
import subprocess
import re

import maya.OpenMaya as om
import maya.cmds as cmds

import importlib

# from ...utils.perforce import MtkP4
import mtk.utils.perforce as _MtkP4
from mtk.utils import getCurrentSceneFilePath

from . import TITLE

importlib.reload(_MtkP4)
MtkP4 = _MtkP4.MtkP4


SUFFIX_EXT = "_alb.tga"
TEXTURE_PREFIX = "tex_"
MATERIAL_SLOT_PREFIX = "mtl_"
CHARACTOR_DIR = "characters"
WORK_TEXTURE_DIR = "texture"
RUNTIME_PATH = "content/mtk/runtime/resources/"

VARIATION_SETTINGS = "{}_variation_settings"
JSON_FILE_NAME = "mdl_variation[{}].dtblj"
COVERTER_FILE_NAME = "convert.py"

CONTENT_RER_PATH = "content/mtk/work/resources/characters"
MATERIAL_PATH = "content/mtk/runtime/resources/characters/"
MATERIAL_DIR = "material"
MATERIAL_EXT = "mtl"

GROUP_NAMES = [
    "head",
    "neck",
    "face",
    "chest",
    "L_upperarm",
    "L_hand",
    "L_shoulder",
    "L_forearm",
    "R_forearm",
    "R_hand",
    "R_shoulder",
    "R_upperarm",
    "LA_waist",
    "LB_waist",
    "LC_waist",
    "RA_waist",
    "RB_waist",
    "RC_waist",
    "C_waist",
    "pants",
    "shoes",
    "R_Knee",
    "L_Knee",
    "default"
]


def _message_dialog(message, title=""):
    if title:
        message += title
    else:
        title = TITLE
    cmds.confirmDialog(
        message=message,
        title=title,
        button=['OK'],
        defaultButton='OK',
        cancelButton="OK",
        dismissString="OK")
    print(u"{}".format(message))


def _confirm_dialog(message, title=""):
    """
    確認用のダイアログ表示
    「OK」ボタンを押さないと処理を開始しない

    Args:
        message (str ): 表示するメッセージ
        title (str, ない場合はツール名): [description]. Defaults to "".

    Returns:
        bool: 「OK」ボタンが押されたらTrue
    """
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


class ProgressWindowBlock(object):
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self, title='', progress=0, minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
        self._show_progress = show_progress and (
            not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None

    def __enter__(self):

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status='[ {} ] : Start'.format(self.title),
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._show_progress:
            cmds.progressWindow(e=True, status='End ')
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)

    def _set_status(self, status):
        if self._show_progress:
            cmds.progressWindow(
                e=True, status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, status))

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


class VariationDatas:
    name = VARIATION_SETTINGS
    variations = []
    submeshdata = OrderedDict()
    materialdata = OrderedDict()

    def get_variation_by_name(self, name):
        for k, v in self.submeshdata.items():
            if k == name:
                return v
        # return self.submeshdata[name]
        # for var in self.variations:
        #     if var.name == name:
        #         return var


class SubMeshGroupData(object):
    group_list = []
    # group_dict = OrderedDict()

    def __init__(self):
        pass

    def get_submesh_group_by_name(self, name):
        for group in self.group_list:
            if group == name:
                return group


class VariationSubMeshGroup(object):
    """[sbm1_pants_002_grp]

    Args:
        object ([type]): [description]
    """
    sbm_name = "sbm"

    def __init__(self, group=None):
        self.variation = ""
        self.default_material_name = ""
        self.current_material_name = ""

        # |mdl_mob00_m_000|model|top_grp|head_grp|sbm1_head_001_grp
        self.group = group

        self.set_up_name()

        # []
        self.inside_groups = []

        # [u'|mdl_mob00_m_000|model|top_grp|head_grp|sbm1_head_005_grp|hair|hairShape',
        # u'|mdl_mob00_m_000|model|top_grp|head_grp|sbm1_head_005_grp|hair_in_1|hair_in_1Shape',
        # u'|mdl_mob00_m_000|model|top_grp|head_grp|sbm1_head_005_grp|hair_in_2|hair_in_2Shape',
        # u'|mdl_mob00_m_000|model|top_grp|head_grp|sbm1_head_005_grp|knot|knotShape']
        self.inside_meshes = []

        # []
        self.inside_meshes_shortnames = []

        # [hair, hair, hair, mask]
        self.material_obj = []
        self.visible = False
        self.check_box = ""

    def set_up_name(self):
        # sbm1_head_001_grp
        # sbm1_L_upperarm_001_grp
        self.short_name = self.group.split("|")[-1]

        # [sbm1] [head_001_grp]
        # [sbm1] [L_upperarm_001_grp]
        switch, self.no_switch_name = self.short_name.split("_", 1)
        self.switch = switch
        self.switch_flag = int(switch[-1])
        self.id = self.no_switch_name.split("_")[1]
        # head
        # name_split = self.short_name.split("_")

        for group in GROUP_NAMES:
            if self.no_switch_name.startswith(group):
                self.group_short_name = group
                break

    def change_switch(self, flag=0):
        if cmds.objExists(self.group):
            pre = self.short_name[:3]
            suf = self.short_name[4:]
            new_name = "{}{}{}".format(pre, flag, suf)
            new_name = cmds.rename(self.group, new_name)
            self.group = new_name
            self.set_up_name()

    def set_visible(self, flag=True):
        if cmds.objExists(self.group):
            cmds.setAttr("{}.v".format(self.group), flag)
            self.visible = flag

    def __repr__(self):
        return self.short_name


class VariationMaterial:
    def __init__(self, path, material_base_name):
        self.file_node = ""
        self.shading_engine = ""
        self.material = ""
        self.variation_textures = OrderedDict()
        self.variation_cyllista_materials = OrderedDict()
        self.default_texture = ""
        self.__current_texture = None

        work_texture_dir, basename = os.path.split(path)
        self.work_texture_path = path.replace(os.sep, '/')

        # boots
        self.material_base_name = material_base_name

        self.work_texture_dir = work_texture_dir
        self.basename = basename

        # boots
        # boots_a でも　boots　となるように
        self.type_name_split = material_base_name.rsplit("_")[0]

        scene_type = basename.split(TEXTURE_PREFIX, 1)[-1]
        scene_type = scene_type.split("_" + material_base_name)[0]

        # mob03_m_000
        self.scene_type = scene_type

        # mtl_boots
        self.material_slot_name = MATERIAL_SLOT_PREFIX + self.type_name_split

        self._get_variation()

        self._get_shading_engine()
        self._get_material()
        self._get_file_node()
        self._set_node_connection()

    def chenge_assign_texture(self, cy_material_name=None):
        """[summary]テクスチャ名の一部
        [tex_mob03_m_000_face01_alb.tga]
        [mob03_m_000_face01]
        Cyllista 上でのマテリアル名

        Args:
            cy_material_name (str): [mob03_m_000_face01]
        """

        if not cy_material_name:
            cy_material_name = list(self.variation_textures.keys())[0]

        path = self.variation_textures.get(cy_material_name)

        if not path:
            return
        cmds.setAttr('{}.fileTextureName'.format(self.file_node),
                     path,
                     type='string')

        self.__current_texture = cy_material_name

    @property
    def current_texture(self):
        return self.__current_texture

    @current_texture.setter
    def set_current_texture(self, cy_material_name):
        self.__current_texture = cy_material_name

    def get_current_face_material(self):
        members = []
        current_mat_name = ""
        if self.shading_engine:
            for mat in self.variation_textures.keys():
                members = cmds.ls(cmds.sets(self.shading_engine, q=True))
                if members:
                    current_mat_name = mat
                    break
        return current_mat_name

    def __repr__(self):
        return self.material_slot_name

    def _set_node_connection(self):
        flag = 0
        if self.shading_engine and self.material:
            if not cmds.isConnected(self.material + ".outColor",
                                    self.shading_engine + ".surfaceShader"):

                cmds.connectAttr('{}.outColor'.format(self.material),
                                 '{}.surfaceShader'.format(
                                     self.shading_engine),
                                 f=True)
            flag += 1

        if self.file_node and self.material:
            if not cmds.isConnected(self.file_node + ".outColor",
                                    self.material + ".color"):

                cmds.connectAttr('{}.outColor'.format(self.file_node),
                                 '{}.color'.format(self.material),
                                 f=True)
            flag += 1

        if flag == 2:
            self.__current_texture = list(self.variation_textures.keys())[0]

    def _get_variation(self):
        texture_name = self.basename.split(self.material_base_name)[
            0] + self.type_name_split
        path = os.path.join(self.work_texture_dir, "{}".format(texture_name))
        path = "{}*{}".format(path, SUFFIX_EXT).replace(os.sep, '/')
        for p in glob.glob(path):
            work_resource_path, tex_basename = p.split(WORK_TEXTURE_DIR, 1)
            tex_basename = tex_basename.rsplit(SUFFIX_EXT, 1)[0]
            tex_basename = tex_basename.split(TEXTURE_PREFIX, 1)[-1]
            p = p.replace(os.sep, '/')
            self.variation_textures[tex_basename] = p

        for tex_basename, path in self.variation_textures.items():
            runtime_path = ""
            work_resource_path = path.split(WORK_TEXTURE_DIR, 1)[0]
            work_resource_path, charactor_path = work_resource_path.split(
                CHARACTOR_DIR, 1)
            material_name = MATERIAL_SLOT_PREFIX + tex_basename + "." + MATERIAL_EXT
            runtime_path = RUNTIME_PATH + CHARACTOR_DIR + \
                charactor_path + MATERIAL_DIR + "/" + material_name
            self.variation_cyllista_materials[tex_basename] = runtime_path
        self.default_texture = list(self.variation_textures.keys())[0]

    def _get_shading_engine(self):
        shading_engine_name = "{}{}".format(self.material_slot_name, "SG")
        shading_engine = cmds.ls(shading_engine_name, type="shadingEngine")

        if shading_engine:
            sg = shading_engine[0]
        else:
            return
        members = cmds.ls(cmds.sets(sg, q=True))

        if not members:
            return
        self.shading_engine = sg

    def _get_material(self):
        if not self.shading_engine:
            return
        shader = cmds.ls(self.material_slot_name, mat=True)
        if not shader:
            return
        shader = shader[0]

        self.material = shader

    def _get_file_node(self):
        if not self.variation_textures and self.material:
            return
        file_path = list(self.variation_textures.values())[0]
        path, basename = os.path.split(file_path)
        file_name, ext = os.path.splitext(basename)

        ext = ext[1:]
        file_node_name = "{}_{}".format(file_name, ext)

        file_node = cmds.ls(file_node_name, type="file")
        if file_node:
            file_node = file_node[0]
        else:
            file_node = cmds.shadingNode("file",
                                         asTexture=True,
                                         name=file_node_name,
                                         ss=True)

        cmds.setAttr('{}.fileTextureName'.format(file_node),
                     file_path.replace(os.sep, '/'),
                     type='string')
        self.file_node = file_node


def get_p4_file_state(json_path):
    """
    P4のファイルステータス取得
    ドライブレターが大文字の場合に取れないケースがあった
    しかし、小文字にして取ると、取ることはできるが別のファイルと認識される
    Mayaを再起動すると取れたりする
    """
    file_status_ext = ""
    stat = ""
    current_users = ""

    if json_path and os.path.exists(json_path):
        try:
            file_status_ext = MtkP4.status_ext([json_path])
            stat = file_status_ext[json_path]["action"]
            # file_status_ext = file_status_ext
            # stat = stat
            current_users = file_status_ext[json_path]["users"]
            # file_fstat = MtkP4.fstat(json_path)
            # self.fstat = self.file_fstat[0]["headAction"]
        except Exception as e:
            print(e)

    return file_status_ext, stat, current_users


def show_p4_stat(json_path, stat, current_users):
    _m = u"指定のバリエーションデータ\n"
    _m += u"{}\n\n".format(json_path)

    if not stat:
        _m += u"は Perforce 上で管理されていないファイルです\n"
        _m += u"[ Release ] ボタンを押すことでサーバーに上げることができます"
    elif stat == "latest":
        _m += u"は最新バージョンのデータです\n"
        _m += u"[ Release ] ボタンを押すことでサーバー上のデータを更新できます"
    elif stat == "stale":
        _m += u"は最新バージョンのデータではありません\n"
        _m += u"最新データを取得してからエディタを起動します\n"
        _m += u"[ Release ] ボタンを押すことでサーバー上のデータを更新できます"
    elif stat == "other":
        if current_users:
            _users = u",".join(current_users)
            _m += u"は [ {} ] さんによってチェックアウトされています\n".format(_users)
            _m += u"[ Save ] ボタンを押しても保存されません\n"
            _m += u"[ Release ] ボタンを押してもデータを更新できません"
    elif stat == "checkout" or stat == "add":
        _m += u"は [ ご自身 ] によってチェックアウトされています\n"
        _m += u"[ Release ] ボタンを押すことでサーバー上のデータを更新できます"

    _message_dialog(_m)
    print(_m)


def get_newest_file(json_path):
    """
    p4 での最新データ取得
    """
    flag = False
    p4_state = get_p4_file_state(json_path)

    file_status_ext = p4_state[0]
    stat = p4_state[1]
    current_users = p4_state[2]
    # file_fstat = p4_state[3]

    if file_status_ext:
        flag = True
        # drive, _path = os.path.splitdrive(self.json_path)
        # drive = drive.upper()
        # _path = os.path.join(drive, _path).replace(os.sep, '/')
        with ProgressWindowBlock(title='Sync P4', maxValue=1) as prg:
            prg.status = 'Start Sync P4'
            _json_directory = os.path.split(json_path)[0]
            MtkP4.sync([u"{}".format(_json_directory)])
            prg.step(1)
            prg.status = 'Sync P4'
        show_p4_stat(json_path, stat, current_users)
    else:
        _message_dialog(u"P4 接続に失敗しました")
        print(u"P4 接続に失敗しました")

    return flag


def get_material_obj(scene_name):
    """[summary]

    Args:
        scene_name (str): シーンパス

    Returns:
        [OrderedDict]: マテリアルスロット名（Maya マテリアル名）
                    マテリアルオブジェクトのインスタンス
    """
    # scene_name = getCurrentSceneFilePath()
    if not scene_name:
        return

    material_dict = OrderedDict()
    path, basename = os.path.split(scene_name)
    scene_file_name, ext = basename.split(".", 1)
    scene_type = scene_file_name.split("mdl_", 1)[-1]
    texture_path = os.path.split(path)[0]
    texture_path = os.path.join(texture_path, "texture")
    texture_name = "{}_{}_".format("tex", scene_type)
    seach_path = os.path.join(
        texture_path, "{}*{}".format(texture_name, SUFFIX_EXT))

    for _path in glob.glob(seach_path):
        _basename = os.path.split(_path)[-1]
        material_base_name = _basename.split(
            texture_name)[-1].split(SUFFIX_EXT)[0]
        type_name_split = material_base_name.rsplit("_")
        if len(type_name_split) == 1:
            _m = VariationMaterial(_path, material_base_name)
            material_dict[_m.material_slot_name] = _m
    return material_dict


def get_scene_name():
    """シーン名取得
    cmds で取得できない時のためにOpenMayaでもやってみる
    シーン名からjsonファイルを特定
    """

    # mob00_m
    charactor_type = ""

    # mob00_m_000
    scene_type = ""

    # mdl_mob00_m_000
    scene_file_name = ""

    # mdl_mob00_m_000.ma
    basename = ""

    scene_name = getCurrentSceneFilePath()
    if not scene_name:
        scene_name = om.MFileIO.currentFile()

    if len(scene_name.split(".")) < 2:
        scene_name = ""

    if scene_name:
        scene_name = scene_name
        path, basename = os.path.split(scene_name)

        if basename[:4] != "mdl_":
            scene_name = ""
        else:
            scene_file_name, ext = basename.split(".", 1)
            scene_type = scene_file_name.split("mdl_", 1)[-1]
            charactor_type = scene_type.rsplit("_", 1)[0]

    if not scene_name:
        scene_name = ""

    return scene_name, basename, scene_file_name, scene_type, charactor_type


def create_convert_file(json_rer_path):
    """コンバート用のpyファイル作成

    [self._converter_path]
    # Z:\\mtk\\tools\\maya\\modules\\mtku\\scripts\\mtku\\maya\\menus\\file\\variationeditor\\convert.py
    C:\\Users\\S09251\\Documents\\variation_editor\\convert.py （こっちに変更）
    に都度生成

    [json_rer_path]
    content/mtk/work/resources/characters/mob/03/mdl_variation[mob03_f_variation_settings].dtblj

    """
    _com = "from cy.asset import asset, assetutil\n"
    _com += "path = '{}'\n".format(json_rer_path)
    _com += "asset_path = asset.path(virtualpath=path)\n"
    _com += "assetutil.export_and_convert(asset_path, logger=None)\n"

    print("--- create convert file -----\n")
    print(_com)

    # _converter_path = os.path.split(__file__)[0]
    _converter_path = os.path.join(
        os.environ["HOME"], "_".join(TITLE.lower().split()))

    if not os.path.exists(_converter_path):
        os.makedirs(_converter_path)

    _converter_path = os.path.join(_converter_path, COVERTER_FILE_NAME)
    _converter_path = os.path.normpath(_converter_path)

    with open(_converter_path, "w") as f:
        f.write(_com)

    return _converter_path


def convert_json(json_rer_path):
    """Cyllista モジュールを使える3系Pythonで[convert.py]を実行させる

    """
    _message = ""

    python = os.path.join(os.environ["CYLLISTA_TOOLS_PATH"],
                          'python',
                          'python.bat')
    print(python, " ----- python bat")
    if not os.path.exists(python):
        _message_dialog(u"Cyllista 環境を確認してください\nPython が見つかりません")

    _converter_path = create_convert_file(json_rer_path)
    if not _converter_path and not os.path.exists(_converter_path):
        _message_dialog(u"環境を確認してください\nコンバートファイルが生成されませんでした")
        return

    cmd = [python, _converter_path]
    print(cmd, " ----- send cmd -------\n")

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    retCode = p.returncode
    _path, basename = os.path.split(json_rer_path)
    if retCode != 0:
        _message = u"{}\nのコンバートに失敗".format(basename)
        # _message_dialog(u"{}\n\nのコンバートに失敗しました".format(json_rer_path))
        # print("failed to run {}".format(_converter_path))
        # raise RuntimeError("failed to run {}".format(COVERTER_FILE_NAME))
    else:
        _message = u"{}\nのコンバート成功".format(basename)
        # _message_dialog(u"{}\n\nをコンバートしました".format(json_rer_path))
        # print("success file convert {}".format(_converter_path))
    return _message


def get_groups(variation_materials):

    _model_node_name = "model"
    _roots = cmds.ls(assemblies=True)
    _model_node = cmds.ls(_model_node_name, type="transform")
    if not _model_node:
        _message_dialog(u"[ {} ] ノードがシーンにありません".format(_model_node_name))
        return

    exists_flag = False
    for _m in _model_node:
        if not cmds.objExists(_m):
            _message_dialog(u"[ {} ] ノードがシーンにありません".format(_m))
            exists_flag = True
            break

    if exists_flag:
        return

    _parent = cmds.listRelatives(_model_node, p=True, type="transform")
    if not _parent:
        _message_dialog(u"[ {} ] ノードがシーンルートになっています".format(_model_node_name))
        return
    elif _parent[0] not in _roots:
        _message_dialog(u"[ {} ] ノードがシーンルートの直下にありません".format(_model_node_name))
        return

    submesh_group_list = []

    need_nodes = []
    for node in cmds.ls("sbm*", type="transform", l=True):

        split_name = node.split("|")
        if split_name[2] == _model_node_name:
            short_name_split = split_name[-1].split("_")

            if len(short_name_split) < 4:
                continue

            # ['sbm0', 'chest', '001', 'grp']
            # chest_001_grp
            no_switch_name = "_".join(short_name_split[1:])

            _check_flag = False
            for _g in GROUP_NAMES:
                if no_switch_name.startswith(_g):
                    _check_flag = True
                    break

            if not _check_flag:
                continue
            need_nodes.append(node)

    need_ndoes = sorted(
        need_nodes, key=lambda x: x.split("|")[-1].split("_")[-2])

    for node in need_ndoes:
        mats = []
        split_name = node.split("|")
        _val = VariationSubMeshGroup(node)
        if split_name[-1].split("_")[-2] == "001":
            cmds.setAttr("{}.v".format(node), 1)
            _val.visible = True
        else:
            cmds.setAttr("{}.v".format(node), 0)
            _val.visible = False

        submesh_group_list.append(_val)
        _meshes = cmds.listRelatives(
            node, allDescendents=True, fullPath=True, type="mesh")
        if not _meshes:
            continue
        _meshes = [x for x in _meshes if not cmds.getAttr(
            "{}.intermediateObject".format(x))]
        default_material_name = ""

        for _mesh in _meshes:
            _sgs = cmds.listConnections(
                _mesh, s=False, d=True, type='shadingEngine')
            if not _sgs:
                continue
            for _sg in _sgs:

                mat = cmds.listConnections(_sg + '.surfaceShader')
                if mat:
                    mats.extend(mat)

        for mat in mats:
            mat_name_split = mat.split("_")
            if len(mat_name_split) < 2 or not mat.startswith("mtl_"):
                continue

            default_material_name = "{}_{}".format(
                mat_name_split[0], mat_name_split[1])

            if default_material_name in variation_materials:
                _val.inside_meshes = _val.inside_meshes + [_mesh]
                _val.material_obj = _val.material_obj + \
                    [variation_materials[default_material_name]]
            _val.default_material_name = default_material_name

    return submesh_group_list


def get_json_path(scene_name="",
                  scene_file_name="",
                  charactor_type=""):

    json_path = ""
    _converter_rer_path = ""
    _variation = ""

    scene_name_split = scene_file_name.split("_")

    # mdl_mob00_m_000.ma の「mob00」から
    # 「mob」と「00」を抽出
    _chara_type = re.findall(r"[a-z]+", scene_name_split[1])[0]
    _chara_num = re.findall(r'([+-]?[0-9]+\.?[0-9]*)', scene_name_split[1])

    if not _chara_num:
        return

    _chara_num = _chara_num[0]

    # Z:/mtk/work/resources/characters/mob/00/000/model/mdl_mob00_m_000.ma
    # の最初の「mob」で切り分け
    _rer_path, _chara_path = scene_name.split(_chara_type, 1)
    _rer_path = os.path.join(_rer_path, _chara_type, _chara_num)

    # {}_variation_settings に「mob00_m」を入れる
    # variation_data_name = VARIATION_SETTINGS.format(charactor_type)
    # json_type_name = VARIATION_SETTINGS.format(charactor_type)

    _variation = VARIATION_SETTINGS.format(charactor_type)

    # mdl_variation[{}].dtbljに「mob00_m_variation_settings」を入れる
    _json_file_name = JSON_FILE_NAME.format(_variation)

    _converter_rer_path = "{}/{}/{}/{}".format(CONTENT_RER_PATH,
                                               _chara_type,
                                               _chara_num,
                                               _json_file_name)
    json_path = os.path.join(_rer_path, _json_file_name)

    drive, json_path = os.path.splitdrive(json_path)
    drive = drive.upper()
    json_path = os.path.join(drive, json_path)

    json_path = json_path.replace(os.sep, '/')

    material_path = os.path.split(_chara_path[1:])[0]
    material_path = os.path.split(material_path)[0]
    material_path = os.path.join(MATERIAL_PATH,
                                 _chara_type,
                                 material_path,
                                 MATERIAL_DIR).replace(os.sep, '/')

    return json_path, _converter_rer_path, _variation


def set_up_json_data(variation_data, variation_materials):
    json_format = OrderedDict()
    json_format["name"] = "{}".format(variation_data.name)
    json_format["version"] = 0
    json_format["row_count"] = len(variation_data.variations)

    _column_data = OrderedDict()
    _column_data["name"] = "sub_meshes"
    _column_data["type"] = "S"
    _column_data["is_array"] = True

    _mat_column_datas = []
    _mat_name_list = []

    for variation in variation_data.variations:
        _variation_materials_dict = variation_data.materialdata.get(variation)
        if not _variation_materials_dict:
            continue
        for material_name, current_texture in _variation_materials_dict.items():
            mat_obj = variation_materials.get(material_name)
            if not mat_obj:
                continue

            if (current_texture != variation_materials[material_name].default_texture
                    and material_name not in _mat_name_list):
                _mat_column_data = OrderedDict()
                _mat_column_data["name"] = material_name
                _mat_column_data["type"] = "R"
                _mat_column_data["is_array"] = False

                _mat_name_list.append(material_name)
                _mat_column_datas.append(_mat_column_data)

    if _mat_column_datas:
        _column_data = [_column_data] + _mat_column_datas
    else:
        _column_data = [_column_data]

    json_format["column"] = _column_data
    json_format["row"] = []

    for variation in variation_data.variations:
        _row_data = OrderedDict()
        _row_data["id"] = variation
        _row_data["sub_meshes"] = variation_data.submeshdata[variation]
        _variation_materials_dict = variation_data.materialdata.get(variation)
        for material_name in _mat_name_list:
            mat_obj = variation_materials.get(material_name)
            current_texture_path = ""
            current_texture = _variation_materials_dict.get(material_name)
            if current_texture != variation_materials[material_name].default_texture:
                current_texture_path = mat_obj.variation_cyllista_materials.get(
                    current_texture, "")
            _row_data[material_name] = current_texture_path
        json_format["row"].append(_row_data)

    return json_format


def save_json(json_path, variation_data, variation_materials):
    _convert_message = ""
    p4_state = get_p4_file_state(json_path)

    file_status_ext = p4_state[0]
    stat = p4_state[1]
    current_users = p4_state[2]

    if not file_status_ext:
        _message_dialog(u"P4 接続に失敗しました")
        return

    if not variation_data.variations:
        _message_dialog(u"登録されたプリセットがありません [ Add Preset ] でプリセットを登録してください")
        return
    if not json_path:
        _message_dialog(u"適切な json ファイル名がありません")
        return

    _m = u"{}\n\n".format(json_path)
    _m += u"を保存しますか？"

    if not _confirm_dialog(_m, u'json ファイルの保存'):
        return

    json_format = set_up_json_data(variation_data, variation_materials)

    _flag = False
    MtkP4.edit([json_path])
    with open(json_path, "w") as _json_file:
        _json_data = json.dumps(
            json_format,
            indent=4,
            separators=(',', ': '))
        try:
            _json_file.write(_json_data)
            _flag = True
        except Exception as e:
            print(e)

    _m = u"バリエーションデータ\n"
    _path, basename = os.path.split(json_path)
    _m += u"{}\n".format(basename)

    if _flag:
        _t = u"保存しました"
        _m += u"の保存成功\n"
        _convert_message = convert_json(json_path)

    else:
        _t = u"！！保存に失敗しました！！"
        _m += u"の保存失敗\n\nファイルはコンバートされません"

    if _convert_message:
        _m += u"\n\n" + _convert_message

    _message_dialog(_m, _t)
    print(_m)


def submit_data(json_path):
    p4_state = get_p4_file_state(json_path)

    file_status_ext = p4_state[0]
    stat = p4_state[1]
    current_users = p4_state[2]

    if not file_status_ext:
        _message_dialog(u"P4 接続に失敗しました")
        return
    _m = u"指定のバリエーションデータ\n"
    _m += u"{}\n\n".format(json_path)

    if os.path.exists(json_path):
        if not stat or stat == "latest":
            MtkP4.edit([u"{}".format(json_path)])
        elif stat == "stale":
            _users = u",".join(file_status_ext[json_path]["users"])
            if _users:
                _m += u"は [ {} ] によってチェックアウトされています\n".format(_users)
            _message_dialog(_m, u"！！サブミットできません")
            return
    else:
        _m = u"json が保存されておりません\n"
        _m += u"一つ以上のプリセットを登録し、json ファイルを保存して下さい"
        _message_dialog(_m)
        return

    __m = _m + u"をサブミットしますか？"

    if not _confirm_dialog(__m):
        return

    description = u"{}".format(TITLE)
    MtkP4.submit([u"{}".format(json_path)], description)
    _t = u"サブミットしました"
    _message_dialog(_m, _t)
    print(_m)
