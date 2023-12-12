# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import os
import maya.cmds as cmds
import maya.mel

from . import TITLE
from . import HDA_PATH
from . import LOD_CREATE_HDA_NAME
from ...utils import gui_util


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
    selection = cmds.ls(selection=True, long=True, type="transform")
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

    meshes = cmds.listRelatives(selection, allDescendents=True, fullPath=True, type="mesh")
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
        _d = gui_util.ConformDialog(title=TITLE, message=_m)
        _d.exec_()
        return None, None

    # 元々フルパス運用だった部分
    # 試験的にショートネーム運用に変更している
    # for parent in get_parents(selection):
    #     root_node = parent
    # if not root_node:
    #     root_node = selection[0]
    root_node = selection[0].rsplit("|")[-1]

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
    _hda = cmds.ls(_hda, long=True)[0]

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

def duplicate_node(node:str, new_name:str, ids:str) -> str:
    dup_obj = cmds.duplicate(node, renameChildren=True)[0]
    dup_obj_long_name = cmds.ls(dup_obj, long=True)[0]

    all_face_ids = [x.rsplit("[", 1)[-1].rsplit("]")[0] for x in cmds.ls("{}.f[*]".format(
                                                                dup_obj_long_name), flatten=True)]
    del_ids = [x for x in all_face_ids if x not in ids]
    if del_ids:
        del_faces = ["{}.f[{}]".format(dup_obj_long_name, x) for x in del_ids]
        cmds.delete(del_faces)
    dup_obj = cmds.rename(dup_obj, new_name)
    dup_obj = cmds.ls(dup_obj, long=True)[0]
    world_dup_obj = cmds.ls(cmds.parent(dup_obj, world=True), long=True)[0]

    return world_dup_obj

def sort_outliner(root_node):
    _new_list = []

    _cld = cmds.listRelatives(root_node, children=True, fullPath=True, type="transform")
    _lods = [x for x in _cld if x.split("|")[-1].startswith("lod")]
    _lods = sorted(_lods)

    _model = None
    _collision = None
    _other = []

    for _c in _cld:
        _short_name = _c.rsplit("|")[-1]
        if _short_name.startswith("jnt"):
            _model = _c
            _new_list.append(_c)
        elif _short_name == "mesh":
            _collision = _c
        elif _short_name == "collision":
            _other.append(_c)

    _new_list.extend(_lods)
    if _collision:
        _new_list.append(_collision)
    if _other:
        _new_list.extend(_other)

    for _ in _new_list:
        cmds.reorder(_, back=True)

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

def _do_parent(name:str, target_node:str, parent_node_long_name:str):
    _new_full_name = f'{parent_node_long_name}|{name}'
    cmds.parent(target_node, parent_node_long_name)
    cmds.rename(target_node, name)
    return _new_full_name


class BakeAsset:
    def __init__(self, hda_name:str="", lod_num:int=0, remove_lod:bool=False):
        self.hda_name = hda_name
        self.lod_num = lod_num
        self.remove_lod = remove_lod

        self.root_node = ""
        self.lod_groups = []
        self.lod_group_dict = {}
        self.lod_group_data_dict = {}
        self._error_set = []

        # LOD 作成の元となったメッシュ
        self.base_node = ""

        self.lod_mesh_group_name = "mesh"
        # mesh グループが入る（lodGroupノード）
        # |enm0000|mesh
        self.lod_mesh_group = ""

        # lod0 のグループノードが入る
        # |enm0000|mesh|lod0
        self.lod_start_group = ""

        self.lod_base_name = "lod{}"
        self.lod_start_num = 0
        self.lod_start_name = f'{self.lod_base_name}'.format(self.lod_start_num)

    def bake_setup(self):
        self.get_base_transform_nodes()
        if not self.base_node:
            # self.base_node = self.hda_name.rsplit("|", 1)[-1]
            return

        # ルートノード取得
        self.get_base_transform_root_node()

        # ルート以下のmesh グループノード取得（lodGroup）
        self.get_shenron_mesh_group_node()

        # mesh がない場合にmesh グループ作成
        self.create_lod_group_root_node()

        # ツールUIからshenron 仕様のグループリスト作成
        self.setup_shenron_lod_groups()
        return True

    def get_base_transform_nodes(self):
        """HDA の元となったジオメトリの特定
        |enm0000|mesh|lod0|body_low_lod0 などの
        lod を作る元のノードのフルパスが入る
        複数オブジェクトには非対応
        """
        meshes = cmds.listRelatives(self.hda_name, allDescendents=True, fullPath=True, type="mesh")
        if not meshes:
            return
        meshes = [x for x in meshes
                        if x and not cmds.getAttr("{}.intermediateObject".format(x))]
        if not meshes:
            return

        shapes = [cmds.ls(x, long=True)[0] for x in cmds.listHistory(meshes, allFuture=True)
                                                                    if cmds.nodeType(x)=="mesh"]
        if not shapes:
            return

        base_shapes = []
        # フルパスの中にHDA の名前が入っているものを抽出
        for shape in shapes:
            if len(shape.split(self.hda_name))==1:
                if cmds.getAttr("{}.intermediateObject".format(shape)):
                    continue
                base_shapes.append(shape)
        if not base_shapes:
            return

        transform_nodes = cmds.listRelatives(base_shapes, parent=True, fullPath=True, type="transform")

        self.base_node = transform_nodes[0]

    def get_base_transform_root_node(self):
        """ルートノード取得
        """
        root_node = None
        if not self.base_node:
            return
        for _p in get_parents(self.base_node):
            root_node = _p
        self.root_node = root_node

    def get_shenron_mesh_group_node(self):
        """ルートノードの子にあるmesh ノード取得
        """
        print(self.base_node, self.root_node)
        if not self.root_node:
            return

        _children_nodes = cmds.listRelatives(self.root_node, children=True, fullPath=True, type="transform")
        if not _children_nodes:
            return

        _lod_mesh_group = [x for x in _children_nodes if x.rsplit("|", 1)[-1]==self.lod_mesh_group_name]
        if _lod_mesh_group:
            self.lod_mesh_group = _lod_mesh_group[0]

    def get_presp_camera(self):
        _cam = cmds.ls("perspShape", type='camera')
        if _cam:
            return _cam[0]

    def create_lod_group_root_node(self):
        """ルートの子にmesh という名前のLODグループノード作成
        """
        if not self.root_node:
            return

        if self.lod_mesh_group:
            return

        _lod_group_base_name = f'{self.root_node}|{self.lod_mesh_group_name}'
        if not cmds.objExists(_lod_group_base_name):
            _node = cmds.createNode("lodGroup", name=self.lod_mesh_group_name, skipSelect=True)
            _preps_cam = self.get_presp_camera()
            if _preps_cam:
                cmds.connectAttr(f'{_preps_cam}.worldMatrix', f'{_node}.cameraMatrix', force=True)
            _node = _do_parent(self.lod_mesh_group_name, _node, self.root_node)
            self.lod_mesh_group = _node

    def setup_shenron_lod_groups(self):
        """mesh 以下に各LODのグループを作成する準備
        """
        if not self.lod_mesh_group:
            return
        for num in range(self.lod_start_num, self.lod_num + 1):
            _lod_group_name = f'{self.lod_mesh_group}|{self.lod_base_name}'.format(num)
            self.lod_groups.append(_lod_group_name)

    def check_remove_lod_group(self):
        if not self.remove_lod:
            return
        _cld = cmds.listRelatives(self.lod_mesh_group, children=True, fullPath=True, type="transform")
        if not _cld or not self.lod_groups:
            return
        remove_lod_group = set(_cld) - set(self.lod_groups)
        if remove_lod_group:
            cmds.delete(list(remove_lod_group))

    def setup_shenron_lod_nodes(self):
        """mesh ノードの下に「lod1」などグループノード
        その下に元の名前を基準とした各メッシュのトランスフォームノード
        body_low_lod0を元として、_lod 以下を切り取り
        各lod グループの最後の一桁を抽出しつなげる
        """
        pattern  = r'\d+'
        self._error_set = []
        base_short_name = self.base_node.rsplit("|", 1)[-1]

        for _lod_group in self.lod_groups:
            lod_group_short_name = _lod_group.rsplit("|", 1)[-1]
            _find_all = re.findall(pattern, lod_group_short_name)

            if not _find_all:
                continue

            lod_num = _find_all[-1]
            if lod_num == '0':
                continue

            lod_num_name = f'lod{lod_num}'
            lod_sets_name = f'{lod_num_name}_*'

            # shenron ではlod0 がメッシュに付くのでそれの回避方法
            new_short_name = base_short_name.split("_lod")[0]
            new_short_name = f'{new_short_name}_{lod_num_name}'
            lod_set = cmds.ls(lod_sets_name, type="objectSet")

            if not lod_set:
                self._error_set.append(lod_num_name)
                continue

            _faces = cmds.ls(cmds.sets(lod_set, q=True), flatten=True, long=True)

            _source_name = _faces[0].rsplit(".", 1)[0]
            _face_ids = [x.rsplit("[", 1)[-1].rsplit("]")[0] for x in _faces]

            _lod_mesh_node = f'{_lod_group}|{new_short_name}'

            self.lod_group_dict[_lod_group] = _lod_mesh_node
            self.lod_group_data_dict[_lod_group] = {
                                                    "lod_group_short_name": lod_group_short_name,
                                                    "lod_mesh_node": _lod_mesh_node,
                                                    "source_name": _source_name,
                                                    "new_short_name": new_short_name,
                                                    "face_ids": _face_ids
                                                    }

    def create_lod_nodes(self):
        self.base_node_in_lod0()
        if not self.lod_group_data_dict:
            return
        for lod_group, lod_data in self.lod_group_data_dict.items():
            _lod_group_new_node = ""
            _exists_mesh_node = lod_data["lod_mesh_node"]
            if cmds.objExists(_exists_mesh_node):
                cmds.delete(_exists_mesh_node)

            if not cmds.objExists(lod_group):
                _lod_group_new_node = cmds.createNode(
                                                "transform",
                                                name=lod_data["lod_group_short_name"],
                                                skipSelect=True
                                                )

            dup_obj = duplicate_node(
                                    node=lod_data["source_name"],
                                    new_name=lod_data["new_short_name"],
                                    ids=lod_data["face_ids"]
                                    )

            if _lod_group_new_node:
                # _do_parent(lod_data["lod_group_short_name"], dup_obj, _lod_group_new_node)
                cmds.parent(dup_obj, _lod_group_new_node)
                cmds.parent(_lod_group_new_node, self.lod_mesh_group)
                cmds.rename(_lod_group_new_node, lod_data["lod_group_short_name"])
            else:
                cmds.parent(dup_obj, lod_group)
                # cmds.rename(dup_obj, lod_data["new_short_name"])

        self.setup_lod_shown_settings()
        sort_outliner(self.lod_mesh_group)

        if self._error_set:
            _m = u"[ {} ] \n".format(", ".join(self._error_set))
            _m += u"はポリゴン数がゼロのため生成されませんでした"
            _d = gui_util.ConformDialog(title=TITLE,
                            message=_m)
            _d.exec_()

    def setup_lod_shown_settings(self):
        _base_range = 300
        cmds.setAttr(f'{self.lod_mesh_group}.useScreenHeightPercentage', 0)
        for num, lod in enumerate(self.lod_groups):
            if num == 0:
                _lod_flag = 1
            else:
                _lod_flag = 0
            cmds.setAttr(f'{self.lod_mesh_group}.displayLevel[{num}]', 0)
            cmds.setAttr(f'{lod}.visibility', 1)
            cmds.setAttr(f'{self.lod_mesh_group}.threshold[{num}]', num*100+_base_range)

    def base_node_in_lod0(self):
        _base_short_name = self.base_node.rsplit("|", 1)[-1]
        check_hierarchy = f'{self.lod_mesh_group}|{self.lod_start_name}|{_base_short_name}'

        if not self.lod_groups:
            return

        if self.base_node == check_hierarchy:
            return

        _parent = cmds.listRelatives(self.base_node, parent=True, fullPath=True)
        if _parent:
            _parent = _parent[0]
        else:
            _parent = self.lod_mesh_group

        _lod0_group_node = self.lod_start_name

        if not cmds.objExists(self.lod_groups[0]):
            _lod0_group_node = cmds.createNode("transform", name=_lod0_group_node, skipSelect=True)
        else:
            _lod0_group_node = self.lod_groups[0]

        _lod0_mesh_name = _base_short_name.rsplit("_lod", 1)[0]
        _lod0_mesh_name = f'{_lod0_mesh_name}_lod0'

        _exis_lod0_mesh = f'{self.lod_mesh_group}|{self.lod_start_name}|{_lod0_mesh_name}'
        if cmds.objExists(_exis_lod0_mesh):
            cmds.delete(_exis_lod0_mesh)

        self.base_node = cmds.rename(self.base_node, _lod0_mesh_name)
        cmds.parent(self.base_node, _lod0_group_node)

        _parent = cmds.listRelatives(_lod0_group_node, parent=True, fullPath=True)
        if _parent:
            _parent = _parent[0]
            if  _parent == self.lod_mesh_group:
                return
        _ = cmds.parent(_lod0_group_node, self.lod_mesh_group)
        cmds.rename(_, self.lod_start_name)

    def get_nodes(self):
        return self.hda_name, self.base_node, self.root_node, self.lod_mesh_group, self.lod_groups


def bake_asset(hda_name:str="", lod_num:int=0, remove_lod:bool=False):
    sync_asset(hda=hda_name, sync_attribute=False, sync_output=True)

    _bs = BakeAsset(hda_name=hda_name, lod_num=lod_num, remove_lod=remove_lod)

    if not _bs.bake_setup():
        _m = f'[ {hda_name} ] の階層にメッシュが見つかりませんでした'
        _d = gui_util.ConformDialog(title=TITLE,
                        message=_m)
        _d.exec_()
        return

    # ツールUIから削除されたlod グループを集めて削除
    _bs.check_remove_lod_group()

    # 各lod グループを作成するための情報収集
    _bs.setup_shenron_lod_nodes()

    # 各lod 作成
    _bs.create_lod_nodes()


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
