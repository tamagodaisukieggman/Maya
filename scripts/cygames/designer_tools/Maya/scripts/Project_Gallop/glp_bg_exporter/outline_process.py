# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import os
import re

import maya.cmds as cmds

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from . import constants
from . import normal_to_uv
from .normal_to_uv import transfer_normal_to_uvset as utility_normal_to_uv

reload(base_common)
reload(constants)
reload(normal_to_uv)


class OutlineProcess(object):

    def __init__(self):
        self.is_ready = False
        self.base_node = ''
        self.outline_mesh_list = []

        self.__saved_skin_datas = []

    def initialize(self, base_node):
        """初期化処理

        Args:
            base_node (str): 基準としたいノード名
        """
        self.is_ready = False
        self.base_node = base_node
        self.outline_mesh_list = []

        # ノード名でマッチして条件に適合しない場合にははじく
        if not self.is_outline_process_target(base_node):
            return

        self.outline_mesh_list = []
        for mesh in cmds.listRelatives(self.base_node, ad=True, type='transform', fullPath=True):
            mesh_name = mesh.split('|')[-1]
            if mesh_name.endswith(constants.SUB_NORMAL_SUFFIX):
                self.outline_mesh_list.append(mesh)

        # 対象が存在した場合のみ通す
        if self.outline_mesh_list:
            self.is_ready = True

    def outline_transfer_to_original(self):
        """アウトラインメッシュの情報をオリジナルに焼き付けて出力に適した形にする
        """

        # 確認が取れていない場合には打ち切る
        if not self.is_ready:
            return

        # skinの保存
        self._save_skin_info()

        # 転写もとに頂点カラーが当たっていない場合は作成する
        self._apply_vertex_color()

        # 法線情報をUV3,4へ転送
        self._transfer_normal_to_uv()

        # メッシュデータを最適化
        self._optimise_all()

        # skinの復元
        self._load_skin_info()

    def _save_skin_info(self):
        """スキニング情報を保持
        """

        self.__saved_skin_datas = []

        if not self.base_node:
            return

        for mesh in cmds.listRelatives(self.base_node, ad=True, type='transform', fullPath=True):

            skin_cluster = cmds.ls(cmds.listHistory(mesh), typ='skinCluster')

            if skin_cluster:

                skined_joints = cmds.ls(cmds.listConnections(skin_cluster, t='joint'), l=True)
                skin_info = base_class.mesh.skin_info.SkinInfo()
                skin_info.create_info([mesh])
                self.__saved_skin_datas.append(
                    {'mesh': mesh, 'joints': skined_joints, 'info': skin_info}
                )

    def _load_skin_info(self):
        """保持したスキニングをロード
        """

        if not self.__saved_skin_datas:
            return
        
        for skin_data in self.__saved_skin_datas:

            if not cmds.objExists(skin_data['mesh']):
                continue

            skin_cluster = cmds.ls(cmds.listHistory(skin_data['mesh']), typ='skinCluster')
            if not skin_cluster:
                cmds.skinCluster(skin_data['mesh'], skin_data['joints'], omi=False, bm=0, mi=2, rui=False, sm=0)

            dst_skin_info = base_class.mesh.skin_info.SkinInfo()
            dst_skin_info.create_info([skin_data['mesh']])

            base_utility.mesh.skin.paste_weight_by_vertex_index(skin_data['info'], dst_skin_info)

    def _apply_vertex_color(self):
        """頂点カラーが設定されていない場合はべた塗りを準備する
        """

        colorset_list = []
        for outline_mesh in self.outline_mesh_list:

            colorset_list = base_utility.mesh.colorset.get_colorset_list(outline_mesh)

            if not colorset_list:
                cmds.select(outline_mesh, r=True)
                cmds.polyColorPerVertex(r=1, g=1, b=1, a=1, cdo=True)

            cmds.delete(outline_mesh, ch=True)

    def _transfer_normal_to_uv(self):
        """法線情報をUVへ焼き付ける
        """
        for outline_mesh in self.outline_mesh_list:

            original_mesh = self._get_original_name(outline_mesh)

            if cmds.objExists(original_mesh):
                utility_normal_to_uv(outline_mesh, original_mesh, constants.UVSET_FOR_NORMAL_XY, constants.UVSET_FOR_NORMAL_Z)

                sub_normal_vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
                sub_normal_vtxcolor_info.create_info([outline_mesh])

                duplicate_vtxcolor_info = base_class.mesh.vertex_color_info.VertexColorInfo()
                duplicate_vtxcolor_info.create_info([original_mesh])

                base_utility.mesh.vertex_color.paste_vertex_color_by_vertex_index(sub_normal_vtxcolor_info, duplicate_vtxcolor_info)

    def _optimise_all(self):
        """不要箇所を削除したりして、出力に適した形に修正
        """
        for outline_mesh in self.outline_mesh_list:

            original_mesh = self._get_original_name(outline_mesh)
            if cmds.objExists(original_mesh):
                self._optimise_uvset(original_mesh)
                self._optimize_colorset(original_mesh)

            # 親が先に消されていたりする場合エラーとなるため、存在確認をはさむ
            # 以後、アウトラインメッシュは不要なため取り除く
            if cmds.objExists(outline_mesh):
                cmds.delete(outline_mesh)

    def _optimise_uvset(self, target_transform):
        """UV関連の調整

        Args:
            target_transform (str): 対象のトランスフォームのフルパス
        """
        cmds.delete(target_transform, ch=True)

        max_uvset = 2
        create_uv = False

        this_uvset_list = base_utility.mesh.uvset.get_uvset_list(target_transform)

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

                current_uvset_list = base_utility.mesh.uvset.get_uvset_list(target_transform)

                if len(current_uvset_list) >= max_uvset:
                    break

                temp_uvset = 'temp{0}'.format(p)

                base_utility.mesh.uvset.create(target_transform, temp_uvset)

                base_utility.mesh.uvset.set_current(target_transform, temp_uvset)

                cmds.polyAutoProjection(target_transform + '.f[0]')

        base_utility.mesh.uvset.change_index(target_transform, constants.UVSET_FOR_NORMAL_XY, 2)
        base_utility.mesh.uvset.change_index(target_transform, constants.UVSET_FOR_NORMAL_Z, 3)

        uvset_list = base_utility.mesh.uvset.get_uvset_list(target_transform)
        for this_uvset in uvset_list:

            this_uvset_index = base_utility.mesh.uvset.get_index(target_transform, this_uvset)

            if this_uvset_index < max_uvset:
                continue

            base_utility.mesh.uvset.delete(target_transform, this_uvset)

        base_utility.mesh.uvset.set_current_from_index(target_transform, 0)

        cmds.delete(target_transform, ch=True)

    def _optimize_colorset(self, target_transform):
        """UVを調整

        Args:
            target_transform (str): 対象のトランスフォームのフルパス
        """

        if not base_utility.node.exists(target_transform):
            return

        cmds.delete(target_transform, ch=True)

        first_colorset = base_utility.mesh.colorset.get_colorset_from_index(target_transform, 0)

        base_utility.mesh.colorset.delete(target_transform, constants.OUTPUT_COLORSET)
        base_utility.mesh.colorset.create(target_transform, constants.OUTPUT_COLORSET)
        base_utility.mesh.colorset.blend(target_transform, constants.OUTPUT_COLORSET, first_colorset, 'over')
        base_utility.mesh.colorset.change_index(target_transform, constants.OUTPUT_COLORSET, 0)

        colorset_list = base_utility.mesh.colorset.get_colorset_list(target_transform)

        for this_colorset in colorset_list:

            if this_colorset == constants.OUTPUT_COLORSET:
                continue

            base_utility.mesh.colorset.delete(target_transform, this_colorset)

        base_utility.mesh.colorset.set_current(target_transform, constants.OUTPUT_COLORSET)

        cmds.delete(target_transform, ch=True)

    def _get_original_name(self, target_name):
        """アウトラインのフルパスからオリジナルのフルパスを取得する

        Args:
            target_name (str): オリジナルメッシュを探したいアウトラインのフルパス

        Returns:
            str: オリジナルのメッシュのフルパス
        """
        parent_path, base_name = target_name.rsplit('|', 1)
        return parent_path + '|' + base_name.replace(constants.SUB_NORMAL_SUFFIX,'')

    @staticmethod
    def is_outline_process_target(node):

        for match in constants.OUTLINE_PROCESS_TARGET_REGEX_LIST:
            if re.search(match, node):
                return True
        return False
