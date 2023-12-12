# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function
from . import controller


def rename(*args):
    """カメラを作成する
    """
    fake_controller = controller.ViewController()
    settings = fake_controller.ui.load_in_dict()

    fake_controller.exec_rename(settings["shotName"], settings["shotNumber"], settings["is_rename_camera"])


def show_option(*args):
    """option起動のエントリーポイント
    """

    global cutscene_shot_renamer_controller

    try:
        cutscene_shot_renamer_controller.close_option()
    except Exception:
        pass
    cutscene_shot_renamer_controller = controller.ViewController()
    cutscene_shot_renamer_controller.show_option()
