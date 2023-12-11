# -*- coding: utf-8 -*-

import re
import os

import maya.cmds as cmds

try:
    import yaml
except Exception:
    cmds.error('ツールエラー: yamlモジュールがありません')

from ....common.maya_checker import utility as utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType


class Wiz2EnvTextureName(CheckTaskBase):
    env_dict = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'テクスチャ名'
        yaml_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..', 'wiz2_env_settings', 'env_info.yaml'
            )
        )
        if not os.path.exists(yaml_path):
            cmds.error('ツールエラー: env_info.yamlが見つかりませんでした')
        self.env_dict = None
        with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
            self.env_dict = yaml.safe_load(yaml_file)
        if self.env_dict is None:
            cmds.error('ツールエラー: env_info.yamlの読み込みに失敗しました')
            return

    def exec_task_method(self):
        found_texture = False
        self.set_error_type(ErrorType.NOERROR)
        # メッシュがないならチェックしない
        if not self.maya_scene_data.root_nodes:
            self.set_error_type(ErrorType.NOCHECKED)
            return
        # RootNodeData
        for root in self.maya_scene_data.root_nodes:
            # コリジョンはテクスチャなし
            if root.root_node_name.endswith('_col'):
                continue
            bg_meshes = root.get_all_mesh_transform()
            if bg_meshes:
                bg_materials = []
                shapes = utils.get_shapes(bg_meshes)
                bg_materials = utils.get_assigned_material(shapes)
                if not bg_materials:
                    continue
                files = []
                for material in bg_materials:
                    files.extend(get_files_from_material(material))
                files = list(set(files))
                textures = []
                for file_node in files:
                    texture = cmds.getAttr('%s.fileTextureName' % file_node)
                    texture = texture.replace('\\', '/')
                    if texture not in textures:
                        textures.append(texture)
                if textures:
                    found_texture = True
                    for texture in textures:
                        match_obj = re.match(self.env_dict['root_location_regex'], root.root_node_name)
                        if not match_obj:
                            if root.root_node_name.find(':'):
                                self.set_error_data(
                                    'env_namespace_root_texture', root.root_node_name,
                                    'rootにネームスペースがある為チェックできません',
                                    is_reset_debug_data=False
                                )
                            else:
                                self.set_error_data(
                                    'env_wrong_root_name_texture', root.root_node_name,
                                    'rootの命名規則違反の為チェックできません',
                                    is_reset_debug_data=False
                                )
                            return
                        bg_type = match_obj.group(1)
                        self.check_texture_name_pattern(texture, bg_type)
        if self.maya_scene_data.root_nodes and not found_texture:
            self.set_error_type(ErrorType.NOCHECKED)
            return

    def check_texture_name_pattern(self, texture, bg_type):
        """テクスチャ名が命名規則にあっているかチェック
        背景       : mt_XXX_XXXX_XXXX01_XX_XX_XXXX
        属性ID _ ロケID(下3桁)_ (役割ID+ナンバリング3桁連番) _ カテゴリナンバリング _ アルファ類 _ サウンド属性 _ フラグ
        コリジョン  : mt_XXX_XXXX_XXXX01_XXX_XX
        属性ID _ ロケID(下3桁)_ (役割ID+ナンバリング3桁連番) _ カテゴリナンバリング _ コリジョン種類 _ サウンド属性
        Args:
            texture (str): テクスチャパスもしくはテクスチャファイル名
            bg_type (str): 背景のロケーション (a, b, c, e, r, w のどれか)
            is_collision (bool): コリジョンかどうか(Root名の最後が_colかどうかで別途判定)
        """
        texture_file_name = os.path.basename(texture)
        file_name_only = texture_file_name.split('.')[0]
        # テクスチャ名のパーツ数が合わないと命名照合できない
        name_parts = file_name_only.split('_')
        # env_info.yamlのname_parts_x はメッシュ、マテリアル、テクスチャで共有している
        # collision_typeの分引く
        name_parts_max_len = len(self.env_dict['name_parts_' + bg_type]) - len(self.env_dict['texture_exclude_parts'])
        # サウンド属性、フラグはオプショナル (2023/09/14)
        name_parts_min_len = name_parts_max_len - len(self.env_dict['texture_optional_parts'])
        if len(name_parts) < name_parts_min_len:
            self.set_error_data(
                'env_short_name_tex',
                texture_file_name,
                'テクスチャの命名規則より短い名前',
                is_reset_debug_data=False,
            )
            return
        elif len(name_parts) > name_parts_max_len:
            self.set_error_data(
                'env_long_name_tex', texture_file_name, 'テクスチャの命名規則より長い名前', is_reset_debug_data=False
            )
            return
        # 命名チェック
        name_idx = 0
        for idx, part in enumerate(self.env_dict['name_parts_' + bg_type]):
            if part in self.env_dict['texture_exclude_parts']:
                continue
            # オプショナルのパーツ（必須パーツはオプショナルの後ろにはない）
            if part in self.env_dict['texture_optional_parts']:
                if len(name_parts)-1 < idx:
                    break
            try:
                if idx == 0:
                    regex = '^(tx)$'
                else:
                    regex = self.env_dict['name_parts_' + bg_type][part]['regex']
                matchObj = re.match(regex, name_parts[name_idx])
                if not matchObj:
                    error_name = self.env_dict['name_parts_' + bg_type][part][
                        'error_name'
                    ]
                    error_message = self.env_dict['name_parts_' + bg_type][part][
                        'error_message'
                    ]
                    self.set_error_data(
                        error_name, texture, error_message, is_reset_debug_data=False
                    )
                else:
                    # 登録されたキーワードか
                    if part in self.env_dict['env_name_types']:
                        if (
                            matchObj.group(1)
                            not in self.env_dict['env_name_types'][part]
                        ):
                            self.set_error_data(
                                'not_registered_' + part,
                                texture,
                                '登録されていません' + matchObj.group(1),
                                is_reset_debug_data=False,
                            )
                name_idx += 1
            except Exception:
                pass


def get_files_from_material(mat_name):
    """
    マテリアルについているfileを返します。
    param mat_name: string. マテリアル名。
    return: string file名
    """
    files = cmds.listConnections(mat_name, source=True, destination=False, type='file')
    if not files:
        files = []
    conns = cmds.listConnections(mat_name, source=True, destination=False)
    if conns:
        for conn in conns:
            files2 = get_files_from_material(conn)
            files.extend(files2)
        files = list(set(files))
    return files
