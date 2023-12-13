# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from mtk.cutscene import utility

from . import view


class CustomHUDDrawer(object):
    def __init__(self, view_name):
        self.view_name = view_name
        self.view_qobject = utility.qt.convert_qwidget_from_modeleditor(view_name)

        self.hud_widgets = None

    def add(self):
        self.hud_widgets = view.CustomHUD(self.view_name)
        self.hud_widgets.show()

        utility.mevent.MEventManager.add_event(self.view_name, self.hud_widgets.sync_geometry, event="idle")

        utility.mevent.MEventManager.add_user_event(self.view_name, self.hud_widgets.sync_focallength, event="ToggleCameraFocalLengthDragged")
        utility.mevent.MEventManager.add_event(self.view_name, self.hud_widgets.sync_focallength)

        utility.mevent.MEventManager.add_event(self.view_name, self.hud_widgets.sync_frame)
        utility.mevent.MEventManager.add_event(self.view_name, self.hud_widgets.sync_camera_sequencer_shot_name)
        utility.mevent.MEventManager.add_event(self.view_name, self.hud_widgets.sync_scene_name, event="SceneOpened")

    def remove(self):
        if not self.hud_widgets:
            return

        utility.mevent.MEventManager.remove_event(self.view_name)

        self.hud_widgets.deleteLater()

        self.hud_widgets = None

    def toggle(self):
        if self.hud_widgets:
            self.remove()
        else:
            self.add()
