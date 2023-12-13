# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Qt, QRegExp
from PySide2.QtGui import QIntValidator, QRegExpValidator

from .ui import CreateCameraOption

from . import settings


class View(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.gui = CreateCameraOption.Ui_MainWindow()
        self.gui.setupUi(self)

        self.gui.shotNumber.setValidator(QIntValidator())

        rx = QRegExpValidator(QRegExp("\\w+"))
        self.gui.shotName.setValidator(rx)
        self.gui.cameraGroup.setValidator(rx)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.settings = settings.CreateCameraSettings()
        self.settings_control_ui = [
            self.gui.cameraGroup,
            self.gui.shotName,
            self.gui.shotNumber,
            self.gui.shotPlacement,
            self.gui.cameraType,
            self.gui.startTime,
            self.gui.endTime
        ]

    def save(self):
        self.settings.save_geometry(self)
        self.settings.save_settings(self.settings_control_ui)

    def load(self):
        self.settings.load_geometry(self)
        self.settings.load_settings(self.settings_control_ui)

    def load_in_dict(self):
        return self.settings.load_in_dict(self.settings_control_ui)

    def showEvent(self, event):
        self.load()
        super(View, self).showEvent(event)

    def closeEvent(self, event):
        self.save()
        super(View, self).closeEvent(event)
