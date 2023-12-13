# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility

from ....priari_common.classes import neck_normal
from ....priari_common.utility import model_define

reload(model_define)


class CreateOutline(object):

    def create_outline_with_current_normal(self, should_show_ui=True):
        """
        """

        if should_show_ui and not base_utility.ui.dialog.open_ok_cancel('確認', '現在のアウトラインの法線を使ってアウトラインモデルを再生成しますか？'):
            return

        select_transform_list = cmds.ls(sl=True, l=True, fl=True, et='transform')

        if not select_transform_list:

            if should_show_ui:
                base_utility.ui.dialog.open_ok(
                    '確認', 'アウトラインを作成するメッシュが選択されていません'
                )
            return

        # メッシュと対応する現在のアウトラインメッシュのペアを作成
        target_pair_list = []

        for select_transform in select_transform_list:

            outline = select_transform + model_define.OUTLINE_SUFFIX

            if cmds.objExists(outline):
                target_pair_list.append([select_transform, outline])

        if not target_pair_list:

            if should_show_ui:
                base_utility.ui.dialog.open_ok(
                    '確認', '選択しているオブジェクトのアウトラインが存在していません'
                )
            return

        for target_pair in target_pair_list:

            src_mesh = target_pair[1]
            dst_mesh = cmds.duplicate(target_pair[0])[0]

            # 新アウトラインの法線を一度全てアンロック
            cmds.polyNormalPerVertex(dst_mesh, ufn=True)

            src_vtx_list = cmds.ls(src_mesh + '.vtx[*]', l=True, fl=True)

            # 元アウトラインの法線ロックしている頂点を取得
            src_normal_lock_vtx_list = []

            for src_vtx in src_vtx_list:

                normal_lock_list = cmds.polyNormalPerVertex(src_vtx, q=True, fn=True)

                if True not in normal_lock_list:
                    continue

                src_normal_lock_vtx_list.append(src_vtx)

            dst_vtx_list = cmds.ls(dst_mesh + '.vtx[*]', l=True, fl=True)

            # 元アウトラインに法線ロックされている頂点がなければ、そのまま入れ替えて終了
            if not src_normal_lock_vtx_list:

                new_outline = self._replace_outline(src_mesh, dst_mesh)

                # 複製で不必要に追加されたネックエッジを除去
                neck_edge_set = neck_normal.NeckNormalInfo()
                neck_edge_set.remove_edge_from_neck_edge_set_by_name(new_outline)
                continue

            src_normal_info = base_class.mesh.normal_info.NormalInfo()
            src_normal_info.create_info(src_normal_lock_vtx_list)

            # 新アウトラインメッシュで法線転写する頂点を捜索するための一時インフォ
            dst_tmp_info = base_class.mesh.vertex_position_info.VertexPositionInfo()
            dst_tmp_info.create_info(dst_vtx_list)

            if not src_normal_info.info_item_list or not dst_tmp_info.info_item_list:
                cmds.delete(dst_mesh)
                continue

            # 元アウトラインのロックされている頂点と、それに一番近い新アウトライン上の頂点のインデックスペアリストを作成
            # 元と対になる新を探したいので、srcとdstを逆順で検索
            nearest_vtx_index_pair_list = base_utility.mesh.get_vertex_index_pair_list_by_position(
                dst_tmp_info.info_item_list[0].target_vertex_index_list,
                dst_tmp_info.info_item_list[0].world_vertex_position_info_list,
                src_normal_info.info_item_list[0].target_vertex_index_list,
                src_normal_info.info_item_list[0].world_vertex_position_info_list,
            )

            # 法線転写
            dst_target_vtx_list = []

            if nearest_vtx_index_pair_list:
                for vtx_index_pair in nearest_vtx_index_pair_list:
                    dst_target_vtx_list.append(dst_mesh + '.vtx[{}]'.format(vtx_index_pair[0]))

            dst_normal_info = base_class.mesh.normal_info.NormalInfo()
            dst_normal_info.create_info(dst_target_vtx_list)

            base_utility.mesh.normal.paste_normal_by_vertex_position(src_normal_info, dst_normal_info)

            # アウトラインの入れ替え
            new_outline = self._replace_outline(src_mesh, dst_mesh)

            # 複製で不必要に追加されたネックエッジを除去
            neck_edge_set = neck_normal.NeckNormalInfo()
            neck_edge_set.remove_edge_from_neck_edge_set_by_name(new_outline)

    def _replace_outline(self, org_outline, new_outline):
        """
        """

        if not cmds.objExists(org_outline) or not cmds.objExists(new_outline):
            return

        cmds.polySoftEdge(new_outline, a=180)
        cmds.setAttr(new_outline + '.visibility', 0)
        cmds.delete(org_outline)
        cmds.delete(new_outline, ch=True)
        result_outline = cmds.rename(new_outline, org_outline.split('|')[-1])

        return result_outline
