# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function
from .controller import CompareBoneToolController


def show(*args):
    global compare_bone_controller
    try:
        compare_bone_controller.close_ui()
    except Exception:
        pass
    compare_bone_controller = CompareBoneToolController()
    compare_bone_controller.show_ui()
