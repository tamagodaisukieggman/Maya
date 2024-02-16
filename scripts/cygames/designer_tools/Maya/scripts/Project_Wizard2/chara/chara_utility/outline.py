# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
try:
    # Maya 2022-
    from builtins import str
except Exception:
    pass

import maya.cmds as cmds


def create_outline():
    """
    選択中のメッシュからアウトライン用のメッシュを作ります。
    アウトライン用のメッシュは法線のアングル180(ソフトエッジ)を設定します。
    既存のアウトライン用メッシュが存在する場合は法線は既存のものを反映させます。
    モデルの頂点カラーをアウトライン用のメッシュにコピーします。
    （頂点カラーの設定はベースモデルで行うが確認用に必要とのこと）
    モデルに頂点カラーがない場合はワーニングでお知らせします。
    """
    cmds.select(cmds.ls(sl=True), hierarchy=True)
    selected_mesh_transforms = [cmds.listRelatives(i, p=True, fullPath=True)[0] for i in cmds.ls(sl=True, long=True, type='mesh')]
    if not selected_mesh_transforms:
        cmds.warning('モデルのメッシュを選択してから実行してください')
        return
    # メッシュと対応する既存のアウトラインメッシュのペアを作成
    mesh_outline_pairs = []
    for transform in selected_mesh_transforms:
        # アウトラインからアウトラインは作らないのでスルー
        if transform.endswith('_Outline'):
            continue
        outline = transform + '_Outline'
        if cmds.objExists(outline):
            mesh_outline_pairs.append((transform, outline))
        else:
            mesh_outline_pairs.append((transform, None)) 
    # 以下、既存のアウトラインの設定を引き継ぎつつ新アウトラインメッシュを作る処理
    if not mesh_outline_pairs:
        cmds.warning('アウトラインを作りたいモデルのメッシュを選択してから実行してください')
        return
    # 既存の_Outlineから法線を引き継ぎつつモデルのメッシュから_Outlineを作り直す
    for target_pair in mesh_outline_pairs:
        chara_mesh = target_pair[0]
        prev_outline = target_pair[1]
        outline_mesh_name = cmds.ls(chara_mesh, shortNames=True)[0] + '_Outline'
        # キャラメッシュから新しいアウトラインメッシュを作成
        # 2022/11 既存_Outlineではなくキャラメッシュから頂点カラーを引き継ぎたいとの要望あり
        new_outline = cmds.duplicate(chara_mesh)[0]
        # _Outlineメッシュの方は頂点カラーを表示しておく
        cmds.polyOptions(new_outline, colorShadedDisplay=True)
        # 既存の_Outlineのロックされている頂点をリストしておく
        locked_vtx_indexes = []
        verticies = cmds.ls(outline_mesh_name+'.vtx[*]', l=True, flatten=True)
        for i, vtx in enumerate(verticies):
            freezed = cmds.polyNormalPerVertex(vtx, q=True, freezeNormal=True)
            if True in freezed:
                locked_vtx_indexes.append(i)
        # 新アウトラインの法線を一度全てアンロック
        cmds.polyNormalPerVertex(new_outline, unFreezeNormal=True)
        # ソフトエッジをかける
        cmds.polySoftEdge(new_outline, a=180)
        # 旧＞新アウトラインメッシュで頂点位置が近くなもの同士で法線をコピー（モデル空間座標）
        # transferAttributesをするとコピーされた方の法線がすべてロックされてしまうので
        # 頂点番号でロックを外す（頂点番号が変わってしまっているものに関してまでは対応できない）
        new_outline = cmds.ls(new_outline, l=True)[0]
        if prev_outline:
            cmds.transferAttributes(prev_outline, new_outline, transferNormals=1,
                                    sampleSpace=1, searchMethod=3,
                                    flipUVs=0)
        # ロックされていない法線をもとに戻す
        cmds.select(clear=True)
        for i in locked_vtx_indexes:
            cmds.select(new_outline + '.vtx[{}]'.format(i), add=True)
        # 選択反転
        cmds.select(new_outline+'.vtx[*]', toggle=True)
        vtxs_to_unlock = cmds.ls(sl=True)
        if vtxs_to_unlock:
            cmds.polyNormalPerVertex(vtxs_to_unlock, unFreezeNormal=True)
        cmds.select(clear=True)
        cmds.setAttr(new_outline + '.visibility', 0)
        # コンストラクションヒストリーを消しておかないと元アウトラインを消した際、コピーした法線の向きが元に戻ってしまうので注意
        cmds.delete(new_outline, constructionHistory=True)
        if prev_outline:
            cmds.delete(prev_outline)
        new_outline = cmds.rename(new_outline, outline_mesh_name)

        # もしedgesetが存在していればその中からoutlineのメッシュをremove
        remove_edgeset_member(new_outline)

        print('_Outline作成・更新: ' + new_outline)

def remove_edgeset_member(remove_mesh:str):
    """対象のメッシュに含まれるコンポーネントをすべてのedge_setから除外

    Args:
        remove_mesh (str): 除外するコンポーネントを所持しているメッシュ
    """
    edge_sets = cmds.ls("*_edge_sets",type='objectSet')
    for edge_set in edge_sets:
        set_mambers = cmds.sets(edge_set, q=True)
        for member in set_mambers:
            # セットから複製したオブジェクトを除外
            if remove_mesh in member:
                cmds.sets(member, remove=edge_set)