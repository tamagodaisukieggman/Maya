# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import range
    from builtins import object
    from importlib import reload
except:
    pass

import os
import math
import subprocess

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from .. import farm_common
from ..farm_chara_facial_tool import facial_blend_shape_info
from ..farm_chara_facial_tool import facial_blend_shape_reorder
from ..farm_common.classes import info as cmn_info
from ..farm_common.utility import model_define
from ..farm_common.utility import model_id_finder
from ..farm_common.utility import model_mesh_finder
from .utility import normal_to_uv as utility_normal_to_uv
from . import chara_exporter_common_item as common_item

import maya.cmds as cmds

reload(base_common)
reload(farm_common)
reload(common_item)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CharaExporter(object):

    # ===============================================
    def __init__(self, main, target_file_path):

        self.main = main

        self.target_file_path = target_file_path

        self.script_file_path = None
        self.script_dir_path = None

        self.chara_info = None

        self.duplicate_suffix = "_Copy_From_Base"

        self.sub_normal_suffix = model_define.OUTLINE_SUFFIX

        self.uvset_for_normal_xy = '____normal_xy'
        self.uvset_for_normal_z = '____normal_z'

        self.output_colorset = '____output_colorset'

        self.export_target_list = None
        self.fix_export_target_list = None
        self.custom_export_target = False

        self.logger = None

        self.keep_temp_file = False
        self.is_ascii = False
        self.show_in_explorer = False

        self.exporter = None

        self.base_skin_info_list = None

        self.exporter_item_list = None

        self.temp_file_path = None

    # ===============================================
    def initialize(self):

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.chara_info = cmn_info.chara_info.CharaInfo()
        self.chara_info.create_info(file_path=self.target_file_path)

        if not self.chara_info.exists:
            return False

        self.exporter = base_class.fbx_exporter.FbxExporter()

        self.exporter_item_list = []

        # 武器・プロップモデルは階層構造が不定なので汎用的なエクスポートアイテムを使う
        if self.chara_info.part_info.data_type.find('weapon') >= 0 or self.chara_info.part_info.data_type.find('prop') >= 0:

            if not self.chara_info.part_info.model_list:
                return

            new_item = common_item.CharaExporterCommonItem(self)
            new_item.initialize(
                self.target_file_path,
                self.chara_info.part_info.root_node,
            )
            self.exporter_item_list.append(new_item)

        # 上記以外
        else:

            new_item = CharaExporterItem(self)

            new_item.export_index = 0
            new_item.output_file_name = \
                model_id_finder.get_fbx_name(self.chara_info.file_name)

            new_item.initialize()

            self.exporter_item_list.append(new_item)

        return True

    # ===============================================
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

        # ベースメッシュをチェック
        self.check_base_mesh()

        base_utility.file.save()

        if not self.keep_temp_file:
            if os.path.exists(self.temp_file_path):
                os.remove(self.temp_file_path)

        for p in range(len(self.exporter_item_list)):

            self.exporter_item_list[p].export()

        if self.show_in_explorer:

            if not self.target_file_path:
                return

            target_dir_path = None

            if os.path.isfile(self.target_file_path):
                target_dir_path = os.path.dirname(self.target_file_path)

            elif os.path.isdir(self.target_file_path):
                target_dir_path = self.target_file_path

            if target_dir_path is None:
                return

            target_dir_path = target_dir_path.replace('/', '\\')
            subprocess.Popen('explorer "' + target_dir_path + '"')



    # ===============================================
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

            self.custom_export_target = False

            self.export_target_list = []
            self.export_target_list.append(self.chara_info.part_info.root_node)

        else:

            self.custom_export_target = True

        self.create_fix_export_target_list()

        if len(self.fix_export_target_list) == 0:
            self.logger.write_error(u'エクスポート対象が見つかりません')
            return False

        check_mesh_list = []

        for target in self.fix_export_target_list:

            transform_list = cmds.listRelatives(target, ad=True, type='transform', f=True)

            for transform in transform_list:

                if transform.split('|')[-1].startswith(model_define.MESH_PREFIX):
                    check_mesh_list.append(transform)

        # マテリアルチェック
        for mesh in check_mesh_list:

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

        # アウトラインチェック
        exist_sub_normal_model = False
        for mesh in check_mesh_list:
            if model_mesh_finder.get_outline_mesh(mesh):
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
            u'出力ファイル名: {0}'.format(
                self.exporter_item_list[0].output_file_name))

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

        # if not os.path.isdir(self.chara_info.part_info.maya_sourceimages_dir_path):
        #     self.logger.write_log()
        #     self.logger.write_error(u'sourceimagesフォルダが見つかりません')
        #     return False

        return True

    # ===============================================
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

    # ===============================================
    def check_base_mesh(self):

        self.base_skin_info_list = {}

        _, mesh_list = self.chara_info.part_info.exclude_extra(
            self.chara_info.part_info.mesh_param_list,
            self.chara_info.part_info.mesh_list,
        )

        for mesh in mesh_list:

            if not mesh or not cmds.objExists(mesh):
                continue

            if mesh.find('|') == -1:
                mesh_name = mesh

            mesh_name = mesh.split('|')[-1]

            this_skin_info = base_class.mesh.skin_info.SkinInfo()
            this_skin_info.create_info([mesh])

            self.base_skin_info_list[mesh_name] = this_skin_info


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CharaExporterItem(object):

    # ===============================================
    def __init__(self, root):

        self.root = root

        self.export_index = 0

        self.temp_file_prefix = None
        self.temp_file_path = None

        self.output_file_name = None
        self.output_file_path = None

        self.duplicate_mesh_list = None
        self.duplicate_locator_list = None

        self.blend_shape_tmp_suffix = '_tmp.shp'
        self.blend_shape_tmp_path_list = None
        self.blend_shape_geometry_list = None

        self.skin_info_list = None

        self.sub_colorset_name = 'colorSet_sub'

        self.exclude_extra_mesh_list = []
        self.special_addicional_joint_dict_list = []
        self.special_addicional_joint_child_list = []
        self.special_additional_joint_parent_list = [
            'Sp_Ch_Bust0_L_01', 'Sp_Ch_Bust0_R_01',
        ]

    # ===============================================
    def initialize(self):

        self.temp_file_prefix = '____temp{0:03d}_'.format(
            self.export_index
        )

        self.output_file_path = '{}/{}'.format(
            self.root.chara_info.part_info.maya_scenes_dir_path,
            self.output_file_name)

        # _, self.exclude_extra_mesh_list = self.root.chara_info.part_info.exclude_extra(
        #     self.root.chara_info.part_info.mesh_param_list,
        #     self.root.chara_info.part_info.mesh_list
        # )

        # 現状grp_meshの子は全て出力対象にする
        self.exclude_extra_mesh_list = model_mesh_finder.get_all_base_mesh_list(self.root.chara_info.part_info.root_node)

    # ===============================================
    def export(self):

        # tempファイルを開く
        self.temp_file_path = base_utility.file.open_temp(
            self.root.target_file_path,
            self.temp_file_prefix + os.path.basename(self.root.target_file_path)
        )

        if self.temp_file_path is None:
            return

        # ブレンドシェープのソート
        self.reorder_blend_shape()

        # ブレンドシェープの書き出し
        self.export_blend_shape()

        # メッシュデータをすべて複製
        self.duplicate_base_mesh_all()

        # サブノーマルメッシュを作成
        self.create_sub_normal_object_all()

        # 頂点カラーの割り当て
        self.fix_vertex_color_all()

        # 法線情報をUV2,3へ転送
        self.create_sub_normal_uv_all()

        # 特殊追加骨対応 対象のリストを作成
        self.set_special_addicional_joint_list()

        # 追加特殊骨対応 追加特殊骨を一旦worldとペアレント
        # ジョイントオリエント対応の影響を受けない様に
        # self.release_special_addicional_joint_parent()

        # ジョイントオリエントの修正
        # self.fix_joint_orient_to_sp_joint()

        # 追加特殊骨対応 追加特殊骨のペアレントを元に戻す
        # self.setting_special_addicional_joint_parent()

        # メッシュデータを最適化
        self.optimize_all()

        # ベースメッシュとの入れ替え
        self.replace_base_mesh_all()

        # 追加特殊骨対応 追加特殊骨のフリーズ
        self.freeze_special_addicional_joint()

        # ブレンドシェープの読み込み
        self.import_blend_shape()

        # tempファイル保存
        base_utility.file.save()

        # FBXで出力
        self.export_fbx()

        # tempファイルを削除
        if not self.root.keep_temp_file:
            if os.path.exists(self.temp_file_path):
                os.remove(self.temp_file_path)

    # ===============================================
    def set_special_addicional_joint_list(self):

        self.special_addicional_joint_dict_list = []
        self.special_addicional_joint_child_list = []

        root_joint = self.root.chara_info.part_info.joint_list[0]
        all_joint_list = cmds.listRelatives(root_joint, ad=True, f=True, type='joint')
        if all_joint_list:

            for _joint in all_joint_list:

                joint_short_name = _joint.split('|')[-1]
                if joint_short_name not in self.special_additional_joint_parent_list:
                    continue

                joint_child_list = cmds.listRelatives(_joint, f=True)
                if not joint_child_list:
                    continue

                for joint_child in joint_child_list:

                    tmp_joint_child_list = [joint_child]
                    joint_grand_child_list = cmds.listRelatives(joint_child_list, ad=True, f=True)
                    if joint_grand_child_list:
                        tmp_joint_child_list += joint_grand_child_list

                    self.special_addicional_joint_dict_list.append({
                        'child': joint_child, 'parent': _joint})

                    self.special_addicional_joint_child_list.extend(tmp_joint_child_list)

    # ===============================================
    def release_special_addicional_joint_parent(self):

        for i in range(len(self.special_addicional_joint_dict_list)):

            child_joint = self.special_addicional_joint_dict_list[i]['child']
            child_joint = cmds.parent(child_joint, w=True)
            self.special_addicional_joint_dict_list[i]['child'] = child_joint

    # ===============================================
    def setting_special_addicional_joint_parent(self):

        for i in range(len(self.special_addicional_joint_dict_list)):

            child_joint = self.special_addicional_joint_dict_list[i]['child']
            parent_joint = self.special_addicional_joint_dict_list[i]['parent']
            cmds.parent(child_joint, parent_joint)

    # ===============================================
    def freeze_special_addicional_joint(self):

        if self.special_addicional_joint_child_list:

            skin_info_dict_list = []

            # meshのskin情報の取得
            for mesh in self.exclude_extra_mesh_list:

                if not mesh or not cmds.objExists(mesh):
                    continue

                skin_root_joint = base_utility.mesh.skin.get_skin_root_joint(mesh)
                if skin_root_joint is None:
                    continue

                skin_info_dict = {}

                child_joint_list = cmds.listRelatives(skin_root_joint, ad=True, f=True, typ='joint')
                joint_list = [skin_root_joint] + child_joint_list

                skin_info = base_class.mesh.skin_info.SkinInfo()
                skin_info.create_info([mesh])

                skin_info_dict['skin_info'] = skin_info
                skin_info_dict['mesh'] = mesh
                skin_info_dict['joint_list'] = joint_list

                skin_info_dict_list.append(skin_info_dict)

            # 全てのヒストリー削除(デタッチ)
            cmds.delete(all=True, ch=True)

            # transformのフリーズ
            cmds.makeIdentity(self.special_addicional_joint_child_list, apply=True, t=False, r=True, s=False, n=False, pn=True)

            # 再bind
            for skin_info_dict in skin_info_dict_list:

                dst_skin_info = skin_info_dict['skin_info']
                dst_mesh = skin_info_dict['mesh']
                dst_joint_list = skin_info_dict['joint_list']

                cmds.skinCluster(
                    dst_mesh,
                    dst_joint_list,
                    obeyMaxInfluences=False,
                    bindMethod=0,
                    maximumInfluences=2,
                    removeUnusedInfluence=False,
                    skinMethod=0)

                target_skin_info = base_class.mesh.skin_info.SkinInfo()
                target_skin_info.create_info([dst_mesh])

                base_utility.mesh.skin.paste_weight_by_vertex_index(
                    dst_skin_info, target_skin_info
                )

    # ===============================================
    def reorder_blend_shape(self):
        blend_shape_info = facial_blend_shape_info.FacialBlendShapeInfo()
        blend_shape_info.initialize()

        reorder = facial_blend_shape_reorder.FacialBlendShapeReorder()
        reorder.initialize(blend_shape_info)
        reorder.reorder_blend_shape_index()

    # ===============================================
    def export_blend_shape(self):
        """
        外部ファイルへ書き出し
        最終出力メッシュは複製後のものなので、一旦外へ書き出して、最後に戻す
        """

        # data_typeの縛りをとる
        # if not self.root.chara_info.part_info.data_type == model_define.AVATAR_DATA_TYPE:
        #     return

        blend_shape_node_list = cmds.ls(typ='blendShape')

        if not blend_shape_node_list:
            return

        self.blend_shape_tmp_path_list = []
        self.blend_shape_geometry_list = []
        dir_path = os.path.dirname(cmds.file(q=True, sn=True, exn=True))

        for blend_shape_node in blend_shape_node_list:

            file_name = blend_shape_node + self.blend_shape_tmp_suffix
            output_path = os.path.join(dir_path, file_name)
            cmds.blendShape(blend_shape_node, e=True, ep=output_path)

            if os.path.exists(output_path):
                self.blend_shape_tmp_path_list.append(output_path)
                self.blend_shape_geometry_list.append(cmds.blendShape(blend_shape_node, q=True, g=True))

    # ===============================================
    def import_blend_shape(self):
        """
        外部ファイルから読み込み
        """

        if not self.blend_shape_tmp_path_list:
            return

        for tmp_file_path, geo in zip(self.blend_shape_tmp_path_list, self.blend_shape_geometry_list):

            if not os.path.exists(tmp_file_path):
                continue

            if not geo:
                continue

            node_name = os.path.basename(tmp_file_path).replace(self.blend_shape_tmp_suffix, '')

            if cmds.objExists(node_name):
                cmds.delete(node_name)
            cmds.blendShape(geo[0], n=node_name, at=True)

            try:
                cmds.blendShape(node_name, e=True, ip=tmp_file_path)
            except Exception:
                print(traceback.format_exc())

            os.remove(tmp_file_path)

    # ===============================================
    def duplicate_base_mesh_all(self):

        self.duplicate_mesh_list = []

        for mesh in self.exclude_extra_mesh_list:

            duplicate_obj = self.duplicate_transform(mesh)

            self.duplicate_mesh_list.append(duplicate_obj)

    # ===============================================
    def duplicate_transform(self, target_transform):

        if not target_transform or not cmds.objExists(target_transform):
            return

        target_transform_name = target_transform.split('|')[-1]

        duplicate_obj_name = \
            target_transform_name + self.root.duplicate_suffix

        duplicate_obj = '|' + duplicate_obj_name

        if not duplicate_obj or not cmds.objExists(duplicate_obj):

            if not target_transform or not cmds.objExists(target_transform):
                return

            target_node_name = target_transform.split('|')[-1]

            if duplicate_obj_name and cmds.objExists(duplicate_obj_name):
                return

            target_shape_node = base_utility.mesh.get_mesh_shape(target_transform)

            if target_shape_node is not None:

                target_shape_node_name = target_shape_node.split('|')[-1]

                if target_node_name.lower() == target_shape_node_name.lower():
                    cmds.rename(target_shape_node, target_shape_node_name + 'Shape')

            _tmp_duplicate_node = cmds.ls(
                cmds.duplicate(target_transform, rr=True, name=duplicate_obj_name), l=True
            )[0]

            cmds.parent(_tmp_duplicate_node, w=True)

        return duplicate_obj

    # ===============================================
    def create_sub_normal_object_all(self):

        for mesh in self.exclude_extra_mesh_list:

            self.create_sub_normal_object(mesh)

    # ===============================================
    def create_sub_normal_object(self, target_transform):

        if not target_transform or not cmds.objExists(target_transform):
            return

        target_transform_name = target_transform.split('|')[-1]

        this_sub_normal_obj_name = \
            target_transform_name + self.root.sub_normal_suffix

        # outlineメッシュは同階層にある想定
        this_sub_normal_obj = model_mesh_finder.get_outline_mesh(target_transform)

        if not this_sub_normal_obj or not cmds.objExists(this_sub_normal_obj):

            if not target_transform or not cmds.objExists(target_transform):
                return

            target_node_name = target_transform.split('|')[-1]

            if this_sub_normal_obj_name and cmds.objExists(this_sub_normal_obj_name):
                return

            target_shape_node = base_utility.mesh.get_mesh_shape(target_transform)

            if target_shape_node is not None:

                target_shape_node_name = target_shape_node.split('|')[-1]

                if target_node_name.lower() == target_shape_node_name.lower():
                    cmds.rename(target_shape_node, target_shape_node_name + 'Shape')

            _tmp_duplicate_node = cmds.ls(
                cmds.duplicate(target_transform, rr=True, name=this_sub_normal_obj_name), l=True
            )[0]

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

    # ===============================================
    def fix_vertex_color_all(self):

        for mesh in self.duplicate_mesh_list:

            self.fix_vertex_color(mesh)

    # ===============================================
    def fix_vertex_color(self, target_transform):

        if not target_transform or not cmds.objExists(target_transform):
            return

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            target_transform
        )

        if not colorset_list:

            cmds.select(target_transform, r=True)
            cmds.polyColorPerVertex(r=1, g=1, b=1, a=1, cdo=True)

        cmds.delete(target_transform, ch=True)

    # ===============================================
    def fix_joint_orient_to_sp_joint(self):

        if not self.root.chara_info.part_info.joint_list:
            return

        root_joint = self.root.chara_info.part_info.joint_list[0]

        if not root_joint or not cmds.objExists(root_joint):
            return

        cmds.select(cl=True)
        cmds.select(root_joint, r=True)
        cmds.select(root_joint, hi=True)

        selected_joint_list = cmds.ls(sl=True, l=True, typ='joint')

        if not selected_joint_list:
            return

        selected_joint_list.sort()

        # オリエントがかかっているSp系ジョイントを収集
        # 今はバストのみで今後他も対応の必要があれば解放検討
        sp_joint_list = []
        for joint in selected_joint_list:

            short_name = joint.split("|")[-1]

            if not short_name.find('Sp_') != -1:
                continue

            if not short_name.find('Bust') != -1:
                continue

            sp_joint_list.append(joint)

        # ジョイントが次のジョイントに正しく向いているかチェック
        error_joint_list = []
        for joint in sp_joint_list:

            child_joint_list = cmds.listRelatives(joint, typ="joint", f=True, c=True)

            if not child_joint_list:
                continue

            if len(child_joint_list) > 1:
                continue

            child_joint = child_joint_list[0]

            # フォワードベクトルとオブジェクト間ベクトルを比較して、
            # 向き先が違えばオリエントが正しく向いていないと判断
            forward_vector = self.get_forward_vector(joint)
            between_vector = self.get_vector_by_two_transform(joint, child_joint, True)

            if base_utility.vector.is_same(forward_vector, between_vector):
                continue

            error_joint_list.append(joint)

        # 方向が間違っているジョイントのオリエントを修正
        for joint in error_joint_list:

            cmds.joint(joint, e=True, oj='zyx',
                       secondaryAxisOrient='yup', zso=True, ch=True)

            # オリエント修正後に末端のジョイントのオリエントも変わってしまうので、
            # オリエントをゼロに戻す

            cmds.select(cl=True)
            cmds.select(joint, r=True)
            cmds.select(joint, hi=True)

            all_child_joint_list = cmds.ls(sl=True, l=True, typ='joint')

            if not all_child_joint_list:
                continue

            for child_joint in all_child_joint_list:

                if child_joint == joint:
                    continue

                this_child_joint_list = cmds.listRelatives(
                    child_joint, typ="joint", f=True, c=True)

                if this_child_joint_list:
                    continue

                value = [0] * 3

                if not child_joint or not cmds.objExists(child_joint):
                    continue

                try:
                    cmds.getAttr(child_joint + '.' + 'jointOrient', type=True)
                except:
                    continue

                attr_type = cmds.getAttr(child_joint + '.' + 'jointOrient', typ=True)

                if attr_type == 'string':

                    is_settable = \
                        cmds.getAttr(child_joint + '.' + 'jointOrient', settable=True)

                    if not is_settable:
                        continue

                    cmds.setAttr(child_joint + '.' + 'jointOrient',
                                value,
                                type='string')

                elif _re.search('.*\d$', attr_type):

                    is_settable = \
                        cmds.getAttr(child_joint + '.' + 'jointOrient', settable=True)

                    if is_settable:

                        if attr_type.find('2') > 0:
                            cmds.setAttr(child_joint + '.' +
                                        'jointOrient', value[0], value[1])
                            continue

                        if attr_type.find('3') > 0:
                            cmds.setAttr(child_joint + '.' + 'jointOrient',
                                        value[0], value[1], value[2])
                            continue

                    attr_list = search_list(
                        child_joint, 'jointOrient' + '.{1}$')

                    if not attr_list:
                        continue

                    value_list = None
                    if type(value) == list:
                        value_list = value
                    else:
                        value_list = [value]

                    count = -1
                    for attr in attr_list:
                        count += 1

                        this_value = value_list[-1]

                        if count < len(value_list):
                            this_value = value_list[count]

                        is_settable = \
                            cmds.getAttr(child_joint + '.' + attr, settable=True)

                        if not is_settable:
                            continue

                        cmds.setAttr(child_joint + '.' + attr, this_value)

                else:

                    is_settable = \
                        cmds.getAttr(child_joint + '.' + 'jointOrient', settable=True)

                    if not is_settable:
                        continue

                    cmds.setAttr(child_joint + '.' + 'jointOrient', value)


    # ===============================================
    def get_forward_vector(self, target_transform):

        forward_vector = [0] * 3

        if not target_transform or not cmds.objExists(target_transform):
            return forward_vector

        matrix = cmds.xform(target_transform, q=True, ws=True, matrix=True)

        forward_vector = [matrix[8], matrix[9], matrix[10]]

        forward_vector = self.get_normalize_vector(forward_vector)

        return forward_vector

    # ===============================================
    def get_vector_by_two_transform(self, src_transform, dst_transform, is_normalize):

        result_vector = [0] * 3

        if not src_transform or not cmds.objExists(src_transform):
            return result_vector

        if not dst_transform or not cmds.objExists(dst_transform):
            return result_vector

        src_pos = cmds.xform(src_transform, q=True, ws=True, t=True)
        dst_pos = cmds.xform(dst_transform, q=True, ws=True, t=True)

        for p in range(len(result_vector)):
            result_vector[p] = dst_pos[p] - src_pos[p]

        if is_normalize:
            result_vector = self.get_normalize_vector(result_vector)

        return result_vector

    # ===============================================
    def get_normalize_vector(self, vector):

        result_vector = [0] * 3

        vector_length = self.get_vector_length(vector)

        for p in range(len(result_vector)):
            result_vector[p] = vector[p] / vector_length

        return result_vector

    # ===============================================
    def get_vector_length(self, vector):

        vector_length = 0

        for p in range(len(vector)):
            vector_length += vector[p] * vector[p]

        vector_length = math.sqrt(vector_length)

        return vector_length

    # ===============================================
    def create_sub_normal_uv_all(self):

        for mesh in self.exclude_extra_mesh_list:

            self.create_sub_normal_uv(mesh)

    # ===============================================
    def create_sub_normal_uv(self, target_transform):

        if not target_transform or not cmds.objExists(target_transform):
            return

        target_transform_name = target_transform.split('|')[-1]

        duplicate_obj = \
            '|' + target_transform_name + self.root.duplicate_suffix

        if not duplicate_obj or not cmds.objExists(duplicate_obj):
            return

        this_sub_normal_obj_name = \
            target_transform_name + self.root.sub_normal_suffix

        this_sub_normal_obj = '|' + this_sub_normal_obj_name

        if not this_sub_normal_obj or not cmds.objExists(this_sub_normal_obj):
            return

        # 法線を複製オブジェクトのUVへ転送
        utility_normal_to_uv.g_logger = self.root.logger
        utility_normal_to_uv.transfer_normal_to_uvset(
            this_sub_normal_obj,
            duplicate_obj,
            self.root.uvset_for_normal_xy,
            self.root.uvset_for_normal_z
        )

        # 頂点カラーのコピー
        sub_normal_vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
        sub_normal_vtxcolor_info.create_info([this_sub_normal_obj])

        duplicate_vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
        duplicate_vtxcolor_info.create_info([duplicate_obj])

        base_utility.mesh.vertex_color.paste_vertex_color_by_vertex_index(
            sub_normal_vtxcolor_info,
            duplicate_vtxcolor_info
        )

    # ===============================================
    def optimize_all(self):

        for mesh in self.exclude_extra_mesh_list:

            if not mesh or not cmds.objExists(mesh):
                continue

            target_transform_name = mesh.split('|')[-1]

            duplicate_obj = \
                target_transform_name + self.root.duplicate_suffix

            if not duplicate_obj or not cmds.objExists(duplicate_obj):
                return

            self.optimize_uvset(duplicate_obj)
            self.optimize_colorset(duplicate_obj)
            self.optimize_skin_mesh(duplicate_obj, mesh)

    # ===============================================
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

        if base_utility.mesh.uvset.exists(target_transform, self.root.uvset_for_normal_xy) and \
                base_utility.mesh.uvset.exists(target_transform, self.root.uvset_for_normal_z):

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
            target_transform, self.root.uvset_for_normal_xy, 2
        )

        base_utility.mesh.uvset.change_index(
            target_transform, self.root.uvset_for_normal_z, 3
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

    # ===============================================
    def optimize_colorset(self, target_transform):

        if not target_transform or not cmds.objExists(target_transform):
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
            target_transform, self.root.output_colorset
        )

        base_utility.mesh.colorset.create(
            target_transform, self.root.output_colorset
        )

        base_utility.mesh.colorset.blend(
            target_transform,
            self.root.output_colorset, first_colorset, 'over'
        )

        base_utility.mesh.colorset.change_index(
            target_transform, self.root.output_colorset, 0)

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            target_transform
        )

        for this_colorset in colorset_list:

            if this_colorset == self.root.output_colorset:
                continue

            base_utility.mesh.colorset.delete(
                target_transform, this_colorset
            )

        base_utility.mesh.colorset.set_current(
            target_transform, self.root.output_colorset
        )

        cmds.delete(target_transform, ch=True)

    # ===============================================
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

            if colorset == self.sub_colorset_name:
                return colorset

    # ===============================================
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

    # ===============================================
    def optimize_skin_mesh(self, target_transform, base_transform):

        if not target_transform or not cmds.objExists(target_transform):
            return

        if not base_transform or not cmds.objExists(base_transform):
            return

        cmds.delete(target_transform, ch=True)

        base_skin_root_joint = base_utility.mesh.skin.get_skin_root_joint(base_transform)

        if base_skin_root_joint is None:
            return

        target_joint_list = [base_skin_root_joint]
        child_joint_list = cmds.listRelatives(base_skin_root_joint, ad=True, type='joint', f=True)

        if child_joint_list:
            target_joint_list.extend(child_joint_list)

        base_skin_info = base_class.mesh.skin_info.SkinInfo()
        base_skin_info.create_info([base_transform])

        cmds.skinCluster(
            target_transform,
            target_joint_list,
            toSelectedBones=True,
            obeyMaxInfluences=False,
            bindMethod=0,
            maximumInfluences=2,
            removeUnusedInfluence=False,
            skinMethod=0)

        target_skin_info = base_class.mesh.skin_info.SkinInfo()
        target_skin_info.create_info([target_transform])

        base_vertex_num = cmds.polyEvaluate(base_transform, v=True)
        target_vertex_num = cmds.polyEvaluate(target_transform, v=True)

        if base_vertex_num == target_vertex_num:

            base_utility.mesh.skin.paste_weight_by_vertex_index(
                base_skin_info, target_skin_info
            )

        else:

            base_utility.mesh.skin.paste_weight_by_vertex_position(
                base_skin_info, target_skin_info
            )

    # ===============================================
    def replace_base_mesh_all(self):

        for mesh in self.exclude_extra_mesh_list:

            if not mesh or not cmds.objExists(mesh):
                continue

            target_mesh_name = mesh.split('|')[-1]

            duplicate_obj = \
                '|' + target_mesh_name + self.root.duplicate_suffix

            if not duplicate_obj or not cmds.objExists(duplicate_obj):
                continue

            temp_mesh_name = target_mesh_name + '_Original'
            cmds.rename(mesh, temp_mesh_name)
            cmds.parent(temp_mesh_name, w=True)

            cmds.parent(duplicate_obj, self.root.chara_info.part_info.root_node + '|' + model_define.MESH_ROOT)
            duplicate_obj = self.root.chara_info.part_info.root_node + '|' + model_define.MESH_ROOT +\
                duplicate_obj

            cmds.rename(duplicate_obj, target_mesh_name)

    # ===============================================
    def export_fbx(self):

        self.root.exporter.is_ascii = self.root.is_ascii
        self.root.exporter.target_node_list = self.root.fix_export_target_list
        self.root.exporter.fbx_file_path = self.output_file_path

        if not self.root.exporter.export():
            self.root.logger.write_log(u'FBXの出力に失敗')
            return

        self.root.logger.write_log(u'FBXを出力しました')
