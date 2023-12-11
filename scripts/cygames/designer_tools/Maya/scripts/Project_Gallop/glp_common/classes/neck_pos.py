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

import math

import maya.cmds as cmds
from .. import classes as glp_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NeckPositionInfo(object):

    # ===============================================
    def __init__(self):

        # region 定数

        self.set_name = 'NeckEdgeSet'

        self.suffix_list = [
            '_Height_SS',
            '_Height_L',
            '_Shape_1',
            '_Shape_2',
            '_Bust_SS',
            '_Bust_S',
            '_Bust_L',
            '_Bust_LL'
        ]

        self.height_ss_suffix = '_Height_SS'
        self.height_l_suffix = '_Height_L'

        # 以下運用モデルから計測したHeadから各頂点への位置ベクトル
        self.default_pos_from_head_list = [
            [0.0, -1.5779866655318244, 3.9121787834167865],
            [1.6488499641418457, -1.129424043461512, 3.2342957544327167],
            [-1.6488499641418457, -1.129424043461512, 3.2342957544327167],
            [2.8118231296539307, -0.6455068071333869, 1.4194979953766254],
            [-2.8118231296539307, -0.6455068071333869, 1.4194979953766254],
            [3.0871293544769287, -0.15591330127401193, -1.082383365631065],
            [-3.0871293544769287, -0.15591330127401193, -1.082383365631065],
            [2.000286102294922, 0.05314736767130057, -2.6636268806457135],
            [-2.000286102294922, 0.05314736767130057, -2.6636268806457135],
            [0.0, -0.02551168994588693, -3.580390663146934],
        ]

        self.height_ss_pos_from_head_list = [
            [0.0, -1.5779866655318244, 4.019833831787148],
            [1.6941499710083008, -1.129424043461512, 3.32332661628727],
            [-1.6941499710083008, -1.129424043461512, 3.32332661628727],
            [2.88907527923584, -0.6455068071333869, 1.458669929504433],
            [-2.88907527923584, -0.6455068071333869, 1.458669929504433],
            [3.171945333480835, -0.15591330127401193, -1.1119472694396588],
            [-3.171945333480835, -0.15591330127401193, -1.1119472694396588],
            [2.0552420616149902, 0.05314736767130057, -2.7366339874267194],
            [-2.0552420616149902, 0.05314736767130057, -2.7366339874267194],
            [0.0, -0.02551168994588693, -3.6785847854613873],
        ]

        self.height_l_pos_from_head_list = [
            [0.0, -1.5779866655318244, 3.8493517923355487],
            [1.6211999654769897, -1.129424043461512, 3.1828367996216205],
            [-1.6211999654769897, -1.129424043461512, 3.1828367996216205],
            [2.7646713256835938, -0.6455068071333869, 1.3984718608856586],
            [-2.7646713256835938, -0.6455068071333869, 1.3984718608856586],
            [3.0353612899780273, -0.15591330127401193, -1.0614545059203717],
            [-3.0353612899780273, -0.15591330127401193, -1.0614545059203717],
            [1.966742992401123, 0.05314736767130057, -2.6161815834045026],
            [-1.966742992401123, 0.05314736767130057, -2.6161815834045026],
            [0.0, -0.02551168994588693, -3.5175721359252545],
        ]

        # endregion

        # region その他のメンバ

        self.neck_edge_list = None

        # endregion

    # ==================================================
    def __print_log(self, msg):

        # python3で文字化けしてしまうため分岐させる
        if sys.version_info.major == 2:
            log_msg = msg.encode('shift_jis')
            print(log_msg)
        else:
            print(msg)

    # ==================================================
    def move_to_default_value(self):

        current_chara_info = glp_class.info.chara_info.CharaInfo()
        current_chara_info.create_info(cmds.file(q=True, sn=True))

        if not current_chara_info.exists:
            print("Chara Infoが見つからないため実行できません")
            return

        current_selection = cmds.ls(selection=True)

        self.neck_edge_list = []

        # ------------------------------
        # 設定

        torelance = 0.001

        if not cmds.objExists(self.set_name):
            msg_str = 'NeckEdgeがありません。'
            self.__print_log(msg_str)
            return

        neck_edge_list = cmds.ls(cmds.sets(self.set_name, q=True), fl=True)
        if not neck_edge_list:
            msg_str = 'NeckEdgeに何も含まれていません。'
            self.__print_log(msg_str)
            return

        vertices = cmds.ls(cmds.polyListComponentConversion(neck_edge_list, tv=True), l=True, fl=True)
        if not vertices:
            cmds.ls(current_selection)
            return

        fix_vertices = []

        for vtx in vertices:

            if not current_chara_info.data_type.endswith('head') and \
                    not current_chara_info.data_type.endswith('body'):
                cmds.ls(current_selection)
                return

            # headならネックエッジ頂点をそのまま追加
            if current_chara_info.data_type.endswith('head'):
                fix_vertices.append(vtx)
                continue

            # bodyは体型差分のネックエッジも考慮する
            for suffix in self.suffix_list:

                if vtx.find(suffix) >= 0:
                    # 体型差分の頂点もNeckEdgeSetに含まれている場合の処理
                    fix_vertices.append(vtx)

                else:

                    # M_Bodyの頂点の場合、体型差分の頂点も追加対象にする
                    fix_vertices.append(vtx)

                    diff_vtx = vtx.replace('|M_Body', '{0}|M_Body{0}'.format(suffix))

                    if cmds.objExists(diff_vtx) and diff_vtx not in fix_vertices:
                        fix_vertices.append(diff_vtx)

        fix_vertices.sort()

        for vtx in fix_vertices:

            base_pos = [0.0, 0.0, 0.0]

            # Headが見つかった場合はHeadからの相対位置をとる
            short_name = vtx.split('|')[-1]
            root_node = vtx.replace('|' + short_name, '')

            descendent_joint_list = []
            if cmds.objExists(root_node):
                descendent_joint_list = cmds.listRelatives(root_node, ad=True, type='joint', f=True)

            for descendent_joint in descendent_joint_list:
                if descendent_joint.endswith('Head'):
                    base_pos = cmds.xform(descendent_joint, q=True, ws=True, t=True)

            vtx_pos = cmds.xform(vtx, q=True, ws=True, t=True)

            vtx_pos_from_base = [
                vtx_pos[0] - base_pos[0],
                vtx_pos[1] - base_pos[1],
                vtx_pos[2] - base_pos[2],
            ]

            ref_pos_list = self.default_pos_from_head_list

            if not current_chara_info.data_info or current_chara_info.data_info.height_id is None:
                # 身長idが取れない汎用衣装などは接尾語からref_pos_listを判定
                if vtx.find(self.height_ss_suffix) >= 0:
                    ref_pos_list = self.height_ss_pos_from_head_list
                elif vtx.find(self.height_l_suffix) >= 0:
                    ref_pos_list = self.height_l_pos_from_head_list
                else:
                    ref_pos_list = self.default_pos_from_head_list
            else:
                # 身長idが取れる場合はそこからref_pos_listを判定
                height_id = int(current_chara_info.data_info.height_id)

                if height_id < 1:
                    ref_pos_list = self.height_ss_pos_from_head_list
                elif height_id > 1:
                    ref_pos_list = self.height_l_pos_from_head_list

            is_error = True
            nearest_ref_distance = 10000
            nearest_ref_pos = [0, 0, 0]

            for ref_pos in ref_pos_list:

                # 最も近い移動先頂点を求める
                x_diff = vtx_pos_from_base[0] - ref_pos[0]
                y_diff = vtx_pos_from_base[1] - ref_pos[1]
                z_diff = vtx_pos_from_base[2] - ref_pos[2]

                x_square = math.pow(x_diff, 2)
                y_square = math.pow(y_diff, 2)
                z_square = math.pow(z_diff, 2)

                this_distance = math.sqrt(x_square + y_square + z_square)

                if this_distance < nearest_ref_distance:
                    nearest_ref_distance = this_distance
                    nearest_ref_pos = ref_pos

                # 許容範囲以内のものを見つけたらloopから離脱し、移動もさせない
                if abs(x_diff) < torelance and abs(y_diff) < torelance and abs(z_diff) < torelance:
                    is_error = False
                    break

            if is_error:
                cmds.move(nearest_ref_pos[0] - vtx_pos_from_base[0], nearest_ref_pos[1] - vtx_pos_from_base[1], nearest_ref_pos[2] - vtx_pos_from_base[2], vtx, r=True)

        cmds.select(current_selection)
