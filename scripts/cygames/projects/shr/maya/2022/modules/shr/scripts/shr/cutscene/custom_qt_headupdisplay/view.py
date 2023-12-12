# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
from PySide2 import QtWidgets
from PySide2 import QtCore

# API1.0
from maya import OpenMayaUI
from maya import cmds

import shiboken2

from .ui import custom_hud

from shr.cutscene import utility
from shr.utils import getCurrentSceneFilePath


class CustomHUD(QtWidgets.QMainWindow):
    def __init__(self, target_view):
        self.target_view = target_view
        self.model_panel_qobject = utility.qt.convert_qwidget_from_modeleditor(target_view)

        ptr = OpenMayaUI.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

        super(CustomHUD, self).__init__(parent)

        self.gui = custom_hud.Ui_MainWindow()
        self.gui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen)

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.initialize_sync_event()

    def initialize_sync_event(self):
        self.sync_geometry()
        self.sync_frame()
        self.sync_focallength()
        self.sync_camera_sequencer_shot_name()
        self.sync_scene_name()

    def event(self, event):
        if event is None:
            return
        super(CustomHUD, self).event(event)

        what_type = event.type()
        if what_type != QtCore.QEvent.DeferredDelete and what_type != QtCore.QEvent.Close:
            self.model_panel_qobject.event(event)

        return False

    def sync_frame(self, *args):
        current_time = cmds.currentTime(query=True)
        self.gui.frameText.setText(str(current_time))

    def sync_geometry(self, *args):

        world_pos = self.model_panel_qobject.mapToGlobal(self.model_panel_qobject.pos())

        target_widget_width = self.model_panel_qobject.width()
        target_widget_height = self.model_panel_qobject.height()

        self.setGeometry(world_pos.x(), world_pos.y(), target_widget_width, target_widget_height)
        self.setFixedSize(target_widget_width, target_widget_height)

    def sync_focallength(self, *args):
        view_camera = cmds.modelPanel(self.target_view, query=True, camera=True)
        view_camera_shapes = cmds.listRelatives(view_camera, shapes=True)[0]
        focal_length = cmds.getAttr(view_camera_shapes + ".focalLength")

        self.gui.forcalLength.setText(str(focal_length) + "mm")

    def sync_camera_sequencer_shot_name(self, *args):
        view_camera = cmds.modelPanel(self.target_view, query=True, camera=True)

        hit_name = False
        shot_list = cmds.sequenceManager(listShots=True)

        if shot_list:
            for shot_name in shot_list:
                shot_camera = cmds.shot(shot_name, query=True, currentCamera=True)
                if view_camera == shot_camera:
                    self.gui.cutName.setText(shot_name)
                    hit_name = True

        if not hit_name:
            self.gui.cutName.setText("")

    def sync_scene_name(self, *args):
        scene_name = os.path.splitext(os.path.basename(getCurrentSceneFilePath()))[0]
        self.gui.sceneName.setText(scene_name)
