from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow

from .gui import actor_animation


class View(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.gui = actor_animation.Ui_MainWindow()
        self.gui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def save(self):
        ...

    def load(self):
        ...

    def showEvent(self, event):
        self.load()
        super(View, self).showEvent(event)

    def closeEvent(self, event):
        self.save()
        super(View, self).closeEvent(event)
