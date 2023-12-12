# -*- coding: cp932 -*-
#===============================================
#
# フェースに物理マテリアルラベルを表示
#
# Fujita Yukihiro
#
#===============================================

# import maya.cmds as cmds
from maya import cmds

def show_phy_material_labels() -> None:
    """ フェースに物理マテリアルラベルを表示 """

    # アノテーションノードグループ名
    LABELS_NODE_NAME = "_physics_mat_labels"

    # すでに存在すれば削除
    if cmds.objExists(LABELS_NODE_NAME):
        cmds.delete(LABELS_NODE_NAME)

    # 選択を取得
    sel = cmds.ls(selection=True)

    # 選択ノードのすべての子孫のうち、mesh を取得
    all_mesh_nodes: list[str] = cmds.listRelatives(sel, fullPath=True, allDescendents=True, type="mesh", noIntermediate=True)

    if all_mesh_nodes is None:
        all_mesh_nodes = []

    # 選択しているメッシュノードを取得
    sel_meshes: list[str] = cmds.ls(selection=True, long=True, type="mesh")

    # 全てのメッシュノードリストに選択メッシュノードを追加
    all_mesh_nodes.extend(sel_meshes)

    # リストから重複を削除
    all_mesh_nodes = list(set(all_mesh_nodes))

    # 全てのターゲットメッシュノード
    target_mesh_nodes = []

    for mesh_node in all_mesh_nodes:

        # collision ノード以下にあるメッシュノードなら
        if "|collision|" in mesh_node:

            # ターゲットメッシュノードリストに追加
            target_mesh_nodes.append(mesh_node)

    # ターゲットメッシュのすべてのフェースを取得
    target_faces: list[str] = cmds.polyListComponentConversion(target_mesh_nodes, toFace=True)

    if len(target_faces) != 0:
        target_faces = cmds.filterExpand(target_faces, selectionMask=34)

    # 選択しているフェースを取得
    sel_faces = cmds.filterExpand(selectionMask=34)

    # 選択しているフェースがある場合
    if sel_faces is not None:

        for face in sel_faces:

            # フェースからメッシュノードを取得
            mesh_node = cmds.listRelatives(face, parent=True, fullPath=True)

            # collision ノード以下にあるメッシュノードなら
            if "|collision|" in mesh_node[0]:

                # ターゲットメッシュノードリストに追加
                target_mesh_nodes.append(mesh_node[0])

                # ターゲットフェースリストに追加
                target_faces.append(face)

    # リストから重複を削除
    target_mesh_nodes = list(set(target_mesh_nodes))

    # 対象メッシュノードがなければ終了
    if len(target_mesh_nodes) == 0:
        return

    # ハイライトされているノードを取得
    hl_nodes = cmds.ls(hilite=True)

    # アサインされているマテリアルを選択
    cmds.hyperShade(shaderNetworksSelectMaterialNodes=True)

    # 選択マテリアルを取得
    sel_materials = cmds.ls(selection=True, materials=True)

    # 作成したアノテーションノード
    ann_nodes = []

    for mat in sel_materials:

        # 物理マテリアルがアサインされていれば
        if cmds.attributeQuery("phyMaterialName", node=mat, exists=True):

            # マテリアルがアサインされている物を選択
            cmds.hyperShade(objects=mat)

            # 選択しているメッシュノードを取得
            assigned_meshes = cmds.ls(selection=True, long=True, type="mesh")

            # ターゲットメッシュノードとアサインされているメッシュノードの積集合
            meshes = set(target_mesh_nodes) & set(assigned_meshes)

            if meshes is None:
                meshes = []

            else:
                meshes = list(meshes)

            # 選択しているフェースを取得
            assigned_faces = cmds.filterExpand(selectionMask=34)

            if assigned_faces is None:
                assigned_faces = []

            # 積集合の結果のメッシュノードをフェースに変換
            assigned_meshes_faces = cmds.polyListComponentConversion(meshes, toFace=True)

            assigned_faces.extend(assigned_meshes_faces)

            # リストをフラット化
            assigned_faces = cmds.ls(assigned_faces, flatten=True)

            # 重複を削除
            assigned_faces = list(set(assigned_faces))

            # ターゲットメッシュノードとアサインされているメッシュノードの積集合
            faces = set(target_faces) & set(assigned_faces)


            if faces is None:
                faces = []

            else:
                faces = list(faces)

            # フェースを頂点リストに変換
            vertex = cmds.polyListComponentConversion(faces, toVertex=True)

            # 頂点リストをフラット化
            vertex = cmds.filterExpand(vertex, selectionMask=31)

            # 作成するアノテーションノードの位置
            ann_pos = [0, 0, 0]

            for v in vertex:

                # 頂点位置を取得
                pos: list = cmds.pointPosition(v, world=True)

                # フェースを構成する頂点位置座標を合計
                ann_pos[0] += pos[0]
                ann_pos[1] += pos[1]
                ann_pos[2] += pos[2]

            # フェースを構成する頂点数
            vertex_count = len(vertex)

            # フェースの中心位置を取得
            ann_pos[0] = ann_pos[0] / vertex_count
            ann_pos[1] = ann_pos[1] / vertex_count
            ann_pos[2] = ann_pos[2] / vertex_count

            # アノテーションノードのカラーを設定（明るければ暗く、暗ければ明るく）
            col = cmds.getAttr(mat + ".color")
            col = list(col[0])

            if (col[0] + col[1] + col[2]) / 3 >= 0.5:
                col[0] = col[0] * 0.2
                col[1] = col[1] * 0.2
                col[2] = col[2] * 0.2

            else:
                col[0] = 1 - (1 - col[0]) * 0.8
                col[1] = 1 - (1 - col[1]) * 0.8
                col[2] = 1 - (1 - col[2]) * 0.8

            # アノテーションノードのテキストを設定
            ann_text = cmds.getAttr(mat + ".phyMaterialName")

            # アノテーションノードを作成
            ann_node = cmds.annotate(faces[0], text=ann_text, point=ann_pos)

            # アノテーションノードの矢印をオフ
            cmds.setAttr(ann_node + ".displayArrow", False)

            # オーバーライドカラーを設定
            cmds.setAttr(ann_node + ".overrideEnabled", True)
            cmds.setAttr(ann_node + ".overrideRGBColors", True)
            cmds.setAttr(ann_node + ".overrideColorRGB", col[0], col[1], col[2], type="double3", clamp=True)

            # アノテーションノードリストに追加
            ann_nodes.append(cmds.listRelatives(ann_node, parent=True)[0])

    if len(ann_nodes) != 0:

        # グループノード作成
        cmds.group(empty=True, name=LABELS_NODE_NAME)

        # アウトライナで非表示に
        cmds.setAttr(LABELS_NODE_NAME + ".hiddenInOutliner", True)

        # 作成したアノテーションノードをグループノードの子に
        cmds.parent(ann_nodes, LABELS_NODE_NAME)

    # 選択を復元
    cmds.hilite(hl_nodes, replace=True)
    cmds.select(sel, replace=True)
