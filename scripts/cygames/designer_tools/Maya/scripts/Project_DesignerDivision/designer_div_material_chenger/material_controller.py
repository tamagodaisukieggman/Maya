# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import itertools

import maya.cmds as cmds
import maya.mel as mel

from . import material_utility as utility
from . import tool_define as tool_define
from .project_data import project_define as pj_define
from .project_data import project_data_method as data_method
from .project_data import project_edit_method as edit_method

try:
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(tool_define)
reload(pj_define)
reload(utility)
reload(data_method)
reload(edit_method)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MaterialController(object):

    # ==================================================
    def __init__(self):

        self.SEPARATE_STR = tool_define.SEPARATE_STR
        self.material_type_list = []

        self.scene_path = ''
        self.tex_root_path = ''

        self.target_mesh_list = []
        self.material_data_list = []

    # ==================================================
    def initialize(self, root_node, scene_path=None, tex_root_path=None):

        self.material_type_list = pj_define.MTL_TYP_LIST
        self.scene_path = ''
        self.tex_root_path = ''
        self.target_mesh_list = []
        self.material_data_list = []

        self.scene_path, self.tex_root_path = self.__get_scene_pathes(scene_path, tex_root_path)
        if not self.scene_path or not self.tex_root_path:
            return

        self.target_mesh_list = data_method.get_target_mesh_list(root_node)
        self.__initialize_material_data_list(self.target_mesh_list)

    # ==================================================
    def change_material_by_type(self, material_type, target_mesh_str=''):

        self.__update_material_data_list()
        all_texture_list = self.__get_all_texture_path_list()

        # 適用するマテリアルデータを選別する
        apply_material_data_list = []
        no_apply_materil_data_list = []
        for material_data in self.material_data_list:

            is_target = False

            if material_data.type == material_type:

                if target_mesh_str:
                    is_target = material_data.mesh.find(target_mesh_str) >= 0
                else:
                    is_target = True

            if is_target:
                print('適用:{} => {}'.format(material_data.name, material_data.mesh))
                apply_material_data_list.append(material_data)
            else:
                no_apply_materil_data_list.append(material_data)

        # マテリアルの適用
        for material_data in apply_material_data_list:
            print('=' * 20)
            print('{} セットアップ開始: {}'.format(material_data.name, material_data.mesh))
            print('=' * 20)
            self.__apply_material(material_data, all_texture_list)
            self.__update_material_data_list()

        # 不要マテリアルの除去
        for material_data in no_apply_materil_data_list:

            # ベースマテリアルは触らない
            if material_data.is_base_material:
                continue

            if material_data.exists and not material_data.is_assigned:
                self.__remove_material(material_data)
                self.__update_material_data_list()
            else:
                self.__execute_project_commands(material_data, False)

    # ==================================================
    def __get_scene_pathes(self, scene_path=None, tex_root_path=None):

        this_scene_path = scene_path
        if not this_scene_path:
            this_scene_path = cmds.file(q=True, sn=True)

        this_tex_root = tex_root_path
        if not this_tex_root:
            if this_scene_path:
                scene_dir = os.path.dirname(this_scene_path)
                this_tex_root = '{}/{}'.format(os.path.dirname(scene_dir), 'sourceimages')

        return this_scene_path, this_tex_root

    # ==================================================
    def __initialize_material_data_list(self, target_mesh_list):

        self.material_data_list = []

        for mesh in target_mesh_list:

            materials = self.__get_assigned_material_list(mesh)

            for material, material_type in itertools.product(materials, self.material_type_list):

                # このツールではマテリアルは全て「this_base_name + tool_define.SEPARATE_STR + ???」になるはず
                this_base_name = material.split(self.SEPARATE_STR)[0]

                # マテリアルデータを作るかどうかフィルタリング
                if not data_method.is_possible_mesh_type_pair(mesh, material_type):
                    continue

                # マテリアルデータ作成と登録
                this_data = MaterialData(this_base_name, material_type)
                this_data.mesh = mesh
                self.material_data_list.append(this_data)

        self.__update_material_data_list()

    # ==================================================
    def __update_material_data_list(self):

        if not self.material_data_list:
            return

        for material_data in self.material_data_list:

            # material名作成
            material_data.name = data_method.get_material_name(material_data.base_name, material_data.type)
            # shaderファイルパス取得
            material_data.shader = data_method.get_shader_file(material_data.base_name, material_data.type)
            # textureパスと接続アトリビュート取得
            material_data.texture_connect_dict = data_method.get_texture_connect_dict(material_data.base_name, material_data.type)
            # アトリビュートの値取得
            material_data.attr_dict = data_method.get_attr_dict(material_data.base_name, material_data.type)
            # プロジェクト処理キー取得
            material_data.project_command_list = data_method.get_project_command_list(material_data.base_name, material_data.type)
            # マテリアルが存在しているかどうか
            material_data.exists = cmds.objExists(material_data.name)
            # マテリアルが接続中かどうか
            material_data.is_assigned = self.__is_assigned_material(material_data.name, material_data.mesh)
            # デフォルトのマテリアルかどうか
            material_data.is_base_material = (material_data.base_name == material_data.name)

            # print('*' * 20)
            # material_data.print_data()

    # ==================================================
    def __get_assigned_material_list(self, obj):

        shapes = cmds.listRelatives(obj, s=True, f=True)
        engins = cmds.listConnections(shapes, s=False, d=True, t='shadingEngine')
        return cmds.ls(cmds.listConnections(engins, s=True, d=False), mat=True)

    # ==================================================
    def __is_assigned_material(self, material_name, mesh):

        return material_name in self.__get_assigned_material_list(mesh)

    # ==================================================
    def __get_all_texture_path_list(self):

        result_list = []
        for curDir, dirs, files in os.walk(self.tex_root_path):
            for file in files:
                if file.endswith('.tga') or file.endswith('.psd'):
                    result_list.append(os.path.join(curDir, file))
        return result_list

    # ==================================================
    def __apply_material(self, material_data, all_texture_list):

        if material_data.exists:
            # 既出ならテクスチャを読み込んで置き換え
            self.__set_textures(material_data, all_texture_list)
            self.__execute_project_commands(material_data, True)
            self.__replace_materials(material_data)
        else:
            # なければ初回セットアップ
            target_material = edit_method.create_project_material(material_data.name, material_data.shader, material_data.mesh)

            if not target_material:
                print('マテリアルの作成に失敗 : {}'.format(target_material))
                return

            self.__set_textures(material_data, all_texture_list)
            self.__set_attr_values(material_data)
            self.__execute_project_commands(material_data, True)
            self.__replace_materials(material_data)

    # ==================================================
    def __set_textures(self, material_data, all_texture_list):

        for connect_attr, tex_file in list(material_data.texture_connect_dict.items()):

            target_path = ''
            for texture_path in all_texture_list:
                if texture_path.endswith(tex_file):
                    target_path = texture_path
                    break

            result = False
            if target_path:
                result = utility.set_texture(material_data.name, connect_attr, target_path)

            if not result:
                print('テスクチャセット失敗: {}'.format(tex_file))

    # ==================================================
    def __set_attr_values(self, material_data):

        for attr, value in list(material_data.attr_dict.items()):
            result = utility.set_attr_value(material_data.name, attr, value)

            if not result:
                print('アトリビュートセット失敗: {}'.format(attr))

    # ==================================================
    def __execute_project_commands(self, material_data, is_setting_up):

        for command_key in material_data.project_command_list:
            if is_setting_up:
                edit_method.execute_project_command_settingup(command_key, material_data)
            else:
                edit_method.execute_project_command_removing(command_key, material_data)

    # ==================================================
    def __replace_materials(self, material_data):

        src_material = None
        dst_material = material_data.name

        for ref_material_data in self.material_data_list:
            if not ref_material_data.base_name == material_data.base_name:
                continue
            if not ref_material_data.mesh == material_data.mesh:
                continue
            if not ref_material_data.is_assigned:
                continue
            src_material = ref_material_data.name
            break

        if not src_material:
            return
        utility.replace_material(src_material, dst_material, material_data.mesh)

    # ==================================================
    def __remove_material(self, material_data):

        target_material = material_data.name
        if not cmds.objExists(target_material):
            return

        # 削除対象の関連ノードを先に取得
        all_file_nodes = utility.get_all_file_node_list(target_material)
        shading_engine = utility.get_shading_engine(target_material)

        # マテリアルの削除
        cmds.delete(target_material)

        # 関連ノードの削除
        utility.delete_file_and_2d_nodes(all_file_nodes)
        if shading_engine:
            cmds.delete(shading_engine)
        self.__execute_project_commands(material_data, False)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MaterialData(object):

    # ==================================================
    def __init__(self, material_base, material_type):

        self.base_name = material_base
        self.type = material_type
        self.name = None

        self.mesh = []

        self.shader = None

        self.texture_connect_dict = {}
        self.attr_dict = {}
        self.project_command_list = []

        self.exists = False
        self.is_assigned = False
        self.is_base_material = False

    # ==================================================
    def print_data(self):

        print('=' * 20)
        print('{}: {}({})'.format('MaterialName', self.name, self.base_name))
        print('{}: {}'.format('Exists', str(self.exists)))
        print('{}: {}'.format('IsAssigned', str(self.is_assigned)))
        print('{}: {}'.format('Mesh', str(self.mesh)))
        print('{}: {}'.format('ShaderFile', self.shader))
        print('{}:'.format('TextureConnect'))
        for key in self.texture_connect_dict:
            print(' {} ==> {}'.format(self.texture_connect_dict[key], key))
        print('{}:'.format('AttrValue'))
        for key in self.attr_dict:
            print(' {} ==> {}'.format(self.attr_dict[key], key))
