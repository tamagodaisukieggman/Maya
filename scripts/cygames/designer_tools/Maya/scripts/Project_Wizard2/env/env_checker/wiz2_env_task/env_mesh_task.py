# -*- coding: utf-8 -*-

import os
import re
import typing as tp
import maya.cmds as cmds

try:
    import yaml
except Exception:
    cmds.error('ツールエラー: yamlモジュールがありません')

from ....common.maya_checker import utility as utils
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.data import ErrorType
from ....common.maya_checker_gui.controller import CheckerMainWindow

class Wiz2EnvCheckVertexColor(CheckTaskBase):
    """メッシュにバーテックスカラーがあればOK"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'バーテックスカラー'

    def exec_task_method(self):
        transforms = []
        # RootNodeData
        for root in self.maya_scene_data.root_nodes:
            if root.root_node_name.endswith('_col'):
                continue
            transforms.extend(root.get_all_mesh_transform())
        no_vtx_color_meshes = []
        if not transforms:
            return
        for mesh in transforms:
            color_set_list = cmds.polyColorSet(mesh, query=True, allColorSets=True)
            if not color_set_list:
                no_vtx_color_meshes.append(mesh)
        if len(no_vtx_color_meshes) > 0:
            self.set_error_data(
                'env_no_vertex_color', no_vtx_color_meshes, '頂点カラーがありません'
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        try:
            if 'env_no_vertex_color' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('env_no_vertex_color')
                for target in debug_targets:
                    try:
                        cmds.polyColorPerVertex(debug_targets, rgb=(1.0, 1.0, 1.0))
                    except Exception:
                        cmds.warning('バーテックスカラーの設定でエラー: ' + target)
        except Exception:
            cmds.error('Error: バーテックスカラー 修正')


class Wiz2EnvNameSpace(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'ネームスペースを含むTransform'

    def exec_task_method(self):
        """選択にネームスペースを含むTransformがあったらエラー"""
        transforms = []
        for root in self.maya_scene_data.root_nodes:
            transforms.extend(root.get_all_mesh_transform())
            transforms.append(root.full_path_name)
        if not transforms:
            self.set_error_data(
                'env_tranfrom_with_namespace',
                None,
                'メッシュがありません',
                is_reset_debug_data=False,
            )
            self.set_error_type(ErrorType.NOCHECKED)
            return
        transform_with_namespace = []
        for long_name in transforms:
            if long_name.find(':') > -1:
                transform_with_namespace.append(long_name)
        if transform_with_namespace:
            self.set_error_data(
                'env_tranfrom_with_namespace',
                transform_with_namespace,
                'namespaceが含まれるTransform',
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        """ネームスペースの削除"""
        renamed_items = []
        try:
            if 'env_tranfrom_with_namespace' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('env_tranfrom_with_namespace')
                for long_name in debug_targets:
                    if long_name.find(':') > -1:
                        name_without_namespace = long_name.split(':')[-1]
                        cmds.rename(long_name, name_without_namespace)
                        renamed_items.append(name_without_namespace)
        except Exception:
            cmds.error('Error: ネームスペースを含むTransform 修正')
            pass
        # ツール側の情報更新
        renamed_roots = []
        for renamed in renamed_items:
            parent = cmds.listRelatives(renamed, parent=True)
            if not parent:
                renamed_roots.append(renamed)
        # Rootとメッシュ名が代わり他のdebug_dataのオブジェクトパスが
        # 存在しなくなる可能性があるためリセット
        try:
            CheckerMainWindow._instance.initialize()
        except:
            pass

class Wiz2EnvMeshName(CheckTaskBase):
    """メッシュ名が背景モデル命名規則に沿っていればOK
    背景モデル命名規則: https://wisdom.cygames.jp/pages/viewpage.action?pageId=436230414
    """

    env_dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'メッシュ名'
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
                        'env_namespace_root_mesh', root.root_node_name,
                        'rootにネームスペースがある為チェックできません\n' +
                        '「ネームスペースを含むTransform」で修正してください',
                        is_reset_debug_data=False
                    )
                else:
                    self.set_error_data(
                        'env_wrong_root_name_mesh', root.root_node_name,
                        'rootの命名規則違反の為チェックできません',
                        is_reset_debug_data=False
                    )
                return
            bg_type = match_obj.group(1)
            self.check_root_name_pattern(root.root_node_name, bg_type)
            # コリジョンは別途チェック
            if root.root_node_name.endswith('_col'):
                collision_meshes = root.get_all_mesh_transform()
                if collision_meshes:
                    for mesh in collision_meshes:
                        self.check_mesh_name_pattern(mesh, bg_type, is_collision=True)
            else:
                bg_meshes = root.get_all_mesh_transform()
                if bg_meshes:
                    for mesh in bg_meshes:
                        self.check_mesh_name_pattern(mesh, bg_type, is_collision=False)

    def exec_fix_method(self):
        """出来る限り修正を試みる"""
        try:
            if 'env_short_name_mesh' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('env_short_name_mesh')
                for target in debug_targets:
                    self.try_fix_mesh_name(target)
        except Exception:
            pass
        try:
            if 'env_long_name_mesh' in self.debug_data.error_target_info.keys():
                debug_targets2 = self.get_debug_target_objects('env_long_name_mesh')
                for target in debug_targets2:
                    self.try_fix_mesh_name(target)
        except Exception:
            pass

    def check_root_name_pattern(self, root, bg_type):
        """Rootのグループ名をチェック
        背景メッシュのRoot: BGXXX_XXXX_XXXX_XX
        コリジョンのRoot  : BGXXX_XXXX_XXXX_XX_col
        Args:
            root (str): シーンのメッシュのRootグループ名
            bg_type (str): 背景のロケーション (a, b, c, e, r, w のどれか)
        """
        if not self.env_dict.get('env_root_' + bg_type, False) or not self.env_dict.get('name_parts_' + bg_type, False):
            self.set_error_data(
                'env_unknown_bg_type', root, '登録外のロケーション: ' + str(bg_type), is_reset_debug_data=False
            )
            return
        root_parts = root.split('_')
        # コリジョンと背景メッシュの命名の違いは最後の_colのみ
        if root_parts[-1] == 'col':
            del root_parts[-1]
        # メッシュ名のパーツ数が合わないと命名照合できない
        if len(root_parts) < len(self.env_dict['env_root_' + bg_type]):
            self.set_error_data(
                'env_short_name_root',
                root,
                'Rootの命名規則より短い名前',
                is_reset_debug_data=False,
            )
            return
        elif len(root_parts) > len(self.env_dict['env_root_' + bg_type]):
            self.set_error_data(
                'env_long_name_root', root, 'Rootの命名規則より長い名前', is_reset_debug_data=False
            )
            return
        # 命名チェック
        for idx, part in enumerate(self.env_dict['env_root_' + bg_type]):
            match_obj = re.match(
                self.env_dict['env_root_' + bg_type][part]['regex'], root_parts[idx]
            )
            if not match_obj:
                error_name = self.env_dict['env_root_' + bg_type][part]['error_name']
                error_message = self.env_dict['env_root_' + bg_type][part][
                    'error_message'
                ]
                self.set_error_data(
                    error_name, root, error_message, is_reset_debug_data=False
                )

    def check_mesh_name_pattern(self, mesh, bg_type, is_collision):
        """メッシュ名が命名規則にあっているかチェック
        背景メッシュ: ms_XXX_XXXX_XXXX01_XX_XX_XXXX
        属性ID _ ロケID(下3桁)_ (役割ID+ナンバリング3桁連番) _ カテゴリナンバリング _ アルファ類 _ サウンド属性 _ フラグ
        コリジョン  : ms_XXX_XXXX_XXXX01_XXX_XX
        属性ID _ ロケID(下3桁)_ (役割ID+ナンバリング3桁連番) _ カテゴリナンバリング _ コリジョン種類 _ サウンド属性
        Args:
            mesh (str): メッシュノード名
            bg_type (str): 背景のロケーション (a, b, c, e, r, w のどれか)
            is_collision (bool): コリジョンかどうか(Root名の最後が_colかどうかで別途判定)
        """
        if not self.env_dict.get('env_root_' + bg_type, False) or not self.env_dict.get('name_parts_' + bg_type, False):
            self.set_error_data(
                'env_unknown_bg_type', mesh, '登録外のロケーション: ' + str(bg_type), is_reset_debug_data=False
            )
            return
        mesh_short_name = mesh
        if mesh.rfind('|') > -1:
            mesh_short_name = mesh[mesh.rfind('|') + 1:]

        # メッシュ名のパーツ数が合わないと命名照合できない
        name_parts = mesh_short_name.split('_')
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
                'env_short_name_mesh',
                mesh,
                'メッシュの命名規則より短い名前',
                is_reset_debug_data=False,
            )
            return
        elif len(name_parts) > name_parts_max_len:
            self.set_error_data(
                'env_long_name_mesh', mesh, 'メッシュの命名規則より長い名前', is_reset_debug_data=False
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
                    regex = '^(ms)$'
                else:
                    regex = self.env_dict['name_parts_' + bg_type][part]['regex']
                match_obj = re.match(regex, name_parts[name_idx])
                if not match_obj:
                    error_name = self.env_dict['name_parts_' + bg_type][part][
                        'error_name'
                    ]
                    error_message = self.env_dict['name_parts_' + bg_type][part][
                        'error_message'
                    ]
                    self.set_error_data(
                        error_name, mesh, error_message, is_reset_debug_data=False
                    )
                else:
                    # 登録されたキーワードか
                    if part in self.env_dict['env_name_types']:
                        if (
                            match_obj.group(1)
                            not in self.env_dict['env_name_types'][part]
                        ):
                            self.set_error_data(
                                'not_registered_' + part + match_obj.group(1),
                                mesh,
                                '登録されていません(' + part + '): ' + match_obj.group(1),
                                is_reset_debug_data=False,
                            )
                name_idx += 1
            except Exception:
                pass

    def try_fix_mesh_name(self, mesh):
        """メッシュ名修正
        とりあえずRootではないグループがあり名前がメッシュよりは
        良さげだったらグループノード名をメッシュ名にする
        Args:
            mesh (str): 命名規則に沿っていないメッシュのフルパス
        """
        parents = cmds.listRelatives(mesh, parent=True)
        root = self.get_root_node(mesh)
        if parents[0] != root:
            mesh_short_name = mesh
            parent_short_name = parents[0]
            if mesh.find('|') > -1:
                mesh_short_name = mesh.split('|')[-1]
            if parents[0].find('|') > -1:
                parent_short_name = parents[0].split('|')[-1]
            if not mesh_short_name.startswith('ms_') and parent_short_name.startswith(
                'ms_'
            ):
                cmds.rename(mesh, parent_short_name)

    def get_root_node(self, node):
        if not node:
            return
        parents = cmds.listRelatives(node, parent=True, fullPath=True)
        if not parents:
            return node
        else:
            for p in parents:
                return get_root_node(p)


class Wiz2EnvMaterialPerMesh(CheckTaskBase):
    """1メッシュ1マテリアルならOK"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = '1メッシュ1マテリアル'

    def exec_task_method(self):
        self.set_error_type(ErrorType.NOERROR)
        mesh_transforms = []
        # RootNodeData
        for root in self.maya_scene_data.root_nodes:
            mesh_transforms.extend(root.get_all_mesh_transform())
        # メッシュがないならチェックしない
        if not mesh_transforms:
            self.set_error_type(ErrorType.NOCHECKED)
            return
        for mesh in mesh_transforms:
            shapes = cmds.listRelatives(mesh, type='shape', fullPath=True)
            shading_groups = cmds.listConnections(shapes, type='shadingEngine')
            if shading_groups:
                shading_groups = list(set(shading_groups))
            if shading_groups:
                assigned_materials = []
                for sg in shading_groups:
                    if sg == 'initialShadingGroup':
                        self.set_error_data('env_missing_material', mesh,
                                            'デフォルトマテリアルです',
                                            is_reset_debug_data=False)
                    else:
                        materials = cmds.ls(cmds.listConnections(sg), materials=True)
                        if materials:
                            assigned_materials.extend(materials)
                assigned_materials = list(set(assigned_materials))
                if not assigned_materials:
                    self.set_error_data('env_missing_material', mesh,
                                        'マテリアルがアサインされていません',
                                        is_reset_debug_data=False)
                elif len(assigned_materials) > 1:
                    self.set_error_data('env_multiple_material', mesh,
                                        '複数のマテリアル', is_reset_debug_data=False)
            else:
                self.set_error_data('env_missing_material', mesh,
                                    'マテリアルがアサインされていません',
                                    is_reset_debug_data=False)

    def exec_fix_method(self):
        """マテリアルのないメッシュ用に新規マテリアルをつくりアサインする
        マテリアル名はメッシュ名のmsをmtに置き換えたものにする
        """
        try:
            if 'env_missing_material' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('env_missing_material')
                if debug_targets:
                    for target in debug_targets:
                        self.apply_material(target)
        except Exception:
            cmds.error('Error: 1メッシュ1マテリアル Missing 修正')
        try:
            if 'env_multiple_material' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('env_multiple_material')
                if debug_targets:
                    for target in debug_targets:
                        self.reduceMaterial(target)
        except Exception:
            cmds.error('Error: 1メッシュ1マテリアル 複数のマテリアル 修正')

    def apply_material(self, mesh, mat_type='lambert'):
        if cmds.objExists(mesh):
            try:
                mesh_short_name = mesh
                if mesh.find('|') > -1:
                    mesh_short_name = mesh.split('|')[-1]
                mat_name = mesh_short_name
                if mesh_short_name.startswith('ms_'):
                    mat_name = mesh_short_name[len('ms_'):]
                    mat_name = 'mt_' + mat_name
                else:
                    mat_name = 'mt_' + mat_name
                shading_group = ''
                # メッシュの名前の既存のマテリアルがあればそれをアサイン
                if cmds.objExists(mat_name):
                    if cmds.objectType(mat_name) == 'lambert':
                        shading_groups = cmds.listConnections(
                            mat_name, type='shadingEngine'
                        )
                        if shading_groups:
                            shading_group = shading_groups[0]
                else:
                    # メッシュの名前のマテリアル(diffuse=1)を作る
                    mat_name = cmds.shadingNode(mat_type, name=mat_name, asShader=True)
                    cmds.setAttr('{0}.diffuse'.format(mat_name), 1)
                    shading_group = cmds.sets(
                        name='{0}SG'.format(mat_name),
                        empty=True,
                        renderable=True,
                        noSurfaceShader=True,
                    )
                    cmds.connectAttr(
                        '{0}.outColor'.format(mat_name),
                        '{0}.surfaceShader'.format(shading_group),
                    )
                # マテリアルをアサイン
                cmds.sets(mesh, e=True, forceElement=shading_group)
            except Exception as ex:
                cmds.error(ex)

    def reduceMaterial(self, mesh):
        """複数のマテリアルがアサインされているメッシュがあったら
        とりあえずテクスチャのついたマテリアル1個をアサインする
        テクスチャのついたマテリアルがない場合は最初のマテリアル1個をアサインする
        """
        shape = cmds.listRelatives(mesh, type='shape')
        if not shape:
            return
        shading_groups = cmds.listConnections(shape, type='shadingEngine')
        if not shading_groups:
            return
        shading_groups = list(set(shading_groups))
        if len(shading_groups) < 2:
            return
        replace_with = shading_groups[0]
        for shading_group in shading_groups:
            materials = cmds.ls(cmds.listConnections(shading_group), materials=1)
            file_nodes = cmds.listConnections(
                '{0}.color'.format(materials[0]), type='file'
            )
            if file_nodes:
                texture_file = cmds.getAttr('{0}.fileTextureName'.format(file_nodes[0]))
                if texture_file:
                    replace_with = shading_group
                    break
        cmds.sets(mesh, e=True, forceElement=replace_with)


class Wiz2EnvTransformFreeze(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'トップノード以下のフリーズ'

    def exec_task_method(self):
        transforms = []
        error_transforms = []
        for root in self.maya_scene_data.root_nodes:
            transforms.extend(root.get_all_mesh_transform())
        if not transforms:
            self.set_error_data(
                'env_transform_freeze_no_mesh',
                None,
                'メッシュがありません',
                is_reset_debug_data=False,
            )
            self.set_error_type(ErrorType.NOCHECKED)
            return
        for transform in transforms:
            if not self.is_transform_freeze(transform):
                error_transforms.append(transform)

        if len(error_transforms) > 0:
            self.set_error_data(
                'env_is_mesh_freeze', error_transforms, 'トップノード以下のフリーズされていません'
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        """Freezeする"""
        try:
            if 'env_is_mesh_freeze' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('env_is_mesh_freeze')
                for target in debug_targets:
                    try:
                        cmds.makeIdentity(target, apply=True)
                    except Exception:
                        print('Failed target: ' + target)
        except Exception:
            cmds.error('Error: トップノード以下のフリーズ 修正')
            pass

    def is_transform_freeze(self, mesh_name):
        """指定されたメッシュがFreezeされているかチェック
        Args:
            mesh_name (str): チェックするメッシュの名前
        Returns:
            bool: FreezeされていればTrue
        """
        if not cmds.objExists(mesh_name):
            raise ValueError('Mesh {0} does not exist.'.format(mesh_name))
        return (
            cmds.getAttr(mesh_name + '.translate')[0] == (0, 0, 0)
            and cmds.getAttr(mesh_name + '.rotate')[0] == (0, 0, 0)
            and cmds.getAttr(mesh_name + '.scale')[0] == (1, 1, 1)
        )


class Wiz2EnvDuplicateNodeNames(CheckTaskBase):
    """FBXエクスポートに含まれるTransform(mesh)ノード名の重複チェック
    選択配下のTransformに対して実行
    マテリアルは階層にならず、Maya上で名前を重複することはできないのでチェックしない
    Args:
        CheckTaskBase (class): commonのtaskでdefineされているクラス
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'Transform名の重複'

    def exec_task_method(self):
        if self.get_duplicate_transform_names_from_selection():
            self.set_error_data(
                'env_duplicate_tranfrom_names',
                self.get_duplicate_transform_names_from_selection(),
                'Transform名の重複'
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        if len(self.maya_scene_data.root_nodes) > 1:
            user_choice = cmds.confirmDialog(title='Confirm',
                                             message='複数のRootが選択されています\n' +
                                             '重複は別グループかもしれませんが続行しますか?',
                                             button=['OK', 'Cancel'], defaultButton='OK',
                                             cancelButton='Cancel', dismissString='Cancel')
            if user_choice == 'Cancel':
                return
        user_choice = cmds.confirmDialog(title='Confirm',
                                         message='重複名の片方に連番を付けます\n' +
                                         '先に選択されている方が優先的にリネームされます\n続行しますか?',
                                         button=['OK', 'Cancel'], defaultButton='OK',
                                         cancelButton='Cancel', dismissString='Cancel')
        if user_choice == 'Cancel':
            return
        try:
            same_name_dict = {}  # short_name, [long_name]
            if 'env_duplicate_tranfrom_names' in self.debug_data.error_target_info.keys():
                debug_targets = self.get_debug_target_objects('env_duplicate_tranfrom_names')
                # リネーム用ディクショナリ作成
                for long_name in debug_targets:
                    short_name = long_name.rsplit('|')[-1]
                    if short_name in same_name_dict:
                        same_name_dict[short_name].append(long_name)
                    else:
                        same_name_dict[short_name] = [long_name]
                # リネーム
                for short_name in same_name_dict:
                    long_names = same_name_dict[short_name]
                    for long_name in long_names[0:-1]:
                        next_name = cmds.duplicate(long_name)
                        cmds.delete(next_name)
                        cmds.rename(long_name, next_name)
        except Exception:
            cmds.error('Error: Transform名の重複 修正')
            pass

    def get_duplicate_transform_names_from_selection(self):
        """選択配下の重複しているtransform名を配列で返す
        Returns:
            str[]: 重複しているノード名のリスト
        """
        transforms = []
        for root in self.maya_scene_data.root_nodes:
            transforms.extend(root.get_all_mesh_transform())
        if not transforms:
            self.set_error_data(
                'env_duplicate_tranfrom_names',
                None,
                'メッシュがありません',
                is_reset_debug_data=False,
            )
            self.set_error_type(ErrorType.NOCHECKED)
            return
        all_duplicate_names = []
        checked_short_name_dict = {}  # short_name: long_name
        for long_name in transforms:
            short_name = long_name.rsplit('|')[-1]
            if short_name not in checked_short_name_dict:
                checked_short_name_dict[short_name] = long_name
            else:
                all_duplicate_names.append(checked_short_name_dict[short_name])
                all_duplicate_names.append(long_name)
        return all_duplicate_names


class EnvUnnecessaryHistory(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = '不要なヒストリ'

    def exec_task_method(self):
        self.register_error_info_to_mesh_descendants(
            self._find_objects_with_non_skin_history,
            'env_unnecessary_history',
            '不必要なヒストリを所有するオブジェクト',
        )

    @staticmethod
    def _find_objects_with_non_skin_history(mesh_names: tp.List[str]) -> tp.List[str]:
        """対象オブジェクトにskinCluster以外のヒストリーが入っていたらそのオブジェクトを返す。
        Args:
            mesh_names (List[str]): チェックするメッシュの名前のリスト。
        Returns:
            List[str]: skinCluster以外のヒストリーが入っているオブジェクトのリスト。
        """
        objects_with_non_skin_history = []
        mesh_names = utils.get_shapes(mesh_names)

        for mesh_name in mesh_names:
            if not cmds.objExists(mesh_name):
                raise ValueError('Mesh {0} does not exist.'.format(mesh_name))

            history_nodes = cmds.listHistory(mesh_name, il=2, pdo=True)
            if not history_nodes:
                continue

            has_non_skin_history = False
            for node in history_nodes:
                if cmds.nodeType(node) != 'skinCluster':
                    has_non_skin_history = True
                    break

            if has_non_skin_history:
                objects_with_non_skin_history.append(mesh_name)

        return objects_with_non_skin_history

    def exec_fix_method(self):
        if 'env_unnecessary_history' in self.debug_data.error_target_info.keys():
            debug_targets = self.get_debug_target_objects('env_unnecessary_history')
            for item in debug_targets:
                cmds.delete(item, constructionHistory=True)


def get_root_node(node):
    if not node:
        return
    parents = cmds.listRelatives(node, parent=True, fullPath=True)
    if not parents:
        return node
    else:
        for p in parents:
            return get_root_node(p)
