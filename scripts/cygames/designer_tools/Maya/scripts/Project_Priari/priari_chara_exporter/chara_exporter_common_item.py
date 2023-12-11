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

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from .. import priari_common
from ..priari_common.classes import info as cmn_info
from ..priari_common.utility import model_define
from ..priari_common.utility import model_id_finder
from ..priari_common.utility import model_mesh_finder
from .utility import normal_to_uv as utility_normal_to_uv

import maya.cmds as cmds

reload(base_common)
reload(priari_common)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CharaExporterCommonItem(object):

    # ===============================================
    def __init__(self, root):

        self.root = root

        self.root_node = ''

        self.no_export_mesh_suffix_list = [
            model_define.OUTLINE_SUFFIX,
        ]

        self.outline_suffix = model_define.OUTLINE_SUFFIX

        self.mesh_data_list = []

        self.export_index = 0

        self.org_file_path = None
        self.temp_file_prefix = None
        self.temp_file_path = None

        self.output_file_path = None
        self.output_file_name = None

        self.blend_shape_tmp_suffix = '_tmp.shp'
        self.blend_shape_tmp_path_list = None
        self.blend_shape_geometry_list = None

        self.sub_colorset_name = 'colorSet_sub'

    # ===============================================
    def initialize(self, org_file_path, export_root_node, output_file_path=''):

        self.org_file_path = org_file_path

        self.temp_file_prefix = '____temp{0:03d}_'.format(
            self.export_index
        )

        if output_file_path:
            self.output_file_path = output_file_path
            self.output_file_name = os.path.basename(self.output_file_path)
        else:
            self.output_file_name = \
                model_id_finder.get_fbx_name(self.root.chara_info.file_name)
            self.output_file_path = '{}/{}'.format(
                self.root.chara_info.part_info.maya_scenes_dir_path,
                self.output_file_name)

        self.root_node = export_root_node

    # ===============================================
    def export(self):

        # tempファイルを開く
        self.temp_file_path = base_utility.file.open_temp(
            self.org_file_path,
            self.temp_file_prefix + os.path.basename(self.org_file_path)
        )

        if self.temp_file_path is None:
            return

        # メッシュデータの作成
        self.mesh_data_list = self.get_mesh_data()

        # ブレンドシェープの書き出し
        self.export_blend_shape()

        # メッシュデータをすべて複製
        self.duplicate_base_mesh_all()

        # アウトラインメッシュを補完
        self.completion_outline_object_all()

        # 頂点カラーの補完
        self.completion_vertex_color_all()

        # アウトライン情報を複製メッシュに焼き付け
        self.bake_outline_data_all()

        # メッシュデータを最適化
        self.optimize_all()

        # ベースメッシュとの入れ替え
        self.replace_base_mesh_all()

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
    def get_mesh_data(self):
        """
        """

        transform_list = cmds.listRelatives(self.root_node, ad=True, ni=True, typ='transform', f=True)
        if not transform_list:
            return

        mesh_list = []
        for transform in transform_list:

            # mesh判定
            shape = cmds.listRelatives(transform, c=True, ni=True, s=True, typ='mesh', f=True)
            if not shape:
                continue

            # 接尾語判定
            is_no_export_mesh = False

            for suffix in self.no_export_mesh_suffix_list:
                if transform.endswith(suffix):
                    is_no_export_mesh = True

            if is_no_export_mesh:
                continue

            mesh_list.append(transform)

        if not mesh_list:
            return

        result_mesh_data_list = []
        for mesh in mesh_list:
            this_mesh_data = MeshData()
            this_mesh_data.initialize(mesh)

            if this_mesh_data.is_initialized:
                result_mesh_data_list.append(this_mesh_data)

        return result_mesh_data_list

    # ===============================================
    def export_blend_shape(self):
        """
        外部ファイルへ書き出し
        最終出力メッシュは複製後のものなので、一旦外へ書き出して、最後に戻す
        """

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

        if not self.mesh_data_list:
            return

        for mesh_data in self.mesh_data_list:
            short_name = mesh_data.long_name.split('|')[-1]
            dup_name = short_name + self.root.duplicate_suffix
            mesh_data.create_new_duplicate_mesh(dup_name)

    # ===============================================
    def completion_outline_object_all(self):

        if not self.mesh_data_list:
            return

        for mesh_data in self.mesh_data_list:

            if not mesh_data.is_initialized:
                continue

            self.completion_outline_object(mesh_data.long_name)

    # ===============================================
    def completion_outline_object(self, target_transform):

        if not cmds.objExists(target_transform):
            return

        outline_object = target_transform + self.outline_suffix

        # アウトラインメッシュがない場合は元を複製して作成
        if not cmds.objExists(outline_object):

            outline_short_name = outline_object.split('|')[-1]
            cmds.duplicate(target_transform, n=outline_short_name)

    # ===============================================
    def completion_vertex_color_all(self):

        if not self.mesh_data_list:
            return

        target_transform_list = []

        for mesh_data in self.mesh_data_list:

            dup_mesh = mesh_data.duplicate_mesh
            outline_mesh = mesh_data.long_name + self.outline_suffix

            if cmds.objExists(dup_mesh):
                target_transform_list.append(dup_mesh)
            if cmds.objExists(outline_mesh):
                target_transform_list.append(outline_mesh)

        for target_transform in target_transform_list:
            self.completion_vertex_color(target_transform)

    # ===============================================
    def completion_vertex_color(self, target_transform):

        if not cmds.objExists(target_transform):
            return

        colorset_list = base_utility.mesh.colorset.get_colorset_list(
            target_transform
        )

        if not colorset_list:

            cmds.select(target_transform, r=True)
            cmds.polyColorPerVertex(r=1, g=1, b=1, a=1, cdo=True)

        cmds.delete(target_transform, ch=True)

    # ===============================================
    def bake_outline_data_all(self):

        if not self.mesh_data_list:
            return

        for mesh_data in self.mesh_data_list:

            dup_mesh = mesh_data.duplicate_mesh
            outline_mesh = mesh_data.long_name + self.outline_suffix

            if not cmds.objExists(dup_mesh) or not cmds.objExists(outline_mesh):
                continue

            # 法線情報をUV2,3へ転送
            self.bake_outline_uv(dup_mesh, outline_mesh)
            # 頂点カラーのコピー
            self.bake_vtx_color(dup_mesh, outline_mesh)

            cmds.delete(outline_mesh)

    # ===============================================
    def bake_outline_uv(self, target_transform, src_tarnsform):

        utility_normal_to_uv.g_logger = self.root.logger
        utility_normal_to_uv.transfer_normal_to_uvset(
            src_tarnsform,
            target_transform,
            self.root.uvset_for_normal_xy,
            self.root.uvset_for_normal_z
        )

    # ===============================================
    def bake_vtx_color(self, target_transform, src_tarnsform):

        sub_normal_vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
        sub_normal_vtxcolor_info.create_info([src_tarnsform])

        duplicate_vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
        duplicate_vtxcolor_info.create_info([target_transform])

        base_utility.mesh.vertex_color.paste_vertex_color_by_vertex_index(
            sub_normal_vtxcolor_info,
            duplicate_vtxcolor_info
        )

    # ===============================================
    def optimize_all(self):

        if not self.mesh_data_list:
            return

        for mesh_data in self.mesh_data_list:

            if not mesh_data.is_initialized or not mesh_data.duplicate_mesh:
                continue

            self.optimize_uvset(mesh_data.duplicate_mesh)
            self.optimize_colorset(mesh_data.duplicate_mesh)
            self.optimize_skin_mesh(mesh_data.duplicate_mesh, mesh_data.long_name)

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

        base_skin_root_joint = base_utility.mesh.skin.get_skin_root_joint(cmds.ls(base_transform)[0])

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

        if not self.mesh_data_list:
            return

        for mesh_data in self.mesh_data_list:

            mesh_data.apply_worked_dup_to_org(True)

    # ===============================================
    def export_fbx(self):

        if not cmds.objExists(self.root_node):
            return

        self.root.exporter.is_ascii = self.root.is_ascii
        self.root.exporter.target_node_list = [self.root_node]
        self.root.exporter.fbx_file_path = self.output_file_path

        if not self.root.exporter.export():
            self.root.logger.write_log(u'FBXの出力に失敗')
            return

        self.root.logger.write_log(u'FBXを出力しました')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MeshData(object):

    # ===============================================
    def __init__(self):

        self.long_name = None
        self.parent = None
        self.skin_root = None
        self.duplicate_mesh = None

        self.is_initialized = False

    # ===============================================
    def initialize(self, long_name):

        self.is_initialized = False

        # メッシュ
        if not cmds.objExists(long_name):
            return
        else:
            self.long_name = long_name
            self.is_initialized = True

        # 親
        parent_list = cmds.listRelatives(self.long_name, p=True, f=True)
        if parent_list:
            self.parent = parent_list[0]

        # スキン
        skin_root_joint = base_utility.mesh.skin.get_skin_root_joint(long_name)
        if skin_root_joint:
            self.skin_root = skin_root_joint

    # ===============================================
    def create_new_duplicate_mesh(self, dup_mesh_name):

        if not self.is_initialized or not cmds.objExists(self.long_name):
            return

        if self.duplicate_mesh and cmds.objExists(self.duplicate_mesh):
            cmds.delete(self.duplicate_mesh)

        dup_list = cmds.duplicate(self.long_name, n=dup_mesh_name)
        if dup_list:
            self.duplicate_mesh = cmds.ls(dup_list[0], l=True)[0]
            return self.duplicate_mesh

    # ===============================================
    def apply_worked_dup_to_org(self, keeps_org_under_world):

        if not cmds.objExists(self.duplicate_mesh):
            return

        org_short_name = self.long_name.split('|')[-1]

        if keeps_org_under_world:
            cmds.parent(self.long_name, w=True)
        else:
            cmds.delete(self.long_name)

        if self.duplicate_mesh:
            result_mesh = cmds.rename(self.duplicate_mesh, org_short_name)
            self.initialize(cmds.ls(result_mesh, l=True)[0])


