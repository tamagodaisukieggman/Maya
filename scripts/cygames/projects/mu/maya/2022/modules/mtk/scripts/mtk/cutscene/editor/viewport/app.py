# -*- coding: utf-8 -*-
"""Viewportに関連するロジック"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from functools import partial

from maya import cmds
from PySide2 import QtCore

from ... import utility
from mtk.cutscene import display_grid_drawer
from mtk.cutscene import custom_qt_headupdisplay

from . import const


# ============================================================
# 3Viewとpresp viewのfocus処理
# ============================================================
class ModelEditorEventRegister(object):
    def __init__(self, event_filter):
        self.model_editor = None
        self.event_filter = event_filter

    def set_event_filter(self):
        target_modelpanel = self.event_filter.name

        self.model_editor = utility.qt.convert_qwidget_from_modeleditor(target_modelpanel)

        self.model_editor.installEventFilter(self.event_filter)

    def remove_event_filter(self):
        self.model_editor.removeEventFilter(self.event_filter)


class ModelEditorFocusHolder(object):
    prev_focus = None

    def __init__(self, callback):
        self.persp_view = None
        self.cinematic_view = None
        self.camera_view = None
        self.edit_view = None
        self.callback = callback

    def create(self):
        cmds.scriptJob(conditionFalse=["busy", self.__create_holder], runOnce=True)

    def __create_holder(self):
        self.cinematic_view = ModelEditorEventRegister(ViewEventFilter(const.CINEMATIC_VIEWPORT_VIEW, self.callback))
        self.cinematic_view.set_event_filter()

        self.edit_view = ModelEditorEventRegister(ViewEventFilter(const.EDIT_VIEWPORT_VIEW, self.callback))
        self.edit_view.set_event_filter()

        self.camera_view = ModelEditorEventRegister(ViewEventFilter(const.CAMERA_VIEWPORT_VIEW, self.callback))
        self.camera_view.set_event_filter()

        self.persp_view = ModelEditorEventRegister(ViewEventFilter("Persp View", self.callback))
        self.persp_view.set_event_filter()

    def delete(self):
        self.persp_view.remove_event_filter()
        self.cinematic_view.remove_event_filter()
        self.camera_view.remove_event_filter()
        self.edit_view.remove_event_filter()

    @classmethod
    def get_prev_focus(cls):
        return ModelEditorFocusHolder.prev_focus


class ViewEventFilter(QtCore.QObject):
    """ModelEditor用ののQtEventFilter

    EventFilterで変換後渡す事でそのイベントを捕捉できる。
    """
    INTERVAL_MILLISECOND = 25

    def __init__(self, model_editor_name, resize_call_back):
        super(ViewEventFilter, self).__init__()

        self.name = cmds.getPanel(withLabel=model_editor_name)
        self.resize_call_back = resize_call_back

        self.__timer = QtCore.QTimer()
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(partial(self.resize_call_back, self.name))

    def eventFilter(self, widget, event):
        target_panel = self.name
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            ModelEditorFocusHolder.prev_focus = target_panel

        if event.type() == QtCore.QEvent.Resize:
            # ドラッグ中ずっと処理が入り、重たいので、指定ミリ秒操作がなかったらリフレッシュさせる
            self.__timer.start(self.INTERVAL_MILLISECOND)

        return False


class ViewGridDrawerManager(object):
    """グリッド描画管理クラス

    各Viewごとのグリッド表示/非表示
    """

    INTERVAL_MILLISECOND = 12

    def __init__(self):
        self.cinematic_view = None
        self.camera_view = None
        self.edit_view = None

        self.__refresh_timer = QtCore.QTimer()
        self.__refresh_timer.setSingleShot(True)
        self.__refresh_timer.timeout.connect(self.__refresh_grid_all_event)

    def initialize(self):
        cmds.scriptJob(conditionFalse=["busy", self.__initialize], runOnce=True)

    def __initialize(self):
        self.cinematic_view_qobject = utility.qt.convert_qwidget_from_modeleditor(const.CINEMATIC_VIEWPORT_VIEW)
        self.cinematic_view = display_grid_drawer.DisplayGridDrawer(const.CINEMATIC_VIEWPORT_VIEW, self.cinematic_view_qobject)

        self.camera_view_qobject = utility.qt.convert_qwidget_from_modeleditor(const.CAMERA_VIEWPORT_VIEW)
        self.camera_view = display_grid_drawer.DisplayGridDrawer(const.CAMERA_VIEWPORT_VIEW, self.camera_view_qobject)

        self.edit_view_qobject = utility.qt.convert_qwidget_from_modeleditor(const.EDIT_VIEWPORT_VIEW)
        self.edit_view = display_grid_drawer.DisplayGridDrawer(const.EDIT_VIEWPORT_VIEW, self.edit_view_qobject)

        persp_view_name = cmds.getPanel(withLabel="Persp View")
        self.persp_view_qobject = utility.qt.convert_qwidget_from_modeleditor(persp_view_name)
        self.persp_view = display_grid_drawer.DisplayGridDrawer(persp_view_name, self.persp_view_qobject)

    def get_drawer_from_view_name(self, name):
        if name == const.CINEMATIC_VIEWPORT_VIEW:
            return self.cinematic_view
        elif name == const.CAMERA_VIEWPORT_VIEW:
            return self.camera_view
        elif name == const.EDIT_VIEWPORT_VIEW:
            return self.edit_view
        elif name == cmds.getPanel(withLabel="Persp View"):
            return self.persp_view

    def delete(self):
        self.cinematic_view.grid_off()
        self.camera_view.grid_off()
        self.edit_view.grid_off()

    def refresh_grid(self, name):
        grid_drawer = self.get_drawer_from_view_name(name)
        if grid_drawer.is_grid_on:
            grid_drawer.grid_off()
            grid_drawer.grid_on()

    def refresh_grid_all(self):
        self.__refresh_timer.start(self.INTERVAL_MILLISECOND)

    def __refresh_grid_all_event(self):
        target_grid_views = [self.cinematic_view,
                             self.camera_view,
                             self.edit_view,
                             self.persp_view]

        for grid_view in target_grid_views:
            if grid_view.is_grid_on:
                grid_view.grid_off()
                grid_view.grid_on()


class ViewHUDManager(object):
    """CustomHUD管理クラス

    各ViewのCustomHUDを保有、表示/非表示
    """

    def __init__(self):
        self.cinematic_view_port_hud = custom_qt_headupdisplay.CustomHUDDrawer(const.CINEMATIC_VIEWPORT_VIEW)
        self.camera_view_port_hud = custom_qt_headupdisplay.CustomHUDDrawer(const.CAMERA_VIEWPORT_VIEW)
        self.edit_view_port_hud = custom_qt_headupdisplay.CustomHUDDrawer(const.EDIT_VIEWPORT_VIEW)

        persp_view_name = cmds.getPanel(withLabel="Persp View")
        self.persp_view_port_hud = custom_qt_headupdisplay.CustomHUDDrawer(persp_view_name)

    def toggle(self, target_view_name):

        if target_view_name == const.CINEMATIC_VIEWPORT_VIEW:
            self.cinematic_view_port_hud.toggle()
        elif target_view_name == const.CAMERA_VIEWPORT_VIEW:
            self.camera_view_port_hud.toggle()
        elif target_view_name == const.EDIT_VIEWPORT_VIEW:
            self.edit_view_port_hud.toggle()
        elif target_view_name == cmds.getPanel(withLabel="Persp View"):
            self.persp_view_port_hud.toggle()

    def delete_all(self):
        self.cinematic_view_port_hud.remove()
        self.camera_view_port_hud.remove()
        self.edit_view_port_hud.remove()
        self.persp_view_port_hud.remove()
