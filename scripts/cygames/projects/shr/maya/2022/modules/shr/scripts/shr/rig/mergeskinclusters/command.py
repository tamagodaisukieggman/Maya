# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import re
import maya.cmds as cmds
import maya.api.OpenMaya as om

import mtk.rig.skinweight.command as skinweight
from mtk.utils.decoration.selections import keep_selections


def get_utcnow(format_str='%Y-%m-%d %H:%M:%S'):
    """現在のutcを取得
    :param str format_str: strftimeフォーマットテキスト
    :return: 現在のutc
    :rtype: str
    """

    return datetime.datetime.utcnow().strftime(format_str)


def reformat_component_strings(components):
    """コンポーネントのリフォーマット
    :param list components:
    :return: リフォーマットしたコンポーネントリスト
    :rtype: list
    """

    if not components:
        return []

    try:
        sel_list = om.MSelectionList()
        [sel_list.add(comp) for comp in components]
        return sel_list.getSelectionStrings()

    except Exception as e:
        cmds.warning(str(e))
        return []


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    v = str(value)
    if force:
        cmds.optionVar(sv=[key, v])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, v])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


def get_object_namespace(node):
    u"""ノード名からネームスペースを取得

    :param str node: ノード名
    :return: ネームスペース名
    :rtype: str
    """

    node = node.rsplit('|', 1)[-1].split('.')[0]
    p = node.rfind(':')

    if p >= 0:
        return ':%s' % node[:p]
    else:
        return ':'


def get_object_name(object_name):
    """ノード名からオブジェクト名(ネームスペース無しのノード名)を取得

    get_object_name の ノード名重複対応版

    :param str object_name: ノード名
    :return: オブジェクト名
    :rtype: str
    """

    namespace = get_object_namespace(object_name).strip(':')
    return re.sub(':+', ':', '|'.join([
        p.replace(namespace, '', 1).strip(':') for p in object_name.split('|') if p
    ])).strip('|').split('.')[0]


def list_related_blendShape(nodes):
    """接続されているblendShapeノードを取得
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

    return cmds.ls(history, typ='blendShape') or []


def get_merge_data_from_blendshape_weight(blendshape):
    """ブレンドシェイプからスキンクラスタ結合用のメンバーシップデータを取得
    |メンバーかどうかの判断はtargetWeight(Vertex)で判断する
    :param str blendshape:
    :return: スキンクラスタ結合用のデータ {'tg_name': [comp, comp, ...]}
    :rtype: dict
    """

    if not cmds.objectType(blendshape, i='blendShape'):
        cmds.error(u'ブレンドシェイプノードを指定して下さい。')
        return

    ret = {}

    shape = cmds.blendShape(blendshape, q=True, geometry=True)[0]
    node = cmds.listRelatives(shape, p=True, pa=True)[0]
    num_components = skinweight.get_component_count(['{}.cp[*]'.format(node)])

    tgs = cmds.blendShape(blendshape, q=True, target=True)
    for i, tg in enumerate(tgs):
        weights = cmds.getAttr('{}.inputTarget[0].inputTargetGroup[{}].targetWeights[0:{}]'.format(
            blendshape, i, num_components - 1
        ))
        ret[tg] = reformat_component_strings(
            ['{}.cp[{}]'.format(node, vid) for vid in range(num_components) if round(weights[vid], 0)]
        )

    return ret


def duplicate_influences(joints, prefix='', suffix='_copy'):
    """world空間にインフルエンスの複製を作る
    :param list joints: 複製対象のジョイント
    :param str prefix: 複製対象のノード名のプレフィックス
    :param str suffix: 複製対象のノード名のサフィックス
    :return: 複製インフルエンスのリスト
    :rtype: list
    """

    if not joints:
        return []

    influences = []
    for jt in joints:
        dup = cmds.createNode('joint', n='{}{}{}'.format(prefix, get_object_name(jt), suffix), ss=True)
        cmds.xform(dup, ws=True, m=cmds.xform(jt, q=True, ws=True, m=True))
        cmds.parentConstraint(jt, dup, weight=1, mo=True)
        cmds.scaleConstraint(jt, dup, weight=1, mo=True)
        influences.append(dup)

    return influences


@keep_selections
def merge_skincluster(node, components, targets, duplicate_joints=False):
    """複数ジオメトリのウェイトを結合
    :param str node: 結合先ノード名
    :param list components: target毎のウェイト転送先コンポーネント
    :param list targets: 結合元のスキニングされたジオメトリのリスト
    :param bool duplicate_joints: インフルエンスを複製するか、直接利用するかのブール値
    """

    bind_influences = []
    for tg in targets:
        clst = skinweight.list_related_skinClusters(tg)
        if not clst:
            continue

        influences = skinweight.list_influences(clst[0], long_name=False)[1]
        if not influences:
            continue

        bind_influences += influences

    if not bind_influences:
        return

    if duplicate_joints:
        bind_influences = duplicate_influences(sorted(set(bind_influences[:]), key=bind_influences.index))

        gp = cmds.createNode('transform', n='{}_influenceGp'.format(get_object_name(node)), ss=True)
        cmds.parent(bind_influences, gp)

    dst_clst = skinweight.list_related_skinClusters(node)
    if dst_clst:
        skinweight.add_influences([node], bind_influences)
    else:
        dst_clst = cmds.skinCluster(
            bind_influences,
            node,
            toSelectedBones=True,
            bindMethod=0,
            normalizeWeights=True,
            weightDistribution=0,
            maximumInfluences=4,
            obeyMaxInfluences=False,
            dropoffRate=4,
            removeUnusedInfluence=False,
            name='{}_skinCluster'.format(node.replace('|', '__'))
        )[0]

    for tg, dst_comps in zip(targets, components):
        cmds.select([tg] + dst_comps, r=True)
        cmds.copySkinWeights(
            noMirror=True,
            influenceAssociation=('label', 'oneToOne', 'closestJoint'),
            surfaceAssociation='closestPoint',
            noBlendWeight=True,
            normalize=True)

    # 不要インフルエンスを除外
    remove_infls = skinweight.remove_unused_influences(dst_clst)
    if duplicate_joints and remove_infls:
        cmds.delete(remove_infls)

    if duplicate_joints:
        return node, gp

    else:
        return node, ''


def get_nearest_verticies(geometry=None, points=None, space=om.MSpace.kWorld, as_index=True):
    """近傍頂点を取得
    :param str geometry: 頂点取得ジオメトリ
    :param list points: 頂点位置のリスト
    :param MSpace space: 頂点座標取得スペース
    :param bool as_index: True: 頂点番号、False: 頂点座標を返す
    :return: 頂点番号、または、頂点座標のリスト
    :rtype: list
    """

    if not geometry or not points:
        return

    dagpath = om.MGlobal.getSelectionListByName(geometry).getDagPath(0)
    mesh_fn = om.MFnMesh(dagpath)

    ret = []
    for point in points:
        in_point = om.MPoint(point)
        out_point, face_index = mesh_fn.getClosestPoint(in_point, space=space)
        vids = mesh_fn.getPolygonVertices(face_index)
        dist = None
        nearest = None
        for vid in vids:
            v_point = mesh_fn.getPoint(vid, space=space)
            if dist is None:
                dist = in_point.distanceTo(v_point)
                nearest = vid if as_index else [v_point.x, v_point.y, v_point.z]
            else:
                diff = in_point.distanceTo(v_point)
                if dist > diff:
                    dist = diff
                    nearest = vid if as_index else [v_point.x, v_point.y, v_point.z]

        if nearest is not None:
            ret.append(nearest)

    return ret


def merge_skinclusters_by_separate_meshes(merge_geo, separate_geometries, duplicate_joints=False):
    """スキンクラスタの結合
    :param str merge_geo: skinCluster結合ターゲットジオメトリ
    :param list separate_geometries: 分割ジオメトリ
    :param bool duplicate_joints: インフルエンスを複製するか、直接利用するかのブール値
    """

    components = []
    for separate_geo in separate_geometries:
        flat_points = cmds.xform('{}.vtx[*]'.format(separate_geo), q=True, ws=True, t=True)
        points = []
        for px, py, pz in zip(flat_points[0::3], flat_points[1::3], flat_points[2::3]):
            points.append([px, py, pz])

        vids = get_nearest_verticies(merge_geo, points)
        if not vids:
            continue

        components.append(['{}.vtx[{}]'.format(merge_geo, vid) for vid in vids])

    return merge_skincluster(
        merge_geo,
        components,
        separate_geometries,
        duplicate_joints=duplicate_joints
    )
