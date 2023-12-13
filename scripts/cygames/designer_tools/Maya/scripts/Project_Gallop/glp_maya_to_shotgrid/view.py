# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PySide2 import QtCore, QtWidgets
from maya.app.general import mayaMixin

from .ui import shotgun_tool_window, shotgrid_login_dialog


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(View, self).__init__(parent)
        self.ui = shotgun_tool_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.close_event_exec = None

    def closeEvent(self, event):

        if self.close_event_exec is not None:
            self.close_event_exec()

        self.deleteLater()
        super(View, self).closeEvent(event)


class ShotgridLoginDialog(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QDialog):
    """[summary]
    """

    def __init__(self, parent=None):

        super(ShotgridLoginDialog, self).__init__(parent)
        self.ui = shotgrid_login_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.close_event_exec = None

    def closeEvent(self, event):

        if self.close_event_exec is not None:
            self.close_event_exec()
        super(ShotgridLoginDialog, self).closeEvent(event)


class CaptureWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """[summary]
    """

    def __init__(self, _parent=None):

        super(CaptureWindow, self).__init__(_parent)
        self.setWindowOpacity(0.6)
        self.setGeometry(300, 300, 200, 150)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self.__setupButton()
        self.__setupBox()
        self.statusBar()

        self.__isDrag = False
        self.__startPos = QtCore.QPoint(0, 0)

        self.close_event_exec = None

    def __setupButton(self):

        closeButton = QtWidgets.QPushButton("Close", self)
        closeButton.clicked.connect(self.close)
        closeButton.move(20, 20)

        self.captureButton = QtWidgets.QPushButton("Capture", self)
        self.captureButton.move(20, 50)

    def __setupBox(self):

        self.width_label = QtWidgets.QLabel(self)
        self.width_label.setObjectName("width_label")
        self.width_label.setText('width')
        self.width_label.move(20, 80)

        self.width_spinbox = QtWidgets.QSpinBox(self)
        self.width_spinbox.setMaximum(10000)
        self.width_spinbox.setProperty("value", 256)
        self.width_spinbox.setObjectName("width_spinbox")
        self.width_spinbox.setSingleStep(10)
        self.width_spinbox.move(60, 80)
        self.width_spinbox.editingFinished.connect(self.__setSize)

        self.height_label = QtWidgets.QLabel(self)
        self.height_label.setObjectName("height_label")
        self.height_label.setText('height')
        self.height_label.move(20, 110)

        self.height_spinbox = QtWidgets.QSpinBox(self)
        self.height_spinbox.setMaximum(10000)
        self.height_spinbox.setProperty("value", 256)
        self.height_spinbox.setObjectName("height_spinbox")
        self.height_spinbox.setSingleStep(10)
        self.height_spinbox.move(60, 110)
        self.height_spinbox.editingFinished.connect(self.__setSize)

    def __setSize(self):

        width = self.width_spinbox.value()
        height = self.height_spinbox.value()

        self.resize(width, height)

    def resizeEvent(self, event):

        self.width_spinbox.setValue(event.size().width())
        self.height_spinbox.setValue(event.size().height())
        super(CaptureWindow, self).resizeEvent(event)

    def closeEvent(self, event):

        if self.close_event_exec is not None:
            self.close_event_exec()
        super(CaptureWindow, self).closeEvent(event)

    def moveEvent(self, e):

        super(CaptureWindow, self).moveEvent(e)

    def mousePressEvent(self, event):

        self.__isDrag = True
        self.__startPos = event.pos()
        super(CaptureWindow, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        self.__isDrag = False
        super(CaptureWindow, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):

        if self.__isDrag:
            self.move(self.mapToParent(event.pos() - self.__startPos))

        super(CaptureWindow, self).mouseMoveEvent(event)
