# -*- coding: utf-8 -*-
from __future__ import print_function

import os

import typing as tp

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin



# パスを指定
filePath = os.path.dirname(__file__).replace("\\", "/")
MAIN_UIFILEPATH = filePath + "/ui/main.ui"
TOOL_TITLE = "DiffSelector"
VERSION = "1.0.1"


class View(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    windowClosed = QtCore.Signal()
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setObjectName(TOOL_TITLE)
        self.setWindowTitle(TOOL_TITLE+":"+VERSION)

        # UIのパスを指定
        self.gui = QUiLoader().load(MAIN_UIFILEPATH)

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.gui)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def closeEvent(self, event):
        self.windowClosed.emit() 

