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

from ....base_common import classes as base_class
from ....base_common import utility as base_utility

from ....glp_common.classes import neck_normal


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

            outline = select_transform + '_Outline'

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

            # 元アウトラインと新アウトラインの頂点情報を取得
            src_vtx_datas = base_class.vertex.get_vtx_datas([src_mesh])
            dst_vtx_datas = base_class.vertex.get_vtx_datas([dst_mesh])

            # 頂点位置検索して法線をコピー
            # 元の法線がロックされている部分のみに限定
            copy_vtx_datas = base_class.vertex.get_nearest_pos_vtx_datas(dst_vtx_datas, src_vtx_datas)
            base_utility.normal.copy_normal(copy_vtx_datas, dst_vtx_datas, keep_edge_state=True, from_lock_only=True)

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
