
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

Tool_Name = "Edge_Set_Editor"
UI_PATH = os.path.dirname(__file__) + "/ui"

class View(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        loader = QUiLoader()
        uiFilePath = os.path.join(UI_PATH, "main.ui")
        self.gui = loader.load(uiFilePath)
        self.setCentralWidget(self.gui)
        self.setWindowTitle(Tool_Name)
        self.setObjectName(Tool_Name)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
