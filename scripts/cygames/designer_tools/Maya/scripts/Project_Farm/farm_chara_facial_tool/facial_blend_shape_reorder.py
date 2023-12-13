# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
    from importlib import reload
except:
    pass

import os
import sys
import re
import glob
import time

import maya.cmds as cmds
import maya.mel as mel

from .. import farm_common
from ..farm_common.utility import model_define
from . import facial_blend_shape_info

reload(farm_common)
reload(facial_blend_shape_info)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialBlendShapeReorder(object):

    # ===============================================
    def __init__(self):

        self.TMP_BLEND_SHAPE_NODE = 'reorder_tmp_blend_shape'
        self.FACE_MESH_NAME = model_define.MESH_PREFIX + 'face'

        self.face_mesh = None
        self.blend_shape_node = None
        self.blend_shape_info = None

    # ===============================================
    def initialize(self, blend_shape_info):

        self.__init__()
        self.face_mesh = self.__get_face_mesh()
        self.blend_shape_node = self.__get_taget_blend_shape_node()

        self.blend_shape_info = blend_shape_info
        if not self.blend_shape_info.is_initialized:
            self.blend_shape_info.initialize()

    # ===============================================
    def __get_face_mesh(self):

        face_list = cmds.ls(self.FACE_MESH_NAME, typ='transform')

        if face_list:
            return face_list[0]

    # ===============================================
    def __get_taget_blend_shape_node(self):

        if not self.face_mesh or not cmds.objExists(self.face_mesh):
            return None

        blend_shape_nodes = cmds.ls(cmds.listHistory(self.face_mesh), typ='blendShape')

        # ブレンドシェイプはシーンにフェイシャル用の一つのみのはず
        if blend_shape_nodes:
            return blend_shape_nodes[0]
        else:
            return None

    # ===============================================
    def reorder_blend_shape_index(self):

        if not self.blend_shape_node:
            return

        if not self.blend_shape_info.blend_shape_item_list:
            return

        target_dict_list = self.__get_target_dict_list()

        org_blend_shape = self.blend_shape_node
        new_blend_shape = cmds.blendShape(
            self.face_mesh, at=True, n=self.TMP_BLEND_SHAPE_NODE)[0]

        # blendShapeの対象shape
        base_shape = cmds.blendShape(new_blend_shape, q=True, g=True)[0]

        for target_dict in target_dict_list:

            alias = target_dict.get('alias')
            index = target_dict.get('index')

            target_mesh = self.__duplicate_target(index, base_shape)

            # 追加するインデックス
            max_index = cmds.blendShape(new_blend_shape, q=True, wc=True)

            cmds.blendShape(
                new_blend_shape,
                e=True,
                t=(base_shape, max_index, target_mesh, 1))

            cmds.delete(target_mesh)

            # ベースメッシュを複製した場合は形状をリセット
            if index is None:
                cmds.blendShape(new_blend_shape, e=True, rtd=(0, max_index))

            # エイリアスの設定
            attr = '{}.w[{}]'.format(new_blend_shape, max_index)
            if cmds.aliasAttr(attr, q=True) != alias:
                cmds.aliasAttr(alias, attr)

        cmds.delete(org_blend_shape)
        cmds.rename(new_blend_shape, org_blend_shape)

    # ===============================================
    def __get_target_dict_list(self):
        """インデックス順に並んだターゲットのリストを返す
        """

        target_dict_list = []

        # csvには抜けはないはずなので、index順に並び替えてそのまま使う
        index_order_item_list = sorted(
            self.blend_shape_info.blend_shape_item_list,
            key=lambda x: x.index)

        alias_dict = self.__get_alias_index_dict()

        target_list = [item.target for item in index_order_item_list]

        # シーン内のみに存在するターゲットを末尾に追加
        extra_target_list = sorted(set(alias_dict.keys()) - set(target_list))
        target_list.extend(extra_target_list)

        for target in target_list:
            target_dict = {
                'alias': target,
                'index': alias_dict.get(target)}
            target_dict_list.append(target_dict)

        return target_dict_list

    def __duplicate_target(self, index, base_shape):
        """指定されたターゲットを複製する
        """

        # ターゲットメッシュ
        target_mesh = None

        if index is not None:
            # ターゲットメッシュが存在するかチェック
            plug = ('{}'.format(self.blend_shape_node)
                    + '.inputTarget[0]'
                    + '.inputTargetGroup[{}]'.format(index)
                    + '.inputTargetItem[6000]'
                    + '.inputGeomTarget')
            target_mesh_list = cmds.listConnections(plug, d=False, s=True)

            # ターゲットメッシュが存在する場合はそれを複製
            if target_mesh_list:
                target_mesh = cmds.duplicate(target_mesh_list[0])[0]
            # ターゲットメッシュが存在しない場合はblendShapeの情報からメッシュを作成
            else:
                target_mesh = cmds.sculptTarget(
                    self.blend_shape_node, e=True, r=True, t=index)[0]
        # 対象のインデックスがない場合はベースメッシュを複製
        else:
            target_mesh = cmds.duplicate(base_shape)[0]
            resetDelta = True

        return target_mesh

    # ===============================================
    def __get_alias_index_dict(self):
        """blendShapeに存在するエイリアスとインデックスの辞書を返す
        """

        alias_list = cmds.aliasAttr(self.blend_shape_node, q=True)

        alias_index_dict = {}

        pattern = re.compile(r'weight\[(\d.*)\]')

        # alias_listはtarget, weight[x]のペアが連なっている
        for i in range(0, len(alias_list), 2):
            alias = alias_list[i]
            # weight[x]の添字のみ取り出す
            index = int(pattern.search(alias_list[i + 1]).group(1))
            alias_index_dict[alias] = index

        return alias_index_dict
