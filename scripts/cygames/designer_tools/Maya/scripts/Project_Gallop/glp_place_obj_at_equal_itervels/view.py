# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin

from .ui import glp_place_obj_at_equal_itervals_window as ui_window


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(View, self).__init__(parent)
        self.ui = ui_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.close_event_exec = None

    def closeEvent(self, event):

        if self.close_event_exec is not None:
            self.close_event_exec()

        self.deleteLater()
        super(View, self).closeEvent(event)
