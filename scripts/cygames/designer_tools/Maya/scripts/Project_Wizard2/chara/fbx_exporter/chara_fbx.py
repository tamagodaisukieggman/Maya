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
import re

from ..chara_utility import utility as chara_utility
from . import uv_transfer
from . import weight_copy_model

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

    # export処理
    export_path = None
    try:
        is_chk_export_parts = chk_export_parts.isChecked()
        is_chk_only_visible =chk_only_visible.isChecked()
        export_path = _export_fbx(is_chk_export_parts, is_chk_only_visible)

    except Exception as e:
        traceback.print_exc()
        print("エラー: ", e)

    cmds.file(secene_path, open=True, force=True)

    if export_path:
        return export_path


def _export_fbx(is_chk_export_parts, is_chk_only_visible) -> str:
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

    # blendshapeグループの削除
    delete_blend_shape_groups()

    # rootが_で切られていたら特殊ルールなのでエクスポート時に規定の名前に変更
    if len(selection_roots) == 1:
        root = selection_roots[0]
        if "_" in root:
            selection_roots[0] = root.split("_")[0]
            cmds.rename(root, selection_roots[0])
            selection = cmds.ls(sl=True, long=True)

    translucent_group = None
        
    # 選択ノードの親グループからa1 a2を別グループへ隔離
    if is_chk_export_parts:
        parent_group = None
        if is_selection_root_transform:
            parent_group = selection[0]
        else:
            parent_group = cmds.listRelatives(selection,parent=True,p=True)[0]
            
        if parent_group:
            transforms = cmds.listRelatives(parent_group,c=True,fullPath=True,type="transform")
            translucent_nodes = [node for node in transforms if check_alpha(node)]
            if translucent_nodes:
                translucent_group = cmds.group(translucent_nodes,w=True,n=f"{parent_group}__temp_translucent")

    cmds.select(selection,r=True)
    
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
    if is_chk_only_visible:
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
        result = cmds.confirmDialog(
            title="Warning",
            message="以下のメッシュには_Outlineがありません\n"
            + "fbxにOutlinbeが含まれない状態でエクスポートしますか？\n"
            + "\n".join(missing_outline),
            button=["Yes", "No"],
        )
        if result == "No":
            raise ValueError("Outlineメッシュ不在")
        
    # ===== End Validation =====

    # =============== シーン内での処理開始 ===============
    # この処理でのFBXプリセットを設定する（Maya本体のプリセットは変わらない）
    set_fbx_load_preset()

    # 差分をマージ
    difference_merge(selection_roots, selected_mesh_transforms)

    convert_outline_meshes = [lp for lp in selected_mesh_transforms if lp not in missing_outline ]

    # Outlineを所有していて書き出す場合のみ
    if convert_outline_meshes:
        # _Outlineの法線情報をキャラメッシュのuvセットに入れる
        if not convert_outline_info(convert_outline_meshes, selection_roots):
            raise ValueError("不正なフェースが存在する")

    # =============== シーン内での処理終了 ===============

    # フォルダがなかったら作る
    export_folder = create_folder(maya_project_path)

    export_node = []
    export_paths = []

    for depth1_node in cmds.listRelatives(
        selection_roots[0], c=True, type="transform", fullPath=True
    ):
        if "offSet_" in depth1_node:
            export_node.append(depth1_node)

    if translucent_group:
        all_translucent_meshs = cmds.listRelatives(translucent_group,c=True,type="transform")
        origine_group = translucent_group.replace("__temp_translucent","")
        cmds.parent(all_translucent_meshs,origine_group)

    # 「メッシュ名単位でFBXをエクスポート」> ON の場合
    if is_chk_export_parts:
        for node in selected_mesh_transforms:
            current_export_nodes = export_node.copy()
            short_name = chara_utility.get_short_name(node)
             
            # 半透明メッシュの追加
            translucent_nodes = get_current_translucent_nodes(node)
            if translucent_nodes:
                current_export_nodes.extend(translucent_nodes)

            export_path = get_fbx_file_path(short_name, export_folder)
            current_export_nodes.append(node)

            cmds.select(current_export_nodes,r=True)
            # bones = get_bones(node)

            # if len(bones) == 1:
            #     reroot_nodes = current_export_nodes.copy()
            #     reroot_nodes = [node for node in reroot_nodes if "offSet_" not in node]
            #     reroot_nodes = reroot_one_joint_meshes(bones[0],reroot_nodes)
                
            #     current_export_nodes.remove()

            mel.eval('FBXExport -f "' + export_path + '" -s')
            export_paths.append(export_path)

    # 「メッシュ名単位でFBXをエクスポート」> OFF の場合
    else:
        # 子ノードが1つだけ選択されていたらメッシュ名でfbxをエクスポート
        if not is_selection_root_transform and len(selected_mesh_transforms) == 1:
            short_name = chara_utility.get_short_name(node)
            export_path = get_fbx_file_path(short_name, export_folder)
            export_node.append(selection[0])

            # 半透明メッシュの追加
            translucent_nodes = get_current_translucent_nodes(selection[0])
            if translucent_nodes:
                export_node.extend(translucent_nodes)

        else:
            # シーン名でfbxをエクスポート
            scene_name = os.path.basename(secene_path).split(".")[0]
            export_path = get_fbx_file_path(scene_name, export_folder)
            export_node = selection

        cmds.select(export_node)
        
        mel.eval('FBXExport -f "' + export_path + '" -s')
        export_paths.append(export_path)

    if os.path.exists(export_folder):
        print("FBXを出力しました: " + export_folder)
        os.startfile(os.path.normpath(export_folder))

    return export_paths

def get_current_translucent_nodes(node:str) -> tp.List[str]:
    """nodeに対応する半透明オブジェクトを取得

    Args:
        node (str): 対象のノード名

    Returns:
        tp.List[str]: 半透明オブジェクト名の配列
    """
    short_name = chara_utility.get_short_name(node)
    secene_path = cmds.file(q=True, sn=True)
    scene_name = os.path.basename(secene_path).split(".")[0]
    parts_id = short_name.replace(f"{scene_name}_","")
    all_translucent_node = get_translucent_mesh(node)
    rtn = []
    for translucent_node in all_translucent_node:
        if "_base_" in translucent_node:
            duplicate_base = rebind_and_copy_weight([translucent_node],mode="duplicate",go_bindpose=False)
            translucent_short_name = chara_utility.get_short_name(translucent_node)
            fixed_base_node = cmds.rename(duplicate_base,translucent_short_name.replace("_base_",f"_{parts_id}_"))
            rtn.append(fixed_base_node)
        else:
            rtn.append(translucent_node)
    return rtn

def get_translucent_mesh(export_node:str) -> tp.List[str]:
    """export_nodeと同階層の半透明メッシュを検索

    Args:
        export_node (str): 対象となる
    """
    rtn = []
    parent_node = cmds.listRelatives(export_node,p=True)[0]
    all_translucent_nodes = cmds.listRelatives(parent_node,c=True,fullPath=True)
    for node in all_translucent_nodes:       
        if check_alpha(node):
            if export_node in node:
                rtn.append(node)
            elif "_base_" in node:
                rtn.append(node)
    return rtn
   
def delete_blend_shape_groups():
    "シーン内に存在しているブレンドシェイプ作成用メッシュを削除"
    blend_shape_groups = cmds.ls("*shapetarget", type="transform")
    if blend_shape_groups:
        cmds.delete(blend_shape_groups)


def convert_outline_info(selected_mesh_transforms, selection_roots):
    for mesh in selected_mesh_transforms:
        try:
            execute_uv_transfer(mesh)
        except Exception as e:
            cmds.confirmDialog( title='Warning', message='不正なフェースが存在します。\n詳細はチェッカーでご確認ください。', button=['Yes'], defaultButton='Yes', cancelButton='Yes', dismissString='Yes' )
            return False

    # 情報を入れ終わったら_Outlineを消す
    child_meshes = chara_utility.list_child_mesh_transforms(selection_roots[0])
    for mesh in child_meshes:
        if mesh.endswith("_Outline"):
            # 参照情報が削除されコピー先の情報もなくなることがあるので念のためヒストリー削除
            cmds.delete(mesh, constructionHistory=True)
            cmds.delete(mesh)

    return True

def execute_uv_transfer(mesh):
    _weight_copy_model = weight_copy_model.WeightCopyModel(mesh)
    _weight_copy_model.copy_skin_weight()
    duplicate_object_name = _weight_copy_model.src_object

    _uv_transfer = uv_transfer.HQNormalUVTransfer()
    _uv_transfer.setup(mesh, duplicate_object_name)
    _uv_transfer.transfer_normal_to_uvset()

    _weight_copy_model.copy_skin_weight(duplicate_object_name, mesh)
    cmds.delete(duplicate_object_name)


def difference_merge(roots: tp.List[str], selected_mesh_transforms: tp.List[str]):
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

def check_alpha(s):
    # 末尾が任意の文字列に続いて "_a" と一桁の数値で終わるかどうかをチェックする正規表現パターン
    pattern = r'.*_a[0-9]$\Z'
    
    # re.searchを使用して、文字列がパターンに一致するかどうかをチェック
    if re.search(pattern, s):
        return True
    else:
        return False
    
def reroot_one_joint_meshes(parent_joint:str,children_meshes:tp.List[str]):
    detach_all_skins(children_meshes)
    reroot_nodes = cmds.parent(children_meshes,parent_joint)
    return reroot_nodes

def get_shapes(transforms:tp.List[str]):
    # transformノードの下のshapeを取得します。
    # 全てのshapeをループします。
    all_shapes = []
    for transform in transforms:
        shapes = cmds.listRelatives(transform, shapes=True)
        all_shapes.extend(shapes)
    return all_shapes

def detach_all_skins(transforms):
    skins = cmds.ls(type='skinCluster')
    shapes = get_shapes(transforms)
    for skin in skins:
        geometry = cmds.skinCluster(skin, query=True, geometry=True)
        if geometry:
            for mesh_name in shapes:
                if mesh_name in geometry:
                    cmds.skinCluster(skin, edit=True, unbind=True)

def get_bones(transform) -> tp.List[str]:
    """
    与えられたトランスフォームノードの子供のシェイプにスキニングされた全てのボーンを取得します。

    Args:
    transform (str): ボーンを取得するメッシュのトランスフォームノード名。

    Returns:
    list: ボーンのリスト
    """
    # transformノードの下のshapeを取得します。
    shapes = get_shapes([transform])
    # ボーンを格納するリストを初期化します。
    bones = []
    # 全てのshapeをループします。
    for mesh in shapes:
        # シーン内のskinClusterのリストを取得します。
        skin_clusters = cmds.ls(type='skinCluster')
        for skin in skin_clusters:
            # skinClusterによって影響を受けるジオメトリを取得します。
            geometry = cmds.skinCluster(skin, query=True, geometry=True)
            # 我々のメッシュがジオメトリの一部であるかを確認します。
            if mesh in geometry:
                # このskinClusterの影響を受けるボーンをボーンリストに追加します。
                bones.extend(cmds.skinCluster(skin, query=True, inf=True))
    return bones