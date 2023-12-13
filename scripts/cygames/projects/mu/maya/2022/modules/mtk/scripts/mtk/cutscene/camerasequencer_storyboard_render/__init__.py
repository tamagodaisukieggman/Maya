# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya.utils import executeDeferred
from maya import cmds


from . import controller, render


def show_option(*args):
    """option起動のエントリーポイント
    """

    global storyboard_render_controller

    try:
        storyboard_render_controller.close_option()
    except Exception:
        pass
    storyboard_render_controller = controller.ViewController()
    storyboard_render_controller.show_option()

    executeDeferred(add_refresh_event)
    add_refresh_event()


def add_refresh_event():
    cmds.scriptJob(event=["PostSceneRead", show_option], parent="StoryboardPatchRenderWindow")


def refresh(*args):
    show_option()


def start_current_frame_render(*args):
    fake_view = controller.ViewController()
    settings = fake_view.ui.load_in_dict()
    render.ArnoldDebugRender.render(settings)
