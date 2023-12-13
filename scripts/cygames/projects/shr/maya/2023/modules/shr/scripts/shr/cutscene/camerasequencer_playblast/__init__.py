# -*- coding: utf-8 -*-
"""カメラシーケンサー用のプレイブラスト機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function
from . import app
from . import controller
from . import view


def start_playblast(target_view, *args):
    fake_view = view.View()
    settings = fake_view.load_in_dict()
    ins = app.CutScenePlayBlastExecutor(target_view, settings)

    ins.start_playblast()


def show_playblast_option(target_view, *args):
    global cutscene_start_playblast_setting_controller

    try:
        cutscene_start_playblast_setting_controller.close_option()
    except Exception:
        pass
    cutscene_start_playblast_setting_controller = controller.SettingsViewController(target_view)
    cutscene_start_playblast_setting_controller.show_option()
