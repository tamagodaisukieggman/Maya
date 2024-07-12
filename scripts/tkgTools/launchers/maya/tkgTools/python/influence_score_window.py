import maya.cmds as cmds
import maya.mel as mel


def get_inf_ui_objects():
    ui_name = 'theSkinClusterInflList'
    inf_list_object = cmds.control(ui_name, q=True, fpn=True)
    infs = cmds.treeView(inf_list_object, query=True, children=True)

    return inf_list_object, infs

def apply_value_to_all_objects(text_scroll_list):
    inf_list_object, infs = get_inf_ui_objects()
    all_items = cmds.textScrollList(text_scroll_list, query=True, ai=True)
    cmds.treeView(inf_list_object, e=True, cs=True)
    if all_items:
        for item in all_items:
            cmds.treeView(inf_list_object, e=True, si=[item, True])

def get_vertex_influence_dict_and_scores():
    # Get selected vertices
    verticies = cmds.ls(os=True, fl=True)
    selection = [v for v in verticies if cmds.objectType(v) == 'mesh']

    if not selection:
        cmds.error("No vertices selected.")
    
    # Initialize dictionaries to store results
    vertex_influence_dict = {}
    influence_scores = {}

    for vertex in selection:
        # Get the skin cluster
        skin_cluster = cmds.ls(cmds.listHistory(vertex), type='skinCluster')
        if not skin_cluster:
            cmds.error("No skin cluster found on the selected vertices.")
        
        skin_cluster = skin_cluster[0]
        
        # Get influences from the skin cluster
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
        
        # Get skin weights of the selected vertices
        weights = cmds.skinPercent(skin_cluster, vertex, query=True, value=True)
        
        # Filter influences with non-zero weights
        influence_weights = [(influence, weight) for influence, weight in zip(influences, weights) if weight > 0]
        
        # Sort influences by weight in descending order
        sorted_influence_weights = sorted(influence_weights, key=lambda x: x[1], reverse=True)
        
        # Create a list of sorted influences
        sorted_influences = [influence for influence, weight in sorted_influence_weights]
        
        # Store vertices as keys in the dictionary
        vertex_influence_dict[vertex] = sorted_influences
        
        # Score influences based on rank
        for rank, influence in enumerate(sorted_influences):
            score = 10 - rank  # 1st place gets 10 points, 2nd gets 9 points, 3rd gets 8 points, etc.
            if influence not in influence_scores:
                influence_scores[influence] = 0
            influence_scores[influence] += score

    # Sort influences by score in descending order
    sorted_influences_by_score = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)
    
    return vertex_influence_dict, sorted_influences_by_score

def on_select(text_scroll_list):
    selected_items = cmds.textScrollList(text_scroll_list, query=True, selectItem=True)
    if selected_items:
        cmds.select(selected_items, replace=True)
    else:
        cmds.select(clear=True)

def vertex_influence_score_list(vertex_influence_dict, sorted_influences_by_score):
    # Get selected objects
    influence_ranks = [inf_score[0] for inf_score in sorted_influences_by_score]
    
    # Delete existing window if any
    title = 'VertexInfluenceScoreWindow'
    if cmds.window(title, exists=True):
        cmds.deleteUI(title, window=True)
    
    # Create a new window
    window = cmds.window(title, title="InfluenceScoreRanking", widthHeight=(300, 200))
    cmds.columnLayout(adjustableColumn=True)
    
    # Create textScrollList
    text_scroll_list = cmds.textScrollList(numberOfRows=8, allowMultiSelection=True, append=influence_ranks)
    
    # Set callback for selection event
    cmds.textScrollList(text_scroll_list, edit=True, selectCommand=lambda: on_select(text_scroll_list))
    
    # Add button to apply value
    cmds.button(label="Select Infs", command=lambda _: apply_value_to_all_objects(text_scroll_list))
    
    # Show window
    cmds.showWindow(window)

def influence_score_window():
    mel.eval('ArtPaintSkinWeightsToolOptions')
    vertex_influence_dict, sorted_influences_by_score = get_vertex_influence_dict_and_scores()
    vertex_influence_score_list(vertex_influence_dict, sorted_influences_by_score)

def show():
    influence_score_window()
