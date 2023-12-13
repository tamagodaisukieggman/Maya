from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2.QtCore import QRegExp, Qt
from PySide2.QtGui import QIntValidator, QRegExpValidator
from PySide2.QtWidgets import QMainWindow

from . import settings
from .ui import main


class View(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.gui = main.Ui_MainWindow()
        self.gui.setupUi(self)

        self.settings = settings.LivelinkUtilitySettings()
        self.settings_control_ui = [
            self.gui.isRigAnimationCheckBox,
            self.gui.isMovieFIleCheckBox,
            self.gui.isWavFileCheckBox,
            self.gui.offsetFrame
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
