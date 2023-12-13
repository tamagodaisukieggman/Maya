# -*- coding: utf-8 -*-
u"""InsertEdgesCmd

.. END__CYGAMES_DESCRIPTION
"""

import math

import maya.cmds as cmds

from mtku.maya.utils.edgesort import sort_contiguous_order
from mtku.maya.mtklog import MtkLog


logger = MtkLog(__name__)


class InsertEdgesCmd(object):

    @classmethod
    def _convert_vertices(cls, comps):
        u"""componentをvertexに変換

        :param comps: コンポーネント
        :return: vertexのリスト
        """
        return cmds.ls(cmds.polyListComponentConversion(comps, tv=True), fl=True)

    @classmethod
    def _convert_edges(cls, comps):
        u"""componentをedgeに変換

        :param comps: コンポーネント
        :return: edgeのリスト
        """
        return cmds.ls(cmds.polyListComponentConversion(comps, te=True), fl=True)

    @classmethod
    def _convert_faces(cls, comps):
        u"""componentをfaceに変換

        :param comps: コンポーネント
        :return: faceのリスト
        """
        return cmds.ls(cmds.polyListComponentConversion(comps, tf=True), fl=True)

    @classmethod
    def _is_connected_face(cls, face1, face2):
        u"""faceが接続されているかどうか

        :param face1: face1
        :param face2: face2
        :return: bool
        """
        vertices1 = cls._convert_vertices(face1)
        vertices2 = cls._convert_vertices(face2)
        common_vertices = set(vertices1) & set(vertices2)
        if len(common_vertices) == 2:
            return True
        else:
            return False

    @classmethod
    def _get_index(cls, comp):
        u"""componentのインデックスの取得

        :param comp: コンポーネント
        :return: index (エラーの場合は-1を返す)
        """
        index = comp.split('[')[-1].split(']')[0]
        try:
            index = int(index)
            return index
        except ValueError:
            logger.warning(u'コンポーネントが指定されていません')
            return -1

    @classmethod
    def _get_length(cls, edge):
        u"""edgeの長さ(cm)を取得

        :param edge: エッジ
        :return: 長さ(cm)
        """
        vertices = cls._convert_vertices(edge)
        pos1 = cmds.pointPosition(vertices[0], w=True)
        pos2 = cmds.pointPosition(vertices[1], w=True)
        vec = (pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2])
        length = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
        return length

    @classmethod
    def _convert_length_to_weight(cls, edge, length):
        u"""指定した長さ(cm)をedgeのウェイト値(パーセンテージ)に変換

        :param edge: エッジ
        :param length: 長さ(cm)
        :return: weight (ウェイト値が0以下または100以上の場合は-1を返す)
        """
        edge_length = cls._get_length(edge)
        weight = float(length) / edge_length
        if weight <= 0 or weight >= 1:
            return -1
        return weight

    @classmethod
    def _is_contigous_edge(cls, edge1, edge2):
        u"""edgeが繋がっているか

        :param edge1: エッジ1
        :param edge2: エッジ2
        :return: bool
        """
        vertices1 = set(cls._convert_vertices(edge1))
        vertices2 = set(cls._convert_vertices(edge2))
        return True if vertices1 & vertices2 else False

    @classmethod
    def _is_loop_edges(cls, sort_edges):
        u"""エッジのリスト(接続順)がループしているか

        :param sort_edges: エッジのリスト(接続順)
        :return: bool
        """
        if len(sort_edges) < 3:
            return False

        if cls._is_contigous_edge(sort_edges[0], sort_edges[-1]):
            return True
        else:
            return False

    @classmethod
    def _is_relation_of_ring_edges(cls, edge1, edge2):
        u"""Ring Edgeの関係かどうか

        :param edge1: エッジ1
        :param edge2: エッジ2
        :return: bool
        """
        faces1 = set(cls._convert_faces(edge1))
        faces2 = set(cls._convert_faces(edge2))
        return True if faces1 & faces2 else False

    @classmethod
    def _sort_vertices(cls, sort_edges):
        u"""エッジ順に並べた頂点のリストを返す

        :param sort_edges: エッジのリスト(接続順)
        :return: 頂点のリスト(接続順)
        """
        sort_vertices = []
        is_loop = cls._is_loop_edges(sort_edges)

        for i, edge in enumerate(sort_edges):
            vertices1 = cls._convert_vertices(sort_edges[i])
            if i == len(sort_edges) - 1:
                vertices2 = cls._convert_vertices(sort_edges[i - 1])
                if list(set([vertices1[0]]) - set(vertices2)):
                    sort_vertices.append(vertices1[1])
                    if not is_loop:
                        sort_vertices.append(vertices1[0])
                else:
                    sort_vertices.append(vertices1[0])
                    if not is_loop:
                        sort_vertices.append(vertices1[1])

            else:
                vertices2 = cls._convert_vertices(sort_edges[i + 1])
                sort_vertices += list(set(vertices1) - set(vertices2))

        return sort_vertices

    @classmethod
    def _get_ring_edges(cls, sort_edges, side_faces):
        u"""リングエッジの取得

        :param sort_edges: エッジのリスト(接続順)
        :param side_faces:
        :return: リングエッジのリスト (接続順)
        """
        sort_ring_edges = []

        checker_edges = cls._convert_edges(cls._convert_vertices(sort_edges))
        ring_edges = list((set(cls._convert_edges(side_faces)) & set(checker_edges)) - set(sort_edges))

        sort_vertices = cls._sort_vertices(sort_edges)
        for edge in ring_edges:
            _vertices = cls._convert_vertices(edge)
            if set(_vertices) & set([sort_vertices[0]]):
                sort_ring_edges.append(edge)
                ring_edges.remove(edge)
                break
        i = 0
        while ring_edges:
            for edge in ring_edges:
                if cls._is_relation_of_ring_edges(sort_ring_edges[i], edge):
                    sort_ring_edges.append(edge)
                    i += 1
                    break
            ring_edges.remove(edge)

        return sort_ring_edges

    @classmethod
    def _sort_edges_by_ring_edges(cls, edges, ring_edges):
        u"""リングエッジの順番に合わせてエッジをソート

        :param edges: ソートしたいエッジのリスト
        :param ring_edges: リングエッジのリスト(接続順)
        :return: エッジのリスト(ソート結果)
        """
        temp_edges = edges[:]
        sort_edges = []

        for i in range(len(ring_edges) - 1):
            checker_vertices = cls._convert_vertices([ring_edges[i], ring_edges[i + 1]])
            for edge in temp_edges:
                count = len(set(cls._convert_vertices(edge)) & set(checker_vertices))
                if count == 2:
                    sort_edges.append(edge)
                    temp_edges.remove(edge)
        if temp_edges:
            sort_edges.append(temp_edges[0])
        return sort_edges

    @classmethod
    def _get_side_faces_of_edges(cls, edges, side_face0):
        u"""指定したエッジに隣接するフェースを取得する

        :param edges: エッジのリスト
        :param side_face0: edges[0]に隣接するフェース(どちら側を取得するかの判定用)
        :return: 隣接フェースのリスト
        """
        faces = [side_face0]
        checker_edges = cls._convert_edges(cls._convert_faces(edges))

        for i in range(1, len(edges)):
            _faces = cls._convert_faces(edges[i])

            if cls._is_connected_face(_faces[0], faces[i - 1]):
                faces.append(_faces[0])
            elif cls._is_connected_face(_faces[1], faces[i - 1]):
                faces.append(_faces[1])
            else:
                _edges = cls._convert_edges(cls._convert_vertices(_faces[0]))
                if len(set(checker_edges) & set(_edges)) < 11:
                    faces.append(_faces[0])
                else:
                    faces.append(_faces[1])
        return faces

    @classmethod
    def _split_list_by_side_faces(cls, sort_edges, side_faces):
        u"""エッジのリストを隣接フェースの情報に基づいて分割

        両脇に4角形以外のフェースがあった場合、連続してスプリットできないので
        連続してスプリットできる単位に分割する

        :param sort_edges: エッジのリスト(接続順)
        :param side_faces: 隣接フェースのリスト (4角形かどうかの判定用)
        :return: エッジのリストのリスト
        """
        edges_group = []
        group = []
        for edge, face in zip(sort_edges, side_faces):
            if len(cls._convert_vertices(face)) == 4:
                group.append(edge)
            else:
                if group:
                    edges_group.append(group)
                    group = []
        if group:
            edges_group.append(group)

        if len(edges_group) > 1:
            group1 = edges_group[0]
            group2 = edges_group[1]
            if cls._is_contigous_edge(group1[0], group2[-1]):
                edges_group = [group2 + group1] + edges_group[1:-1]

        logger.debug(u'リストの分割前')
        logger.debug(sort_edges)
        logger.debug(u'リストの分割後')
        logger.debug(edges_group)

        return edges_group

    @classmethod
    def _filter_ring_edges(cls, ring_edges):
        u"""Ring Edgeとして不正なEdgeを除外する

        不正なエッジ => 隣接ポリゴンが4角形以外

        :param ring_edges: Ring Edge
        :return: 適切なリングエッジのリスト
        """
        _ring_edges = ring_edges[:]
        for i, edge in enumerate(ring_edges):
            count = 0
            faces = cls._convert_faces(ring_edges[i])
            for face in faces:
                count += len(cls._convert_vertices(face))
            # if count == 3 or count == 6 or count == 7:
            if count == 3 or count == 6:
                _ring_edges.remove(ring_edges[i])

        return _ring_edges

    @classmethod
    def _verifies_insertpoint(cls, insertpoint):
        u"""insertpointが問題ないかチェック

        :param insertpoint: insertpoint
        :return: bool
        """
        if not insertpoint:
            logger.warning(u'対象が全て4角形以外のポリゴンだったため処理を停止しました')
            return False

        for index, weight in insertpoint:
            if index == -1:
                logger.warning(u'不正なコンポーネントが選択されています')
                return False
            elif weight >= 1 or weight < 0:
                logger.warning(u'指定した長さがエッジの長さに対して不正です')
                return False

        return True

    @classmethod
    def _insert_edges(cls, sort_edges, ring_edges, distance, angle):
        u"""Insert Edges

        :param sort_edges: エッジのリスト(接続順)
        :param ring_edges: リングエッジのリスト
        :param distance: 距離
        :param angle: Smoothing Angle
        """
        if not ring_edges:
            return

        _ring_edges = cls._filter_ring_edges(ring_edges)

        insertpoint = [
            (cls._get_index(edge), cls._convert_length_to_weight(edge, distance)) for edge in _ring_edges
        ]
        if cls._is_loop_edges(sort_edges):
            insertpoint.append(insertpoint[0])

        # insertpointが適切かチェック
        if not cls._verifies_insertpoint(insertpoint):
            return

        # 分割
        cmds.select(ring_edges)
        his = cmds.polySplit(ip=insertpoint, sma=angle, ch=True)[0]

        # 分割後の長さチェック
        check_vertices = set(cls._convert_vertices(sort_edges))
        for i, edge in enumerate(_ring_edges):
            vertices = set(cls._convert_vertices(edge))
            if not (vertices & check_vertices):
                weight = 1.0 - cmds.getAttr('{0}.edge[{1}]'.format(his, i))
                cmds.setAttr('{0}.edge[{1}]'.format(his, i), weight)

        if cls._is_loop_edges(sort_edges):
            weight = cmds.getAttr('{0}.edge[0]'.format(his))
            cmds.setAttr('{0}.edge[{1}]'.format(his, len(sort_edges)), weight)

    @classmethod
    def main(cls, edges, mode, inverse, distance, angle):
        u"""main関数

        :param edges: エッジのリスト
        :param mode: 1 片側, 2 両側
        :param inverse: 片側のとき分割側を反転する
        :param distance: 距離
        :param angle: Smoothing Angle
        """
        sort_edges = sort_contiguous_order(edges)
        start_faces = cls._convert_faces(sort_edges[0])

        faces1 = cls._get_side_faces_of_edges(sort_edges, start_faces[0])
        faces2 = cls._get_side_faces_of_edges(sort_edges, start_faces[1])

        edges_group1 = cls._split_list_by_side_faces(sort_edges, faces1)
        edges_group2 = cls._split_list_by_side_faces(sort_edges, faces2)

        sort_edges_group1 = []
        sort_edges_group2 = []
        ring_edges_group1 = []
        ring_edges_group2 = []

        for _sort_edges in edges_group1:
            temp_ring_edges = cls._get_ring_edges(_sort_edges, faces1)
            temp_sort_edges = cls._sort_edges_by_ring_edges(_sort_edges, temp_ring_edges)
            sort_edges_group1.append(temp_sort_edges)
            ring_edges_group1.append(temp_ring_edges)

        for _sort_edges in edges_group2:
            temp_ring_edges = cls._get_ring_edges(_sort_edges, faces2)
            temp_sort_edges = cls._sort_edges_by_ring_edges(_sort_edges, temp_ring_edges)
            sort_edges_group2.append(temp_sort_edges)
            ring_edges_group2.append(temp_ring_edges)

        if mode == 1:
            if not inverse:
                sort_edges_group = sort_edges_group1
                ring_edges_group = ring_edges_group1
            else:
                sort_edges_group = sort_edges_group2
                ring_edges_group = ring_edges_group2
        else:
            sort_edges_group = sort_edges_group1 + sort_edges_group2
            ring_edges_group = ring_edges_group1 + ring_edges_group2

        for i, _sort_edges in enumerate(sort_edges_group):
            cls._insert_edges(sort_edges_group[i], ring_edges_group[i], distance, angle)
