import maya.cmds as cmds

def get_selected_vertices():
    # 選択された頂点を取得
    return cmds.ls(selection=True, fl=True)

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

def set_influence_weight_to(influence, skin_cluster, value):
    vertices = get_selected_vertices()
    for vertex in vertices:
        cmds.skinPercent(skin_cluster, vertex, transformValue=[(influence, value)])

def create_influence_selector_gui():
    # 既存のウィンドウを削除
    if cmds.window("influenceSelectorWin", exists=True):
        cmds.deleteUI("influenceSelectorWin", window=True)

    # 新しいウィンドウを作成
    window = cmds.window("influenceSelectorWin", title="Influence Selector", widthHeight=(300, 400))
    cmds.scrollLayout('scrollLayout', horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    cmds.columnLayout(adjustableColumn=True)

    selected_vertices = get_selected_vertices()
    if not selected_vertices:
        cmds.text(label="頂点が選択されていません。")
    else:
        # 選択した頂点を再度選択するボタンを追加
        cmds.button(label="選択した頂点を再選択", command=lambda x: cmds.select(selected_vertices, replace=True))
        
        # インフルエンスのボタンを追加
        influences = get_influences_from_selected_vertices()
        if not influences:
            cmds.text(label="影響を与えるインフルエンスが見つかりませんでした。")
        else:
            skin_cluster = cmds.ls(cmds.listHistory(selected_vertices[0]), type='skinCluster')[0]
            for influence in influences:
                cmds.rowLayout(numberOfColumns=4, adjustableColumn=1)
                cmds.button(label=influence, command=lambda x, inf=influence: select_influence(inf))
                cmds.button(label=f"Select vertices", command=lambda x, inf=influence: select_influenced_vertices(inf, skin_cluster))
                cmds.button(label=f"Set to 0 from sel", command=lambda x, inf=influence: set_influence_weight_to(inf, skin_cluster, 0))
                cmds.button(label=f"Set to 1 from sel", command=lambda x, inf=influence: set_influence_weight_to(inf, skin_cluster, 1))
                cmds.setParent('..')

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
