# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import re
import csv

import maya.cmds as cmds

from ..glp_common.classes.info import chara_info
from ..glp_common.classes.path_finder import path_finder
from ..base_common.classes.mesh import skin_info
from ..base_common.utility.mesh import skin


def search_chara_model_id(file_path):
    """ファイルパスからモデルIDを取得する

    Args:
        file_path (str): モデルIDを取得するファイルパス

    Returns:
        str: モデルメインID, サブID
    """

    main_id = None
    sub_id = None

    match_obj = re.search(r'([0-9]{4})_([0-9]{2})', file_path)
    if match_obj:
        main_id = match_obj.group(1)
        sub_id = match_obj.group(2)

    return main_id, sub_id


def get_is_unique_chara(file_path):
    """ユニークキャラかどうかを取得する

    Args:
        file_path (str): ユニークキャラかどうかを取得したいファイルパス

    Returns:
        bool: ユニークキャラかどうか
    """

    info = chara_info.CharaInfo()
    info.create_info(file_path=file_path)

    return info.is_unique_chara if info.exists else False


def fetch_type_id(main_id, sub_id, file_path, csv_file_path):
    """dress_dataからモデルIDに合致するheadとtailのモデルIDを取得する

    Args:
        main_id (str): モデルのメインID
        sub_id (str): モデルのサブID
        file_path (str): bodyのファイルパス(chara_infoのdress_dataを利用する場合)
        csv_file_path (str): dress_data.csvのパス

    Returns:
        [{str: str}]: headとtailのモデルIDセットのリスト
    """

    fetch_list = []

    if os.path.exists(csv_file_path):

        with open(csv_file_path, 'r') as f:

            reader = csv.DictReader(f)
            next(reader)

            chara_id_key = 'chara_id'
            body_type_sub_key = 'body_type_sub'
            head_sub_id_key = 'head_sub_id'
            tail_model_id_key = 'tail_model_id'
            tail_model_sub_id_key = 'tail_model_sub_id'

            for r in reader:

                if int(main_id) != int(r[chara_id_key]) or int(sub_id) != int(r[body_type_sub_key]):
                    continue

                head_sub_id = r[head_sub_id_key]
                tail_id = r[tail_model_id_key] if not (r[tail_model_id_key] == -1 or r[tail_model_id_key] == '-1') else '0001'
                tail_sub_id = r[tail_model_sub_id_key] if not (r[tail_model_sub_id_key] == -1 or r[tail_model_sub_id_key] == '-1') else '00'

                fetch_list.append({
                    'head_id': '{0}_{1:02}'.format(main_id, int(head_sub_id)),
                    'tail_id': '{0}_{1:02}'.format(tail_id, int(tail_sub_id))
                })

    else:

        info = chara_info.CharaInfo()
        info.create_info(file_path=file_path)

        if not info.exists:
            return []

        head_sub_id = info.data_info.dress_head_sub_id
        tail_model_id = info.data_info.dress_tail_model_id
        tail_model_sub_id = info.data_info.dress_tail_model_sub_id
        tail_id = tail_model_id if not (tail_model_id == -1 or tail_model_id == '-1') else '0001'
        tail_sub_id = tail_model_sub_id if not (tail_model_sub_id == -1 or tail_model_sub_id == '-1') else '00'

        fetch_list.append({
            'head_id': '{0}_{1:02}'.format(main_id, int(head_sub_id)),
            'tail_id': '{0}_{1:02}'.format(tail_id, int(tail_sub_id))
        })

    return fetch_list


def fetch_type_id_model_paths(parts_type, id):
    """モデルidと種類からモデルmaのパスを取得する

    Args:
        parts_type (str): 取得するモデルの種類(body, head, tail等)
        id (str): 取得したいモデルのID

    Returns:
        list(str): モデルmaのパスリスト
    """

    type_pf = path_finder.PathFinder(parts_type, id)

    return type_pf.model_ma_list


def create_union_chara_model(body_file_path, head_file_path, save_union_file_path, tail_file_path=''):
    """頭・身体・尻尾が合成したモデルを作成する

    Args:
        body_file_path (str): 身体のファイル名
        head_file_path (str): 頭のファイル名
        save_union_file_path (str): 合体モデルの保存パス
        tail_file_path (str): 尻尾のファイル名. default is ''

    Returns:
        bool : 処理が成功したかどうか
    """

    use_tail_path = False

    if not all([os.path.exists(path) for path in [body_file_path, head_file_path, save_union_file_path]]):
        return False

    # chara_infoの生成
    bdy_chara_info = chara_info.CharaInfo()
    bdy_chara_info.create_info(body_file_path)
    head_chara_info = chara_info.CharaInfo()
    head_chara_info.create_info(head_file_path)
    if not bdy_chara_info.exists or not head_chara_info.exists:
        return False

    # 尻尾ありの処理
    if tail_file_path:

        if not os.path.exists(tail_file_path):
            return False

        tail_chara_info = chara_info.CharaInfo()
        tail_chara_info.create_info(tail_file_path)
        if not tail_chara_info.exists:
            return False

        use_tail_path = True

    # 新しいシーンにする
    cmds.file(new=True, f=True)

    # モデルの全import
    for ma_path in [body_file_path, head_file_path]:
        cmds.file(ma_path, i=True)

    bdy_mesh_list = [mesh for mesh in bdy_chara_info.part_info.mesh_list if cmds.objExists(mesh) and skin.get_skin_cluster(mesh)]
    head_mesh_list = [mesh for mesh in head_chara_info.part_info.mesh_list if cmds.objExists(mesh) and skin.get_skin_cluster(mesh)]
    org_mesh_list = bdy_mesh_list + head_mesh_list

    # 尻尾ありの処理
    if use_tail_path:

        cmds.file(tail_file_path, i=True)
        tail_mesh_list = [mesh for mesh in tail_chara_info.part_info.mesh_list if cmds.objExists(mesh) and skin.get_skin_cluster(mesh)]
        org_mesh_list += tail_mesh_list

    # weightの取得
    org_skin_info = skin_info.SkinInfo()
    org_skin_info.create_info(org_mesh_list)

    body_node = bdy_chara_info.part_info.root_node
    head_node = head_chara_info.part_info.root_node
    all_part_node = [body_node, head_node]

    # NeckJointを入れ替え
    body_neck = get_node_from_node_hierarcy(body_node, 'Neck')
    head_neck = get_node_from_node_hierarcy(head_node, 'Neck')
    replacement_node(body_neck, head_neck)

    # 中身を入れ替え
    cmds.parent(head_mesh_list, body_node)

    # 尻尾ありの処理
    if use_tail_path:

        tail_node = tail_chara_info.part_info.root_node
        all_part_node += [tail_node]

        # 不要なBodyにあるTail_Ctrl削除
        body_tail_ctrl = get_node_from_node_hierarcy(body_node, 'Tail_Ctrl')
        cmds.delete(body_tail_ctrl)

        # HipJointを入れ替え
        body_hip_joint = get_node_from_node_hierarcy(body_node, 'Hip')
        tail_hip_joint = get_node_from_node_hierarcy(tail_node, 'Hip')
        replacement_node(body_hip_joint, tail_hip_joint)

        # 中身を入れ替え
        cmds.parent(tail_mesh_list, body_node)

    # 入れ替え後のモデルを複製して大元のファイルを削除
    dup_node = cmds.duplicate(body_node)[0]
    cmds.delete(all_part_node)
    cmds.rename(dup_node, body_node.split('|')[-1].split(':')[-1])

    body_in_head_mesh_list = [mesh.replace(head_node, body_node) for mesh in head_mesh_list]
    dst_meshes = bdy_mesh_list + body_in_head_mesh_list

    # 尻尾ありの処理
    if use_tail_path:
        body_in_tail_mesh_list = [mesh.replace(tail_node, body_node) for mesh in tail_mesh_list]
        dst_meshes += body_in_tail_mesh_list

    # 複製後のモデルのバインド
    joints = cmds.ls([node for node in cmds.listRelatives('{}'.format(body_node), ad=True)], type='joint')
    bind_skin(dst_meshes, joints)

    # ウェイト再設定
    mesh_skin_info = skin_info.SkinInfo()
    mesh_skin_info.create_info(dst_meshes)
    skin.paste_weight_by_vertex_index(org_skin_info, mesh_skin_info)

    # シーンのunknownノード削除
    unknown_nodes = cmds.ls(type='unknown')
    cmds.delete(unknown_nodes)

    # maとして保存
    body_file_name = os.path.splitext(os.path.basename(body_file_path))[0]
    cmds.file(rename='{}/{}.ma'.format(save_union_file_path, body_file_name))
    cmds.file(save=True, type='mayaAscii')

    return True


def bind_skin(meshes, joints):
    """バインドスキンを行う

    Args:
        meshes ([str]): バインド対象メッシュ
        joints ([str]): バインド対象ジョイント
    """

    for mesh in meshes:
        cmds.skinCluster(
            mesh,
            joints,
            obeyMaxInfluences=False,
            bindMethod=0,
            maximumInfluences=2,
            removeUnusedInfluence=False,
            skinMethod=0
        )


def get_node_from_node_hierarcy(node, search_name):
    """対象のノード以下から名前が一致するノードを取得する

    Args:
        node (str): 階層を検索する対象ノード名
        search_name (str): 検索する対象の名前

    Returns:
        str or None: 名前が一致したノード名
    """

    nodes = cmds.listRelatives(node, ad=True, f=True)
    search_nodes = [n for n in nodes if n.split('|')[-1].split(':')[-1] == search_name]
    if len(search_nodes) != 1:
        return None

    return search_nodes[0]


def get_node_parent(node):
    """指定されたノードの親を取得する

    Args:
        node (str): 親を取得したいノード名

    Returns:
        str or None: 親のノード名 or None
    """

    parents = cmds.listRelatives(node, p=True, f=True)
    if parents is None or len(parents) != 1:
        return None

    return parents[0]


def get_order(node):
    """対象ノードのOutliner上での並び順を取得する

    Args:
        node (str): Outliner上での並び順を取得するノード名

    Returns:
        int: Outliner上での並び順
    """

    node_parent = get_node_parent(node)
    nodes = cmds.listRelatives(node_parent, f=True)
    return nodes.index(node)


def set_order(node, index):
    """Outliner上の順番を設定する

    Args:
        node (str): 順番を並び替えるノード
        index (int): 位置番号
    """

    cmds.reorder(node, f=True)
    cmds.reorder(node, r=index)


def replacement_node(src_node, dst_node):
    """異なるノード同士を挿げ替える

    Args:
        src_node (str): 挿げ替える元になるノード
        dst_node (str): 挿げ替えるノード
    """

    src_node_parent = get_node_parent(src_node)
    moved_node = cmds.parent(dst_node, src_node_parent)[0]
    src_node_order = get_order(src_node)
    set_order(moved_node, src_node_order)
    src_node_pos = cmds.xform(src_node, q=True, ws=True, t=True)
    cmds.xform(moved_node, ws=True, t=src_node_pos)

    src_child_node = cmds.listRelatives(src_node, f=True)
    cmds.parent(src_child_node, moved_node)

    cmds.delete(src_node)
    cmds.rename(moved_node, src_node.split('|')[-1].split(':')[-1])


def determine_node_type(node, node_type):
    """対象のノードが指定する特定のノードタイプか判定する

    Args:
        node (str): _description_
        node_type (str): _description_

    Returns:
        bool : 特定のノードタイプかどうか
    """

    is_decide_type = False

    shapes = cmds.listRelatives(node, s=True)
    if shapes:
        shapes = [shape for shape in shapes if cmds.objectType(shape) == node_type]
        if shapes:
            is_decide_type = True

    return is_decide_type


def determine_model_type(path, path_type):
    """ファイルパスが指定のタイプと合致しているかを判別する

    Args:
        path (str): 判別するファイルパス
        path_type (str): 合致しているか判断するタイプ

    Returns:
        bool: ファイルパスが指定のタイプと合致しているか
    """

    if path_type:
        regex = ''
        if path_type == 'body':
            regex = re.compile(r'bdy[0-9]{4}_[0-9]{2}')
        elif path_type == 'head':
            regex = re.compile(r'chr[0-9]{4}_[0-9]{2}')
        elif path_type == 'tail':
            regex = re.compile(r'tail[0-9]{4}_[0-9]{2}')

        if regex:
            m_obj = regex.search(os.path.basename(path))
            return True if m_obj else False

    return True


def get_option_var(key):
    """OptionVarから値を取得する

    Args:
        key (str): OptionVarから取得してくる値のkey

    Returns:
        str: optionVarから取得してきた値 or ''
    """

    value = ''

    if cmds.optionVar(exists=key):
        value = cmds.optionVar(q=key)

    return value


def set_option_var(key, value):
    """OptionVarに値を設定する

    Args:
        key (str): OptionVarに登録するkey
        value (str): OptionVarに登録する値
    """

    cmds.optionVar(sv=[key, str(value)])
