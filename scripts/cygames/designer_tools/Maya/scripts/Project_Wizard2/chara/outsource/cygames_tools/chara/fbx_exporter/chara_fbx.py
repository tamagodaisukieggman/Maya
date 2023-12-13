# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import traceback
import typing as tp

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

import os
import subprocess
import maya.cmds as cmds
import maya.mel as mel

from ..chara_utility import utility as chara_utility

reload(chara_utility)


def export_fbx(chk_export_parts, chk_only_visible, save_before):
    """_export_fbxの事前処理、事後処理を行う
    事前処理として保存処理、事後処理として事前に保存したファイルを開く処理

    Args:
        create_parts_fbx (PySide2.QtWidgets.QCheckBox): 「メッシュ名単位でFBXをエクスポート」チェックボックス
        chk_only_visible (PySide2.QtWidgets.QCheckBox): 「非表示のメッシュは除く」チェックボックス
        save_before (PySide2.QtWidgets.QCheckBox): 「実行前にシーンを保存」チェックボックス
    """
    secene_path = cmds.file(q=True, sn=True)

    if not secene_path:
        cmds.confirmDialog(title="確認", message="シーンを開いてから実行してください", button=["OK"])
        return

    is_scene_modified = cmds.file(q=True, modified=True)
    is_writable = os.access(secene_path, os.W_OK)

    if is_scene_modified and not is_writable:
        cmds.confirmDialog(
            title="確認",
            message="シーンが読み取り専用です\n"
            + "Perforceでチェックアウトしていますか？\n"
            + "シーンが保存できないのでキャンセルします",
            button=["OK"],
        )
        return

    if save_before.isChecked():
        cmds.file(save=True)

    # _export_fbx(chk_export_parts, chk_only_visible)
    # export処理
    try:
        _export_fbx(chk_export_parts, chk_only_visible)
    except Exception as e:
        traceback.print_exc()
        print("エラー: ", e)

    cmds.file(secene_path, open=True, force=True)


def _export_fbx(chk_export_parts, chk_only_visible):
    """
    選択しているオブジェクトのfbxをMayaプロジェクトフォルダ内のfbxフォルダに出力します
    _Outlineメッシュの法線情報をモデルのuvセットに持たせます
    メッシュ名に対応する_Outlineメッシュがない場合はお知らせのポップアップを出し、エクスポートしません
    FBXエクスポートオプションはツールフォルダ内のwizard2_chara.fbxexportpresetの設定を使います
    前提条件: シーン内に複数のキャラモデルがある場合もある。その場合2体にわたって選択はしない
    基本的にMayaのExprt Selectionの挙動に合わせつつ以下の点を取り入れる:
    1. 「非表示のメッシュは除く」> ON の場合は非表示のメッシュはエクスポートしない
    2. 「メッシュ名単位でFBXをエクスポート」> ON の場合
        A. rootノードが選択されていてもシーン名のfbxはエクスポートしない
        B. rootノードと子ノードが選択されていたら選択されている子ノードのみ個別にfbxエクスポート（子ノード名.fbx）
        C. 子ノードが1つだけ選択されていたらfbx名は子ノード名
        D. 子ノードが2つ以上選択されていたら選択されている子ノードのみ個別にfbxエクスポート（子ノード名.fbx）
        E. rootノードだけ選択されている場合はrootノード配下の子メッシュを一個ずつ選択しそれぞれの子ノード名のfbxをエクスポート
    3. 「メッシュ名単位でFBXをエクスポート」> OFF の場合
        A. rootノードが選択されていたらシーン名でfbxをエクスポート
        B. rootノードと子ノードが選択されていたら子が全部入ったシーン名のfbxをエクスポート(Exprt Selectionに準じる)
        C. 子ノードが1つだけ選択されていたらfbx名はノード名
        D. 子ノードが2つ以上選択されていたらfbx名はシーン名
    Args:
        create_parts_fbx (PySide2.QtWidgets.QCheckBox): 「メッシュ名単位でFBXをエクスポート」チェックボックス
        chk_only_visible (PySide2.QtWidgets.QCheckBox): 「非表示のメッシュは除く」チェックボックス
    """
    # ===== Begin Validation =====
    # 実行前にシーン保存の確認等はしないで欲しいとの要望あり
    # 実行前に何も聞かずにシーンの保存をし、実行後は保存していたシーンに戻って欲しいとの要望あり 2022/11/25
    # 「実行前にシーンを保存」チェックボックスを作りデフォルトはONにして欲しいとの要望あり 2023/03/14

    secene_path = cmds.file(q=True, sn=True)
    selection = cmds.ls(sl=True, long=True)
    selected_mesh_transforms = []

    # 選択ノードのrootノードの取得
    selection_roots = chara_utility.get_root_nodes(selection)
    is_selection_root_transform = chara_utility.is_selection_root_transform()

    if is_selection_root_transform:
        if not selection_roots:
            raise ValueError("モデルを選択してからエクスポートしてください")

        elif len(selection_roots) > 1:
            # 2体にわたって選択はしない
            raise ValueError("複数キャラの出力には対応していません")

        selected_mesh_transforms = chara_utility.list_child_mesh_transforms(
            selection[0], except_outline=True
        )
    else:
        selected_mesh_transforms = chara_utility.get_selected_mesh_transforms(
            except_outline=True
        )

    # シーンのプロジェクトパスの確認
    maya_project_path = chara_utility.get_current_project_dir()
    if not maya_project_path:
        # TODO: バッチモードを作るのであればダイアログにしない対応
        cmds.confirmDialog(
            title="Confirm",
            message="シーンパスの取得に失敗しました\n【考えられる対応】" + "\n1.シーンを開いてから実行\n2.シーンエラーを修正してから実行",
            button=["OK"],
        )
        raise ValueError("シーンパスの取得に失敗")

    # 「非表示のメッシュは除く」> ON の場合
    if chk_only_visible.isChecked():
        # 子階層のメッシュをリスト
        for mesh in selected_mesh_transforms:
            if mesh.endswith("_Outline"):
                continue
            if not cmds.getAttr("{}.visibility".format(mesh)):
                # 非表示のメッシュを削除
                cmds.delete(mesh)
                # 選択リストからも抜く
                try:
                    selected_mesh_transforms.remove(mesh)
                    selection.remove(mesh)
                except Exception:
                    pass
        if len(selection) == 0:
            cmds.warning("「非表示のメッシュは除く」がONです\nエクスポートできるノードが選択されていません")
            # 元のシーンを開く
            raise ValueError("エクスポート可能なメッシュが存在しない")

    # 設定チェック
    missing_outline = get_outline(selected_mesh_transforms)
    if len(missing_outline) > 0:
        # 自動で_Outlineは作らないでという要望あり
        cmds.confirmDialog(
            title="Error",
            message="以下のメッシュには_Outlineがありません\n"
            + "_Outlineを作ってから実行してください\n"
            + "\n".join(missing_outline),
            button=["OK"],
        )
        raise ValueError("Outlineメッシュ不在")

    # ===== End Validation =====

    # =============== シーン内での処理開始 ===============
    # この処理でのFBXプリセットを設定する（Maya本体のプリセットは変わらない）
    set_fbx_load_preset()

    # 差分をマージ
    difference_processing(selection_roots, selected_mesh_transforms)

    # _Outlineの法線情報をキャラメッシュのuvセットに入れる
    for mesh in selected_mesh_transforms:
        if not transfer_normal_to_uvset(mesh):
            raise ValueError("transfer_normal_to_uvsetにて問題が発生")

    # 情報を入れ終わったら_Outlineを消す
    child_meshes = chara_utility.list_child_mesh_transforms(selection_roots[0])
    for mesh in child_meshes:
        if mesh.endswith("_Outline"):
            # 参照情報が削除されコピー先の情報もなくなることがあるので念のためヒストリー削除
            cmds.delete(mesh, constructionHistory=True)
            cmds.delete(mesh)

    # フォルダがなかったら作る
    export_folder = create_folder(maya_project_path)

    export_node = []

    # 「メッシュ名単位でFBXをエクスポート」> ON の場合
    if chk_export_parts.isChecked():
        for node in selected_mesh_transforms:
            mesh_name = node.split("|")[-1]
            export_path = get_fbx_file_path(mesh_name, export_folder)
            cmds.select(node)
            mel.eval('FBXExport -f "' + export_path + '" -s')

    # 「メッシュ名単位でFBXをエクスポート」> OFF の場合
    else:
        # 子ノードが1つだけ選択されていたらメッシュ名でfbxをエクスポート
        if not is_selection_root_transform and len(selected_mesh_transforms) == 1:
            mesh_name = selection[0].split("|")[-1]
            export_path = get_fbx_file_path(mesh_name, export_folder)
            export_node.append(selection[0])
        else:
            # シーン名でfbxをエクスポート
            scene_name = os.path.basename(secene_path).split(".")[0]
            export_path = get_fbx_file_path(scene_name, export_folder)
            export_node = selection

        cmds.select(export_node)
        mel.eval('FBXExport -f "' + export_path + '" -s')

    if os.path.exists(export_folder):
        print("FBXを出力しました: " + export_folder)
        subprocess.Popen('explorer "{}"'.format(os.path.normpath(export_folder)))
    # =============== シーン内での処理終了 ===============


def difference_processing(roots: tp.List[str], selected_mesh_transforms: tp.List[str]):
    """差分整理のエントリーポイント

    Args:
        selection_roots (tp.List(str)): 対象のroot

    Raises:
        ValueError: 法線情報の転送失敗時にエラー
    """
    base_meshes = get_base_mesh_transforms(roots)

    if len(base_meshes) > 0:
        dif_data = get_dif_data(base_meshes)
        for base_mesh in dif_data:
            for dif_mesh_name in dif_data[base_mesh]:
                dup_base_mesh = rebind_and_copy_weight([base_mesh], "duplicate", False)[
                    0
                ]
                # 差分のマージメッシュを用意
                combine_mesh = combine_meshes(dup_base_mesh, dif_mesh_name)
                # historyのclean
                rebind_and_copy_weight([combine_mesh], "clean", False)

                # # 複製したbaseメッシュの削除
                if cmds.objExists(dup_base_mesh):
                    cmds.delete(dup_base_mesh)

                dup_base_mesh = cmds.duplicate(
                    base_mesh + "_Outline", rr=True, ic=True
                )[0]
                # マージされたoutlineを用意
                combine_meshes(dup_base_mesh, dif_mesh_name + "_Outline")

            base_mesh = cmds.ls(base_mesh, l=True)[0]
            if base_mesh in selected_mesh_transforms:
                selected_mesh_transforms.remove(base_mesh)
            cmds.delete(base_mesh)


def delete_non_use_shape_orig():
    """不用なorigの削除"""
    shape_node = cmds.ls(type="mesh")
    for shape in shape_node:
        shape_relative = cmds.listRelatives(shape)
        shape_connection = cmds.listConnections(shape)
        if not shape_relative and not shape_connection:
            if "Orig" in shape:
                cmds.delete(shape)


def rebind_and_copy_weight(objects: tp.List[str], mode: str, go_bindpose: bool):
    """ウエイトをコピーして複製

    Args:
        objects:tp.List[str]: objects
        mode (str): "clean" or "duplicate"
        go_bindpose (str): _description_

    Returns:
        tp.List[str]: duplicateしたオブジェクト
    """
    sel_obj = objects
    duplicate_obj = []
    num = 0
    for obj in sel_obj:
        skin_cluster_node = mel.eval("findRelatedSkinCluster {};".format(obj))

        if not skin_cluster_node:
            print("{} is not skin mesh".format(obj))
            return []

        maxInf = cmds.skinCluster(skin_cluster_node, q=True, mi=True)
        connection_joint = cmds.listConnections(
            skin_cluster_node + ".matrix", type="joint"
        )
        if go_bindpose:
            tmpsel = objects
            cmds.select(connection_joint, r=True)
            go_to_bindPose_flag = False
            try:
                cmds.gotoBindPose()
            except:
                go_to_bindPose_flag = True
            cmds.select(tmpsel, r=True)

            if go_to_bindPose_flag:
                print("can't go bindPose. Cancel processing.")
                return []
        duplicate_obj_buff = cmds.duplicate(obj, rr=True)
        duplicate_obj.append(duplicate_obj_buff[0])
        cmds.skinCluster(
            duplicate_obj[num],
            mi=maxInf,
            tsb=True,
            removeUnusedInfluence=False,
            *connection_joint,
        )
        cmds.copySkinWeights(
            obj,
            duplicate_obj[num],
            noMirror=True,
            surfaceAssociation="closestPoint",
            influenceAssociation=["oneToOne", "name"],
        )
        if mode == "clean":
            cmds.delete(obj)
            obj = obj.split("|")[-1]
            cmds.rename(duplicate_obj[num], obj)
        num += 1

    if mode == "clean":
        cmds.select(sel_obj, r=True)
        delete_non_use_shape_orig()
        return []
    else:
        cmds.select(duplicate_obj, r=True)
        delete_non_use_shape_orig()
        return duplicate_obj


def combine_meshes(source: str, target: str):
    """skinを含んだmeshをマージ

    Returns:
        str: マージ後のメッシュを返す
    """
    parent = cmds.listRelatives(source, p=True)[0]
    merged_obj = None
    if len(cmds.ls(cmds.listHistory(target), type="skinCluster")) > 0:
        merged_obj = mel.eval(
            # f"polyUniteSkinned -ch 1 -mergeUVSets 1 -centerPivot ;"
            f"polyUniteSkinned -ch 1 -mergeUVSets 1 {source} {target};"
        )[0]

    else:
        merged_obj = cmds.polyUnite(source, target, mergeUVSets=True, centerPivot=True)[
            0
        ]

    cmds.select(merged_obj, r=True)
    mel.eval('doBakeNonDefHistory( 1, {"prePost" });')

    # ヒストリ削除後、トランスフォームが存在している場合は削除
    if cmds.objExists(target):
        cmds.delete(target)

    # マージされたオブジェクトの名前を変更する
    merged_obj_name = cmds.rename(merged_obj, target.rsplit("|")[-1])

    # 元の親にparent
    cmds.parent(merged_obj_name, parent)
    return merged_obj_name


def create_folder(maya_project_path: str) -> str:
    """
    プロジェクトパスに/fbxを付けた、フォルダを検索
    存在していなければフォルダの作成

    Args:
        maya_project_path (str): プロジェクトパスを取得

    Returns:
        str: 作成したフォルダー
    """
    export_folder = os.path.join(maya_project_path, "fbx")
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    return export_folder


def set_fbx_load_preset():
    """load presetの設定"""
    preset_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".", "wizard2_chara.fbxexportpreset")
    ).replace("\\", "/")
    mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_path))


def get_outline(selected_mesh_transforms):
    missing_outline = []
    for mesh in selected_mesh_transforms:
        if mesh.endswith("_Outline"):
            continue
        # 対応する_Outlineメッシュがあるか
        outline = mesh + "_Outline"
        if not cmds.objExists(outline):
            missing_outline.append(mesh)
    return missing_outline


def get_dif_data(base_meshes: tp.List[str]) -> dict:
    """差分情報をdictで取得

    Args:
        roots (tp.List[str]): 対象となるbase meshの配列

    Returns:
        dict: {base_mesh:[dif_mesh,...]}のdict
    """
    if len(base_meshes) > 0:
        base_data = {}
        for base_mesh in base_meshes:
            # 差分の取得
            meshes = chara_utility.list_child_mesh_transforms(
                cmds.listRelatives(base_mesh, p=True)[0], except_outline=True
            )
            parts_id = base_mesh.replace("_base", "")
            dif_parts = []
            for mesh in meshes:
                if parts_id in mesh and not mesh.endswith("_base"):
                    dif_parts.append(mesh)

            # baseをkeyに、差分を配列のvalueにした変数の作成
            base_data[base_mesh] = dif_parts
    return base_data


def get_fbx_file_path(item, folder_path):
    """item(メッシュ名を想定)の名前でfolder_path配下のfbxパスを返す
    Args:
        item (str): メッシュ名を想定（例: chr0004_bot_swim001）
        folder_path (str): fbxフォルダパス
    Returns:
        str: item名を持ったfbxパス
    """
    export_file_name = item.split("|")[-1]
    export_path = os.path.join(folder_path, export_file_name + ".fbx").replace(
        "\\", "/"
    )
    return export_path


def get_base_mesh_transforms(group_name: str) -> list:
    """指定されたグループ内で、名前が "_base" で終わるメッシュを持つトランスフォームを取得する。

    Args:
        group_name (str): 基本メッシュトランスフォームを検索するグループ名

    Returns:
        list: 基本メッシュトランスフォーム名のリスト
    """

    base_mesh_transforms = []

    # グループのすべてのトランスフォームノードを取得
    all_transforms = cmds.listRelatives(
        group_name, allDescendents=True, type="transform"
    )

    if all_transforms:
        for transform in all_transforms:
            # トランスフォームの名前が '_base' で終わるかどうかを確認する
            if transform.endswith("_base"):
                # トランスフォームの子のシェイプノードを取得する
                shapes = cmds.listRelatives(transform, children=True, shapes=True)

                # トランスフォームの下にメッシュシェイプがあるか確認する
                mesh_shapes = cmds.ls(shapes, type="mesh")
                if mesh_shapes:
                    base_mesh_transforms.append(transform)

    return base_mesh_transforms


def transfer_normal_to_uvset(transform):
    """
    transformの対応_Outlineメッシュから法線情報を取得し、transformのuvセットにxy, zの値として持たせます
    ①メッシュ名で判定はせず、angelringという名前のuvセットがあればそのままにし、ない場合は2番目にtemp0を作る
    ②angelring uvセットがなくてもワーニングは出さない
    uv1: テクスチャーuv(アーティスト手動)
    uv2: angelringのuvセット(アーティスト手動) もしくは未使用のtemp0
    uv3: ____normal_xy アウトラインのxy情報
    uv4: ____normal_z アウトラインのz情報
    Args:
        transform (transform): メッシュのtransformノード
    Returns:
        bool: 最後まで処理が問題なく通ればTrueを返す
    """
    if not transform or transform.endswith("_Outline"):
        cmds.error("transfer_normal_to_uvset 予期しない使い方: " + transform)
        return False
    # ソフトエッジのかかったoutlineのvertexを取得
    outline = transform + "_Outline"
    if not cmds.objExists(outline):
        cmds.error("_Outlineが存在しません: " + transform)
        return False
    cmds.select(transform + "_Outline", r=True)
    cmds.ConvertSelectionToVertices()
    outline_vertexes = cmds.ls(sl=True, flatten=True)
    # 通常のバーテックスを取得
    cmds.select(transform, r=True)
    cmds.ConvertSelectionToVertices()
    model_vertexes = cmds.ls(sl=True, flatten=True)
    # 既存の「temp0」UVSetがあったら削除する (選択しないと削除が上手くいかない)
    # 「temp0」の使用用途が決まったら削除するフロー見直す
    try:
        cmds.select(transform)
        cmds.polyUVSet(uvSet="temp0", delete=True, perInstance=False)
    except Exception:
        pass
    # 既存の「xy」UVSetがあったら削除する (選択しないと削除が上手くいかない)
    try:
        cmds.select(transform)
        cmds.polyUVSet(uvSet="____normal_xy", delete=True, perInstance=False)
    except Exception:
        pass
    # 既存の「z」UVSetがあったら削除する
    try:
        cmds.select(transform)
        cmds.polyUVSet(uvSet="____normal_z", delete=True, perInstance=False)
    except Exception:
        pass
    uv_sets = cmds.polyUVSet(transform, q=True, allUVSets=True, perInstance=False)
    if len(uv_sets) > 1:
        if uv_sets[1] != "angelring":
            userChoice = cmds.confirmDialog(
                title="確認",
                message="想定外のUVセットがあります: "
                + str(transform)
                + "\n\n"
                + "\n".join(uv_sets)
                + "\nこのままエクスポートしますか?",
                button=["OK", "Cancel"],
                defaultButton="Cancel",
                cancelButton="Cancel",
                dismissString="Cancel",
            )
            print("想定外のUVセット: " + str(transform) + "\n\n" + "\n".join(uv_sets))
            if userChoice == "Cancel":
                return False
    if len(model_vertexes) != len(outline_vertexes):
        cmds.confirmDialog(
            title="Error",
            message="モデルと_Outlineモデルの頂点数が違います。 キャンセルします。\n"
            + "モデル: "
            + str(len(model_vertexes))
            + ",  _Outline: "
            + str(len(outline_vertexes)),
            button=["OK"],
        )
        return False
    main_uvset = cmds.polyUVSet(transform, q=True, currentUVSet=True)[0]
    if len(uv_sets) == 1:
        # angelring uvセットがないメッシュはtemp0を2番目のuvセットとして作る
        copied_uvset = cmds.polyUVSet(transform, copy=True)
        cmds.polyUVSet(rename=True, newUVSet="temp0", uvSet=copied_uvset[0])
    # uv3にxy
    copied_uvset = cmds.polyUVSet(transform, copy=True)
    cmds.polyUVSet(rename=True, newUVSet="____normal_xy", uvSet=copied_uvset[0])
    # uv4にz
    copied_uvset = cmds.polyUVSet(transform, copy=True)
    cmds.polyUVSet(rename=True, newUVSet="____normal_z", uvSet=copied_uvset[0])
    z_values = []
    # X, Y値をUVセット「xy」に入れる
    # Memo: uvSetNameで指定してもcurrentUVSetにしておかないとpolyEditUVで指定できない
    cmds.polyUVSet(transform, uvSet="____normal_xy", currentUVSet=True)
    for i in range(len(model_vertexes)):
        outline_vtx = outline_vertexes[i]
        model_vtx = model_vertexes[i]
        cmds.select(outline_vtx, r=True)
        nml = cmds.polyNormalPerVertex(query=True, xyz=True)
        cmds.polyEditUV(
            model_vtx,
            relative=False,
            uvSetName="____normal_xy",
            uValue=nml[0],
            vValue=nml[1],
        )
        z_values.append(nml[2])  # UVセットをいちいち切り替えると遅いので次のループでやる
    # Z値をUVセット「z」に入れる
    cmds.polyUVSet(transform, uvSet="____normal_z", currentUVSet=True)
    for i in range(len(model_vertexes)):
        model_vtx = model_vertexes[i]
        # vValueは今のところ使っていない
        cmds.polyEditUV(
            model_vtx,
            relative=False,
            uvSetName="____normal_z",
            uValue=z_values[i],
            vValue=1.0,
        )
    # 念のため最初のUVセットをcurrentにしておく
    cmds.polyUVSet(transform, uvSet=main_uvset, currentUVSet=True)
    return True
