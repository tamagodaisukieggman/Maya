# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds

from .app import ModelEditorFocusHolder, ViewGridDrawerManager
from .controller import ViewPortController
from .const import *

# グローバルでカメラを保持する
# TODO: 堅牢性上げるなら、クラス化する
# cinematic_view_camera = None
edit_view_camera = None
camera_view_camera = None
default_view_camera = None


class CinematicViewPortInfo(object):
    def get_name(self):
        global CINEMATIC_VIEWPORT_VIEW

        return CINEMATIC_VIEWPORT_VIEW

    def get_camera(self):
        target_camera = cmds.modelPanel(self.get_name(), query=True, camera=True)
        return target_camera
