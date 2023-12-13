# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from builtins import zip
    from importlib import reload
except Exception:
    pass

import itertools
import operator

import maya.api.OpenMaya as om2

from ..utility import open_maya as om_utility

reload(om_utility)


class NormalInfo(object):
    """法線情報クラス

    法線情報クラスはそれぞれ、さらに細かい単位の法線情報クラスのリストを持つ
    NormalInfo > ObjectNormalInfo > VertexNormalInfo > VertexFaceNormalInfo
    法線自体はVertexFaceNormalInfoが持つ

    Attributes:
        info_list (list[ObjectNormalInfo]): オブジェクトごとの法線情報リスト
    """

    def __init__(self):

        self.info_list = None

    def create_info(self, target_list, is_locked_vtx_only):
        """法線情報を作成する

        Args:
            target_list (OpenMaya.MSelectionList): 作成対象の選択リスト
            is_locked_vtx_only (bool): ロック法線のみを対象とするか
        """

        vert_sel_list = om_utility.convert_to_vertex(target_list)

        info_dict = {}

        for sel_iter in om_utility.get_iter(om2.MItSelectionList(vert_sel_list)):
            dag_path, obj = sel_iter.getComponent()

            mesh_fn = om2.MFnMesh(dag_path)

            normal_locked_list = self.__get_normal_locked_list(mesh_fn)

            for vert_iter in om_utility.get_iter(om2.MItMeshVertex(dag_path, obj)):

                is_locked = normal_locked_list[vert_iter.index()]

                if not is_locked_vtx_only or is_locked:

                    path = dag_path.fullPathName()

                    if path not in list(info_dict.keys()):
                        info_dict[path] = []

                    info_dict[path].append(VertexNormalInfo.create(vert_iter, is_locked))

        self.info_list = [ObjectNormalInfo(*item) for item in list(info_dict.items())]

    def get_pair_list_by_name(self, src_info):
        """オブジェクト名が一致する法線情報のペアを返す

        与えられたリストと自身のinfo_listを比較し、オブジェクト名が一致するObjectNormalInfo同士をペアにして返す

        Args:
            src_info (NormalInfo): 対象の法線情報

        Returns:
            list[tuple[ObjectNormalInfo, ObjectNormalInfo]]: オブジェクト名が一致する法線情報のペアのリスト
        """

        if not src_info:
            return

        if not src_info.info_list:
            return

        if not self.info_list:
            return

        if len(src_info.info_list) == 1 and len(self.info_list) == 1:
            return [(src_info.info_list[0], self.info_list[0])]

        info_item_pair_list = []

        for dst_obj_info in self.info_list:
            for src_obj_info in src_info.info_list:
                if src_obj_info.name == dst_obj_info.name:
                    info_item_pair_list.append((src_obj_info, dst_obj_info))
                    break

        return info_item_pair_list

    def __get_normal_locked_list(self, mesh_fn):
        """頂点ごとのノーマルのロック状態リストを返す

        OpenMaya.MItMeshVertex.getNormalIndicesが不安定なため実装

        Attributes:
            mesh_fn (OpenMaya.MFnMesh): メッシュデータ

        Returns:
            list[bool]: ノーマルのロック状態リスト
        """

        vertex_ids = mesh_fn.getVertices()
        normal_ids = mesh_fn.getNormalIds()

        get_vertex_id = operator.itemgetter(0)
        normal_id_pairs_by_vertex_id = itertools.groupby(sorted(zip(vertex_ids[1], normal_ids[1]), key=get_vertex_id), key=get_vertex_id)
        normal_ids_list = ({normal_id_pair[1] for normal_id_pair in normal_id_pairs} for _, normal_id_pairs in normal_id_pairs_by_vertex_id)
        normal_locked_list = [any(mesh_fn.isNormalLocked(normal_id) for normal_id in normal_ids) for normal_ids in normal_ids_list]

        return normal_locked_list


class ObjectNormalInfo(object):
    """オブジェクトごとの法線情報クラス

    Attributes:
        dag_path (OpenMaya.MDagPath): オブジェクトのDAGパス
        name (str): オブジェクト名
        info_list (list[VertexNormalInfo]): 頂点ごとの法線情報リスト
    """

    def __init__(self, dag_path, info_list):

        self.dag_path = dag_path
        self.name = dag_path.split('|')[-1]
        self.info_list = info_list

    def __str__(self):

        return 'dag_path: {}, info_list: {}'.format(
            self.dag_path,
            *self.info_list
        )

    def copy(self, info_list=None):
        """データを複製したObjectNormalInfoのインスタンスを返す

        info_listを指定した場合は頂点ごとの法線情報リストを置き換える

        Args:
            info_list (list[VertexNormalInfo], optional): 頂点ごとの法線情報リスト

        Returns:
            ObjectNormalInfo: データを複製したインスタンス
        """

        return ObjectNormalInfo(self.dag_path, info_list if info_list is not None else self.info_list[:])

    def update(self, info_list):
        """頂点ごとの法線情報リストを更新する

        Args:
            info_list (list[VertexNormalInfo]): 頂点ごとの法線情報リスト
        """

        self.info_list = [dst.update(src) for src, dst in zip(info_list, self.info_list)]

    def get_command_arguments(self):
        """
        コマンドの引数として渡せるように変換した情報を返す

        Returns:
            (str, list[int], list[int], list[OpenMaya.MVector]): メッシュ, 頂点ID, フェースID, 法線のタプル
        """

        if not self.info_list:
            return None

        sel_list = om2.MGlobal.getSelectionListByName(self.dag_path)

        if sel_list.isEmpty():
            return None

        vertex_ids = []
        face_ids = []
        normals = []

        for vert_info in self.info_list:
            for face_info in vert_info.info_list:
                vertex_ids.append(vert_info.index)
                face_ids.append(face_info.index)
                normals.append(face_info.normal)

        return self.dag_path, vertex_ids, face_ids, normals


class VertexNormalInfo(object):
    """頂点ごとの法線情報クラス

    Attributes:
        index (int): 頂点番号
        world_position (OpenMaya.MPoint): ワールド空間の頂点位置
        local_position (OpenMaya.MPoint): オブジェクト空間の頂点位置
        info_list (list[VertexFaceNormalInfo]): 頂点フェースごとの法線情報リスト
        is_locked (bool): 法線のロック状態
    """

    def __init__(self, index, world_position, local_position, info_list, is_locked):

        self.index = index
        self.world_position = world_position
        self.local_position = local_position
        self.info_list = info_list
        self.is_locked = is_locked

    def __str__(self):

        return 'index: {}, world_position: {}, local_position: {}, info_list: {}'.format(
            self.index,
            self.world_position,
            self.local_position,
            self.info_list
        )

    def mirror(self, mirror_index, mirror_normal):
        """指定軸で反転した頂点法線情報を返す

        Args:
            mirror_index (int): 反転する軸 (x: 0, y: 1, z: 2)
            mirror_normal (bool): 法線も反転するか

        Returns:
            VertexNormalInfo: 反転した頂点法線情報
        """

        world_position = om2.MPoint(self.world_position)
        local_position = om2.MPoint(self.local_position)

        info_list = self.info_list[:]

        if mirror_index is not None:
            world_position[mirror_index] *= -1
            local_position[mirror_index] *= -1

            if mirror_normal:
                info_list = [face_info.mirror(mirror_index) for face_info in info_list]

        return VertexNormalInfo(self.index, world_position, local_position, info_list, self.is_locked)

    def update(self, vert_info):
        """頂点フェース法線情報リストを更新した新しいインスタンスを返す

        Args:
            vert_info (VertexNormalInfo): 更新する頂点法線情報

        Returns:
            VertexNormalInfo: 頂点フェース法線情報リストを更新した新しいインスタンス
        """

        info_list = []

        src_len = len(vert_info.info_list)

        for i, dst_face_info in enumerate(self.info_list):
            src_face_info = vert_info.info_list[min(i, src_len - 1)]
            info_list.append(VertexFaceNormalInfo(dst_face_info.index, om2.MVector(src_face_info.normal)))

        return VertexNormalInfo(self.index, self.world_position, self.local_position, info_list, self.is_locked)

    def is_every_normal_same(self):
        """すべての頂点フェース法線が同一かを返す

        Returns:
            bool: すべての頂点フェース法線が同一か
        """

        if not self.info_list:
            return False

        first_normal = self.info_list[0].normal

        return all(info.normal.isEquivalent(first_normal, tolerance=0.001) for info in self.info_list[1:])

    @classmethod
    def create(cls, vert_iter, is_locked):
        """法線情報を作成する

        Args:
            vert_iter (OpenMaya.MItMeshVertex): 頂点イテレータ
            mesh_fn (OpenMaya.MFnMesh): メッシュデータ
            is_locked (bool): 法線のロック状態

        Returns:
            VertexNormalInfo: 頂点法線情報
        """

        index = vert_iter.index()
        world_position = vert_iter.position(om2.MSpace.kWorld)
        local_position = vert_iter.position(om2.MSpace.kObject)
        info_list = [VertexFaceNormalInfo(i, vert_iter.getNormal(i, om2.MSpace.kObject)) for i in sorted(vert_iter.getConnectedFaces())]

        return cls(index, world_position, local_position, info_list, is_locked)


class VertexFaceNormalInfo(object):
    """頂点フェースごとの法線情報クラス

    Attributes:
        index (int): フェース番号
        normal (OpenMaya.MVector): 法線
    """

    def __init__(self, index, normal):

        self.index = index
        self.normal = normal

    def __str__(self):

        return 'index: {}, normal: {}'.format(
            self.index,
            self.normal
        )

    def mirror(self, mirror_index):
        """指定軸で反転した頂点法線情報を返す

        Args:
            mirror_index (int): 反転する軸 (x: 0, y: 1, z: 2)

        Returns:
            VertexFaceNormalInfo: 反転した頂点フェース法線情報
        """

        normal = om2.MVector(self.normal)

        normal[mirror_index] *= -1

        return VertexFaceNormalInfo(self.index, normal)
