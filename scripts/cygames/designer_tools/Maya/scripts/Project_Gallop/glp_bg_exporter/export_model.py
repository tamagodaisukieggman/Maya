# -*- coding: utf-8 -*-

"""
エクスポート用のモデルを作成

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

from maya import cmds
from maya import mel

from . import constants
from . import utility

reload(constants)
reload(utility)


def create_all(trans_nodes=[]):
    """エクスポート用のモデルを作成

    Args:
        trans_nodes (list[str]): 作成元のノード名リスト
    """

    if len(trans_nodes) == 0:
        # 確認メッセージ
        message_str = '「CyExportModel」によってエクスポートされるデータを確認用として作成します。'
        message_str += '\n' + '※作成されるデータはフラグによる追加処理を実行した後のものになります。'
        message_str += '\n'
        message_str += '\n' + '実行しますか？'

        dialog_result = cmds.confirmDialog(title=constants.TOOL_NAME, message=message_str, button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')

        if dialog_result == 'No':
            return

        trans_nodes = cmds.ls(sl=1, transforms=1, flatten=1)

        if len(trans_nodes) == 0:
            message_str = '操作対象が1つも選択されていません。'
            cmds.confirmDialog(title=constants.TOOL_NAME, message='● ' + message_str)
            return

    result_nodes = []

    for current_node in trans_nodes:
        # エクスポート用のデータを作成(1データ)
        result_info = create_one(current_node, 'create')

        current_top_node = result_info['topNode']

        result_nodes.append(current_top_node)

    cmds.select(result_nodes)


def create_one(src_top_node, mode):
    """エクスポート用のモデルを作成(1データ)

    Args:
        src_top_node (str): 作成元のトップノード名
        mode (str): 処理モード（create or export）

    Returns:
        dict[str, str]: トップノード名と出力名を含む辞書
    """

    result_info = {}

    export_name = src_top_node.split('|')[-1].split(constants.TEMP_NODE_SUFFIX)[0].split('__')[0]

    # 移動値と回転値を取得
    world_pos_value = cmds.xform(src_top_node, q=True, translation=True, worldSpace=True)
    world_rot_value = cmds.xform(src_top_node, q=True, rotation=True, worldSpace=True)
    world_scale_value = cmds.xform(src_top_node, q=True, scale=True, relative=True)

    # 上流ノードも含めて複製
    duplicated_node = cmds.duplicate(src_top_node, upstreamNodes=True)[0]
    copied_top_node = cmds.ls(duplicated_node, long=True)[0]

    # 親子付解除（親ノードがあるなら）
    if cmds.listRelatives(copied_top_node, parent=True):
        unparented_node = cmds.parent(copied_top_node, world=True)
        copied_top_node = cmds.ls(unparented_node, long=True)[0]

    # エクスポートオプション情報を取得(再帰)
    all_nodes, export_option_info = get_export_option_info(copied_top_node, [], {})

    # トップノードのエクスポートオプションを保持
    top_node_export_option_info = export_option_info[copied_top_node]

    # トップノードを初期化
    if export_option_info[copied_top_node]['topNodeReset']:
        init_top_node(copied_top_node)
    delete_pre_deformer_history(copied_top_node)

    # エクスポートオプションを適用
    all_result_nodes = apply_export_option(all_nodes, export_option_info)

    if not cmds.objExists(copied_top_node):
        copied_top_node = all_result_nodes[0]

    if mode == 'create':
        # 一時グループを作成
        temp_group_name = '|export_temp'
        if not cmds.objExists(temp_group_name):
            temp_group = cmds.group(name=temp_group_name, empty=True)
            temp_group_name = cmds.ls(temp_group, long=True)[0]

        # 一時グループに移動
        parented_node = cmds.parent(copied_top_node, temp_group_name)
        copied_top_node = cmds.ls(parented_node, long=True)[0]

    # リネーム
    renamed_top_node = cmds.rename(copied_top_node, export_name)

    result_info['topNode'] = cmds.ls(renamed_top_node, long=True)[0]
    result_info['exportName'] = export_name

    cmds.select(renamed_top_node)

    return result_info


def init_top_node(top_node):
    """トップノードを初期化

    Args:
        top_node (str): トップノード名
    """

    # トップノードのトランスフォームをリセットする
    cmds.xform(top_node, translation=[0, 0, 0], worldSpace=True)
    cmds.xform(top_node, rotation=[0, 0, 0], worldSpace=True)
    cmds.xform(top_node, scale=[1, 1, 1])


def delete_pre_deformer_history(top_node):
    """デフォーマ前のヒストリーを削除

    Args:
        top_node (str): トップノード名
    """

    try:
        cmds.select(top_node)
        mel.eval('doBakeNonDefHistory(1, {"pre"})')
    except Exception:
        pass


def apply_export_option(all_nodes, export_option_info):
    """エクスポートオプションを適用

    Args:
        all_nodes (list[str]): ノードリスト
        export_option_info (dict[str, dict[str, Any]]): エクスポートオプション

    Returns:
        list[str]: 処理後のノードリスト
    """

    all_result_nodes = []
    all_node_export_names = []
    temp_result_nodes = []

    for current_node in all_nodes:

        # ノード名
        current_node_export_name = current_node.split('|')[-1].split('__')[0]
        all_node_export_names.append(current_node_export_name)

        cmds.select(current_node)

        # スキンメッシュの場合
        if export_option_info[current_node]['isSkinMesh'] == 1:
            # バインドポーズに戻す
            mel.eval('gotoBindPose')

        # フラグ
        combine_flg = export_option_info[current_node]['combine']
        keep_trans_flg = export_option_info[current_node]['keeptrans']
        merge_flg = export_option_info[current_node]['merge']
        freeze_flg = export_option_info[current_node]['freeze']
        boundingbox_flg = export_option_info[current_node]['boundingbox']
        attribute_flg = export_option_info[current_node]['attribute']
        no_piv_reset_flg = export_option_info[current_node]['nopivreset']

        current_new_node = None

        # コンバインする場合
        if combine_flg == 1:

            # keepTransFlgが立っている場合は元のトランスフォーム情報を最後に戻す必要がある
            # コンバイン時にトランスフォーム情報が消えてしまうので、一旦保存してリセットからコンバインし後で復元する
            org_position = None
            org_rotation = None
            org_scale = None

            if keep_trans_flg == 1:
                # トランスフォーム情報の取得. ピボットはコンバイン後に復元されるので不要
                org_position = cmds.xform(current_node, q=True, t=True)
                org_rotation = cmds.xform(current_node, q=True, ro=True)
                org_scale = cmds.xform(current_node, q=True, s=True)

                cmds.xform(current_node, t=[0, 0, 0])
                cmds.xform(current_node, ro=[0, 0, 0])
                cmds.xform(current_node, s=[1, 1, 1])

            current_parent_nodes = cmds.listRelatives(current_node, parent=True, fullPath=True)
            current_parent_node = current_parent_nodes[0] if current_parent_nodes else None

            # 子メッシュを取得
            child_mesh_nodes = utility.get_child_transform_nodes(current_node, recurse=True, include_self=True, node_types=['mesh'])

            # 子メッシュが1つも存在しない場合
            if len(child_mesh_nodes) == 0:
                current_new_node = current_node
            else:
                # 子メッシュが1つの場合→コンバインしない
                if len(child_mesh_nodes) == 1:
                    current_new_node = child_mesh_nodes[0]

                    # 現在のノードがメッシュの場合
                    if current_new_node == current_node:
                        pass

                    # 現在のノードがメッシュ以外の場合
                    else:
                        new_parent_nodes = cmds.listRelatives(current_new_node, parent=True, fullPath=True)
                        new_parent_node = new_parent_nodes[0] if new_parent_nodes else None

                        if new_parent_node != current_node:
                            parented_node = cmds.parent(current_new_node, current_node)
                            current_new_node = cmds.ls(parented_node, long=True)[0]

                        # フリーズ・リセット
                        freeze_reset(current_new_node, no_piv_reset_flg)

                        # 親子付を変更
                        if current_parent_node is not None:
                            if cmds.objExists(current_parent_node):
                                parented_node = cmds.parent(current_new_node, current_parent_node)
                                current_new_node = cmds.ls(parented_node, long=True)[0]

                        # 残ったノードを削除
                        if cmds.objExists(current_node):
                            cmds.delete(current_node)

                # 子メッシュが2つ以上ある場合→コンバインする
                elif len(child_mesh_nodes) >= 2:
                    # コンバイン前のワールド座標を取得
                    current_world_pos = cmds.xform(current_node, q=True, translation=True, worldSpace=True)

                    # コンバイン ※親ノードが自動的に削除されてしまう可能性があるため、あえてヒストリーを残す
                    united_node, _ = cmds.polyUnite(current_node, constructionHistory=True, mergeUVSets=1)
                    current_new_node = cmds.ls(united_node, long=True)[0]

                    # 親子付を復帰
                    if current_parent_node is not None:
                        if cmds.objExists(current_parent_node):
                            parented_node = cmds.parent(current_new_node, current_parent_node)
                            current_new_node = cmds.ls(parented_node, long=True)[0]

                    # コンバイン後のヒストリー削除
                    cmds.delete(current_new_node, constructionHistory=True)

                    # 残ったノードを削除
                    if cmds.objExists(current_node):
                        cmds.delete(current_node)

                    # 親にトランスフォーム値が入っていると親子付を復活させた時に値が入ってしまいトランスフォーム情報を復元できなくなるのでリセット
                    if keep_trans_flg == 1:
                        freeze_reset(current_new_node, no_piv_reset_flg)

                    # センターをコンバイン前のワールド座標に移動
                    utility.move_center(current_new_node, current_world_pos)

            # トランスフォーム情報の復元
            if keep_trans_flg == 1:
                cmds.xform(current_new_node, t=org_position)
                cmds.xform(current_new_node, ro=org_rotation)
                cmds.xform(current_new_node, s=org_scale)

        else:
            current_new_node = current_node

        # センターピボットを実行する場合
        if boundingbox_flg == 1:
            if freeze_flg == 0:
                cmds.xform(current_new_node, centerPivots=True)

                # センター → ピボット
                utility.move_center_to_pivot(current_new_node)

        # フリーズする場合
        if freeze_flg == 1:
            # フリーズ・リセット
            freeze_reset(current_new_node, no_piv_reset_flg)

        # 頂点マージする場合
        if merge_flg == 1:
            # 頂点マージ
            cmds.polyMergeVertex(current_new_node, distance=0.01, constructionHistory=False)

        if attribute_flg == 1:
            # 不要なエクストラアトリビュートを削除
            utility.delete_extra_attributes(current_new_node, 'exportInfo_path', 'string')
        else:
            # 全てのエクストラアトリビュートを削除
            utility.delete_extra_attributes(current_new_node)

        temp_result_nodes.append(current_new_node)

    for current_node, export_name in reversed(list(zip(temp_result_nodes, all_node_export_names))):
        renamed_node = cmds.rename(current_node, export_name)
        all_result_nodes.append(cmds.ls(renamed_node, long=True)[0])

    all_result_nodes.reverse()

    return all_result_nodes


def get_export_option_info(node, all_nodes=[], export_option_info={}):
    """エクスポートオプション情報を取得(再帰)

    Args:
        node (str): 対象ノード名
        all_nodes (list[str]): ノードリスト
        export_option_info (dict[str, dict[str, Any]]): エクスポートオプション

    Returns:
        tuple[list[str], dict[str, dict[str, Any]]]: ノードリスト、エクスポートオプションのタプル
    """

    all_nodes.append(node)

    # ノード名
    node_short_name = node.split('|')[-1]

    export_option_info[node] = {}

    # 汎用フラグ
    export_option_info[node]['combine'] = 0
    export_option_info[node]['merge'] = 0
    export_option_info[node]['freeze'] = 0
    export_option_info[node]['boundingbox'] = 0
    export_option_info[node]['attribute'] = 0
    export_option_info[node]['nopivreset'] = 0
    export_option_info[node]['keeptrans'] = 0

    # トップノード限定フラグ
    export_option_info[node]['topNodeReset'] = 0

    # ノードタイプ
    export_option_info[node]['nodeType'] = utility.get_node_type(node)

    # スキンメッシュかどうか
    export_option_info[node]['isSkinMesh'] = 0

    # ヒストリーを調べる
    history_nodes = cmds.listHistory(node)
    for current_history_node in history_nodes:
        # スキンメッシュの場合
        if cmds.nodeType(current_history_node) == 'skinCluster':
            export_option_info[node]['isSkinMesh'] = 1

    # Mayaが複製時につける数字とツールがつける接尾辞を削除
    node_trim_name = re.sub('[0-9]$', '', node_short_name)
    node_trim_name = node_trim_name.replace(constants.TEMP_NODE_SUFFIX, '')

    # ノード名を分解してエクスポートオプションを取得
    name_parts = node_trim_name.lower().split('__')
    if len(name_parts) > 1:
        if name_parts[1] != '':

            option_flgs = name_parts[1].split('_')

            for current_flg in option_flgs:
                # コンバインする場合
                if current_flg in ['combine', 'cmb']:
                    export_option_info[node]['combine'] = 1

                # コンバイン時にトランスフォーム値を保持する
                elif current_flg in ['keeptrans', 'kts']:
                    export_option_info[node]['keeptrans'] = 1

                # 頂点マージする場合
                elif current_flg in ['merge', 'mrg']:
                    export_option_info[node]['merge'] = 1

                # フリーズする場合
                elif current_flg in ['freeze', 'frz']:
                    export_option_info[node]['freeze'] = 1

                # センターピボットを実行する場合
                elif current_flg in ['boundingbox', 'bbox']:
                    export_option_info[node]['boundingbox'] = 1

                # エクストラアトリビュートを残す場合
                elif current_flg in ['attribute', 'atr']:
                    export_option_info[node]['attribute'] = 1

                # ピボットのリセットをしない場合
                elif current_flg in ['nopivreset', 'npr']:
                    export_option_info[node]['nopivreset'] = 1

                # トップノードのトランスフォームのリセットする場合
                elif current_flg in ['topnodereset', 'tnr']:
                    export_option_info[node]['topNodeReset'] = 1

    if export_option_info[node]['combine'] == 0:
        # 子ノードが存在する場合
        child_nodes = utility.get_child_transform_nodes(node)

        if len(child_nodes) > 0:
            for child_node in child_nodes:
                # エクスポートオプション情報を取得(再帰)
                all_nodes, export_option_info = get_export_option_info(child_node, all_nodes, export_option_info)

    return all_nodes, export_option_info


def freeze_reset(node, no_piv_reset_flg):
    """フリーズ・リセット
    """

    # フリーズ
    cmds.makeIdentity(node, apply=True, translate=True, rotate=True, scale=True, normal=0)

    if not no_piv_reset_flg:
        # ピボット位置をリセットする
        cmds.xform(node, zeroTransformPivots=True)


if __name__ == '__main__':
    create_all()
