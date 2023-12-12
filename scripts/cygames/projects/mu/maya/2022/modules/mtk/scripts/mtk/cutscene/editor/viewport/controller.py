# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from . import view
from . import const
from .app import ModelEditorFocusHolder, ViewGridDrawerManager, ViewHUDManager


class ViewPortController(object):
    def __init__(self):
        self.view = None
        self.modeleditor_focus_holder = None
        self.view_grid_drawermanager = None
        self.view_hud_drawermanager = None

    def show_view_port(self):
        """エントリーポイント
        """

        self.view = view.View()
        self.view.show()

        self.view_grid_drawermanager = ViewGridDrawerManager()
        self.view_grid_drawermanager.initialize()

        self.view_hud_drawermanager = ViewHUDManager()

        self.modeleditor_focus_holder = ModelEditorFocusHolder(self.view_grid_drawermanager.refresh_grid)
        self.modeleditor_focus_holder.create()

    def close_view_port(self):
        if self.modeleditor_focus_holder is not None:
            self.modeleditor_focus_holder.delete()
            self.modeleditor_focus_holder = None

        if self.view_grid_drawermanager is not None:
            self.view_grid_drawermanager.delete()
            del self.view_grid_drawermanager

        if self.view_hud_drawermanager is not None:
            self.view_hud_drawermanager.delete_all()
            self.view_hud_drawermanager = None

        self.view.close()

    def get_cinematic_view_panel(self):
        return const.CINEMATIC_VIEWPORT_VIEW

    def get_edit_view_panel(self):
        return const.EDIT_VIEWPORT_VIEW

    def get_camera_view_panel(self):
        return const.CAMERA_VIEWPORT_VIEW

    def change_cutscene_layout(self):
        view.View.set_cutscene_layout()
