# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function

from .controller import DiffTextureSelectorController as TextureSelector


def show(*args):
    """TextureSelectorのGUI呼び出し"""
    global texture_selector_main_window
    try:
        texture_selector_main_window.close_ui()
    except Exception:
        pass

    texture_selector_main_window = TextureSelector()
    texture_selector_main_window.show_ui()


def get_view_controller(*args):
    diff_select_controller = TextureSelector()
    return diff_select_controller
