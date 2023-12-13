# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from .. import glp_common
from ..glp_common.classes import neck_normal
from ..glp_common.classes import info as cmn_info
from ..glp_common.classes import body_shape as body_shape_classes
from ..glp_common.classes import vertex_color_info as vetex_color_info_classes
from ..glp_common.utility import normal_to_uv as normal_to_uv_utility
from ..glp_common.utility import open_maya as om_utility
from . import constants
from . import commands

import maya.cmds as cmds

try:
    # maya 2022-
    from builtins import zip
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(base_common)
reload(glp_common)
reload(neck_normal)
reload(body_shape_classes)
reload(vetex_color_info_classes)
reload(normal_to_uv_utility)
reload(om_utility)
reload(constants)
reload(commands)


class CharaExporter(object):

    def __init__(self, target_file_path):

        self.target_file_path = target_file_path

        self.chara_info = None

        self.export_target_list = None
        self.fix_export_target_list = None

        self.logger = None

        self.keep_temp_file = False
        self.is_ascii = False
        self.is_icon_model = False
        self.show_in_explorer = False
        self.export_base_setting = False
        self.export_bodydiff_id_list = []
        self.body_shape_check_enabled = True

        self.exporter_item_list = None

        self.temp_file_path = None

    def initialize(self):

        self.chara_info = cmn_info.chara_info.CharaInfo()
        self.chara_info.create_info(file_path=self.target_file_path)

        if not self.chara_info.exists:
            return False

        self.exporter_item_list = []

        if self.export_base_setting:
            if not self.export_bodydiff_id_list:
                return False

        # 汎用衣装
        if self.chara_info.is_common_body:
            body_shape_info = body_shape_classes.BodyShapeInfoParser.create_from_chara_info(self.chara_info, self.body_shape_check_enabled)

            if not body_shape_info:
                return False

            file_name = 'mdl_' + self.chara_info.data_id

            for i, shape in enumerate(body_shape_info.shapes):
                file_suffix = shape.suffix

                if self.export_base_setting:
                    if file_suffix not in self.export_bodydiff_id_list:
                        continue

                new_item = CharaExporterItem(self)

                new_item.export_index = i
                new_item.output_file_name = file_name + file_suffix
                new_item.body_shape = shape

                new_item.initialize()

                self.exporter_item_list.append(new_item)

        # アタッチモデル
        elif self.chara_info.part_info.data_type.find('attach') >= 0:

            if not self.chara_info.part_info.model_list:
                return

            for model in self.chara_info.part_info.model_list:
                new_item = CharaExporterItem(self)
                new_item.output_file_name = model
                new_item.initialize()
                self.exporter_item_list.append(new_item)

        # 上記以外
        else:

            new_item = CharaExporterItem(self)

            new_item.export_index = 0
            new_item.output_file_name = \
                'mdl_' + self.chara_info.part_info.data_id

            new_item.initialize()

            self.exporter_item_list.append(new_item)

        return True

    def export(self):

        is_export = self.initialize()
        if not is_export:
            self.logger.write_error(u'キャラの情報が取得できませんでした')
            return

        self.logger.write_log()
        self.logger.write_log('*****')
        self.logger.write_log(u'エクスポート')
        self.logger.write_log(u'{0}'.format(self.target_file_path))
        self.logger.write_log('*****')
        self.logger.write_log()

        self.logger.write_log()
        self.logger.write_log('++++')
        self.logger.write_log(u'一時ファイルを作成')
        self.logger.write_log('++++')
        self.logger.write_log()

        # tempファイル作成後、開く
        self.temp_file_path = \
            base_utility.file.open_temp(
                self.target_file_path,
                '____temp000_base_' + os.path.basename(self.target_file_path)
            )

        if self.temp_file_path is None:
            return

        # データチェック
        if not self.check_data():
            if os.path.exists(self.temp_file_path):
                os.remove(self.temp_file_path)
            return

        base_utility.file.save()

        if not self.keep_temp_file:
            if os.path.exists(self.temp_file_path):
                os.remove(self.temp_file_path)

        for p in range(len(self.exporter_item_list)):

            self.exporter_item_list[p].export()

        if self.show_in_explorer:
            base_utility.io.open_directory(self.target_file_path)

    def check_data(self):

        is_export = self.initialize()
        if not is_export:
            self.logger.write_error(u'キャラの情報が取得できませんでした')
            return False

        self.logger.write_log()
        self.logger.write_log('++++')
        self.logger.write_log(u'エクスポートデータチェック')
        self.logger.write_log('++++')
        self.logger.write_log()

        if not os.path.isfile(self.target_file_path):
            self.logger.write_error(u'ファイルが見つかりません')
            return False

        if not self.export_target_list:

            self.export_target_list = []
            self.export_target_list.append(self.chara_info.part_info.root_node)

        self.create_fix_export_target_list()

        if len(self.fix_export_target_list) == 0:
            self.logger.write_error(u'エクスポート対象が見つかりません')
            return False

        for mesh in self.chara_info.part_info.mesh_list:

            if not cmds.objExists(mesh):
                continue

            material_list = base_utility.material.get_material_list(mesh)

            if not material_list:
                self.logger.write_error(u'{}にマテリアルが割りあたっていません'.format(mesh))
                return False

            for material in material_list:

                if not cmds.objectType(material, i='lambert'):
                    self.logger.write_error(u'{}のマテリアルが正しくありません'.format(mesh))
                    return False

        exist_sub_normal_model = False
        for target in self.chara_info.part_info.outline_mesh_list:

            if base_utility.node.exists(target):
                exist_sub_normal_model = True
                break

        # part_infoの中にfile_nameは渡していないのでそこだけchara_infoから取得する
        self.logger.write_log(u'対象ファイル: {0}'.format(self.chara_info.file_name))
        self.logger.write_log(u'ID: {0}'.format(self.chara_info.part_info.data_id))
        self.logger.write_log(u'File ID: {0}'.format(self.chara_info.part_info.file_id))
        self.logger.write_log(u'タイプ: {0}'.format(self.chara_info.part_info.data_type))
        self.logger.write_log(u'対象オブジェクト: {0}'.format(self.export_target_list))
        self.logger.write_log(u'アウトラインモデル: {0}'.format(exist_sub_normal_model))
        self.logger.write_log(u'SSR: {0}'.format(self.chara_info.part_info.is_unique_chara))

        self.logger.write_log(
            u'出力ファイル名:\n {0}'.format(
                '\n'.join(['{}.fbx'.format(export_item.output_file_name) for export_item in self.exporter_item_list])))

        if len(self.fix_export_target_list) == 0:
            self.logger.write_log()
            self.logger.write_error(u'対象オブジェクトが見つかりません')
            return False

        if not os.path.isdir(self.chara_info.part_info.maya_root_dir_path):
            self.logger.write_log()
            self.logger.write_error(u'ルートフォルダが見つかりません')
            return False

        if not os.path.isdir(self.chara_info.part_info.maya_scenes_dir_path):
            self.logger.write_log()
            self.logger.write_error(u'scenesフォルダが見つかりません')
            return False

        if not os.path.isdir(self.chara_info.part_info.maya_sourceimages_dir_path):
            self.logger.write_log()
            self.logger.write_error(u'sourceimagesフォルダが見つかりません')
            return False

        if len(self.exporter_item_list) == 0:
            self.logger.write_log()
            self.logger.write_error(u'出力ファイルが見つかりません')
            return False

        return True

    def create_fix_export_target_list(self):

        self.fix_export_target_list = []

        if not self.export_target_list:
            return

        transform_list = cmds.ls(l=True, type='transform')

        if transform_list is None:
            return

        if len(transform_list) == 0:
            return

        for transform in transform_list:

            transform_lower_name = transform.lower()

            exist = False
            for target in self.export_target_list:

                target_lower_name = target.lower()

                if target_lower_name == transform_lower_name:
                    exist = True
                    break

            if not exist:
                continue

            self.fix_export_target_list.append(transform)

        if len(self.fix_export_target_list) == len(self.export_target_list):
            return

        self.fix_export_target_list = []


class CharaExporterItem(object):

    def __init__(self, root):

        self.root = root

        self.export_index = 0

        self.output_file_name = None

        self.body_shape = None

        self.duplicate_mesh_list = None

        self.exclude_extra_mesh_list = []

    def initialize(self):

        _, self.exclude_extra_mesh_list = self.root.chara_info.part_info.exclude_extra(
            self.root.chara_info.part_info.mesh_param_list,
            self.root.chara_info.part_info.mesh_list
        )

    def export(self):

        # tempファイルを開く
        temp_file_name = '____temp{0:03d}_'.format(self.export_index) + os.path.basename(self.root.target_file_path)
        temp_file_path = base_utility.file.open_temp(self.root.target_file_path, temp_file_name)

        if temp_file_path is None:
            return

        # メッシュ操作をする前にアイコンモデルのフェースを保持
        icon_mask_faces = []
        if self.root.is_icon_model:
            icon_mask_faces = commands.get_mask_faces()

        # すべてのメッシュを表示
        self.show_all_base_mesh()

        # フェースセットからメッシュを生成(アタッチ用)
        self.create_attach_mesh()

        # メッシュデータをすべて複製
        self.duplicate_base_mesh_all()

        # サブノーマルメッシュを作成
        self.create_sub_normal_object_all()

        # 頂点カラーの割り当て
        self.fix_vertex_color_all()

        # ネックエッジに法線割り当て
        self.apply_neck_edge_set_all()

        # 法線情報をUV2,3へ転送
        self.create_sub_normal_uv_all()

        # ブレンドシェイプの位置を修正
        self.reset_blendshape_position()

        # ブレンドシェイプを適用
        self.apply_blendshape()

        # ブレンドジョイントを適用
        self.apply_blend_joint()

        # メッシュデータを最適化
        self.optimize_all()

        # メッシュをバインド
        self.bind_duplicated_mesh()

        # ベースメッシュとの入れ替え
        self.replace_base_mesh_all()

        # アイコンモデルのメッシュを切り分け
        if self.root.is_icon_model and icon_mask_faces:
            self.create_icon_mesh(icon_mask_faces)

        # tempファイル保存
        base_utility.file.save()

        # FBXで出力
        output_file_path = self.root.chara_info.part_info.maya_scenes_dir_path + '/' + self.output_file_name
        self.export_fbx(output_file_path)

        # tempファイルを削除
        if not self.root.keep_temp_file:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def show_all_base_mesh(self):
        """すべてのメッシュを表示
        """

        for mesh in self.exclude_extra_mesh_list:

            if cmds.objExists(mesh):
                cmds.showHidden(mesh)

    def create_attach_mesh(self):
        """出力する衣装に合わせてアタッチの差分を切り出す
        """

        if not self.root.chara_info.part_info.data_type.endswith('attach'):
            return

        # face_setの確定
        face_set_name = ''
        face_set_base_name = 'set_bdy'
        face_set_body_id = '0000_00'

        if self.root.chara_info.is_mini:
            face_set_base_name = 'set_mbdy'

        this_body_id = base_utility.string.get_string_by_regex(self.output_file_name, r'\d{4}_\d{2}.fbx')
        this_body_id = this_body_id.replace('.fbx', '')

        if this_body_id:
            face_set_body_id = this_body_id

        face_set_name = face_set_base_name + face_set_body_id

        if not cmds.objExists(face_set_name):
            return

        mesh_list = []
        for mesh in self.exclude_extra_mesh_list:
            if cmds.objExists(mesh):
                mesh_list.append(mesh)

        # 削除するfaceのリストを作成
        target_face_list = cmds.ls(cmds.sets(face_set_name, q=True), l=True, fl=True)

        if not target_face_list:
            return

        all_face_list = []
        for mesh in mesh_list:
            this_face_list = cmds.ls(mesh + '.f[*]', l=True, fl=True)

            if this_face_list:
                all_face_list.extend(this_face_list)

        del_face_list = []

        for face in all_face_list:
            if face not in target_face_list:

                # メインモデルのフェース
                del_face_list.append(face)

                # アウトラインモデルのフェース
                this_mesh = None

                for mesh in mesh_list:
                    if face.find(mesh) >= 0:
                        this_mesh = mesh
                        break

                if not this_mesh:
                    continue

                this_outline_face = face.replace(this_mesh, this_mesh + constants.SUB_NORMAL_SUFFIX)

                # alphaメッシュにはアウトラインがないのでチェック
                if cmds.objExists(this_outline_face):
                    del_face_list.append(this_outline_face)

        if not del_face_list:
            return

        # オリジナルのウェイトインフォを作成
        org_weight_info = base_class.mesh.skin_info.SkinInfo()
        org_weight_info.create_info(mesh_list)

        # 削除
        cmds.delete(del_face_list)

        # ヒストリ削除と再バインド
        for mesh in mesh_list:

            skin_root_joint = base_utility.mesh.skin.get_skin_root_joint(mesh)

            if skin_root_joint is None:
                continue

            cmds.select(skin_root_joint, r=True)
            cmds.select(hi=True)

            target_joint_list = cmds.ls(sl=True, typ='joint')

            if not target_joint_list:
                continue

            cmds.delete(mesh, ch=True)

            cmds.skinCluster(mesh, target_joint_list, obeyMaxInfluences=False, bindMethod=0, maximumInfluences=2, removeUnusedInfluence=False, skinMethod=0)

        # ウェイトコピー
        target_weight_info = base_class.mesh.skin_info.SkinInfo()
        target_weight_info.create_info(mesh_list)

        base_utility.mesh.skin.paste_weight_by_vertex_position(org_weight_info, target_weight_info)

    def duplicate_base_mesh_all(self):

        self.duplicate_mesh_list = []

        for mesh in self.exclude_extra_mesh_list:

            first_colorset = base_utility.mesh.colorset.get_colorset_from_index(mesh, 0)

            base_utility.mesh.colorset.set_current(mesh, first_colorset)

            duplicate_obj = commands.duplicate_with_suffix(mesh, constants.DUPLICATE_SUFFIX, True)

            self.duplicate_mesh_list.append(duplicate_obj)

    def create_sub_normal_object_all(self):

        for mesh in self.exclude_extra_mesh_list:

            self.create_sub_normal_object(mesh)

    def create_sub_normal_object(self, target_transform):

        if not base_utility.node.exists(target_transform):
            return

        target_transform_name = base_utility.name.get_short_name(target_transform)

        this_sub_normal_obj_name = \
            target_transform_name + constants.SUB_NORMAL_SUFFIX

        this_sub_normal_obj = self.root.chara_info.part_info.root_node + '|' + \
            this_sub_normal_obj_name

        if not base_utility.node.exists(this_sub_normal_obj):

            _tmp_duplicate_node = base_utility.node.duplicate(
                target_transform, this_sub_normal_obj_name
            )

            cmds.parent(_tmp_duplicate_node, w=True)

        else:

            cmds.parent(this_sub_normal_obj, w=True)

        this_sub_normal_obj = '|' + this_sub_normal_obj_name

        # カラーセットがない場合は白で作成
        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            this_sub_normal_obj
        )

        if not colorset_list:

            cmds.select(this_sub_normal_obj, r=True)
            cmds.polyColorPerVertex(r=1, g=1, b=1, a=1, cdo=True)

        cmds.delete(this_sub_normal_obj, ch=True)

    def fix_vertex_color_all(self):

        for mesh in self.duplicate_mesh_list:

            self.fix_vertex_color(mesh)

    def fix_vertex_color(self, target_transform):

        if not base_utility.node.exists(target_transform):
            return

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            target_transform
        )

        if not colorset_list:

            cmds.select(target_transform, r=True)
            cmds.polyColorPerVertex(r=1, g=1, b=1, a=1, cdo=True)

        cmds.delete(target_transform, ch=True)

    def apply_neck_edge_set_all(self):

        self.apply_neck_edge_set(False)
        self.apply_neck_edge_set(True)

    def apply_neck_edge_set(self, is_outline):

        target_transform_list = []
        name_prefix = None
        name_suffix = None

        # miniにneckEdgeSetは存在していない
        if self.root.chara_info.part_info.is_mini:
            return

        if self.root.chara_info.part_info.data_type.endswith('body'):

            body_object = 'M_Body'

            if is_outline:
                name_prefix = '|'
                name_suffix = constants.SUB_NORMAL_SUFFIX
            else:
                name_prefix = '|'
                name_suffix = constants.DUPLICATE_SUFFIX

            target_transform_list.append(body_object)

        elif self.root.chara_info.part_info.data_type.endswith('head'):

            face_object = '|M_Face'
            hair_object = '|M_Hair'

            if is_outline:
                name_prefix = '|'
                name_suffix = constants.SUB_NORMAL_SUFFIX
            else:
                name_prefix = '|'
                name_suffix = constants.DUPLICATE_SUFFIX

            target_transform_list.append(face_object)
            target_transform_list.append(hair_object)

        if not target_transform_list:
            return

        neck_normal_info = neck_normal.NeckNormalInfo()

        neck_normal_info.set_neck_normal_from_neck_edge_set(
            target_transform_list, name_prefix, name_suffix)

    def reset_blendshape_position(self):

        if not self.root.chara_info.is_common_body:
            return

        mesh = self.exclude_extra_mesh_list[0]

        for target in self.body_shape.targets:
            position = commands.get_target_root_locator(mesh, target)

            if not base_utility.node.exists(position):
                continue

            base_utility.attribute.set_value(position, 'translate', [0] * 3)

    def apply_blendshape(self):
        """体型差分のブレンドシェイプを適用

        self.body_shapeが持つすべてのターゲットの変形を適用したメッシュを作成し、頂点位置を複製メッシュにコピーする
        """

        if not self.root.chara_info.is_common_body:
            return

        for mesh, duplicated_mesh in zip(self.exclude_extra_mesh_list, self.duplicate_mesh_list):
            # すべてのターゲットの変形を適用したメッシュを作成
            deformed_mesh = commands.create_deformed_mesh(mesh, self.body_shape)
            # 頂点位置をコピー
            commands.transfer_vertex_position(deformed_mesh, duplicated_mesh)

    def apply_blend_joint(self):
        """体型のジョイント差分を適用

        ジョイントのオリエントと位置を、self.body_shapeが持つ各ターゲットの値にそのウェイト分だけ近づける
        """

        if not self.root.chara_info.is_common_body:
            return

        root = self.root.chara_info.part_info.locator_list[0]
        mesh = self.exclude_extra_mesh_list[0]

        if not base_utility.node.exists(root):
            return

        # 編集用ジョイントを作成
        blend_root = commands.duplicate_with_suffix(root, constants.BLENDJOINT_SUFFIX)
        # 各ターゲットのジョイントを作成
        target_roots = commands.create_target_joints(root, mesh, self.body_shape.targets)

        # 元のジョイントのオリエント情報を取得
        base_orients = commands.get_orientations(blend_root)
        # 各ターゲットのジョイントのオリエント情報を取得
        target_orients = {target: commands.get_orientations(target_root) for target, target_root in target_roots.items()}
        # オリエントとウェイトのタプルリストを作成
        target_orients_and_weights = [(orients, self.body_shape.targets.get(target)) for target, orients in target_orients.items()]
        # すべてのターゲットの差分を適用したオリエント情報を作成
        blend_orients = commands.blend_vectors(base_orients, target_orients_and_weights)

        # 元のジョイントの位置情報を取得
        base_transforms = commands.get_transforms(blend_root)
        # 各ターゲットのジョイントの位置情報を取得
        target_transforms = {target: commands.get_transforms(target_root) for target, target_root in target_roots.items()}
        # 位置とウェイトのタプルリストを作成
        target_transforms_and_weights = [(transforms, self.body_shape.targets.get(target)) for target, transforms in target_transforms.items()]
        # すべてのターゲットの差分を適用した位置情報を作成
        blend_transforms = commands.blend_vectors(base_transforms, target_transforms_and_weights)

        # 編集用ジョイントにオリエント、位置を適用
        commands.set_orientations(blend_root, blend_orients)
        commands.set_transforms(blend_root, blend_transforms)

        # 編集用ジョイントからオリエント、位置を取得
        current_blend_orients = commands.get_orientations(blend_root)
        current_blend_transforms = commands.get_transforms(blend_root)

        # 元のジョイントにオリエント、位置を適用
        commands.set_orientations(root, current_blend_orients)
        commands.set_transforms(root, current_blend_transforms)

    def create_sub_normal_uv_all(self):

        for mesh in self.exclude_extra_mesh_list:

            self.create_sub_normal_uv(mesh)

    def create_sub_normal_uv(self, target_transform):

        if not base_utility.node.exists(target_transform):
            return

        target_transform_name = base_utility.name.get_short_name(target_transform)

        duplicate_obj = \
            '|' + target_transform_name + constants.DUPLICATE_SUFFIX

        if not base_utility.node.exists(duplicate_obj):
            return

        this_sub_normal_obj_name = \
            target_transform_name + constants.SUB_NORMAL_SUFFIX

        this_sub_normal_obj = '|' + this_sub_normal_obj_name

        if not base_utility.node.exists(this_sub_normal_obj):
            return

        # 法線を複製オブジェクトのUVへ転送
        normal_to_uv_utility.transfer_normal_to_uvset(
            this_sub_normal_obj,
            duplicate_obj,
            constants.UVSET_FOR_NORMAL_XY,
            constants.UVSET_FOR_NORMAL_Z
        )

        # 頂点カラーのコピー
        normal_sel_list = om_utility.get_m_selection_list(this_sub_normal_obj)

        vc_info = vetex_color_info_classes.VertexColorInfo()
        vc_info.create_info(normal_sel_list)

        if not vc_info.info_list:
            return

        obj_vc_info = vc_info.info_list[0]
        obj_vc_info.dag_path = duplicate_obj
        obj_vc_info.apply_to_mesh()

    def optimize_all(self):

        for mesh in self.exclude_extra_mesh_list:

            if not base_utility.node.exists(mesh):
                continue

            target_transform_name = base_utility.name.get_short_name(mesh)

            duplicate_obj = \
                target_transform_name + constants.DUPLICATE_SUFFIX

            if not base_utility.node.exists(duplicate_obj):
                return

            self.optimize_uvset(duplicate_obj)
            self.optimize_colorset(duplicate_obj)

        mesh_list = []

        root_node = self.root.chara_info.part_info.root_node

        if base_utility.node.exists(root_node):

            position_transform = root_node + '|Position'

            if base_utility.node.exists(position_transform):

                cmds.select(position_transform, r=True)
                cmds.select(hi=True)
                select_list = cmds.ls(sl=True, l=True, typ='transform')

                if select_list:

                    for select in select_list:

                        mesh_shape = base_utility.mesh.get_mesh_shape(select)

                        if mesh_shape is None:
                            continue

                        mesh_list.append(select)

        for mesh in mesh_list:

            self.optimize_uvset(mesh)
            self.optimize_colorset(mesh)

    def optimize_uvset(self, target_transform):

        cmds.delete(target_transform, ch=True)

        max_uvset = 2
        create_uv = False

        this_uvset_list = base_utility.mesh.uvset.get_uvset_list(
            target_transform
        )

        if this_uvset_list:

            for uvset in this_uvset_list:

                if not base_utility.mesh.uvset.is_empty(target_transform, uvset):
                    continue

                base_utility.mesh.uvset.set_current(
                    target_transform, uvset
                )

                cmds.polyAutoProjection(target_transform + '.f[0]')

        if base_utility.mesh.uvset.exists(target_transform, constants.UVSET_FOR_NORMAL_XY) and \
                base_utility.mesh.uvset.exists(target_transform, constants.UVSET_FOR_NORMAL_Z):

            max_uvset = 4
            create_uv = True

        if create_uv:

            for p in range(5):

                current_uvset_list = base_utility.mesh.uvset.get_uvset_list(
                    target_transform
                )

                if len(current_uvset_list) >= max_uvset:
                    break

                temp_uvset = 'temp{0}'.format(p)

                base_utility.mesh.uvset.create(
                    target_transform, temp_uvset
                )

                base_utility.mesh.uvset.set_current(
                    target_transform, temp_uvset
                )

                cmds.polyAutoProjection(target_transform + '.f[0]')

        base_utility.mesh.uvset.change_index(
            target_transform, constants.UVSET_FOR_NORMAL_XY, 2
        )

        base_utility.mesh.uvset.change_index(
            target_transform, constants.UVSET_FOR_NORMAL_Z, 3
        )

        uvset_list = base_utility.mesh.uvset.get_uvset_list(
            target_transform
        )

        for this_uvset in uvset_list:

            this_uvset_index = base_utility.mesh.uvset.get_index(
                target_transform, this_uvset
            )

            if this_uvset_index < max_uvset:
                continue

            base_utility.mesh.uvset.delete(
                target_transform, this_uvset
            )

        base_utility.mesh.uvset.set_current_from_index(
            target_transform, 0
        )

        cmds.delete(target_transform, ch=True)

    def optimize_colorset(self, target_transform):

        if not base_utility.node.exists(target_transform):
            return

        cmds.delete(target_transform, ch=True)

        first_colorset = base_utility.mesh.colorset.get_colorset_from_index(
            target_transform, 0
        )

        # アルファ用のカラーセットが見つかればアルファ用のカラーセットのRを出力のAとして使う
        alpha_colorset = self.get_alpha_colorset(target_transform)

        if alpha_colorset:
            self.set_vtx_color_alpha(target_transform, first_colorset, alpha_colorset)

        base_utility.mesh.colorset.delete(
            target_transform, constants.OUTPUT_COLORSET
        )

        base_utility.mesh.colorset.create(
            target_transform, constants.OUTPUT_COLORSET
        )

        base_utility.mesh.colorset.blend(
            target_transform,
            constants.OUTPUT_COLORSET, first_colorset, 'over'
        )

        base_utility.mesh.colorset.change_index(
            target_transform, constants.OUTPUT_COLORSET, 0)

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            target_transform
        )

        for this_colorset in colorset_list:

            if this_colorset == constants.OUTPUT_COLORSET:
                continue

            base_utility.mesh.colorset.delete(
                target_transform, this_colorset
            )

        base_utility.mesh.colorset.set_current(
            target_transform, constants.OUTPUT_COLORSET
        )

        cmds.delete(target_transform, ch=True)

    def get_alpha_colorset(self, target_transform):

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            target_transform
        )

        if len(colorset_list) < 2:
            return

        # インデックス1以降で、self.sub_colorset_nameと一致しているものをalpha_colorsetとする
        for i, colorset in enumerate(colorset_list):

            if i == 0:
                continue

            if colorset == constants.SUB_COLORSET_NAME:
                return colorset

    def set_vtx_color_alpha(self, target_transform, base_colorset, alpha_colorset):

        if not base_utility.mesh.colorset.exists(target_transform, base_colorset):
            return

        if not base_utility.mesh.colorset.exists(target_transform, alpha_colorset):
            return

        base_utility.mesh.colorset.set_current(
            target_transform, alpha_colorset
        )

        vtx_alpha_color_info = base_utility.mesh.vertex_color.get_all_vertex_color_info_list(target_transform)

        base_utility.mesh.colorset.set_current(
            target_transform, base_colorset
        )

        vtx_base_color_info = base_utility.mesh.vertex_color.get_all_vertex_color_info_list(target_transform)

        if not vtx_alpha_color_info or not vtx_base_color_info:
            return

        # alpha_colorsetの頂点カラーのRを、base_colorsetの頂点カラーのAに移植
        for base_info, alpha_info in zip(vtx_base_color_info, vtx_alpha_color_info):

            base_info[2][3] = alpha_info[2][0]

        base_utility.mesh.vertex_color.set_vertex_color_info_list(target_transform, vtx_base_color_info)

    def bind_duplicated_mesh(self):

        for mesh, duplicated_mesh in zip(self.exclude_extra_mesh_list, self.duplicate_mesh_list):
            commands.bind_and_copy_weight(mesh, duplicated_mesh)

    def replace_base_mesh_all(self):

        for mesh in self.exclude_extra_mesh_list:

            if not base_utility.node.exists(mesh):
                continue

            target_mesh_name = base_utility.name.get_short_name(mesh)

            duplicate_obj = \
                '|' + target_mesh_name + constants.DUPLICATE_SUFFIX

            if not base_utility.node.exists(duplicate_obj):
                continue

            temp_mesh_name = target_mesh_name + '_Original'
            cmds.rename(mesh, temp_mesh_name)
            cmds.parent(temp_mesh_name, w=True)

            cmds.parent(duplicate_obj, self.root.chara_info.part_info.root_node)
            duplicate_obj = self.root.chara_info.part_info.root_node + \
                duplicate_obj

            cmds.rename(duplicate_obj, target_mesh_name)

    def create_icon_mesh(self, icon_mask_faces):
        """アイコンモデルのメッシュを分割する

        Args:
            icon_mask_faces (list): アイコンマスク用のフェースリスト
        """

        mask_obj_faces_dict = commands.get_obj_face_dict(icon_mask_faces)

        # スキンやマテリアルのため、メッシュごとに各処理を行う
        for obj in mask_obj_faces_dict:

            if not cmds.objExists(obj):
                continue

            # 階層を合わせるために親を取得しておく
            root = cmds.listRelatives(obj, p=True, f=True)[0]

            # スキニング情報を保持
            skin_joints = base_utility.mesh.skin.get_skin_joint_list(obj)
            org_weight_info = base_class.mesh.skin_info.SkinInfo()
            org_weight_info.create_info(obj)

            # メッシュの分割
            base_obj, mask_obj = commands.separate_mesh(obj, mask_obj_faces_dict[obj])

            if not mask_obj:
                continue

            # UVの状態を合わせる
            self.optimize_uvset(base_obj)
            self.optimize_uvset(mask_obj)

            # 分割時にワールドの子になっているので階層を合わせる
            base_obj = cmds.parent(base_obj, root)[0]
            mask_obj = cmds.parent(mask_obj, root)[0]

            # 命名を合わせる
            if cmds.objExists(obj):
                cmds.delete(obj)

            base_name = obj.split('|')[-1]
            base_obj = cmds.rename(base_obj, base_name)
            mask_obj = cmds.rename(mask_obj, commands.get_mask_name(base_obj, False))

            # オリジナルのスキニング情報があれば、分割後のメッシュにコピー
            if org_weight_info:

                cmds.skinCluster(base_obj,
                                 skin_joints,
                                 obeyMaxInfluences=False,
                                 bindMethod=0,
                                 maximumInfluences=2,
                                 removeUnusedInfluence=False,
                                 skinMethod=0)

                cmds.skinCluster(mask_obj,
                                 skin_joints,
                                 obeyMaxInfluences=False,
                                 bindMethod=0,
                                 maximumInfluences=2,
                                 removeUnusedInfluence=False,
                                 skinMethod=0)

                new_body_wight_info = base_class.mesh.skin_info.SkinInfo()
                new_body_wight_info.create_info(base_obj)

                mask_wight_info = base_class.mesh.skin_info.SkinInfo()
                mask_wight_info.create_info(mask_obj)

                base_utility.mesh.skin.paste_weight_by_vertex_position(org_weight_info, new_body_wight_info)
                base_utility.mesh.skin.paste_weight_by_vertex_position(org_weight_info, mask_wight_info)

            base_materials = base_utility.material.get_material_list(base_obj)
            base_material = None

            # マテリアル付与
            if base_materials:
                base_material = base_materials[0]

            if base_material:
                skin_material_name = commands.get_mask_name(base_material, True)

                if not cmds.objExists(skin_material_name):
                    base_utility.material.create_lambert_material(skin_material_name)

                base_utility.material.assign_material(skin_material_name, mask_obj)

    def export_fbx(self, output_path):

        if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
            cmds.warning(u'FBXプラグインをロードしました')
            cmds.loadPlugin('fbxmaya.mll')

        exporter = base_class.fbx_exporter.FbxExporter()

        exporter.is_ascii = self.root.is_ascii
        exporter.target_node_list = self.root.fix_export_target_list
        exporter.fbx_file_path = output_path

        if not exporter.export():
            self.root.logger.write_log(u'FBXの出力に失敗')
            return

        self.root.logger.write_log(u'FBXを出力しました')
