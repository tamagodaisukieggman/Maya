from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import xml.etree.ElementTree as ET
import os
from pathlib import Path
import shutil
import json
import threading
import yaml
import webbrowser
import xml.etree.ElementTree as ET

from PySide2 import QtCore
from maya import cmds
import maya.mel
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim

from ...utils import getCurrentSceneFilePath
from ...utils import gui_util
from ...utils.color_management import ColorManagement
from . import TOOL_NAME


HERE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "settings.yaml"
DELETE_LAYER_SETTING_FILE = r'C:\cygames\shrdev\shr\tools\in\ext\maya\2023\modules\shr\scripts\shr\file\maya_scene_checker\cheker_settings.yaml'


def open_help_site()->None:
    """ヘルプサイトを開く
    """
    _web_site = load_config('web_site')
    webbrowser.open(_web_site)

def conform_dialog(title='', message=''):
    """ダイアログ表示

    Args:
        title (str, optional): ウィンドウタイトル. Defaults to ''.
        message (str, optional): 表示メッセージ. Defaults to ''.
    """
    if not title:
        title=TOOL_NAME
    _d = gui_util.ConformDialog(title=title,
                    message=message)
    _d.exec_()
    print(message)

def show_message(message:str=''):
    if not message:
        return
    cmds.inViewMessage(assistMessage=f'{message}', position='midCenter', fade=True)
    print(f'{message}')

def load_config(config_name:str = '', config_file_path:str = ''):
    if not config_file_path:
        config_file_path:str = HERE / YAML_FILE_NAME
    with open(config_file_path, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    _confing_data = config.get(config_name, None)
    return _confing_data

def delete_display_layer():
    _config_path = DELETE_LAYER_SETTING_FILE
    NEED_LAYERS:list = load_config(config_name='NOT_DELETE_DISPLAY_LAYER', config_file_path=_config_path)
    DEFAULT_LAYER_NAME:str = load_config(config_name='DEFAULT_LAYER_NAME', config_file_path=_config_path)
    layers = [x for x in cmds.ls(type="displayLayer") if not x.startswith(DEFAULT_LAYER_NAME)]

    for layer in layers:
        if layer in NEED_LAYERS:
            continue
        try:
            cmds.delete(layer)
            print(f'delete layer: [ {layer} ]')
        except Exception as e:
            cmds.warning(f'could not delete display layer: [ {e} ]')

def parent_nodes(parent:str='', child:str='', rename_name:str='')->str:
    _result = ''
    if cmds.objExists(parent) and cmds.objExists(child):
        _result = cmds.parent(child, parent)[0]
        if rename_name:
            cmds.rename(_result, rename_name)
    if _result:
        print(f'Parent: [ {parent: <20} ] <- [ {child} ]')
    return _result

def get_presp_camera():
    """LOD 設定のためのカメラ取得

    Returns:
        _type_: _description_
    """
    _cam = cmds.ls("perspShape", type='camera')
    if _cam:
        return _cam[0]

def chenge_outliner_color(node:str=''):
    if not node:
        return
    default_node_flag:bool = False

    colors:dict = load_config('instalod_protect_color')
    default_metahuman_meshes:list = load_config('metahuman_default_meshes')

    for default_name in default_metahuman_meshes:
        if node.startswith(default_name):
            default_node_flag = True
            break

    if default_node_flag:
        cmds.setAttr(f'{node}.useOutlinerColor ', True)
        print(f'chenge outliner color: [ {node} ]')
        for color_attr, value  in colors.items():
            cmds.setAttr(f'{node}.{color_attr} ', value)
    else:
        cmds.setAttr(f'{node}.useOutlinerColor ', False)


def chenge_outliner_color_scene_all():
    meshes = cmds.ls(type='mesh', long=True)
    if not meshes:
        return
    for mesh in meshes:
        if cmds.getAttr(f"{mesh}.intermediateObject"):
            continue
        transform = cmds.listRelatives(mesh, parent=True, type='transform')
        if transform:
            transform:str = transform[0]
            if transform.endswith('lod0'):
                # print(transform)
                # print(mesh)
                chenge_outliner_color(node=transform)

def sort_outliner(root_node)->None:
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

def change_group_node(group_node_type:str='transform'):
    group_types:list = ['transform', 'lodGroup']
    outliner_order:list = []

    group_types.pop(group_types.index(group_node_type))
    current_group_type:str = group_types[0]

    mesh_group_node_name:str = load_config('lod_group_name')
    nodes:list = cmds.ls(mesh_group_node_name, type=current_group_type, long=True)

    if not nodes:
        cmds.warning(f'not found :[ {mesh_group_node_name} ]: node type: [ {current_group_type} ]')
        return

    if len(nodes) != 1:
        cmds.warning(f'found more one nodes :[ {mesh_group_node_name} ]: node type: [ {current_group_type} ]')
        return

    current_mesh_group_node:str = nodes[0]
    parent = cmds.listRelatives(current_mesh_group_node, parent=True, type='transform')
    if parent:
        outliner_order = cmds.listRelatives(parent, children=True, path=True, type='transform')

    inside_meshes:list = cmds.listRelatives(current_mesh_group_node, children=True, type='transform')
    print("inside_meshes -- ", inside_meshes)
    # cmds.select(clear=True)
    new_group = cmds.createNode(group_node_type, name=mesh_group_node_name, skipSelect=True)


    group_parent_visible_settings(node_type=group_node_type, lod_mesh_group=new_group, lod_groups=inside_meshes)
    cmds.delete(current_mesh_group_node)

    if parent:
        parent:str = parent[0]
        cmds.parent(new_group, parent)
        for _ in outliner_order:
            cmds.reorder(_, back=True)
    elif new_group != mesh_group_node_name:
        cmds.rename(new_group, mesh_group_node_name)



def setup_group_shown_settings(nodes:list=[]):
    if not nodes:
        return
    for i, node in enumerate(nodes):
        if i != 0:
            cmds.setAttr(f'{node}.visibility', False)
        else:
            cmds.setAttr(f'{node}.visibility', True)

def setup_lod_shown_settings(lod_mesh_group:str='', lod_groups:list=[]):
    # print('--setup lod shown settings')
    _base_range = 300
    _multiply = 100
    cmds.setAttr(f'{lod_mesh_group}.useScreenHeightPercentage', 0)
    for num, lod in enumerate(lod_groups):
        if cmds.objExists(lod):
            cmds.setAttr(f'{lod_mesh_group}.displayLevel[{num}]', 0)
            cmds.setAttr(f'{lod}.visibility', 1)
            cmds.setAttr(f'{lod_mesh_group}.threshold[{num}]', num*_multiply + _base_range)

def rig_rename(node:str=''):
    _rename = '|rig_grp'
    _result = ''
    if '|rig' == node:
        _result = cmds.rename(node, _rename)
    else:
        _result = node
    return _result

def get_character_id_from_scene()->str:
    character_id:str = ''
    scene_path:str = getCurrentSceneFilePath()
    if not scene_path:
        return character_id
    scene_path:Path = Path(scene_path)
    character_id = scene_path.stem
    return character_id

def lod_group_parent(lod_mesh_group:str='', lod_groups:list=''):
    _nodes = []
    for _node in lod_groups:
        print(_node, cmds.objExists(_node))
        _node = cmds.parent(_node, lod_mesh_group)[0]
        _nodes.append(_node)
    return _nodes

def remove_mesh_suffix(root_node:str=''):
    if not cmds.objExists(root_node):
        return
    _meshes = cmds.listRelatives(root_node, allDescendents=True, type='mesh')
    if not _meshes:
        return
    for _mesh in _meshes:
        if not cmds.objExists(_mesh):
            continue
        if cmds.getAttr(f"{_mesh}.intermediateObject"):
            continue
        _transform = cmds.listRelatives(_mesh, parent=True, type='transform')
        if _transform:
            _transform = _transform[0]
            if _transform.endswith('_mesh'):
                result = cmds.rename(_transform, _transform.rsplit('_', 1)[0])
                print(f'chenge name: [ {_transform: <20} ] -> [ {result} ]')

def visible_nodes():
    _flag = False
    for _node in load_config('visible_nodes'):
        if cmds.objExists(_node):
            cmds.setAttr(f'{_node}.v', 1)
            _flag = True
            print(f'visible node: [ {_node} ]')
    ColorManagement._enable_color_management()
    return _flag

def delete_nodes():
    _flag = False
    delete_nodes = load_config('delete_nodes')
    for delete_node in delete_nodes:
        if cmds.objExists(delete_node):
            cmds.delete(delete_node)
            print(f'delete node: [ {delete_node} ]')
            _flag = True
    return _flag

def spine04_parent():
    _parent_node = load_config('parent_nodes')['parent']
    _children_node =load_config('parent_nodes')['child']
    parent_nodes(child=_children_node, parent=_parent_node)
    # show_message('Visible Nodes & Delete Nodes & Parent Chenge')

def get_current_axis()->str:
    current_axis:str = cmds.upAxis(q=True, axis=True)
    print(f'current axis: [ {current_axis} ]')
    return current_axis

def set_up_displlay(change_to_axis:str='y', current_axis:str='z'):

    print(f'axis chenge: [ {current_axis} ] to [ {change_to_axis} ]')
    cmds.upAxis(axis=change_to_axis, rotateView=True)
    cmds.viewSet('|persp|perspShape', persp=True, animate=False)


def set_up_rotation():
    _rotate_nodes = load_config('Rotation_Nodes')
    for _node in _rotate_nodes:
        if cmds.objExists(_node):
            print(f'rotate -90: [ {_node} ]')
            cmds.setAttr(f'{_node}.rx', -90)

def remove_name_space():
    _flag = False
    cmds.namespace(setNamespace=':')
    all_name_spaces = [x for x in cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True) if x != "UI" and x != "shared"]
    if not all_name_spaces:
        return
    all_name_spaces.sort(key=len, reverse=True)
    for name_space in all_name_spaces:
        if cmds.namespace(exists=name_space):
            try:
                cmds.namespace(removeNamespace=name_space, mergeNamespaceWithRoot=True)
                print(f'remove name space: [ {name_space} ]')
                _flag = True
            except Exception as e:
                print(f'{name_space}: [ {e} ]')
    # if _flag:
    #     show_message('Remove Name Space')


def group_parent_visible_settings(node_type:str='transform', lod_mesh_group:str='', lod_groups:list=''):
    new_lod_groups = lod_group_parent(lod_mesh_group=lod_mesh_group, lod_groups=lod_groups)
    if node_type == 'lodGroup':
        _preps_cam = get_presp_camera()
        if _preps_cam:
            cmds.connectAttr(f'{_preps_cam}.worldMatrix', f'{lod_mesh_group}.cameraMatrix', force=True)

        setup_lod_shown_settings(lod_mesh_group=lod_mesh_group, lod_groups=new_lod_groups)
    else:
        setup_group_shown_settings(nodes=new_lod_groups)

def create_lodgroup(node_type:str='transform'):
    """メタヒューマンの「geometry_grp」を「mesh」という名前のLOD グループに変更
    self.lod_groups に格納
    デフォルトを「transform」ノードに変更
    「lodGroup」に
    """

    _lod_root_node:str = load_config('lod_root_node')
    if not cmds.objExists(_lod_root_node):
        cmds.warning(f'not exists: [ {_lod_root_node} ]')
        return
    lod_groups:list = cmds.listRelatives(_lod_root_node, children=True, fullPath=True, type='transform')

    if not lod_groups:
        cmds.warning(f'has no children: [ {_lod_root_node} ]')
        return

    remove_mesh_suffix(root_node=_lod_root_node)

    _lod_group_name:str = load_config('lod_group_name')

    lod_mesh_group:str = cmds.createNode(node_type, name=_lod_group_name, skipSelect=True)
    if not lod_mesh_group:
        return

    group_parent_visible_settings(node_type=node_type, lod_mesh_group=lod_mesh_group, lod_groups=lod_groups)
    # new_lod_groups = lod_group_parent(lod_mesh_group=lod_mesh_group, lod_groups=lod_groups)

    # if node_type == 'lodGroup':
    #     _preps_cam = get_presp_camera()
    #     if _preps_cam:
    #         cmds.connectAttr(f'{_preps_cam}.worldMatrix', f'{lod_mesh_group}.cameraMatrix', force=True)

    #     setup_lod_shown_settings(lod_mesh_group=lod_mesh_group, lod_groups=new_lod_groups)
    # else:
    #     setup_group_shown_settings(nodes=new_lod_groups)


def get_geometory_root_node()->str:
    lod_root_node:str = load_config('lod_root_node')
    _meshes:list = []
    lod_root_node:str = ''
    group_types:dict = load_config('group_type')
    if cmds.objExists(lod_root_node):
        _meshes = cmds.listRelatives(lod_root_node, allDescendents=True, type='mesh')
    if not _meshes:
        for node_type in group_types.values():
            lod_root_nodes:list = cmds.ls(load_config('lod_group_name'), type=node_type, long=True)
            if lod_root_nodes:
                lod_root_node = lod_root_nodes[0]
                break

    return lod_root_node


def lod_mesh_rename(lod_root_node:str=''):
    if not lod_root_node:
        lod_root_node = get_geometory_root_node()
    print("lod_root_node -- ", lod_root_node)
    if not cmds.objExists(lod_root_node):
        cmds.warning(f'not found lod root node: [ {lod_root_node} ]')
        return

    _meshes = cmds.listRelatives(lod_root_node, allDescendents=True, type='mesh')
    print("_meshes -- ", _meshes)

    if not _meshes:
        cmds.warning(f'not found lod group: [ {lod_root_node} ]')
        return

    for node in cmds.listRelatives(lod_root_node, allDescendents=True, type='transform', fullPath=True):
        _shepe = cmds.listRelatives(node, children=True, type='mesh', shapes=True, fullPath=True)
        if not _shepe:
            parent = cmds.listRelatives(node, parent=True, type='transform', fullPath=True)[0]
            if parent != lod_root_node:
                continue
            _name:str = node.rsplit('|', 1)[-1]
            if node.endswith('_grp'):
                _name:str = _name.rsplit('_grp')[0]
            if _name[-1].isdigit():
                cmds.rename(node, f'lod{_name[-1]}')
            else:
                cmds.rename(node, _name)
        elif node.endswith('_mesh'):
            cmds.rename(node, node.rsplit('|', 1)[-1].rsplit('_', 1)[0])


def lod_group_rename_selection():
    selections = cmds.ls('mesh', type='lodGroup', long=True)
    if not selections:
        cmds.warning('select [ mesh ] lod groupnode')
        return

    lod_root_node = selections[0]
    lod_mesh_rename(lod_root_node=lod_root_node)


def create_character_id_group(lod_mesh_group:str=''):
    character_id:str = get_character_id_from_scene()
    if not character_id:
        cmds.warning('Open Scene')
        return

    _exist_node = cmds.ls(character_id, type='transform')
    if _exist_node:
        cmds.warning(f'node exists: [ {_exist_node} ]')
        return
        # cmds.delete(_exist_node)
        # for _ex_node in _exist_node:
        #     cmds.rename(_ex_node, f'{_ex_node}_old')

    lod_mesh_rename()
    _nodes:list = load_config('charactor_nodes')
    not_exists:list = []

    for _node in _nodes:
        if not cmds.objExists(_node):
            not_exists.append(_node)
        if lod_mesh_group and cmds.objExists(lod_mesh_group):
            _nodes.append(lod_mesh_group)

    if not_exists:
        _m = ','.join(not_exists)
        cmds.warning(f'These nodes must be in the root hierarchy: [ {_m} ]')
        return

    _nodes = [rig_rename(node=x) for x in _nodes]
    _character_group_node = cmds.createNode('transform', name=f'{character_id}', skipSelect=True)

    for node in _nodes:
        parent_nodes(parent=_character_group_node, child=node)
    # show_message('Create Character ID Group')

def show_head_display_layers():
    _flag = False
    delete_display_layer()
    for _layer in load_config('display_layers'):
        if cmds.objExists(_layer):
            cmds.setAttr(f'{_layer}.v', 1)
            _flag = True
    ColorManagement._enable_color_management()
    # if _flag:
    #     show_message('Show Display Layer')



class SetupFacialScene:
    def __init__(self):
        self.not_exists_node:list = []
        self.lod_mesh_group:str = ''
        self.lod_groups:list = []
        self.charactor_id:str = ''
        self.get_character_id_from_scene()
        ColorManagement._enable_color_management()

    def check_scene(self):
        if not self.charactor_id:
            return
        else:
            return True

    def get_character_id_from_scene(self):
        scene_path:str = getCurrentSceneFilePath()
        if not scene_path:
            return
        scene_path:Path = Path(scene_path)
        self.charactor_id:str = scene_path.stem
        # cmds.select(clear=True)

    def get_presp_camera(self):
        """LOD 設定のためのカメラ取得

        Returns:
            _type_: _description_
        """
        _cam = cmds.ls("perspShape", type='camera')
        if _cam:
            return _cam[0]

    def node_exists_check(self):
        for _node in load_config('need_nodes'):
            if not cmds.objExists(_node):
                self.not_exists_node.append(_node)
        return self.not_exists_node

    def visible_nodes(self):
        """非表示になっているノードを表示
        """
        # print('---visibility chenge')
        for _node in load_config('visible_nodes'):
            # print(f'[ {_node} ] visible')
            cmds.setAttr(f'{_node}.v', 1)

    def delete_nodes(self):
        """不要なノード削除
        """
        _nodes = load_config('delete_nodes')
        # print('---delete node')
        cmds.delete(_nodes)
        # for node in _nodes:
        #     if cmds.objExists(node):
        #         try:
        #             cmds.delete(node)
        #             print(f'[ {node} ] delete')
        #         except Exception as e:
        #             print(e)

    def parent_nodes(self, parent:str='', child:str='', rename_name:str='')->str:
        # print('---parent node')
        _result = ''
        if cmds.objExists(parent) and cmds.objExists(child):
            _result = cmds.parent(child, parent)[0]
            # print(f'parent: [ {child} ] to [ {parent} ]')
            if rename_name:
                cmds.rename(_result, rename_name)
                # print(f'rename: [ {_result} ] to [ {rename_name} ]')
        return _result

    def spine04_parent(self):
        _parent_node = load_config('parent_nodes')['parent']
        _children_node =load_config('parent_nodes')['child']
        self.parent_nodes(child=_children_node, parent=_parent_node)

    def create_lodgroup_select_mode(self):
        _geometory_grp_name = load_config('lod_root_node')
        cmds.select(_geometory_grp_name, replace=True)
        self.create_lodgroup_from_selection()


    def create_lodgroup_from_selection(self):
        selections = cmds.ls(selection=True, type='transform', long=True)

        if not selections:
            _d = gui_util.ConformDialog(title="Select Transform Node",
                                        message="Select Transform Node")
            _d.exec_()
            return

        if len(selections) != 1:
            _d = gui_util.ConformDialog(title="Select One Transform Node",
                                        message="Lod Select the parent you want to group")
            _d.exec_()
            return

        self.lod_groups = cmds.listRelatives(selections[0], children=True, fullPath=True, type='transform')
        _parent = cmds.listRelatives(self.lod_groups, parent=True, fullPath=True, type='transform')[0]
        self.lod_mesh_group = cmds.createNode("lodGroup", name=load_config('lod_group_name'), skipSelect=True)
        cmds.select(clear=True)
        self.lod_group_parent()
        cmds.delete(selections)

        _preps_cam = self.get_presp_camera()

        if _preps_cam:
            cmds.connectAttr(f'{_preps_cam}.worldMatrix', f'{self.lod_mesh_group}.cameraMatrix', force=True)

        self.setup_lod_shown_settings()
        self.parent_nodes(parent=_parent, child=self.lod_mesh_group)

        _preps_cam = self.get_presp_camera()

        if _preps_cam:
            cmds.connectAttr(f'{_preps_cam}.worldMatrix', f'{self.lod_mesh_group}.cameraMatrix', force=True)

        self.setup_lod_shown_settings()
        self.parent_nodes(parent=load_config('head_grp'), child=self.lod_mesh_group)


    def create_lodgroup_mel(self):
        _lod_group_default_name:str = 'LOD_Group_'
        _lod_group_name:str = load_config('lod_group_name')
        _lod_root_node:str = load_config('lod_root_node')

        # remove_mesh_suffix(root_node=_lod_root_node)
        # cmds.select(clear=True)
        maya.mel.eval('LevelOfDetailGroup;')
        lod_group_node = cmds.ls(selection=True)[0]
        cmds.select(clear=True)
        # lod_group_node = cmds.ls(f'{_lod_group_default_name}*', type='lodGroup')
        # print(lod_group_node)
        _result = cmds.rename(lod_group_node, 'mesh')

        self.lod_mesh_group = _result
        self.lod_group_parent()
        # _preps_cam = self.get_presp_camera()

        # if _preps_cam:
        #     cmds.connectAttr(f'{_preps_cam}.worldMatrix', f'{self.lod_mesh_group}.cameraMatrix', force=True)
        self.setup_lod_shown_settings()
        # self.parent_nodes(parent=load_config('head_grp'), child=self.lod_mesh_group)


    def create_lodgroup(self):
        """メタヒューマンの「geometry_grp」を「mesh」という名前のLOD グループに変更
        self.lod_groups に格納
        """
        # print('-- create lodgroup')
        _lod_root_node:str = load_config('lod_root_node')
        lod_mesh_rename(lod_root_node=_lod_root_node)
        # remove_mesh_suffix(root_node=_lod_root_node)
        self.lod_groups:list = cmds.listRelatives(_lod_root_node, children=True, fullPath=True, type='transform')

        if not self.lod_groups:
            return

        _lod_group_name:str = load_config('lod_group_name')
        self.lod_mesh_group:str = cmds.createNode("lodGroup", name=_lod_group_name, skipSelect=True)
        # cmds.select(clear=True)
        # self.lod_mesh_group = cmds.ls(self.lod_mesh_group, long=True)[0]
        # for x in self.lod_groups:
        #     print(x)
        # print(f'create lod group node: [ {self.lod_mesh_group} ]')

        self.lod_group_parent()

        _preps_cam = self.get_presp_camera()
        if _preps_cam:
            cmds.connectAttr(f'{_preps_cam}.worldMatrix', f'{self.lod_mesh_group}.cameraMatrix', force=True)
        self.setup_lod_shown_settings()

        # self.parent_nodes(parent=load_config('head_grp'), child=self.lod_mesh_group)

    def lod_group_parent(self):
        # print('lod group parent')
        _nodes = []
        for _node in self.lod_groups:
            # print(f'parent node: [ {_node} ]')
            # _node = self.parent_nodes(parent=self.lod_mesh_group, child=_node)
            _node = cmds.parent(_node, self.lod_mesh_group)[0]
            # print(f'lod group parent: [{_node}] to [{self.lod_mesh_group}]')
            _nodes.append(_node)
        self.lod_groups = _nodes

    def setup_lod_shown_settings(self):
        # print('--setup lod shown settings')
        _base_range = 300
        _multiply = 100
        cmds.setAttr(f'{self.lod_mesh_group}.useScreenHeightPercentage', 0)
        for num, lod in enumerate(self.lod_groups):
            if cmds.objExists(lod):
                cmds.setAttr(f'{self.lod_mesh_group}.displayLevel[{num}]', 0)
                cmds.setAttr(f'{lod}.visibility', 1)
                cmds.setAttr(f'{self.lod_mesh_group}.threshold[{num}]', num*_multiply + _base_range)

    def show_head_display_layers(self):
        for _layer in load_config('display_layers'):
            if cmds.objExists(_layer):
                cmds.setAttr(f'{_layer}.v', 1)

    def rig_rename(self, node:str=''):
        _rename = '|rig_grp'
        _result = ''
        if '|rig' == node:
            _result = cmds.rename(node, _rename)
        else:
            _result = node
        return _result

    def create_character_id_group(self):
        # print('--create character id group')
        _nodes:list = load_config('charactor_nodes')
        not_exists:list = []

        for _node in _nodes:
            if not cmds.objExists(_node):
                not_exists.append(_node)
            if self.lod_mesh_group and cmds.objExists(self.lod_mesh_group):
                _nodes.append(self.lod_mesh_group)

        if not_exists:
            _m = ','.join(not_exists)
            cmds.error(f'[ {_m} ] node not exists')
            return

        _nodes = [self.rig_rename(node=x) for x in _nodes]
        _character_group_node = cmds.createNode('transform', name=f'{self.charactor_id}', skipSelect=True)
        # cmds.select(clear=True)
        print(f'create id group: [ {_character_group_node} ]')

        for node in _nodes:
            self.parent_nodes(parent=_character_group_node, child=node)

    @classmethod
    def select_export_nodes(self):
        nodes = []
        for node in load_config('export_selection_nodes'):
            if cmds.objExists(node):
                nodes.append(node)
        if nodes:
            cmds.select(nodes, replace=True)
        return nodes


class ThredingFileCopy:
    def __init__(self, src_path:Path=Path(), dst_path:Path=Path()):
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
        _thread = threading.Thread(target=copy_tree, args=(self.src_path, self.dst_path))
        _thread.start()
        _next = 1
        _current = 0
        _end = get_directory_size(path=self.src_path)

        _all = range(100)
        _length = len(_all)
        prg = gui_util.ProgressDialog()
        prg.setUp(_length, "copy files ... ")
        prg.show()

        for i in _all:
            QtCore.QCoreApplication.processEvents()
            while(_next > _current) :
                _current = round(get_directory_size(path=self.dst_path)/_end*100)
            if prg.wasCanceled():
                break
            _next = _current + 1
            prg.setValue(_current)
            prg.step(_current)
            if _next > _length:
                break
        _thread.join()


class MetahumanJointReConnections:
    def __init__(self):
        self.root_node:str = ''
        self.body_model_path:str = ''
        self.body_root_node:str = ''
        # joint: [source_attribute_list, target_attribute_list]
        self.joints_connections:dict = {}
        self.mesh_connection_data:dict = {}
        # self.get_root_node()

    def get_root_node_chara(self)->None:
        # scene_name, root_node = get_shenron_nodes()
        geometory_group_node = load_config('lod_root_node')
        print("root_node ---------- ", geometory_group_node)
        # if not scene_name or not root_node:
        #     return
        self.root_node:str = geometory_group_node
        self.root_joints:list = ['|root', '|root_drv']

    def get_root_node_facial(self)->None:
        scene_name, root_node = get_shenron_nodes()
        self.root_node:str = root_node
        self.root_joints:list = [f'{self.root_node}|root', f'{self.root_node}|root_drv']

    def get_root_node(self)->None:
        # scene_name, root_node = get_shenron_nodes()
        geometory_group_node = load_config('lod_root_node')
        print("root_node ---------- ", geometory_group_node)
        # if not scene_name or not root_node:
        #     return
        self.root_node:str = geometory_group_node

    def un_bind(self, body_model_path:str='')->None:
        if not self.root_node:
            return

        body_model_path:Path = Path(body_model_path)
        file_name:str = body_model_path.stem
        body_root_node_name:str = file_name.split("_", 1)[-1]
        self.body_model_path = str(body_model_path)

        body_root_node:list = cmds.ls(body_root_node_name, type='transform')
        if not body_root_node:
            cmds.warning(f'not found body root node: [ {body_root_node_name} ]')
            return
        if len(body_root_node) != 1:
            cmds.warning(f'More than one exists: [ {body_root_node_name} ]  [ {body_root_node} ]')
            return

        self.body_root_node = body_root_node[0]
        is_done = un_bind(root_node=self.root_node)
        if body_root_node:
            is_done = un_bind(root_node=self.body_root_node)
        print(f'unbind: [ {self.root_node} ]')

    def delete_history_reconneciotns_from_selection_deep(self):
        if not self.root_node:
            return
        cmds.select(self.root_node, replace=True)
        self.mesh_connection_data = delete_history_reconneciotns_from_selection_deep()
        cmds.select(clear=True)
        print('delete_history_reconneciotns_from_selection_deep ----')

    def reconnection_memory_data(self):
        if not self.mesh_connection_data:
            return
        cmds.select(self.root_node, replace=True)
        reconnection_memory_data(mesh_connection_data = self.mesh_connection_data)
        cmds.select(clear=True)

    def un_bind_chara(self, body_model_path:str='')->None:

        if self.root_node:
            is_done = un_bind(root_node = self.root_node)
            print(f'unbind: [ {self.root_node} ]')


    def re_bind_chara(self):
        # self.get_root_node()
        self.root_node = '|pfc1020|mesh'
        # if not self.root_node:
        #     return

        geometory_node:str = self.root_node

        # if not geometory_node:
        #     cmds.warning(f'not found geometory node: [ {self.root_node} ]')
        #     return
        # if len(geometory_node) != 1:
        #     cmds.warning(f'Multiple Existence: [ {self.root_node} ]')
        #     return

        # geometory_node:str = geometory_node[0]

        lod_groups:list = cmds.listRelatives(geometory_node, children=True, type='transform', fullPath=True)

        _weitht_import = ImportSkinWeight()
        _weitht_import.apply_metahuman_weights(lod_groups=lod_groups)

    def disconnect_attribute_joint(self):
        # target:str = '|root'
        # self.root_node = target
        targets:list = self.root_joints
        for target in targets:
            if not cmds.objExists(target):
                continue
            # print(f'disconnect_attribute {target}------------------')
            joints:list = [target]
            joints.extend(cmds.listRelatives(target, allDescendents=True, type='joint', fullPath=True))
            for i,joint in enumerate(joints):
                _con = cmds.listConnections(joint, connections=True, plugs=True, destination=False, fullNodeName=True)

                if not _con:
                    continue

                _target = _con[0::2]
                _source = _con[1::2]

                self.joints_connections[joint] = zip(_source, _target)
                for t,s in zip(_target, _source):
                    cmds.disconnectAttr(s, t)
                    # print(f'disconnect: {s}, {t}')

        # print(f'disconnect attribute: [ {self.root_node} ]')

    def connect_attribute_joint(self):
        targets:list = self.root_joints
        print('connect_attribute ----------------------')

        if not self.joints_connections:
            return

        for joint, attributes in self.joints_connections.items():
            # if not cmds.objExists(joint):
            #     continue
            for source_attirubute, target_attribute in attributes:

                if not cmds.objExists(source_attirubute) and not cmds.objExists(target_attribute):
                    continue

                cmds.connectAttr(source_attirubute, target_attribute, force=True)
                # print(f're connect: {source_attirubute}, {target_attribute}')

        print(f'connect attribute: [ {self.joints_connections} ]')

    def rotation_geometory(self):
        node_name:str = '|rig|head_grp|geometry_grp'
        if cmds.objExists(node_name):
            cmds.setAttr(f'{node_name}.rx', -90)

    def freeze_transform_joint(self):
        # geometory_grp:str = self.root_node
        # targets:list = ['|root', '|root_drv', geometory_grp]
        targets:list = self.root_joints + self.root_node
        # print('freeze_transform_joint -----------------')
        for target in targets:
            if not cmds.objExists(target):
                continue
            try:
                # print('freeze target ------- ', target)
                cmds.makeIdentity(target, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
            except Exception as e:
                print(e)

    def delete_history_chara(self):
        geometory_grp:str = '|rig|head_grp|geometry_grp'
        if cmds.objExists(geometory_grp):
            nodes = cmds.listRelatives(geometory_grp, allDescendents=True, type='transform', fullPath=True)
            if nodes:
                for target in  nodes:
                    cmds.delete(target, constructionHistory=True)


    def disconnect_attribute(self):
        print('disconnect_attribute ------------------')
        if not self.root_node or not self.body_root_node:
            return

        joints:list = cmds.listRelatives(self.root_node, allDescendents=True, type='joint', fullPath=True)
        for i,joint in enumerate(joints):
            _con = cmds.listConnections(joint, connections=True, plugs=True, destination=False)

            if not _con:
                continue

            _target = _con[0::2]
            _source = _con[1::2]

            self.joints_connections[joint] = zip(_source, _target)
            for t,s in zip(_target, _source):
                cmds.disconnectAttr(s, t)

        print(f'disconnect attribute: [ {self.root_node} ]')

    def freeze_transform_joint(self):
        print('freeze_transform_joint -----------------')
        if not self.root_node and not self.body_root_node:
            return

        for joint in self.joints_connections.keys():
            if not cmds.objExists(joint):
                continue
            # print(joint, " --- freeze")
            cmds.makeIdentity(joint, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
        try:
            cmds.makeIdentity(self.root_node, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
        except Exception as e:
            print(e)
        try:
            # print(self.body_root_node, " --- freeze")
            cmds.makeIdentity(self.body_root_node, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
        except Exception as e:
            print(e)
        print(f'freeze transform: [ {self.root_node} ]')

    def delete_history(self):
        if not self.root_node:
            return
        for node in cmds.listRelatives(self.root_node, allDescendents=True, type='mesh', fullPath=True):
            try:
                cmds.delete(node, channels=True)
                print(node)
            except Exception as e:
                print(e)

    def connect_attribute(self):
        print('connect_attribute ----------------------')
        if not self.root_node and not self.body_root_node and self.joints_connections:
            return

        for joint, attributes in self.joints_connections.items():
            # if not cmds.objExists(joint):
            #     continue
            for source_attirubute, target_attribute in attributes:

                if not cmds.objExists(source_attirubute) and not cmds.objExists(target_attribute):
                    continue

                cmds.connectAttr(source_attirubute, target_attribute, force=True)

        print(f'connect attribute: [ {self.root_node} ]')

    def reparent_nodes(self):
        print('reparent_nodes --------------------------')
        if not self.root_node and not self.body_root_node:
            return
        re_parent_ndoes()
        print(f're parent nodes: [ {self.root_node} ]')

    def delete_node_facial(self):
        print('delete_node_facial --------------------')
        if not self.root_node and not self.body_root_node:
            return
        delete_nodes_facial(body_model_path=str(self.body_model_path))
        print(f'delete nodes: [ {self.root_node} ]')

    def import_metahuman_weight(self):
        print('import_metahuman_weight --------------------')
        if not self.root_node and not self.body_root_node:
            return
        import_metahuman_weight()
        print(f'import shenron weights: [ {self.root_node} ]')


def get_name_from_json(json_path:Path=Path())->str:
    if not json_path.exists():
        return
    if not json_path.suffix == ".json":
        return
    json_open = open(str(json_path), 'r')
    json_load = json.load(json_open)
    return json_load.get('name', None)


def chenge_light_modelPanel4(display_light:str='all'):
    cmds.modelEditor(
                    'modelPanel4',
                    edit=True,
                    displayAppearance='smoothShaded',
                    displayTextures=True,
                    displayLights=display_light
                    )


def set_current_character_path()->None:
    common_file_path = Path(load_config('Common_file_path'))
    file_replace(local_path=common_file_path)

def rename_shaders(charactor_id='')->None:
    # シェーダ名をshenron 仕様に変更

    if not charactor_id:
        cmds.warning('Need Character ID')
        return
    shaders = cmds.ls(materials=True)

    if not shaders:
        cmds.warning('Not Found Materials')
        return

    metahuman_material_name_type:dict = load_config('materials')
    character_name = charactor_id.rsplit('_', 1)[0]

    for shader in shaders:
        shader_type = cmds.nodeType(shader)
        if shader in metahuman_material_name_type.keys():
            metahuman_shader_type = metahuman_material_name_type.get(shader)
            if metahuman_shader_type == shader_type:
                name_split = shader.split('_')
                if len(name_split) != 1:
                    parts_name = name_split[1]
                    new_shader_name = f'mi_{character_name}_{parts_name}'.lower()
                    _new_material = cmds.rename(shader, new_shader_name)

def rename_shenron_material_to_lower()->None:
    shaders = cmds.ls(materials=True)
    if not shaders:
        return
    for shader in shaders:
        if shader.startswith('mi_'):
            cmds.rename(shader, shader.lower())

def file_replace(local_path:Path=Path(), shader=True)->None:
    if not local_path.exists():
        return
    _files = cmds.ls(type="file")
    if not _files:
        return
    change_path = {}
    _basename_filepath = dict([x.stem, x] for x in local_path.glob("**/*")if x.is_file())
    for _f in _files:
        _path = Path(cmds.getAttr(f'{_f}.ftn'))
        _bn = _path.stem
        local_path = _basename_filepath.get(_bn)
        if local_path and _path != local_path:
            local_path = str(local_path).replace(os.sep, '/')
            cmds.setAttr(f'{_f}.ftn', local_path, type="string")
            change_path[_f] = local_path

    if shader:
        _shaders = cmds.ls(materials=True)
        for x in _shaders:
            if not "shader" in cmds.listAttr(x):
                continue
            _s_path = Path(cmds.getAttr(f'{x}.shader'))
            _f = _basename_filepath.get(_s_path.stem)
            if _f and _s_path != _f:
                cmds.setAttr(f'{x}.shader', _f, type="string")
                change_path[x] = str(_f).replace(os.sep, '/')

    if change_path:
        _m = f'Replace [ {len(change_path)} ] File(s)'
    else:
        _m = 'Not File Path Chenge'

    _d = gui_util.ConformDialog(title="Chenge File Path",
                                message=_m)
    _d.exec_()

def check_joint_exists(joints:list=[])->list:
    _no_exists_joints = []
    for joint in joints:
        if not cmds.objExists(joint):
            _no_exists_joints.append(joint)

    return _no_exists_joints


def texture_file_replace(dst_path:Path=None, character_id:str='')->Path:
    if not character_id:
        return

    files:list = cmds.ls(type='file')

    if not files:
        return
    Original_Texture_Names:list = load_config('Original_Texture_Names')
    Project_Texture_Names:list = load_config('Project_Texture_Names')
    dst_path = dst_path / 'texture'
    create_directory_tree(path=dst_path)

    for file in files:
        path = Path(cmds.getAttr(f'{file}.ftn'))
        namebase = path.stem
        new_namebase = Project_Texture_Names.get(namebase)
        if new_namebase:
            new_namebase = new_namebase.replace('ID', character_id)
            new_path = dst_path / f'{new_namebase}.tga'
            shutil.copy(str(path), str(new_path))
            if new_path.exists():
                cmds.setAttr(f'{file}.ftn', str(new_path), type="string")
    return dst_path

def rotation_reset():
    _rotate_nodes = load_config('Rotation_Nodes')
    for _node in _rotate_nodes:
        if cmds.objExists(_node):
            cmds.setAttr(f'{_node}.rx', 0)



def save_maya_scene(scene_path:Path=None):
    cmds.file(save=True, force=True)

def change_dna_filepath(rl4Embedded_nodename:str='', dna_file_path:str=''):
    print('node name --- ', rl4Embedded_nodename)
    print('dna file path --- ', dna_file_path)
    cmds.setAttr(f'{rl4Embedded_nodename}.dnaFilePath', dna_file_path ,type="string")

def set_up_maya_scene(scene_path:Path=Path(), dst_path:Path=Path(), character_id:str='')->None:
    # _maya_file = list(path.glob('**/*.mb'))
    if not character_id:
        return

    if scene_path.exists():
        # _maya_file = _maya_file[0]
        dna_file_path = scene_path.parent
        dna_file_path = dna_file_path / f'{character_id}_rl.dna'
        cmds.file(str(scene_path), open=True, ignoreVersion=True, type='mayaBinary', options='v=0;', force=True)
        common_file_path = Path(load_config('Common_file_path'))
        file_replace(local_path=common_file_path)

        rl4Embedded_node = cmds.ls(f'rl4Embedded_{character_id}_rl')
        print('character_id -- ', character_id)
        print('rl4Embedded_node  - ', rl4Embedded_node)

        if not rl4Embedded_node:
            return
        rl4Embedded_node = rl4Embedded_node[0]
        print(cmds.attributeQuery('dnaFilePath', node=rl4Embedded_node, exists=True))
        if not cmds.attributeQuery('dnaFilePath', node=rl4Embedded_node, exists=True):
            return

        change_dna_filepath(rl4Embedded_nodename=rl4Embedded_node, dna_file_path=str(dna_file_path))
        # set_up_displlay(axis='z')
        # set_up_rotation()
        # dst_path = texture_file_replace(dst_path=dst_path, character_id=character_id)
        # file_replace(local_path=dst_path, shader=False)
        chenge_light_modelPanel4(display_light='all')
        ColorManagement._enable_color_management()


def get_directory_size(path:Path=Path())->int:
    total_size = 0
    path = str(path)
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total_size += entry.stat().st_size
            elif entry.is_dir():
                total_size += get_directory_size(entry.path)
    return total_size

def check_and_create_work_directory(work_directory:Path=Path()):
    # print(work_directory, work_directory.exists())
    # if not work_directory.exists():
    #     return
    work_directory = work_directory / 'work' / 'maya'
    print(str(work_directory))

def create_directory_tree(path:Path=None):
    if not path:
        return
    path = Path(path)
    os.makedirs(str(path), exist_ok=True)

def copy_scene_file(src_path:Path=None, dst_path:Path=None, new_scene_name:str=''):
    chancel_flag = False
    _result = None
    if not src_path or not dst_path or not new_scene_name:
        return _result

    dst_directory = dst_path / 'work' / 'maya'
    create_directory_tree(dst_directory)

    new_dst_path = dst_directory / f'{new_scene_name}.mb'
    new_dst_dna_path = dst_directory / f'{new_scene_name}.dna'
    new_dst_dna_rl_path = dst_directory / f'{new_scene_name}_rl.dna'
    print('new_dst_dna_path -- ', new_dst_dna_path)
    print('new_dst_dna_rl_path -- ', new_dst_dna_rl_path)
    if new_dst_path.exists():
        _m = str(new_dst_path).replace(os.sep, '/')
        _m += '\n\nAlready there'
        _m += '\nRemove Old?'
        _d = gui_util.ConformDialogResult(title='Remove Old?', message=_m)
        result = _d.exec_()

        if not result:
            return _result
        else:
            try:
                new_dst_path.unlink()
            except Exception as e:
                chancel_flag = True
                print(e)

    if chancel_flag:
        return _result

    _maya_file = list(src_path.glob('**/*_full_rig.mb'))
    _dna_rl_file = list(src_path.glob('**/*_rl.dna'))
    _dna_file = [x for x in list(src_path.glob('**/*.dna'))if not str(x).endswith('_rl.dna')]
    print(src_path)
    print('_dna_rl_file -- ', _dna_rl_file)
    print('_dna_file -- ', _dna_file)

    if not _maya_file:
        return _result
    src_path = _maya_file[0]

    if _dna_rl_file:
        shutil.copy(str(_dna_rl_file[0]), str(new_dst_dna_rl_path))

    if _dna_file:
        shutil.copy(str(_dna_file[0]), str(new_dst_dna_path))

    _result = Path(shutil.copy(str(src_path), str(new_dst_path)))
    print(_result)
    return _result


def copy_tree(src_path:Path=Path(), dst_path:Path=Path())->str:
    result = ''
    try:
        result = shutil.copytree(str(src_path), str(dst_path))
    except Exception as e:
        print(e)
    return result

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
    # _file_copy = ThredingFileCopy(src_path=src_path, dst_path=dst_path)
    # _file_copy.calculate()
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

def import_scene_file(file_path:str=''):
    file_path:Path = Path(file_path)
    ext = file_path.suffix
    file_type = load_config('Import_File_Type').get(ext)
    if not file_type:
        cmds.warning(f'Unknown File Type: [ {ext} ]')
        return
    cmds.file(
            str(file_path).replace(os.sep, '/'),
            i=True,
            type=file_type,
            ignoreVersion=True,
            renameAll=True,
            mergeNamespacesOnClash=True,
            preserveReferences=True,
            importTimeRange="combine",
            )

def fbx_import(fbx_file_path:str='')->list:
    _result:list = cmds.file(
            fbx_file_path,
            i=True,
            type="FBX",
            ignoreVersion=True,
            renameAll=True,
            mergeNamespacesOnClash=True,
            preserveReferences=True,
            importTimeRange="combine",
            )
    return _result



def fbx_import_apply_name_space(name_space:str='', fbx_file_path:str='')->list:
    if not fbx_file_path:
        return
    current_name_space = cmds.namespaceInfo(currentNamespace=True)

    if not cmds.namespace(exists=f':{name_space}'):
        cmds.namespace(addNamespace=f':{name_space}')

    cmds.namespace(setNamespace=f':{name_space}')
    _result:list = cmds.file(
            fbx_file_path,
            i=True,
            type="FBX",
            ignoreVersion=True,
            renameAll=True,
            mergeNamespacesOnClash=True,
            preserveReferences=True,
            importTimeRange="combine",
            namespace=name_space
            )

    cmds.namespace(setNamespace=current_name_space)
    return _result

def import_body_model(file_path:str='', name_space:str='')->list:
    file_path:Path = Path(file_path)
    if not file_path and str(file_path) != '.':
        return
    # if file_path.suffix != '.fbx':
    #     return
    file_path = str(file_path).replace(os.sep, '/')

    if name_space:
        _imports:list = fbx_import_apply_name_space(name_space=name_space, fbx_file_path=file_path)
    else:
        _imports:list = fbx_import(fbx_file_path=file_path)
    # import_scene_file(file_path=file_path)
    print(_imports)
    return _imports

def get_skin_cluster(node: str) -> str:
    """スキンクラスタの存在確認

    Args:
        node (str): メッシュノード

    Returns:
        str: スキンクラスタノード
    """

    skin_cluster = ""
    if cmds.objExists(node):
        _historys = cmds.listHistory(node)
        if _historys:
            for _history in _historys:
                if cmds.nodeType(_history) == "skinCluster":
                    skin_cluster = _history
                    break
    return skin_cluster

def load_weight_file_cmds(shape= "",
                        import_path="",
                        file_name="",
                        deformer="",
                        method="index",
                        remap=""):
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
    # print("remap ---- ", remap)
    # print(f"{remap}:(.*);$1")
    # print("shape -- ", shape)
    # print("import_path  ^^^ ", import_path)
    # print("method ^-- ", method)

    # if remap:
    #     remap = f"{remap}:(.*);$1"
    # try:
    cmds.deformerWeights(
                        file_name,
                        im = True,
                        shape = shape,
                        # deformer = deformer,
                        path = import_path,
                        method = method,
                        # weightPrecision = 10,
                        defaultValue = 0.0,
                        ignoreName = False,
                        # vertexConnections=True,
                        # worldSpace=True,
                        # remap=remap
                        # positionTolerance=0.1
                        )
    # except Exception as e:
    #     cmds.warning(f'Could not import: {e}')



def get_weight_file_jointsdict(weight_directory:str='Metahuman'):
    if weight_directory == 'Metahuman':
        _weight_path:Path = Path(load_config('Metahuman_Weight_Filepath'))
    else:
        _weight_path:Path = Path(load_config('Shenron_weight_Filepath'))

    file_name_joint_dict:dict = {}
    file_name_file_path_dict:dict = {}

    if not _weight_path.exists():
        cmds.warning('not found weight data')
        return file_name_joint_dict, file_name_file_path_dict

    _weight_files = list(_weight_path.glob('*xml'))
    _length = len(_weight_files)
    with gui_util.ProgressDialog(title='Check Weight File ...', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, _file in enumerate(_weight_path.glob('*xml')):
            if prg.wasCanceled():
                break
            prg.setValue(i)
            prg.step(i)
            prg.setLabelText(f'check file: [ {_file.stem} ]')
            # print(f'check weight file: [ {_file.stem} ]')

            result_joints:list = []
            file_name = _file.stem
            file_name = file_name.rsplit('__', 1)[-1]

            tree = ET.parse(_file)
            root = tree.getroot()
            joints = [x.attrib.get('source') for x in root]

            if joints:
                for joint in joints:
                    if joint and cmds.objExists(joint):
                        result_joints.append(joint)

            file_name_joint_dict[file_name] = result_joints
            file_name_file_path_dict[file_name] = _file

    return file_name_joint_dict, file_name_file_path_dict

def get_shenron_nodes()->str:
    root_node_name:str = ''
    scene_name = str(getCurrentSceneFilePath())
    if not scene_name:
        cmds.warning('Scene Not Open')
        return scene_name, root_node_name
    scene_name = Path(scene_name)
    if not scene_name.exists():
        cmds.warning('Scene Not Exosts')
        return scene_name, root_node_name
    root_node_name = scene_name.stem.split('_')[0]
    # root_node_name = f'|{root_node_name}'
    root_nodes = cmds.ls(assemblies=True)
    if root_node_name not in root_nodes:
        cmds.warning(f'Not Found RootNode: [ {root_node_name} ]')
        root_node_name = ''
    return scene_name, root_node_name

def check_nodes():
    scene_name, root_node = get_shenron_nodes()
    print(f'scene name: [ {scene_name} ]')
    print(f'root node: [ {root_node} ]')
    lod_groups:list = []

    if not scene_name or not root_node:
        return scene_name, root_node, lod_groups

    shenron_lod_grps:list = load_config('Mesh_Groups')
    print(f'target lod group: [{shenron_lod_grps}]')
    for group_name in shenron_lod_grps:
        _full_path_name = f'|{root_node}|mesh|{group_name}'
        if cmds.objExists(_full_path_name):
            lod_groups.append(_full_path_name)

    # children = cmds.listRelatives(root_node, children=True, type='transform', fullPath=True)
    # print(f'root node children: [{children}]')
    # if not children:
    #     cmds.warning(f'No children: [ {root_node} ]')
    #     return scene_name, root_node, lod_groups

    # for cld in children:
    #     second_gen = cmds.listRelatives(cld, children=True, type='transform', fullPath=True)
    #     if not second_gen:
    #         continue
    #     for sec in second_gen:
    #         if sec.split('|')[-1] in shenron_lod_grps:
    #         lod_groups.append(cld)
    print(f'lod groups: [ {lod_groups} ]')
    if len(shenron_lod_grps) < len(lod_groups):
        for x in shenron_lod_grps:
            print(f'scene LOD: {x}')

        for x in lod_groups:
            print(f'need LOD: {x}')
        cmds.warning(f'LOD Count Error: sceneLOD: [ {len(shenron_lod_grps)} ] Need LOD Length: [ {len(lod_groups)} ]')
        return scene_name, root_node, lod_groups
    return scene_name, root_node, lod_groups

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

def unbind_hierarchy_skin(root_node:str)->None:

    if not root_node:
        return

    meshes = cmds.listRelatives(root_node, children=True, type="mesh", fullPath=True)
    if not meshes:
        return

    with gui_util.ProgressDialog(title='Unbind', message="UnBindSKin ...", maxValue=len(meshes)) as prg:
        for i, mesh in enumerate(meshes):
            prg.step(i)
            if prg.wasCanceled():
                break

            if not mesh:
                continue

            historys = cmds.listHistory(mesh)
            if not historys:
                continue

            skin_cluster = [x for x in historys if cmds.nodeType(x) == "skinCluster"]
            if not skin_cluster:
                continue

            cmds.skinCluster(skin_cluster, edit=True, unbind=True)

def re_parent_ndoes():
    not_exsist_nodes = []
    _delete_joints = []
    _re_parent_joints = []

    root_jnt_name:str = 'root_jnt'
    facial1 = '|root|pelvis|spine_01|spine_02|spine_03|spine_04|spine_05|neck_01|FACIAL_C_Neck1Root'
    facial2 = '|root|pelvis|spine_01|spine_02|spine_03|spine_04|spine_05|neck_01|neck_02|FACIAL_C_Neck2Root'
    facial3 = '|root|pelvis|spine_01|spine_02|spine_03|spine_04|spine_05|neck_01|neck_02|head|FACIAL_C_FacialRoot'

    shenron_neck_jnt0_name = '|root_jnt|pelvis_jnt|spine0_jnt|spine1_jnt|chest_jnt|neck0_jnt'
    shenron_neck_jnt1_name = '|root_jnt|pelvis_jnt|spine0_jnt|spine1_jnt|chest_jnt|neck0_jnt|neck1_jnt'
    shenron_head_jnt_name = '|root_jnt|pelvis_jnt|spine0_jnt|spine1_jnt|chest_jnt|neck0_jnt|neck1_jnt|head_jnt'

    shenron_delete_nodes = [
        '|root_jnt|pelvis_jnt|spine0_jnt|spine1_jnt|chest_jnt|neck0_jnt|neck1_jnt|head_jnt|jaw_jnt',
        '|root_jnt|pelvis_jnt|spine0_jnt|spine1_jnt|chest_jnt|neck0_jnt|neck1_jnt|head_jnt|R_eye_jnt',
        '|root_jnt|pelvis_jnt|spine0_jnt|spine1_jnt|chest_jnt|neck0_jnt|neck1_jnt|head_jnt|L_eye_jnt',
        ]

    scene_name, root_node = get_shenron_nodes()
    if not scene_name or not root_node:
        return

    facial1 = f'|{root_node}{facial1}'
    facial2 = f'|{root_node}{facial2}'
    facial3 = f'|{root_node}{facial3}'

    metahuman_reparent_joints = [
                facial3,
                facial2,
                facial1,
                ]
    shenron_target_joints = [
                shenron_head_jnt_name,
                shenron_neck_jnt1_name,
                shenron_neck_jnt0_name,
                ]

    need_nodes = metahuman_reparent_joints + shenron_delete_nodes + [root_jnt_name]

    for node in need_nodes:
        if not cmds.objExists(node):
            not_exsist_nodes.append(node)

    if not_exsist_nodes:
        _m = ', '.join(not_exsist_nodes)
        cmds.warning(f'not exists nodes: [ {_m} ]')
        return

    try:
        cmds.makeIdentity(root_jnt_name, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
    except Exception as e:
        print(f'could not Freeze Transform: [ {root_jnt_name} ]: {e}')

    children_joints = cmds.listRelatives(root_node, children=True, type='joint', fullPath=True)

    _length = len(metahuman_reparent_joints)
    with gui_util.ProgressDialog(title='Re Parent Joints ...', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, (mh_joint, sh_joint) in enumerate(zip(metahuman_reparent_joints, shenron_target_joints)):
            mh_joint_short_name = mh_joint.rsplit('|', 1)[-1]
            sh_joint_short_name = sh_joint.rsplit('|', 1)[-1]
            if prg.wasCanceled():
                break
            prg.setValue(i)
            prg.step(i)
            prg.setLabelText(f'Re parent: [ {mh_joint_short_name} ] to [ {mh_joint_short_name} ]')

            _old_parent = cmds.listRelatives(mh_joint, parent=True, type='joint')[0]
            _result = cmds.parent(mh_joint, sh_joint)[0]

            # 骨自体を削除するので不要
            # cmds.rename(_old_parent, f'{_old_parent}_mh')

    for del_node in shenron_delete_nodes:
        if cmds.objExists(del_node):
            cmds.delete(del_node)

    cmds.parent(root_jnt_name, root_node)
    if children_joints:
        for joint in children_joints:
            cmds.setAttr(f'{joint}.v', 0)
            _del_jiont = cmds.parent(joint, world=True)
            _delete_joints.append(_del_jiont)

def reset_rig_transform():
    ctrl_set_name:str = 'FacialControls'
    _ctrl_set = cmds.ls(ctrl_set_name, type='objectSet')
    if not _ctrl_set:
        cmds.warning(f'not found control set: [ {ctrl_set_name} ]')
        return

    for node in cmds.sets(_ctrl_set, q=True):
        try:
            cmds.setAttr(f'{node}.ty', 0)
        except Exception as e:
            # print(f'could not reset: [ {e} ]')
            pass
        try:
            cmds.setAttr(f'{node}.tx', 0)
        except Exception as e:
            # print(f'could not reset: [ {e} ]')
            pass

def get_node_from_selection(is_single:bool=True)->list:
    result:list = []
    selections:list = cmds.ls(selection=True, type='transform', long=True)
    if not selections:
        return result

    if is_single:
        result = [selections[0]]
    else:
        result = selections
    return result

def get_blendshape_skincluster(node:str=''):
    skincluster:str = ''
    blendshape:str = ''
    if not node:
        return blendshape, skincluster
    for history in cmds.listHistory(node):
        if cmds.nodeType(history) == 'blendShape':
            blendshape = history
        if cmds.nodeType(history) == 'skinCluster':
            skincluster = history
    return blendshape, skincluster

def get_connections(node:str='', type='blendShape'):
    connections:list = []
    source:list = []
    target:list = []
    if not node:
        return source, target
    if type == 'blendShape':
        connections = cmds.listConnections(node, connections=True, plugs=True, destination=False, source=True, type='embeddedNodeRL4')
    elif type == 'skinCluster':
        connections = cmds.listConnections(node, connections=True, plugs=True, destination=True, source=False, type='skinCluster')
    else:
        connections = cmds.listConnections(node, connections=True, plugs=True, destination=False, fullNodeName=True)

    if not connections:
        return source, target

    source = connections[1::2]
    target = connections[0::2]

    return source, target

def import_metahuman_weight_to_selections(weight_type:str='Metahuman'):
    nodes:str = get_node_from_selection(is_single=False)

    if not nodes:
        cmds.warning('select mesh node')
        return
    meshes:list = cmds.listRelatives(nodes, allDescendents=True, type='mesh', fullPath=True)
    if not meshes:
        return

    meshes:list = [x for x in meshes if not cmds.getAttr(f"{x}.intermediateObject")]
    if not meshes:
        return

    _length = len(meshes)
    with gui_util.ProgressDialog(title='Import Skin Weight', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, mesh in enumerate(meshes):
            mesh_short_name = mesh.rsplit('|', 1)[-1]

            joints_dict, file_path_dict = get_weight_file_jointsdict(weight_directory=weight_type)
            if not joints_dict and not file_path_dict:
                cmds.warning(f'could not find weight data: [ {mesh_short_name} ]')
                continue

            mesh_weight_file:str = file_path_dict.get(mesh_short_name)

            if not mesh_weight_file:
                cmds.warning(f'not found weight file: [ {mesh_short_name} ]')
                continue

            weight_file_name = mesh_short_name
            joints = joints_dict.get(mesh_short_name)

            blend_shape, skin_cluster = get_blendshape_skincluster(node=mesh)
            if not skin_cluster:
                skin_cluster = create_skin_cluster(joints=joints, node=mesh)

            prg.setValue(i)
            prg.step(i)
            prg.setLabelText(f'import weight: [ {mesh_short_name} ]')
            set_weight_zero(mesh=mesh, skinCluster=skin_cluster)
            cmds.setAttr(f'{skin_cluster}.maintainMaxInfluences', 0)
            load_weight_file_cmds(
                                shape=mesh,
                                import_path=str(mesh_weight_file.parent),
                                file_name=mesh_weight_file.name,
                                deformer="",
                                method='index',
                                )
            cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)


def disconnect_attribute_joint() -> dict:

    nodes:list = get_node_from_selection(is_single=False)
    joint_connection_data:dict = {}

    if not nodes:
        cmds.warning('select joint node')
        return

    for target in nodes:
        if not cmds.objExists(target):
            continue
        # print(f'disconnect_attribute {target}------------------')
        joints:list = [target]
        joints.extend(cmds.listRelatives(target, allDescendents=True, type='joint', fullPath=True))
        for i,joint in enumerate(joints):
            _con = cmds.listConnections(joint, connections=True, plugs=True, destination=False, fullNodeName=True)

            if not _con:
                continue

            _target = _con[0::2]
            _source = _con[1::2]

            joint_connection_data[joint] = zip(_source, _target)
            for t,s in zip(_target, _source):
                cmds.disconnectAttr(s, t)
    return joint_connection_data

def connect_attribute_joint(joint_connection_data:dict) -> None:
    nodes:list = get_node_from_selection(is_single=False)
    # targets:list = self.root_joints
    # print('connect_attribute ----------------------')

    # if not nodes:
    #     cmds.warning('select joint node')
    #     return

    for joint, attributes in joint_connection_data.items():
        for source_attirubute, target_attribute in attributes:

            if not cmds.objExists(source_attirubute) and not cmds.objExists(target_attribute):
                continue

            cmds.connectAttr(source_attirubute, target_attribute, force=True)
            # print(f're connect: {source_attirubute}, {target_attribute}')

    print(f'connect attribute: [ {joint_connection_data} ]')


def delete_history_from_selection_mesh_joint(is_reset_transform:bool=False, weight_type:str='Metahuman')->dict:
    nodes:str = get_node_from_selection(is_single=False)
    connection_data:dict = {}

    if not nodes:
        cmds.warning('select node')
        return

    _length = len(nodes)
    with gui_util.ProgressDialog(title='Unconnection', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, node in enumerate(nodes):
            mesh_nodes = cmds.listRelatives(node, allDescendents=True, type='mesh', fullPath=True)
            joint_nodes = cmds.listRelatives(node, allDescendents=True, type='joint', fullPath=True)
            # print(mesh_nodes)
            prg.setLabelText(f'Un connection: [ {node} ]')
            if prg.wasCanceled():
                break

            if joint_nodes:
                for joint in joint_nodes:
                    _con = cmds.listConnections(joint, connections=True, plugs=True, destination=False, fullNodeName=True)

                    if not _con:
                        continue

                    target_cone = _con[0::2]
                    source_cone = _con[1::2]

                    joint_connection:dict = {
                        'joint_connection_source': source_cone,
                        'joint_connection_target': target_cone,
                    }
                    connection_data[joint] = joint_connection
                    # print(target_cone, source_cone)
                    for t,s in zip(target_cone, source_cone):
                        cmds.disconnectAttr(s, t)

            if mesh_nodes:
                for mesh_node in mesh_nodes:
                    if cmds.getAttr(f"{mesh_node}.intermediateObject"):
                        continue
                    # print(mesh_node)
                    skin_cluster:str = ''
                    blend_shape:str = ''
                    joints:list = []
                    blend_shape_source_cone:list = []
                    blend_shape_target_cone:list = []

                    parent_node:str = cmds.listRelatives(mesh_node, parent=True, path=True)[0]
                    node_histories:list = cmds.listHistory(parent_node)

                    for history in node_histories:
                        if cmds.nodeType(history) == 'skinCluster':
                            skin_cluster = history
                        elif cmds.nodeType(history) == 'blendShape':
                            blend_shape = history

                    if skin_cluster:
                        joints = cmds.skinCluster(skin_cluster, influence=True, q=True)

                    if blend_shape:
                        blend_shape_source_cone, blend_shape_target_cone = get_connections(node=blend_shape, type='blendShape')

                    mesh_data:dict = {
                                    'skin_cluster': skin_cluster,
                                    'joints': joints,
                                    'blend_shape': blend_shape,
                                    'blend_shape_source_cone': blend_shape_source_cone,
                                    'blend_shape_target_cone': blend_shape_target_cone
                                    }

                    connection_data[mesh_node] = mesh_data
                cmds.delete(node, constructionHistory=True)
            prg.setValue(i)
            prg.step(i)

    if is_reset_transform:
        reset_rig_transform()

    return connection_data


def reconnection_memory_data_mesh_joint(connection_data:dict = {})->None:
    if not connection_data:
        cmds.warning('not found connection data')
        return

    _length = len(connection_data)
    # with gui_util.ProgressDialog(title='Reconnection', maxValue=_length) as prg:
    #     QtCore.QCoreApplication.processEvents()
    for i,(node, connections) in enumerate(connection_data.items()):
        if not cmds.objExists(node):
            continue
        # print(cmds.nodeType(node), "-----", node)

        # _text = f'Re connection: [ {node} ]'
        # prg.setLabelText(_text)
        # print(_text)

        # if prg.wasCanceled():
        #     break

        if cmds.nodeType(node) == 'joint':
            joint_connection_source = connections.get('joint_connection_source')
            joint_connection_target = connections.get('joint_connection_target')
            for _i, (source_attirubute, target_attribute) in enumerate(zip(joint_connection_source, joint_connection_target)):
                try:
                    cmds.connectAttr(source_attirubute, target_attribute, force=True)
                except Exception as e:
                    print(f'connent error: {e}')
        else:
            joints = connections.get('joints')
            # print(joints)
            if joints:
                skin_cluster = create_skin_cluster(joints=joints, node=node)
            else:
                cmds.warning(f'not found need joints: [ {node} ]')

            blend_shape = connections.get('blend_shape')
            if blend_shape:
                blend_shape_source_cone = connections.get('blend_shape_source_cone')
                blend_shape_target_cone = connections.get('blend_shape_target_cone')

                if not blend_shape_source_cone and not blend_shape_target_cone:
                    cmds.warning(f'not found connections: [ {node} ]')
                    continue

                blend_shape = cmds.blendShape(node, name=blend_shape)[0]

                for _i, (source_attirubute, target_attribute) in enumerate(zip(blend_shape_source_cone, blend_shape_target_cone)):
                    target = target_attribute.split('.', 1)[-1]
                    source = source_attirubute.split('.', 1)[-1]
                    cmds.aliasAttr(f'{target}', f'{blend_shape}.w[{_i}]')

                    try:
                        cmds.connectAttr(source_attirubute, target_attribute, force=True)
                    except Exception as e:
                        print(f'connent error: {e}')
        # prg.setValue(i)
        # prg.step(i)




def reconnection_data_deep(weight_type:str='')->None:
    if not weight_type:
        return

    nodes:list = get_node_from_selection(is_single=False)

    if not nodes:
        cmds.warning('select mesh node')
        return

    rl4_node = get_rl4_node_inscene()
    if not rl4_node:
        return

    meshes:list = cmds.listRelatives(nodes, allDescendents=True, type='mesh', path=True)
    if not meshes:
        return

    meshes:list = [x for x in meshes if not cmds.getAttr(f"{x}.intermediateObject")]
    if not meshes:
        return

    connection_data:dict = load_config('blend_shape_connections')

    _length = len(meshes)
    with gui_util.ProgressDialog(title='Reconnection', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, mesh_node in enumerate(meshes):
            if not cmds.objExists(mesh_node):
                continue

            histories:list = [x for x in cmds.listHistory(mesh_node) if x != mesh_node]

            if histories:
                continue

            joints_dict, file_path_dict = get_weight_file_jointsdict(weight_directory=weight_type)
            if not joints_dict and not file_path_dict:
                cmds.warning(f'could not find weight data: [ {mesh_node} ]')
                continue

            joints = joints_dict.get(mesh_node)
            if joints:
                skin_cluster = create_skin_cluster(joints=joints, node=mesh_node)
            else:
                cmds.warning(f'not found need joints: [ {mesh_node} ]')

            connections:dict = connection_data.get(mesh_node)

            if connections:
                blend_shape = f'{mesh_node}_blendShape'
                blend_shape = cmds.blendShape(mesh_node, name=blend_shape)[0]

                for source, target in connections.items():
                    cmds.aliasAttr(f'{target}', f'{blend_shape}.w[{i}]')
                    source_attirubute:str = f'{rl4_node}.{source}'
                    target_attribute:str = f'{blend_shape}.{target}'
                    try:
                        cmds.connectAttr(source_attirubute, target_attribute, force=True)
                    except Exception as e:
                        print(f'connent error: {e}')
            prg.setValue(i)
            prg.step(i)
    cmds.select(nodes, replace=True)

def delete_history_reconneciotns_from_selection_deep(is_reset_transform:bool=False, weight_type:str='Metahuman')->dict:
    nodes:str = get_node_from_selection(is_single=False)
    mesh_connection_data:dict = {}

    if not nodes:
        cmds.warning('select mesh node')
        return

    meshes:list = cmds.listRelatives(nodes, allDescendents=True, type='mesh', path=True)
    if not meshes:
        cmds.warning('not found mesh shapes')
        return

    meshes:list = [x for x in meshes if not cmds.getAttr(f"{x}.intermediateObject")]
    if not meshes:
        cmds.warning('not found mesh shapes')
        return

    _length = len(meshes)
    with gui_util.ProgressDialog(title='Unconnection', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, mesh_node in enumerate(meshes):
            prg.setLabelText(f'Un connection: [ {mesh_node} ]')
            if prg.wasCanceled():
                break

            skin_cluster:str = ''
            blend_shape:str = ''
            joints:list = []
            blend_shape_source_cone:list = []
            blend_shape_target_cone:list = []

            node:str = cmds.listRelatives(mesh_node, parent=True, path=True)[0]
            node_histories:list = cmds.listHistory(mesh_node)

            for history in node_histories:
                if cmds.nodeType(history) == 'skinCluster':
                    skin_cluster = history
                elif cmds.nodeType(history) == 'blendShape':
                    blend_shape = history

            if skin_cluster:
                joints = cmds.skinCluster(skin_cluster, influence=True, q=True)

            if blend_shape:
                blend_shape_source_cone, blend_shape_target_cone = get_connections(node=blend_shape, type='blendShape')

            mesh_data:dict = {
                            'skin_cluster': skin_cluster,
                            'joints': joints,
                            'blend_shape': blend_shape,
                            'blend_shape_source_cone': blend_shape_source_cone,
                            'blend_shape_target_cone': blend_shape_target_cone
                            }

            mesh_connection_data[mesh_node] = mesh_data
            cmds.delete(node, constructionHistory=True)
            prg.setValue(i)
            prg.step(i)

    if is_reset_transform:
        reset_rig_transform()

    return mesh_connection_data


def delete_history_reconneciotns_from_selection(is_reset_transform:bool=False, weight_type:str='Metahuman')->dict:
    nodes:str = get_node_from_selection(is_single=False)
    mesh_connection_data:dict = {}

    if not nodes:
        cmds.warning('select mesh node')
        return

    _length = len(nodes)
    with gui_util.ProgressDialog(title='Unconnection', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, node in enumerate(nodes):
            prg.setLabelText(f'Un connection: [ {node} ]')
            if prg.wasCanceled():
                break
            skin_cluster:str = ''
            blend_shape:str = ''
            joints:list = []
            blend_shape_source_cone:list = []
            blend_shape_target_cone:list = []

            mesh:list = cmds.listRelatives(node, children=True, type='mesh', path=True)
            if not mesh:
                cmds.warning(f'no mesh: [{node}]')
                continue

            mesh:list = [x for x in mesh if not cmds.getAttr(f"{x}.intermediateObject")]
            if not mesh:
                cmds.warning(f'no mesh: [{node}]')
                continue

            mesh_node:str = mesh[0]
            node_histories:list = cmds.listHistory(mesh_node)

            for history in node_histories:
                if cmds.nodeType(history) == 'skinCluster':
                    skin_cluster = history
                elif cmds.nodeType(history) == 'blendShape':
                    blend_shape = history

            if skin_cluster:
                joints = cmds.skinCluster(skin_cluster, influence=True, q=True)

            if blend_shape:
                blend_shape_source_cone, blend_shape_target_cone = get_connections(node=blend_shape, type='blendShape')

            mesh_data:dict = {
                            'skin_cluster': skin_cluster,
                            'joints': joints,
                            'blend_shape': blend_shape,
                            'blend_shape_source_cone': blend_shape_source_cone,
                            'blend_shape_target_cone': blend_shape_target_cone
                            }

            mesh_connection_data[mesh_node] = mesh_data
            cmds.delete(node, constructionHistory=True)
            prg.setValue(i)
            prg.step(i)

    if is_reset_transform:
        reset_rig_transform()

    return mesh_connection_data

def get_rl4_node_inscene()->str:
    _result:str = ''
    rl4_node_type = load_config('rl4_nodetype')
    rl4_node = cmds.ls(type=rl4_node_type)

    if not rl4_node:
        cmds.warning(f'not found [ {rl4_node_type} ] node type')
        return _result
    if len(rl4_node) != 1:
        cmds.warning(f'too many [ {rl4_node_type} ] node type')
        return _result

    _result = rl4_node[0]
    return _result

def reconnection_data_deep(weight_type:str='')->None:
    if not weight_type:
        return

    nodes:list = get_node_from_selection(is_single=False)

    if not nodes:
        cmds.warning('select mesh node')
        return

    rl4_node = get_rl4_node_inscene()
    if not rl4_node:
        return

    meshes:list = cmds.listRelatives(nodes, allDescendents=True, type='mesh', path=True)
    if not meshes:
        return

    meshes:list = [x for x in meshes if not cmds.getAttr(f"{x}.intermediateObject")]
    if not meshes:
        return

    connection_data:dict = load_config('blend_shape_connections')

    _length = len(meshes)
    with gui_util.ProgressDialog(title='Reconnection', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, mesh_node in enumerate(meshes):
            if not cmds.objExists(mesh_node):
                continue

            histories:list = [x for x in cmds.listHistory(mesh_node) if x != mesh_node]

            if histories:
                continue

            joints_dict, file_path_dict = get_weight_file_jointsdict(weight_directory=weight_type)
            if not joints_dict and not file_path_dict:
                cmds.warning(f'could not find weight data: [ {mesh_node} ]')
                continue

            joints = joints_dict.get(mesh_node)
            if joints:
                skin_cluster = create_skin_cluster(joints=joints, node=mesh_node)
            else:
                cmds.warning(f'not found need joints: [ {mesh_node} ]')

            connections:dict = connection_data.get(mesh_node)

            if connections:
                blend_shape = f'{mesh_node}_blendShape'
                blend_shape = cmds.blendShape(mesh_node, name=blend_shape)[0]

                for source, target in connections.items():
                    cmds.aliasAttr(f'{target}', f'{blend_shape}.w[{i}]')
                    source_attirubute:str = f'{rl4_node}.{source}'
                    target_attribute:str = f'{blend_shape}.{target}'
                    try:
                        cmds.connectAttr(source_attirubute, target_attribute, force=True)
                    except Exception as e:
                        print(f'connent error: {e}')
            prg.setValue(i)
            prg.step(i)
    cmds.select(nodes, replace=True)



def reconnection_memory_data(mesh_connection_data:dict = {})->None:
    if not mesh_connection_data:
        cmds.warning('not found connection data')
        return

    nodes:list = get_node_from_selection(is_single=False)

    print(nodes, " -------aaa")
    if not nodes:
        cmds.warning('select mesh node')
        return

    meshes:list = cmds.listRelatives(nodes, allDescendents=True, type='mesh', path=True)
    print(meshes, " ----- meshes")
    if not meshes:
        cmds.warning(f'{nodes} has no children')
        return

    _length = len(mesh_connection_data)
    with gui_util.ProgressDialog(title='Reconnection', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i,(mesh_node, mesh_data) in enumerate(mesh_connection_data.items()):
            if not cmds.objExists(mesh_node):
                continue

            if mesh_node not in meshes:
                continue

            _text = f'Re connection: [ {mesh_node} ]'
            prg.setLabelText(_text)
            print(_text)

            if prg.wasCanceled():
                break
            joints = mesh_data.get('joints')
            print("joints ---- ", joints)
            if joints:
                skin_cluster = create_skin_cluster(joints=joints, node=mesh_node)
            else:
                cmds.warning(f'not found need joints: [ {mesh_node} ]')

            blend_shape = mesh_data.get('blend_shape')
            print("blend_shape --- ", blend_shape)
            if blend_shape:
                blend_shape_source_cone = mesh_data.get('blend_shape_source_cone')
                blend_shape_target_cone = mesh_data.get('blend_shape_target_cone')
                print("blend_shape_source_cone --- ", blend_shape_source_cone)
                print("blend_shape_target_cone --- ", blend_shape_target_cone)
                # for x in blend_shape_target_cone:
                #     print(x)
                if not blend_shape_source_cone and not blend_shape_target_cone:
                    cmds.warning(f'not found connections: [ {mesh_node} ]')
                    continue

                blend_shape = cmds.blendShape(mesh_node, name=blend_shape)[0]

                for _i, (source_attirubute, target_attribute) in enumerate(zip(blend_shape_source_cone, blend_shape_target_cone)):
                    target = target_attribute.split('.', 1)[-1]
                    source = source_attirubute.split('.', 1)[-1]
                    cmds.aliasAttr(f'{target}', f'{blend_shape}.w[{_i}]')
                    # print(f'{source: <20}: {target}')
                    try:
                        cmds.connectAttr(source_attirubute, target_attribute, force=True)
                    except Exception as e:
                        print(f'connent error: {e}')
            prg.setValue(i)
            prg.step(i)


    cmds.select(nodes, replace=True)

def get_connection_history(mesh_node:str='', weight_type:str='Metahuman'):
    blend_shape:str = ''
    skin_cluster:str = ''
    joints:list = []
    blend_shape_source_cone:list = []
    blend_shape_target_cone:list = []

    blend_shape, skin_cluster = get_blendshape_skincluster(node=mesh_node)
    blend_shape_source_cone, blend_shape_target_cone = get_connections(node=blend_shape, type='blendShape')
    joints_dict, file_path_dict = get_weight_file_jointsdict(weight_directory=weight_type)
    if not joints_dict and not file_path_dict:
        cmds.warning('could not find weight data')
        return skin_cluster, joints, blend_shape, blend_shape_source_cone, blend_shape_target_cone

    mesh_weight_file = file_path_dict.get(mesh_node)
    joints = joints_dict.get(mesh_node)
    if not mesh_weight_file:
        cmds.warning(f'not found weight file: [ {mesh_node} ]')
        return skin_cluster, joints, blend_shape, blend_shape_source_cone, blend_shape_target_cone

    if not joints:
        cmds.warning(f'not found need joints: [ {mesh_node} ]')
        return skin_cluster, joints, blend_shape, blend_shape_source_cone, blend_shape_target_cone
    return skin_cluster, joints, blend_shape, blend_shape_source_cone, blend_shape_target_cone


def disconnect_attribute(root_node:str='')-> dict:
    connection_source_target:dict = {}
    if not root_node:
        return connection_source_target

    nodes:list = cmds.listRelatives(root_node, allDescendents=True, type='mesh', fullPath=True)
    # joints = cmds.skinCluster(src_skin_cluster, influence=True, q=True)
    cmds.blendShape('head_lod0_mesh_blendShapes', edit=True, topologyCheck=True, target=['|nfc0010|mesh|lod0|head_lod0|head_lod0Shape', 682, 'test2', 1], weight=[682, 1])
    #  -tc on -t |nfc0010|mesh|lod0|head_lod0|head_lod0Shape 681 head_lod8 1 -w 681 1  head_lod0_mesh_blendShapes)
    for i,node in enumerate(nodes):

        _con = cmds.listConnections(node, connections=True, plugs=True, destination=False)

        if not _con:
            continue

        _target = _con[0::2]
        _source = _con[1::2]

        connection_source_target[node] = zip(_source, _target)
        for t,s in zip(_target, _source):
            print(t, cmds.nodeType(t))
            print(s, cmds.nodeType(s))

            cmds.disconnectAttr(s, t)

    return connection_source_target

def delete_history(root_node:str=''):
    if not root_node:
        return
    for node in cmds.listRelatives(root_node, allDescendents=True, fullPath=True):
        try:
            cmds.delete(node, channels=True)
            print(node)
        except Exception as e:
            print(e)


def un_bind_character_part():
    geometory_node_name:str = load_config('lod_root_node')
    geometory_node_shortname:str = geometory_node_name.rsplit('|', 1)[-1]
    geometory_node:list = cmds.ls(geometory_node_shortname, type='transform')
    metahuman_root_joint:list = [x for x in cmds.ls(assemblies=True) if x == 'root']

    # print("--------------------------geometory_node")
    # print(geometory_node)
    # print(metahuman_root_joint)

    if not geometory_node:
        cmds.warning(f'not found geometory node: [ {geometory_node_name} ]')
        return
    if len(geometory_node) != 1:
        cmds.warning(f'Multiple Existence: [ {geometory_node_shortname} ]')
        return

    if not metahuman_root_joint:
        cmds.warning('not found metahuman root joint')
        return

    metahuman_root_joint:str = metahuman_root_joint[0]
    geometory_node:str = geometory_node[0]

    is_done = un_bind(root_node=geometory_node)
    print(f'un bind node: [ {geometory_node} ] [ {is_done} ]')
    if not is_done:
        return

    cmds.setAttr(f'{geometory_node}.rotateX', -90)
    print(f'rotate X -90: [ {geometory_node} ]')
    # cmds.makeIdentity(geometory_node, apply=True, translate=True, rotate=True, scale=True, normal=False, preserveNormals=True)
    # print(f'transfomation freeze: [ {geometory_node} ]')
    cmds.setAttr(f'{metahuman_root_joint}.rotateX', 0)
    print(f'rotate X 0: [ {metahuman_root_joint} ]')

def un_bind(root_node :str = '') -> bool:
    is_done:bool = False

    if not root_node or not cmds.objExists(root_node):
        return is_done
    meshes:list = cmds.listRelatives(root_node, allDescendents=True, type='mesh', fullPath=True)

    if not meshes:
        cmds.warning(f'[ {root_node} ] has no meshes')
        return is_done

    _length = len(meshes)

    with gui_util.ProgressDialog(title='Unbind', message="UnBindSKin ...", maxValue=_length) as prg:
        for i, mesh in enumerate(meshes):
            prg.step(i)
            if prg.wasCanceled():
                break

            historys = cmds.listHistory(mesh)
            skin_cluster = [x for x in historys if cmds.nodeType(x) == "skinCluster"]
            if not skin_cluster:
                continue
            cmds.skinCluster(skin_cluster, edit=True, unbind=True)
            is_done:bool = True

    return is_done



def re_bind():
    geometory_node_name:str = load_config('lod_root_node')
    geometory_node_shortname:str = geometory_node_name.rsplit('|', 1)[-1]
    geometory_node:list = cmds.ls(geometory_node_shortname, type='transform')

    if not geometory_node:
        cmds.warning(f'not found geometory node: [ {geometory_node_name} ]')
        return
    if len(geometory_node) != 1:
        cmds.warning(f'Multiple Existence: [ {geometory_node_shortname} ]')
        return

    geometory_node:str = geometory_node[0]

    lod_groups:list = cmds.listRelatives(geometory_node, children=True, type='transform', fullPath=True)

    _weitht_import = ImportSkinWeight()
    _weitht_import.apply_metahuman_weights(lod_groups=lod_groups)



def import_metahuman_weight():
    _weitht_import = ImportSkinWeight()
    _weitht_import.apply_shenron_weights()


class ImportSkinWeight:
    def __init__(self):
        # self.weight_type:str = weight_type
        self.root_node:str = ''
        self.scene_name:str = ''
        self.lod_groups:list = ''
        self.joints_dict:dict = {}
        self.file_path_dict:dict = {}
        self.head_model_lod_group:dict = {}

    def apply_metahuman_weights(self, lod_groups:list=[]):
        self.lod_groups = lod_groups
        joints_dict, file_path_dict = get_weight_file_jointsdict(weight_directory='Metahuman')

        if not joints_dict and not file_path_dict:
            return
        self.import_weights(joints_dict=joints_dict, file_path_dict=file_path_dict)
        print("head_model_lod_group ----------------- ", self.head_model_lod_group)
        if self.head_model_lod_group:
            self.transfar_weight()

    def apply_shenron_weights(self):
        scene_name, root_node, lod_groups = check_nodes()

        if not scene_name:
            cmds.warning('open maya scene')
            return
        if not root_node:
            cmds.warning('not found [ root node ]')
            return

        if not lod_groups:
            cmds.warning(f'not found lod group')
            return

        self.lod_groups = lod_groups
        joints_dict, file_path_dict = get_weight_file_jointsdict(weight_directory='Shenron')

        if not joints_dict and not file_path_dict:
            cmds.warning('not found shenron weithts')
            return

        self.import_weights(joints_dict=joints_dict, file_path_dict=file_path_dict)
        # print("head_model_lod_group ----------------- ", self.head_model_lod_group)
        if self.head_model_lod_group:
            self.transfar_weight()

    def transfar_weight(self):
        _length = len(self.lod_groups)
        with gui_util.ProgressDialog(title='Transfer Skin Weight', maxValue=_length) as prg:
            QtCore.QCoreApplication.processEvents()
            for i, lod_group in enumerate(self.lod_groups):
                # print(f"lod group: [ {lod_group} ]")
                if prg.wasCanceled():
                    break
                prg.setValue(i)
                prg.step(i)
                prg.setLabelText(f'Transfer weight: [ {lod_group} ]')
                children = cmds.listRelatives(lod_group, allDescendents=True, type='mesh', fullPath=True)
                for cld in children:
                    _not_exist_joint = []
                    _duplication_joint = []

                    if cmds.getAttr(f"{cld}.intermediateObject"):
                        continue
                    # print(cld, " -------------------------------------------------")
                    # スキンクラスタ取得に必要
                    long_name = cmds.ls(cld, long=True)[0]

                    # 同名がある確率が高いのでショートネームはこちらの手法を使う
                    short_name = cld.split('|')[-1]
                    # _prg.setLabelText(f'import weight: [ {short_name} ]')
                    skin_cluster = get_skin_cluster(long_name)
                    # print("skin_cluster  --- ", skin_cluster)
                    if skin_cluster:
                        continue

                    head_mesh = self.head_model_lod_group.get(lod_group)
                    # print("head_mesh ------------", head_mesh)
                    if not head_mesh:
                        continue

                    src_skin_cluster = get_skin_cluster(head_mesh)
                    # print("src_skin_cluster -- ", src_skin_cluster)
                    if not src_skin_cluster:
                        continue

                    joints = cmds.skinCluster(head_mesh, q=True, influence=True)

                    if not joints:
                        cmds.warning(f'not found joint from weight data: [{short_name}]')
                        continue

                    for joint in joints:
                        if not cmds.objExists(joint):
                            _not_exist_joint.append(joint)
                        else:
                            _jnt = cmds.ls(joint, type='joint')
                            if len(_jnt) != 1:
                                _duplication_joint.append(joint)

                    if _not_exist_joint:
                        _m = ', '.join(_not_exist_joint)
                        cmds.warning(f'not found joints: [ {_m} ]')
                        continue

                    if _duplication_joint:
                        _m = ', '.join(_duplication_joint)
                        cmds.warning(f'duplication joints: [ {_m} ]')
                        continue

                    skin_cluster = create_skin_cluster(joints=joints, node=long_name)
                    cmds.setAttr(f'{skin_cluster}.maintainMaxInfluences', 0)

                    cmds.copySkinWeights(sourceSkin=src_skin_cluster,
                                        destinationSkin=skin_cluster,
                                        noMirror=True,
                                        surfaceAssociation='closestPoint',
                                        influenceAssociation='closestJoint',
                                        noBlendWeight=True,
                                        normalize=True)

                    cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)

    def import_weights(self, joints_dict:dict={}, file_path_dict:dict={}):
        if not self.lod_groups:
            cmds.warning('not found lod groups')
            return

        _length = len(self.lod_groups)
        with gui_util.ProgressDialog(title='Import Skin Weight', maxValue=_length) as prg:
            QtCore.QCoreApplication.processEvents()
            for i, lod_group in enumerate(self.lod_groups):
                print(f"lod group: [ {lod_group} ]")
                if prg.wasCanceled():
                    break
                prg.setValue(i)
                prg.step(i)
                prg.setLabelText(f'import weight: [ {lod_group} ]')
                children = cmds.listRelatives(lod_group, allDescendents=True, type='mesh', fullPath=True)
                for cld in children:
                    _not_exist_joint = []
                    _duplication_joint = []

                    if cmds.getAttr(f"{cld}.intermediateObject"):
                        continue
                    # スキンクラスタ取得に必要
                    long_name = cmds.ls(cld, long=True)[0]

                    # 同名がある確率が高いのでショートネームはこちらの手法を使う
                    short_name = cld.split('|')[-1]
                    # _prg.setLabelText(f'import weight: [ {short_name} ]')
                    skin_cluster = get_skin_cluster(long_name)

                    if short_name.startswith('head'):
                        self.head_model_lod_group[lod_group] = short_name

                    joints = joints_dict.get(short_name)

                    if not joints:
                        cmds.warning(f'not found joint from weight data: [{short_name}]')
                        continue

                    for joint in joints:
                        if not cmds.objExists(joint):
                            _not_exist_joint.append(joint)
                        else:
                            _jnt = cmds.ls(joint, type='joint')
                            if len(_jnt) != 1:
                                _duplication_joint.append(joint)

                    if _not_exist_joint:
                        _m = ', '.join(_not_exist_joint)
                        cmds.warning(f'not found joints: [ {_m} ]')
                        continue

                    if _duplication_joint:
                        _m = ', '.join(_duplication_joint)
                        cmds.warning(f'duplication joints: [ {_m} ]')
                        continue

                    if not skin_cluster:
                        skin_cluster = create_skin_cluster(joints=joints, node=long_name)
                    else:
                        add_influence(skin_cluster=skin_cluster, joints=joints)

                    mesh_weight_file = file_path_dict.get(short_name)
                    if not mesh_weight_file:
                        cmds.warning(f'not found weight file: [ {short_name} ]')
                        continue

                    print(f'import weight: [ {short_name} ]')
                    set_weight_zero(mesh=long_name, skinCluster=skin_cluster)
                    cmds.setAttr(f'{skin_cluster}.maintainMaxInfluences', 0)
                    load_weight_file_cmds(
                                        shape=long_name,
                                        import_path=str(mesh_weight_file.parent),
                                        file_name=mesh_weight_file.name,
                                        deformer="",
                                        method='index',
                                        )
                    cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)

def delete_nodes_character()->None:
    delete_nodes:list = []
    delete_node_type:dict = load_config('character_delete_nodes')
    for _node_name, _node_type in delete_node_type.items():
        _node = cmds.ls(_node_name, type=_node_type)
        if _node:
            delete_nodes.append(_node[0])
    if delete_nodes:
        cmds.delete(delete_nodes)
    maya.mel.eval('MLdeleteUnused();')

def delete_nodes_facial(body_model_path:str=''):
    if not body_model_path:
        cmds.warning('need path: [Import Body Model]')
        return
    body_model_path:Path = Path(body_model_path)
    file_name:str = body_model_path.stem
    character_id:str = file_name.split('_', 1)[-1]
    if not character_id:
        cmds.warning('nod found character ID')
        return

    _character_id = {'|' + character_id: 'transform'}
    _delete_nodes:dict = load_config('facial_delete_nodes')
    _delete_nodes.update(_character_id)
    for _delete_node_name, node_type in _delete_nodes.items():
        _delete_node = cmds.ls(_delete_node_name, type=node_type)
        if _delete_node:
            try:
                cmds.delete(_delete_node)
                print(f'delete node: [ {_delete_node} ]')
            except Exception as e:
                print(f'could not delete node: [ {_delete_node} ]: {e}')
    maya.mel.eval('MLdeleteUnused();')

def get_parents(node:str='') -> str:
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
    else:
        yield node[0] if isinstance(node, list) else node

def set_joint_preferred_angles(joint:str=""):
    """ジョイントのpreferred_anglesを復元

    Args:
        joint (str, optional): _description_. Defaults to "".
    """
    if not joint:
        return
    cmds.joint(joint, edit=True, setPreferredAngles=True, children=True)

def restore_bindpose(joints:list='') -> None:
    if not joints:
        return

    bindPose = cmds.dagPose(q=True, bindPose=True)
    root_joints = set()
    root_joint = ''
    for joint in joints:
        for _p in get_parents(joint):
            if cmds.nodeType(_p) == 'joint':
                root_joint = _p
            root_joints.add(_p)

    root_joints = list(root_joints)
    all_joints = cmds.listRelatives(root_joints, allDescendents=True, fullPath=True, type="joint")
    do_restore_bindpose(posees=bindPose, joints=all_joints, old_selections=joints, root_joint=root_joint)

def do_restore_bindpose(posees:list=[], joints:list=[], old_selections:list=[], root_joint:str=''):
    cmds.select(joints, replace=True)
    if not posees:
        new_pose = cmds.dagPose(bindPose=True, save=True, selection=True)
    else:
        pose = posees[0]
        # for pose in posees:
        cmds.delete(pose)
        cmds.dagPose(bindPose=True, save=True, selection=True, name=pose)

    if root_joint:
        set_joint_preferred_angles(joint=root_joint)

    if old_selections:
        cmds.select(old_selections, replace=True)


def create_skin_cluster(joints:list=[], node:str='', max_influences=30):
    skin_cluster_base_name = node.rsplit("|", 1)[-1]
    skin_cluster = cmds.skinCluster(
                                joints,
                                node,
                                toSelectedBones=True,
                                bindMethod=0,
                                normalizeWeights=True,
                                weightDistribution=0,
                                maximumInfluences=max_influences,
                                obeyMaxInfluences=False,
                                dropoffRate=4,
                                removeUnusedInfluence=False,
                                name='{}_skinCluster'.format(skin_cluster_base_name)
                                )[0]
    cmds.setAttr(f'{skin_cluster}.maintainMaxInfluences', 0)
    set_joint_preferred_angles(joints[-1])
    return skin_cluster


def add_influence(skin_cluster:str='', joints:list=[]):
    _length = len(joints)
    _count = 0
    _flag = True

    # cmds.setAttr(f'{skin_cluster}.maintainMaxInfluences', 1)
    cmds.skinCluster(skin_cluster, edit=True, maximumInfluences=30)
    # with gui_util.ProgressDialog(title='Add Influence', message="Add Influence ...", maxValue=_length) as prg:
    #     QtCore.QCoreApplication.processEvents()
    for joint in joints:
        # _count += 1
        if not joint:
            continue
        if not cmds.objExists(joint):
            continue
        # print(joint, " -----")
        # print(joint not in cmds.skinCluster(skin_cluster, influence=joint, q=True))
        # if prg.wasCanceled():
        #     break
        if joint not in cmds.skinCluster(skin_cluster, influence=joint, q=True):
            # _flag = True
            cmds.skinCluster(skin_cluster, edit=True, useGeometry=False, polySmoothness=0.0, lockWeights=True, weight=0.0, addInfluence=joint)
            cmds.skinCluster(skin_cluster, edit=True, influence=joint, lockWeights=False)
        # print(joint not in cmds.skinCluster(skin_cluster, influence=joint, q=True))
    # set_joint_preferred_angles(joints[-1])

def add_influence_skincluster(src_skin_cluster:str='', dst_skin_clusters:list=[]):
    joints = cmds.skinCluster(src_skin_cluster, influence=True, q=True)

    for dst_skin_cluster in dst_skin_clusters:
        add_influence(skin_cluster=dst_skin_cluster, joints=joints)


def get_skin_cluster(node: str='') -> str:
    """スキンクラスタの存在確認

    Args:
        node (str): メッシュノード

    Returns:
        str: スキンクラスタノード
    """

    skin_cluster = ""
    # if cmds.objExists(node):
    _historys = cmds.listHistory(node)

    if _historys:
        for _history in _historys:
            if cmds.nodeType(_history) == "skinCluster":
                skin_cluster = _history
                break
    return skin_cluster


def select_lod_joints(button_name:str='')->None:
    exists_joints:list = []
    _0joints = set()
    _1joints = set()
    _2joints = set()
    _3joints = set()
    _4joints = set()
    _5joints = set()
    _6joints = set()
    _7joints = set()

    if not button_name:
        return

    lod_num:str = button_name[:4]
    scene_name, root_node, lod_groups = check_nodes()

    if not scene_name:
        cmds.warning('not open scene')
        return

    joints_dict, file_path_dict = get_weight_file_jointsdict(weight_directory='Shenron')

    if not joints_dict:
        cmds.warning('not found joint data')
        return

    need_joints = [
                'root_jnt',
                'pelvis_jnt',
                'spine0_jnt',
                'spine1_jnt',
                'chest_jnt',
                'neck0_jnt',
                'neck1_jnt',
                'head_jnt',
                'L_clavicle_jnt',
                'L_shoulderTwist0_drv',
                'R_clavicle_jnt',
                'R_shoulderTwist0_drv',
                'neckTwist_drv',
                'L_clavicleTwist_drv',
                'R_clavicleTwist_drv'
                ]

    for shape, joints in joints_dict.items():
        _id = shape.split('Shape')[0][-1]
        if _id == '0':
            _0joints = _0joints | set(joints)
        if _id == '1':
            _1joints = _1joints | set(joints)
        if _id == '2':
            _2joints = _2joints | set(joints)
        if _id == '3':
            _3joints = _3joints | set(joints)
        if _id == '4':
            _4joints = _4joints | set(joints)
        if _id == '5':
            _5joints = _5joints | set(joints)
        if _id == '6':
            _6joints = _6joints | set(joints)
        if _id == '7':
            _7joints = _7joints | set(joints)

    _only_0_joints = list(_0joints-_1joints-_2joints-_3joints-_4joints-_5joints-_6joints-_7joints)
    _only_1_joints = list(_1joints-_2joints-_3joints-_4joints-_5joints-_6joints-_7joints)
    _only_2_joints = list(_2joints-_3joints-_4joints-_5joints-_6joints-_7joints)
    _only_3_joints = list(_3joints-_4joints-_5joints-_6joints-_7joints)
    _only_4_joints = list(_4joints-_5joints-_6joints-_7joints)
    _only_5_joints = list(_5joints-_6joints-_7joints)
    _only_6_joints = list(_6joints-_7joints)

    if lod_num == 'LOD0':
        _prev_joints = list(_only_0_joints)
    elif lod_num == 'LOD1':
        _prev_joints = list(_only_1_joints)
    elif lod_num == 'LOD3':
        _prev_joints = list(_only_3_joints)
    else:
        return

    for _j in _prev_joints:
        if cmds.objExists(_j) and _j not in need_joints and not cmds.listRelatives(_j, children=True, type='transform'):
            exists_joints.append(_j)

    cmds.select(exists_joints, replace=True)
    exists_joints = sorted(exists_joints)

    print(f'[ {len(exists_joints)} Joints]: [ {exists_joints} ]')

