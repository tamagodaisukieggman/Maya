# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import math

import maya.cmds as cmds
import maya.mel as mel


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GlpArrangeVtxOrder:

    # ==================================================
    def __init__(self):

        # meshの方向判定用ベクトル
        self.foward_direction = [0, 0, 1]

        # meshの結合方向=面ごとに頂点番号が増えていく向き（初期値は手前から奥
        self.mesh_unite_direction = [0, 0, -1]
        # meshの流れ=面の中で頂点番号が増えていく向き（初期値は上から下
        self.mesh_direction = [0, -1, 0]

        # 面のつながり判定用の内積の制限値
        self.tri_mesh_direction_div_limit = 0.3
        self.quad_mesh_direction_div_limit = 0.5
        self.normal_div_limit = 0.85

    # ==================================================
    def get_face_chain_list(self, target_face_list):
        """メッシュの向きに一列ずつ切り取った面のリストを返す
        """

        mesh_direction_sort_list = self.__get_ordered_face_dict_list(target_face_list, self.mesh_direction)
        result_chain_list = []
        used_face_list = []

        for face_dict in mesh_direction_sort_list:

            if face_dict['face'] in used_face_list:
                continue

            this_chain_raw = self.get_face_chain(face_dict['face'])
            this_chain = []

            for face in this_chain_raw:
                if face not in used_face_list:
                    this_chain.append(face)

            result_chain_list.append(this_chain)
            used_face_list.extend(this_chain)

        return result_chain_list

    # ==================================================
    def get_face_chain(self, first_face):
        """ある面からメッシュの向きに一列の面のリストを返す
        """

        return self.get_next_chain(first_face, [first_face], self.mesh_direction)

    # ==================================================
    def get_next_chain(self, current_face, face_list, prev_direction):
        """ある面から再帰的につながっている面を探していく
        """

        current_cg = self.__get_face_cg(current_face)
        current_face_normal = self.__get_face_normal(current_face)

        to_edge = cmds.polyListComponentConversion(current_face, te=True)
        to_face = cmds.ls(cmds.polyListComponentConversion(to_edge, tf=True), l=True, fl=True)

        neighbor_face_list = [face for face in to_face if face not in face_list]

        top_score = 0.0
        next_face = None

        for neighbor_face in neighbor_face_list:

            score = self.__get_chain_score(current_face, neighbor_face, prev_direction)

            if score == 0.0:
                continue

            if score > top_score:
                top_score = score
                next_face = neighbor_face

        next_face_list = []
        if next_face:
            next_face_list = [next_face]

        if not next_face_list:
            return face_list
        else:
            result_face_list = []
            for face in next_face_list:
                this_cg = self.__get_face_cg(face)
                direction = [this_cg[0] - current_cg[0], this_cg[1] - current_cg[1], this_cg[2] - current_cg[2]]
                direction = self.__normalize_vector(direction)
                face_list.append(face)
                result_face_list.extend(self.get_next_chain(face, face_list, direction))

            return result_face_list

    # ==================================================
    def separate_mesh(self, target_mesh, face_chain_list):
        """メッシュをface_chain_listを元に別々のメッシュに分割
        """

        if not cmds.objExists(target_mesh):
            return

        if not face_chain_list:
            return

        for face_chain in face_chain_list:
            cmds.polyChipOff(face_chain, dup=False)

        res = cmds.polySeparate(target_mesh)
        separete_mesh_list = res[:-1]
        cmds.parent(separete_mesh_list, w=True)
        cmds.delete(separete_mesh_list, ch=True)

        return separete_mesh_list

    # ==================================================
    def reorder_vtx(self, mesh_list):
        """各メッシュの頂点番号を再振り分け
        分割された一列ずつのメッシュリストを元メッシュの方向に頂点番号が増えるようにする
        """

        if not mesh_list:
            return

        for mesh in mesh_list:

            if not cmds.objExists(mesh):
                continue

            # 元メッシュ方向に面を見た時一番最初の面の頂点番号を修正する
            face_list = cmds.ls(cmds.polyListComponentConversion(mesh, tf=True), l=True, fl=True)
            ordered_face_dict_list = self.__get_ordered_face_dict_list(face_list, self.mesh_direction)
            top_face = ordered_face_dict_list[0]['face']

            vtx_list = cmds.ls(cmds.polyListComponentConversion(top_face, tv=True), l=True, fl=True)
            sel_list = self.__get_reorder_sel_list(vtx_list, self.__get_face_cg(top_face))

            if not sel_list:
                continue

            mel.eval('meshReorder {} {} {}'.format(sel_list[0], sel_list[1], sel_list[2]))

    # ==================================================
    def unite_mesh(self, mesh_list, order_source='uv'):
        """メッシュリストをself.mesh_unite_directionの方向にorder_sourceの近い順で結合する
        メッシュのUVが一つながりならorder_sourceはuv、そうでなければposを使う想定
        100%上手くいくことはなさそうなので、手動の選択順での結合も必要になるはず
        """

        if not mesh_list:
            return

        ref_face_list = []
        for mesh in mesh_list:

            if not cmds.objExists(mesh):
                continue

            face_list = cmds.ls(cmds.polyListComponentConversion(mesh, tf=True), l=True, fl=True)
            # メッシュの流れ的に一番最後の面を参考面に設定
            sort_direction = [self.mesh_direction[0], self.mesh_direction[1], self.mesh_direction[2]]
            ordered_face_dict_list = self.__get_ordered_face_dict_list(face_list, sort_direction)
            ref_face_list.append(ordered_face_dict_list[-1]['face'])

        # 左右の面
        right_side_face_list = []
        left_side_face_list = []

        center_pos_sum = [0, 0, 0]
        mesh_count = 0
        for mesh in mesh_list:
            mesh_cg = self.__get_mesh_cg(mesh)
            center_pos_sum[0] += mesh_cg[0]
            center_pos_sum[1] += mesh_cg[1]
            center_pos_sum[2] += mesh_cg[2]
            mesh_count += 1

        center_pos = [
            center_pos_sum[0] / mesh_count,
            center_pos_sum[1] / mesh_count,
            center_pos_sum[2] / mesh_count]

        for face in ref_face_list:
            face_pos = self.__get_face_cg(face)
            face_drection = [
                face_pos[0] - center_pos[0],
                face_pos[1] - center_pos[1],
                face_pos[2] - center_pos[2]]

            foward_cross = self.__get_cross_vector(self.foward_direction, face_drection)
            if self.__get_dot_value(foward_cross, self.mesh_direction) >= 0:
                right_side_face_list.append(face)
            else:
                left_side_face_list.append(face)

        first_right_face = None
        first_left_face = None
        if right_side_face_list:
            first_right_face = self.__get_ordered_face_dict_list(right_side_face_list, self.mesh_unite_direction)[0]['face']
        if left_side_face_list:
            first_left_face = self.__get_ordered_face_dict_list(left_side_face_list, self.mesh_unite_direction)[0]['face']

        ordered_right_side_face_list = self.__get_distance_ordered_face_list(
            right_side_face_list, self.__get_face_cg(first_right_face, order_source), order_source
        )
        ordered_left_side_face_list = self.__get_distance_ordered_face_list(
            left_side_face_list, self.__get_face_cg(first_left_face, order_source), order_source
        )

        top_face_unite_order_list = ordered_right_side_face_list + ordered_left_side_face_list
        unite_mesh_list = [face.split('.')[0] for face in top_face_unite_order_list]

        result = cmds.polyUnite(unite_mesh_list, op=True)

        if not result:
            return

        unite_mesh = result[0]
        vtx_list = cmds.ls(cmds.polyListComponentConversion(unite_mesh, tv=True), l=True, fl=True)
        cmds.polyMergeVertex(vtx_list, d=0.0001)

        uv_list = cmds.ls(cmds.polyListComponentConversion(unite_mesh, tuv=True), l=True, fl=True)
        cmds.polyMergeUV(uv_list, d=0.0001)

        cmds.delete(unite_mesh, ch=True)

        return unite_mesh

    # ==================================================
    def __get_chain_score(self, current_face, neighbor_face, prev_direction):
        """current_faceから見たneighbor_faceの連続性をスコアリング
        面の重心を結ぶ流れがそろっているほど、面法線の向きが一致しているほど高スコアにしている
        """

        # 重みづけの割合（あくまで感覚的な値です）
        # 三角面の方が重心を結ぶ流れが乱れるので向きの比重を下げている
        current_tri_rate = {'normal': 0.8, 'direction': 0.2}
        current_quad_rate = {'normal': 0.5, 'direction': 0.5}
        score_rate = {}

        # self.mesh_directionとの内積値がこれを下回るとアウト
        mesh_direction_limit = 0.0

        current_face_vtx = cmds.ls(cmds.polyListComponentConversion(current_face, tv=True), l=True, fl=True)
        if not current_face_vtx:
            return 0.0
        elif len(current_face_vtx) == 3:
            score_rate = current_tri_rate
            mesh_direction_limit = self.tri_mesh_direction_div_limit
        elif len(current_face_vtx) == 4:
            score_rate = current_quad_rate
            mesh_direction_limit = self.quad_mesh_direction_div_limit
        else:
            return 0.0

        current_cg = self.__get_face_cg(current_face)
        current_face_normal = self.__get_face_normal(current_face)

        neighbor_cg = self.__get_face_cg(neighbor_face)
        neighbor_face_normal = self.__get_face_normal(neighbor_face)

        neighbour_direction = [neighbor_cg[0] - current_cg[0], neighbor_cg[1] - current_cg[1], neighbor_cg[2] - current_cg[2]]
        neighbour_direction = self.__normalize_vector(neighbour_direction)

        # meshの流れに反していたらアウト
        if self.__get_dot_value(self.mesh_direction, neighbour_direction) < mesh_direction_limit:
            return 0.0

        # 法線の差が許容値を超えていたらアウト
        if self.__get_dot_value(current_face_normal, neighbor_face_normal) < self.normal_div_limit:
            return 0.0

        normal_score = self.__get_dot_value(current_face_normal, neighbor_face_normal) * score_rate['normal']
        direction_score = self.__get_dot_value(prev_direction, neighbour_direction) * score_rate['direction']

        return normal_score + direction_score

    # ==================================================
    def __get_face_cg(self, face, source_type='pos'):
        """面の重心（位置かUV）
        """

        if not face or not cmds.objExists(face):
            return
        to_vtx = cmds.ls(cmds.polyListComponentConversion(face, tv=True), l=True, fl=True)

        if not to_vtx:
            return

        if source_type == 'pos':
            sum_pos = [0, 0, 0]
            count = 0
            for vtx in to_vtx:
                pos = cmds.xform(vtx, q=True, t=True, ws=True)
                sum_pos[0] += pos[0]
                sum_pos[1] += pos[1]
                sum_pos[2] += pos[2]
                count += 1
            return [(sum_pos[0] / count), (sum_pos[1] / count), (sum_pos[2] / count)]

        elif source_type == 'uv':
            sum_uv = [0, 0]
            count = 0
            for vtx in to_vtx:
                uv = cmds.polyEditUV(cmds.polyListComponentConversion(vtx, tuv=True)[0], q=True)
                sum_uv[0] += uv[0]
                sum_uv[1] += uv[1]
                count += 1
            return [(sum_uv[0] / count), (sum_uv[1] / count)] 

    # ==================================================
    def __get_mesh_cg(self, mesh, source_type='pos'):
        """メッシュの重心（位置かUV）
        """

        if not mesh or not cmds.objExists(mesh):
            return
        to_face = cmds.ls(cmds.polyListComponentConversion(mesh, tf=True), l=True, fl=True)

        if not to_face:
            return

        if source_type == 'pos':
            sum_pos = [0, 0, 0]
            count = 0
            for face in to_face:
                pos = self.__get_face_cg(face, source_type)
                sum_pos[0] += pos[0]
                sum_pos[1] += pos[1]
                sum_pos[2] += pos[2]
                count += 1
            return [(sum_pos[0] / count), (sum_pos[1] / count), (sum_pos[2] / count)]

        elif source_type == 'uv':
            sum_uv = [0, 0]
            count = 0
            for face in to_face:
                uv = self.__get_face_cg(face, source_type)
                sum_uv[0] += uv[0]
                sum_uv[1] += uv[1]
                count += 1
            return [(sum_uv[0] / count), (sum_uv[1] / count)] 

    # ==================================================
    def __get_reorder_sel_list(self, vtx_list, face_cg):
        """mel.eval('meshReorder {} {} {}')に渡すlistを作成
        """

        if len(vtx_list) < 3:
            return

        base_point = cmds.xform(vtx_list[0], q=True, t=True, ws=True)
        base_vector = self.__normalize_vector([base_point[0] - face_cg[0], base_point[1] - face_cg[1], base_point[2] - face_cg[2]])

        dot_info_dict_list = []
        for vtx in vtx_list:
            vtx_point = cmds.xform(vtx, q=True, t=True, ws=True)
            from_cg_vector = self.__normalize_vector([vtx_point[0] - face_cg[0], vtx_point[1] - face_cg[1], vtx_point[2] - face_cg[2]])
            dot_info_dict_list.append({'vtx': vtx, 'dot': self.__get_dot_value(base_vector, from_cg_vector)})

        result_list = []
        for dot_info_dict in sorted(dot_info_dict_list, key=lambda x: x['dot'], reverse=True):
            result_list.append(dot_info_dict['vtx'])

        return result_list

    # ==================================================
    def __get_face_normal(self, face):
        """面法線
        """

        if not cmds.objExists(face):
            return
        tmp = cmds.polyInfo(face, fn=True)[0].split(' ')

        # 得られる面法線が正規化されていない場合があるため、正規化して返す
        return self.__normalize_vector([float(tmp[-3]), float(tmp[-2]), float(tmp[-1])])

    # ==================================================
    def __get_dot_value(self, src_vector, dst_vector):
        """内積
        """

        dot_value = \
            src_vector[0] * dst_vector[0] + \
            src_vector[1] * dst_vector[1] + \
            src_vector[2] * dst_vector[2]

        return dot_value

    # ==================================================
    def __get_cross_vector(self, src_vector, dst_vector):
        """外積
        """

        cross_vector = [0] * 3

        cross_vector[0] = \
            src_vector[1] * dst_vector[2] - \
            src_vector[2] * dst_vector[1]

        cross_vector[1] = \
            src_vector[2] * dst_vector[0] - \
            src_vector[0] * dst_vector[2]

        cross_vector[2] = \
            src_vector[0] * dst_vector[1] - \
            src_vector[1] * dst_vector[0]

        cross_length = \
            cross_vector[0] * cross_vector[0] + \
            cross_vector[1] * cross_vector[1] + \
            cross_vector[2] * cross_vector[2]

        cross_vector[0] /= cross_length
        cross_vector[1] /= cross_length
        cross_vector[2] /= cross_length

        return cross_vector

    # ==================================================
    def __normalize_vector(self, vector):
        """正規化
        """

        raw_length = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

        if raw_length == 0:
            return vector

        return [vector[0] / raw_length, vector[1] / raw_length, vector[2] / raw_length]

    # ==================================================
    def __get_distance(self, point1, point2):
        """2点間の距離（次元問わず）
        """

        pow_sum = 0

        for elm1, elm2 in zip(point1, point2):
            pow_sum += pow(elm1 - elm2, 2)

        return math.sqrt(pow_sum)

    # ==================================================
    def __get_ordered_face_dict_list(self, target_face_list, order_source):
        """order_sourceの向きに面を重心位置で並べたdictのリストを返す
        """

        raw_face_dict_list = []

        for face in target_face_list:
            if not cmds.objExists(face):
                continue
            face = cmds.ls(face, l=True)[0]
            this_face_cg = self.__get_face_cg(face)
            raw_face_dict_list.append({'face': face, 'cg_x': this_face_cg[0], 'cg_y': this_face_cg[1], 'cg_z': this_face_cg[2]})

        sort_key = 'cg_y'
        should_reverse = True

        if not order_source[0] == 0:
            sort_key = 'cg_x'
            if order_source[0] < 0:
                should_reverse = True
            else:
                should_reverse = False
        elif not order_source[1] == 0:
            sort_key = 'cg_y'
            if order_source[1] < 0:
                should_reverse = True
            else:
                should_reverse = False
        elif not order_source[2] == 0:
            sort_key = 'cg_z'
            if order_source[2] < 0:
                should_reverse = True
            else:
                should_reverse = False

        return sorted(raw_face_dict_list, key=lambda x: x[sort_key], reverse=should_reverse)

    # ==================================================
    def __get_distance_ordered_face_list(self, target_face_list, ref_point, source_type='pos'):
        """面リストを基準点からの距離で並び替えたリストに変換
        """

        if not target_face_list:
            return []

        raw_dict_list = []
        for face in target_face_list:

            this_dict = {'face': face, 'distance': 0}
            face_cg = self.__get_face_cg(face, source_type=source_type)
            this_dict['distance'] = self.__get_distance(ref_point, face_cg)
            raw_dict_list.append(this_dict)

        reorder_dict_list = sorted(raw_dict_list, key=lambda x: x['distance'])
        return [reorder_dict['face'] for reorder_dict in reorder_dict_list]

