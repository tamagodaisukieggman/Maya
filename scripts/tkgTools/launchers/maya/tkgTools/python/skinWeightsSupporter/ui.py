# -*- coding: utf-8 -*-
import maya.cmds as cmds

import re
import traceback

def get_selected_vertices():
    # 選択された頂点を取得
    sel = cmds.ls(os=True)
    sel_buf = []
    for obj in sel:
        if cmds.objectType(obj) == 'transform':
            sh = cmds.listRelatives(obj, s=True, f=True) or []
            if sh:
                vertices = cmds.ls(cmds.polyListComponentConversion(sh[0], toVertex=True), flatten=True)
                [sel_buf.append(v) for v in vertices]
        else:
            sel_buf.append(obj)

    return sel_buf

def get_influences_from_selected_vertices():
    selected_vertices = get_selected_vertices()
    if not selected_vertices:
        cmds.warning("頂点を選択してください。")
        return []
    
    influences = set()
    for vertex in selected_vertices:
        skin_cluster = cmds.ls(cmds.listHistory(vertex), type='skinCluster')
        if skin_cluster:
            skin_cluster = skin_cluster[0]
            vertex_influences = cmds.skinPercent(skin_cluster, vertex, query=True, transform=None)
            for influence in vertex_influences:
                weight = cmds.skinPercent(skin_cluster, vertex, transform=influence, query=True)
                if weight > 0:
                    influences.add(influence)
    
    return list(influences)

def get_vertices_influenced_by(influence, skin_cluster):
    vertices = cmds.ls(cmds.polyListComponentConversion(cmds.skinCluster(skin_cluster, query=True, geometry=True), toVertex=True), flatten=True)
    influenced_vertices = []
    for vertex in vertices:
        weight = cmds.skinPercent(skin_cluster, vertex, transform=influence, query=True)
        if weight > 0:
            influenced_vertices.append(vertex)
    return influenced_vertices

def get_soft_selection():
    # 現在の選択を取得
    selection = om2.MGlobal.getRichSelection()
    richList = selection.getSelection()
    iter = om2.MItSelectionList(richList)

    softSelectionData = []

    while not iter.isDone():
        # 選択されたオブジェクトのDAGパスとコンポーネントを取得
        try:
            dagPath, component = iter.getComponent()
        except:
            iter.next()
            continue

        if component.isNull() or not dagPath.node().hasFn(om2.MFn.kMesh):
            iter.next()
            continue

        # 頂点の選択重みを取得
        vertexComponent = om2.MFnSingleIndexedComponent(component)
        for i in range(vertexComponent.elementCount):
            idx = vertexComponent.element(i)
            weight = vertexComponent.weight(i).influence

            # ノード名と頂点インデックスを取得
            nodeName = dagPath.fullPathName()
            softSelectionData.append((f"{nodeName}.vtx[{idx}]", weight))

        iter.next()

    return softSelectionData

def set_influence_weight_to(influence, skin_cluster, value):
    vertices = get_selected_vertices()
    for vertex in vertices:
        cmds.skinPercent(skin_cluster, vertex, transformValue=[(influence, value)])

def find_controls_by_name(name):
    # すべてのUIコントロールオブジェクトをリストアップ
    all_controls = cmds.lsUI(controls=True)
    
    # 指定された名前に一致するコントロールをリストに追加
    matching_controls = [control for control in all_controls if name in control]
    
    return matching_controls

def set_weight_from_soft_selection(set_zero_others=None):
    matching_controls = find_controls_by_name("_cbx")

    if matching_controls:
        for inf_cbx in matching_controls:
            inf_cbx_sts = cmds.checkBox(inf_cbx, q=True, value=False)
            if inf_cbx_sts:
                influence = re.sub(r'_cbx+$', '', inf_cbx)
                selected_vertices = get_selected_vertices()
                skin_cluster = cmds.ls(cmds.listHistory(selected_vertices[0]), type='skinCluster')[0]

                softSelectionData = get_soft_selection()

                if set_zero_others:
                    inf_vertices = get_vertices_influenced_by(influence, skin_cluster)

                    for vertex in inf_vertices:
                        cmds.skinPercent(skin_cluster, vertex, transformValue=[(influence, 0)])

                for vertex, value in softSelectionData:
                    cmds.skinPercent(skin_cluster, vertex, transformValue=[(influence, value)])


def filter_buttons(influences):
    # テキストフィールドから入力を取得
    filter_text = cmds.textField('filterField', query=True, text=True)
    
    # 各ボタンをチェックし、フィルターテキストが含まれるかどうかで表示/非表示を切り替え
    for influence in influences:
        if filter_text in influence or filter_text == '':
            cmds.control(influence+'_row_lay', edit=True, visible=True)

        else:
            cmds.control(influence+'_row_lay', edit=True, visible=False)

def set_liw(liw_sts=False):
    mesh = cmds.ls(os=True)
    if mesh:
        mesh = mesh[0]
    else:
        return

    # Get the skin cluster of the mesh
    skin_cluster = cmds.ls(cmds.listHistory(mesh), type='skinCluster')[0]

    # Get the influences (joints) affecting the skin
    influences = cmds.skinCluster(skin_cluster, query=True, inf=True)

    for inf in influences:
        cmds.setAttr(inf + '.liw', liw_sts)

    try:
        mel.eval('artAttrSkinSetPaintMode 1;')
    except:
        print(traceback.format_exc())

def select_inf_from_tool(influence, influences):
    mel.eval('ArtPaintSkinWeightsToolOptions;')
    mel.eval('artAttrSkinJointMenu( "artJoinListPopupMenu", "artAttrSkinPaintCtx" );')
    for off_inf in influences:
        mel.eval('artSkinInflListChanging "{}" 0;'.format(off_inf))

    mel.eval('artSkinInflListChanging "{}" 1;'.format(influence))
    mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')


def set_trs_ui(obj, pos, rot):
    # Translate X, Y, Z
    cmds.floatFieldGrp(obj+"_translateFields",
                       e=True,
                       value1=pos[0],
                       value2=pos[1],
                       value3=pos[2])

    # Rotate X, Y, Z
    cmds.floatFieldGrp(obj+"_rotateFields",
                       e=True,
                       value1=rot[0],
                       value2=rot[1],
                       value3=rot[2])

def get_pos_rot(obj):
    pos = cmds.getAttr(obj+'.t')[0]
    rot = cmds.getAttr(obj+'.r')[0]
    return pos, rot

def applyTransform(influence):
    # 入力されたオブジェクト名を取得
    # objectName = cmds.control(influence+"_btn", query=True, label=True)

    # Translateの値を取得
    translateValues = cmds.floatFieldGrp(influence+"_translateFields", query=True, value=True)
    
    # Rotateの値を取得
    rotateValues = cmds.floatFieldGrp(influence+"_rotateFields", query=True, value=True)
    
    if cmds.objExists(influence):
        # Translateを適用
        cmds.setAttr(f"{influence}.translateX", translateValues[0])
        cmds.setAttr(f"{influence}.translateY", translateValues[1])
        cmds.setAttr(f"{influence}.translateZ", translateValues[2])

        # Rotateを適用
        cmds.setAttr(f"{influence}.rotateX", rotateValues[0])
        cmds.setAttr(f"{influence}.rotateY", rotateValues[1])
        cmds.setAttr(f"{influence}.rotateZ", rotateValues[2])

        pos, rot = get_pos_rot(influence)
        set_trs_ui(influence, pos, rot)


def reset_trs(obj, pos, rot):
    cmds.setAttr(obj+'.t', *pos)
    cmds.setAttr(obj+'.r', *rot)

    set_trs_ui(obj, pos, rot)

def get_skin_clusters_and_mesh_from_joint():
    # 選択したジョイントを取得
    selected_joints = cmds.ls(selection=True, type='joint')
    
    if not selected_joints:
        cmds.warning("ジョイントを選択してください。")
        return

    meshes = []
    for joint in selected_joints:
        # ジョイントに影響されるスキンクラスターを取得
        skin_clusters = cmds.listConnections(joint, d=True, scn=True, type='skinCluster')
        if not skin_clusters:
            continue

        skin_clusters = list(set(skin_clusters))

        for skin_cluster in skin_clusters:
            # スキンクラスターに影響されるメッシュを取得
            geometry = cmds.skinCluster(skin_cluster, query=True, geometry=True)

            geo_pa = cmds.listRelatives(geometry[0], p=True, f=True) or []
            if geo_pa:
                meshes.append(geo_pa[0])

    return meshes

def get_meshes_from_joints():
    # スクリプトを実行
    meshes = get_skin_clusters_and_mesh_from_joint()
    if meshes:
        cmds.select(meshes, r=True)

def menu_bar(parent=None):
    # メニューバーの作成
    cmds.menuBarLayout(parent=parent)

    # メニューの作成
    cmds.menu(label="File")
    cmds.menuItem(label="New Scene")
    cmds.menuItem(label="Open Scene")
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Save Scene")
    cmds.menuItem(label="Save Scene As...")

    cmds.menu(label="Edit")
    cmds.menuItem(label="Lock All Influences", c='set_liw(liw_sts=True)')
    cmds.menuItem(label="Unlock All Influences", c='set_liw(liw_sts=False)')
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Select Meshes from Joints", c='get_meshes_from_joints()')
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Set Weight From SoftSelection", c='set_weight_from_soft_selection()')
    cmds.menuItem(label="Set Weight From SoftSelection(Set 0 Others)", c='set_weight_from_soft_selection(True)')
    cmds.menuItem(divider=True)

    cmds.menu(label="Help")
    cmds.menuItem(label="About Maya")

def create_influence_selector_gui():
    # 既存のウィンドウを削除
    win_obj = "influenceSelectorWin"
    if cmds.window(win_obj, exists=True):
        cmds.deleteUI(win_obj, window=True)

    # 新しいウィンドウを作成
    window = cmds.window(win_obj, title="Influence Selector", widthHeight=(300, 400))
    cmds.scrollLayout('scrollLayout', horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    col_lay = cmds.columnLayout(adjustableColumn=True)
    menu_bar(parent=col_lay)

    selected_vertices = get_selected_vertices()
    if not selected_vertices:
        cmds.text(label="頂点が選択されていません。")
    else:
        # 選択した頂点を再度選択するボタンを追加
        cmds.button(label="選択した頂点を再選択", command=lambda x: cmds.select(selected_vertices, replace=True))

        cmds.textField('filterField')

        # インフルエンスのボタンを追加
        influences = get_influences_from_selected_vertices()
        influences.sort()

        if not influences:
            cmds.text(label="影響を与えるインフルエンスが見つかりませんでした。")
        else:
            skin_cluster = cmds.ls(cmds.listHistory(selected_vertices[0]), type='skinCluster')[0]
            for influence in influences:
                cmds.rowLayout(influence+'_row_lay', numberOfColumns=5, adjustableColumn=1)
                cmds.columnLayout(adjustableColumn=True)

                button_width = len(influence) * 8
                cmds.button(influence+'_btn',
                            label=influence,
                            command=lambda x, inf=influence: select_influence(inf),
                            width=button_width)

                pos, rot = get_pos_rot(influence)

                cmds.button(label='Reset', c='reset_trs("{}", {}, {})'.format(influence, pos, rot))

                # Translate X, Y, Z
                cmds.floatFieldGrp(influence+"_translateFields",
                                   numberOfFields=3,
                                   label="Translate",
                                   value1=pos[0],
                                   value2=pos[1],
                                   value3=pos[2],
                                   pre=5,
                                   dc='applyTransform("{}")'.format(influence))

                # Rotate X, Y, Z
                cmds.floatFieldGrp(influence+"_rotateFields",
                                   numberOfFields=3,
                                   label="Rotate",
                                   value1=rot[0],
                                   value2=rot[1],
                                   value3=rot[2],
                                   pre=5,
                                   dc='applyTransform("{}")'.format(influence))

                cmds.setParent('..')
                cmds.columnLayout(adjustableColumn=True)
                cmds.button(influence+'_sel_vtx_btn', label=f"Select vertices", command=lambda x, inf=influence: select_influenced_vertices(inf, skin_cluster))
                cmds.button(influence+'_sel_inf_btn', label=f"Select influence", c='select_inf_from_tool("{}", {})'.format(influence, influences))
                cmds.button(influence+'_set_w_0_btn', label=f"Set Weights 0", command=lambda x, inf=influence: set_influence_weight_to(inf, skin_cluster, 0))
                cmds.button(influence+'_set_w_1_btn', label=f"Set Weights 1", command=lambda x, inf=influence: set_influence_weight_to(inf, skin_cluster, 1))
                cmds.setParent('..')
                cmds.checkBox(influence+'_cbx', label="Check", value=False)
                cmds.setParent('..')

        cmds.textField('filterField', e=True, tcc='filter_buttons({})'.format(influences))

    cmds.setParent('..')
    cmds.showWindow(window)

def select_influence(influence):
    cmds.select(influence, replace=True)

def select_influenced_vertices(influence, skin_cluster):
    vertices = get_vertices_influenced_by(influence, skin_cluster)
    if vertices:
        cmds.select(vertices, replace=True)
    else:
        cmds.warning(f"No vertices influenced by {influence} with weight > 0")

# ウィンドウを開く
create_influence_selector_gui()
