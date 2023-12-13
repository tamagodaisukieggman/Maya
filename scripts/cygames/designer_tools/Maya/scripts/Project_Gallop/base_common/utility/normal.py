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

import maya.cmds as cmds
import maya.api.OpenMaya as om

from ..classes import vertex as vertex_data

reload(vertex_data)


def copy_normal(from_vtx_datas, to_vtx_datas, keep_edge_state=True, from_lock_only=False, to_lock_only=False):
    """法線をコピー

    Args:
        from_vtx_datas ([base_common.classes.vertex.VtxData]): コピー元のVtxDataリスト
        to_vtx_datas ([base_common.classes.vertex.VtxData]): コピー先のVtxDataリスト
        keep_edge_state (bool, optional): エッジのハードorソフトを維持する. Defaults to True.
        from_lock_only (bool, optional): ロックされている法線からのみコピー. Defaults to False.
        to_lock_only (bool, optional): ロックされている法線に対してのみコピー. Defaults to False.
    """

    apply_face_vtx_datas = []
    apply_normals = []

    for from_vtx_data, to_vtx_data in zip(from_vtx_datas, to_vtx_datas):

        if not from_vtx_data or not to_vtx_data:
            continue
        if not from_vtx_data.face_vtx_datas or not to_vtx_data.face_vtx_datas:
            continue

        for to_face_vtx_data in to_vtx_data.face_vtx_datas:

            if to_lock_only and not to_face_vtx_data.is_locked():
                continue

            target_face_vtx_data = __get_best_face_nomrmal_match_face_vtx_data(to_face_vtx_data, from_vtx_data.face_vtx_datas)

            if from_lock_only and not target_face_vtx_data.is_locked():
                continue

            apply_face_vtx_datas.append(to_face_vtx_data)
            apply_normals.append(target_face_vtx_data.face_vtx_normal)

    set_face_vtx_normal(apply_face_vtx_datas, apply_normals, keep_edge_state)


def set_face_vtx_normal(face_vtx_datas, normals, keep_edge_state=True):
    """フェース頂点法線をセット

    Args:
        face_vtx_datas ([base_common.classes.vertex.FaceVtxData]): フェース頂点のリスト
        normals ([om.MVector]): 法線のリスト
        keep_edge_state (bool, optional): エッジ状態を維持するか. Defaults to True.
    """

    set_queue_dict = {}

    if len(face_vtx_datas) != len(normals):
        cmds.warning('フェイス頂点数とセットする法線の数があっていません')

    # transformごとに実行用辞書を作成
    for face_vtx_data, normal in zip(face_vtx_datas, normals):

        if not face_vtx_data or not normal:
            continue

        this_queue = None
        if face_vtx_data.transform not in set_queue_dict:
            this_queue = {
                'om_mesh': face_vtx_data.om_mesh,
                'faces': [face_vtx_data.face_index],
                'vtxs': [face_vtx_data.vtx_index],
                'normals': [normal]
            }
            set_queue_dict[face_vtx_data.transform] = this_queue
        else:
            this_queue = set_queue_dict[face_vtx_data.transform]
            this_queue['faces'].append(face_vtx_data.face_index)
            this_queue['vtxs'].append(face_vtx_data.vtx_index)
            this_queue['normals'].append(normal)

    # 法線ペーストの実行
    for transform_key in set_queue_dict:

        if not cmds.objExists(transform_key):
            cmds.warning('トランスフォームが存在しません: {}'.format(transform_key))

        queue = set_queue_dict[transform_key]

        # エッジ情報の保持
        org_edge_indexes = []
        org_edge_smoothes = []

        if keep_edge_state:
            dag_path = queue['om_mesh'].dagPath()
            om_edge_itr = om.MItMeshEdge(dag_path)

            while not om_edge_itr.isDone():
                org_edge_indexes.append(om_edge_itr.index())
                org_edge_smoothes.append(om_edge_itr.isSmooth)
                om_edge_itr.next()

        # 法線をセット
        queue['om_mesh'].setFaceVertexNormals(queue['normals'], queue['faces'], queue['vtxs'])

        # エッジ情報の復元
        if org_edge_indexes:
            queue['om_mesh'].setEdgeSmoothings(org_edge_indexes, org_edge_smoothes)
            queue['om_mesh'].cleanupEdgeSmoothing()

        # メッシュ描画更新
        queue['om_mesh'].updateSurface()


def __get_best_face_nomrmal_match_face_vtx_data(face_vtx_data, search_from_face_vtx_datas):
    """隣接フェースの法線が一番近いフェース頂点データを取得

    Args:
        vtx_data (FaceVtxData): 検索するFaceVtxData
        search_from_vtx_datas ([FaceVtxData]): 検索されるFaceVtxDataリスト

    Returns:
        FaceVtxData: 隣接フェースの法線が一番近いFaceVtxData
    """

    if len(search_from_face_vtx_datas) == 1:
        return search_from_face_vtx_datas[0]

    max_dot_value = None
    bast_match_data = None

    for search_from_data in search_from_face_vtx_datas:
        this_face_normal = search_from_data.face_normal

        if max_dot_value is None or face_vtx_data.face_normal * this_face_normal >= max_dot_value:
            max_dot_value = face_vtx_data.face_normal * this_face_normal
            bast_match_data = search_from_data

    return bast_match_data

