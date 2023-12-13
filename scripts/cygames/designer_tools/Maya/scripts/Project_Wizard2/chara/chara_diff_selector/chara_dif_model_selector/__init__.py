# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function
from .controller import DiffModelSelectController


def show(*args):
    global diff_model_select_controller
    try:
        print(diff_model_select_controller)
        diff_model_select_controller.close_ui()
    except Exception:
        pass
    diff_model_select_controller = DiffModelSelectController()
    diff_model_select_controller.show_ui()


def get_view_controller(*args):
    diff_model_select_controller = DiffModelSelectController()
    return diff_model_select_controller
