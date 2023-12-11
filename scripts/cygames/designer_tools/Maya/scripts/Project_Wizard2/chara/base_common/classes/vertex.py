# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


__version__ = '22121201'


try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import re
import math
import operator

import maya.cmds as cmds
import maya.api.OpenMaya as om

from . import kd_tree

reload(kd_tree)


class VtxData(object):
    """頂点情報を保持するクラス
    """

    def __init__(self):

        # 基礎情報
        self.transform = ''
        self.om_mesh = None
        self.index = -1
        self.position = None
        self.face_vtx_datas = []

        # 法線情報
        self.vtx_normal = None
        self.normal_ids = []

    def is_locked(self):
        """全てのフェース頂点法線がロックされているか
        """
        if self.om_mesh:
            return all([self.om_mesh.isNormalLocked(x) for x in self.normal_ids])
        else:
            return False

    def get_name(self):
        """Mayaコマンドで使用する名前の取得
        """
        return self.transform + '.vtx[{}]'.format(str(self.index))


class FaceVtxData(object):
    """VtxDataに紐づいてフェース頂点の法線情報を保持するクラス
    """

    def __init__(self):

        # 基礎情報
        self.transform = ''
        self.om_mesh = None
        self.vtx_index = -1
        self.face_index = -1
        self.face_normal = None

        # 法線情報
        self.face_vtx_normal = None
        self.normal_id = -1

        # UV位置情報
        self.uv_pos = None

    def is_locked(self):
        """フェース頂点法線がロックされているか
        """
        if self.om_mesh:
            return self.om_mesh.isNormalLocked(self.normal_id)
        else:
            return False

    def get_name(self):
        """Mayaコマンドで使用する名前の取得
        """
        return self.transform + '.vtxFace[{}][{}]'.format(self.vtx_index, self.face_index)


def get_vtx_datas(target_components, om_pos_space=om.MSpace.kWorld):
    """頂点情報を取得

    Args:
        target_components ([str]): 頂点情報を取得したいコンポーネントのリスト
        om_pos_space (om.MSpace, optional): 取得する座標空間. Defaults to om.MSpace.kWorld.

    Returns:
        list: VtxDataのリスト
    """

    result_datas = []
    tramsform_vtx_datas_dict = {}

    for target_component in target_components:

        if not cmds.objExists(target_component):
            result_datas.append(None)

        # トランスフォームが指定されていれば全頂点のデータを取得して完了
        if cmds.objectType(target_component, isType='transform'):

            transform = cmds.ls(target_component, l=True)[0]

            if transform not in tramsform_vtx_datas_dict:
                tramsform_vtx_datas_dict[transform] = __get_vtx_datas_per_transform(transform, om_pos_space)

            result_datas.extend(tramsform_vtx_datas_dict[transform])

        # 頂点単位で取得する場合は個別に回すと処理が煩雑になるため
        # 一度メッシュ全体の情報を保持しておいて、その後必要な頂点情報を引き抜く
        else:

            vtxs = cmds.ls(cmds.polyListComponentConversion(target_component, tv=True), l=True, fl=True)
            transform = vtxs[0].split('.vtx')[0]

            if transform not in tramsform_vtx_datas_dict:
                tramsform_vtx_datas_dict[transform] = __get_vtx_datas_per_transform(transform, om_pos_space)

            this_transform_vtx_datas = tramsform_vtx_datas_dict[transform]

            for vtx in vtxs:
                vtx_match = re.search(r'\.vtx\[(\d+)\]', vtx)
                vtx_index = int(vtx_match.group(1))

                result_datas.append(this_transform_vtx_datas[vtx_index])

    return result_datas


def __get_vtx_datas_per_transform(target_transform, om_pos_space):
    """トランスフォームごとの頂点データを取得

    Args:
        target_components ([str]): 頂点情報を取得したいコンポーネントのリスト
        om_pos_space (om.MSpace): 取得する座標空間

    Returns:
        [VtxData]: VtxDataのリスト
    """

    result_vtx_datas = []

    if not cmds.objExists(target_transform):
        return result_vtx_datas

    om_selection = om.MSelectionList()
    om_selection.add(target_transform)
    om_mesh = om.MFnMesh(om_selection.getDagPath(0))
    om_vtx_itr = om.MItMeshVertex(om_selection.getDagPath(0))
    om_face_vtx_itr = om.MItMeshFaceVertex(om_selection.getDagPath(0))

    # 頂点データの取得
    while not om_vtx_itr.isDone():

        this_vtx_data = VtxData()

        # 基礎情報
        this_vtx_data.transform = target_transform
        this_vtx_data.om_mesh = om_mesh
        this_vtx_data.index = int(om_vtx_itr.index())
        this_vtx_data.position = om.MPoint(om_vtx_itr.position(om_pos_space))

        # 法線情報
        this_vtx_data.vtx_normal = om.MVector(om_vtx_itr.getNormal())
        this_vtx_data.normal_ids = om_vtx_itr.getNormalIndices()

        result_vtx_datas.append(this_vtx_data)

        om_vtx_itr.next()

    # フェース頂点データの取得
    while not om_face_vtx_itr.isDone():

        this_face_vtx_data = FaceVtxData()

        # 基礎情報
        this_face_vtx_data.transform = target_transform
        this_face_vtx_data.om_mesh = om_mesh
        this_face_vtx_data.vtx_index = int(om_face_vtx_itr.vertexId())
        this_face_vtx_data.face_index = int(om_face_vtx_itr.faceId())
        this_face_vtx_data.face_normal = this_vtx_data.om_mesh.getPolygonNormal(this_face_vtx_data.face_index)

        # 法線情報
        this_face_vtx_data.face_vtx_normal = om.MVector(om_face_vtx_itr.getNormal())
        this_face_vtx_data.normal_id = int(om_face_vtx_itr.normalId())

        # UV情報
        this_face_vtx_data.uv_pos = om_face_vtx_itr.getUV() if om_face_vtx_itr.hasUVs() else None

        this_vtx_data = result_vtx_datas[this_face_vtx_data.vtx_index]
        this_vtx_data.face_vtx_datas.append(this_face_vtx_data)

        om_face_vtx_itr.next()

    return result_vtx_datas


def get_nearest_pos_vtx_datas(src_vtx_datas, search_from_vtx_datas, should_check_face_normal=True):
    """対応する最近傍頂点データを取得

    Args:
        src_vtx_datas ([VtxData]): 検索するVtxDataリスト
        search_from_vtx_datas ([VtxData]): 検索されるVtxDataリスト
        should_check_face_normal (bool, optional): 同一座標に複数頂点が存在している場合隣接面の向きを考慮にいれるか. Defaults to True.

    Returns:
        [VtxData]: src_vtx_datasに対応するsearch_from_vtx_datas内のVtxDataリスト
    """

    result_datas = []
    vtx_data_tree = __create_kd_tree(search_from_vtx_datas, 'position', 3)

    for vtx_data in src_vtx_datas:

        if should_check_face_normal:
            nearest_vtx_datas = __get_nearest_vtx_datas(vtx_data.position, vtx_data_tree)
            result_datas.append(__get_best_face_normal_match_vtx_data(vtx_data, nearest_vtx_datas))
        else:
            result_datas.append(__get_nearest_vtx_data(vtx_data.position, vtx_data_tree))

    return result_datas


def get_index_match_vtx_datas(src_vtx_datas, search_from_vtx_datas):
    """インデックスが一致する頂点データを取得

    Args:
        src_vtx_datas ([VtxData]): 検索するVtxDataリスト
        search_from_vtx_datas ([VtxData]): 検索されるVtxDataリスト

    Returns:
        [VtxData]: src_vtx_datasに対応するsearch_from_vtx_datas内のVtxDataリスト
    """

    result_datas = []
    search_from_vtx_datas.sort(key=lambda x: x.index)
    split_datas_list = []

    # 検索時間短縮のためにリストをインデックス順にとりあえず100個ずつ区切る
    target_length = 100
    div_num = len(search_from_vtx_datas) // target_length if len(search_from_vtx_datas) >= target_length else 1
    elm_count = len(search_from_vtx_datas) // div_num
    start_index = 0

    while True:
        if start_index + elm_count >= len(search_from_vtx_datas):
            split_datas_list.append(search_from_vtx_datas[start_index:])
            break
        else:
            split_datas_list.append(search_from_vtx_datas[start_index:start_index + elm_count])
            start_index = start_index + elm_count

    for vtx_data in src_vtx_datas:

        is_hit = False

        # 目的のindexがいる区切りの中から探す
        search_datas = []
        for split_datas in split_datas_list:
            if split_datas[0].index <= vtx_data.index <= split_datas[-1].index:
                search_datas = split_datas
                break

        for from_vtx_data in search_datas:

            if vtx_data.index == from_vtx_data.index:
                result_datas.append(from_vtx_data)
                is_hit = True
                break

        if not is_hit:
            result_datas.append(None)

    return result_datas


def get_transform_matched_vtx_datas(target_transform, target_vtxdatas):
    """トランスフォーム名がマッチしたvtxdataのリストを収集

    Args:
        target_transform (str): ターゲットのtransform
        target_vtxdatas (list(vtxdata)): 検索対象のvtxdataのlist

    Returns:
        list(vtxdata): マッチしたvtxdataのリスト
    """
    result_vtx_datas = []
    for vtx_data in target_vtxdatas:
        if vtx_data.transform == target_transform:
            result_vtx_datas.append(vtx_data)

    return result_vtx_datas


def get_nearest_uv_pos_vtx_datas(query_vtxdatas, search_target_vtxdatas, tolerance=-1):
    """対応するUVが最近傍である頂点データを取得

    Args:
        query_vtxdatas (list[vtxdata]): 検索するvtxdataのリスト
        search_target_vtxdatas (list[vtxdata]): 検索されるvtxdataのリスト
        tolerance (int|float, optional): UV距離の許容値を設定します。-1の場合はすべての距離を許容. Defaults to -1.

    Returns:
        list(vtxdata|None): 検索結果のvtxdataのリスト(マッチできなかったものはNoneが帰る)
    """

    result_datas = []

    # facevtxだけのリストとfacevtx->vtx逆引きデータを作っておく
    facevtxdatas = []
    facevtx_to_vtx = {}
    for vtxdata in search_target_vtxdatas:
        facevtxdatas.append(vtxdata.face_vtx_datas[0])

        facevtx_to_vtx[vtxdata.face_vtx_datas[0]] = vtxdata

    vtx_data_tree = __create_kd_tree(facevtxdatas, 'uv_pos', 2)

    for vtx_data in query_vtxdatas:

        if not vtx_data.face_vtx_datas[0].uv_pos:
            result_datas.append(None)

        vtx_in_tolerance = __get_nearest_facevtx(vtx_data.face_vtx_datas[0].uv_pos, vtx_data_tree, 'uv_pos', tolerance)
        if not vtx_in_tolerance:
            result_datas.append(None)
        else:
            vtx_distance = 9999
            best = None
            for facevtx in vtx_in_tolerance:
                if best is None:
                    best = facevtx_to_vtx[facevtx]
                    vtx_distance = __get_distance(facevtx_to_vtx[facevtx].position, vtx_data.position)

                current_vtx_distance = __get_distance(facevtx_to_vtx[facevtx].position, vtx_data.position)
                if current_vtx_distance < vtx_distance:
                    vtx_distance = current_vtx_distance
                    best = facevtx_to_vtx[facevtx]

            result_datas.append(best)

    return result_datas


def __get_best_face_normal_match_vtx_data(vtx_data, search_from_vtx_datas):
    """隣接フェースの法線平均が一番近い頂点データを取得

    Args:
        vtx_data (VtxData): 検索するVtxData
        search_from_vtx_datas ([VtxData]): 検索されるVtxDataリスト

    Returns:
        VtxData: 隣接フェースの平均が一番近いVtxData
    """

    if len(search_from_vtx_datas) == 1:
        return search_from_vtx_datas[0]

    face_normal_avarage = __get_face_nomal_avarage_around_vtx(vtx_data)
    max_dot_value = -1
    bast_match_data = None

    for search_from_vtx_data in search_from_vtx_datas:
        this_face_normal_avarage = __get_face_nomal_avarage_around_vtx(search_from_vtx_data)
        if face_normal_avarage * this_face_normal_avarage >= max_dot_value:
            max_dot_value = face_normal_avarage * this_face_normal_avarage
            bast_match_data = search_from_vtx_data

    return bast_match_data


def __get_face_nomal_avarage_around_vtx(vtx_data):
    """隣接フェースの法線平均を取得

    Args:
        vtx_data (VtxData): 隣接フェースの法線平均を取得する頂点データ

    Returns:
        om.MVector: 隣接フェースの法線平均
    """

    face_normal_sum = om.MVector([0, 0, 0])

    for face_vtx_data in vtx_data.face_vtx_datas:
        face_normal_sum += face_vtx_data.face_normal

    return face_normal_sum.normalize()


def __create_kd_tree(src_datas, target_attr, dimentions):
    """KDツリーを作成する

    Args:
        src_datas (list(VtxData|FaceVtxData)): KDツリーのもととなるデータ
        target_attr (str): 対象のアトリビュート
        dimentions (int): 次元数

    Returns:
        kd_tree.KDTree: 作成されたkdツリー
    """
    return kd_tree.KDTree(src_datas, operator.attrgetter(target_attr), dimentions)


def __get_nearest_vtx_data(position, vtx_data_tree):
    """再近傍のVtxDataを取得

    Args:
        position (list[int|float]): 検索座標
        vtx_data_tree (kd_tree.KDTree): 頂点位置のKDツリー

    Returns:
        VtxData: 再近傍のVtxData
    """
    return vtx_data_tree.search_point(position)[0]


def __get_nearest_vtx_datas(position, vtx_data_tree, tolerance=0.0001):
    """検索座標から許容範囲内の近傍VtxDataを取得

    Args:
        position (list[int|float]): 検索座標
        vtx_data_tree (kd_tree.KDTree): 頂点位置のKDツリー
        tolerance (float, optional): 許容範囲内. Defaults to 0.0001.

    Returns:
        list[VtxData]: 検索座標から許容範囲内の近傍VtxDataのリスト
    """
    nearest = __get_nearest_vtx_data(position, vtx_data_tree)
    return vtx_data_tree.search_radius(nearest.position, tolerance)


def __get_nearest_facevtx(position, data_tree, pos_attr, tolerance):
    """ある位置から許容範囲内にあるfaceVtxを返す。


    Args:
        position (list(int, float)): 比較したい位置情報
        data_tree (kd_tree.KDTree): 作成されたkdツリー
        pos_attr (str): 位置を取得するアトリビュート名. UVなら'uv_pos'など.
        tolerance (int|float): 距離の誤差の許容値。-1の場合は距離は無視する

    Returns:
        list(FaceVtxData)|None: マッチしたkdツリーのアイテム。範囲内に存在しない場合はNoneを返す
    """
    match_point, distance = data_tree.search_point(position)
    if not match_point or distance > tolerance:
        return None
    current_pos = operator.attrgetter(pos_attr)(match_point)
    match_points = data_tree.search_radius(current_pos, 0.0001)
    return match_points


def __get_distance(pos1, pos2):
    """2点間の距離を計算する

    Args:
        pos1 (list(int|float)): 位置座標1
        pos2 (list(int|float)): 位置座標2

    Returns:
        float: pos1とpos2の距離
    """
    squared_distance = 0.0
    for i in range(len(pos1)):
        squared_distance += pow(pos1[i] - pos2[i], 2)

    return math.sqrt(squared_distance)
