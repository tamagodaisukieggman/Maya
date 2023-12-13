# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from . import facial_tear_attach

reload(facial_tear_attach)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialTearAnimController(object):
    """
    涙リファレンスのUVアニメーションを操作するクラス
    """

    # ===============================================
    def __init__(self):

        # ------------------------------
        # 定数

        # UVアニメーションのコマ割り
        self.row_len = 16
        self.column_len = 8

        # UVを制御をするメッシュ
        self.target_mesh_name = 'M_Tear'

        # ------------------------------
        # メンバ変数
        self.tear_mesh_list = None
        self.uv_list = None
        self.current_frame = 0

    # ===============================================
    def update(self):
        """
        現在の涙の状態を取得
        ユーザーが操作している可能性があるので各処理の前で必ず呼ぶ
        """

        # 涙メッシュの検索
        self.tear_mesh_list = []

        tear_attach = facial_tear_attach.FacialTearAttach()
        tear_attach.check_data()
        tear_attach.create_attach_info_dict_list()

        for attach_info_dict in tear_attach.attach_info_dict_list:

            namespace = attach_info_dict.get('namespace')

            if not namespace:
                continue

            target_meshes = cmds.ls('{}:{}'.format(namespace, self.target_mesh_name), typ='transform', l=True)

            if not target_meshes:
                continue

            self.tear_mesh_list.append(target_meshes[0])

        # 涙のUVの取得
        self.uv_list = []

        for tear_mesh in self.tear_mesh_list:
            this_uv_list = cmds.polyListComponentConversion(tear_mesh, tuv=True)
            this_uv_list = cmds.ls(this_uv_list, fl=True, l=True)
            self.uv_list.extend(this_uv_list)

        # 現在のフレームの取得
        self.current_frame = self.__get_current_tear_frame()

    # ===============================================
    def go_to_next_frame(self):
        """
        UVアニメーションを次のコマへ進める
        """

        self.update()

        if not self.uv_list:
            return

        self.go_to_frame(self.current_frame + 1)

    # ===============================================
    def go_to_previous_frame(self):
        """
        UVアニメーションを前のコマへ戻す
        """

        self.update()

        if not self.uv_list:
            return

        self.go_to_frame(self.current_frame - 1)

    # ===============================================
    def go_to_frame(self, dst_frame):
        """
        UVアニメーションを指定のコマへ飛ばす
        """

        self.update()

        if not self.uv_list:
            return

        uv_value = self.__calc_relative_uv_value(self.current_frame, dst_frame)

        cmds.polyEditUV(self.uv_list, u=uv_value[0], v=uv_value[1])

    # ===============================================
    def __calc_relative_uv_value(self, src_frame, dst_frame):

        src_frame = self.optimize_frame(src_frame)
        dst_frame = self.optimize_frame(dst_frame)

        src_row = src_frame // self.column_len
        src_column = src_frame % self.column_len

        dst_row = dst_frame // self.column_len
        dst_column = dst_frame % self.column_len

        u_value = (dst_column - src_column) * (1.0 / self.column_len)
        v_value = (dst_row - src_row) * (1.0 / self.row_len) * -1

        return [u_value, v_value]

    # ===============================================
    def optimize_frame(self, frame):
        """
        入力フレーム数が範囲を超えていた場合最適化する
        """

        optimized_frame = frame % (self.row_len * self.column_len)

        if not frame == optimized_frame:
            print('optimize frame : {} -> {}'.format(str(frame), str(optimized_frame)))

        return optimized_frame

    # ===============================================
    def __get_current_tear_frame(self):

        current_frame = 0

        if not self.uv_list:
            return current_frame

        uv_avarage = self.__get_uv_avarage(self.uv_list)
        row_column = self.__get_current_row_column(uv_avarage)

        current_frame = self.column_len * row_column[0] + row_column[1]

        return current_frame

    # ===============================================
    def __get_uv_avarage(self, uv_list):

        uv_avarage = [0.0, 0.0]
        uv_count = 0

        if not uv_list:
            return uv_avarage

        for uv_item in uv_list:
            this_uv = cmds.polyEditUV(uv_item, q=True)
            uv_avarage[0] += this_uv[0]
            uv_avarage[1] += this_uv[1]
            uv_count += 1

        uv_avarage[0] = uv_avarage[0] / uv_count
        uv_avarage[1] = uv_avarage[1] / uv_count

        return uv_avarage

    # ===============================================
    def __get_current_row_column(self, uv_avarage):

        if not uv_avarage:
            return [0, 0]

        column_num = int(uv_avarage[0] / (1.0 / self.column_len))
        row_num = int((1 - uv_avarage[1]) / (1.0 / self.row_len))

        return [row_num, column_num]

