# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin

from . import glp_timewarp_baker_window_pyside2 as ui_window

reload(ui_window)


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
