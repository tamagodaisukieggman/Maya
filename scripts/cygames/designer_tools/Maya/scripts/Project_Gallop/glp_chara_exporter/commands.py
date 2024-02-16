# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re

import maya.cmds as cmds
import maya.api.OpenMaya as om2

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility
from ..glp_common.utility import open_maya as om_utility

from . import constants

try:
    # maya 2022-
    from importlib import reload
except Exception:
    pass

reload(base_common)
reload(base_class)
reload(base_utility)
reload(constants)

export_log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'export_log.txt'))


def output_log_file(logger):

    logger.output_log(export_log_file_path)
    base_utility.io.open_notepad(export_log_file_path)


def duplicate_with_suffix(node, suffix, check_world=False):
    """指定したサフィックスをつけてノードを複製する

    Args:
        node (str): 複製するノード
        suffix (str): ノード名に付けるサフィックス
        check_world (bool): 複製先オブジェクトの存在確認をワールド直下に限定する

    Returns:
        str: 複製されたノード
    """

    if not cmds.objExists(node):
        return None

    duplicate_node = base_utility.name.get_short_name(node) + suffix

    world_duplicate_node = '|{}'.format(duplicate_node)

    check_node = world_duplicate_node if check_world else duplicate_node

    if not base_utility.node.exists(check_node):
        duplicated_node = base_utility.node.duplicate(node, duplicate_node)
        world_duplicated_nodes = cmds.parent(duplicated_node, w=True)
        return base_utility.name.get_long_name(world_duplicated_nodes[0])

    return base_utility.name.get_long_name(duplicate_node)


def create_deformed_mesh(mesh, body_shape):
    """ブレンドシェイプを適用したメッシュを作成する

    Args:
        mesh (str): 作成元のメッシュ
        body_shape (BodyShape): 適用する体型差分

    Returns:
        str: ブレンドシェイプを適用したメッシュ
    """

    if not cmds.objExists(mesh):
        return None

    base_mesh = duplicate_with_suffix(mesh, constants.BLENDSHAPE_SUFFIX)

    target_meshes = []
    weights = []

    for i, (target, weight) in enumerate(body_shape.targets.items()):
        target_mesh = duplicate_with_suffix(mesh, target)
        target_meshes.append(target_mesh)
        weights.append((i, weight))

    blendshape_meshes = target_meshes[:]
    blendshape_meshes.append(base_mesh)

    blendshape = cmds.blendShape(blendshape_meshes, parallel=True)

    cmds.blendShape(blendshape, e=True, w=weights)

    return base_mesh


def transfer_vertex_position(src_mesh, dst_mesh):
    """頂点位置をコピーする

    Args:
        src_mesh (str): コピー元のメッシュ
        dst_mesh (str): コピー先のメッシュ
    """

    if not src_mesh or not cmds.objExists(src_mesh):
        return None

    if not dst_mesh or not cmds.objExists(dst_mesh):
        return None

    temp_mesh = base_utility.node.duplicate(src_mesh)

    src_vtx = base_class.mesh.vertex_position_info.VertexPositionInfo()
    src_vtx.create_info([temp_mesh])

    dst_vtx = base_class.mesh.vertex_position_info.VertexPositionInfo()
    dst_vtx.create_info([dst_mesh])

    base_utility.mesh.vertex_position.paste_position_by_vertex_index(src_vtx, dst_vtx)

    cmds.delete(temp_mesh)


def get_target_root_locator(mesh, target):
    """指定したメッシュとターゲット名からルートロケーターを取得する

    Args:
        mesh (str): 元のメッシュ
        target (str): ターゲット（サフィックス）名

    Returns:
        str: ルートロケーター名
    """

    target_mesh = base_utility.name.get_short_name(mesh) + target

    if not cmds.objExists(target_mesh):
        return None

    parents = cmds.listRelatives(target_mesh, p=True, f=True)

    if not parents:
        return None

    root_locator = '{}|{}'.format(parents[0], constants.ROOT_LOCATOR_NAME)

    if not cmds.objExists(root_locator):
        return None

    return root_locator


def get_relative_transforms(node):
    """指定したノード以下のtransformノードを取得する

    Args:
        node (str): 元のノード名

    Returns:
        list[str]: 指定したノード以下のtransformのリスト
    """

    if node is None:
        return []

    relatives = cmds.listRelatives(node, ad=True, f=True, typ='transform') or []

    joints = [node] + relatives
    joints.sort()

    return joints


def get_transform(node):
    """指定したノードのtransformの値を取得する

    Args:
        node (str): 元のノード名

    Returns:
        tuple[list[float], list[float], list[float]]: 指定したノードのtransformの値
    """

    translation = cmds.xform(node, q=True, ws=True, t=True)
    rotation = cmds.xform(node, q=True, ws=True, ro=True)
    scale = cmds.xform(node, q=True, ws=True, s=True)

    return (translation, rotation, scale)


def get_transforms(root):
    """指定したノード以下のtransformの値を取得する

    ルート以下のノードから、ショートネームをキーとするtransformの値の辞書を取得する

    Args:
        root (str): ルートノード名

    Returns:
        dict[str, tuple[list[float], list[float], list[float]]]: ノードのショートネームをキー、transformを値とした辞書
    """

    nodes = get_relative_transforms(root)

    return {node.split('|')[-1]: get_transform(node) for node in nodes}


def set_transforms(root, transforms):
    """指定したノード以下にtransformの値をセットする

    ルート以下のノードに対し、ショートネームをキーとしてtransformの値の辞書から取得した値をセットする

    Args:
        root (str): ルートノード名
        transforms (dict[str, tuple[list[float], list[float], list[float]]]): セットするtransformの値の辞書
    """

    nodes = get_relative_transforms(root)

    for node in nodes:
        transform = transforms.get(node.split('|')[-1])

        if not transform:
            continue

        translation, _, _ = transform

        cmds.xform(node, ws=True, t=translation)


def get_orientations(root):
    """指定したノード以下のジョイントのオリエントの値を取得する

    Args:
        root (str): ルートノード名

    Returns:
        dict[str, tuple[list[float]]]: ジョイントのショートネームをキー、オリエントを値とした辞書
    """

    nodes = get_relative_transforms(root)

    return {node.split('|')[-1]: (cmds.joint(node, q=True, o=True),) for node in nodes if cmds.joint(ex=node)}


def set_orientations(root, orientations):
    """指定したノード以下のジョイントにオリエントの値をセットする

    Args:
        root (str): ルートノード名
        orientations (dict[str, tuple[list[float]]]): セットするジョイントオリエントの値の辞書
    """

    nodes = get_relative_transforms(root)

    for node in nodes:
        orientation = orientations.get(node.split('|')[-1])

        if not orientation:
            continue

        # タプル解除
        orientation, = orientation

        cmds.joint(node, e=True, o=orientation)


def blend_vector(vector, base, target, weight):
    """vectorをブレンドする

    baseとtargetの差にweightを掛けた値を元のvectorに追加する

    Args:
        vector (list[float]): 追加元のvector
        base (list[float]): 差の基準vector
        target (list[float]): ターゲットvector
        weight (float): ブレンドするウェイト

    Returns:
        list[float]: ブレンドしたvector
    """

    diff = base_utility.vector.sub(target, base)
    addend = base_utility.vector.multiply_value(diff, weight)
    return base_utility.vector.add(vector, addend)


def blend_vectors(base_dict, target_dict_and_weights):
    """vectorの辞書同士をブレンドする

    Args:
        base_dict (dict[str, tuple[list[float], list[float], list[float]]]): 追加元のvectorの辞書
        target_dict_and_weights (tuple[dict[str, tuple[list[float], list[float], list[float]]], float]): ブレンドするvectorの辞書とウェイト

    Returns:
        dict[str, tuple[list[float], list[float], list[float]]]: ブレンドしたvectorの辞書
    """

    blend_vectors = {}

    for key, base_vectors in base_dict.items():
        vectors = tuple(base_utility.vector.clone(vector) for vector in base_vectors)

        for target_dict, weight in target_dict_and_weights:
            target_vectors = target_dict.get(key)

            if not target_vectors:
                continue

            vectors = tuple(blend_vector(vector, base, target, weight) for vector, base, target in zip(vectors, base_vectors, target_vectors))

        blend_vectors[key] = vectors

    return blend_vectors


def create_target_joints(base_root, mesh, targets):
    """ターゲットごとのジョイントを作成（複製）する

    Args:
        base_root (str): シーンにターゲットが存在しない場合に使用するルートノード
        mesh (str): メッシュ名
        targets (list[str]): ターゲットのリスト

    Returns:
        dict[str, str]: ターゲット名をキー、作成（複製）されたジョイントのルートノードを値とする辞書
    """

    target_roots = {}

    for target in targets:
        target_root = get_target_root_locator(mesh, target) or base_root
        duplicated_target_root = duplicate_with_suffix(target_root, target)

        target_roots[target] = duplicated_target_root

    return target_roots


def bind_and_copy_weight(src_mesh, dst_mesh):
    """メッシュのバインドとウェイト値のコピーを行う

    コピー元メッシュと同じジョイントにコピー先メッシュをバインドし、元のメッシュからウェイト値をコピーする

    Args:
        src_mesh (str): コピー元メッシュ名
        dst_mesh (str): コピー先メッシュ名
    """

    if not src_mesh or not cmds.objExists(src_mesh):
        return

    if not dst_mesh or not cmds.objExists(dst_mesh):
        return

    src_skin_cluster = om_utility.get_mfn_skin_cluster(src_mesh)

    if src_skin_cluster is None:
        return

    influences = src_skin_cluster.influenceObjects()

    joints = [influence.fullPathName() for influence in influences if influence.apiType() == om2.MFn.kJoint]

    if not joints:
        return
    
    influence_indices = om2.MIntArray([src_skin_cluster.indexForInfluenceObject(influence) for influence in influences])

    src_sel_list = om_utility.get_m_selection_list(src_mesh)
    src_vert_sel_list = om_utility.convert_to_vertex(src_sel_list)
    src_dag_path, src_obj = src_vert_sel_list.getComponent(0)

    weights = src_skin_cluster.getWeights(src_dag_path, src_obj, influence_indices)

    cmds.delete(dst_mesh, ch=True)
    cmds.skinCluster(dst_mesh, joints, omi=False, bm=0, mi=2, rui=False, sm=0)

    dst_skin_cluster = om_utility.get_mfn_skin_cluster(dst_mesh)

    if dst_skin_cluster is None:
        return

    dst_influences = dst_skin_cluster.influenceObjects()

    # srcとdstでインフルエンスは同じはずだが、インフルエンスインデックスが異なることがあるのでweightsに対応したdstのインフルエンスインデックスリストを作成
    paste_influence_indices = []
    for src_influence in influences:
        for dst_influence in dst_influences:
            if src_influence.fullPathName() == dst_influence.fullPathName():  # 元インフルエンスのjointでバインドしているので必ずあるはず
                paste_influence_indices.append(dst_skin_cluster.indexForInfluenceObject(dst_influence))
    paste_influence_indices = om2.MIntArray(paste_influence_indices)

    dst_sel_list = om_utility.get_m_selection_list(dst_mesh)
    dst_vert_sel_list = om_utility.convert_to_vertex(dst_sel_list)
    dst_dag_path, dst_obj = dst_vert_sel_list.getComponent(0)

    dst_skin_cluster.setWeights(dst_dag_path, dst_obj, paste_influence_indices, weights, False)


def get_mask_faces():
    """アイコン撮影用マスクのフェースリストを取得

    マスクセット内のフェースとそのアウトラインのフェースのリストを作成

    Returns:
        list: アイコン撮影用マスクのリスト
    """

    if cmds.objExists(constants.MMASK_SET_NAME):
        return cmds.ls(cmds.sets(constants.MMASK_SET_NAME, q=True), l=True, fl=True)
    else:
        return []


def get_obj_face_dict(org_faces):
    """メッシュとフェースリストの辞書を取得

    Args:
        org_faces (list): フェースリスト

    Returns:
        dict: {'メッシュ名': [フェースリスト],,,}
    """

    result_dict = {}

    if not org_faces:
        return result_dict

    for face in org_faces:

        obj = face.split('.f')[0]

        if obj in result_dict:
            result_dict[obj].append(face)
        else:
            result_dict[obj] = [face]

    return result_dict


def separate_mesh(target_obj, target_faces):
    """オブジェクトを指定した面で分割
    分割する際にヒストリーを削除しているためウェイトなどは事前に保存する必要がある

    Args:
        target_obj (str): 分割対象のオブジェクト
        target_faces (list): 切り分けたいフェースリスト

    Returns:
        list: [分割された元オブジェクト, 分割したオブジェクト]
    """

    nodes = []
    try:

        cmds.polyChipOff(target_faces, dup=False, ch=False)
        nodes = cmds.polySeparate(target_obj, rs=True, ch=True)
        cmds.delete(target_obj, ch=True)

    except Exception:

        # 全選択されてしまっているなど分割出来ない場合はエラーになるので元を返す
        return [target_obj, None]

    objs = nodes[:-1]
    base_obj = objs[-1]
    separate_objs = objs[:-1]

    separate_obj = None
    if len(separate_objs) == 1:
        separate_obj = separate_objs[0]
    else:
        unite_skin_objs = cmds.polyUnite(separate_objs)
        cmds.delete(unite_skin_objs, ch=True)
        separate_obj = unite_skin_objs[0]

    return [base_obj, separate_obj]


def get_mask_name(base_obj_name, is_material):
    """アイコンマスク用の名前を取得する

    Args:
        base_obj_name (str): 元になるオブジェクトの名前
        is_material (bool): マテリアルかどうか

    Returns:
        str: アイコンマスク用のオブジェクト名
    """

    search_str = ''

    if is_material:
        search_str = r'(^mtl)_'
    else:
        search_str = r'(M_[^_]+)'  # メッシュは'M_XXX'の後ろに接尾辞をつける

    m = re.search(search_str, base_obj_name)

    if not m:
        return base_obj_name
    else:
        return base_obj_name.replace(m.group(1), m.group(1) + constants.MMASK_SUFFIX)
