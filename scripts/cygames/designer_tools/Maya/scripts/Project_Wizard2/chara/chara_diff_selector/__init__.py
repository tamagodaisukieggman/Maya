# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function
from .controller import DiffSelectController


def show(*args):
    global diff_select_controller
    try:
        diff_select_controller.close_ui()
    except Exception:
        pass
    diff_select_controller = DiffSelectController()
    diff_select_controller.show_ui()
