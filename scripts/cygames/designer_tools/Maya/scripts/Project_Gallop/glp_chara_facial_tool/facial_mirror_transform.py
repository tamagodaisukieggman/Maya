# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialMirrorTransform(object):

    # ==================================================
    def _get_pair_list(self):
        """
        ユーザーの選択からコントロールリグ用（末尾が_Ctrl）の
        transformノードの左右のペアのリストのリストを返す。
        パスの_Lと_Rを置き換えたものがペア
        Returns:
            list[list[]]: [[選択アイテム, 選択アイテムのペア][選択アイテム, 選択アイテムのペア]]
        """
        selection_list = cmds.ls(sl=True, l=True, fl=True, typ='transform')

        selected_ctrls = []
        for selection in selection_list:
            # 名前が「_Ctrl」で終わっているトランスフォームのみリスト
            if selection.endswith('_Ctrl'):
                selected_ctrls.append(selection)

        if not selected_ctrls:
            cmds.warning('「_Ctrl」リグを選択してから実行してください')
            return

        result_pair_list = []
        for selected_path in selected_ctrls:
            if selected_path.find('_R_Ctrl') >= 0:
                pair_path = selected_path.replace('_R_', '_L_')
                # |Rig_eye_high|Eye_high_root_R|Eye_big_info_R_Ctrl みたいなパスの対応
                pair_path = pair_path.replace('_R|', '_L|')
                result_pair_list.append([selected_path, pair_path])
            elif selected_path.find('_L_Ctrl') >= 0:
                pair_path = selected_path.replace('_L_', '_R_')
                pair_path = pair_path.replace('_L|', '_R|')
                result_pair_list.append([selected_path, pair_path])
        return result_pair_list

    # ==================================================
    def x_mirror_transform(self):
        """
        選択中の_Ctrlトランスフォームの位置、回転、スケールを左右反対側の_Ctrlに反映します
        """
        src_dst_pair_list = self._get_pair_list()

        if not src_dst_pair_list:
            return

        # [オブジェクト, 移動, 回転, スケール]の配列を作成
        final_move_list = []

        for pair in src_dst_pair_list:

            src_ctrl = pair[0]  # ユーザーが選択した_Ctrl
            dst_ctrl = pair[1]  # 反対側の_Ctrl

            if not cmds.objExists(dst_ctrl):
                cmds.warning('対のCtrlが見つかりませんでした: ' + str(dst_ctrl))
                continue

            src_translate = cmds.xform(src_ctrl, q=True, t=True)
            src_rotate = cmds.xform(src_ctrl, q=True, ro=True)
            src_scale = cmds.xform(src_ctrl, q=True, s=True, r=True)

            # gallopでは親にマイナススケールが入っていて左右の_Ctrlには同じ値が入るのが仕様
            if src_ctrl == dst_ctrl:
                # _Ctrlでフルパスに_Lや_Rが入っていないものは-1で変換（何のためかは不明）
                dst_translate = [src_translate[0] * -1, src_translate[1], src_translate[2]]
                dst_rotate = [src_rotate[0], src_rotate[1] * -1, src_rotate[2] * -1]
            else:
                dst_translate = [src_translate[0], src_translate[1], src_translate[2]]
                dst_rotate = [src_rotate[0], src_rotate[1], src_rotate[2]]

            dst_scale = src_scale
            final_move_list.append([dst_ctrl, dst_translate, dst_rotate, dst_scale])

        # ミラー実行
        for final_move in final_move_list:
            cmds.warning('ミラーコピーしました: ' + final_move[0])
            cmds.xform(final_move[0], t=final_move[1], a=True)
            cmds.xform(final_move[0], ro=final_move[2], a=True)
            cmds.xform(final_move[0], s=final_move[3], a=True)
