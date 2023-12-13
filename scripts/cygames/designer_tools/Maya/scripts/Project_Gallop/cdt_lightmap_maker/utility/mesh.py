# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from . import name as utility_name
from . import list as utility_list
from . import node as utility_node


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ==================================================
    @staticmethod
    def get_mesh_shape(target_transform):
        """シェープノードを取得

        :param target_transform: 対象となるトランスフォーム
        """

        if not utility_node.Method.exist_transform(target_transform):
            return

        long_target_name = utility_name.Method.get_long_name(target_transform)

        if long_target_name is None:
            return

        shapes = cmds.listRelatives(long_target_name, shapes=True, f=True)

        if not utility_list.Method.exist_list(shapes):
            return

        long_shape_name = utility_name.Method.get_long_name(shapes[0])

        if long_shape_name is None:
            return

        if cmds.objectType(long_shape_name) != 'mesh':
            return

        return long_shape_name

    # ===============================================
    @staticmethod
    def combine_mesh(target_transform_list, combined_transform_name):
        """メッシュを統合
        統合されたメッシュはワールドに置かれます

        :param target_transform_list: 対象となるトランスフォームリスト
        :param combine_name: 統合トランスフォーム名
        """

        if utility_node.Method.exist_node(combined_transform_name):
            return

        # 存在するトランスフォームのみに絞る
        fix_target_transform_list = []

        for target_transform in target_transform_list:

            if not utility_node.Method.exist_transform(target_transform):
                continue

            fix_target_transform_list.append(target_transform)

        if len(fix_target_transform_list) == 0:
            return

        # 下層に存在するメッシュを検索
        cmds.select(fix_target_transform_list, r=True)
        cmds.select(hi=True)

        child_transform_list = cmds.ls(sl=True, l=True, typ='transform')

        mesh_transform_list = []

        for child_transform in child_transform_list:

            this_mesh = Method.get_mesh_shape(child_transform)

            if this_mesh is None:
                continue

            mesh_transform_list.append(child_transform)

        dummy_transform_list = []

        if len(mesh_transform_list) == 0:
            return

        if len(mesh_transform_list) == 1:

            # メッシュが一つの場合はコンバインできないので、
            # そのメッシュの名前を変えて対応

            try:
                mesh_transform_list[0] = \
                    cmds.parent(mesh_transform_list[0], w=True)[0]
            except Exception:
                pass

            cmds.rename(mesh_transform_list[0], combined_transform_name)

            for child_transform in child_transform_list:

                if not utility_node.Method.exist_transform(child_transform):
                    continue

                cmds.delete(child_transform)

        else:

            # ダミーグループを一旦作り、コンバイン時に親が消えないようにする
            for this_transform in fix_target_transform_list:

                parent_list = cmds.listRelatives(this_transform, p=True, f=True)

                if not utility_list.Method.exist_list(parent_list):
                    continue

                parent_transform = utility_name.Method.get_long_name(
                    parent_list[0])

                cmds.group(name='__dummy', em=True, p=parent_transform)

                dummy_transform = parent_transform + '|__dummy'

                dummy_transform_list.append(dummy_transform)

            # コンバイン
            cmds.polyUnite(
                fix_target_transform_list,
                ch=False,
                mergeUVSets=True,
                name=combined_transform_name
            )

        combined_transform = '|' + combined_transform_name

        cmds.delete(combined_transform, ch=True)

        if utility_list.Method.exist_list(dummy_transform_list):
            cmds.delete(dummy_transform_list)

        return combined_transform
