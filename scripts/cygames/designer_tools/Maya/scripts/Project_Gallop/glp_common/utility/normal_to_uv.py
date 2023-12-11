# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from importlib import reload
except Exception:
    pass

import maya.api.OpenMaya as om2

from . import open_maya as om_utility
from ..classes import normal_info as normal_info_classes

reload(om_utility)
reload(normal_info_classes)


def transfer_normal_to_uvset(src_transform, dst_transform, xy_uvset, zw_uvset):
    src_mesh_fn = om_utility.get_mfn_mesh(src_transform)
    dst_mesh_fn = om_utility.get_mfn_mesh(dst_transform)

    if src_mesh_fn is None or dst_mesh_fn is None:
        return

    dst_uv_set_names = dst_mesh_fn.getUVSetNames()

    # UV3の存在チェック
    uv_set_3 = None

    if len(dst_uv_set_names) >= 3:
        uv_set_3 = dst_uv_set_names[2]

    # 転送用UVSetの作成
    if xy_uvset not in dst_uv_set_names:
        dst_mesh_fn.createUVSet(xy_uvset)

    if zw_uvset not in dst_uv_set_names:
        dst_mesh_fn.createUVSet(zw_uvset)

    src_normal_info = normal_info_classes.NormalInfo()
    src_normal_info.create_info(om_utility.get_m_selection_list(src_transform), False)

    dst_normal_info = normal_info_classes.NormalInfo()
    dst_normal_info.create_info(om_utility.get_m_selection_list(dst_transform), False)

    # UVをマージする頂点の取得
    # フェース頂点の法線がすべて同じ場合は頂点に対してUVは1つとする
    src_merge_indices = {info.index for info in src_normal_info.info_list[0].info_list if info.is_every_normal_same()}
    dst_merge_indices = {info.index for info in dst_normal_info.info_list[0].info_list if info.is_every_normal_same()}
    merge_indices = src_merge_indices & dst_merge_indices

    face_iter = om2.MItMeshPolygon(om_utility.get_m_dag_path(dst_transform))
    # フェースごとの頂点番号
    vertices_by_faces = [list(face.getVertices()) for face in om_utility.get_iter(face_iter)]
    # フェースごとの頂点数。assignUVsにも使用する
    vertex_counts = [len(vertices) for vertices in vertices_by_faces]

    normal_values = []
    uv_ids_by_faces = [[None] * vertex_count for vertex_count in vertex_counts]

    for vert_info in src_normal_info.info_list[0].info_list:
        if vert_info.index in merge_indices:
            # 法線を1つ登録し、同じIDを指定する
            normal_values.append(vert_info.info_list[0].normal)
            for vertface_info in vert_info.info_list:
                face_index = vertface_info.index
                vert_index = vertices_by_faces[face_index].index(vert_info.index)
                uv_ids_by_faces[face_index][vert_index] = len(normal_values) - 1
        else:
            # フェースごとに法線の登録、ID指定を行う
            for vertface_info in vert_info.info_list:
                normal_values.append(vertface_info.normal)
                face_index = vertface_info.index
                vert_index = vertices_by_faces[face_index].index(vert_info.index)
                uv_ids_by_faces[face_index][vert_index] = len(normal_values) - 1

    normal_count = len(normal_values)
    # 法線を要素ごとの配列に展開
    x_values, y_values, z_values = (list(v) for v in zip(*normal_values))
    # 2つ目の法線用UVSetのVは1固定
    w_values = [1] * normal_count

    if uv_set_3 is not None:
        # 3番目のUVSetのuvを2ずつ移動
        u_values, v_values = dst_mesh_fn.getUVs(uv_set_3)
        u_values = [u_value + 2 for u_value in u_values]
        v_values = [v_value + 2 for v_value in v_values]
        dst_mesh_fn.setUVs(u_values, v_values, uv_set_3)
        dst_mesh_fn.assignUVs(*dst_mesh_fn.getAssignedUVs(uv_set_3), uvSet=uv_set_3)

        # 3番目のUVSetのuvを法線用のUVSetに追加
        x_values.extend(u_values)
        y_values.extend(v_values)
        z_values.extend(u_values)
        w_values.extend(v_values)

        face_iter.reset()
        for face in om_utility.get_iter(face_iter):
            if not face.hasUVs(uv_set_3):
                continue
            face_index = face.index()
            for i in range(face.polygonVertexCount()):
                # 法線分のUVID数をオフセットして設定
                uv_ids_by_faces[face_index][i] = face.getUVIndex(i, uv_set_3) + normal_count

    # フェースごとのUVIDを平坦化
    uv_ids = [uv_id for uv_ids in uv_ids_by_faces for uv_id in uv_ids]

    dst_mesh_fn.clearUVs(xy_uvset)
    dst_mesh_fn.setUVs(x_values, y_values, xy_uvset)
    dst_mesh_fn.assignUVs(vertex_counts, uv_ids, xy_uvset)

    dst_mesh_fn.clearUVs(zw_uvset)
    dst_mesh_fn.setUVs(z_values, w_values, zw_uvset)
    dst_mesh_fn.assignUVs(vertex_counts, uv_ids, zw_uvset)
