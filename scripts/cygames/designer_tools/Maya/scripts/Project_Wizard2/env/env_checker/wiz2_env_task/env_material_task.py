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


class Wiz2EnvUnusedMaterial(CheckTaskBase):
    """
    シーン内でアサインされていない（未使用）マテリアルをチェック
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = '未使用マテリアル'

    def exec_task_method(self):
        materials = list_all_materials_in_scene_except_defaults()
        if not materials:
            self.set_error_data(
                'env_material_type_no_mesh',
                None,
                'マテリアルがありません',
                is_reset_debug_data=False,
            )
            self.set_error_type(ErrorType.NOCHECKED)
            return

        unused_materials = self.get_unused_materials(materials)

        if unused_materials:
            self.set_error_data(
                'wiz2_env_unused_material', unused_materials, '使用されていないマテリアル'
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        try:
            if 'wiz2_env_unused_material' in self.debug_data.error_target_info.keys():
                error_targets = self.debug_data.error_target_info[
                    'wiz2_env_unused_material'
                ]['target_objects']
                cmds.delete(error_targets)
        except Exception:
            cmds.error('Error: 未使用マテリアル 修正')

    def get_unused_materials(self, all_materials):
        """
        デフォルトマテリアル以外でシーン内でアサインされていない（使用されていない）マテリアルを返す
        Returns:
            List[str]: 使用されていないマテリアルのリスト
        """
        all_meshes = cmds.ls(type='mesh')
        assigned_materials = []
        for mesh in all_meshes:
            shading_groups = cmds.listConnections(mesh, type='shadingEngine')
            if shading_groups is None:
                continue
            for shading_group in shading_groups:
                materials = cmds.ls(cmds.listConnections(shading_group), materials=True)
                if materials is None:
                    continue
                assigned_materials.extend(materials)

        assigned_materials = list(set(assigned_materials))
        unused_materials = [
            material for material in all_materials if material not in assigned_materials
        ]
        return unused_materials


class Wiz2EnvMaterialName(CheckTaskBase):
    env_dict = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'マテリアル名'
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
        self.set_error_type(ErrorType.NOERROR)
        # メッシュがないならチェックしない
        if not self.maya_scene_data.root_nodes:
            self.set_error_type(ErrorType.NOCHECKED)
            return
        # RootNodeData
        for root in self.maya_scene_data.root_nodes:
            match_obj = re.match(self.env_dict['root_location_regex'], root.root_node_name)
            if not match_obj:
                if root.root_node_name.find(':'):
                    self.set_error_data(
                        'env_namespace_root_mat', root.root_node_name,
                        'rootにネームスペースがある為チェックできません',
                        is_reset_debug_data=False
                    )
                else:
                    self.set_error_data(
                        'env_wrong_root_name_mat', root.root_node_name,
                        'rootの命名規則違反の為チェックできません',
                        is_reset_debug_data=False
                    )
                return
            bg_type = match_obj.group(1)
            # コリジョンは別途チェック
            if root.root_node_name.endswith('_col'):
                collision_meshes = root.get_all_mesh_transform()
                if collision_meshes:
                    shapes = utils.get_shapes(collision_meshes)
                    collision_materials = utils.get_assigned_material(shapes)
                    if collision_materials:
                        for material in collision_materials:
                            self.check_material_name_pattern(material, bg_type, is_collision=True)
            else:
                bg_meshes = root.get_all_mesh_transform()
                if bg_meshes:
                    for mesh in bg_meshes:
                        shapes = utils.get_shapes(bg_meshes)
                        bg_materials = utils.get_assigned_material(shapes)
                        if not bg_materials:
                            self.set_error_data('env_missing_material', mesh,
                                                'マテリアルがアサインされていません',
                                                is_reset_debug_data=False)
                        else:
                            for material in bg_materials:
                                self.check_material_name_pattern(material, bg_type, is_collision=False)

    def check_material_name_pattern(self, material, bg_type, is_collision):
        """マテリアル名が命名規則にあっているかチェック
        背景       : mt_XXX_XXXX_XXXX01_XX_XX_XXXX
        属性ID _ ロケID(下3桁)_ (役割ID+ナンバリング3桁連番) _ カテゴリナンバリング _ アルファ類 _ サウンド属性 _ フラグ
        コリジョン  : mt_XXX_XXXX_XXXX01_XXX_XX
        属性ID _ ロケID(下3桁)_ (役割ID+ナンバリング3桁連番) _ カテゴリナンバリング _ コリジョン種類 _ サウンド属性
        Args:
            material (str): マテリアルノード名
            bg_type (str): 背景のロケーション (a, b, c, e, r, w のどれか)
            is_collision (bool): コリジョンかどうか(Root名の最後が_colかどうかで別途判定)
        """
        # マテリアル名のパーツ数が合わないと命名照合できない
        name_parts = material.split('_')
        # env_info.yamlのname_parts_x には背景メッシュとコリジョンメッシュの項目両方入っている
        if is_collision:
            # shader_typeとimport_flagの分引く
            name_parts_max_len = len(self.env_dict['name_parts_' + bg_type]) - len(self.env_dict['collision_exclude_parts'])
            # サウンド属性はオプショナル (2023/09/14)
            name_parts_min_len = name_parts_max_len - len(self.env_dict['collision_optional_parts'])
        else:
            # collision_typeの分引く
            name_parts_max_len = len(self.env_dict['name_parts_' + bg_type]) - len(self.env_dict['mesh_exclude_parts'])
            # サウンド属性、フラグはオプショナル (2023/09/14)
            name_parts_min_len = name_parts_max_len - len(self.env_dict['mesh_optional_parts'])
        if len(name_parts) < name_parts_min_len:
            self.set_error_data(
                'env_short_name_mat',
                material,
                'マテリアルの命名規則より短い名前',
                is_reset_debug_data=False,
            )
            return
        elif len(name_parts) > name_parts_max_len:
            self.set_error_data(
                'env_long_name_mat', material, 'マテリアルの命名規則より長い名前', is_reset_debug_data=False
            )
            return
        # 命名チェック
        name_idx = 0
        for idx, part in enumerate(self.env_dict['name_parts_' + bg_type]):
            # コリジョンでチェックしないパーツの定義はスキップ
            if is_collision:
                if part in self.env_dict['collision_exclude_parts']:
                    continue
            else:
                if part in self.env_dict['mesh_exclude_parts']:
                    continue
            # オプショナルのパーツ（必須パーツはオプショナルの後ろにはない）
            if is_collision:
                if part in self.env_dict['collision_optional_parts']:
                    if len(name_parts)-1 < idx:
                        break
            else:
                if part in self.env_dict['mesh_optional_parts']:
                    if len(name_parts)-1 < idx:
                        break
            try:
                if idx == 0:
                    regex = '^(mt)$'
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
                        error_name, material, error_message, is_reset_debug_data=False
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
                                material,
                                '登録されていません' + matchObj.group(1),
                                is_reset_debug_data=False,
                            )
                name_idx += 1
            except Exception as ex:
                print(ex)


class Wiz2EnvMaterialNameSameAsMesh(CheckTaskBase):
    env_dict = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'メッシュ名とマテリアル名の一致'
        yaml_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..', 'wiz2_env_settings', 'env_info.yaml'
            )
        )
        if not os.path.exists(yaml_path):
            cmds.error('ツールエラー: env_info.yamlが見つかりませんでした')
        with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
            self.env_dict = yaml.safe_load(yaml_file)
        if self.env_dict is None:
            cmds.error('ツールエラー: env_info.yamlの読み込みに失敗しました')
            return

    def exec_task_method(self):
        meshes = []
        self.set_error_type(ErrorType.NOERROR)
        # メッシュがないならチェックしない
        if not self.maya_scene_data.root_nodes:
            self.set_error_type(ErrorType.NOCHECKED)
            return
        # RootNodeData
        for root in self.maya_scene_data.root_nodes:
            match_obj = re.match(self.env_dict['root_location_regex'], root.root_node_name)
            if not match_obj:
                if root.root_node_name.find(':'):
                    self.set_error_data(
                        'env_namespace_root_mat2', root.root_node_name,
                        'rootにネームスペースがある為チェックできません',
                        is_reset_debug_data=False
                    )
                else:
                    self.set_error_data(
                        'env_wrong_root_name_mat2', root.root_node_name,
                        'rootの命名規則違反の為チェックできません',
                        is_reset_debug_data=False
                    )
                return
            meshes.extend(root.get_all_mesh_transform())
        wrong_name_materials = []
        for mesh in meshes:
            shapes = utils.get_shapes([mesh])
            materials = utils.get_assigned_material(shapes)
            if not materials:
                self.set_error_type(ErrorType.NOCHECKED)
                return
            materials = list(set(materials))
            for mat in materials:
                # フルパス > メッシュの名前only
                mesh_name = mesh.split('|')[-1]
                # メッシュの名前からms_を除く
                mesh_name = mesh_name[len('ms_'):]
                # マテリアルの名前からmt_を除く
                mat_name = mat[len('mt_'):]
                if mesh_name != mat_name:
                    wrong_name_materials.append(mat)
                    self.set_error_data(
                        'mesh_mat_name_different',
                        mat,
                        'マテリアル名が一致しません' + mat,
                        is_reset_debug_data=True,
                    )
        if not wrong_name_materials:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        """マテリアル名をメッシュ名と同じにリネームする
        マテリアルが他のメッシュから参照されている場合はユーザーにお知らせしリネームしない
        """
        try:
            if 'mesh_mat_name_different' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('mesh_mat_name_different')
                if debug_targets:
                    for mat in debug_targets:
                        all_mats = list_all_materials_in_scene_except_defaults()
                        assigned_meshes = []
                        for m in all_mats:
                            if m == mat:
                                con = cmds.listConnections('{0}.outColor'.format(m))
                                meshes = cmds.listConnections(con, type='mesh')
                                assigned_meshes.extend(meshes)
                                if not assigned_meshes:
                                    continue
                                # 1メッシュ1マテリアルのはずなので
                                if len(assigned_meshes) == 1:
                                    mesh = assigned_meshes[0]
                                    # フルパス > メッシュの名前only
                                    mesh_name = mesh.split('|')[-1]
                                    # メッシュの名前からms_を除く
                                    mesh_name = mesh_name[len('ms_'):]
                                    cmds.rename(mat, 'mt_' + mesh_name)
                                elif len(assigned_meshes) > 1:
                                    cmds.warning('{0}は複数のメッシュから参照されているためリネームできません\n'.format(mat) +
                                                 '\n'.join(assigned_meshes))
                                else:
                                    cmds.error('アサインされているメッシュがありません: ' + mat)
        except Exception:
            cmds.error('Error: メッシュ名とマテリアル名の一致 修正')


class Wiz2EnvMaterialType(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'マテリアルタイプ'

    def exec_task_method(self):
        self.set_error_type(ErrorType.NOERROR)
        bg_meshes = []
        # RootNodeData
        for root in self.maya_scene_data.root_nodes:
            # コリジョン以外のメッシュ
            if not root.root_node_name.endswith('_col'):
                bg_meshes.extend(root.get_all_mesh_transform())
        # メッシュがないならチェックしない
        if not bg_meshes:
            self.set_error_data(
                'env_material_type_no_mesh',
                None,
                'メッシュがありません',
                is_reset_debug_data=False,
            )
            self.set_error_type(ErrorType.NOCHECKED)
            return
        bg_materials = []
        if bg_meshes:
            shapes = utils.get_shapes(bg_meshes)
            bg_materials = utils.get_assigned_material(shapes)
        if not bg_materials:
            self.set_error_type(ErrorType.NOCHECKED)
            return
        for mat in bg_materials:
            if cmds.nodeType(mat) != 'lambert':
                self.set_error_data(
                    'env_not_lambert', mat, 'lambertではありません', is_reset_debug_data=False
                )
            elif cmds.getAttr('{0}.diffuse'.format(mat)) != 1:
                self.set_error_data(
                    'env_not_diffuse_1',
                    mat,
                    'Diffuseが1ではありません(unityシェーダ内のカラーにも影響)',
                    is_reset_debug_data=False,
                )

    def exec_fix_method(self):
        try:
            if 'env_not_lambert' in self.debug_data.error_target_info.keys():
                not_lambert_mats = self.debug_data.error_target_info['env_not_lambert'][
                    'target_objects'
                ]
                if not_lambert_mats:
                    self.replace_with_new_lambert(not_lambert_mats)
        except Exception:
            cmds.error('Error: マテリアルタイプ lambertではない 修正')
        try:
            if 'env_not_diffuse_1' in self.debug_data.error_target_info.keys():
                not_diffuse_1_mats = self.debug_data.error_target_info[
                    'env_not_diffuse_1'
                ]['target_objects']
                for mat in not_diffuse_1_mats:
                    cmds.setAttr('{0}.diffuse'.format(mat), 1)
        except Exception:
            cmds.error('Error: マテリアルタイプ Diffuseが1ではない 修正')

    def replace_with_new_lambert(self, not_lambert_mats):
        for material in not_lambert_mats:
            # マテリアルにアサインされたメッシュをリスト
            cmds.hyperShade(o=material)
            # 新規lambertマテリアル作成
            tmp_mat_name = 'env_material_task_Wiz2EnvMaterialType_tmp_material'
            mat_name = cmds.shadingNode('lambert', name=tmp_mat_name, asShader=True)
            cmds.setAttr('{0}.diffuse'.format(mat_name), 1)
            # オリジナルのマテリアルのノードを引き継ぐ(file, bump2d, shadingEngineのみ対応)
            orig_mat_name = material
            orig_file = self.get_file_node(material)
            orig_bump2d = self.get_bump2d(material)
            orig_shading_engine = self.get_shading_engine(material)
            cmds.connectAttr(
                '{0}.outColor'.format(orig_file),
                '{0}.color'.format(mat_name),
                force=True,
            )
            cmds.connectAttr(
                '{0}.outNormal'.format(orig_bump2d),
                '{0}.normalCamera'.format(mat_name),
                force=True,
            )
            # メッシュはShadingEngineに紐づいているので新しいマテリアルがアサインされる
            cmds.connectAttr(
                '{0}.outColor'.format(mat_name),
                '{0}.surfaceShader'.format(orig_shading_engine),
                force=True,
            )
            # オリジナルのマテリアルを削除
            cmds.delete(material)
            # 新規lambertをオリジナルのマテリアルの名前にリネーム
            cmds.rename(mat_name, orig_mat_name)

    def get_file_node(self, material):
        conns = cmds.listConnections(material)
        for con in conns:
            if cmds.objectType(con) == 'file':
                return con

    def get_bump2d(self, material):
        conns = cmds.listConnections(material)
        for con in conns:
            if cmds.objectType(con) == 'bump2d':
                return con

    def get_shading_engine(self, material):
        conns = cmds.listConnections(material)
        for con in conns:
            if cmds.objectType(con) == 'shadingEngine':
                return con


def list_all_materials_in_scene_except_defaults():
    """デフォルト以外のシーン内全てのマテリアルを返す
    Returns:
        str[]: マテリアル名
    """
    defalt_material_types = ['standardSurface', 'particleCloud']
    all_materials = cmds.ls(materials=True)
    materials = []
    for mat in all_materials:
        if cmds.objectType(mat) == 'lambert':
            # デフォルトlambertは含まない
            shading_groups = cmds.listConnections(mat, type='shadingEngine')
            if 'initialShadingGroup' in shading_groups:
                continue
        if cmds.objectType(mat) not in defalt_material_types:
            materials.append(mat)
    return materials