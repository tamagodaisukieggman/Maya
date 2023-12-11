# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

import math
import re
import itertools

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om


def main():

    this_main = GlpUVDistanceChecker()
    this_main.create_ui()


class GlpUVDistanceChecker(object):

    DEFAULT_MAX_DISTANCE = 0.0
    DEFAULT_MIN_DISTANCE = 0.005

    def __init__(self):

        self.tool_version = '18100401'
        self.tool_name = 'GallopUVdistanceChecker'
        self.window_name = self.tool_name + 'Win'

        self.idx_suffix_pattern = re.compile(r'\[(\d+)\]$')

        self.window_width = 250
        self.window_height = 150

        self.ui_minimum_size_field = None
        self.ui_maximum_size_field = None
        self.ui_is_non_checked_overrap_shell_checkbox = None

        self.create_ui()

    def create_ui(self):
        """UIを作成・表示する
        """

        if cmds.window(self.window_name, q=True, exists=True):
            cmds.deleteUI(self.window_name, window=True)

        self.window_name = cmds.window(
            self.window_name,
            title=self.tool_name + '  ' + self.tool_version,
            s=True, mnb=True, mxb=False, rtf=True)
        cmds.window(
            self.window_name, e=True,
            widthHeight=(self.window_width, self.window_height))

        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(
            l=u'UVのアイランド間隔チェック',
            cll=True, cl=False, bv=True,
            mw=10, mh=10, visible=True, height=self.window_height - 2)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        self.ui_minimum_size_field = cmds.floatFieldGrp(
            numberOfFields=1, label='間隔チェック　最小値',
            value1=self.DEFAULT_MAX_DISTANCE, columnAlign=[1, 'left'], columnWidth=[1, 140], precision=3)
        self.ui_maximum_size_field = cmds.floatFieldGrp(
            numberOfFields=1, label='間隔チェック　最大値',
            value1=self.DEFAULT_MIN_DISTANCE, columnAlign=[1, 'left'], columnWidth=[1, 140], precision=3)
        self.ui_is_non_checked_overrap_shell_checkbox = cmds.checkBoxGrp(
            numberOfCheckBoxes=1, label='重複するshellはチェックしない',
            columnAlign=[1, 'left'], columnWidth=[1, 140])
        cmds.button(label='チェック実行', command=self.exec_script)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.showWindow(self.window_name)

    def exec_script(self, *args):
        """UV距離チェックの処理を開始する
        """

        too_close_uvs = []

        # 現在の選択を取得
        selected = cmds.ls(sl=True, o=True)
        if not selected:
            cmds.warning('オブジェクトを選択してから実行して下さい')
            return

        is_non_checked_overlap_shell = cmds.checkBoxGrp(self.ui_is_non_checked_overrap_shell_checkbox, q=True, v1=True)
        min_distance = cmds.floatFieldGrp(self.ui_minimum_size_field, q=True, v=True)[0]
        max_distance = cmds.floatFieldGrp(self.ui_maximum_size_field, q=True, v=True)[0]

        for sel in selected:
            result = self.check_uv_distance(sel, is_non_checked_overlap_shell, min_distance, max_distance)
            if result:
                too_close_uvs.extend(result)

        cmds.select(too_close_uvs)

    def check_uv_distance(self, target_node, is_non_checked_overlap_shell=False, min_distance=DEFAULT_MIN_DISTANCE, max_distance=DEFAULT_MAX_DISTANCE):
        """UVShellとBorderEdgeのUVの距離をチェックし、事前に規定した値内であるUVの名前を返却する
        UVShell同士の重なりを無視しない場合(is_non_checked_overlap_shell=False)、BorderEdge同士が重なっている時もエラー判定を行う
        UVShell同士が重なりを無視する場合(is_non_checked_overlap_shell=True)、UVShell同士の距離が規定値内でも少しでも重なっている場合は判定を行わない

        Args:
            target_node (string): チェック対象のノード名
            is_non_checked_overlap_shell (bool, optional): UVShell同士の重なりを無視しないかどうか 規定値はFalse
            min_distance (float, optional): UVShellとBorderEdgeのUVとの距離の最低値
            max_distance (_type_, optional): UVShellとBorderEdgeのUVとの距離の最高値 最低値と最高値の間にあるUVをチェック対象とする

        Returns:
            list: UVShellBorderEdgeのUVとの距離が最低値から最高値の間に値するUVのリスト
        """

        too_close_uvs = []

        # dagPathを取得
        dag_path = self.__get_dag_path(target_node)
        # meshノードを取得
        target_mfn_mesh = om.MFnMesh(dag_path)
        # meshノードのuv情報を取得
        uvset_names = target_mfn_mesh.getUVSetNames()

        for uvset in uvset_names:

            # face毎のuv数とアサインされているuv一覧
            uv_per_face_counts, assigned_uvs = target_mfn_mesh.getAssignedUVs(uvset)

            # 各uvの位置座標(idx順)
            uv_u_pos_list, uv_v_pos_list = target_mfn_mesh.getUVs(uvset)
            uv_pos_list = zip(uv_u_pos_list, uv_v_pos_list)

            # uvShellのBorderEdge一覧
            uv_shell_border_edges = self.fetch_uv_shell_border_edges_by_mesh(target_node)

            # UVShellのUVの数一覧と、UVShellにアサインされているUVのインデックス一覧
            uv_counts_per_uvshell, uv_indices_by_uvshell = target_mfn_mesh.getUvShellsIds(uvset)

            # UVShellとUVのインデックスの組み合わせリスト
            uvshells_uv_list = []
            if is_non_checked_overlap_shell:
                for i in range(uv_counts_per_uvshell):
                    uvshells_uv_list.append([target_node + '.map[' + str(j) + ']' for j in range(len(uv_indices_by_uvshell)) if uv_indices_by_uvshell[j] == i])

            # UVShellのBorderEdgeのUV一覧
            border_edge_uvs = cmds.ls(cmds.polyListComponentConversion(uv_shell_border_edges, toUV=True), fl=True)

            # borderUVと接続しているEdge一覧
            adjacent_edges_to_border_uv = {}
            for border_edge_uv in border_edge_uvs:
                border_uv_adjacent_edges = cmds.ls(cmds.polyListComponentConversion(border_edge_uv, toEdge=True), fl=True)
                adjacent_edges_to_border_uv[border_edge_uv] = border_uv_adjacent_edges

            # 重複するShellもチェックする場合、距離が遠くてもBorderEdge同士が交錯していたらHITさせる
            if not is_non_checked_overlap_shell:
                overwrap_edges = cmds.polyUVOverlap(uv_shell_border_edges, oc=True)
                if overwrap_edges:
                    too_close_uvs.extend(cmds.ls(cmds.polyListComponentConversion(overwrap_edges, toUV=True), fl=True))

            # BorderEdgeのUVのインデックス番号の一覧
            border_uv_suffix_idxs = [self.__pop_up_suffix_idx(border_edge_uv) for border_edge_uv in border_edge_uvs]

            # メッシュにアサインされているテクスチャ一覧と、テクスチャがアサインされているフェース一覧
            asseined_textures, texture_assigned_faces = target_mfn_mesh.getConnectedShaders(0)

            border_uvs_per_texture_idxs_list = []
            # アサインされているテクスチャが同uvsetに2つ以上ある時の処理
            # テクスチャが同じUVShell同士で判定を行う為に切り分けを実行する
            if len(asseined_textures) != 1:

                for i in range(len(asseined_textures)):
                    border_uvs_per_texture_idxs_list.append([])

                count = 0
                for i in range(len(uv_per_face_counts)):
                    face_vtx_counts = uv_per_face_counts[i]
                    texture_idx = texture_assigned_faces[i]
                    cut_count = count + face_vtx_counts
                    uvs_idx = assigned_uvs[count:cut_count]
                    border_uvs_per_texture_idxs_list[texture_idx].extend(uvs_idx)
                    count = cut_count

                for i in range(len(asseined_textures)):
                    diff_list = list(set(border_uvs_per_texture_idxs_list[i][:]) & set(border_uv_suffix_idxs))
                    border_uvs_per_texture_idxs_list[i] = diff_list

            edge_count = 0
            edge_length = len(uv_shell_border_edges)

            cmds.progressWindow(title='Progress...', progress=edge_count,
                                status='Sleeping: 0%', isInterruptable=True,
                                maxValue=edge_length)

            for edge in uv_shell_border_edges:

                if cmds.progressWindow(query=True, isCancelled=True):
                    break
                if cmds.progressWindow(query=True, progress=True) >= edge_length:
                    break

                edge_count += 1
                status = '現在実行中 : {0} / {1}'.format(str(edge_count), str(edge_length))
                cmds.progressWindow(edit=True, progress=edge_count, status=status)

                uvs = cmds.ls(cmds.polyListComponentConversion(edge, toUV=True), fl=True)
                uvs_combies = list(itertools.combinations(uvs, 2))

                for uvs_combi in uvs_combies:

                    uv1 = uvs_combi[0]
                    uv2 = uvs_combi[1]

                    uv1_suffix_idx = self.__pop_up_suffix_idx(uv1)
                    uv2_suffix_idx = self.__pop_up_suffix_idx(uv2)
                    if uv1_suffix_idx is None or uv2_suffix_idx is None:
                        continue

                    uv1_shells_idx = uv_indices_by_uvshell[uv1_suffix_idx]
                    uv2_shells_idx = uv_indices_by_uvshell[uv2_suffix_idx]

                    if uv1_shells_idx != uv2_shells_idx:
                        continue

                    # uv頂点の隣接した頂点以外は対象としない(隣接していないとuvs_shortest_pathが2以上になる)
                    uvs_shortest_path = cmds.polySelect(q=True, shortestEdgePathUV=[uv1_suffix_idx, uv2_suffix_idx])
                    if len(uvs_shortest_path) > 1:
                        continue

                    uv1_pos = uv_pos_list[uv1_suffix_idx]
                    uv2_pos = uv_pos_list[uv2_suffix_idx]

                    u_min = min(uv1_pos[0], uv2_pos[0]) - max_distance
                    u_max = max(uv1_pos[0], uv2_pos[0]) + max_distance
                    v_min = min(uv2_pos[1], uv2_pos[1]) - max_distance
                    v_max = max(uv2_pos[1], uv2_pos[1]) + max_distance

                    border_idxs = []

                    for border_uvs_per_texture_idxs in border_uvs_per_texture_idxs_list:
                        if uv1_suffix_idx in border_uvs_per_texture_idxs:
                            border_idxs = border_uvs_per_texture_idxs
                            break
                    else:
                        border_idxs = border_uv_suffix_idxs

                    for border_idx in border_idxs:

                        uv_border_uvs_shells_idx = uv_indices_by_uvshell[border_idx]
                        if uv1_shells_idx == uv_border_uvs_shells_idx:
                            continue

                        uv3_pos = uv_pos_list[border_idx]

                        # uv3がuv1と2から一定距離離れていたら処理しない
                        if uv3_pos[0] < u_min or uv3_pos[0] > u_max:
                            continue
                        if uv3_pos[1] < v_min or uv3_pos[1] > v_max:
                            continue

                        # BorderEdgeからの距離処理
                        closest_point = self.nearest_point_on_line(uv1_pos, uv2_pos, uv3_pos)
                        # uv3と最近傍頂点の距離計算
                        dist = self.distance_between_points(closest_point, uv3_pos)
                        if min_distance < dist <= max_distance:

                            if is_non_checked_overlap_shell:
                                faces = cmds.polyListComponentConversion(
                                    uvshells_uv_list[uv1_shells_idx] + uvshells_uv_list[uv_border_uvs_shells_idx],
                                    toFace=True)
                                if cmds.polyUVOverlap(faces, oc=True):
                                    continue

                            too_close_uvs.append(target_node + '.map[' + str(border_idx) + ']')

            cmds.progressWindow(endProgress=True)

        return too_close_uvs

    def nearest_point_on_line(self, point_a, point_b, query_point):
        """
        2点AとBで定義された線分上で、与えられたクエリ点に最も近い点を見つける

        Args:
            point_a (tuple): 線分の始点A
            point_b (tuple): 線分の終点B
            query_point (tuple): 線分上で最も近い点を見つけたい点

        Returns:
            tuple: クエリ点に最も近い線分上の点
        """

        # MVectorに変換
        a = om.MVector(point_a)
        b = om.MVector(point_b)
        p = om.MVector(query_point)

        # aからpへのベクトルとaからbへのベクトル
        ap = p - a
        ab = b - a

        # abベクトルの長さの２乗
        ab_squared = ab.length() ** 2

        # zero divide対策
        if ab_squared == 0:
            t = 0
        else:
            # apとabの内積をabの長さの2乗で割る
            t = ap * ab / ab_squared

        # もしt <= 0 だったら、点aが最も近い
        if t <= 0:
            nearest_point = point_a

        # もしt >= 1 だったら、点bが最も近い
        elif t >= 1:
            nearest_point = point_b

        # tが0から1の間にある場合、線上の最も近い点を計算する
        else:
            nearest_point = a + (ab * t)
            nearest_point = (nearest_point.x, nearest_point.y)

        return nearest_point

    def distance_between_points(self, point1, point2):
        """2点間の距離を計算

        Args:
            point1 (taple): 座標1 (x1, y1) or (x1, y1, z1) または任意次元
            point2 (taple): 座標2 (x2, y2) or (x2, y2, z2) または任意次元

        Returns:
            taple: 2点間の距離
        """

        return math.sqrt(sum((x2 - x1) ** 2 for x1, x2 in zip(point1, point2)))

    def fetch_uv_shell_border_edges_by_mesh(self, mesh):
        """メッシュのUVShellのBorderEdgeを取得する

        Args:
            mesh (str): UVShellのBorderEdgeを取得したいメッシュ名

        Returns:
            list: メッシュのUVShellのBOrderEdge一覧
        """

        # 元の選択を取っておく
        selected = cmds.ls(sl=True, l=True)

        # UV境界エッジを取得する
        borderUVEdges = []
        cmds.select(mesh + ".map[*]", r=True)
        mel.eval("polySelectBorderShell 1;")
        borders = cmds.polyListComponentConversion(te=True)
        borders = cmds.ls(borders, fl=True)
        for border in borders:
            edge = cmds.polyListComponentConversion(border, tuv=True)
            edge = cmds.ls(edge, fl=True)
            if len(edge) > 2:
                borderUVEdges.append(border)
        cmds.select(mesh + ".e[*]", r=True)
        mel.eval("polySelectBorderShell 1;")
        borderUVEdges.extend(cmds.ls(sl=True, fl=True))

        # 選択状態を元に戻す
        cmds.select(selected)

        return borderUVEdges

    def __pop_up_suffix_idx(self, node_name):
        """対象のノード名からインデックス番号を切り抜く

        Args:
            target_name (string): インデックスを取得したいノード名

        Returns:
            str or None: 切り抜いたインデックス番号若しくはNone
        """

        suffix = None
        matchObj = self.idx_suffix_pattern.search(node_name)
        if matchObj:
            suffix = matchObj.group(1)
            suffix = int(suffix)

        return suffix

    def __get_dag_path(self, target_node):
        """対象のノードのdagPathを取得する

        Args:
            target_node (string): dagPathを取得したいノード

        Returns:
            MFnDagPath: dagPath
        """

        selectionList = om.MSelectionList()
        selectionList.add(target_node)

        return selectionList.getDagPath(0)
