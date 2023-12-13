# -*- coding: utf-8 -*-

from __future__ import absolute_import as __absolute_import
from __future__ import unicode_literals as __unicode_literals
from __future__ import division as _division
from __future__ import print_function as __print_function

import itertools
import operator

import maya.cmds as __cmds
import maya.api.OpenMaya as om2

from ...utility import transform, vector

try:
    from importlib import reload
except Exception:
    pass

reload(transform)
reload(vector)


class KDTree(object):

    def __init__(self, data_list, position_getter, k, depth=0):

        self.position_getter = position_getter

        self.axis = depth % k

        self.data = None
        self.left = None
        self.right = None

        if data_list:
            data_list.sort(key=lambda x: self.position_getter(x)[self.axis])
            index = len(data_list) // 2

            self.data = data_list[index]
            self.left = KDTree(data_list[:index], self.position_getter, k, depth + 1)
            self.right = KDTree(data_list[index + 1:], self.position_getter, k, depth + 1)

    def search_point(self, point):
        """近傍探索

        Args:
            point (MPoint): 探索する位置

        Returns:
            object: 最近傍点に位置するオブジェクト
        """

        if self.data is None:
            return None

        pos = self.position_getter(self.data)

        best = (self.data, pos.distanceTo(point))

        first, second = (self.left, self.right) if pos[self.axis] > point[self.axis] else (self.right, self.left)

        first_best = first.search_point(point)

        if first_best and first_best[1] < best[1]:
            best = first_best

        if best[1] > abs(point[self.axis] - pos[self.axis]):
            second_best = second.search_point(point)

            if second_best and second_best[1] < best[1]:
                best = second_best

        return best

    def search_radius(self, point, radius):
        """半径探索

        Args:
            point (MPoint): 探索する位置
            radius (float): 探索する頂点からの範囲

        Returns:
            list[object]: 半径内に位置するオブジェクト
        """

        result = []

        if self.data is None:
            return result

        pos = self.position_getter(self.data)

        if pos.distanceTo(point) <= radius:
            result.append(self.data)

        first, second = (self.left, self.right) if pos[self.axis] > point[self.axis] else (self.right, self.left)

        result.extend(first.search_radius(point, radius))

        if radius >= abs(point[self.axis] - pos[self.axis]):
            result.extend(second.search_radius(point, radius))

        return result


class VertexInfo(object):

    def __init__(self, index, position):

        self.index = index
        self.position = om2.MPoint(position)


# ==================================================
def get_mesh_shape(target_transform):
    """
    シェープノードを取得

    :param target_transform: 対象トランスフォーム

    :return: メッシュシェープ名
    """

    return transform.get_shape(target_transform, ['mesh'])


# ==================================================
def get_transform_from_vertex(vertex_name):
    """
    トランスフォームを頂点名から取得

    :param vertex_face: 対象頂点名など

    :return トランスフォーム
    """

    transform = vertex_name.split('.')[0]

    return transform


# ==================================================
def get_vertex_index(vertex_name):
    """
    頂点名から頂点番号を取得

    :param vertex_name: 対象頂点名

    :return: 頂点番号
    """

    start_index = vertex_name.find('[') + 1
    end_index = vertex_name.find(']')

    return int(vertex_name[start_index:end_index])


# ==================================================
def get_vertex_list(target_transform):
    """
    頂点リストを取得

    :param target_transform: 対象トランスフォーム

    :return: 頂点リスト取得
    """

    if not transform.exists(target_transform):
        return

    vertex_list = __cmds.ls(
        (__cmds.polyListComponentConversion(target_transform, tv=True)),
        l=True,
        fl=True
    )

    if not vertex_list:
        return

    return vertex_list


# ==================================================
def get_vertex_index_list(target_transform):
    """
    頂点番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: 頂点番号の配列
    """

    vertex_list = get_vertex_list(target_transform)

    if not vertex_list:
        return

    vertex_index_list = []

    for vertex in vertex_list:

        vertex_index = get_vertex_index(vertex)

        vertex_index_list.append(vertex_index)

    return vertex_index_list


# ==================================================
def get_edge_index(edge_name):
    """
    エッジ名から頂点番号を取得

    :param vertex_name: 対象エッジ名

    :return: エッジ番号
    """

    start_index = edge_name.find('[') + 1
    end_index = edge_name.find(']')

    return int(edge_name[start_index:end_index])


# ==================================================
def get_edge_list(target_transform):
    """
    エッジリストを取得

    :param target_transform: 対象トランスフォーム

    :return: エッジリスト取得
    """

    if not transform.exists(target_transform):
        return

    edge_list = __cmds.ls(
        (__cmds.polyListComponentConversion(target_transform, te=True)),
        l=True,
        fl=True
    )

    if not edge_list:
        return

    return edge_list


# ==================================================
def get_edge_index_list(target_transform):
    """
    エッジ番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: エッジ番号の配列
    """

    edge_list = get_edge_list(target_transform)

    if not edge_list:
        return

    edge_index_list = []

    for edge in edge_list:

        edge_index = get_edge_index(edge)

        edge_index_list.append(edge_index)

    return edge_index_list


# ==================================================
def get_face_index(face_name):
    """
    フェース名から頂点番号を取得

    :param vertex_name: 対象フェース名

    :return: フェース番号
    """

    start_index = face_name.find('[') + 1
    end_index = face_name.find(']')

    return int(face_name[start_index:end_index])


# ==================================================
def get_face_list(target_transform):
    """
    フェースリストを取得

    :param target_transform: 対象トランスフォーム

    :return: フェースリスト取得
    """

    if not transform.exists(target_transform):
        return

    face_list = __cmds.ls(
        (__cmds.polyListComponentConversion(target_transform, tf=True)),
        l=True,
        fl=True
    )

    if not face_list:
        return

    return face_list


# ==================================================
def get_face_index_list(target_transform):
    """
    フェース番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: フェース番号の配列
    """

    face_list = get_face_list(target_transform)

    if not face_list:
        return

    face_index_list = []

    for face in face_list:

        face_index = get_face_index(face)

        face_index_list.append(face_index)

    return face_index_list


# ==================================================
def get_vertex_and_face_index(vertex_face_name):
    """
    頂点フェース名から頂点フェース番号を取得

    :param vertex_face_name: 対象頂点フェース名

    :return [頂点番号, フェース番号]
    """

    vtx_face_string = vertex_face_name.split('.')[-1]

    vtx_face_string = vtx_face_string.replace('vtxFace[', '')
    vtx_face_string = vtx_face_string.replace(']', '')

    split_string = vtx_face_string.split('[')

    vertex_index = split_string[0]
    face_index = split_string[1]

    return [int(vertex_index), int(face_index)]


# ==================================================
def get_vertex_face_list(target_transform):
    """
    頂点フェースリストを取得

    :param target_transform: 対象トランスフォーム

    :return: 頂点フェースリスト取得
    """

    if not transform.exists(target_transform):
        return

    vertex_face_list = __cmds.ls(
        (__cmds.polyListComponentConversion(target_transform, tvf=True)),
        l=True,
        fl=True
    )

    if not vertex_face_list:
        return

    return vertex_face_list


# ==================================================
def get_vertex_face_index_list(target_transform):
    """
    頂点フェース番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: [頂点番号,フェース番号]の配列
    """

    if not transform.exists(target_transform):
        return

    vertex_face_list = get_vertex_face_list(target_transform)

    if not vertex_face_list:
        return

    vertex_face_index_list = []
    for vertex_face in vertex_face_list:

        vtx_and_face_index = get_vertex_and_face_index(vertex_face)

        vertex_face_index_list.append(
            [vtx_and_face_index[0], vtx_and_face_index[1]])

    return vertex_face_index_list


# ==================================================
def get_uv_index(uv_name):
    """
    UV名からUV番号を取得

    :param uv_name: 対象UV名

    :return: UV番号
    """

    start_index = uv_name.find('[') + 1
    end_index = uv_name.find(']')

    return int(uv_name[start_index:end_index])


# ==================================================
def get_uv_list(target_transform):
    """
    UVリストを取得

    :param target_transform: 対象トランスフォーム

    :return: UVリスト取得
    """

    if not transform.exists(target_transform):
        return

    uv_list = __cmds.ls(
        (__cmds.polyListComponentConversion(target_transform, tuv=True)),
        l=True,
        fl=True
    )

    if not uv_list:
        return

    return uv_list


# ==================================================
def get_uv_index_list(target_transform):
    """
    UV番号リストを取得

    :param target_transform: 対象トランスフォーム

    :return: UV番号の配列
    """

    uv_list = get_uv_list(target_transform)

    if not uv_list:
        return

    uv_index_list = []

    for uv in uv_list:

        uv_index = get_uv_index(uv)

        uv_index_list.append(uv_index)

    return uv_index_list


# ==================================================
def get_vertex_index_pair_list_by_index(
    src_vertex_index_list,
    dst_vertex_index_list,
):
    """
    頂点番号によって対応する頂点番号ペアリストを取得

    :param src_vertex_index_list: 元頂点番号リスト
    :param dst_vertex_index_list: 先頂点番号リスト

    :return: [元頂点番号,先頂点番号]の配列
    """

    if not src_vertex_index_list:
        return

    if not dst_vertex_index_list:
        return

    vertex_index_pair_list = [None] * len(src_vertex_index_list)

    count = 0
    for src_vertex_index in src_vertex_index_list:

        for dst_vertex_index in dst_vertex_index_list:

            if src_vertex_index != dst_vertex_index:
                continue

            vertex_index_pair_list[count] = \
                [src_vertex_index, dst_vertex_index]

            count += 1

            break

    if count == 0:
        return

    vertex_index_pair_list = vertex_index_pair_list[0:count]

    return vertex_index_pair_list


def get_vertex_index_pair_list_by_position(
        src_vertex_index_list,
        src_all_vtx_info_list,
        dst_vertex_index_list,
        dst_all_vtx_info_list):
    """座標を元にした近傍頂点ペアのリストを返す

    Args:
        src_all_vtx_info_list (list[int, [float, float, float]]): コピー元の頂点情報リスト
        dst_all_vtx_info_list (list[int, [float, float, float]]): コピー先の頂点情報リスト

    Returns:
        list[int, int]: 近傍頂点ペアのリスト
    """

    # src_all_vtx_info_list、dst_all_vtx_info_listは[頂点番号, [x, y, z]]のリスト
    src_info_list = [VertexInfo(index, pos) for index, pos in src_all_vtx_info_list if index in src_vertex_index_list]
    dst_info_list = [VertexInfo(index, pos) for index, pos in dst_all_vtx_info_list if index in dst_vertex_index_list]

    tree = KDTree(src_info_list, operator.attrgetter('position'), 3)

    return [[tree.search_point(dst_info.position)[0].index, dst_info.index] for dst_info in dst_info_list]


def get_vertex_index_pair_list_by_uv_position(
        src_vertex_index_list,
        src_all_uv_info_list,
        src_all_vtx_info_list,
        dst_vertex_index_list,
        dst_all_uv_info_list,
        dst_all_vtx_info_list):
    """UV座標を元にした近傍頂点ペアのリストを返す

    まずコピー先の『頂点』に対して最近傍であるコピー元の『UV』を求める
    その後、コピー元の『UV』を持つ『頂点』を取得し、コピー先の『頂点』と比較、最近傍を求める

    Args:
        src_all_uv_info_list (list[int, int, int, [float, float]]): コピー元のuv情報リスト
        src_all_vtx_info_list (list[int, [float, float, float]]): コピー元の頂点情報リスト
        dst_all_uv_info_list (list[int, int, int, [float, float]]): コピー先のuv情報リスト
        dst_all_vtx_info_list (list[int, [float, float, float]]): コピー先の頂点情報リスト

    Returns:
        list[int, int]: 近傍頂点ペアのリスト
    """

    # src_uv_info_list、dst_uv_info_listは[uv番号 ,頂点番号, 頂点フェース番号,[u,v]]のリスト
    src_uv_info_list = [VertexInfo(uv_index, uv) for uv_index, vtx_index, _, uv in src_all_uv_info_list if vtx_index in src_vertex_index_list]
    src_vtx_info_list = [VertexInfo(vtx_index, uv) for _, vtx_index, _, uv in src_all_uv_info_list if vtx_index in src_vertex_index_list]
    dst_vtx_info_list = [VertexInfo(vtx_index, uv) for _, vtx_index, _, uv in dst_all_uv_info_list if vtx_index in dst_vertex_index_list]

    src_uv_tree = KDTree(src_uv_info_list, operator.attrgetter('position'), 2)
    search_point_pair_list = [(src_uv_tree.search_point(dst_info.position), dst_info.index) for dst_info in dst_vtx_info_list]
    # (src_index, dst_index, distance)のリストを作成
    index_dist_list = [(src_info[0].index, dst_index, src_info[1]) for src_info, dst_index in search_point_pair_list]
    # dst_indexとdistanceでソートしてdst_indexでグループ化
    # dst_indexをキーとし、距離が近い順に上記タプルが入ったgroupが得られる
    key_group_list = itertools.groupby(sorted(index_dist_list, key=operator.itemgetter(1, 2)), key=operator.itemgetter(1))
    # (uv_index, dst_index)のリスト
    uv_dst_pair_list = [(next(group)[0], key) for key, group in key_group_list]

    # UVとsrc_indexを紐づける辞書
    src_vtx_tree = KDTree(src_vtx_info_list, operator.attrgetter('position'), 3)
    uv_src_dict = {
        uv_info.index: set(vtx_info.index for vtx_info in src_vtx_tree.search_radius(uv_info.position, 0)) for uv_info in src_uv_info_list
    }

    src_pos_list = [om2.MPoint(position) for _, position in src_all_vtx_info_list]
    dst_pos_list = [om2.MPoint(position) for _, position in dst_all_vtx_info_list]

    def get_nearest(uv_index, dst_index):
        """uv_src_dict、src_pos_list、dst_pos_listを元に最も近い頂点インデックスを返す

        上記リストを使用するため関数内関数として定義

        Args:
            uv_index (int): uv番号
            dst_index (int): コピー先頂点番号

        Returns:
            int: 近傍頂点インデックス
        """

        index = None
        min_distance = None

        for src_index in uv_src_dict[uv_index]:
            distance = src_pos_list[src_index].distanceTo(dst_pos_list[dst_index])
            if min_distance is None or distance < min_distance:
                index = src_index
                min_distance = distance

        return index

    return [[get_nearest(uv_index, dst_index), dst_index] for uv_index, dst_index in uv_dst_pair_list]
