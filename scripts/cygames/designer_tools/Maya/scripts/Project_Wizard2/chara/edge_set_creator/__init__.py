from __future__ import division, print_function, absolute_import

from . import controller
from .app import EdgeSetDataExporter
from .data import EdgeSetType


def show(*arg):
    """Windowの起動"""
    global wiz2_edge_set_creator_controller
    try:
        wiz2_edge_set_creator_controller.close_ui()
    except Exception:
        pass
    wiz2_edge_set_creator_controller = controller.EdgeSetController()
    wiz2_edge_set_creator_controller.show_ui()


def export_edge_set_data(edge_set_type_str: str):
    edge_set_type = None
    if edge_set_type_str == "hair":
        edge_set_type = EdgeSetType.HAIR
    elif edge_set_type_str == "neck":
        edge_set_type = EdgeSetType.NECK
    elif edge_set_type_str == "waist":
        edge_set_type = EdgeSetType.WAIST
    elif edge_set_type_str == "face_hair":
        edge_set_type = EdgeSetType.FACE_HAIR

    if edge_set_type:
        EdgeSetDataExporter.export_edge_set_data(edge_set_type)
        print(f"{edge_set_type_str}で書き出し")
