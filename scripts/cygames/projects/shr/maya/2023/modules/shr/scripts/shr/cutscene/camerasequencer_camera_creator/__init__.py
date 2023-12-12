# -*- coding: utf-8 -*-
"""カメラシーケンサー用のカメラ作成機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function


from . import app
from . import controller


def create(*args):
    """カメラを作成する
    """
    fake_controller = controller.SettingsViewController()
    settings = fake_controller.ui.load_in_dict()
    app.CutSceneCameraCreator(settings).duplicate()


def show_option(*args):
    """option起動のエントリーポイント
    """
    global cutscene_create_camera_setting_controller

    try:
        cutscene_create_camera_setting_controller.close_option()
    except Exception:
        pass
    cutscene_create_camera_setting_controller = controller.SettingsViewController()
    cutscene_create_camera_setting_controller.show_option()
