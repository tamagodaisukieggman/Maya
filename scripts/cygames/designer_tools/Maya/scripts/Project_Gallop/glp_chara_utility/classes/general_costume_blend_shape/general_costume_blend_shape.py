# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

from PySide2 import QtWidgets

import maya.cmds as cmds

from ....glp_common.classes.info import chara_info

reload(chara_info)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GeneralCostumeBlendShape(object):
    """汎用衣装の出力用ブレンドシェイプを一括作成する
    """

    # ==================================================
    def create_general_costume_blend_shape(self, should_show_information=False):
        """汎用衣装の出力用ブレンドシェイプを一括作成する
        """

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if not _chara_info.exists:
            return

        # 汎用衣装でのみ実行する(Mini含む)
        if _chara_info.part_info.is_unique_chara or not _chara_info.part_info.data_type.endswith('body'):
            if should_show_information:
                cmds.warning('この機能は汎用衣装にのみ対応しています')
            return

        root_node = _chara_info.part_info.root_node
        if not cmds.objExists(root_node):
            if should_show_information:
                cmds.warning('シーン名から想定したキャラクターのルートが見つかりません: {}'.format(_chara_info.part_info.root_node))
            return

        org_mesh_node_list = [mesh for mesh in _chara_info.part_info.mesh_list if cmds.objExists(mesh)]
        if not org_mesh_node_list:
            if should_show_information:
                cmds.warning('シーン名から想定したキャラクターのメッシュが見つかりません: {}'.format(_chara_info.part_info.root_node))
            return

        is_skin_cluster = False
        blendshape_target_node_list_dict = {}

        # 体型差分ノードの特定
        assemblies_node_list = cmds.ls(assemblies=True, l=True)
        for assemblies_node in assemblies_node_list:

            # 体型差分の命名規則に合致しないものとルートノード自身は対象にしない
            if assemblies_node.find(root_node) > 0 or root_node == assemblies_node:
                continue

            for org_mesh_node in org_mesh_node_list:

                mesh_name = org_mesh_node.split('|')[-1]

                suffix = assemblies_node.replace(root_node, '')
                target_node = '{0}|{1}{2}'.format(assemblies_node, mesh_name, suffix)
                if not cmds.objExists(target_node):
                    continue
                target_node_shapes = cmds.listRelatives(target_node, shapes=True)
                if not target_node_shapes:
                    continue

                # 体型差分側にSkinClusterがついていたらBlendShapeが正常に動作しない可能性があるため
                # デタッチを促すために処理を中断する
                if cmds.listConnections(target_node_shapes[0], type='skinCluster'):
                    is_skin_cluster = True
                    break

                if mesh_name not in blendshape_target_node_list_dict:
                    blendshape_target_node_list_dict[mesh_name] = []

                blendshape_target_node_list_dict[mesh_name].append(target_node)

        if is_skin_cluster:
            if should_show_information:
                text = '体型差分にSkinClusterが設定されているため、処理を中断しました\nデタッチしてから利用してください'
                QtWidgets.QMessageBox.warning(None, '警告', text, QtWidgets.QMessageBox.Ok)
            return

        if not blendshape_target_node_list_dict:
            return

        # 対象のメッシュについているblendShapeノードを一度削除してきれいにする
        for org_mesh_node in org_mesh_node_list:
            mesh_blendshape_list = cmds.ls(cmds.listHistory(org_mesh_node), type='blendShape')
            for org_mbody_blendshape in mesh_blendshape_list:
                cmds.delete(org_mbody_blendshape)

        # 改めてblendShapeセット
        for org_mesh_node in org_mesh_node_list:
            mesh_name = org_mesh_node.split('|')[-1]
            cmds.blendShape(blendshape_target_node_list_dict[mesh_name] + [org_mesh_node], automatic=True)

        if should_show_information:
            text = '汎用衣装用のBlendShape作成が完了しました'
            QtWidgets.QMessageBox.information(None, '完了', text, QtWidgets.QMessageBox.Ok)
