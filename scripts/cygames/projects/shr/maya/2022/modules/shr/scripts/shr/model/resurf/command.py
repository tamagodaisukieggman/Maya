# -*- coding: utf-8 -*-

from __future__ import absolute_import

from math import degrees

import maya.cmds as cmds
import maya.api.OpenMaya as om2


def list_related_skinClusters(nodes):
    """接続されているskinClusterノードを取得
    :param list/str nodes: ノードのリスト
    :return: skinClusterノードのリスト
    :rtype: list
    """

    if not nodes:
        return []

    shapes = cmds.listRelatives(nodes, s=True, ni=True, pa=True, type='controlPoint')
    if not shapes:
        shapes = cmds.ls(nodes, ni=True, type='controlPoint')
        if not shapes:
            return []

    history = cmds.listHistory(shapes, pdo=True)
    if not history:
        return []

    return cmds.ls(history, typ='skinCluster') or []


def get_component_weight(skincluster, component, joint, include_neighbours=False):
    """コンポーネントのウェイトを取得
    :param str skincluster: skinClusterノード
    :param str component: コンポーネント名
    :param str joint: インフルエンスジョイント
    :param bool include_neighbours: 隣接頂点のウェイトを含む
    :return: ウェイト値, include_neighboursがTrueの場合は隣接頂点のウェイトの平均値
    :rtype: float
    """

    if include_neighbours:
        comps = cmds.polyListComponentConversion(cmds.polyListComponentConversion(component, tf=True), tv=True)
        weights = [cmds.skinPercent(skincluster, comp, query=True, transform=joint) for comp in comps]
        return sum(weights) / len(comps)

    else:
        return cmds.skinPercent(skincluster, component, query=True, transform=joint)


def to_degrees(angles):
    """入力をデグリー角に変換
    :param list angles: ラジアン角
    :return: list [float, float, float]
    :rtype: list
     """

    return [degrees(x) for x in angles]


def get_dagpath(obj):
    """MDagPathを取得
    :param str obj: オブジェクト名
    :return: MDagPath
    :rtype: MDagPath
    """

    sel_list = om2.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0)


def get_nearest_point_data(pos=None, geometry=None):
    """
    :param MPoint pos:
    :param str geometry: ジオメトリ(mesh)
    :return: 近傍頂点の情報の辞書 {頂点番号、面番号、頂点位置、頂点法線、頂点接線}
    :rtype: dict
    """

    dag_path = get_dagpath(geometry)
    if dag_path.apiType() != om2.MFn.kMesh:
        dag_path.extendToShape()
        if dag_path.apiType() != om2.MFn.kMesh:
            return None

    mesh_fn = om2.MFnMesh(dag_path)

    # closest point
    pos = om2.MPoint(pos)
    c_pos, face_id = mesh_fn.getClosestPoint(pos)
    v_ids = mesh_fn.getPolygonVertices(face_id)

    # nearest vertex
    nearest_v_id = v_ids[0]
    dist = mesh_fn.getPoint(v_ids[0]).distanceTo(c_pos)
    for v_id in v_ids[1:]:
        tmp_dist = mesh_fn.getPoint(v_id).distanceTo(c_pos)
        if dist > tmp_dist:
            dist = tmp_dist
            nearest_v_id = v_id

    # normal, tangent
    v_pos = mesh_fn.getPoint(nearest_v_id)
    v_normal = mesh_fn.getVertexNormal(nearest_v_id, True)
    v_tangent = mesh_fn.getFaceVertexTangent(face_id, nearest_v_id)

    return {
        'vertex_id': nearest_v_id,
        'face_id': face_id,
        'position': v_pos,
        'normal': v_normal,
        'tangent': v_tangent
    }


def calc_rot(normal, tangent):
    """normal, tangentから角度を計算
    :param MVector normal: ノーマル
    :param MVector tangent: タンジェント
    :return: MQuaternion
    :rtype: MQuaternion
    """

    vx = normal.normalize()
    vy = tangent.normalize()
    vz = vx ^ vy

    rot_mat = om2.MMatrix([
        vx.x, vx.y, vx.z, 0.0,
        vy.x, vy.y, vy.z, 0.0,
        vz.x, vz.y, vz.z, 0.0,
        0.0, 0.0, 0.0, 1.0
    ])

    return om2.MTransformationMatrix(rot_mat).rotation(asQuaternion=True)


def reset_joints(joints, reset_translate=True, reset_rotate=True):
    """ジョイント位置をリセット
    :param list joints: ジョイント
    """

    for jt in joints:
        if reset_translate:
            for attr in ['tx', 'ty', 'tz']:
                cmds.setAttr('{}.{}'.format(jt, attr), cmds.getAttr('{}.{}InitVal'.format(jt, attr)))

        if reset_rotate:
            for attr in ['rx', 'ry', 'rz']:
                cmds.setAttr('{}.{}'.format(jt, attr), cmds.getAttr('{}.{}InitVal'.format(jt, attr)))


def fit_joints(
        joints,
        target_geometry,
        base_geometry,
        apply_translate=True,
        apply_rotate=False,
        correct_by_weights=True,
        skinned_geometry=None
):
    """
    :param list joints: ジョイント
    :param str target_geometry: ターゲットジオメトリ
    :param str base_geometry: ベースジオメトリ
    :param bool apply_translate: translate設定する
    :param bool apply_rotate: rotateを設定する(vertex-normal, vertex-tangentを利用した角度を使用)
    :param bool correct_by_weights: rotate設定でウェイト値による補正をするか
    :param str skinned_geometry: スキニングされたジオメトリ (correct_by-weightsオプションで使用)
    """

    if not joints:
        cmds.warning(u'移動させるジョイントを指定して下さい。')
        return

    if not cmds.objExists(target_geometry):
        cmds.warning(u'target_geometry (リサーフターゲット) を指定して下さい。')
        return

    if not cmds.objExists(base_geometry):
        cmds.warning(u'base_geometry (デフォルト形状ジオメトリ) を指定して下さい。')
        return

    for jt in joints:
        try:
            init_pos = [
                cmds.getAttr('{}.txInitVal'.format(jt)),
                cmds.getAttr('{}.tyInitVal'.format(jt)),
                cmds.getAttr('{}.tzInitVal'.format(jt))
            ]
            jt_pos = om2.MPoint(init_pos) * om2.MMatrix(cmds.getAttr('{}.pm'.format(jt)))

        except Exception as e:
            cmds.warning(str(e))
            jt_pos = cmds.xform(jt, q=True, ws=True, t=True)

        base_data = get_nearest_point_data(jt_pos, base_geometry)

        tg_pos = cmds.xform('{}.vtx[{}]'.format(target_geometry, base_data['vertex_id']), q=True, ws=True, t=True)

        if apply_translate:
            cmds.xform(jt, ws=True, t=tg_pos)
            cmds.xform(jt, ro=[0.0, 0.0, 0.0])

        if apply_rotate:
            weight = 1.0
            if correct_by_weights:
                skinned_geometry = skinned_geometry or ''
                if cmds.objExists(skinned_geometry):
                    skin_clusters = list_related_skinClusters([skinned_geometry])
                    if skin_clusters:
                        weight = get_component_weight(
                            skin_clusters[0],
                            '{}.vtx[{}]'.format(skinned_geometry, base_data['vertex_id']),
                            jt,
                            include_neighbours=True
                        )

            tg_daga = get_nearest_point_data(tg_pos, target_geometry)
            base_rot = calc_rot(base_data['normal'], base_data['tangent'])
            tg_rot = calc_rot(tg_daga['normal'], tg_daga['tangent'])

            diff_rot = tg_rot * base_rot.inverse()
            if weight < 1.0:
                diff_rot = om2.MQuaternion.slerp(om2.MQuaternion(), diff_rot, weight)

            diff_rot = to_degrees(diff_rot.asEulerRotation())
            cmds.xform(jt, ro=diff_rot)
