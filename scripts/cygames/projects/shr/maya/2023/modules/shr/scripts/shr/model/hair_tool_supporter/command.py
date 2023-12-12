from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path
import json
import base64
from functools import partial
import threading
import shutil
import webbrowser
import yaml

from PySide2 import QtCore, QtGui, QtWidgets
from ...utils import gui_util
from ...utils import getCurrentSceneFilePath

import maya.cmds as cmds

from . import TOOL_NAME
from . import TITLE

from . import FILE_NODE_NAME
from . import BUTTONS

# HAIR_MATERIAL_NAME = "HairMat"

HERE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "settings.yaml"


def load_config(config_name:str = '', config_file_path:str = ''):
    if not config_file_path:
        config_file_path:str = HERE / YAML_FILE_NAME
    with open(config_file_path, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    _confing_data = config.get(config_name, None)
    return _confing_data


# # BCM_GSCurvetoolsHelpers までのパス
# mydocument = Path(os.getenv("HOME"))
# mayascript = mydocument / "maya" / "scripts"
# bmc_helper = mayascript / "BCM_GSCurvetoolsHelpers"

# # プラグインパス、信頼できるパスを設定するためのパス
# trust_paths = [bmc_helper / "BCM_manip_plugin",
#             bmc_helper / "BCM_XRayCvs"]

# # プラグインファイル
# plugins = [bmc_helper / "BCM_manip_plugin" / "bcmCurveWarpManip.py",
#             bmc_helper / "BCM_XRayCvs" / "BCM_DrawXRayCvs.py"]


HAIR_MATERIAL_NAME = load_config('HAIR_MATERIAL_NAME')
CURRENT_MAYA_VERSION = cmds.about(version=True)


# BCM_GSCurvetoolsHelpers までのパス
mydocument = Path(os.getenv("HOME"))
mayascript = mydocument / "maya" / "scripts"
bmc_helper = mayascript / load_config('GS_Curve_Tools_Helpers_Inside_Name')

# プラグインパス、信頼できるパスを設定するためのパス
trust_paths = [
        bmc_helper / load_config('Helper_Plugin_Directory'),
        bmc_helper / load_config('Helper_XRay_Directory')
        ]

# プラグインファイル
plugins = [
        bmc_helper / load_config('Helper_Plugin_Directory') / load_config('Helper_Plugin_Name'),
        bmc_helper / load_config('Helper_XRay_Directory') / load_config('Helper_XRay_Name')
        ]


def _check_path(path: Path) -> bool:
    # パスの存在確認
    flag = True
    if not path.exists():
        cmds.warning(f'not found path -- [{path}]')
        flag = False
    return flag

def set_environ(paths:list=trust_paths):
    if not paths:
        return
    plugin_path = os.environ.get("MAYA_PLUG_IN_PATH")
    for path in paths:
        path = str(path).replace(os.sep, '/')
        if path not in plugin_path.split(";"):
            plugin_path += f';{path}'
    os.environ["MAYA_PLUG_IN_PATH"] = plugin_path
    plugin_path = os.environ.get("MAYA_PLUG_IN_PATH")

    print('Set Env Path -----------------------------------')
    for path in plugin_path.split(";"):
        print(f'Maya Plugin Path: [ {path} ]')


def set_plugin_path(paths:list=trust_paths):
    if not paths:
        return
    # プラグインパス、信頼できるパスに設定する
    safe_paths = cmds.optionVar(q="SafeModeAllowedlistPaths")
    for path in paths:
        if not _check_path(path):
            continue
        path = str(path).replace(os.sep, '/')
        if path not in safe_paths:
            cmds.optionVar(stringValueAppend=["SafeModeAllowedlistPaths", path])
    safe_paths = cmds.optionVar(q="SafeModeAllowedlistPaths")
    print('Set Trust Path ----------------------------------------')
    for path in safe_paths:
        print(f'Set Trust path: [ {path} ]')

def load_plugins(paths:list=plugins):
    if not paths:
        return
    for path in paths:
        if not _check_path(path):
            continue
        path = str(path).replace(os.sep, '/')
        cmds.loadPlugin(path, quiet=True)
        cmds.pluginInfo(path, edit=True, autoload=False)
    print('Loaded Plugins -----------------------------------------')
    for plugin, path in zip(cmds.pluginInfo(q=True, listPlugins=True), cmds.pluginInfo(q=True, listPluginsPath=True)):
        print(f'Load Plugin: [ {plugin} ] - [ {path} ]')


class ThredingFileCopy:
    def __init__(self, src_path:Path=Path(), dst_path:Path=Path())->None:
        self.count = 0
        self.src_path = src_path
        self.dst_path = dst_path

    def get_directory_size(self, path:Path=Path())->int:
        total_size = 0
        path = str(path)
        with os.scandir(path) as _iter:
            for entry in _iter:
                if entry.is_file():
                    total_size += entry.stat().st_size
                elif entry.is_dir():
                    total_size += self.get_directory_size(entry.path)
        return total_size

    def copy_tree(self)->str:
        result = ''
        try:
            result = shutil.copytree(str(self.src_path), str(self.dst_path))
        except Exception as e:
            print(e)
        return result

    def calculate(self):
        _thread = threading.Thread(
                                target=self.copy_tree,
                                args=(str(self.src_path),
                                      str(self.dst_path))
                                      )
        _thread.start()
        _next = 1
        _current = 0
        _end = self.get_directory_size(path=self.src_path)

        _all = range(100)
        _length = len(_all)
        prg = gui_util.ProgressDialog()
        prg.setUp(_length, "copy files ... ")
        prg.show()

        for i in _all:
            QtCore.QCoreApplication.processEvents()
            while(_next > _current) :
                _current = round(self.get_directory_size(path=self.dst_path) / _end * 100)
            if prg.wasCanceled():
                break
            _next = _current + 1
            prg.setValue(_current)
            prg.step(_current)
            if _next > _length:
                break
        _thread.join()


def file_copy(src_path:Path=None, dst_path:Path=None)->str:
    _success_flag = False
    dst_path = Path(dst_path)

    if dst_path.exists():
        _m = str(dst_path).replace(os.sep, '/')
        _m += '\n\nAlready there'
        _m += '\nRemove Old?'
        _d = gui_util.ConformDialogResult(title='Remove Old?', message=_m)
        result = _d.exec_()

        if not result:
            return
        try:
            shutil.rmtree(str(dst_path))
            _success_flag = True
        except Exception as e:
            print(e)
            pass
    else:
        _success_flag = True

    if not _success_flag:
        _d = gui_util.ConformDialog(title="Could not Remove Files",
                                    message="Could not Remove Files")
        _d.exec_()
        return
    else:
        _file_copy = ThredingFileCopy(src_path=src_path, dst_path=dst_path)
        _file_copy.calculate()

    return True



# import sys
# _path = r'C:\Users\S09251\Documents\maya\scripts\BCM_GSCurvetoolsHelpers'
# _path2 = 'C:/Users/S09251/Documents/maya/2022/scripts'
# if _path not in sys.path:
#     sys.path.append(_path)
# if _path2 not in sys.path:
#     sys.path.append(_path2)
# import gs_curvetools
# import binstall
# binstall.installUI()


def open_web_site():
    """ヘルプサイトを開く
    """
    _web_site = "https://wisdom.cygames.jp/pages/viewpage.action?pageId=284836889"
    # webbrowser.open(_web_site)
    cmds.warning('coming soon ....')

def get_scene_name():
    """シーン名取得

    Returns:
        _type_: _description_
    """
    return getCurrentSceneFilePath()

def attach_job(object_name="", job=None):
    """GUI にスクリプトジョブを付ける

    Args:
        object_name (str): GUI Object name
        job (function):
    """
    if not object_name or not job:
        return
    cmds.scriptJob(parent=object_name, event=("SceneOpened", partial(job)))
    cmds.scriptJob(parent=object_name, event=("NewSceneOpened", partial(job)))

def check_path_exists(path="", make_dir=False):
    """パスが存在するかの確認

    Args:
        path (str): [description]
        make_dir (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    if not os.path.exists(path) and make_dir:
        os.makedirs(path)

    if not os.path.exists(path):
        print("Not Found [ {} ]".format(path.replace(os.sep, '/')))
        cmds.warning("Not Found [ {} ]".format(path.replace(os.sep, '/')))
        return
    else:
        return True

def get_file_info_data(data_name="") -> str:
    """Maya のシーンに設定されたfileInfo のデータ取得
    shenron Easy Bind_{data_name}
    の形になる
    Args:
        data_name (str, optional): fileInfo のデータ名. Defaults to "".

    Returns:
        str: _description_
    """
    _info_data = cmds.fileInfo("{}_{}".format(TOOL_NAME, data_name), q=True)
    # _info_data = file_info_load(f"{TOOL_NAME}_{data_name}")

    return _info_data or None

def set_file_info_data(data_name="", value=""):
    """Maya シーンにfileInfo のデータを設定する

    Args:
        data_name (str, optional): fileInfo のデータ名. Defaults to "".
        value (str, optional): 設定するのデータの値. Defaults to "".
    """
    # file_info_save(f"{TOOL_NAME}_{data_name}", value=value)
    cmds.fileInfo("{}_{}".format(TOOL_NAME, data_name), value)





class Material:
    def __init__(self):
        self.name = ""
        self.material_node = ""
        self.blend_node1 = ""
        self.blend_node2 = ""
        self.reverse_node = ""
        self.shading_group_name = ""
        self.shading_group = ""
        self.blend_color = [0, 0, 0]
        self.exists_material=False
        self.depth_tex_node = ""
        self.irda_tex_ndoe = ""

    def create_material(self):
        """マテリアル作成
        """
        shader = cmds.shadingNode(
                        "lambert",
                        asShader=True,
                        name=self.name,
                        skipSelect=True
                        )
        self.material_node = shader
        self.connection(
                        source=self.material_node,
                        source_connection="outColor",
                        target=self.shading_group,
                        target_connection="surfaceShader"
                        )
        self.create_reverse_node()
        self.connection_irda_to_reverse()
        self.create_blend_nodes()
        self.connect_blend_nodes()

    def create_shading_group(self):
        """シェーディンググループ作成
        """
        shading_group = cmds.sets(
                        name=self.shading_group_name,
                        renderable=True,
                        noSurfaceShader=True,
                        empty=True
                        )
        self.shading_group = shading_group

    def create_reverse_node(self):
        """reverse ノード作成
        """
        utility = cmds.shadingNode("reverse", asUtility=True, skipSelect=True)
        self.reverse_node = utility

    def create_blend_node(self, num:int=0):
        """ブレンドノード作成

        Args:
            num (int, optional): _description_. Defaults to 0.
        """
        utility = cmds.shadingNode("blendColors", name=f'{self.name}_blend{num}',asUtility=True, skipSelect=True)

        if num == 0:
            self.blend_node1 = utility

        elif num == 1:
            self.blend_node2 = utility

        cmds.setAttr(
                    f"{utility}.color2",
                    self.blend_color[0], self.blend_color[1], self.blend_color[2],
                    type="double3"
                    )

    def create_blend_nodes(self):
        """ブレンドノード複数作成
        """
        for i in range(2):
            self.create_blend_node(num=i)

    def get_material(self, name:str="", color:list=[0, 0, 0], irda_texture_node:str="") -> str:
        """シーン中のヘアマテリアル取得

        Args:
            name (str, optional): ヘアマテリアル名（HairMatA）等. Defaults to "".
            color (list, optional): マテリアルに設定される色. Defaults to [0, 0, 0].
            irda_texture_node (str, optional): テクスチャノード. Defaults to "".

        Returns:
            str: ヘアマテリアル名
        """
        self.name = name
        self.shading_group_name = f'{name}SG'
        self.blend_color = color
        self.irda_tex_ndoe = irda_texture_node

        self.shading_group_exists()
        self.material_exists()
        if not self.shading_group:
           self.create_shading_group()
        if not self.material_node:
            self.create_material()

        return self.material_node

    def shading_group_exists(self):
        """シェーディンググループ存在確認
        """
        _shading_group = cmds.ls(self.shading_group_name, type="shadingEngine")
        if _shading_group:
            self.shading_group = _shading_group[0]

    def get_exists_material(self, name:str="") -> bool:
        """マテリアルの存在問い合わせ

        Returns:
            bool: _description_
        """
        material_node = [x for x in cmds.ls(materials=True)if x==name]

        if material_node:
            self.exists_material=True
            self.material_node = material_node[0]
        return self.exists_material

    def material_exists(self):
        """マテリアル存在確認
        """
        material_node = [x for x in cmds.ls(materials=True)if x==self.name]

        if material_node:
            self.exists_material=True
            self.material_node = material_node[0]

    def connection(self, source:str, target:str, source_connection:str, target_connection:str):
        """ノードコネクション

        Args:
            source (str): _description_
            target (str): _description_
            source_connection (str): _description_
            target_connection (str): _description_
        """
        if not cmds.isConnected(f'{source}.{source_connection}', f'{target}.{target_connection}'):
            cmds.connectAttr(f'{source}.{source_connection}', f'{target}.{target_connection}')

    def connect_blend_nodes(self):
        """ブレンドノードコネクト
        """
        self.connection(source=self.blend_node1, source_connection="output", target=self.material_node, target_connection="color")
        for _input in ["R", "G", "B"]:
            self.connection(source=self.irda_tex_ndoe, source_connection="outColorB", target=self.blend_node1, target_connection=f"color1{_input}")
        self.connection(source=self.blend_node2, source_connection="output", target=self.blend_node1, target_connection="color2")
        cmds.setAttr("{}.blender".format(self.blend_node1), 0.35)
        cmds.setAttr("{}.blender".format(self.blend_node2), 0.0)

    def connention_alpha(self, alpha_texture_node:str=""):
        """アルファマップをトランスペアレンシーに接続

        Args:
            alpha_texture_node (str, optional): _description_. Defaults to "".
        """
        self.connection(
                    source=alpha_texture_node,
                    source_connection='outTransparency',
                    target=self.material_node,
                    target_connection='transparency'
                    )

    def connection_irda_to_reverse(self):
        """テクスチャマップのアルファからトランスペアレンシーに接続
        """
        for _input in ["X", "Y", "Z"]:
            self.connection(
                        source=self.irda_tex_ndoe,
                        source_connection='outAlpha',
                        target=self.reverse_node,
                        target_connection=f'input{_input}'
                        )
        self.connection(
                    source=self.reverse_node,
                    source_connection='output',
                    target=self.material_node,
                    target_connection=f'transparency'
                    )

    def assign_mesh_to_material(self, mesh_nodes:list=[]):
        """マテリアルアサイン

        Args:
            mesh_nodes (list, optional): _description_. Defaults to [].
        """
        if not mesh_nodes:
            return
        cmds.sets(mesh_nodes, edit=True, forceElement=self.shading_group)
        print(f'assign material: [ {self.shading_group: <20} ] -> [ {mesh_nodes} ]')

def get_assigned_material_faces(material:str=""):
    """マテリアルがアサインされているフェース取得

    Args:
        material (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    members = None
    if cmds.objExists(material):
        sg = cmds.listConnections(
                material, source=False, destination=True, type='shadingEngine')
        members = cmds.ls(cmds.sets(sg, q=True), flatten=True)
    if members:
        members = cmds.listRelatives(members, parent=True, path=True)
    return members

def get_gs_type_nodes(base_nodes:str="", gs_type:str="geoCard"):
    """gs ノード取得

    Args:
        base_nodes (str, optional): _description_. Defaults to "".
        gs_type (str, optional): getCard or pathCurve. Defaults to "geoCard".

    Returns:
        _type_: _description_
    """
    nodes = []
    for base_node in base_nodes:
        parent = cmds.listRelatives(base_node, parent=True, path=True)
        children = cmds.listRelatives(parent, children=True, path=True)
        for child in children:
            if gs_type in child:
                nodes.append(child)
    return nodes

def mesh_or_curve_select(material_name:str="", selection_type:str=""):
    """gs メッシュ、カーブの選択

    Args:
        material_name (str, optional): _description_. Defaults to "".
        selection_type (str, optional): _description_. Defaults to "".
    """
    _types = {"Curve": "pathCurve", "Mesh": "geoCard"}
    if not material_name:
        return

    _type = _types[selection_type]
    material_mesh_nodes = get_assigned_material_faces(material=material_name)
    if not material_mesh_nodes:
        cmds.select(clear=True)
        cmds.warning(f'Not Found Matarial Assigned: [ {_type: <10} ]:  [ {material_name} ]')
        return

    selection_nodes = get_gs_type_nodes(base_nodes=material_mesh_nodes, gs_type=_type)

    if selection_nodes:
        cmds.select(selection_nodes, replace=True)


def assign_material(
                        selections:list=[],
                        material_name:str="",
                        material_color:list=[0,0,0],
                        irda:dict={}
                        ):
    """アサインマテリアル

    Args:
        selections (list, optional): _description_. Defaults to [].
        material_name (str, optional): _description_. Defaults to "".
        material_color (list, optional): _description_. Defaults to [0,0,0].
        irda (dict, optional): _description_. Defaults to {}.
        depth (dict, optional): _description_. Defaults to {}.
    """
    nodes = []

    if not irda:
        gui_util.conform_dialog(title=TITLE, message="Alpha Texture not Assigned")
        return

    nodes = get_gs_type_nodes(selections, gs_type="geoCard")

    if nodes:
        _mat = Material()

        current_material = _mat.get_material(name=material_name,
                                            color=material_color,
                                            irda_texture_node=irda[FILE_NODE_NAME])
        _mat.assign_mesh_to_material(mesh_nodes=nodes)

def button_clicked(
                action_type:str="assign",
                selection_type:str="Curve",
                button_name:str="",
                button_color:list=[0, 0, 0],
                irda:dict={}
                ):
    """カラーボタンクリック動作

    Args:
        selection_type (str, optional): _description_. Defaults to "Curve".
        button_name (str, optional): _description_. Defaults to "".
        button_color (list, optional): _description_. Defaults to [0, 0, 0].
        irda (dict, optional): _description_. Defaults to {}.
        depth (dict, optional): _description_. Defaults to {}.
    """
    if not button_name or not button_color:
        return

    _material_name = f"{HAIR_MATERIAL_NAME}{button_name[-1]}"
    _material_color = [x/255 for x in button_color]

    selections = cmds.ls(selection=True, objectsOnly=True, flatten=True)

    if action_type.lower().startswith("assign"):
        if not selections:
            cmds.warning('Select Assign Geometory')
        else:
            assign_material(
                    selections=selections,
                    material_name=_material_name,
                    material_color=_material_color,
                    irda=irda
                    )
    else:
        mesh_or_curve_select(material_name=_material_name, selection_type=selection_type)

def color_change_switch(button_name:str):
    """ユニークカラーとグレースケールの変更

    Args:
        button_name (str): _description_
    """
    for button, color in BUTTONS.items():
        hair_material_name = f'{HAIR_MATERIAL_NAME}{button[-1]}'
        hair_blend_node_name = f'{HAIR_MATERIAL_NAME}{button[-1]}_blend1'
        hair_blend_node = cmds.ls(hair_blend_node_name, type="blendColors")
        if not hair_blend_node:
            continue
        hair_blend_node = hair_blend_node[0]
        if button_name.startswith("gray"):
            color = [0.5, 0.5, 0.5]
        else:
            color = [x/255 for x in color]
        cmds.setAttr(
                    f"{hair_blend_node}.color2",
                    color[0], color[1], color[2],
                    type="double3"
                    )

def create_file_node(texture_file_path:str) -> str:
    """file node 作成

    Args:
        texture_file_path (str): テクスチャファイルパス

    Returns:
        str: file node name
    """
    texture_file_path = texture_file_path.replace(os.sep, '/')
    file_path, file_name = texture_file_path.rsplit("/", 1)
    node_name, ext = file_name.split(".", 1)
    file_node = cmds.shadingNode(
                                "file",
                                asTexture=True,
                                name=node_name,
                                skipSelect=True)

    cmds.setAttr(f'{file_node}.fileTextureName',
                    texture_file_path.replace(os.sep, '/'), type='string')
    return file_node

def file_node_exists(file_path:str) -> str:
    """ファイルノード存在確認

    Args:
        file_path (str): _description_

    Returns:
        str: _description_
    """
    just_node = ""
    file_path = Path(file_path.replace(os.sep, '/'))
    file_nodes = cmds.ls(type="file")
    for file_node in file_nodes:
        _path = Path(cmds.getAttr(f'{file_node}.fileTextureName').replace(os.sep, '/'))
        if _path.stem == file_path.stem:
            just_node = file_node
            break
    return just_node

def texture_file_name_check(file_path:str) -> bool:
    """ファイル名のサフィックス確認

    Args:
        file_path (str): _description_

    Returns:
        bool: _description_
    """
    check_suffix = "irda"
    check_flag = False
    file_path = file_path.replace(os.sep, '/')
    basename = file_path.rsplit("/", 1)[-1]
    basename = basename.split(".")[0]
    suffix = basename.rsplit("_", 1)[-1]

    if suffix == check_suffix:
        check_flag = True
    if not check_flag:
        gui_util.conform_dialog(title=TITLE, message="Suffixes are only accepted at [ _irda ]")
    return check_flag



