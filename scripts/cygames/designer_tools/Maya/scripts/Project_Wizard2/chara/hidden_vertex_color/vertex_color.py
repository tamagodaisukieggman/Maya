import maya.cmds as cmds
import maya.mel as mel


def set_vertex_color_for_shoes(type):
    """
    足先非表示の頂点カラー設定
    選択しているフェイスに頂点カラーBをセットします
    Args:
        type (str): 低い靴用, 中間の靴用, 高い靴用, 消さない部分用 の4種類
    """
    color_by_type = {'パンプス用': 0.1,
                     '低い靴用': 0.2,
                     '中間の靴用': 0.3,
                     '高い靴用': 0.4,
                     '消さない部分用': 1}
    value = color_by_type.get(type)
    if value:
        try:
            cmds.polyColorPerVertex(b=value)
        except Exception:
            pass


def paint_vertex_color_tool_options():
    mel.eval("PaintVertexColorToolOptions;")


def toggle_display_colors_attr():
    selections = cmds.ls(sl=True)
    if selections:
        if cmds.objectType(selections[0]) != "transform":
            cmds.select(selections[0].split('.')[0], r=True)
    cmds.selectMode(object=True)
    mel.eval("ToggleDisplayColorsAttr;")
