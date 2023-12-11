# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import object
except Exception:
    pass

import re
import math

import maya.cmds as cmds
import maya.OpenMaya as om


# ++++++++++++++++++++++++++++++++++++++++++++++++++
class BlendNormal(object):

    # ========================================
    def __init__(self):

        self.edge_vertex_dict = {}

        # EdgeChainインスタンスのリスト
        self.edge_chain_list = []

    # ========================================
    def execute(self, blend_value=1):
        """
        法線ブレンドの実行関数

        blend_value: 元の法線からのブレンド値
        """

        if blend_value <= 0 or blend_value > 1:
            return

        # 選択からエッジ単位の頂点の辞書を作成
        self.__create_edge_vertex_dict()

        if not self.edge_vertex_dict:
            return

        # ひと繋がりのエッジグループのリストを作成
        self.__create_edge_chain_list()

        if not self.edge_chain_list:
            return

        for edge_chain in self.edge_chain_list:

            if not edge_chain.is_correct:
                continue

            edge_chain.blend_normals(blend_value)

    # ========================================
    def __create_edge_vertex_dict(self):
        """
        エッジ単位の頂点の辞書を取得

        self.edge_vertex_dict: {edge1: [vertex1, vertex2], edge2:...}
        """

        edge_list = self.__get_selection_edge_list()

        if not edge_list:
            om.MGlobal.displayError("エッジ選択モードで選択してください。")
            return

        for edge in edge_list:

            this_edge_vertices = cmds.ls(
                cmds.polyListComponentConversion(edge, tv=True),
                fl=True,
                l=True)

            self.edge_vertex_dict[edge] = this_edge_vertices

    # ========================================
    def __get_selection_edge_list(self):
        """
        選択しているエッジのリストを取得
        """

        edge_list = []

        if cmds.ls(sl=True, l=True, o=True, typ="transform"):
            return

        # ------------------------------
        # 選択されたエッジのリスト作成
        select_list = cmds.ls(sl=True, fl=True, l=True)

        for select in select_list:
            if ".e" in select:
                edge_list.append(select)

        return edge_list

    # ========================================
    def __create_edge_chain_list(self):
        """
        ひと繋がりのエッジグループのリストを作成
        """

        edge_group_index = 0

        for search_edge_item in list(self.edge_vertex_dict.items()):

            # ------------------------------
            # エッジグループに追加されていないかの判定
            is_chain = False
            for this_chain in self.edge_chain_list:
                if search_edge_item[0] in list(this_chain.edge_vertex_dict.keys()):
                    is_chain = True

            if is_chain:
                continue

            # ------------------------------
            # ひと繋がりのエッジを判定し、EdgeChainのインスタンスを作成
            chain_edge_dict = self.__get_edge_chain_dict(search_edge_item, {})

            searched_edge_chain = EdgeChain()
            searched_edge_chain.initialize(edge_group_index, chain_edge_dict)

            self.edge_chain_list.append(searched_edge_chain)

            edge_group_index += 1

    # ========================================
    def __get_edge_chain_dict(self, search_edge_item, chain_edge_dict):
        """
        指定エッジからの接続エッジをすべて調べて辞書にする
        """

        search_edge = search_edge_item[0]
        search_edge_vertex = search_edge_item[1]

        chain_edge_dict[search_edge] = search_edge_vertex

        for search_vertex in self.edge_vertex_dict[search_edge]:

            for this_edge in list(self.edge_vertex_dict.keys()):

                if this_edge == search_edge:
                    continue

                if this_edge in list(chain_edge_dict.keys()):
                    continue

                this_edge_vertex_list = \
                    self.edge_vertex_dict[this_edge]

                if search_vertex in this_edge_vertex_list:

                    self.__get_edge_chain_dict(
                        (this_edge, this_edge_vertex_list),
                        chain_edge_dict
                    )

        return chain_edge_dict


# ++++++++++++++++++++++++++++++++++++++++++++++++++
class EdgeChain(object):
    """
    ひと繋がりのエッジのクラス
    """

    # ========================================
    def __init__(self):

        self.index = None

        self.edge_vertex_dict = {}

        self.src_vertex_info_list = []
        self.dst_vertex_info_list = []

        self.is_correct = False
        self.is_choose_front_normal = None

    # ========================================
    def initialize(self, index, edge_vertex_dict):
        """
        EdgeChainクラスに必要な情報を作成

        index: ひと繋がりのエッジの番号
        edge_vertex_dict: エッジごとの頂点の辞書
        """

        self.index = index
        self.edge_vertex_dict = edge_vertex_dict

        if len(list(self.edge_vertex_dict.keys())) < 2:
            # ここにグループ内のエッジが2箇所未満のときの処理
            om.MGlobal.displayError("エッジが２つ以上繋がっていません: {0}".format(
                list(self.edge_vertex_dict.keys())[0]))
            return

        # ------------------------------
        vertex_type_dict = self.__get_vertex_dict()

        for vertex_type_item in list(vertex_type_dict.items()):

            this_vertex_info = VertexInfo()
            this_vertex_info.initialize(vertex_type_item[0])

            if vertex_type_item[1] == "src":
                self.src_vertex_info_list.append(this_vertex_info)

            if vertex_type_item[1] == "dst":
                self.dst_vertex_info_list.append(this_vertex_info)

        if len(self.src_vertex_info_list) < 2:
            # ここに末端が2箇所未満のときの処理
            om.MGlobal.displayError("選択したエッジグループに端の頂点がありません: {}".format(
                cmds.ls(list(self.edge_vertex_dict.keys()), fl=False, l=True)))
            return

        if len(self.src_vertex_info_list) > 2:
            # ここに末端が2箇所より多いのときの処理
            # 3箇所以上だと法線の方向計算がうまくいかないため、処理対象外に
            om.MGlobal.displayError("選択したエッジグループの端の頂点が3箇所以上です: {}".format(
                cmds.ls(list(self.edge_vertex_dict.keys()), fl=False, l=True)))
            return

        # ------------------------------
        for src_vertex_info in self.src_vertex_info_list:

            # 末端頂点がハードエッジの判定、スムース部分のみの法線取得
            self.src_normal_dict = \
                self.__set_src_vertex_normal(src_vertex_info)

            if not src_vertex_info.src_normal:
                # 端の頂点法線がハードエッジだった場合の処理
                om.MGlobal.displayError("選択したエッジの端点がハードエッジです: {}".format(
                    src_vertex_info.name))
                return

        # ひと繋がりのエッジに含まれる全ての頂点情報に、ブレンド元頂点からの距離を設定
        for src_vertex_info in self.src_vertex_info_list:

            add_length = \
                self.__create_edge_distance(src_vertex_info.name, 0, [], [])

            if add_length is None:
                # エッジがループしている場合の処理
                om.MGlobal.displayError("選択したエッジがループしています: {}".format(
                    list(self.edge_vertex_dict.keys())))
                return

        self.is_correct = True

    # ========================================
    def __get_vertex_dict(self):
        """
        頂点のタイプを取得する

        vertex: 'src' :: 末端頂点
        vertex: 'dst' :: 末端頂点でない
        """

        vertex_type_dict = {}

        # 辞書のエッジ頂点を検索しやすいリストに変換
        edge_vertex_list = \
            [v for ev in list(self.edge_vertex_dict.values()) for v in ev]

        for edge in list(self.edge_vertex_dict.keys()):

            for edge_vertex in self.edge_vertex_dict[edge]:

                if edge_vertex_list.count(edge_vertex) <= 1:

                    # 重複する頂点がなかったら、末端頂点に設定
                    vertex_type_dict[edge_vertex] = "src"
                    continue

                if edge_vertex in list(vertex_type_dict.keys()):
                    continue

                # 重複する頂点があったら、接続頂点に設定
                vertex_type_dict[edge_vertex] = "dst"

        return vertex_type_dict

    # ========================================
    def __set_src_vertex_normal(self, vertex_info):
        """
        末端頂点がハードエッジでなければ、ブレンド元のノーマルを作成
        """

        target_edge = None

        for edge in list(self.edge_vertex_dict.keys()):
            if vertex_info.name in self.edge_vertex_dict[edge]:
                target_edge = edge
                break

        if not target_edge:
            return

        face_list = cmds.ls(
            cmds.polyListComponentConversion(target_edge, fe=True, tf=True),
            fl=True,
            l=True)

        # ------------------------------
        vtf_normal_list = []

        for face in face_list:

            this_face_index = re.search(r'.f\[(\d+)\]', face).group(1)

            this_vtf = "{}.vtxFace[{}][{}]".format(
                vertex_info.name.split(".vtx")[0],
                vertex_info.index,
                this_face_index)

            if this_vtf in list(vertex_info.normal_dict.keys()):
                vtf_normal_list.append(vertex_info.normal_dict[this_vtf])

        for vtf_normal in vtf_normal_list:
            if vtf_normal_list[0] != vtf_normal:
                return

        vertex_info.src_normal = vtf_normal_list[0]

    # ========================================
    def __create_edge_distance(self, target_vertex, add_length, checked_vertex_list, checked_edge_list, src_vertex=None):
        """
        全てのブレンド対象の頂点の、ブレンド元の頂点からのエッジの長さを計算

        target_vertex: ブレンド元の頂点、再帰処理時は次の検索用頂点
        add_length: 追加されたエッジの長さ、初回計算時は0を指定する
        checked_vertex_list: チェックし終わった頂点のリスト
        checked_edge_list: チェックし終わったエッジのリスト
        src_vertex: 距離検索元の頂点、デフォルトでは初回計算時のtarget_vertexが入る
        """

        if add_length == 0:
            src_vertex = target_vertex

        # ------------------------------
        # 頂点を共有するエッジのリストを検索
        this_edge_list = []

        for edge, vertex_list in list(self.edge_vertex_dict.items()):
            if target_vertex in vertex_list:
                this_edge_list.append(edge)

        # ------------------------------
        # エッジの回数分距離計算の再起処理を行う
        for this_edge in this_edge_list:

            # ------------------------------
            # すでに距離が計算されていたら次のエッジの計算、あったら処理済みに追加
            if this_edge in checked_edge_list:
                continue

            checked_edge_list.append(this_edge)

            # ------------------------------
            # エッジのもう一端の頂点を検索
            this_vertex_list = self.edge_vertex_dict[this_edge]

            pair_vertex = \
                [v for v in this_vertex_list if target_vertex != v][0]

            # ------------------------------
            # すでに指定頂点の距離が計算されていたらループしているためreturn
            if pair_vertex in checked_vertex_list:
                return

            checked_vertex_list.append(pair_vertex)

            # ------------------------------
            # 距離計算元頂点と距離計算先頂点の位置情報を設定
            vertex_pos = None
            pair_vertex_pos = None

            # 法線ブレンド先の頂点からチェック
            for search_dst_vertex_info in self.dst_vertex_info_list:

                # 元頂点の位置設定
                if search_dst_vertex_info.name == target_vertex:
                    vertex_pos = search_dst_vertex_info.position_dict

                # 先頂点の位置設定
                elif search_dst_vertex_info.name == pair_vertex:
                    pair_vertex_pos = search_dst_vertex_info.position_dict

            # 先頂点がブレンド先の頂点でない場合
            if not pair_vertex_pos:
                continue

            # 元頂点が見つかっていなければ、法線ブレンド元の頂点からチェック
            if not vertex_pos:

                for search_src_vertex_info in self.src_vertex_info_list:

                    if search_src_vertex_info.name == target_vertex:
                        vertex_pos = search_src_vertex_info.position_dict

            # ------------------------------
            # エッジの長さ計算
            this_distance = math.sqrt(
                (vertex_pos['x'] - pair_vertex_pos['x']) ** 2 +
                (vertex_pos['y'] - pair_vertex_pos['y']) ** 2 +
                (vertex_pos['z'] - pair_vertex_pos['z']) ** 2)

            add_length += this_distance

            # ------------------------------
            # ブレンド先の頂点情報に、ブレンド元頂点からのエッジをたどった距離を設定
            for set_vertex_info in self.dst_vertex_info_list:

                if set_vertex_info.name == pair_vertex:
                    set_vertex_info.to_src_distance_dict[src_vertex] = \
                        add_length
                    break

            # ------------------------------
            # エッジ距離計算先の頂点からの頂点距離の計算を繰り返し足していく
            add_length = self.__create_edge_distance(
                pair_vertex,
                add_length,
                checked_vertex_list,
                checked_edge_list,
                src_vertex)

            if add_length is None:
                return

        return add_length

    # ========================================
    def blend_normals(self, blend_value):
        """
        末端頂点のノーマル値をブレンドして接続頂点に転写

        blend_value: 0~1の元法線からのブレンド値
        """

        locked_normal_count = 0

        for dst_vertex_info in self.dst_vertex_info_list:

            # 頂点法線がロックされていなかったら無視
            if not dst_vertex_info.is_locked_normal:
                locked_normal_count += 1
                continue

            blend_normal_dict = \
                self.__get_blend_normal_dict(dst_vertex_info, blend_value)

            if not blend_normal_dict:
                cmds.warning("ノーマル情報が作成できませんでした: {}".format(
                    dst_vertex_info.name))
                continue

            # 法線転写
            # 最終的な転写法線がハードエッジだったら無視
            if not self.__is_smooth_normal(blend_normal_dict):
                continue

            else:
                paste_normal = \
                    self.__get_normalize_noramal(list(blend_normal_dict.values())[0])

                cmds.polyNormalPerVertex(
                    dst_vertex_info.name,
                    e=True,
                    xyz=paste_normal)

        if locked_normal_count == len(self.dst_vertex_info_list):
            om.MGlobal.displayError("エッジグループの法線が１つもロックされていません: \n{}".format(
                self.dst_vertex_info_list))

    # ========================================
    def __get_blend_normal_dict(self, vertex_info, blend_value):
        """
        ブレンドされた接続頂点のノーマル情報を作成

        vertex_info: ノーマル転写対象の頂点情報
        blend_value: 0~1の元法線からのブレンド値
        """

        # ------------------------------
        # 法線のブレンド
        blend_src_normal = [0] * 3
        reverse_blend_src_normal = [0] * 3

        add_distance = 0
        blend_count = 0

        # 元法線と対象の法線のブレンド値を計算
        for src_vertex_info in self.src_vertex_info_list:

            this_src_normal = src_vertex_info.src_normal

            src_distance = \
                vertex_info.to_src_distance_dict[src_vertex_info.name]

            add_distance += src_distance

            # 初回の計算
            if blend_count == 0:
                blend_src_normal = this_src_normal
                blend_count += 1
                continue

            # 初回以降の計算
            normal_blend_rate = \
                src_distance / add_distance

            reverse_blend_src_normal = self.__get_slerp_normal(
                this_src_normal,
                blend_src_normal,
                normal_blend_rate,
                is_reverse=True
            )

            blend_src_normal = self.__get_slerp_normal(
                this_src_normal,
                blend_src_normal,
                normal_blend_rate,
                is_reverse=False
            )

            blend_count += 1

        if blend_src_normal == [0] * 3:
            return
        if reverse_blend_src_normal == [0] * 3:
            return

        # ------------------------------
        # フェース法線の平均とブレンドした法線の向き判定(初回のみ)
        if self.is_choose_front_normal is None:
            self.is_choose_front_normal = self.__is_front_vertex_normal(
                blend_src_normal,
                reverse_blend_src_normal,
                vertex_info)

        if self.is_choose_front_normal:
            blend_normal = blend_src_normal
        else:
            blend_normal = reverse_blend_src_normal

        # ------------------------------
        # 元の法線とのブレンド(ハードエッジにも対応しているが未使用)
        dst_normal_dict = vertex_info.normal_dict
        blend_normal_dict = {}

        for this_dst_vtf, this_dst_normal in list(dst_normal_dict.items()):

            this_blended_normal = self.__get_slerp_normal(
                this_dst_normal,
                blend_normal,
                blend_value,
                is_reverse=False
            )

            blend_normal_dict[this_dst_vtf] = this_blended_normal

        if not blend_normal_dict:
            return

        return blend_normal_dict

    # ========================================
    def __get_slerp_normal(self, nml_s, nml_e, interpolation, is_reverse=False):
        """
        球面線形補間で回転した法線の値を取得する関数

        nml_s: 回転元の法線
        nml_e: 回転先の法線
        interpolation: 補間値
        is_reverse: 逆方向に回転した法線を取得するか

        return: 補間した法線
        """

        nml_s = self.__get_normalize_noramal(nml_s)
        nml_e = self.__get_normalize_noramal(nml_e)

        dot_value = self.__dot(nml_s, nml_e)

        if dot_value >= 1:
            return nml_e

        angle = math.acos(dot_value)
        # 度数法への変換 -> angle * 180 / math.pi

        sin_angle = math.sin(angle)

        slerp_normal = [0] * 3

        # ------------------------------
        # 正の方向へのブレンド
        if not is_reverse:

            sin_start = math.sin(angle * (1 - interpolation))
            sin_end = math.sin(angle * interpolation)

            slerp_normal = [
                (sin_start * nml_s[0] + sin_end * nml_e[0]) / sin_angle,
                (sin_start * nml_s[1] + sin_end * nml_e[1]) / sin_angle,
                (sin_start * nml_s[2] + sin_end * nml_e[2]) / sin_angle
            ]

        # ------------------------------
        # 反転方向へのブレンド
        else:
            sin_average = math.sin(angle * 0.5)

            rev_aver_nml = [
                -(sin_average * nml_s[0] + sin_average * nml_e[0]) / sin_angle,
                -(sin_average * nml_s[1] + sin_average * nml_e[1]) / sin_angle,
                -(sin_average * nml_s[2] + sin_average * nml_e[2]) / sin_angle
            ]

            # ブレンド空間が半分になったため、ブレンド値を倍に
            reversed_interpolation = interpolation * 2

            if interpolation < 0.5:
                # ブレンド値0.5未満用の角度計算
                first_half_dot_value = self.__dot(nml_s, rev_aver_nml)
                first_half_angle = math.acos(first_half_dot_value)
                first_half_sin_angle = math.sin(first_half_angle)

                # ブレンド空間の調整(0.5以下の値*2は1~0の空間に収まる)
                sin_start = \
                    math.sin(first_half_angle * (1 - reversed_interpolation))
                sin_end = \
                    math.sin(first_half_angle * (reversed_interpolation))

                # 回転元ノーマルから反転した中心ノーマルをブレンド
                slerp_normal = [
                    (sin_start * nml_s[0] + sin_end * rev_aver_nml[0]) / first_half_sin_angle,
                    (sin_start * nml_s[1] + sin_end * rev_aver_nml[1]) / first_half_sin_angle,
                    (sin_start * nml_s[2] + sin_end * rev_aver_nml[2]) / first_half_sin_angle
                ]

            elif interpolation >= 0.5:
                # ブレンド値0.5以上用の角度計算
                second_half_dot_value = self.__dot(rev_aver_nml, nml_e)
                second_half_angle = math.acos(second_half_dot_value)
                second_half_sin_angle = math.sin(second_half_angle)

                # ブレンド空間の調整(0.5より大きい値*2は2~1の空間に収まる)
                sin_start = \
                    math.sin(second_half_angle * (2 - reversed_interpolation))
                sin_end = \
                    math.sin(second_half_angle * (reversed_interpolation - 1))

                # 反転した中心ノーマルから回転先ノーマルをブレンドする
                slerp_normal = [
                    (sin_start * rev_aver_nml[0] + sin_end * nml_e[0]) / second_half_sin_angle,
                    (sin_start * rev_aver_nml[1] + sin_end * nml_e[1]) / second_half_sin_angle,
                    (sin_start * rev_aver_nml[2] + sin_end * nml_e[2]) / second_half_sin_angle
                ]

        # ------------------------------
        slerp_normal = self.__get_normalize_noramal(slerp_normal)

        return slerp_normal

    # ========================================
    def __is_front_vertex_normal(self, normal, reverse_normal, vertex_info):
        """
        正と逆方向の２つの法線のどちらが選択頂点を共有するフェースの正面方向かを判定する

        normal: 正の方向の法線
        reverse_normal: 逆方向の法線
        vertex_info: 向きを判定する頂点情報

        return: 正であればTrue、逆であればFalse
        """

        # ------------------------------
        # 指定の頂点を共有するフェースのリスト取得
        face_list = cmds.ls(
            cmds.polyListComponentConversion(
                vertex_info.name,
                fv=True,
                tf=True),
            fl=True,
            l=True)

        # ------------------------------
        # 取得したフェース法線の平均を作成
        add_normal = [0] * 3

        for face in face_list:
            this_normal = cmds.polyInfo(face, fn=True)[0].split(' ')

            this_normal = [
                float(this_normal[-3]),
                float(this_normal[-2]),
                float(this_normal[-1])
            ]

            add_normal = [an+tn for an, tn in zip(add_normal, this_normal)]

        face_count = len(face_list)
        average_face_normal = [an/face_count for an in add_normal]

        # ------------------------------
        # フェース法線と指定法線の内積値で正しい方向かを判定
        dot_value = self.__dot(average_face_normal, normal)
        reverse_dot_value = self.__dot(average_face_normal, reverse_normal)

        if dot_value < 0:
            return False

        elif reverse_dot_value > dot_value:
            return False

        return True

    # ========================================
    def __is_smooth_normal(self, normal_dict):
        """
        頂点フェースのノーマル情報から、スムースエッジかどうか判定

        normal_dict: 頂点フェースごとのノーマル情報

        return: 頂点ノーマルがスムースエッジならTrue
        """

        normal_value_list = list(normal_dict.values())
        vertex_face_count = len(list(normal_dict.keys()))

        if normal_value_list.count(normal_value_list[0]) == vertex_face_count:
            return True

        return False

    # ========================================
    def __get_normalize_noramal(self, normal):
        """
        正規化した法線を計算

        normal: 正規化したい法線

        return: 正規化された法線
        """

        n = normal

        if len(n) == 3:
            length = (n[0]*n[0] + n[1]*n[1] + n[2]*n[2]) ** 0.5

            if not length:
                return n

            return [n[0] / length, n[1] / length, n[2] / length]

        else:
            return

    # ========================================
    def __dot(self, vec_a, vec_b):
        """
        ２つのベクトルの内積を計算

        vec_a: ベクトルa
        vec_b: ベクトルb

        return: ベクトルaとベクトルbの内積値
        """

        if len(vec_a) != len(vec_b):
            return

        added_value = 0

        for a, b in zip(vec_a, vec_b):
            added_value += a * b

        return added_value


# ++++++++++++++++++++++++++++++++++++++++++++++++++
class VertexInfo(object):
    """
    単一頂点の情報クラス
    """

    # ========================================
    def __init__(self):

        self.name = None
        self.index = None

        self.position_dict = {}

        self.vertex_face_list = []
        self.normal_dict = {}
        self.is_locked_normal = None

        self.src_normal = []
        self.to_src_distance_dict = {}

    # ========================================
    def initialize(self, vertex):
        """
        VertexInfoクラスで必要な情報を作成します

        vertex: 頂点名
        """

        self.name = vertex
        self.index = re.search(r'.vtx\[(\d+)\]', vertex).group(1)

        self.__create_position_dict()

        self.__create_vertex_face_list()

        self.__create_normal_dict()

        self.__create_is_locked_normal()

    # ========================================
    def __create_position_dict(self):
        """
        頂点の位置情報を取得
        """

        position_list = cmds.pointPosition(self.name, w=True)

        self.position_dict["x"] = position_list[0]
        self.position_dict["y"] = position_list[1]
        self.position_dict["z"] = position_list[2]

    # ========================================
    def __create_vertex_face_list(self):
        """
        頂点を共有する頂点フェースのリストを取得
        """

        self.vertex_face_list = cmds.ls(
            cmds.polyListComponentConversion(self.name, fv=True, tvf=True),
            fl=True,
            l=True)

    # ========================================
    def __create_normal_dict(self):
        """
        頂点の法線情報を取得
        """

        for vertex_face in self.vertex_face_list:

            this_vertex_face_normal = \
                cmds.polyNormalPerVertex(vertex_face, q=True, xyz=True)

            self.normal_dict[vertex_face] = this_vertex_face_normal

    # ========================================
    def __create_is_locked_normal(self):
        """
        頂点法線がロックされているかを判定
        """

        for vertex_face in self.vertex_face_list:

            is_locked = \
                cmds.polyNormalPerVertex(vertex_face, q=True, fn=True)[0]

            if not is_locked:
                break

        self.is_locked_normal = is_locked
