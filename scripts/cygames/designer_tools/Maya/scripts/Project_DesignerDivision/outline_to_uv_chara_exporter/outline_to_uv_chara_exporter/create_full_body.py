# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re

import maya.cmds as cmds

from ..base_common import classes as base_class
from ..base_common import utility as base_utility


# scene判定用パターン. idをグループにする.
HEAD_SCENE_PATTERN = 'chr([0-9]{4}_[0-9]{2})'
BODY_SCENE_PATTERN = 'bdy([0-9]{4}_[0-9]{2})'

# 各パーツのフォルダ名
HEAD_DIR = 'Head'
BODY_DIR = 'Body'

# このスクリプトでパーツの管理に用いるラベル
HEAD_PART_LABEL = 'head'
BODY_PART_LABEL = 'body'

# 一体化したモデルの接頭辞
FULL_BODY_PREFIX = 'mdl_chr'


def create_full_body_scene():
    """頭部or身体シーンから全身シーンを作成

    Returns:
        bool, str: 成功or失敗, 作成された全身モデルのノード
    """

    # 現在のシーンのパーツ判定
    this_part = get_part(os.path.basename(cmds.file(q=True, sn=True)))
    this_id = get_scene_id(this_part)

    # 全パーツのパスを収集
    part_path_dict = get_part_path_dict(this_part)

    # 他パーツのインポート
    for key, val in part_path_dict.items():
        if key == this_part:
            continue
        if not val:
            continue
        if os.path.exists(val):
            cmds.file(val, i=True)

    # 各パーツのルートノードを特定
    head_root = get_part_root(HEAD_PART_LABEL, this_id)
    body_root = get_part_root(BODY_PART_LABEL, this_id)

    head_neck_joint = get_descendent(head_root, 'Neck')
    body_neck_joint = get_descendent(body_root, 'Neck')
    body_head_joint = get_descendent(body_root, 'Head')

    # nullチェック
    if not head_root or not body_root or not head_neck_joint or not body_neck_joint or not body_head_joint:
        return False, None

    # 複製
    head_dup_root = cmds.duplicate(head_root, n=head_root + '__dup__')[0]
    body_dup_root = cmds.duplicate(body_root, n=body_root + '__dup__')[0]

    head_dup_neck_joint = get_descendent(head_dup_root, 'Neck')
    body_dup_neck_joint = get_descendent(body_dup_root, 'Neck')
    body_dup_head_joint = get_descendent(body_dup_root, 'Head')
    body_dup_chest_joint = get_descendent(body_dup_root, 'Chest')

    # ノード整理
    final_full_body_root = body_dup_root
    finally_delete_nodes = [head_root, body_root, head_dup_root]

    # 位置合わせ
    set_all_attr_unlock(head_dup_root, True)
    neck_translate = cmds.xform(body_dup_neck_joint, q=True, t=True, ws=True)
    cmds.xform(head_dup_root, r=True, t=neck_translate)

    # 骨とメッシュの階層を移動(頭部を身体の子階層にいれる)
    cmds.delete([body_dup_neck_joint, body_dup_head_joint])
    cmds.parent(head_dup_neck_joint, body_dup_chest_joint)

    all_head_dup_children = cmds.listRelatives(head_dup_root, c=True, f=True)
    for child in all_head_dup_children:
        cmds.parent(child, final_full_body_root)

    # 全身モデルのバインド
    bind_skin(final_full_body_root)

    # ウェイトのコピー
    org_skin_meshes = get_skin_meshes(head_root)
    org_skin_meshes.extend(get_skin_meshes(body_root))

    dup_skin_meshes = ['{}|{}'.format(final_full_body_root, x.split('|')[-1]) for x in org_skin_meshes]

    org_skin_info = base_class.mesh.skin_info.SkinInfo()
    org_skin_info.create_info(org_skin_meshes)

    dup_skin_info = base_class.mesh.skin_info.SkinInfo()
    dup_skin_info.create_info(dup_skin_meshes)

    base_utility.mesh.skin.paste_weight_by_vertex_index(org_skin_info, dup_skin_info)

    # 不要な元ノードを削除
    cmds.delete(finally_delete_nodes)

    # リネーム
    result = cmds.rename(final_full_body_root, '{}{}'.format(FULL_BODY_PREFIX, this_id))

    return True, result


def get_part(scene_name):
    """開いているシーンのパーツ名を返す
    """

    this_part = ''

    if re.search(HEAD_SCENE_PATTERN, scene_name):
        this_part = HEAD_PART_LABEL
    elif re.search(BODY_SCENE_PATTERN, scene_name):
        this_part = BODY_PART_LABEL

    return this_part


def get_scene_id(part):
    """開いているシーンのキャラIDを返す

    Args:
        part (str): 開いているシーンのパーツ名

    Returns:
        str: キャラID（[0-9]{4}_[0-9]{2}）
    """

    id = ''

    match = None
    if part == HEAD_PART_LABEL:
        match = re.search(HEAD_SCENE_PATTERN, os.path.basename(cmds.file(q=True, sn=True)))
    elif part == BODY_PART_LABEL:
        match = re.search(BODY_SCENE_PATTERN, os.path.basename(cmds.file(q=True, sn=True)))

    if match:
        id = match.group(1)

    return id


def get_part_path_dict(current_part):
    """各パーツ名をキー、パスをバリューとした辞書を返す

    Args:
        current_part (str): 現在シーンのパーツ

    Returns:
        dict: {パーツ名: パス,,,}
    """

    part_path_dict = {}

    part_path_dict[BODY_PART_LABEL] = get_part_path_from_current(current_part, BODY_PART_LABEL)
    part_path_dict[HEAD_PART_LABEL] = get_part_path_from_current(current_part, HEAD_PART_LABEL)

    return part_path_dict


def get_part_path_from_current(current_part, target_part):
    """現在のシーンから他パーツのシーンパスを取得
    "キャラID/パーツ名/scenes/maファイル"というディレクトリ構成を想定
    """

    # 分岐点のIDフォルダ
    root_dir = ''

    if current_part == HEAD_PART_LABEL:
        scene_dir = os.path.dirname(cmds.file(q=True, sn=True))
        part_dir = os.path.dirname(scene_dir)
        root_dir = os.path.dirname(part_dir)
    elif current_part == BODY_PART_LABEL:
        scene_dir = os.path.dirname(cmds.file(q=True, sn=True))
        part_dir = os.path.dirname(scene_dir)
        root_dir = os.path.dirname(part_dir)

    if not os.path.exists(root_dir):
        return ''

    # IDフォルダからシーンをとる
    id = get_scene_id(current_part)

    mid_path = ''
    scene_name = ''
    if target_part == HEAD_PART_LABEL:
        mid_path = os.path.join(HEAD_DIR, 'scenes')
        scene_name = 'mdl_chr{}.ma'.format(id)
    elif target_part == BODY_PART_LABEL:
        mid_path = os.path.join(BODY_DIR, 'scenes')
        scene_name = 'mdl_bdy{}.ma'.format(id)

    return os.path.join(root_dir, mid_path, scene_name)


def get_part_root(part, id):
    """パーツのルートノード名を取得
    """

    root_node = ''

    if part == HEAD_PART_LABEL:
        root_node = '|mdl_chr{}'.format(id)
    elif part == BODY_PART_LABEL:
        root_node = '|mdl_bdy{}'.format(id)

    return root_node


def get_descendent(root, target_short_name):
    """下階層から命名一致でノードを取得
    """

    target = ''

    if not cmds.objExists(root):
        return target

    all_descendents = cmds.listRelatives(root, ad=True, f=True)

    for descendent in all_descendents:
        short_name = descendent.split('|')[-1]
        if short_name == target_short_name:
            target = descendent
            break

    return target


def set_all_attr_unlock(node, is_all_descentents):
    """全アトリビュートのロックを解除
    結合時にロックに起因するエラーを回避するために使用

    Args:
        node (str): ロック解除対象のノード
        is_all_descentents (bool): 下階層のロックも解除するか
    """

    target_nodes = [node]

    if is_all_descentents:
        target_nodes.extend(cmds.listRelatives(node, f=True))

    for node in target_nodes:
        target_attr = cmds.listAttr(node, l=True)
        if target_attr:
            for attr in target_attr:
                cmds.setAttr('{}.{}'.format(node, attr), l=False)


def bind_skin(root):
    """スキニング
    root以下のメッシュとジョイントが仕様に沿っている前提でスキニング. インフルエンスは4.
    """

    meshes = get_skin_meshes(root)
    joints = get_skin_joints(root)

    for mesh in meshes:

        connection_node_list = cmds.listHistory(mesh)
        skinCluster_list = cmds.ls(connection_node_list, typ='skinCluster')

        if skinCluster_list:
            continue

        cmds.skinCluster(mesh,
                         joints,
                         obeyMaxInfluences=False,
                         bindMethod=0,
                         maximumInfluences=4,
                         removeUnusedInfluence=False,
                         skinMethod=0)


def get_skin_meshes(root):
    """root以下のスキニングするメッシュのリストを取得
    root直下のアウトライン以外が対象の想定
    """

    children = cmds.listRelatives(root, c=True, f=True)
    skin_meshes = []

    for child in children:
        short_name = child.split('|')[-1]
        if short_name.startswith('M_') and not short_name.endswith('_Outline'):
            skin_meshes.append(child)

    return skin_meshes


def get_skin_joints(root):
    """root以下のスキニングするジョイントのリストを取得
    """

    position = '{}|Position'.format(root)
    return cmds.listRelatives(position, ad=True, f=True, type='joint')


def get_full_body_scene_name():
    """一体化後のシーン名（拡張子なし）を取得
    """
    return '{}{}'.format(FULL_BODY_PREFIX, get_scene_id(get_part(os.path.basename(cmds.file(q=True, sn=True)))))
